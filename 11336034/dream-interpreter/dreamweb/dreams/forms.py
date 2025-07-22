from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Dream
from .models import UserProfile, Achievement, UserAchievement # 確保 Achievement 和 UserAchievement 也被匯入，以便動態稱號/徽章功能

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
    # 新增 email 字段，這會對應到 User 模型上的 email
    email = forms.EmailField(required=True, label="電子郵件",
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '您的電子郵件地址'}))
    
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '寫一些關於您自己的內容...'}), required=False)
    avatar = forms.ImageField(required=False, help_text="上傳您的頭像圖片")

    class Meta:
        model = UserProfile
        # 這裡的 fields 仍然是 UserProfile 模型的字段
        fields = ['bio', 'avatar', 'current_title', 'current_badge_icon'] 

        widgets = {
            'current_title': forms.Select(attrs={'class': 'form-select'}),
            'current_badge_icon': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化 email 字段的值，從關聯的 User 物件中獲取
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            # 獲取用戶已解鎖的成就，並提取可選的稱號和徽章
            unlocked_achievements = self.instance.user.userachievement_set.select_related('achievement')
            
            available_titles = set()
            available_badges = set()

            for ua in unlocked_achievements:
                if ua.achievement.title:
                    available_titles.add((ua.achievement.title, ua.achievement.title))
                if ua.achievement.badge_icon:
                    # 對於徽章圖標，將圖標 class 作為值，名稱和圖標作為顯示標籤
                    available_badges.add((ua.achievement.badge_icon, f"{ua.achievement.name} ({ua.achievement.badge_icon})"))

            # 確保 choices 被正確設定
            self.fields['current_title'].choices = [('', '--- 選擇稱號 ---')] + sorted(list(available_titles))
            self.fields['current_badge_icon'].choices = [('', '--- 選擇徽章 ---')] + sorted(list(available_badges))

    def save(self, commit=True):
        # 先保存 UserProfile 的部分，但不提交到資料庫
        user_profile = super().save(commit=False)

        # 處理 email 字段，更新到 User 模型
        email = self.cleaned_data.get('email')
        if email and user_profile.user.email != email: # 檢查 email 是否有變化
            user_profile.user.email = email
            user_profile.user.save() # 保存 User 模型的更改

        # --- BEGIN MODIFICATION ---
        # 明確地將選定的稱號和徽章值從 cleaned_data 賦予到 user_profile 實例
        user_profile.current_title = self.cleaned_data.get('current_title', '')
        user_profile.current_badge_icon = self.cleaned_data.get('current_badge_icon', '')
        # --- END MODIFICATION ---

        if commit:
            user_profile.save() # 提交 UserProfile 的更改
        
        return user_profile
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

            # --- 臨時診斷打印 ---
            print(f"DEBUG in UserProfileForm.__init__: Form Initialized for user {self.instance.user.username}")
            unlocked_achievements = self.instance.user.userachievement_set.select_related('achievement')
            print(f"DEBUG in UserProfileForm.__init__: unlocked_achievements count from form: {unlocked_achievements.count()}")
            for ua in unlocked_achievements:
                print(f"DEBUG in UserProfileForm.__init__: Form sees Unlocked Achievement: {ua.achievement.name} (Title: {ua.achievement.title}, Icon: {ua.achievement.badge_icon})")
            # --- 臨時診斷打印結束 ---

            available_titles = set()
            available_badges = set()

            for ua in unlocked_achievements:
                if ua.achievement.title:
                    available_titles.add((ua.achievement.title, ua.achievement.title))
                if ua.achievement.badge_icon:
                    available_badges.add((ua.achievement.badge_icon, f"{ua.achievement.name} ({ua.achievement.badge_icon})"))

            self.fields['current_title'].choices = [('', '--- 選擇稱號 ---')] + sorted(list(available_titles))
            self.fields['current_badge_icon'].choices = [('', '--- 選擇徽章 ---')] + sorted(list(available_badges))