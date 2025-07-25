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
        ("心理分析", {
            'fields': ('stress_index', 'emotion_score', 'anxiety', 'fear', 'surprise', 'hope', 'confusion')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'points', 'is_therapist', 'is_verified_therapist',
        'current_title', 'current_badge_icon', 'coin_price'  # ✅ 加入這行
    )
    list_filter = ('is_therapist', 'is_verified_therapist')
    search_fields = ('user__username', 'current_title', 'bio')

    fieldsets = (
        (None, {
            'fields': ('user', 'points', 'is_therapist', 'is_verified_therapist', 'coin_price')  # ✅ 加入這行
        }),
        ("個人資料", {
            'fields': ('bio', 'avatar', 'current_title', 'current_badge_icon')
        }),
    )


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'title', 'condition_key', 'condition_value')
    search_fields = ('name', 'category', 'condition_key')
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
