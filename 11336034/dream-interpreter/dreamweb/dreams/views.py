import json
import os
from dotenv import load_dotenv
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,logout
from openai import OpenAI  # 導入 OpenAI SDK
from .forms import DreamForm, UserRegisterForm
import logging
from django.http import HttpResponse
from django.http import JsonResponse
import random  # 模擬 AI 建議，可替換為 NLP 分析
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from .models import Dream,DreamPost,DreamComment,DreamTag,DreamPost,DreamTrend,DreamRecommendation
from django.db.models import Count,Q
from django.utils import timezone
import jieba  # 中文分詞庫
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize


def welcome_page(request):
    return render(request, 'dreams/welcome.html')


# 登入介面導向首頁
class CustomLoginView(LoginView):
    template_name = 'dreams/login.html'

    def get_redirect_url(self):
        redirect_to = self.request.GET.get('next', None)
        return redirect_to if redirect_to else '/dream_form/'  # 預設導向儀表板

# 登出介面導向首頁
def logout_view(request):
    if request.method == "POST" or request.method == "GET":  # 支援 GET 和 POST
        logout(request)
        return redirect('logout_success')  # 重定向到登出成功頁面
    else:
        return HttpResponseForbidden("Invalid request method.")

def logout_success(request):
    return render(request, 'dreams/logout_success.html')  # 顯示登出成功頁面

class EmotionAnalyzer:
    def __init__(self, dreams):
        self.dreams = dreams
    
    def calculate_stress_index(self):
        """
        計算壓力指數
        根據夢境內容的情緒關鍵詞和頻率進行評估
        """
        stress_keywords = [
            '焦慮', '恐懼', '壓力', '逃避', '失落', 
            '被追', '無助', '困境', '迷茫'
        ]
        
        total_stress_score = 0
        for dream in self.dreams:
            keyword_count = sum(
                keyword in dream.dream_content for keyword in stress_keywords
            )
            total_stress_score += keyword_count
        
        # 計算平均壓力指數
        stress_index = (total_stress_score / len(self.dreams)) * 10 if self.dreams else 0
        return min(stress_index, 100)  # 限制在0-100範圍
    
    def generate_health_recommendations(self, stress_index):
        """
        根據壓力指數生成個人化建議
        """
        recommendations = {
            (0, 30): [
                "目前壓力水平正常，保持良好的生活習慣",
                "繼續進行日常放鬆活動"
            ],
            (30, 60): [
                "壓力水平略高，建議增加放鬆活動",
                "嘗試冥想或瑜伽",
                "確保充足睡眠"
            ],
            (60, 80): [
                "壓力指數偏高，需要積極調節",
                "建議諮詢心理輔導師",
                "減少工作負荷",
                "每週安排運動時間"
            ],
            (80, 100): [
                "壓力水平嚴重，強烈建議尋求專業幫助",
                "立即調整生活作息",
                "考慮心理諮詢",
                "可能需要短期休假"
            ]
        }
        
        for (low, high), recs in recommendations.items():
            if low <= stress_index < high:
                return recs
        
        return ["建議尋求專業心理諮詢"]

# 夢境儀表板
def dream_dashboard(request):
    dreams = Dream.objects.filter(user=request.user)
    analyzer = EmotionAnalyzer(dreams)
    stress_index = analyzer.calculate_stress_index()
    recommendations = analyzer.generate_health_recommendations(stress_index)
    
    return render(request, 'dreams/dream_dashboard.html', {
        'dreams': dreams,
        'stress_index': stress_index,
        'recommendations': recommendations
    })

# 載入環境變量
load_dotenv()
# DEEPSEEK_API_KEY = os.getenv("sk-b1e7ea9f25184324aaa973412b081f6f")  # 修正為正確的環境變量名稱

# 初始化 OpenAI 客戶端
client = OpenAI(api_key="sk-b1e7ea9f25184324aaa973412b081f6f", base_url="https://api.deepseek.com")

# 註冊
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '註冊成功！您現在已登入。')
            return redirect('dream_form')
    else:
        form = UserRegisterForm()
    return render(request, 'dreams/register.html', {'form': form})


