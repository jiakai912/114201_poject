import json
import os
from dotenv import load_dotenv
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from openai import OpenAI  # 導入 OpenAI SDK
from .forms import DreamForm, UserRegisterForm,UserProfileForm,TherapistProfileForm
import logging
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,HttpResponseForbidden
import random  # 模擬 AI 建議，可替換為 NLP 分析
from django.contrib.auth.views import LoginView
from .models import User,Dream,DreamPost,DreamComment,DreamTag,DreamTrend,DreamRecommendation,PointTransaction,DreamShareAuthorization, UserProfile,TherapyAppointment, TherapyMessage,ChatMessage,UserAchievement,Achievement, CommentLike,PostLike
from django.db.models import Count,Q
from django.utils import timezone
import jieba  # 中文分詞庫
from collections import Counter,defaultdict
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
# 心理諮商相關
from django.contrib.auth.models import User
from django.db import models,transaction
from django.views.decorators.http import require_POST
from datetime import datetime

# 綠界
import datetime
from django.views.decorators.csrf import csrf_exempt
from dreams.sdk.ecpay_payment_sdk import ECPayPaymentSdk
# 個人檔案
from dreams.achievement_helper import check_and_unlock_achievements

#使用者查看已預約時段
from django.views.decorators.http import require_GET
from django.utils.dateparse import parse_datetime
from django.utils.timezone import localtime #已預約時段變成台灣地區時間

# 燈箱
def welcome_page(request):
    return render(request, 'dreams/welcome.html')

# 登入介面導向首頁
class CustomLoginView(LoginView):
    template_name = 'dreams/login.html'

    def get_redirect_url(self):
        redirect_to = self.request.GET.get('next', None)
        return redirect_to if redirect_to else '/dream_form/'  # 預設導向儀表板
    
# 註冊
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_therapist = form.cleaned_data.get('is_therapist')

            # 這裡設定 UserProfile
            profile = UserProfile.objects.get(user=user)
            profile.is_therapist = is_therapist
            profile.save()

            login(request, user)
            messages.success(request, '註冊成功！您現在已登入。')
            return redirect('dream_form')
    else:
        form = UserRegisterForm()
    return render(request, 'dreams/register.html', {'form': form})
    
# 心理諮商登入
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            profile, created = UserProfile.objects.get_or_create(user=user)

            if profile.is_therapist and not profile.is_verified_therapist:
                return redirect('not_verified')

            login(request, user)
            return redirect('dream_form')
        else:
            messages.error(request, '帳號或密碼錯誤')
            return redirect('login')
    else:
        return render(request, 'dreams/login.html')

# 心理諮商審核介面
def not_verified(request):
    return render(request, 'dreams/not_verified.html')


# 登出介面導向首頁
def logout_view(request):
    if request.method == "POST" or request.method == "GET":  # 支援 GET 和 POST
        logout(request)
        return redirect('logout_success')  # 重定向到登出成功頁面
    else:
        return HttpResponseForbidden("Invalid request method.")

def logout_success(request):
    return render(request, 'dreams/logout_success.html')  # 顯示登出成功頁面


# 編輯個人檔案
@login_required
def edit_profile(request):
    """
    編輯用戶個人檔案，心理師可額外設定點券價格。
    """
    user_profile_instance = request.user.userprofile

    # 選擇對應的表單
    form_class = TherapistProfileForm if user_profile_instance.is_therapist else UserProfileForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=user_profile_instance)
        if form.is_valid():
            form.save()
            messages.success(request, '個人檔案已成功更新！')
            return redirect('profile')
        else:
            messages.error(request, '更新失敗，請檢查輸入內容。')
    else:
        form = form_class(instance=user_profile_instance)

    # 使用統一模板
    return render(request, 'dreams/edit_profile.html', {'form': form})



# 個人檔案
@login_required
def user_profile(request):
    user_profile_instance, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile_instance, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '個人檔案和展示設定已成功更新！')
            return redirect('profile')
        else:
            print(form.errors) 
            messages.error(request, '更新個人檔案失敗，請檢查您的輸入。')
    else:
        form = UserProfileForm(instance=user_profile_instance, user=request.user) 

    unlocked_achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement').order_by('-unlocked_at')

    context = {
        'user_profile': user_profile_instance,
        'unlocked_achievements': unlocked_achievements,
        'form': form, # 將表單傳遞給模板
    }
    return render(request, 'dreams/profile.html', context)




# 用戶成就
@login_required
def user_achievements(request):
    user = request.user
    unlocked_achievements = UserAchievement.objects.filter(user=user).select_related('achievement').order_by('-unlocked_at')
    
    # 獲取用戶在各種條件鍵上的當前數值
    user_data = {
        'parse_count': Dream.objects.filter(user=user).count(),
        'post_count': DreamPost.objects.filter(user=user).count(),
        'total_post_likes': PostLike.objects.filter(post__user=user).count(), 
        'comment_count': DreamComment.objects.filter(user=user).count(), 
        'total_comment_likes': CommentLike.objects.filter(comment__user=user).count(),
    }
    
    # 獲取所有成就，並按條件值排序 - 確保這行在 for 迴圈之前
    all_achievements = Achievement.objects.all().order_by('condition_value') # <--- 關鍵行

    achievements_progress = []
    for achievement in all_achievements: # 遍歷所有成就
        is_unlocked = UserAchievement.objects.filter(user=user, achievement=achievement).exists()
        
        current_progress = user_data.get(achievement.condition_key, 0)
      
        current_progress = min(current_progress, achievement.condition_value)
        percentage = (current_progress / achievement.condition_value) * 100 if achievement.condition_value > 0 else 0  
        achievements_progress.append({
            'achievement': achievement,
            'current_progress': current_progress,
            'total_needed': achievement.condition_value,
            'percentage': round(percentage, 2),
            'is_unlocked': is_unlocked
        })
    context = {
        'unlocked_achievements': unlocked_achievements,
        'achievements_progress': achievements_progress,
    }
    return render(request, 'dreams/achievements.html', context)


