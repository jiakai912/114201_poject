from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('dream_form/', views.dream_form, name='dream_form'),  # ✅ 修正
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/',  views.logout_view, name='logout'),  # ✅ 修正
    path('history/', views.dream_history, name='dream_history'),
    path('api/emotion-data/', views.get_emotion_data, name='emotion_data'),
    path('dream/<int:dream_id>/', views.dream_detail, name='dream_detail'),
    path('dashboard/', views.dream_dashboard, name='dream_dashboard'),
    path('api/global-trends/', views.get_global_trends_data, name='global-trends'), # ✅ 熱門夢境
    path('api/user-keywords/', views.get_user_keywords, name='get_user_keywords'),# ✅ 個人關鍵字
    path('mental_health_dashboard/', views.mental_health_dashboard, name='mental_health_dashboard'),  # ✅ 修正
    #path('api/mental-health-suggestions/<int:dream_id>/', views.get_mental_health_suggestions, name='mental_health_suggestions'),
    path('get_dream_detail/<int:dream_id>/', views.get_dream_detail_ajax, name='get_dream_detail_ajax'),
    path('logout_success/', views.logout_success, name='logout_success'), 
    path('community/', views.community, name='dream_community'),
    path('share/', views.share_dream, name='share_dream'),
    path('search/', views.search_dreams, name='search_dreams'),
    path('post/<int:post_id>/', views.dream_post_detail, name='dream_post_detail'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('post/<int:post_id>/edit/', views.edit_dream_post, name='edit_dream_post'),
    path('dream_post/<int:post_id>/delete/', views.delete_dream_post, name='delete_dream_post'),
    path('dream_news/', views.dream_news, name='dream_news'),
    path('dream/upload_audio/', views.upload_audio, name='upload_audio'),
    #path('polls/', views.polls, name='polls'),
    path('consultation/', views.consultation_chat, name='consultation_chat'),
    path('consultation/chat/<int:counselor_id>/', views.chat_with_counselor_view, name='consultation_chat_with_counselor'),
    path('counselors/', views.counselor_list_view, name='counselor_list'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('achievements/', views.user_achievements, name='achievements'),
    path('achievements/', views.user_achievements, name='user_achievements'),
]

    
