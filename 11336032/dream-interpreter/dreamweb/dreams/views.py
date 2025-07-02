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
from .models import Dream,DreamPost,DreamComment,DreamTag,DreamPost,DreamTrend,DreamRecommendation,Counselor
from django.db.models import Count,Q
from django.utils import timezone
import jieba  # 中文分詞庫
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
# 歷史分頁
from django.core.paginator import Paginator
# 新聞相關
import time
import re
import openai
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# 語音相關
import speech_recognition as sr
from .utils import convert_to_wav
from pydub import AudioSegment
import io

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

# 將音檔轉換為 WAV 格式
# 音檔轉換函數
def convert_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file)
    wav_audio = io.BytesIO()
    audio.export(wav_audio, format='wav')
    wav_audio.seek(0)
    return wav_audio

# 夢境解析
@login_required
def dream_form(request):
    dream_content = ""  # 預設夢境內容
    error_message = None

    if request.method == 'POST':
        form = DreamForm(request.POST, request.FILES)

        # 檢查是否有上傳音檔並處理
        audio_file = request.FILES.get('audio_file')
        if audio_file:
            try:
                # 將音檔轉換為 WAV 格式
                wav_audio = convert_to_wav(audio_file)

                recognizer = sr.Recognizer()

                # 使用語音識別
                with sr.AudioFile(wav_audio) as source:
                    audio = recognizer.record(source)
                    try:
                        dream_content = recognizer.recognize_google(audio, language="zh-TW")  # 設定中文
                    except sr.UnknownValueError:
                        error_message = "無法識別音檔內容，請再試一次。"
                    except sr.RequestError:
                        error_message = "語音識別服務無法訪問，請稍後重試。"
            except Exception as e:
                error_message = f"音檔處理錯誤: {e}"

        # 使用者可以修改夢境內容
        if form.is_valid():
            dream_content = form.cleaned_data.get('dream_content', dream_content)  # 確保語音識別後的內容能顯示在表單中

            # 進行夢境解析
            interpretation, emotions, mental_health_advice = interpret_dream(dream_content)

            if emotions:
                dream = Dream(
                    user=request.user,
                    dream_content=dream_content,
                    interpretation=interpretation,
                    Happiness=emotions.get("快樂", 0),
                    Anxiety=emotions.get("焦慮", 0),
                    Fear=emotions.get("恐懼", 0),
                    Excitement=emotions.get("興奮", 0),
                    Sadness=emotions.get("悲傷", 0)
                )
                dream.save()

                return render(request, 'dreams/dream_result.html', {
                    'dream': dream,
                    'mental_health_advice': mental_health_advice  # 傳遞心理診斷建議
                })

    else:
        form = DreamForm()

    dreams = Dream.objects.filter(user=request.user)
    # 把夢境內容帶入表單，確保語音識別結果能顯示
    return render(request, 'dreams/dream_form.html', {
        'form': form,
        'dream_content': dream_content,
        'error_message': error_message,
        'dreams': dreams,
    })

# 音檔並轉換為文字
def upload_audio(request):
    """接收音檔並轉換為文字"""
    if request.method == "POST" and request.FILES.get("audio_file"):
        audio_file = request.FILES["audio_file"]
        try:
            # 轉換音檔格式
            wav_audio = convert_to_wav(audio_file)
            recognizer = sr.Recognizer()

            # 語音轉文字
            with sr.AudioFile(wav_audio) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language="zh-TW")  # 中文識別

            return JsonResponse({"success": True, "dream_content": text})

        except sr.UnknownValueError:
            return JsonResponse({"success": False, "error": "無法識別音檔內容"})

        except sr.RequestError:
            return JsonResponse({"success": False, "error": "語音識別服務無法訪問"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "未收到音檔"})

