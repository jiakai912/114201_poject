from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # 首頁與帳號相關
    path('', views.welcome_page, name='welcome'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout_success/', views.logout_success, name='logout_success'),
    path('not_verified/', views.not_verified, name='not_verified'),
    
    
    # 夢境解析與歷史
    path('dream_form/', views.dream_form, name='dream_form'),
    path('history/', views.dream_history, name='dream_history'),
    path('dream/<int:dream_id>/', views.dream_detail, name='dream_detail'),
    path('dream/upload_audio/', views.upload_audio, name='upload_audio'),
    path('get_dream_detail/<int:dream_id>/', views.get_dream_detail, name='get_dream_detail'),
    path('dashboard/', views.dream_dashboard, name='dream_dashboard'),

    # 社群功能
    path('community/', views.community, name='dream_community'),
    path('share/', views.share_dream, name='share_dream'),
    path('search/', views.search_dreams, name='search_dreams'),
    path('post/<int:post_id>/', views.dream_post_detail, name='dream_post_detail'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('post/<int:post_id>/edit/', views.edit_dream_post, name='edit_dream_post'),
    path('dream_post/<int:post_id>/delete/', views.delete_dream_post, name='delete_dream_post'),
    path('dream_news/', views.dream_news, name='dream_news'),
    path('comment/<int:comment_id>/like_toggle/', views.toggle_comment_like, name='toggle_comment_like'),
    path('post/<int:post_id>/like_toggle/', views.toggle_post_like, name='toggle_post_like'),

    # 個人檔案與成就
    path('profile/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('achievements/', views.user_achievements, name='achievements'),
    path('profile/<int:user_id>/', views.profile_view_other, name='profile_view_other'),
    path('profile/', views.profile_view, name='profile'),

    # 心理健康與預約
    path('mental_health_dashboard/', views.mental_health_dashboard, name='mental_health_dashboard'),
    path('share_dreams/', views.share_dreams, name='share_dreams'),
    path('cancel_share/<int:therapist_id>/', views.cancel_share, name='cancel_share'),
    path('shared_users/', views.shared_with_me, name='shared_with_me'),
    path('view_user_dreams/<int:user_id>/', views.view_user_dreams, name='view_user_dreams'),
    path('share_and_schedule/', views.share_and_schedule, name='share_and_schedule'),
    path('my_therapists/', views.therapist_list_with_chat, name='therapist_list_with_chat'),
    path('my_clients/', views.my_clients, name='my_clients'),
    path('my_appointments/', views.user_appointments, name='user_appointments'),
    path('appointment/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('api/booked_slots/<int:therapist_id>/', views.get_therapist_booked_slots, name='get_booked_slots'),
    path('all_users_appointments/', views.all_users_appointments, name='all_users_appointments'),
    path('therapist/consultation/<int:user_id>/', views.consultation_schedule, name='consultation_schedule'),
    path('appointment/confirm/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('appointments/<int:appointment_id>/delete/', views.therapist_delete_appointment, name='therapist_delete_appointment'),
    
    # 聊天室
    path('chat/user/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    path('send_chat_invitation/', views.send_chat_invitation, name='send_chat_invitation'),
    path('invitation/respond/<int:invitation_id>/', views.respond_invitation, name='respond_invitation'),
    path('invitation/delete/<int:invitation_id>/', views.delete_invitation, name='delete_invitation'),
    path('chat/invitation/delete/<int:user_id>/', views.delete_chat_invitation, name='delete_chat_invitation'),

    
    path('my_therapists/', views.therapist_list_with_chat, name='my_therapists'),
    path('chat/<int:therapist_id>/', views.chat_with_therapist, name='chat_with_therapist'),
    path('my_clients/', views.my_clients, name='my_clients'),
    path('chat/client/<int:user_id>/', views.chat_with_client, name='chat_with_client'),
    path('chat/<int:chat_user_id>/', views.chat_room, name='chat_room'),
    path('chat/user/<int:user_id>/', views.chat_with_user, name='chat_with_user'),


    path('invitation/respond/<int:invitation_id>/', views.respond_invitation, name='respond_invitation'),
    path('send_chat_invitation/', views.send_chat_invitation, name='send_chat_invitation'),
    path('invitation/delete/<int:invitation_id>/', views.delete_invitation, name='delete_invitation'),
    path('chat/invitation/delete/<int:user_id>/', views.delete_chat_invitation, name='delete_chat_invitation'),

    # 綠界支付與點券
    path('ecpay/checkout/', views.ecpay_checkout, name='ecpay_checkout'),
    path('ecpay/return/', views.ecpay_return, name='ecpay_return'),
    path('result/', views.ecpay_result, name='ecpay_result'),
    path('pointshop/', views.pointshop, name='pointshop'),
    path('pointshop/buy/<int:pkg_id>/', views.pointshop_buy, name='pointshop_buy'),
    path('points/history/', views.point_history, name='point_history'),

    # API
    path('api/emotion-data/', views.get_emotion_data, name='emotion_data'),
    path('api/global-trends/', views.get_global_trends_data, name='global-trends'),
    path('api/user-keywords/', views.get_user_keywords, name='get_user_keywords'),
    path('api/mental-health-suggestions/<int:dream_id>/', views.get_mental_health_suggestions, name='mental_health_suggestions'),
]

# 確保在開發模式下能夠存取媒體檔案
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


