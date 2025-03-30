from django.db import models
from django.contrib.auth.models import User

class Dream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dream_content = models.TextField(verbose_name="夢境內容")
    interpretation = models.TextField(verbose_name="解析結果")
    stress_index = models.IntegerField(default=0, verbose_name="壓力指數")
    emotion_score = models.FloatField(default=0, verbose_name="情緒得分")
    anxiety = models.FloatField(default=0, verbose_name="焦慮 (%)")
    fear = models.FloatField(default=0, verbose_name="恐懼 (%)")
    surprise = models.FloatField(default=0, verbose_name="驚奇 (%)")
    hope = models.FloatField(default=0, verbose_name="希望 (%)")
    confusion = models.FloatField(default=0, verbose_name="困惑 (%)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "夢境"
        verbose_name_plural = "夢境"

    def __str__(self):
        return f"{self.user.username}的夢境 - {self.created_at.strftime('%Y-%m-%d')}"

    

# 1. 夢境社群相關模型
class DreamComment(models.Model):
    """夢境評論模型"""
    dream_post = models.ForeignKey('DreamPost', on_delete=models.CASCADE, related_name='comments')
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
    """夢境標籤模型"""
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

# 擴展 DreamPost 模型
class DreamPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # 可匿名
    content = models.TextField(verbose_name="夢境內容") # 夢境內容
    title = models.CharField(max_length=100, default="", verbose_name="標題")
    is_anonymous = models.BooleanField(default=False, verbose_name="匿名發布") # 是否匿名
    view_count = models.IntegerField(default=0, verbose_name="瀏覽次數")
    tags = models.ManyToManyField(DreamTag, blank=True, verbose_name="標籤")
    emotion_data = models.JSONField(default=dict, blank=True, verbose_name="情緒數據")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "夢境貼文"
        verbose_name_plural = "夢境貼文"
    
    def __str__(self):
        return f"夢境貼文: {'匿名' if self.is_anonymous else self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def increase_view_count(self):
        """增加瀏覽次數"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

# 2. 全球夢境趨勢分析模型
class DreamTrend(models.Model):
    """夢境趨勢模型"""
    date = models.DateField(unique=True)
    trend_data = models.JSONField(verbose_name="趨勢數據")  # 存儲當天熱門夢境關鍵詞和數量
    
    class Meta:
        ordering = ['-date']
        verbose_name = "夢境趨勢"
        verbose_name_plural = "夢境趨勢"
    
    def __str__(self):
        return f"夢境趨勢 - {self.date}"

# 3. 夢境推薦系統模型
class DreamRecommendation(models.Model):
    """夢境推薦模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    recommended_dreams = models.ManyToManyField(DreamPost, related_name='recommended_to')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "夢境推薦"
        verbose_name_plural = "夢境推薦"
    
    def __str__(self):
        return f"{self.user.username}的夢境推薦 - {self.created_at.strftime('%Y-%m-%d')}"