# API
def interpret_dream(dream_content, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一位專業的解夢專家，請解析夢境意義並輸出格式如下：\n"
                                                  "1. 快樂 X%\n"
                                                  "2. 焦慮 Y%\n"
                                                  "3. 恐懼 Z%\n"
                                                  "4. 興奮 A%\n"
                                                  "5. 悲傷 B%\n"
                                                  "夢境關鍵字:\n"
                                                  "夢境象徵的意義請以專業且具深度的方式詳細解析\n"
                                                  "以上解析裡不要出現＊或**符號，且不用給我建議"},
                    {"role": "user", "content": dream_content}
                ],
                temperature=0.7,
                stream=False,
            )
            interpretation = response.choices[0].message.content
            break  

        except openai.APITimeoutError:
            logging.warning(f"API 超時，正在重試...（第 {attempt + 1} 次）")
            time.sleep(2)
            if attempt == max_retries - 1:
                return "API 超時，請稍後再試。", None, None  
        except Exception as e:
            logging.error(f"API 請求失敗: {str(e)}", exc_info=True)
            return f"API 請求失敗: {str(e)}", None, None  

    # **解析數據**
    emotions = {"快樂": 0, "焦慮": 0, "恐懼": 0, "興奮": 0, "悲傷": 0}
    mental_health_advice = ""

    for line in interpretation.split("\n"):
        match = re.search(r"(\S+)\s(\d+)%", line)
        if match:
            emotion, value = match.groups()
            emotion = emotion.strip()
            if emotion in emotions:
                emotions[emotion] = float(value)

    # 擷取心理診斷個人化建議
    advice_match = re.search(r"心理診斷建議:\s*(.*)", interpretation, re.DOTALL)
    if advice_match:
        mental_health_advice = advice_match.group(1).strip()

    return interpretation, emotions, mental_health_advice



# 夢境儀表板
@login_required
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

# 個人關鍵字
def get_user_keywords(request):
    user = request.user  # 獲取當前登錄的用戶
    dreams = Dream.objects.filter(user=user)  # 獲取該用戶的所有夢境
    all_words = []

    # 中文分詞處理夢境內容
    for dream in dreams:
        content = dream.dream_content
        words = jieba.cut(content)  # 用 jieba 分詞
        all_words.extend(list(words))  # 收集所有分詞

    # 過濾停用詞
    stopwords = ['的', '是', '了', '在', '和', '我']  # 示例停用詞
    filtered_words = [word for word in all_words if word not in stopwords and len(word) > 1]  # 過濾停用詞及過短的字

    # 統計詞頻
    word_counts = Counter(filtered_words)  # 計算每個詞出現的頻率
    top_keywords = dict(word_counts.most_common(8))  # 取前8個最常出現的詞

    # 返回JSON數據，包含關鍵字及其頻率
    result = [{"keyword": key, "count": value} for key, value in top_keywords.items()]
    return JsonResponse(result, safe=False)  # 返回 JSON 格式的結果

# 熱門關鍵字
def get_global_trends_data(request):
    """返回所有過去的夢境趨勢資料，並合併成一個總圖"""
    trend_entries = DreamTrend.objects.all()  # 獲取所有趨勢資料

    if trend_entries:
        all_trends = {}
        for trend_entry in trend_entries:
            trend_dict = trend_entry.trend_data  # 假設 trend_data 是字典
            # 將每一天的趨勢數據合併
            for keyword, percentage in trend_dict.items():
                if keyword in all_trends:
                    all_trends[keyword] += percentage
                else:
                    all_trends[keyword] = percentage

        # 將合併後的數據按比例排序，並取前 8 條
        top_8 = sorted(all_trends.items(), key=lambda x: x[1], reverse=True)[:8]
        trend_data = [{'text': k, 'percentage': v} for k, v in top_8]
    else:
        trend_data = []

    return JsonResponse(trend_data, safe=False)

# 最近 7 筆夢境數據
def get_emotion_data(request):
    # 取得當前登入用戶的最近 7 筆夢境數據
    dreams = Dream.objects.filter(user=request.user).order_by('-created_at')[:7]
    
    labels = [dream.created_at.strftime('%Y-%m-%d') for dream in dreams[::-1]]
    Happiness_data = [dream.Happiness for dream in dreams[::-1]]
    Anxiety_data = [dream.Anxiety for dream in dreams[::-1]]
    Fear_data = [dream.Fear for dream in dreams[::-1]]
    Excitement_data = [dream.Excitement for dream in dreams[::-1]]
    Sadness_data = [dream.Sadness for dream in dreams[::-1]]

    data = {
        "labels": labels,
        "datasets": [
            {"label": "快樂指數", "data": Happiness_data, "borderColor": "rgba(255, 99, 132, 1)", "fill": False},
            {"label": "焦慮指數", "data": Anxiety_data, "borderColor": "rgba(255, 159, 64, 1)", "fill": False},
            {"label": "恐懼指數", "data": Fear_data, "borderColor": "rgba(54, 162, 235, 1)", "fill": False},
            {"label": "興奮指數", "data": Excitement_data, "borderColor": "rgba(75, 192, 192, 1)", "fill": False},
            {"label": "悲傷指數", "data": Sadness_data, "borderColor": "rgba(153, 102, 255, 1)", "fill": False},
        ]
    }
    return JsonResponse(data)


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


