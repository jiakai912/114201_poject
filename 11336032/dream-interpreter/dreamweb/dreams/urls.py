from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # ✅ 管理員
    # 管理使用者
    path('admin_dashboard/users/', views.manage_users, name='manage_users'),
    path('admin_dashboard/users/block/<int:user_id>/', views.block_user, name='block_user'),
    path('admin_dashboard/users/unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('admin_dashboard/users/<int:user_id>/', views.view_user_detail, name='view_user_detail'),
    
    # 管理夢境
    path('admin_manage-dreams/', views.manage_dreams, name='manage_dreams'),
    path('admin_manage-dreams/<int:dream_id>/delete/', views.delete_dream, name='delete_dream'),
    path('admin_manage-dreams/<int:dream_id>/toggle-flag/', views.toggle_flag_dream, name='toggle_flag_dream'),
    path('admin_manage-dreams/<int:dream_id>/', views.dream_detail, name='dream_detail'),
    path('admin_dreams/<int:dream_id>/', views.dream_manage_detail, name='dream_manage_detail'),# 詳細夢境
    # 管理貼文
    path('admin_manage-posts/', views.manage_posts, name='manage_posts'),
    path('admin_manage-posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('admin_manage-posts/<int:post_id>/toggle-flag/', views.toggle_flag_post, name='toggle_flag_post'),
    path('admin_posts/<int:post_id>/toggle-flag/', views.toggle_flag_post, name='toggle_flag_post'),
    path('admin_posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
    # 管理評論
    path('admin_manage-comments/', views.manage_comments, name='manage_comments'),
    path('admin_manage-comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),



    # 管理夢境
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/therapists/', views.manage_therapists, name='manage_therapists'),
    path('admin_dashboard/chat_messages/', views.manage_chat_messages, name='manage_chat_messages'),
    path('admin_dashboard/points/', views.manage_points, name='manage_points'),

    # 核准/拒絕心理師申請
    path('manage/therapists/approve/<int:user_id>/', views.approve_therapist, name='approve_therapist'),
    path('manage/therapists/reject/<int:user_id>/', views.reject_therapist, name='reject_therapist'),
    # 預約管理
    path('admin_dashboard/appointments/', views.manage_appointments, name='manage_appointments'),



    # 通知系統
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/', views.notification_detail, name='notification_detail'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/send_broadcast/', views.send_broadcast, name='send_broadcast'),

    path('', views.welcome_page, name='welcome'),
    path('dream_form/', views.dream_form, name='dream_form'),  # ✅ 修正
    path('daily-task/claim/', views.claim_daily_task, name='claim_daily_task'),
    path('daily-task/check/', views.check_daily_task, name='check_daily_task'),# 每日任務
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/',  views.logout_view, name='logout'),  # ✅ 修正
    path('history/', views.dream_history, name='dream_history'),# 夢境歷史
    path('my-dreams/<int:dream_id>/delete/', views.user_delete_dream, name='user_delete_dream'), # 刪除夢境
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
    path('comment/<int:comment_id>/like_toggle/', views.toggle_comment_like, name='toggle_comment_like'), # 評論按讚
    path('post/<int:post_id>/like_toggle/', views.toggle_post_like, name='toggle_post_like'), # 貼文按讚
    path('profile/<int:user_id>/', views.profile_view_other, name='profile_view_other'),# 個人簡介浮窗
    # 我的個人貼文
    path('my_posts/', views.my_posts, name='my_posts'),
    path('post/<int:post_id>/edit/', views.edit_dream_post, name='edit_dream_post'),
    path('dream_post/<int:post_id>/delete/', views.delete_dream_post, name='delete_dream_post'),


    path('dream_news/', views.dream_news, name='dream_news'),
    path('dream/upload_audio/', views.upload_audio, name='upload_audio'),


    # 個人檔案
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('achievements/', views.user_achievements, name='achievements'),
    path('achievements/', views.user_achievements, name='user_achievements'),
    path('profile/', views.profile_view, name='profile'),
    

    # 使用者分享與取消分享夢境
    path('cancel_share/<int:therapist_id>/', views.cancel_share, name='cancel_share'),

    path('not_verified/', views.not_verified, name='not_verified'),
    path('shared_users/', views.shared_with_me, name='shared_with_me'),
    path('view_user_dreams/<int:user_id>/', views.view_user_dreams, name='view_user_dreams'),
    path('share_and_schedule/', views.share_and_schedule, name='share_and_schedule'),
    path('therapists/chat_list/', views.therapist_list_with_chat, name='therapist_list_with_chat'),
    path('chat/respond/<int:invitation_id>/', views.respond_invitation, name='respond_invitation'),


    #使用者看到的預約狀態及取消預約按鈕及已預約時段
    path('my_appointments/', views.user_appointments, name='user_appointments'),
    path('appointment/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('api/booked_slots/<int:therapist_id>/', views.get_therapist_booked_slots, name='get_booked_slots'),
    #使用者刪除已取消的預約
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),

    # 一鍵刪除已取消的預約
    path('delete_all_cancelled/', views.delete_all_cancelled_appointments, name='delete_all_cancelled'),

    #心理師看到的預約及確認按鈕
    path('consultation/schedule/<int:user_id>/', views.consultation_schedule, name='consultation_schedule'),
    path('appointment/confirm/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('all_users_appointments/', views.all_users_appointments, name='all_users_appointments'),

    #心理師的刪除預約按鈕
    path('therapist/consultation/<int:user_id>/', views.consultation_schedule, name='therapist_view_client_appointments'),
    path('appointments/<int:appointment_id>/delete/', views.therapist_delete_appointment, name='therapist_delete_appointment'),

    # 心理師邀請聊天功能
    path('invitation/respond/<int:invitation_id>/', views.respond_invitation, name='respond_invitation'),
    # 使用者能夠看到的通知訊息
    path('send_chat_invitation/', views.send_chat_invitation, name='send_chat_invitation'),
    # 刪除邀請記錄
    path('invitation/delete/<int:invitation_id>/', views.delete_invitation, name='delete_invitation'),
    # 刪除邀請記錄
    path('chat/invitation/delete/<int:user_id>/', views.delete_chat_invitation, name='delete_chat_invitation'),


    # 使用者看到的聊天對象列表
    path('my_therapists/', views.therapist_list_with_chat, name='my_therapists'),
    #聊天室
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

    
    path('weather/forecast/', views.weather_forecast, name='weather_forecast'),     # ✅ 新增：天氣預報頁面
    path('watchlist/', views.manage_watchlist, name='manage_watchlist'),    # ✅ 新增：關注清單管理
    path('api/watchlist-data/', views.get_watchlist_data, name='get_watchlist_data'),# ✅ 新增：API 接口，供前端獲取關注清單的即時數據
    path('api/save_notes/', views.save_private_notes, name='save_private_notes'),



]
    
