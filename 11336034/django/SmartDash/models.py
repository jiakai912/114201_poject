from django.db import models

class ScamMessage(models.Model):
    text = models.TextField()  # 使用者輸入的訊息
    risk_score = models.FloatField()  # AI 判斷的詐騙風險分數 (0-1)
    category = models.CharField(max_length=50, choices=[  # 詐騙類型
        ('phishing', '釣魚詐騙'),
        ('investment', '投資詐騙'),
        ('shopping', '購物詐騙'),
        ('loan', '貸款詐騙'),
        ('other', '其他')
    ], default='other')
    keywords = models.TextField(blank=True, null=True)  # AI 偵測到的關鍵字
    source = models.CharField(max_length=100, blank=True, null=True)  # 訊息來源 (如 Email, SMS, 社群平台)
    is_verified_scam = models.BooleanField(default=False)  # 是否為人工確認的詐騙訊息
    created_at = models.DateTimeField(auto_now_add=True)  # 訊息提交時間

    def __str__(self):
        return f"Message ID {self.id} - Risk: {self.risk_score} - Type: {self.category}"
