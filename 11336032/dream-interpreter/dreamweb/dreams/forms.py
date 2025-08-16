# dreams/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Dream, UserProfile, Achievement, UserAchievement
from django.core.exceptions import ValidationError

# 管理員編輯
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'is_active']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



# 用戶註冊表單，包含心理師身份選項
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_therapist = forms.BooleanField(required=False, label="我是心理師")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_therapist']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 2 or len(username) > 8:
            raise forms.ValidationError("用戶名必須介於 2 到 8 個字之間")
        return username

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
    class Meta:
        model = UserProfile
        fields = ['is_therapist', 'is_verified_therapist', 'points']
        widgets = {
            'is_therapist': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_verified_therapist': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'points': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class UserProfileForm(forms.ModelForm):
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


    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # 檔案大小限制 (2MB)
            if avatar.size > 2 * 1024 * 1024:
                raise ValidationError("上傳的圖片檔案不能超過 2MB。")

            # 檔案類型限制
            # ✅ FIX: 在存取 content_type 前，檢查它是否存在。對於非上傳檔案，這個屬性不存在。
            # 如果是已經儲存的圖片，cleaned_data.get('avatar') 會是 ImageFieldFile 物件，不需檢查 content_type
            if hasattr(avatar, 'content_type'):
                if not avatar.content_type.startswith('image/'):
                    raise ValidationError("請上傳有效的圖片檔案（例如 JPG, PNG）。")
        return avatar
    
    def save(self, commit=True):
        user_profile = super().save(commit=False)

        if commit:
            user_profile.save()
        return user_profile


class TherapistProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['coin_price']
        labels = {
            'coin_price': '每小時點券價格',
        }
        widgets = {
            'coin_price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class TherapistFullProfileForm(UserProfileForm):
    coin_price = forms.IntegerField(
        required=False,
        label="每小時點券價格",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0})
    )
    specialties = forms.CharField(
        required=False,
        label="專長領域",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '用逗號分隔多個專長，如：焦慮治療, 兒童心理, 認知行為療法'}),
        help_text="用逗號分隔多個專長"
    )

    class Meta(UserProfileForm.Meta):
        fields = UserProfileForm.Meta.fields + ['coin_price', 'specialties']