# 夢境歷史
@login_required
def dream_history(request):
    query = request.GET.get('q')  # 取得搜尋文字
    dreams = Dream.objects.filter(user=request.user)

    if query:
        dreams = dreams.filter(Q(dream_content__icontains=query) | Q(interpretation__icontains=query))

    paginator = Paginator(dreams.order_by('-created_at'), 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dreams/dream_history.html', {
        'page_obj': page_obj,
        'query': query,  # 回傳到前端顯示搜尋欄的值
    })

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
        "interpretation": dream.interpretation,
    })


# 夢境心理健康診斷建議
@login_required
def mental_health_dashboard(request):
    dreams = Dream.objects.filter(user=request.user)

    selected_dream = None
    mental_health_advice = None
    emotion_alert = None  # 新增：情緒警報訊息

    if request.method == 'POST':
        dream_id = request.POST.get('dream_id')
        selected_dream = Dream.objects.get(id=dream_id, user=request.user)

        # AI 心理健康建議
        mental_health_advice = generate_mental_health_advice(
            selected_dream.dream_content,
            selected_dream.emotion_score,
            selected_dream.Happiness,
            selected_dream.Anxiety,
            selected_dream.Fear,
            selected_dream.Excitement,
            selected_dream.Sadness
        )

        # 新增：偵測異常情緒並觸發警報
        if (selected_dream.Anxiety >= 70 or 
            selected_dream.Fear >= 70 or 
            selected_dream.Sadness >= 70):
            emotion_alert = "🚨 <strong>情緒警報：</strong> 您的夢境顯示 <strong>焦慮、恐懼或悲傷</strong> 指數偏高，建議您多關注自己的心理健康，必要時可尋求專業協助。"

    return render(request, 'dreams/mental_health_dashboard.html', {
        'dreams': dreams,
        'selected_dream': selected_dream,
        'mental_health_advice': mental_health_advice,
        'emotion_alert': emotion_alert  # 傳送至模板
    })


def generate_mental_health_advice(dream_content, emotion_score, happiness, anxiety, fear, excitement, sadness):
    """根據夢境內容與最高情緒指數，提供個性化的心理健康建議"""
    advice = []

    # 夢境主題分析
    dream_patterns = {
        "掉牙": "🦷 **夢見掉牙** 可能代表焦慮或變化，建議檢視近期壓力來源，調整步調。",
        "飛行": "✈️ **夢見飛行** 可能象徵對自由的渴望，或是逃避現實壓力。",
        "被追逐": "🏃 **夢見被追逐** 可能表示內心壓力較大，建議透過放鬆技巧來調適。",
        "迷路": "🗺️ **夢見迷路** 可能代表缺乏方向感，建議整理思緒，設定明確目標。",
        "考試": "📖 **夢見考試** 可能代表擔憂表現或對未來的不確定感。"
    }

    for keyword, response in dream_patterns.items():
        if keyword in dream_content:
            advice.append(response)

    # 找出最高的情緒指數
    emotion_scores = {
        "快樂": happiness,
        "焦慮": anxiety,
        "恐懼": fear,
        "興奮": excitement,
        "悲傷": sadness
    }
    
    highest_emotion = max(emotion_scores, key=emotion_scores.get)  # 找到最高指數的情緒
    highest_value = emotion_scores[highest_emotion]

    # 根據最高指數提供個性化建議
    emotion_advice = {
        "快樂": "😃 您最近感到快樂！建議記錄每天的幸福時刻，幫助增強正向情緒。",
        "焦慮": "⚠️ 焦慮指數較高，可以嘗試『呼吸練習』或每日 10 分鐘正念冥想來減壓。",
        "恐懼": "😨 恐懼感較強，可能對未來或未知事物感到不安，建議寫下擔憂，嘗試逐步面對。",
        "興奮": "🚀 興奮感較高！ 這可能代表您對未來充滿期待，建議好好規劃並利用這份能量。",
        "悲傷": "💙 悲傷指數較高，建議與信任的朋友聊天，或透過寫日記來整理情緒。"
    }

    # 選擇最高情緒的建議
    advice.append(emotion_advice[highest_emotion])

    # 心理資源推薦
    resource_recommendations = {
        "快樂": ["💡 推薦書籍：《快樂的習慣》，幫助您維持正向心態。"],
        "焦慮": ["📖 推薦書籍：《焦慮解方》，學習如何有效應對焦慮情緒。"],
        "恐懼": ["🎭 推薦心理工具：暴露療法，幫助您逐步適應恐懼源。"],
        "興奮": ["🔖 推薦管理方法：番茄鐘時間管理，將興奮轉化為生產力。"],
        "悲傷": ["🎵 音樂療法推薦：聆聽輕音樂有助於穩定情緒，如 Lo-Fi 或古典樂。"]
    }

    # 添加個性化的心理資源建議
    advice.append(random.choice(resource_recommendations[highest_emotion]))

    return " ".join(advice)