@login_required
def dream_form(request):
    if request.method == 'POST':
        form = DreamForm(request.POST)
        if form.is_valid():
            dream_content = form.cleaned_data['dream_content']
            interpretation, emotions = interpret_dream(dream_content)

            if emotions:
                dream = Dream(
                    user=request.user,
                    dream_content=dream_content,
                    interpretation=interpretation,
                    anxiety=emotions["焦慮"],
                    fear=emotions["恐懼"],
                    surprise=emotions["驚奇"],
                    hope=emotions["希望"],
                    confusion=emotions["困惑"]
                )
                dream.save()

                return render(request, 'dreams/dream_result.html', {'dream': dream})

    else:
        form = DreamForm()

    dreams = Dream.objects.filter(user=request.user)
    return render(request, 'dreams/dream_form.html', {'form': form, 'dreams': dreams})


import time
import logging
import re
import openai

def interpret_dream(dream_content, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一位專業的解夢專家，請解析夢境情緒並輸出格式如下：\n"
                                                  "1. 焦慮 X%\n"
                                                  "2. 恐懼 Y%\n"
                                                  "3. 驚奇 Z%\n"
                                                  "4. 希望 A%\n"
                                                  "5. 困惑 B%\n"
                                                  "AI 解析的關鍵字\n"
                                                  "夢境象徵的意義請以專業且具深度的方式解析\n"
                                                  "用以上資訊提供一個詳細的心理診斷個人化建議"},
                    {"role": "user", "content": dream_content}
                ],
                temperature=0.7,
                stream=False,
                #timeout=timeout  # 設定 API 請求超時時間
            )
            interpretation = response.choices[0].message.content
            break  # 如果請求成功，就跳出重試迴圈

        except openai.APITimeoutError:
            logging.warning(f"API 超時，正在重試...（第 {attempt + 1} 次）")
            time.sleep(2)  # 等待 2 秒再重試
            if attempt == max_retries - 1:
                return "API 超時，請稍後再試。", None  # 如果超過最大重試次數，返回錯誤訊息
        except Exception as e:
            logging.error(f"API 請求失敗: {str(e)}", exc_info=True)
            return f"API 請求失敗: {str(e)}", None

    # **解析數據**
    emotions = {"焦慮": 0, "恐懼": 0, "驚奇": 0, "希望": 0, "困惑": 0}

    for line in interpretation.split("\n"):
        match = re.search(r"(\S+)\s(\d+)%", line)
        if match:
            emotion, value = match.groups()
            emotion = emotion.strip()
            if emotion in emotions:
                emotions[emotion] = float(value)  # 確保數值正確解析

    print(f"解析後的情緒百分比：{emotions}")  # 偵錯輸出
    return interpretation, emotions


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Dream

@login_required
def get_emotion_data(request):
    # 取得當前登入用戶的最近 7 筆夢境數據
    dreams = Dream.objects.filter(user=request.user).order_by('-created_at')[:7]
    
    labels = [dream.created_at.strftime('%Y-%m-%d') for dream in dreams[::-1]]
    anxiety_data = [dream.anxiety for dream in dreams[::-1]]
    fear_data = [dream.fear for dream in dreams[::-1]]
    surprise_data = [dream.surprise for dream in dreams[::-1]]
    hope_data = [dream.hope for dream in dreams[::-1]]
    confusion_data = [dream.confusion for dream in dreams[::-1]]

    data = {
        "labels": labels,
        "datasets": [
            {"label": "焦慮指數", "data": anxiety_data, "borderColor": "rgba(255, 99, 132, 1)", "fill": False},
            {"label": "恐懼指數", "data": fear_data, "borderColor": "rgba(255, 159, 64, 1)", "fill": False},
            {"label": "驚奇指數", "data": surprise_data, "borderColor": "rgba(54, 162, 235, 1)", "fill": False},
            {"label": "希望指數", "data": hope_data, "borderColor": "rgba(75, 192, 192, 1)", "fill": False},
            {"label": "困惑指數", "data": confusion_data, "borderColor": "rgba(153, 102, 255, 1)", "fill": False},
        ]
    }
    return JsonResponse(data)


