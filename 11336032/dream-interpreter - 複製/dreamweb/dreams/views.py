import json
import os
from dotenv import load_dotenv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from openai import OpenAI
from .forms import DreamForm, UserRegisterForm
import logging
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth.views import LoginView
from .models import Dream, DreamPost, DreamComment, DreamTag, DreamTrend, DreamRecommendation, Counselor, Achievement, UserAchievement, UserProfile
from django.db.models import Count, Q
from django.utils import timezone
import jieba
from collections import Counter
import random
import re
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import speech_recognition as sr
from pydub import AudioSegment
import io
from django.core.paginator import Paginator
# from bs4 import BeautifulSoup # 如果沒有直接使用，可以註釋或刪除

# ====================================================================================================
# 全局變數與配置 (Global Variables & Configurations)
# ====================================================================================================

load_dotenv()

# DeepSeek AI API 客戶端
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY", "sk-b1e7ea9f25184324aaa973412b081f6f"), base_url="https://api.deepseek.com")

# NewsAPI 的 API KEY
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "44c026b581564a6f9d55df137196c6f4")

# 中文停用詞列表
stopwords_chinese = [
    '的', '是', '了', '在', '和', '我', '你', '他', '她', '它', '們', '一個', '一些', '什麼', '怎麼', '沒有', '有', '也', '還',
    '很', '多', '少', '大', '小', '上', '下', '前', '後', '左', '右', '裡', '外', '會', '可以', '要', '想', '說', '看', '到',
    '去', '來', '出', '入', '之', '與', '而', '及', '從', '為', '與', '或', '但', '卻', '又', '才', '就', '所以', '因為', '如果',
    '雖然', '但是', '然而', '並且', '因此', '於是', '則', '以', '及', '其', '可', '各', '同', '向', '如', '等', '與', '此', '這',
    '那', '些', '這種', '這樣', '那樣', '如此', '例如', '由於', '至於', '對於', '關於', '為了', '除了', '隨著', '按照', '根據',
    '關於', '直到', '雖然', '因為', '但是', '以便', '以及', '即使', '假如', '豈不', '反而', '儘管', '無論', '由於', '由於', '至於',
    '因此', '從而', '甚至', '以致', '何況', '總之', '再說', '換言之', '其實', '此外', '特別是', '當然', '究竟', '大概', '恐怕', '簡直',
    '畢竟', '到底', '根本', '往往', '常常', '不斷', '一直', '始終', '永遠', '終於', '突然', '仍然', '還是', '已經', '正在', '即將',
    '將要', '才能', '才能夠', '為了', '不但', '不僅', '而且', '就是', '既然', '雖然', '只要', '只有', '除非', '無論', '不管', '即使',
    '如果', '要是', '假設', '因此', '於是', '總之', '反而', '再說', '何況', '此外', '特別是', '當然', '究竟', '大概', '恐怕', '簡直',
    '畢竟', '到底', '根本', '往往', '常常', '不斷', '一直', '始終', '永遠', '終於', '突然', '仍然', '還是', '已經', '正在', '即將',
    '將要', '才能', '才能夠', '為了', '為了', '以便', '以免', '免得', '以免', '使得', '為了', '因而', '由於', '從而', '結果', '既然',
    '只要', '只有', '除非', '不管', '無論', '不論', '盡管', '雖然', '可是', '但是', '然而', '雖然', '而且', '並且', '此外', '再說',
    '何況', '特別是', '況且', '就是說', '換句話說', '例如', '比如', '譬如', '像', '根據', '依照', '按照', '關於', '對於', '至於',
    '隨著', '除了', '除非', '除了', '而是', '即使', '儘管', '然而', '因為', '由於', '由於', '因為', '所以', '因此', '從而', '結果',
    '於是', '既然', '假如', '如果', '要是', '除非', '只要', '只有', '不管', '無論', '不論', '除了', '以免', '以便', '免得', '使得',
    '因而', '況且', '並且', '此外', '再說', '何況', '特別是', '此外', '就是說', '換句話說', '等等', '等'
]


# ====================================================================================================
# 工具函數 (Utility Functions)
# ====================================================================================================

