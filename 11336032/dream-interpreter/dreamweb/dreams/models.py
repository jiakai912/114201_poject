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