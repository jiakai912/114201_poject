from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Dream
from .models import UserProfile 


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


class UserProfileForm(forms.ModelForm):
    # 如果您在 UserProfile 中有 bio 和 avatar 字段，可以在這裡加入
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '寫一些關於您自己的內容...'}), required=False)
    avatar = forms.ImageField(required=False, help_text="上傳您的頭像圖片")

    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'current_title', 'current_badge_icon'] # 包含所有可編輯的字段

        widgets = {
            'current_title': forms.Select(attrs={'class': 'form-select'}), # 將稱號顯示為下拉選單
            'current_badge_icon': forms.Select(attrs={'class': 'form-select'}), # 將徽章顯示為下拉選單
        }
    
    # 這裡可以根據已解鎖的成就動態設置稱號和徽章的選項
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            # 獲取用戶已解鎖的成就，並提取可選的稱號和徽章
            unlocked_achievements = self.instance.user.userachievement_set.select_related('achievement')
            
            available_titles = set()
            available_badges = set()

            for ua in unlocked_achievements:
                if ua.achievement.title:
                    available_titles.add((ua.achievement.title, ua.achievement.title)) # (value, display_text)
                if ua.achievement.badge_icon:
                    available_badges.add((ua.achievement.badge_icon, ua.achievement.name + ' (' + ua.achievement.badge_icon + ')')) # 顯示徽章名稱和圖標類

            self.fields['current_title'].choices = [('', '--- 選擇稱號 ---')] + sorted(list(available_titles))
            self.fields['current_badge_icon'].choices = [('', '--- 選擇徽章 ---')] + sorted(list(available_badges))