@login_required
def profile_view(request):
    # 獲取當前使用者的 UserProfile
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # 如果使用者沒有 UserProfile (理論上 signals.py 應該會創建，但以防萬一)
        user_profile = UserProfile.objects.create(user=request.user)

    # 獲取使用者已解鎖的成就
    unlocked_achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement').order_by('-unlocked_at')

    context = {
        'user': request.user,
        'user_profile': user_profile,
        'unlocked_achievements': unlocked_achievements,
    }
    return render(request, 'dreams/profile.html', context)


# 檢查並解鎖成就
def check_and_unlock_achievements(user):
    user_data = {
        'parse_count': Dream.objects.filter(user=user).count(),
        'post_count': DreamPost.objects.filter(user=user).count(),
        'comment_count': DreamComment.objects.filter(user=user).count(),
        'total_post_likes': PostLike.objects.filter(post__user=user).count(),
        'total_comment_likes': CommentLike.objects.filter(comment__user=user).count(),
    }

    all_achievements = Achievement.objects.all()

    for achievement in all_achievements: # 遍歷所有成就
        current_progress = user_data.get(achievement.condition_key, 0)

        if current_progress >= achievement.condition_value:
            already_unlocked = UserAchievement.objects.filter(user=user, achievement=achievement).exists()
            if not already_unlocked:
                UserAchievement.objects.create(
                    user=user,
                    achievement=achievement,
                    unlocked_at=timezone.now()
                )
                messages.info(user, f"恭喜！您解鎖了成就：『{achievement.name}』！") # 解鎖時給予通知


