from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from .models import ScamMessage  # 確保從 models 導入 ScamMessage
from .forms import ScamMessageForm
from .utils import analyze_message

def detect_scam(request):
    if request.method == "POST":
        form = ScamMessageForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            analysis = analyze_message(text)

            # 儲存分析結果
            scam_message = ScamMessage.objects.create(
                text=text,
                risk_score=analysis["risk_score"],
                keywords=analysis.get("keywords", ""),  # 確保 keywords 存在
                category=analysis.get("category", "other")  # 若無 category，預設為 "other"
            )
            return redirect('result', message_id=scam_message.id) 

    else:
        form = ScamMessageForm()

    return render(request, "SmartDash/detect_scam.html", {"form": form})
    

def result_view(request, message_id):
    scam_message = get_object_or_404(ScamMessage, id=message_id)  # 根據 ID 查找 ScamMessage 實例
    return render(request, 'SmartDash/result.html', {'message': scam_message})



def dashboard(request):
    messages = ScamMessage.objects.all()
    risk_avg = messages.aggregate(Avg("risk_score"))["risk_score__avg"] or 0  # 若無資料，設預設值 0
    return render(request, "SmartDash/dashboard.html", {"messages": messages, "risk_avg": risk_avg})


# tests.py
from django.test import TestCase
from django.urls import reverse
from .models import ScamMessage

class DetectScamViewTest(TestCase):
    
    def test_valid_post_request(self):
        # 準備有效的 POST 請求數據
        response = self.client.post(reverse('detect_scam'), {'text': 'This is a test scam message'})
        
        # 確保返回 302 重定向，意味著成功提交並重定向到結果頁面
        self.assertEqual(response.status_code, 302)
        
        # 確保數據已儲存在數據庫中
        scam_message = ScamMessage.objects.first()
        self.assertEqual(scam_message.text, 'This is a test scam message')

    def test_invalid_post_request(self):
        # 發送無效的 POST 請求數據
        response = self.client.post(reverse('detect_scam'), {'text': ''})
        
        # 確保表單錯誤並返回 200 狀態碼（即返回到同一頁面）
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')


# tests.py
from django.test import TestCase
from django.urls import reverse
from .models import ScamMessage

class ResultViewTest(TestCase):
    
    def test_result_view(self):
        # 創建一個 ScamMessage 實例
        scam_message = ScamMessage.objects.create(
            text="This is a test result",
            risk_score=90.0,
            keywords="test, result",
            category="scam"
        )
        
        # 測試能否訪問結果頁面
        response = self.client.get(reverse('result', args=[scam_message.id]))
        
        # 確保返回 200 狀態碼
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a test result")


