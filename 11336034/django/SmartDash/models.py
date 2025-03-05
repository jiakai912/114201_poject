# models.py
from django.db import models
from django.utils import timezone

class Dashboard(models.Model):  # 將模型名稱改為 Dashboard
    KPI_CHOICES = [
        ("產量達成率", "產量達成率"),
        ("工時效率", "工時效率"),
        ("生產成本偏差率", "生產成本偏差率"),
        ("銷售退貨率", "銷售退貨率"),
        ("進貨單價", "進貨單價"),
        ("委外加工退貨率", "委外加工退貨率"),
        ("離職率", "離職率"),
        ("庫存水位", "庫存水位"),
    ]
    
    kpi_name = models.CharField(max_length=50, choices=KPI_CHOICES, default="產量達成率")
    value = models.FloatField(default=0.0)
    date = models.DateField(default=timezone.now)  # ✅ 加上預設值，避免錯誤

    class Meta:
        db_table = 'dashboard'  # 指定新的資料表名稱為 'dashboard'

    def __str__(self):
        return f"{self.kpi_name} - {self.value}"
