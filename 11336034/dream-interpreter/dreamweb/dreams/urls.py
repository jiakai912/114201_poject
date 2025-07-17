from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('dream_form/', views.dream_form, name='dream_form'),  # ✅ 修正
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/',  views.logout_view, name='logout'),  # ✅ 修正
    path('history/', views.dream_history, name='dream_history'),
    path('api/emotion-data/', views.get_emotion_data, name='emotion_data'),
    path('dream/<int:dream_id>/', views.dream_detail, name='dream_detail'),
    path('dashboard/', views.dream_dashboard, name='dream_dashboard'),
    path('api/global-trends/', views.get_global_trends_data, name='global-trends'), # ✅ 熱門夢境
    path('api/user-keywords/', views.get_user_keywords, name='get_user_keywords'),# ✅ 個人關鍵字
    path('mental_health_dashboard/', views.mental_health_dashboard, name='mental_health_dashboard'),  # ✅ 修正
    path('api/mental-health-suggestions/<int:dream_id>/', views.get_mental_health_suggestions, name='mental_health_suggestions'),
    path('get_dream_detail/<int:dream_id>/', views.get_dream_detail, name='get_dream_detail'),
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

    # 個人檔案
    path('profile/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('achievements/', views.user_achievements, name='achievements'),
    path('achievements/', views.user_achievements, name='user_achievements'),
    path('profile/', views.profile_view, name='profile'),
    

    # 使用者分享與取消分享夢境
    path('share_dreams/', views.share_dreams, name='share_dreams'),
    path('cancel_share/<int:therapist_id>/', views.cancel_share, name='cancel_share'),

    path('not_verified/', views.not_verified, name='not_verified'),
    path('shared_users/', views.shared_with_me, name='shared_with_me'),
    path('view_user_dreams/<int:user_id>/', views.view_user_dreams, name='view_user_dreams'),
    path('share_and_schedule/', views.share_and_schedule, name='share_and_schedule'),
    path('therapists/chat_list/', views.therapist_list_with_chat, name='therapist_list_with_chat'),

    #使用者看到的預約狀態及取消預約按鈕
    path('my_appointments/', views.user_appointments, name='user_appointments'),
    path('appointment/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),

    #心理師看到的預約及確認按鈕
    path('consultation/schedule/<int:user_id>/', views.consultation_schedule, name='consultation_schedule'),
    path('appointment/confirm/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('all_users_appointments/', views.all_users_appointments, name='all_users_appointments'),
    

    #心理師的刪除預約按鈕
    path('therapist/consultation/<int:user_id>/', views.consultation_schedule, name='therapist_view_client_appointments'),
    path('appointments/<int:appointment_id>/delete/', views.therapist_delete_appointment, name='therapist_delete_appointment'),

    #聊天室
    path('my_therapists/', views.therapist_list_with_chat, name='my_therapists'),
    path('chat/<int:therapist_id>/', views.chat_with_therapist, name='chat_with_therapist'),
    #聊天室
    path('my_clients/', views.my_clients, name='my_clients'),
    path('chat/client/<int:user_id>/', views.chat_with_client, name='chat_with_client'),
    path('chat/<int:chat_user_id>/', views.chat_room, name='chat_room'),
    path('chat/user/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    #綠界第三方支付
    path('ecpay/checkout/', views.ecpay_checkout, name='ecpay_checkout'),
    path('ecpay/return/', views.ecpay_return, name='ecpay_return'),
    path('result/', views.ecpay_result, name='ecpay_result'),
    #點券包
    path('pointshop/', views.pointshop, name='pointshop'),
    path('pointshop/buy/<int:pkg_id>/', views.pointshop_buy, name='pointshop_buy'),
    path('points/history/', views.point_history, name='point_history'),#點券使用記錄

]


    
