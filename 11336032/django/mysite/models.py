from django.db import models # 匯入 Django 的 models 模組

class Dashboard(models.Model): # 定義 Dashboard 模型
    name = models.CharField(max_length=100) # 定義 name 欄位
    description = models.TextField() # 定義 description 欄位
    kpi_name = models.CharField(max_length=100) # 定義 kpi_name 欄位
    value = models.FloatField() # 定義 value 欄位
    date = models.DateField() # 定義 date 欄位

    def __str__(self): # 定義 __str__ 方法
        return self.name # 回傳 name 欄位的值
