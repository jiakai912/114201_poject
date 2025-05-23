from django.contrib import admin # 匯入 Django 的 admin 模組
from .models import Dashboard # 匯入 Dashboard 模型

class DashboardAdmin(admin.ModelAdmin): # 定義 DashboardAdmin 類別
    list_display = ('title', 'slug', 'publish_date', 'status') # 設定顯示欄位
admin.site.register(Dashboard) # 註冊 Dashboard 模型
