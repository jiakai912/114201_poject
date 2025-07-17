# 夢境解析觸發成就dreams/utils/achievement_helper.py
from dreams.models import Dream, Achievement, UserAchievement
from django.utils import timezone

def check_and_unlock_achievements(user):
    """
    檢查並解鎖符合條件的成就（目前支援解析夢境數量條件）。
    """
    dream_count = Dream.objects.filter(user=user).count()
    achievements = Achievement.objects.filter(condition_key='parse_count')

    for achievement in achievements:
        if dream_count >= achievement.condition_value:
            already_unlocked = UserAchievement.objects.filter(user=user, achievement=achievement).exists()
            if not already_unlocked:
                UserAchievement.objects.create(
                    user=user,
                    achievement=achievement,
                    unlocked_at=timezone.now()
                )