def convert_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file)
    wav_audio = io.BytesIO()
    audio.export(wav_audio, format='wav')
    wav_audio.seek(0)
    return wav_audio

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
                                                  "心理診斷建議:\n"
                                                  "以上解析裡不要出現＊或**符號"},
                    {"role": "user", "content": dream_content}
                ],
                temperature=0.7,
                stream=False,
            )
            interpretation_raw = response.choices[0].message.content
            break

        except openai.APITimeoutError:
            logging.warning(f"API 超時，正在重試...（第 {attempt + 1} 次）")
            time.sleep(2)
            if attempt == max_retries - 1:
                return "API 超時，請稍後再試。", None, None

        except Exception as e:
            logging.error(f"API 請求失敗: {str(e)}", exc_info=True)
            return f"API 請求失敗: {str(e)}", None, None

    emotions = {"快樂": 0, "焦慮": 0, "恐懼": 0, "興奮": 0, "悲傷": 0}
    mental_health_advice = ""
    interpretation_text = ""

    lines = interpretation_raw.split("\n")
    emotion_lines = []
    keyword_lines = []
    meaning_lines = []
    advice_lines = []
    
    current_section = None
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue

        if "快樂" in line_stripped or "焦慮" in line_stripped or "恐懼" in line_stripped or "興奮" in line_stripped or "悲傷" in line_stripped:
            current_section = "emotions"
            emotion_lines.append(line_stripped)
        elif "夢境關鍵字:" in line_stripped:
            current_section = "keywords"
        elif "心理診斷建議:" in line_stripped:
            current_section = "advice"
        elif current_section == "emotions":
            emotion_lines.append(line_stripped)
        elif current_section == "keywords":
            keyword_lines.append(line_stripped)
        elif current_section == "advice":
            advice_lines.append(line_stripped)
        elif current_section is None or current_section == "meaning":
            if not ("快樂" in line_stripped or "焦慮" in line_stripped or "恐懼" in line_stripped or "興奮" in line_stripped or "悲傷" in line_stripped or "夢境關鍵字:" in line_stripped or "心理診斷建議:" in line_stripped):
                meaning_lines.append(line_stripped)
            else:
                current_section = "meaning"

    for line in emotion_lines:
        match = re.search(r"(\S+)\s(\d+)%", line)
        if match:
            emotion, value = match.groups()
            emotion = emotion.strip()
            if emotion in emotions:
                emotions[emotion] = float(value)

    interpretation_text = ""
    if emotion_lines:
        interpretation_text += "\n".join(emotion_lines) + "\n\n"
    
    if keyword_lines:
        interpretation_text += "\n".join(keyword_lines) + "\n\n"
    
    if meaning_lines:
        interpretation_text += "\n".join(meaning_lines) + "\n\n"

    if advice_lines:
        mental_health_advice = "\n".join(advice_lines).replace("心理診斷建議:", "").strip()
    
    interpretation_text = interpretation_text.replace("心理診斷建議:", "").strip()

    return interpretation_text, emotions, mental_health_advice

# ====================================================================================================
# 用戶認證與註冊 (Authentication & Registration)
# ====================================================================================================

def welcome_page(request):
    return render(request, 'dreams/welcome.html')

class CustomLoginView(LoginView):
    template_name = 'dreams/login.html'

    def get_redirect_url(self):
        redirect_to = self.request.GET.get('next', None)
        return redirect_to if redirect_to else '/dream_form/'

def logout_view(request):
    if request.method == "POST" or request.method == "GET":
        logout(request)
        messages.info(request, "您已成功登出。")
        return redirect('logout_success') # 保持重定向到 logout_success 頁面
    else:
        return HttpResponseForbidden("Invalid request method.")

