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
    path('mental_health_dashboard/', views.mental_health_dashboard, name='mental_health_dashboard'),  # ✅ 修正
    path('api/mental-health-suggestions/<int:dream_id>/', views.get_mental_health_suggestions, name='mental_health_suggestions'),
    path('get_dream_detail/<int:dream_id>/', views.get_dream_detail, name='get_dream_detail'),
    path('logout_success/', views.logout_success, name='logout_success'), 
]


    
