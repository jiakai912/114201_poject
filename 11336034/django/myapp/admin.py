# admin.py
from django.contrib import admin
from .models import Dashboard  # 改為引用新模型名稱

# 這裡注冊新的模型
admin.site.register(Dashboard)

from .models import Dream
@admin.register(Dream)
class DreamAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'keywords', 'sentiment', 'interpretation')
    search_fields = ('dream_text', 'keywords', 'sentiment', 'interpretation')