def logout_success(request): # <--- 添加這個函數
    """顯示登出成功頁面"""
    return render(request, 'dreams/logout_success.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '註冊成功！您現在已登入。')
            return redirect('dream_form')
        else:
            messages.error(request, '註冊失敗，請檢查您的輸入。')
    else:
        form = UserRegisterForm()
    return render(request, 'dreams/register.html', {'form': form})

# ====================================================================================================
# 夢境解析核心功能 (Dream Interpretation Core)
# ====================================================================================================

@login_required
def dream_form(request):
    dreams = []
    dream_content_from_audio = ""
    error_message = None

    if request.user.is_authenticated:
        dreams = Dream.objects.filter(user=request.user).order_by('-created_at')[:7]

    if request.method == 'POST':
        form = DreamForm(request.POST, request.FILES)
        
        if 'submit_dream' in request.POST:
            dream_content = request.POST.get('dream_content', '').strip()

            if not dream_content:
                error_message = "夢境內容不能為空，請輸入或上傳音檔轉文字。"
                return render(request, 'dreams/dream_form.html', {
                    'form': DreamForm(request.POST),
                    'dreams': dreams,
                    'error_message': error_message,
                    'dream_content': dream_content_from_audio
                })
            
            try:
                interpretation, emotions, mental_health_advice = interpret_dream(dream_content)

                if emotions:
                    dream = Dream(
                        user=request.user,
                        dream_content=dream_content,
                        interpretation=interpretation,
                        stress_index=random.randint(30, 80),
                        emotion_score=sum(emotions.values()),
                        Happiness=emotions.get("快樂", 0),
                        Anxiety=emotions.get("焦慮", 0),
                        Fear=emotions.get("恐懼", 0),
                        Excitement=emotions.get("興奮", 0),
                        Sadness=emotions.get("悲傷", 0),
                        advice=mental_health_advice
                    )
                    dream.save()

                    # --- 成就解鎖邏輯 ---
                    user = request.user
                    user_parsed_dreams_count = Dream.objects.filter(user=user).count()
                    
                    parse_achievements = Achievement.objects.filter(condition_key='parse_count')
                    
                    for achievement in parse_achievements:
                        if user_parsed_dreams_count >= achievement.condition_value:
                            user_achievement, created = UserAchievement.objects.get_or_create(
                                user=user,
                                achievement=achievement
                            )
                            if created:
                                messages.success(request, f"恭喜您解鎖了成就：『{achievement.name}』！您獲得了稱號：『{achievement.title}』！")
                                if user.userprofile.current_title is None and achievement.title:
                                    user.userprofile.current_title = achievement.title
                                    user.userprofile.save()
                    # --- 成就解鎖邏輯結束 ---

                    return redirect('dream_detail', dream_id=dream.id)

                else:
                    error_message = "夢境解析失敗，請稍後再試或檢查夢境內容是否清晰。"
                    return render(request, 'dreams/dream_form.html', {
                        'form': DreamForm(request.POST),
                        'dreams': dreams,
                        'error_message': error_message,
                        'dream_content': dream_content
                    })

            except Exception as e:
                logging.error(f"夢境解析或保存時發生未預期錯誤: {e}", exc_info=True)
                error_message = f"處理您的請求時發生錯誤：{e}"
                return render(request, 'dreams/dream_form.html', {
                    'form': DreamForm(request.POST),
                    'dreams': dreams,
                    'error_message': error_message,
                    'dream_content': dream_content
                })
        
        else:
            error_message = "無效的表單提交，請確保您點擊的是『解析夢境』按鈕。"
            return render(request, 'dreams/dream_form.html', {
                'form': DreamForm(request.POST),
                'dreams': dreams,
                'error_message': error_message,
                'dream_content': dream_content
            })

    else:
        form = DreamForm()
        dream_content = "" 

    return render(request, 'dreams/dream_form.html', {
        'form': form,
        'dreams': dreams,
        'dream_content': dream_content,
        'error_message': error_message
    })

@login_required
def upload_audio(request):
    """接收音檔並轉換為文字 (透過 AJAX 請求)"""
    if request.method == "POST" and request.FILES.get("audio_file"):
        audio_file = request.FILES["audio_file"]
        try:
            wav_audio = convert_to_wav(audio_file)
            recognizer = sr.Recognizer()

            with sr.AudioFile(wav_audio) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language="zh-TW")

            return JsonResponse({"success": True, "dream_content": text})

        except sr.UnknownValueError:
            return JsonResponse({"success": False, "error": "無法識別音檔內容"})
        except sr.RequestError as e:
            logging.error(f"語音識別服務請求錯誤: {e}", exc_info=True)
            return JsonResponse({"success": False, "error": f"語音識別服務無法訪問: {e}"})
        except Exception as e:
            logging.error(f"音檔處理錯誤: {e}", exc_info=True)
            return JsonResponse({"success": False, "error": f"音檔處理錯誤: {e}"})

    return JsonResponse({"success": False, "error": "未收到音檔或無效請求"}, status=400)


# ====================================================================================================
# 夢境數據與趨勢 (Dream Data & Trends)
# ====================================================================================================

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

