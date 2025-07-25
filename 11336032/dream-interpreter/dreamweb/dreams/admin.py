from django.contrib import admin
from .models import (
    Dream, UserProfile, Achievement, UserAchievement,
    DreamPost, DreamComment, DreamTag, DreamTrend,
    DreamRecommendation, TherapyAppointment, TherapyMessage,
    ChatMessage, PointTransaction, CommentLike, PostLike,
    DreamShareAuthorization
)

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
        # ✅ FIX: 修正 fieldsets 中的情緒字段名稱以匹配 models.py
        ("心理分析", {
            'fields': ('stress_index', 'emotion_score', 'Happiness', 'Anxiety', 'Fear', 'Excitement', 'Sadness', 'advice')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # ✅ FIX: 更新 list_display 顯示新的 display_title 和 display_badge
    list_display = (
        'user', 'points', 'is_therapist', 'is_verified_therapist', 'get_display_title_name', 'get_display_badge_name'
    )
    list_filter = ('is_therapist', 'is_verified_therapist')
    search_fields = ('user__username', 'bio') # ✅ FIX: 移除不存在的 current_title
    
    # ✅ FIX: 更新 fieldsets 顯示新的 display_title 和 display_badge
    fieldsets = (
        (None, {
            'fields': ('user', 'points', 'is_therapist', 'is_verified_therapist')
        }),
        ("個人資料", {
            'fields': ('bio', 'avatar', 'display_title', 'display_badge') # ✅ FIX: 使用新的字段
        }),
    )

    # ✅ ADD: 定義方法來顯示 ForeignKey 關聯的名稱，因為 list_display 無法直接顯示外鍵的屬性
    def get_display_title_name(self, obj):
        return obj.display_title.name if obj.display_title else '-'
    get_display_title_name.short_description = '社群展示稱號' # 定義欄位標題

    def get_display_badge_name(self, obj):
        return obj.display_badge.name if obj.display_badge else '-'
    get_display_badge_name.short_description = '社群展示徽章' # 定義欄位標題


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'title', 'badge_icon', 'condition_key', 'condition_value') # ✅ FIX: 增加 badge_icon 顯示
    search_fields = ('name', 'category', 'condition_key', 'title') # ✅ FIX: 增加 title 到搜尋
    list_filter = ('category',)


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'unlocked_at')
    search_fields = ('user__username', 'achievement__name')
    list_filter = ('unlocked_at',)


@admin.register(DreamPost)
class DreamPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_anonymous', 'view_count', 'created_at', 'is_flagged')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('is_anonymous', 'is_flagged', 'created_at')


@admin.register(DreamComment)
class DreamCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'dream_post', 'content', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at',)


@admin.register(DreamTag)
class DreamTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(DreamTrend)
class DreamTrendAdmin(admin.ModelAdmin):
    list_display = ('date',)
    search_fields = ('date',)


@admin.register(DreamRecommendation)
class DreamRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)


@admin.register(TherapyAppointment)
class TherapyAppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'therapist', 'scheduled_time', 'is_confirmed', 'is_cancelled', 'point_change')
    list_filter = ('is_confirmed', 'is_cancelled', 'scheduled_time')
    search_fields = ('user__username', 'therapist__username')


@admin.register(TherapyMessage)
class TherapyMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'message')


@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'description', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('user__username', 'description')


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'liked_at')
    search_fields = ('user__username', 'comment__content')


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'liked_at')
    search_fields = ('user__username', 'post__title')


@admin.register(DreamShareAuthorization)
class DreamShareAuthorizationAdmin(admin.ModelAdmin):
    list_display = ('user', 'therapist', 'shared_at', 'expires_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'therapist__username')