from django.db import models
from django.contrib.auth.models import User

class Dream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dream_content = models.TextField(verbose_name="夢境內容")
    interpretation = models.TextField(verbose_name="解析結果")
    stress_index = models.IntegerField(default=0, verbose_name="壓力指數")
    emotion_score = models.FloatField(default=0, verbose_name="情緒得分")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
        verbose_name = "夢境"
        verbose_name_plural = "夢境"
    
    def __str__(self):
        return f"{self.user.username}的夢境 - {self.created_at.strftime('%Y-%m-%d')}"