def get_user_keywords(request):
    user = request.user
    dreams = Dream.objects.filter(user=user)
    all_words = []

    for dream in dreams:
        content = dream.dream_content
        words = jieba.cut(content)
        all_words.extend(list(words))

    stopwords = ['的', '是', '了', '在', '和', '我', '你', '他', '她', '它', '們', '一個', '一個個', '一些', '一些些']
    filtered_words = [word for word in all_words if word not in stopwords and len(word) > 1]

    word_counts = Counter(filtered_words)
    top_keywords = dict(word_counts.most_common(8))

    result = [{"keyword": key, "count": value} for key, value in top_keywords.items()]
    return JsonResponse(result, safe=False)

def get_global_trends_data(request):
    trend_entries = DreamTrend.objects.all()

    if trend_entries:
        all_trends = {}
        for trend_entry in trend_entries:
            if isinstance(trend_entry.trend_data, dict):
                trend_dict = trend_entry.trend_data
            else:
                try:
                    trend_dict = json.loads(trend_entry.trend_data)
                except json.JSONDecodeError:
                    trend_dict = {}
            
            for keyword, percentage in trend_dict.items():
                if keyword in all_trends:
                    all_trends[keyword] += percentage
                else:
                    all_trends[keyword] = percentage

        top_8 = sorted(all_trends.items(), key=lambda x: x[1], reverse=True)[:8]
        trend_data = [{'text': k, 'percentage': v} for k, v in top_8]
    else:
        trend_data = []

    return JsonResponse(trend_data, safe=False)

def get_emotion_data(request):
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
        
        stress_index = (total_stress_score / len(self.dreams)) * 10 if self.dreams else 0
        return min(stress_index, 100)
    
    def generate_health_recommendations(self, stress_index):
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

# ====================================================================================================
# 夢境歷史與詳情 (Dream History & Detail)
# ====================================================================================================

@login_required
def dream_history(request):
    query = request.GET.get('q')
    dreams = Dream.objects.filter(user=request.user)

    if query:
        dreams = dreams.filter(Q(dream_content__icontains=query) | Q(interpretation__icontains=query))

    paginator = Paginator(dreams.order_by('-created_at'), 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dreams/dream_history.html', {
        'page_obj': page_obj,
        'query': query,
    })

@login_required
def dream_detail(request, dream_id):
    try:
        dream = Dream.objects.get(id=dream_id, user=request.user)
        return render(request, 'dreams/dream_detail.html', {'dream': dream})
    except Dream.DoesNotExist:
        messages.error(request, '找不到指定的夢境記錄')
        return redirect('dream_history')

def get_dream_detail_ajax(request, dream_id):
    dream = get_object_or_404(Dream, id=dream_id)
    return JsonResponse({
        "created_at": dream.created_at.strftime("%Y-%m-%d %H:%M"),
        "dream_content": dream.dream_content,
        "interpretation": dream.interpretation,
    })

# ====================================================================================================
# 夢境心理健康診斷 (Dream Mental Health Diagnosis)
# ====================================================================================================

@login_required
def mental_health_dashboard(request):
    dreams = Dream.objects.filter(user=request.user)

    selected_dream = None
    mental_health_advice = None
    emotion_alert = None

    if request.method == 'POST':
        dream_id = request.POST.get('dream_id')
        selected_dream = get_object_or_404(Dream, id=dream_id, user=request.user)
        
        if selected_dream.advice:
            mental_health_advice = selected_dream.advice
        else:
            mental_health_advice = generate_mental_health_advice_internal(
                selected_dream.dream_content,
                selected_dream.Happiness,
                selected_dream.Anxiety,
                selected_dream.Fear,
                selected_dream.Excitement,
                selected_dream.Sadness
            )
            selected_dream.advice = mental_health_advice
            selected_dream.save()

        if (selected_dream.Anxiety >= 70 or 
            selected_dream.Fear >= 70 or 
            selected_dream.Sadness >= 70):
            emotion_alert = "🚨 <strong>情緒警報：</strong> 您的夢境顯示 <strong>焦慮、恐懼或悲傷</strong> 指數偏高，建議您多關注自己的心理健康，必要時可尋求專業協助。"

    return render(request, 'dreams/mental_health_dashboard.html', {
        'dreams': dreams,
        'selected_dream': selected_dream,
        'mental_health_advice': mental_health_advice,
        'emotion_alert': emotion_alert
    })

