from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Dream

# 用戶註冊表單，包含心理師身份選項
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_therapist = forms.BooleanField(required=False, label="我是心理師")  # ← 加這一行

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_therapist']

class DreamForm(forms.ModelForm):
    audio_file = forms.FileField(required=False)  # 音檔為可選填項
    dream_content = forms.CharField(widget=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '請詳細描述您的夢境...',
                'rows': 8,
            }), required=False)  # 將 dream_content 欄位設置為非必填

    class Meta:
        model = Dream
        fields = ['dream_content', 'audio_file']  # 確保這裡列出了需要使用的欄位




