from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import mental_health_dashboard

urlpatterns = [
    path('', views.dream_form, name='dream_form'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='dreams/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='dreams/logout.html'), name='logout'),
    path('history/', views.dream_history, name='dream_history'),
    path('dream/<int:dream_id>/', views.dream_detail, name='dream_detail'),
    path('dashboard/', views.dream_dashboard, name='dream_dashboard'),
    path('mental_health_dashboard/', views.mental_health_dashboard, name='mental_health_dashboard'),
    path("mental_health_dashboard/", mental_health_dashboard, name="mental_health_dashboard"),
    path('api/mental-health-suggestions/<int:dream_id>/', views.get_mental_health_suggestions, name='mental_health_suggestions'),
    path('get_dream_detail/<int:dream_id>/', views.get_dream_detail, name='get_dream_detail'),
]