def generate_mental_health_advice_internal(dream_content, happiness, anxiety, fear, excitement, sadness):
    advice = []

    dream_patterns = {
        "掉牙": "🦷 **夢見掉牙** 可能代表焦慮或變化，建議檢視近期壓力來源，調整步步。",
        "飛行": "✈️ **夢見飛行** 可能象徵對自由的渴望，或是逃避現實壓力。",
        "被追逐": "🏃 **夢見被追逐** 可能表示內心壓力較大，建議透過放鬆技巧來調適。",
        "迷路": "🗺️ **夢見迷路** 可能代表缺乏方向感，建議整理思緒，設定明確目標。",
        "考試": "📖 **夢見考試** 可能代表擔憂表現或對未來的不確定感。"
    }

    for keyword, response in dream_patterns.items():
        if keyword in dream_content:
            advice.append(response)

    emotion_scores = {
        "快樂": happiness,
        "焦慮": anxiety,
        "恐懼": fear,
        "興奮": excitement,
        "悲傷": sadness
    }
    
    highest_emotion = max(emotion_scores, key=emotion_scores.get)
    # highest_value = emotion_scores[highest_emotion] # 這一行似乎未被使用

    emotion_advice = {
        "快樂": "😃 您最近感到快樂！建議記錄每天的幸福時刻，幫助增強正向情緒。",
        "焦慮": "⚠️ 焦慮指數較高，可以嘗試『呼吸練習』或每日 10 分鐘正念冥想來減壓。",
        "恐懼": "😨 恐懼感較強，可能對未來或未知事物感到不安，建議寫下擔憂，嘗試逐步面對。",
        "興奮": "🚀 興奮感較高！ 這可能代表您對未來充滿期待，建議好好規劃並利用這份能量。",
        "悲傷": "💙 悲傷指數較高，建議與信任的朋友聊天，或透過寫日記來整理情緒。"
    }

    advice.append(emotion_advice[highest_emotion])

    resource_recommendations = {
        "快樂": ["💡 推薦書籍：《快樂的習慣》，幫助您維持正向心態。"],
        "焦慮": ["📖 推薦書籍：《焦慮解方》，學習如何有效應對焦慮情緒。"],
        "恐懼": ["🎭 推薦心理工具：暴露療法，幫助您逐步適應恐懼源。"],
        "興奮": ["🔖 推薦管理方法：番茄鐘時間管理，將興奮轉化為生產力。"],
        "悲傷": ["🎵 音樂療法推薦：聆聽輕音樂有助於穩定情緒，如 Lo-Fi 或古典樂。"]
    }

    advice.append(random.choice(resource_recommendations[highest_emotion]))

    return " ".join(advice)

# ====================================================================================================
# 社群功能 (Community Features)
# ====================================================================================================

def community(request):
    """夢境社群主頁 - 顯示熱門或最新貼文和全球趨勢"""
    sort_type = request.GET.get('sort', 'popular')

    if sort_type == 'latest':
        dream_posts = DreamPost.objects.order_by('-created_at')[:10]
    else:
        dream_posts = DreamPost.objects.order_by('-view_count')[:10]

    trend_data = DreamTrend.objects.filter(date=timezone.now().date()).first()
    if trend_data:
        if isinstance(trend_data.trend_data, str):
            try:
                trend_data = json.loads(trend_data.trend_data)
            except json.JSONDecodeError:
                trend_data = {}
        else:
            trend_data = trend_data.trend_data
    else:
        trend_data = {}

    top_8_trend_data = dict(sorted(trend_data.items(), key=lambda item: item[1], reverse=True)[:8])

    return render(request, 'dreams/community.html', {
        'dream_posts': dream_posts,
        'trend_data': top_8_trend_data,
        'sort_type': sort_type,
    })

