# dreams/achievement_helper.py
from django.contrib import messages
from django.utils import timezone
from .models import Dream, DreamPost, DreamComment, UserAchievement, Achievement, PostLike, CommentLike, UserProfile

def check_and_unlock_achievements(user):
    """
    檢查用戶是否達到任何成就的條件，如果達到則解鎖，
    並自動更新用戶的稱號和徽章（如果設定為自動賦予模式）。
    此處的邏輯是根據用戶已解鎖的成就，將最新的帶稱號/徽章的成就賦予給用戶。
    """
    user_data = {
        'parse_count': Dream.objects.filter(user=user).count(),
        'post_count': DreamPost.objects.filter(user=user).count(),
        'comment_count': DreamComment.objects.filter(user=user).count(),
        'total_post_likes': PostLike.objects.filter(post__user=user).count(),
        'total_comment_likes': CommentLike.objects.filter(comment__user=user).count(),
    }

    all_achievements = Achievement.objects.all()
    user_profile = user.userprofile

    for achievement in all_achievements:
        current_progress = user_data.get(achievement.condition_key, 0)

        if current_progress >= achievement.condition_value:
            already_unlocked = UserAchievement.objects.filter(user=user, achievement=achievement).exists()
            if not already_unlocked:
                UserAchievement.objects.create(
                    user=user,
                    achievement=achievement,
                    unlocked_at=timezone.now()
                )
                messages.info(user, f"恭喜！您解鎖了成就：『{achievement.name}』！")

    # 在所有成就檢查完畢後，根據最新的解鎖狀態來設定當前稱號和徽章
    # 這裡的邏輯是選擇已解鎖成就中，condition_value 最高的稱號和徽章
    # 如果 condition_value 相同，則選擇最近解鎖的
    
    # 選擇最高級的稱號
    best_title_achievement = UserAchievement.objects.filter(user=user, achievement__title__isnull=False) \
                                                    .order_by('-achievement__condition_value', '-unlocked_at') \
                                                    .first()
    if best_title_achievement and user_profile.current_title != best_title_achievement.achievement.title:
        user_profile.current_title = best_title_achievement.achievement.title
        messages.info(user, f"您的稱號已自動更新為：『{user_profile.current_title}』")
    
    # 選擇最高級的徽章
    best_badge_achievement = UserAchievement.objects.filter(user=user, achievement__badge_icon__isnull=False) \
                                                    .order_by('-achievement__condition_value', '-unlocked_at') \
                                                    .first()
    if best_badge_achievement and user_profile.current_badge_icon != best_badge_achievement.achievement.badge_icon:
        user_profile.current_badge_icon = best_badge_achievement.achievement.badge_icon
        messages.info(user, f"您的徽章已自動更新為：『{best_badge_achievement.achievement.name}』的徽章")
    
    # 只有當稱號或徽章有變化時才保存 UserProfile
    if user_profile.current_title != user_profile.userprofile_original_title or \
       user_profile.current_badge_icon != user_profile.userprofile_original_badge_icon:
        user_profile.save()