# 心理分析建議
@login_required
def get_mental_health_suggestions(request, dream_id):
    try:
        dream = Dream.objects.get(Dream,id=dream_id, user=request.user)
        print(f"找到夢境: {dream.dream_content}")  # 確保夢境存在

        # 調用解夢函數
        mental_health_advice = interpret_dream(dream.dream_content)
        # 返回解析後的數據
        return JsonResponse({
            "mental_health_advice": mental_health_advice,
        })
    
    except Dream.DoesNotExist:
        print("夢境不存在")
        return JsonResponse({"error": "夢境不存在"}, status=404)


# 1. 社群主頁和全球夢境趨勢
def community(request):
    """夢境社群主頁"""
    sort_type = request.GET.get('sort', 'popular')  # 預設為 popular

    if sort_type == 'latest':
        dream_posts = DreamPost.objects.order_by('-created_at')[:10]
    else:
        dream_posts = DreamPost.objects.order_by('-view_count')[:10]

    # 獲取最新夢境趨勢
    try:
        latest_trend = DreamTrend.objects.latest('date')
        trend_data = latest_trend.trend_data
    except DreamTrend.DoesNotExist:
        trend_data = {}

    # 處理熱門主題趨勢
    if trend_data:
        trend_data = dict(sorted(trend_data.items(), key=lambda item: item[1], reverse=True)[:8])

    return render(request, 'dreams/community.html', {
        'dream_posts': dream_posts,
        'trend_data': trend_data,
        'sort_type': sort_type,  # 傳入目前排序類型
    })


# 用這個來獲取當天的熱門趨勢
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
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        tags = request.POST.getlist('tags')  # 來自 select 的標籤
        
        # 創建新的 DreamPost
        dream_post = DreamPost.objects.create(
            title=title,
            content=content,
            user=request.user if not is_anonymous else None,  # 如果匿名則不設置使用者
            is_anonymous=is_anonymous,
        )

        # 處理標籤（現有標籤或新增標籤）
        for tag_name in tags:
            tag, created = DreamTag.objects.get_or_create(name=tag_name)
            dream_post.tags.add(tag)

        dream_post.save()  # 保存 DreamPost

        return redirect('dream_community')  # 重定向到夢境社群頁面

    # 取得流行標籤
    popular_tags = DreamTag.objects.all()

    return render(request, 'dreams/share_dream.html', {
        'popular_tags': popular_tags
    })

#查看貼文功能
@login_required
def my_posts(request):
    """顯示用戶自己發佈的夢境貼文，包括匿名貼文"""
    my_posts = DreamPost.objects.filter(
        Q(user=request.user) | Q(is_anonymous=True, user__isnull=True)
    ).order_by('-created_at')

    return render(request, 'dreams/my_posts.html', {'my_posts': my_posts})