@login_required
def share_dream(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        tags_raw = request.POST.getlist('tags')

        dream_post = DreamPost.objects.create(
            title=title,
            content=content,
            user=request.user if not is_anonymous else None,
            is_anonymous=is_anonymous,
        )

        for tag_name in tags_raw:
            tag, created = DreamTag.objects.get_or_create(name=tag_name.strip())
            dream_post.tags.add(tag)

        messages.success(request, '您的夢境貼文已成功分享！')
        return redirect('dream_community')

    popular_tags = DreamTag.objects.annotate(
        num_posts=Count('dreampost')
    ).order_by('-num_posts')[:20]

    return render(request, 'dreams/share_dream.html', {
        'popular_tags': popular_tags
    })

@login_required
def my_posts(request):
    my_posts = DreamPost.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dreams/my_posts.html', {'my_posts': my_posts})

@login_required
def edit_dream_post(request, post_id):
    dream_post = get_object_or_404(DreamPost, id=post_id)

    if dream_post.user != request.user:
        messages.error(request, "您沒有權限編輯這篇貼文。")
        return redirect('dream_post_detail', post_id=post_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous', 'off') == 'on'
        tags_raw = request.POST.getlist('tags')

        dream_post.title = title
        dream_post.content = content
        dream_post.is_anonymous = is_anonymous
        dream_post.user = None if is_anonymous else request.user
        dream_post.save()

        dream_post.tags.clear()
        for tag_name in tags_raw:
            tag, created = DreamTag.objects.get_or_create(name=tag_name.strip())
            dream_post.tags.add(tag)

        messages.success(request, "貼文已更新！")
        return redirect('dream_post_detail', post_id=dream_post.id)

    popular_tags = DreamTag.objects.annotate(
        usage_count=Count('dreampost')
    ).order_by('-usage_count')[:20]

    return render(request, 'dreams/edit_dream_post.html', {
        'dream_post': dream_post,
        'popular_tags': popular_tags
    })

@login_required
def delete_dream_post(request, post_id):
    post = get_object_or_404(DreamPost, id=post_id)
    
    if post.user != request.user:
        messages.error(request, "您沒有權限刪除這篇貼文。")
        return redirect('dream_post_detail', post_id=post_id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "貼文已成功刪除！")
        return redirect('my_posts')

    messages.warning(request, "無效的刪除請求。")
    return redirect('my_posts')

def search_dreams(request):
    query = request.GET.get('q', '')
    
    dreams = DreamPost.objects.all()

    if query:
        dreams = dreams.filter(
            Q(content__icontains=query) | 
            Q(title__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'dreams/search_results.html', {
        'dreams': dreams,
        'query': query
    })

def dream_post_detail(request, post_id):
    dream_post = get_object_or_404(DreamPost, id=post_id)
    
    dream_post.increase_view_count()
    
    comments = dream_post.comments.all()
    
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
        else:
            messages.error(request, '評論內容不能為空。')
            
    return render(request, 'dreams/dream_post_detail.html', {
        'dream': dream_post,
        'comments': comments,
        'similar_dreams': similar_dreams
    })

def get_similar_dreams(dream_post, limit=5):
    if dream_post.tags.exists():
        tag_based_dreams = DreamPost.objects.filter(
            tags__in=dream_post.tags.all()
        ).exclude(id=dream_post.id).distinct().order_by('-created_at')[:limit]
        if tag_based_dreams.count() > 0:
            return tag_based_dreams
    
    return DreamPost.objects.exclude(id=dream_post.id).order_by('-view_count')[:limit]

def update_dream_trends():
    today = timezone.now().date()
    
    time_threshold = timezone.now() - timezone.timedelta(hours=24)
    recent_dreams = DreamPost.objects.filter(created_at__gte=time_threshold)
    
    all_words = []
    for dream in recent_dreams:
        words = jieba.cut(dream.content)
        all_words.extend(list(words))
    
    filtered_words = [word for word in all_words if word not in stopwords_chinese and len(word) > 1]
    
    word_counts = Counter(filtered_words)
    top_keywords = dict(word_counts.most_common(20))
    
    trend, created = DreamTrend.objects.get_or_create(
        date=today,
        defaults={'trend_data': top_keywords}
    )
    
    if not created:
        trend.trend_data = top_keywords
        trend.save()

# ====================================================================================================
# 夢境與相關新聞 (Dream & News)
# ====================================================================================================

def dream_news(request):
    news_results = []
    
    if request.method == 'POST':
        dream_input = request.POST.get('dream_input')

        if not dream_input:
            messages.error(request, "請輸入夢境內容以查找相關新聞。")
            return render(request, 'dreams/dream_news.html', {'news_results': news_results})

        try:
            news_api_url = f'https://newsapi.org/v2/everything?q={dream_input}&language=zh&apiKey={NEWS_API_KEY}'
            response = requests.get(news_api_url, timeout=10)
            response.raise_for_status()
            news_data = response.json()

            logging.info(f"NewsAPI Response for '{dream_input}': {news_data}")

            if news_data.get('status') == 'ok':
                articles = news_data.get('articles', [])
                if not articles:
                    messages.info(request, "很抱歉，沒有找到與您的夢境相關的新聞。")
                else:
                    documents = [dream_input] + [a['title'] + " " + (a['description'] if a['description'] else '') for a in articles]
                    
                    if len(documents) > 1:
                        vectorizer = TfidfVectorizer(stop_words=stopwords_chinese)
                        tfidf_matrix = vectorizer.fit_transform(documents)

                        dream_vector = tfidf_matrix[0:1]
                        article_vectors = tfidf_matrix[1:]

                        similarities = cosine_similarity(dream_vector, article_vectors)[0] * 100

                        for i, article in enumerate(articles):
                            similarity_score = similarities[i]
                            if similarity_score > 0:
                                news_results.append({
                                    'title': article['title'],
                                    'description': article['description'],
                                    'url': article['url'],
                                    'similarity_score': round(similarity_score, 2)
                                })
                    else:
                        messages.warning(request, "新聞資料不足，無法進行相似度分析。")

                news_results.sort(key=lambda x: x['similarity_score'], reverse=True)

        except requests.exceptions.Timeout:
            messages.error(request, "請求新聞服務超時，請稍後再試。")
            logging.error("NewsAPI request timed out.")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"無法連接新聞服務：{e}")
            logging.error(f"Error connecting to NewsAPI: {e}", exc_info=True)
        except Exception as e:
            messages.error(request, f"處理新聞時發生錯誤：{e}")
            logging.error(f"Unexpected error in dream_news: {e}", exc_info=True)

    return render(request, 'dreams/dream_news.html', {'news_results': news_results})

# ====================================================================================================
# 諮詢與心理師 (Consultation & Counselors)
# ====================================================================================================

def consultation_chat(request):
    """新的諮詢對話介紹頁面 (Landing Page)"""
    return render(request, 'dreams/consultation_chat.html')

def chat_with_counselor_view(request, counselor_id):
    """與特定諮詢師的聊天頁面"""
    counselor = get_object_or_404(Counselor, id=counselor_id) # 這裡修正了 counselor_id 拼寫
    return render(request, 'dreams/chat_with_counselor.html', {
        'counselor': counselor
    })

def counselor_list_view(request):
    """諮詢師列表頁面"""
    counselors = Counselor.objects.all()
    return render(request, 'dreams/counselor_list.html', {
        'counselors': counselors
    })

# ====================================================================================================
# 用戶設定與成就 (User Settings & Achievements)
# ====================================================================================================

@login_required
def user_profile(request):
    """用戶個人檔案頁面"""
    user_profile_instance, created = UserProfile.objects.get_or_create(user=request.user)
    
    unlocked_achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement').order_by('-unlocked_at')

    if request.method == 'POST':
        selected_title = request.POST.get('selected_title')
        selected_badge = request.POST.get('selected_badge')

        if selected_title:
            user_profile_instance.current_title = selected_title
        if selected_badge:
            user_profile_instance.current_badge_icon = selected_badge
        user_profile_instance.save()
        messages.success(request, "您的個人檔案已更新！")
        return redirect('profile')

    available_titles = set()
    available_badges = set()
    for ua in unlocked_achievements:
        if ua.achievement.title:
            available_titles.add(ua.achievement.title)
        if ua.achievement.badge_icon:
            available_badges.add(ua.achievement.badge_icon)

    context = {
        'user_profile': user_profile_instance,
        'unlocked_achievements': unlocked_achievements,
        'available_titles': sorted(list(available_titles)),
        'available_badges': sorted(list(available_badges)),
    }
    return render(request, 'dreams/profile.html', context)

@login_required
def user_achievements(request):
    user = request.user
    
    unlocked_achievements = UserAchievement.objects.filter(user=user).select_related('achievement').order_by('-unlocked_at')

    user_parsed_dreams_count = Dream.objects.filter(user=user).count()

    parse_achievements = Achievement.objects.filter(condition_key='parse_count').order_by('condition_value')

    achievements_progress = []
    for achievement in parse_achievements:
        is_unlocked = UserAchievement.objects.filter(user=user, achievement=achievement).exists()
        current_progress = min(user_parsed_dreams_count, achievement.condition_value)
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

# ====================================================================================================
# 其他 (Miscellaneous)
# ====================================================================================================

def polls(request):
    return HttpResponse("這是 polls 頁面")