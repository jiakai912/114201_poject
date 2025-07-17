from django.contrib import admin
from .models import Dream,UserProfile,Achievement # 確保 Achievement 也被匯入

@admin.register(Dream)
class DreamAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'stress_index', 'emotion_score')
    list_filter = ('user', 'created_at', 'stress_index')
    search_fields = ('dream_content', 'interpretation')
    readonly_fields = ('created_at',)

    fieldsets = (
        ("基本信息", {
            'fields': ('user', 'dream_content', 'interpretation', 'created_at')
        }),
        ("心理分析", {
            'fields': ('stress_index', 'emotion_score', 'anxiety', 'fear', 'surprise', 'hope', 'confusion')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_therapist', 'is_verified_therapist', 'current_title', 'current_badge_icon') # 添加 current_title 和 current_badge_icon 到列表顯示
    list_filter = ('is_therapist', 'is_verified_therapist')
    search_fields = ('user__username', 'current_title', 'bio') # 允許搜尋用戶名、稱號和個人簡介

    # 添加 fieldsets 來明確定義編輯頁面顯示的字段
    fieldsets = (
        (None, { # 基本信息
            'fields': ('user', 'is_therapist', 'is_verified_therapist')
        }),
        ("個人資料", { # 新增個人資料部分
            'fields': ('bio', 'avatar', 'current_title', 'current_badge_icon')
        }),
    )



@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'title', 'condition_key', 'condition_value')
    search_fields = ('name', 'category', 'condition_key')
    list_filter = ('category',)