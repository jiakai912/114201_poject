# admin.py
from django.contrib import admin
from .models import Dashboard  # 改為引用新模型名稱

# 這裡注冊新的模型
admin.site.register(Dashboard)