# 夢境歷史
@login_required
def dream_history(request):
    dreams = Dream.objects.filter(user=request.user)
    return render(request, 'dreams/dream_history.html', {'dreams': dreams})

# 夢境詳情
@login_required
def dream_detail(request, dream_id):
    try:
        # 嘗試根據夢境 ID 查找夢境
        dream = Dream.objects.get(id=dream_id, user=request.user)
        # 返回帶有夢境詳情的模板
        return render(request, 'dreams/dream_detail.html', {'dream': dream})
    except Dream.DoesNotExist:
        # 如果找不到夢境，顯示錯誤消息並重定向
        messages.error(request, '找不到指定的夢境記錄')
        return redirect('dream_history')

def get_dream_detail(request, dream_id):
    dream = get_object_or_404(Dream, id=dream_id)
    return JsonResponse({
        "created_at": dream.created_at.strftime("%Y-%m-%d %H:%M"),
        "dream_content": dream.dream_content,
        "interpretation": dream.interpretation
    })


# 夢境心理健康診斷建議
@login_required
def mental_health_dashboard(request):
    # 取得當前使用者的夢境歷史（按時間倒序排列）
    dreams = Dream.objects.filter(user=request.user).order_by('-created_at')[:5]  # 只顯示最近 5 筆夢境
    return render(request, 'dreams/mental_health_dashboard.html', {'dreams': dreams})


@login_required
def get_mental_health_suggestions(request, dream_id):
    try:
        dream = Dream.objects.get(id=dream_id, user=request.user)
        print(f"找到夢境: {dream.dream_content}")  # 確保夢境存在

        suggestions = {
            "焦慮": "您的夢境顯示焦慮，建議冥想或散步放鬆。",
            "壓力": "您的夢境顯示壓力過大，建議適當休息。",
            "恐懼": "夢境顯示恐懼感，建議多與人交流舒緩。",
            "探索": "夢境顯示好奇心，建議學習新事物。",
        }
        
        dream_keywords = ["焦慮", "壓力", "恐懼", "探索"]
        selected_suggestion = random.choice(dream_keywords)
        suggestion_text = suggestions[selected_suggestion]

        return JsonResponse({"suggestions": suggestion_text})
    
    except Dream.DoesNotExist:
        print("夢境不存在")
        return JsonResponse({"error": "夢境不存在"}, status=404)



# 1. 社群主頁和全球夢境趨勢
def community(request):
    """夢境社群主頁"""
    # 獲取熱門夢境
    popular_dreams = DreamPost.objects.order_by('-view_count')[:10]
    
    # 獲取最新夢境趨勢
    try:
        latest_trend = DreamTrend.objects.latest('date')
        trend_data = latest_trend.trend_data
    except DreamTrend.DoesNotExist:
        trend_data = {}
    
    return render(request, 'dreams/community.html', {
        'popular_dreams': popular_dreams,
        'trend_data': trend_data
    })

def dream_community(request):
    # 獲取今日熱門夢境趨勢
    trend_data = DreamTrend.objects.filter(date=timezone.now().date()).first()
    if trend_data:
        trend_data = json.loads(trend_data.trend_data)  # 將 JSON 字符串解析為字典
    else:
        trend_data = {}

    # 按次數降序排序，並且只取前 8 個
    top_8_trend_data = dict(sorted(trend_data.items(), key=lambda item: item[1], reverse=True)[:8])

    # 將資料傳遞給模板
    context = {
        'trend_data': top_8_trend_data,  # 傳遞已排序並限制為 8 條的資料
    }

    return render(request, 'dreams/community.html', context)

