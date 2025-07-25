# dreams/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Dream, UserProfile, Achievement, UserAchievement

# 用戶註冊表單，包含心理師身份選項
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_therapist = forms.BooleanField(required=False, label="我是心理師")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_therapist']

class DreamForm(forms.ModelForm):
    audio_file = forms.FileField(required=False)
    dream_content = forms.CharField(widget=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '請詳細描述您的夢境...',
                'rows': 8,
            }), required=False)

    class Meta:
        model = Dream
        fields = ['dream_content', 'audio_file']


# dreams/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Dream, UserProfile, Achievement, UserAchievement

# 用戶註冊表單，包含心理師身份選項
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_therapist = forms.BooleanField(required=False, label="我是心理師")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_therapist']

class DreamForm(forms.ModelForm):
    audio_file = forms.FileField(required=False)
    dream_content = forms.CharField(widget=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '請詳細描述您的夢境...',
                'rows': 8,
            }), required=False)

    class Meta:
        model = Dream
        fields = ['dream_content', 'audio_file']


class UserProfileForm(forms.ModelForm):
    # ✅ FIX: 移除 email 字段，因為它屬於 User 模型，而不是 UserProfile
    # email = forms.EmailField(required=True, label="電子郵件",
    #                          widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '您的電子郵件地址'}))

    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '寫一些關於您自己的內容...'}), required=False)
    avatar = forms.ImageField(required=False, help_text="上傳您的頭像圖片")

    display_title = forms.ModelChoiceField(
        queryset=Achievement.objects.none(),
        required=False,
        label="社群展示稱號",
        empty_label="--- 不顯示稱號 ---",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    display_badge = forms.ModelChoiceField(
        queryset=Achievement.objects.none(),
        required=False,
        label="社群展示徽章",
        empty_label="--- 不顯示徽章 ---",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = UserProfile
        # ✅ FIX: 移除 email 字段
        fields = ['bio', 'avatar', 'display_title', 'display_badge']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # 雖然 email 字段移除了，但這個 user 參數可能用於其他自定義邏輯
        super().__init__(*args, **kwargs)
        if user: # 確保有 user 才過濾成就
            unlocked_achievements_queryset = UserAchievement.objects.filter(user=user).select_related('achievement').order_by('-unlocked_at')

            display_title_choices = [(ua.achievement.id, ua.achievement.title)
                                     for ua in unlocked_achievements_queryset if ua.achievement.title and ua.achievement.title.strip()]
            self.fields['display_title'].queryset = Achievement.objects.filter(id__in=[id for id, _ in display_title_choices])
            self.fields['display_title'].choices = [('', '--- 不顯示稱號 ---')] + display_title_choices

            display_badge_choices = [(ua.achievement.id, f"{ua.achievement.name} ({ua.achievement.badge_icon})")
                                     for ua in unlocked_achievements_queryset if ua.achievement.badge_icon and ua.achievement.badge_icon.strip()]
            self.fields['display_badge'].queryset = Achievement.objects.filter(id__in=[id for id, _ in display_badge_choices])
            self.fields['display_badge'].choices = [('', '--- 不顯示徽章 ---')] + display_badge_choices

            # 設置初始值
            if self.instance.display_title:
                self.fields['display_title'].initial = self.instance.display_title.id
            if self.instance.display_badge:
                self.fields['display_badge'].initial = self.instance.display_badge.id

    def save(self, commit=True):
        user_profile = super().save(commit=False)

        if commit:
            user_profile.save()
        return user_profile