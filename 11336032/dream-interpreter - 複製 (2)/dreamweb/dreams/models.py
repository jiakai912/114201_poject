from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# 心理諮商個人資料擴展模型
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)  # 點券餘額
    is_therapist = models.BooleanField(default=False)
    is_verified_therapist = models.BooleanField(default=False) # ✅ 審核心理師註冊
    current_title = models.CharField(max_length=50, blank=True, null=True, verbose_name="當前稱號")
    current_badge_icon = models.CharField(max_length=100, blank=True, null=True, verbose_name="當前徽章圖標")
    
    # 新增 bio 和 avatar 字段
    bio = models.TextField(blank=True, null=True, verbose_name="個人簡介")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="頭像")

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # 改用 get_or_create 避免重複 key 錯誤
        UserProfile.objects.get_or_create(user=instance)

class DreamShareAuthorization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_by')
    therapist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authorized_clients')
    shared_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'therapist')  # 一個使用者只能對一位心理師有一筆紀錄

    def __str__(self):
        return f"{self.user.username} 授權給 {self.therapist.username}"
    

# 個人檔案

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

# 夢境資料庫
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
    is_flagged = models.BooleanField(default=False, verbose_name="是否含有危險字詞")

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



# 心理諮商預約及對話

class TherapyAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    therapist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_appointments')
    scheduled_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} 預約 {self.therapist.username} - {self.scheduled_time}"


class TherapyMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='therapy_sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='therapy_received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}：{self.content[:20]}"



class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_received')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.message[:20]}"
    
    