# 載入環境變量
load_dotenv()
# DEEPSEEK_API_KEY = os.getenv("sk-b1e7ea9f25184324aaa973412b081f6f")  # 修正為正確的環境變量名稱
# 初始化 OpenAI 客戶端
client = OpenAI(api_key="sk-b1e7ea9f25184324aaa973412b081f6f", base_url="https://api.deepseek.com")


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
    dream_content = ""
    error_message = None
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = DreamForm(request.POST, request.FILES)

        # 檢查點券是否足夠（20點）
        if user_profile.points < 20:
            messages.error(request, "點券不足，無法解析夢境。請前往點券商店購買。")
            return redirect('pointshop')

        # 音檔處理邏輯
        audio_file = request.FILES.get('audio_file')
        if audio_file:
            try:
                wav_audio = convert_to_wav(audio_file)
                recognizer = sr.Recognizer()

                with sr.AudioFile(wav_audio) as source:
                    audio = recognizer.record(source)
                    try:
                        dream_content = recognizer.recognize_google(audio, language="zh-TW")
                    except sr.UnknownValueError:
                        error_message = "無法識別音檔內容，請再試一次。"
                    except sr.RequestError:
                        error_message = "語音識別服務無法訪問，請稍後重試。"
            except Exception as e:
                error_message = f"音檔處理錯誤: {e}"

        if form.is_valid():
            dream_content = form.cleaned_data.get('dream_content', dream_content)

            # 🔍 呼叫 NLP 解釋夢境
            interpretation, emotions, mental_health_advice = interpret_dream(dream_content)

            if emotions:
                # ✅ 儲存夢境
                dream = Dream.objects.create(
                    user=request.user,
                    dream_content=dream_content,
                    interpretation=interpretation,
                    Happiness=emotions.get("快樂", 0),
                    Anxiety=emotions.get("焦慮", 0),
                    Fear=emotions.get("恐懼", 0),
                    Excitement=emotions.get("興奮", 0),
                    Sadness=emotions.get("悲傷", 0)
                )

                # ✅ 解鎖成就
                check_and_unlock_achievements(request.user)

                # ✅ 扣除 20 點券
                user_profile.points -= 20
                user_profile.save()

                # 建立使用紀錄
                PointTransaction.objects.create(
                    user=request.user,
                    transaction_type='USE',
                    amount=20,
                    description='夢境解析'
                )

                messages.success(request, "夢境解析成功，已扣除 20 點券")

                return render(request, 'dreams/dream_result.html', {
                    'dream': dream,
                    'mental_health_advice': mental_health_advice
                })

    else:
        form = DreamForm()

    # 顯示歷史夢境
    dreams = Dream.objects.filter(user=request.user)

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
    emotion_alert = None
    therapist = None
    all_therapists = []

    if request.method == 'POST':
        dream_id = request.POST.get('dream_id')
        try:
            selected_dream = Dream.objects.get(id=dream_id, user=request.user)

            # AI 建議
            mental_health_advice = generate_mental_health_advice(
                selected_dream.dream_content,
                selected_dream.emotion_score,
                selected_dream.Happiness,
                selected_dream.Anxiety,
                selected_dream.Fear,
                selected_dream.Excitement,
                selected_dream.Sadness
            )

            # 情緒警報
            if (selected_dream.Anxiety >= 70 or 
                selected_dream.Fear >= 70 or 
                selected_dream.Sadness >= 70):
                emotion_alert = "🚨 <strong>情緒警報：</strong> 您的夢境顯示 <strong>焦慮、恐懼或悲傷</strong> 指數偏高，建議您多關注自己的心理健康，必要時可尋求專業協助。"

            # 嘗試取得已分享的心理師（其中一位）
            share = DreamShareAuthorization.objects.filter(user=request.user, is_active=True).first()
            if share:
                therapist = share.therapist

        except Dream.DoesNotExist:
            selected_dream = None

    # 所有已分享的心理師（下拉用）
    all_therapists = User.objects.filter(userprofile__is_therapist=True)

    return render(request, 'dreams/mental_health_dashboard.html', {
        'dreams': dreams,
        'selected_dream': selected_dream,
        'mental_health_advice': mental_health_advice,
        'emotion_alert': emotion_alert,
        'therapist': therapist,
        'therapists': all_therapists,
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
        dream = Dream.objects.get(id=dream_id, user=request.user)
        print(f"找到夢境: {dream.dream_content}")

        # ✅ FIX: interpret_dream 返回三個值，這裡也要正確解包
        _, _, mental_health_advice = interpret_dream(dream.dream_content)
        
        return JsonResponse({
            "mental_health_advice": mental_health_advice,
        })
    
    except Dream.DoesNotExist:
        print("夢境不存在")
        return JsonResponse({"error": "夢境不存在"}, status=404)


# 1. 社群主頁和全球夢境趨勢
# ✅ FIX: 合併兩個 community 函數，確保邏輯完整且變數已定義
def community(request):
    sort_type = request.GET.get('sort', 'popular')
    
    # 預加載 userprofile 和相關的 Achievement 物件
    # ✅ FIX: 確保 select_related 能夠正確載入 Achievement 的所有字段
    base_query = DreamPost.objects.select_related(
        'user__userprofile',
        'user__userprofile__display_title', # <-- 加載 display_title 關聯的 Achievement
        'user__userprofile__display_badge'  # <-- 加載 display_badge 關聯的 Achievement
    ).annotate(
        total_post_likes=Count('likes'),
        total_comments=Count('comments')
    )

    if sort_type == 'latest':
        dream_posts_raw = base_query.order_by('-created_at')[:10]
    else:
        dream_posts_raw = base_query.order_by('-view_count')[:10]

    posts_for_template = []
    for post in dream_posts_raw:
        post.is_liked_by_user = False
        if request.user.is_authenticated:
            post.is_liked_by_user = PostLike.objects.filter(post=post, user=request.user).exists()

        if post.user and hasattr(post.user, 'userprofile'):
            user_profile = post.user.userprofile
            # ✅ FIX: 從 Achievement 對象中獲取 'name' 作為稱號，'badge_icon' 作為圖標
            post.author_display_title = user_profile.display_title.name if user_profile.display_title else None
            post.author_display_badge_icon = user_profile.display_badge.badge_icon if user_profile.display_badge else None
            
            # 預加載已解鎖的成就，用於懸停卡片，同樣需要 select_related('achievement')
            post.author_unlocked_achievements = UserAchievement.objects.filter(user=post.user).select_related('achievement').order_by('-unlocked_at')[:5]
        else:
            post.author_display_title = None
            post.author_display_badge_icon = None
            post.author_unlocked_achievements = []

        posts_for_template.append(post)

    # 確保 trend_data 始終有初始值
    trend_data = {} 
    try:
        latest_trend = DreamTrend.objects.latest('date')
        if latest_trend:
            if isinstance(latest_trend.trend_data, dict):
                trend_data = latest_trend.trend_data
            else:
                trend_data = json.loads(latest_trend.trend_data)
    except DreamTrend.DoesNotExist:
        logging.info("No DreamTrend data found.")
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from DreamTrend.trend_data", exc_info=True)

    if trend_data:
        trend_data = dict(sorted(trend_data.items(), key=lambda item: item[1], reverse=True)[:8])

    today = timezone.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    
    top_this_week_posts = DreamPost.objects.filter(
        created_at__date__gte=start_of_week 
    ).annotate(
        num_comments=Count('comments'),
        num_likes=Count('likes')
    ).order_by('-num_comments', '-view_count', '-num_likes')[:5]

    return render(request, 'dreams/community.html', {
        'dream_posts': posts_for_template,
        'trend_data': trend_data,
        'sort_type': sort_type,
        'top_today_posts': top_this_week_posts,
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
# ai審核貼文
from .utils import contains_dangerous_keywords

@login_required
def share_dream(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        tags = request.POST.getlist('tags')

        # 危險字眼檢查
        flagged = contains_dangerous_keywords(content)

        dream_post = DreamPost.objects.create(
            title=title,
            content=content,
            user=request.user if not is_anonymous else None,
            is_anonymous=is_anonymous,
            is_flagged=flagged  # 儲存標記狀態
        )

        for tag_name in tags:
            tag, created = DreamTag.objects.get_or_create(name=tag_name)
            dream_post.tags.add(tag)

        return redirect('dream_community')

    popular_tags = DreamTag.objects.all()
    return render(request, 'dreams/share_dream.html', {
        'popular_tags': popular_tags
    })

#查看貼文功能
@login_required
def my_posts(request):
    # 確保也預加載 userprofile 以取得稱號/徽章資訊
    my_posts_raw = DreamPost.objects.filter(
        Q(user=request.user) | Q(is_anonymous=True, user__isnull=True)
    ).select_related(
        'user__userprofile__display_title',
        'user__userprofile__display_badge'
    ).order_by('-created_at')

    posts_for_template = []
    for post in my_posts_raw:
        post.is_liked_by_user = False # my_posts 頁面目前沒用到這個
        if request.user.is_authenticated:
            post.is_liked_by_user = PostLike.objects.filter(post=post, user=request.user).exists()

        if post.user and hasattr(post.user, 'userprofile'):
            user_profile = post.user.userprofile
            # ✅ FIX: 從 Achievement 對象中獲取 'name' 作為稱號，'badge_icon' 作為圖標
            post.author_display_title = user_profile.display_title.name if user_profile.display_title else None
            post.author_display_badge_icon = user_profile.display_badge.badge_icon if user_profile.display_badge else None
            post.author_unlocked_achievements = UserAchievement.objects.filter(user=post.user).select_related('achievement').order_by('-unlocked_at')[:5]
        else: # 處理匿名貼文的情況
            post.author_display_title = None
            post.author_display_badge_icon = None
            post.author_unlocked_achievements = []

        posts_for_template.append(post)

    return render(request, 'dreams/my_posts.html', {'my_posts': posts_for_template})


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
@login_required
def dream_post_detail(request, post_id):
    # ✅ FIX: 預加載貼文作者和評論者的 userprofile、display_title 和 display_badge (深度到 Achievement)
    dream_post = get_object_or_404(
        DreamPost.objects.select_related(
            'user__userprofile', # 確保載入 userprofile
            'user__userprofile__display_title',
            'user__userprofile__display_badge'
        ), id=post_id
    )
    dream_post.increase_view_count()

    # 為貼文作者添加稱號和徽章資訊
    if dream_post.user and hasattr(dream_post.user, 'userprofile'):
        user_profile = dream_post.user.userprofile
        dream_post.author_display_title = user_profile.display_title.name if user_profile.display_title else None
        dream_post.author_display_badge_icon = user_profile.display_badge.badge_icon if user_profile.display_badge else None
        dream_post.author_unlocked_achievements = UserAchievement.objects.filter(user=dream_post.user).select_related('achievement').order_by('-unlocked_at')[:5]
    else:
        dream_post.author_display_title = None
        dream_post.author_display_badge_icon = None
        dream_post.author_unlocked_achievements = []

    comments = []
    # ✅ FIX: 預加載評論者的 userprofile、display_title 和 display_badge (深度到 Achievement)
    raw_comments = dream_post.comments.select_related(
        'user__userprofile', # 確保載入 userprofile
        'user__userprofile__display_title',
        'user__userprofile__display_badge'
    ).order_by('created_at')
    
    for comment in raw_comments:
        comment_data = {
            'id': comment.id,
            'user': comment.user,
            'content': comment.content,
            'created_at': comment.created_at,
            'likes_count': comment.likes.count(),
            'is_liked_by_user': False,
            'commenter_display_title': None,
            'commenter_display_badge_icon': None,
            'commenter_unlocked_achievements': []
        }
        if request.user.is_authenticated:
            comment_data['is_liked_by_user'] = CommentLike.objects.filter(comment=comment, user=request.user).exists()

        # ✅ 新增：為每個評論者添加稱號和徽章資訊
        if comment.user and hasattr(comment.user, 'userprofile'):
            user_profile = comment.user.userprofile
            comment_data['commenter_display_title'] = user_profile.display_title.name if user_profile.display_title else None
            comment_data['commenter_display_badge_icon'] = user_profile.display_badge.badge_icon if user_profile.display_badge else None
            comment_data['commenter_unlocked_achievements'] = UserAchievement.objects.filter(user=comment.user).select_related('achievement').order_by('-unlocked_at')[:5]

        comments.append(comment_data)

    similar_dreams = get_similar_dreams(dream_post)

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
                documents = [dream_input, (title or "") + " " + (description or "")]
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


# 心理諮商頁面分享夢境給心理師
@login_required
def share_dreams(request):
    if request.method == 'POST':
        therapist_id = request.POST.get('therapist_id')
        therapist = User.objects.get(id=therapist_id)

        if not therapist.userprofile.is_therapist:
            return HttpResponseForbidden("只能分享給心理師")

        DreamShareAuthorization.objects.update_or_create(
            user=request.user,
            therapist=therapist,
            defaults={'is_active': True}
        )

        messages.success(request, f"已成功分享夢境給 {therapist.username} 心理師！")
        return redirect('dream_form')  # 或你想回到的頁面

    # 補上 GET 請求的回傳（渲染頁面或其他）
    therapists = User.objects.filter(userprofile__is_therapist=True)
    return render(request, 'dreams/share_dreams.html', {'therapists': therapists})



#取消分享夢境 
@login_required
@require_POST
def cancel_share(request, therapist_id):
    try:
        share = DreamShareAuthorization.objects.get(user=request.user, therapist_id=therapist_id, is_active=True)
        share.is_active = False
        share.save()
        messages.success(request, "已取消分享夢境給該心理師。")
    except DreamShareAuthorization.DoesNotExist:
        messages.error(request, "找不到該分享紀錄。")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



#心理師可以看到分享的列表    
@login_required
def shared_with_me(request):
    """心理師查看所有曾經分享過的使用者（包含取消分享）"""
    if not request.user.userprofile.is_therapist:
        return HttpResponseForbidden("只有心理師可以查看分享名單")

    shares = DreamShareAuthorization.objects.filter(
        therapist=request.user,
        # is_active=True  # 改成全部都抓
    ).select_related('user')

    return render(request, 'dreams/shared_users.html', {'shared_users': shares})


#心理師可以看到分享的夢境
@login_required
def view_user_dreams(request, user_id):
    if not request.user.userprofile.is_therapist:
        return HttpResponseForbidden("只有心理師可以查看夢境")

    # 不只查 is_active=True 的授權，而是找所有授權紀錄
    share = DreamShareAuthorization.objects.filter(
        user_id=user_id,
        therapist=request.user
    ).first()

    if not share:
        return HttpResponseForbidden("您沒有查看此使用者夢境的權限")

    # 分享是否啟用決定夢境資料是否取出
    dreams = Dream.objects.filter(user_id=user_id).order_by('-created_at') if share.is_active else []

    target_user = User.objects.get(id=user_id)

    return render(request, 'dreams/user_dreams_for_therapist.html', {
        'dreams': dreams,
        'target_user': target_user,
        'is_active_share': share.is_active,
    })


# 心理諮商預約及對話
@login_required
def share_and_schedule(request):
    therapists = User.objects.filter(userprofile__is_therapist=True, userprofile__is_verified_therapist=True)

    if request.method == 'POST':
        therapist_id = request.POST.get('therapist_id')
        scheduled_time = request.POST.get('scheduled_time')
        message_content = request.POST.get('message')

        try:
            therapist = User.objects.get(id=therapist_id)
        except User.DoesNotExist:
            messages.error(request, "找不到該心理師。")
            return render(request, 'dreams/mental_health_dashboard.html', {'therapists': therapists})

        user_profile = request.user.userprofile
        therapist_profile = therapist.userprofile
        appointment_cost = therapist_profile.coin_price if therapist_profile.coin_price else 1500  # 預設1500

        with transaction.atomic():
            if user_profile.points < appointment_cost:
                messages.error(request, f"點數不足（需 {appointment_cost} 點），請先儲值。")
                return render(request, 'dreams/mental_health_dashboard.html', {'therapists': therapists})

            try:
                from datetime import datetime
                scheduled_dt = datetime.strptime(scheduled_time, "%Y-%m-%dT%H:%M")
                if scheduled_dt.minute != 0 or scheduled_dt.second != 0:
                    messages.error(request, "預約時間必須為整點（例如 14:00、15:00）。")
                    return render(request, 'dreams/mental_health_dashboard.html', {'therapists': therapists})
            except Exception:
                messages.error(request, "預約時間格式錯誤。")
                return render(request, 'dreams/mental_health_dashboard.html', {'therapists': therapists})

            if TherapyAppointment.objects.filter(therapist=therapist, scheduled_time=scheduled_dt).exists():
                messages.error(request, "此時間已被預約，請選擇其他時間。")
                return render(request, 'dreams/mental_health_dashboard.html', {'therapists': therapists})

            # 點數扣除與記錄
            user_profile.points -= appointment_cost
            user_profile.save()

            PointTransaction.objects.create(
                user=request.user,
                amount=-appointment_cost,
                description=f"預約心理師 {therapist.username} 諮商（1 小時）"
            )

            # 分享授權
            DreamShareAuthorization.objects.update_or_create(
                user=request.user,
                therapist=therapist,
                defaults={'is_active': True}
            )

            TherapyAppointment.objects.create(
                user=request.user,
                therapist=therapist,
                scheduled_time=scheduled_dt
            )

            if message_content:
                TherapyMessage.objects.create(
                    sender=request.user,
                    receiver=therapist,
                    content=message_content
                )

        messages.success(request, f"已成功預約，並扣除 {appointment_cost} 點，目前剩餘 {user_profile.points} 點。")
        return redirect('user_appointments')

    return render(request, 'dreams/mental_health_dashboard.html', {'therapists': therapists})

#使用者查看自己的預約
@login_required
def user_appointments(request):
    appointments = TherapyAppointment.objects.filter(
    user=request.user
    ).order_by('-scheduled_time')

    # 找出使用者已授權的心理師
    therapists = [
        share.therapist for share in DreamShareAuthorization.objects.filter(
            user=request.user, is_active=True
        ).select_related('therapist')
    ]

    # 找出所有已確認的預約心理師 id
    confirmed_therapist_ids = set(
        appointments.filter(is_confirmed=True).values_list('therapist_id', flat=True)
    )

    # 對每筆預約附加 point_change 屬性
    for appt in appointments:
        if appt.is_confirmed:
            appt.point_change = -1500
        else:
            appt.point_change = 0  # 未確認預約尚未扣點

    return render(request, 'dreams/user_appointments.html', {
        'appointments': appointments,
        'therapists': therapists,
        'confirmed_therapist_ids': confirmed_therapist_ids,
    })


#使用者查看已預約時段
@require_GET #只有使用者看得到
def get_therapist_booked_slots(request, therapist_id):
    appointments = TherapyAppointment.objects.filter(
        therapist_id=therapist_id,
        is_cancelled=False,
        is_confirmed=True
    )

    # 修正這一行
    booked_slots = [
    localtime(appt.scheduled_time).strftime("%Y-%m-%dT%H:%M") 
    for appt in appointments
]

    return JsonResponse({'booked_slots': booked_slots})


#使用者取消未確認的預約
@require_POST
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(TherapyAppointment, id=appointment_id)

    if appointment.user != request.user:
        return HttpResponseForbidden("您無權取消此預約")

    if appointment.is_confirmed:
        return HttpResponseForbidden("已確認的預約無法取消")

    # 標記為已取消
    appointment.is_cancelled = True
    appointment.save()

    # 退回點券
    profile = request.user.userprofile
    profile.points += 1500
    profile.save()

    # 點數紀錄
    PointTransaction.objects.create(
        user=request.user,
        transaction_type='GAIN',
        amount=1500,
        description='取消預約退還點數'
    )

    return redirect('user_appointments')



#聊天室
@login_required
def therapist_list_with_chat(request):
    # 授權紀錄（不限定 is_active）
    authorized_records = DreamShareAuthorization.objects.filter(
        user=request.user,
        therapist__userprofile__is_therapist=True,
        therapist__userprofile__is_verified_therapist=True
    ).select_related('therapist')

    therapist_statuses = []
    for record in authorized_records:
        therapist_statuses.append({
            'therapist': record.therapist,
            'is_active': record.is_active
        })

    # 查出哪些心理師的預約已確認
    confirmed_therapist_ids = set(
        TherapyAppointment.objects.filter(
            user=request.user,
            is_confirmed=True
        ).values_list('therapist_id', flat=True)
    )

    return render(request, 'dreams/therapist_list.html', {
        'therapist_statuses': therapist_statuses,
        'confirmed_therapist_ids': confirmed_therapist_ids
    })


# 心理師端的預約時間
@login_required
def consultation_schedule(request, user_id):
    client = get_object_or_404(User, id=user_id)
    if not request.user.userprofile.is_therapist:
        return HttpResponseForbidden("只有心理師能查看預約資料")

    # 只查詢這個使用者的預約
    appointments = TherapyAppointment.objects.filter(
        therapist=request.user,
        user__id=user_id,
        is_cancelled=False
    ).order_by('-scheduled_time')

    return render(request, 'dreams/consultation_schedule.html', {
        'client': client,
        'appointments': appointments
    })



# 心理師端可以看到的所有使用者預約時間
@login_required
def all_users_appointments(request):
    # 限制只有心理師可以使用
    if not request.user.userprofile.is_therapist:
        return HttpResponseForbidden("只有心理師可以查看此頁面")

    # 抓取所有預約我的紀錄（排除已取消的）
    appointments = TherapyAppointment.objects.select_related('user', 'therapist') \
        .filter(therapist=request.user, is_cancelled=False).order_by('-scheduled_time')

    # 取得有預約我的使用者（去重）
    users_with_appointments = User.objects.filter(
        received_appointments__therapist=request.user,
        received_appointments__is_cancelled=False
    ).distinct()

    return render(request, 'dreams/all_users_appointments.html', {
        'appointments': appointments,
        'users_with_appointments': users_with_appointments,
    })



# 心理師端的確認預約按鈕
@require_POST
@login_required
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(TherapyAppointment, id=appointment_id)

    # 檢查是否是該心理師本人
    if appointment.therapist != request.user:
        return HttpResponseForbidden("您無權確認此預約")

    appointment.is_confirmed = True
    appointment.save()
    return redirect('consultation_schedule', user_id=appointment.user.id)


    
# 心理師端的刪除預約按鈕
@require_POST
@login_required
def therapist_delete_appointment(request, appointment_id):
    appointment = get_object_or_404(TherapyAppointment, id=appointment_id)

    # 驗證心理師身份
    if appointment.therapist != request.user:
        return HttpResponseForbidden("您無權刪除此預約。")

    # 檢查預約是否已過期
    if appointment.scheduled_time < timezone.now():
        messages.error(request, "預約時間已過，無法刪除。")
        return redirect('therapist_view_client_appointments', user_id=appointment.user.id)

    # 只有已確認的預約會退點數
    if appointment.is_confirmed:
        user_profile = appointment.user.userprofile

        with transaction.atomic():
            user_profile.points += 1500
            user_profile.save()

            PointTransaction.objects.create(
                user=appointment.user,
                transaction_type='GAIN',
                amount=1500,
                description=f'心理師取消已確認預約退還點數（ID:{appointment.id}）'
            )

            appointment.delete()

        messages.success(request, "已確認的預約已刪除並退還使用者1500點。")
    else:
        # 未確認的預約不加點，直接刪除
        appointment.delete()
        messages.success(request, "未確認的預約已刪除。")

    return redirect('therapist_view_client_appointments', user_id=appointment.user.id)




# 心理師端的聊天室
@login_required
def my_clients(request):
    # 只限心理師存取
    if not request.user.userprofile.is_therapist:
        return HttpResponseForbidden("只有心理師可以使用此功能")

    # 找出授權給我的使用者
    shared_users = DreamShareAuthorization.objects.filter(
        therapist=request.user,
        is_active=True
    ).select_related('user')

    return render(request, 'dreams/my_clients.html', {
        'shared_users': shared_users,  # 傳入整個 queryset
    })


@login_required
def chat_with_client(request, user_id):
    chat_user = get_object_or_404(User, id=user_id)

    # 先檢查授權
    authorized = DreamShareAuthorization.objects.filter(
        therapist=request.user,
        user=chat_user,
        is_active=True
    ).exists()
    if not authorized:
        return HttpResponseForbidden("尚未獲得該使用者授權")

    messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=chat_user) |
        Q(sender=chat_user, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            ChatMessage.objects.create(sender=request.user, receiver=chat_user, message=message_text)
            return redirect('chat_with_client', user_id=user_id)

    return render(request, 'dreams/chat_room.html', {
        'messages': messages,
        'chat_user': chat_user,
    })


@login_required
def chat_with_therapist(request, therapist_id):
    chat_user = get_object_or_404(User, id=therapist_id)

    messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=chat_user) |
        Q(sender=chat_user, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            ChatMessage.objects.create(sender=request.user, receiver=chat_user, message=message_text)
            return redirect('chat_with_therapist', therapist_id=therapist_id)

    return render(request, 'dreams/chat_room.html', {
        'messages': messages,
        'chat_user': chat_user,
    })



@login_required
def chat_room(request, chat_user_id):
    chat_user = get_object_or_404(User, id=chat_user_id)

    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg:
            ChatMessage.objects.create(sender=request.user, receiver=chat_user, message=msg)
            return redirect('chat_room', chat_user_id=chat_user.id)  # 重導避免表單重送

    messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=chat_user) |
        Q(sender=chat_user, receiver=request.user)
    ).order_by('timestamp')

    return render(request, 'dreams/chat_room.html', {
        'chat_user': chat_user,
        'messages': messages,
    })



@login_required
def chat_with_user(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # 決定目前使用者的身份
    is_self_therapist = request.user.userprofile.is_therapist
    is_other_therapist = other_user.userprofile.is_therapist

    if is_self_therapist:
        # 心理師只能與授權給他的使用者聊天
        authorized = DreamShareAuthorization.objects.filter(
            therapist=request.user,
            user=other_user,
            is_active=True
        ).exists()
    else:
        # 使用者只能與他授權的心理師聊天
        authorized = DreamShareAuthorization.objects.filter(
            therapist=other_user,
            user=request.user,
            is_active=True
        ).exists()

    if not authorized:
        return HttpResponseForbidden("尚未取得授權或無效聊天對象")

    # 抓訊息紀錄
    messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    # 發送新訊息
    if request.method == 'POST':
        text = request.POST.get('message', '').strip()
        if text:
            ChatMessage.objects.create(sender=request.user, receiver=other_user, message=text)
            return redirect('chat_with_user', user_id=other_user.id)

    return render(request, 'dreams/chat_room.html', {
        'messages': messages,
        'chat_user': other_user
    })


# 綠界第三方支付
def ecpay_checkout(request):
    sdk = ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )

    order_params = {
        'MerchantTradeNo': 'TEST' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        'MerchantTradeDate': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'CustomField1': str(request.user.id),  # 傳使用者 ID 給 return 用
        'PaymentType': 'aio',
        'TotalAmount': 100,
        'TradeDesc': '測試交易',
        'ItemName': '夢境分析報告 x1',
        'ReturnURL': 'http://127.0.0.1:8000/ecpay/return/',
        'OrderResultURL': 'http://127.0.0.1:8000/ecpay/return/',
        'ClientBackURL': 'http://127.0.0.1:8000/thankyou/',
        'NeedExtraPaidInfo': 'Y',
        'EncryptType': 1,
        'ChoosePayment': 'Credit'
    }

    try:
        final_params = sdk.create_order(order_params)
        action_url = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"
        return render(request, 'dreams/ecpay_checkout.html', {
        'final_params': final_params,
        'action_url': action_url
        })

    except Exception as e:
        return HttpResponse(f"發生錯誤：{e}")
    

def result(request):
    return HttpResponse("付款結果頁面")

# 點券包
POINT_PACKAGES = [
    {'id': 1, 'name': '100 點券', 'price': 100, 'points': 100},
    {'id': 2, 'name': '500 點券', 'price': 500, 'points': 500},
    {'id': 3, 'name': '1000 點券', 'price': 1000, 'points': 1000},
]

@login_required
def pointshop(request):
    return render(request, 'dreams/pointshop.html', {'packages': POINT_PACKAGES})
    

@login_required
def pointshop_buy(request, pkg_id):
    pkg = next((p for p in POINT_PACKAGES if p['id'] == int(pkg_id)), None)
    if not pkg:
        return HttpResponse("找不到點券包", status=404)

    sdk = ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )

    def clean_username(username):
        return ''.join(re.findall(r'[A-Za-z0-9]', username))[:5].ljust(5, 'X')

    username_short = clean_username(request.user.username)
    timestamp = datetime.datetime.now().strftime('%y%m%d%H%M')  # 12字元
    trade_no = f"PT{username_short}{timestamp}"  # 總長 19

    order_params = {
        'MerchantTradeNo': trade_no,
        'MerchantTradeDate': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'CustomField1': str(request.user.id),  # 傳使用者 ID 給 return 用
        'PaymentType': 'aio',
        'TotalAmount': pkg['price'],
        'TradeDesc': f'購買點券包：{pkg["name"]}',
        'ItemName': pkg['name'],
        'ReturnURL': 'http://127.0.0.1:8000/ecpay/return/',
        'OrderResultURL': 'http://127.0.0.1:8000/ecpay/return/',
        'ClientBackURL': 'http://127.0.0.1:8000/thankyou/',
        'NeedExtraPaidInfo': 'Y',
        'EncryptType': 1,
        'ChoosePayment': 'Credit'
    }

    try:
        final_params = sdk.create_order(order_params)
        action_url = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"
        return render(request, 'dreams/ecpay_checkout.html', {
            'final_params': final_params,
            'action_url': action_url
        })
    except Exception as e:
        return HttpResponse(f"發生錯誤：{e}")


logger = logging.getLogger(__name__)
@csrf_exempt
def ecpay_return(request):
    if request.method == 'POST':
        data = request.POST.dict()
        trade_amt_str = data.get('TradeAmt', '0')
        user_id = data.get('CustomField1')

        try:
            trade_amt = int(trade_amt_str)
            if trade_amt <= 0:
                logger.warning(f"收到不合理的 TradeAmt: {trade_amt}")
                return HttpResponse("付款金額異常")
        except ValueError:
            logger.error(f"TradeAmt 轉換錯誤: {trade_amt_str}")
            return HttpResponse("付款金額錯誤")

        if not user_id:
            logger.error("沒有收到使用者ID(CustomField1)")
            return HttpResponse("缺少使用者資訊")

        try:
            user = User.objects.get(id=user_id)
            profile = user.userprofile
            old_points = profile.points
            profile.points += trade_amt
            profile.save()

            # ✅ 寫入點券交易紀錄
            PointTransaction.objects.create(
                user=user,
                transaction_type='GAIN',
                amount=trade_amt,
                description='儲值點券（綠界付款）'
            )

            logger.info(f"已為 {user.username} 加值 {trade_amt} 點，點數從 {old_points} -> {profile.points}")
        except User.DoesNotExist:
            logger.error(f"找不到使用者 id={user_id}")
            return HttpResponse("找不到使用者")

        # ✅ 回傳點券商店頁（附成功訊息）
        return render(request, 'dreams/pointshop.html', {
            'success_message': f"✅ 成功加值 {trade_amt} 點，目前總點數：{profile.points}",
            'packages': POINT_PACKAGES  # 別忘了傳回方案資料
        })

    return HttpResponse("非 POST 請求")


# 點券使用記錄
@login_required
def point_history(request):
    transactions = PointTransaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dreams/point_history.html', {'transactions': transactions})


# 綠界測試付款完成頁
@csrf_exempt
def ecpay_result(request):
    if request.method == "POST":
        print("✅ OrderResult 收到綠界回傳資料：", request.POST.dict())
        # 付款成功後導回點券商店
        return redirect('pointshop')
    return HttpResponse("這是綠界付款完成後導回的頁面")






from django.http import JsonResponse
@login_required
@require_POST 
def toggle_comment_like(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': '請先登入'}, status=401)

    comment = get_object_or_404(DreamComment, id=comment_id)
    user = request.user

    try:
        like = CommentLike.objects.get(comment=comment, user=user)
        like.delete() # 如果已按讚，則取消按讚
        liked = False
        message = '已取消按讚'
    except CommentLike.DoesNotExist:
        CommentLike.objects.create(comment=comment, user=user) # 如果未按讚，則按讚
        liked = True
        message = '已按讚'

    # 獲取最新的按讚數量
    likes_count = comment.likes.count()
    return JsonResponse({'success': True, 'liked': liked, 'likes_count': likes_count, 'message': message})





# 黃忠
from django.db.models import Count 

@login_required
@require_POST
def toggle_post_like(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': '請先登入'}, status=401)

    post = get_object_or_404(DreamPost, id=post_id)
    user = request.user

    try:
        like = PostLike.objects.get(post=post, user=user)
        like.delete()
        liked = False
        message = '已取消按讚貼文'
    except PostLike.DoesNotExist:
        PostLike.objects.create(post=post, user=user)
        liked = True
        message = '已按讚貼文'

    likes_count = post.likes.count()
    return JsonResponse({'success': True, 'liked': liked, 'likes_count': likes_count, 'message': message})


from django.http import JsonResponse
@login_required
@require_POST
def toggle_comment_like(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': '請先登入'}, status=401)

    comment = get_object_or_404(DreamComment, id=comment_id)
    user = request.user

    try:
        like = CommentLike.objects.get(comment=comment, user=user)
        like.delete()
        liked = False
        message = '已取消按讚'
    except CommentLike.DoesNotExist:
        CommentLike.objects.create(comment=comment, user=user)
        liked = True
        message = '已按讚'

    likes_count = comment.likes.count()
    return JsonResponse({'success': True, 'liked': liked, 'likes_count': likes_count, 'message': message})
