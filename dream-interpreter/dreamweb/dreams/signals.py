from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # 改用 get_or_create 避免重複 key 錯誤
        UserProfile.objects.get_or_create(user=instance)
