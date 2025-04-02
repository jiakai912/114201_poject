from django.db import models

class Dashboard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    kpi_name = models.CharField(max_length=100)
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return self.name  #用來定義當Dashboard物件轉換為字串時的顯示內容

class Dream(models.Model):
    dream_text = models.TextField(verbose_name="夢境內容", default="")
    keywords = models.TextField(verbose_name="關鍵字", blank=True)  # 儲存關鍵字，作為字符串
    sentiment = models.CharField(max_length=100, verbose_name="情緒指數", blank=True)  # 情緒指數
    interpretation = models.TextField(verbose_name="心理學解析", blank=True)  # 夢境解析結果
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    def __str__(self):
        return f"夢境解析 - {self.id}"

    class Meta:
        verbose_name = "夢境"
        verbose_name_plural = "夢境"