#編輯貼文功能
@login_required
def edit_dream_post(request, post_id):
    """編輯夢境貼文"""
    dream_post = get_object_or_404(DreamPost, id=post_id)

    # 確保只有原作者或該貼文擁有者（匿名也算）才能編輯
    if dream_post.user != request.user and not dream_post.is_anonymous:
        messages.error(request, "你沒有權限編輯這篇貼文。")
        return redirect('dream_post_detail', post_id=post_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous', False) == 'on'
        tags = request.POST.getlist('tags')

        # 更新貼文內容
        dream_post.title = title
        dream_post.content = content
        dream_post.is_anonymous = is_anonymous
        dream_post.user = None if is_anonymous else request.user  # 根據匿名狀態變更使用者
        dream_post.save()

        # 更新標籤
        dream_post.tags.clear()
        for tag_name in tags:
            tag, created = DreamTag.objects.get_or_create(name=tag_name)
            dream_post.tags.add(tag)

        messages.success(request, "貼文已更新！")
        return redirect('dream_post_detail', post_id=dream_post.id)

    # 取得現有標籤
    popular_tags = DreamTag.objects.annotate(
        usage_count=Count('dreampost')
    ).order_by('-usage_count')[:20]

    return render(request, 'dreams/edit_dream_post.html', {
        'dream_post': dream_post,
        'popular_tags': popular_tags
    })

#刪除貼文功能
@login_required
def delete_dream_post(request, post_id):
    # 確保獲取到該貼文
    post = get_object_or_404(DreamPost, id=post_id)
    
    # 如果是 POST 請求才進行刪除
    if request.method == 'POST':
        post.delete()  # 刪除該貼文
        return redirect('my_posts')  # 重定向到「我的夢境貼文」頁面

    # 如果不是 POST 請求，重定向回列表頁（防止未經授權的請求）
    return redirect('my_posts')


# 3. 夢境搜索功能
def search_dreams(request):
    """搜索夢境"""
    query = request.GET.get('q', '')
    
    # 初步獲取所有夢境
    dreams = DreamPost.objects.all()

    # 根據搜尋關鍵字過濾夢境
    if query:
        dreams = dreams.filter(
            Q(content__icontains=query) | 
            Q(title__icontains=query)
        )
    
    # 傳遞資料到模板
    return render(request, 'dreams/search_results.html', {
        'dreams': dreams,
        'query': query
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


# 夢境與相關新聞
def dream_news(request):
    news_results = []
    articles = []  # 在這裡初始化 articles 變數，避免未定義的錯誤
    if request.method == 'POST':
        dream_input = request.POST.get('dream_input')

        # 1. 抓取新聞資料
        news_api_url = f'https://newsapi.org/v2/everything?q={dream_input}&language=zh&apiKey=44c026b581564a6f9d55df137196c6f4'
        response = requests.get(news_api_url)
        news_data = response.json()

        # 打印 NewsAPI 回應
        print("NewsAPI 回應: ", news_data)

        # 2. 計算新聞與夢境的相似度
        if news_data.get('status') == 'ok':
            articles = news_data.get('articles', [])
            print(f"找到 {len(articles)} 條新聞")  # 打印找到的新聞數量
            
            for article in articles:
                title = article['title']
                description = article['description']
                url = article['url']
                
                # 計算夢境與新聞的相似度
                documents = [dream_input, title + " " + description]
                vectorizer = TfidfVectorizer(stop_words='english')
                tfidf_matrix = vectorizer.fit_transform(documents)
                similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100

                news_results.append({
                    'title': title,
                    'description': description,
                    'url': url,
                    'similarity_score': round(similarity_score, 2)
                })
        # 只將相似度大於 0 的新聞加入 news_results
        news_results = [article for article in news_results if article['similarity_score'] > 0]

        # 如果沒有找到新聞，提供提示
        if not articles:
            print("沒有找到相關新聞")
            news_results.append({'title': '沒有找到相關新聞', 'description': '請稍後再試', 'url': '#', 'similarity_score': 0})

        # 按相似度從高到低排序
        news_results.sort(key=lambda x: x['similarity_score'], reverse=True)

    print("返回的新聞結果: ", news_results)  # 打印返回的新聞結果

    return render(request, 'dreams/dream_news.html', {'news_results': news_results})




# ...existing code...
from django.http import HttpResponse

def polls(request):
    return HttpResponse("這是 polls 頁面")
# ...existing code...



# dream/views.py
from django.shortcuts import render

def consultation_chat(request):
    return render(request, 'dreams/consultation_chat.html')


def consultation_landing_page(request):
    """渲染新的諮詢對話介紹頁面."""
    return render(request, 'dreams/consultation_chat.html')

def chat_with_counselor_view(request, counselor_id):
    """渲染與特定諮詢師的聊天頁面."""
    # counselor = get_object_or_404(Counselor, id=counselor_id) # 如果需要傳遞諮詢師對象
    return render(request, 'dreams/chat_with_counselor.html', {
        # 'counselor': counselor # 如果有傳遞諮詢師對象，可以在這裡傳入
    })

def counselor_list_view(request):
    """渲染諮詢師列表頁面."""
    # counselors = Counselor.objects.all() # 獲取所有諮詢師
    return render(request, 'dreams/counselor_list.html', {
        # 'counselors': counselors # 將諮詢師列表傳入模板
    })