# 2. 匿名夢境分享
@login_required
def share_dream(request):
    """分享夢境到社群"""
    if request.method == 'POST':
        content = request.POST.get('content')
        title = request.POST.get('title')
        is_anonymous = request.POST.get('is_anonymous', False) == 'on'
        tags = request.POST.getlist('tags')
        
        # 創建夢境貼文
        dream_post = DreamPost(
            user=request.user if not is_anonymous else None,
            content=content,
            title=title,
            is_anonymous=is_anonymous,
        )
        dream_post.save()
        
        # 添加標籤
        for tag_name in tags:
            tag, created = DreamTag.objects.get_or_create(name=tag_name)
            dream_post.tags.add(tag)
        
        messages.success(request, '夢境已成功分享到社群！')
        return redirect('dream_post_detail', post_id=dream_post.id)
    
    # 獲取常用標籤供選擇
    popular_tags = DreamTag.objects.annotate(
        usage_count=Count('dreampost')
    ).order_by('-usage_count')[:20]
    
    return render(request, 'dreams/share_dream.html', {
        'popular_tags': popular_tags
    })

# 3. 夢境搜索功能
def search_dreams(request):
    """搜索夢境"""
    query = request.GET.get('q', '')
    tag = request.GET.get('tag', '')
    
    dreams = DreamPost.objects.all()
    
    if query:
        dreams = dreams.filter(
            Q(content__icontains=query) | 
            Q(title__icontains=query)
        )
    
    if tag:
        dreams = dreams.filter(tags__name=tag)
    
    return render(request, 'dreams/search_results.html', {
        'dreams': dreams,
        'query': query,
        'tag': tag
    })

# 4. 夢境詳情頁與評論功能
def dream_post_detail(request, post_id):
    """夢境貼文詳情頁"""
    dream_post = get_object_or_404(DreamPost, id=post_id)
    
    # 增加瀏覽次數
    dream_post.increase_view_count()
    
    # 獲取評論
    comments = dream_post.comments.all()
    
    # 獲取相似夢境推薦
    similar_dreams = get_similar_dreams(dream_post)
    
    # 處理評論提交
    if request.method == 'POST' and request.user.is_authenticated:
        comment_content = request.POST.get('comment')
        if comment_content:
            DreamComment.objects.create(
                dream_post=dream_post,
                user=request.user,
                content=comment_content
            )
            messages.success(request, '評論已提交！')
            return redirect('dream_post_detail', post_id=post_id)
    
    return render(request, 'dreams/dream_post_detail.html', {
        'dream': dream_post,
        'comments': comments,
        'similar_dreams': similar_dreams
    })

# 5. 夢境推薦系統
def get_similar_dreams(dream_post, limit=5):
    """獲取相似夢境推薦"""
    # 基於標籤的推薦
    if dream_post.tags.exists():
        tag_based = DreamPost.objects.filter(
            tags__in=dream_post.tags.all()
        ).exclude(id=dream_post.id).distinct()[:limit]
        return tag_based
    
    # 如果沒有標籤，返回熱門夢境
    return DreamPost.objects.exclude(id=dream_post.id).order_by('-view_count')[:limit]


# 6. 生成並更新全球夢境趨勢
def update_dream_trends():
    """更新夢境趨勢數據 (建議通過定時任務每天運行)"""    
    today = timezone.now().date()
    
    # 獲取過去24小時的夢境
    time_threshold = timezone.now() - timezone.timedelta(hours=24)
    recent_dreams = DreamPost.objects.filter(created_at__gte=time_threshold)
    
    # 提取關鍵詞 (這裡使用簡單的分詞和計數，可以替換為更複雜的關鍵詞提取算法)
    all_words = []
    for dream in recent_dreams:
        # 中文分詞
        words = jieba.cut(dream.content)
        all_words.extend(list(words))
    
    # 過濾停用詞 (需要自定義停用詞表)
    stopwords = ['的', '是', '了', '在', '和', '我']  # 示例停用詞
    filtered_words = [word for word in all_words if word not in stopwords and len(word) > 1]
    
    # 統計詞頻
    word_counts = Counter(filtered_words)
    top_keywords = dict(word_counts.most_common(20))
    
    # 保存趨勢數據
    trend, created = DreamTrend.objects.get_or_create(
        date=today,
        defaults={'trend_data': top_keywords}
    )
    
    if not created:
        trend.trend_data = top_keywords
        trend.save()
