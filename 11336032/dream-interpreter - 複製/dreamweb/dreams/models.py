from django.db import models
from django.contrib.auth.models import User
from django.db.models import F

class Dream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dream_content = models.TextField(verbose_name="夢境內容")
    interpretation = models.TextField(verbose_name="解析結果")
    stress_index = models.IntegerField(default=0, verbose_name="壓力指數")
    
    # 修正情緒對應名稱
    emotion_score = models.FloatField(default=0, verbose_name="情緒得分 (%)")
    Happiness = models.FloatField(default=0, verbose_name="快樂 (%)")
    Anxiety  = models.FloatField(default=0, verbose_name="焦慮 (%)")
    Fear = models.FloatField(default=0, verbose_name="恐懼 (%)")
    Excitement = models.FloatField(default=0, verbose_name="興奮 (%)")
    Sadness = models.FloatField(default=0, verbose_name="悲傷 (%)")

    advice = models.TextField(verbose_name="心理診斷個人化建議", blank=True, null=True)  # 新增欄位
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "夢境"
        verbose_name_plural = "夢境"

    def __str__(self):
        return f"{self.user.username}'的夢境 - {self.created_at.strftime('%Y-%m-%d')}"


class DreamPost(models.Model):
    """夢境貼文與社群功能"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # 可匿名
    content = models.TextField(verbose_name="夢境內容")  # 夢境內容
    title = models.CharField(max_length=100, default="", verbose_name="標題")
    is_anonymous = models.BooleanField(default=False, verbose_name="匿名發布")  # 是否匿名
    view_count = models.IntegerField(default=0, verbose_name="瀏覽次數")
    tags = models.ManyToManyField('DreamTag', blank=True, verbose_name="標籤")
    emotion_data = models.JSONField(default=dict, blank=True, verbose_name="情緒數據")  # 儲存情緒 JSON
    advice = models.TextField(verbose_name="心理診斷個人化建議", blank=True, null=True)  # 心理建議
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "夢境貼文"
        verbose_name_plural = "夢境貼文"

    def __str__(self):
        return f"夢境貼文: {'匿名' if self.is_anonymous else self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"

    def increase_view_count(self):
        DreamPost.objects.filter(id=self.id).update(view_count=F('view_count') + 1)
        self.refresh_from_db(fields=['view_count'])  # 讓 self.view_count 拿到更新後的實際值


class DreamComment(models.Model):
    """夢境評論"""
    dream_post = models.ForeignKey(DreamPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="評論內容")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = "夢境評論"
        verbose_name_plural = "夢境評論"

    def __str__(self):
        return f"{self.user.username}對夢境的評論 - {self.created_at.strftime('%Y-%m-%d')}"


class DreamTag(models.Model):
    """夢境標籤"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class DreamTrend(models.Model):
    """全球夢境趨勢"""
    date = models.DateField(unique=True)
    trend_data = models.JSONField(verbose_name="趨勢數據")  # 存儲當天熱門夢境關鍵詞和數量

    class Meta:
        ordering = ['-date']
        verbose_name = "夢境趨勢"
        verbose_name_plural = "夢境趨勢"

    def __str__(self):
        return f"夢境趨勢 - {self.date}"


class DreamRecommendation(models.Model):
    """夢境推薦"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    recommended_dreams = models.ManyToManyField(DreamPost, related_name='recommended_to')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "夢境推薦"
        verbose_name_plural = "夢境推薦"
        unique_together = ('user', 'created_at')  # 避免同一天多次推薦

    def __str__(self):
        return f"{self.user.username}的夢境推薦 - {self.created_at.strftime('%Y-%m-%d')}"


# 新增 Counselor 模型
class Counselor(models.Model):
    name = models.CharField(max_length=100, verbose_name="諮詢師姓名")
    specialty = models.CharField(max_length=200, verbose_name="專長領域")
    description = models.TextField(verbose_name="簡介", blank=True, null=True)
    image_url = models.URLField(verbose_name="頭像圖片網址", blank=True, null=True)

    class Meta:
        verbose_name = "諮詢師"
        verbose_name_plural = "諮詢師"

    def __str__(self):
        return self.name
    




class Achievement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    # 可以用來分類成就，例如 '解析', '活躍', '社群'
    category = models.CharField(max_length=50, default='General')
    # 稱號
    title = models.CharField(max_length=50, blank=True, null=True)
    # 徽章圖標的檔案路徑或 FontAwesome class
    badge_icon = models.CharField(max_length=100, blank=True, null=True)
    # 達成條件的關鍵字，例如 'parse_count', 'login_streak'
    condition_key = models.CharField(max_length=50)
    # 達成條件的數值，例如 5, 20, 100
    condition_value = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement') # 確保每個用戶只能解鎖一次同一成就

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

# dreams/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.signals import post_save # 確保只導入 post_save
from django.dispatch import receiver

# ... (現有的 Dream, DreamPost 等模型定義)

# 新增 UserProfile 模型
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 用戶當前選擇的稱號
    current_title = models.CharField(max_length=50, blank=True, null=True, verbose_name="當前稱號")
    # 用戶當前選擇的徽章圖標 (可以存儲 FontAwesome class 或圖片路徑)
    current_badge_icon = models.CharField(max_length=100, blank=True, null=True, verbose_name="當前徽章圖標")
    # 您可以根據需要添加其他用戶資料欄位，例如：
    # bio = models.TextField(blank=True, null=True, verbose_name="個人簡介")
    # avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="頭像")

    def __str__(self):
        return f"{self.user.username}'s Profile"

# 確保在 User 創建時自動創建 UserProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    # 不需要 instance.userprofile.save() 這行，因為它會導致循環或 RelatedObjectDoesNotExist

# dreams/models.py

# ... (確保您已導入其他必要的模組，如 User, models)
from django.db import models
from django.contrib.auth.models import User # 確保有這個
# ... (您的其他模型，如 Dream, UserProfile 等)


class Achievement(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="成就名稱")
    description = models.TextField(verbose_name="成就描述")
    category = models.CharField(max_length=50, default='General', verbose_name="類別")
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name="稱號")
    badge_icon = models.CharField(max_length=100, blank=True, null=True, verbose_name="徽章圖標")
    condition_key = models.CharField(max_length=50, verbose_name="條件鍵") # 例如 'parse_count'
    condition_value = models.IntegerField(default=1, verbose_name="條件值") # 例如 5, 20, 100

    class Meta:
        verbose_name = "成就"
        verbose_name_plural = "成就"
        ordering = ['condition_value'] # 依條件值排序，方便展示進度

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用戶")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, verbose_name="成就")
    unlocked_at = models.DateTimeField(auto_now_add=True, verbose_name="解鎖時間")

    class Meta:
        unique_together = ('user', 'achievement')
        verbose_name = "用戶成就"
        verbose_name_plural = "用戶成就"

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

# ... (UserProfile 模型和相關信號處理，確保它們正確無誤)
# 確保 UserProfile 的模型已經創建，並且與 User 關聯正確，且現有用戶已有 UserProfile 實例。