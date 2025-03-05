from django.db import models

class Dashboard(models.Model):
    # 定义 Dashboard 模型的字段
    name = models.CharField(max_length=100)
    description = models.TextField()
    kpi_name = models.CharField(max_length=100)  # 示例字段
    value = models.FloatField()
    date = models.DateField()
    def __str__(self):
        return self.name
