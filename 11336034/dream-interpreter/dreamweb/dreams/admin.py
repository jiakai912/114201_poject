from django.contrib import admin
from .models import Dream
from .models import UserProfile

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
    list_display = ('user', 'is_therapist', 'is_verified_therapist')
    list_filter = ('is_therapist', 'is_verified_therapist')
