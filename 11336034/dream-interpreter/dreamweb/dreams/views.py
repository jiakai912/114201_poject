import json
import os
from dotenv import load_dotenv
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from openai import OpenAI  # 導入 OpenAI SDK
from .models import Dream
from .forms import DreamForm, UserRegisterForm
import logging
from django.http import HttpResponse
from django.http import JsonResponse
import random  # 模擬 AI 建議，可替換為 NLP 分析

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

# 在 view 中使用示例
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
            interpretation = interpret_dream(dream_content)
            dream = Dream(user=request.user, dream_content=dream_content, interpretation=interpretation)
            dream.save()
            return render(request, 'dreams/dream_result.html', {'dream': dream})
    else:
        form = DreamForm()
    dreams = Dream.objects.filter(user=request.user)
    return render(request, 'dreams/dream_form.html', {'form': form, 'dreams': dreams})


def interpret_dream(dream_content):
    """
    使用指定的 API 解析夢境內容
    
    Args:
        dream_content (str): 夢境描述
    
    Returns:
        str: 夢境解析結果或錯誤信息
    """
    try:
        # 確保使用正確的 API 客戶端和模型
        response = client.chat.completions.create(
            model="deepseek-chat",  # 確認模型名稱正確
            messages=[
                {
                    "role": "system",
                    "content": "你是一位專業的解夢專家，請根據用戶描述分析夢境內容。請提供：\n"
                    "1. 夢境情緒分析（焦慮、壓力、快樂、悲傷、興奮等，以百分比表示）。\n"
                    "2. AI 解析的關鍵字。\n"
                    "3. 夢境象徵的意義。\n"
                    "請以專業且具深度的方式解析，不要提供建議。"
                },
                {
                    "role": "user",
                    "content": dream_content
                }
            ],
            temperature=0.7,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        # 記錄詳細的錯誤信息
        logging.error(f"夢境解析API調用失敗: {str(e)}", exc_info=True)
        return f"API 調用失敗: {str(e)}"

@login_required
def dream_history(request):
    dreams = Dream.objects.filter(user=request.user)
    return render(request, 'dreams/dream_history.html', {'dreams': dreams})

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

def dream_dashboard(request):
    dreams = Dream.objects.filter(user=request.user)
    return render(request, 'dreams/dream_dashboard.html', {'dreams': dreams})

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


