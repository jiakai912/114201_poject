from django.urls import path
from . import views

urlpatterns = [
    path('result/<int:message_id>/', views.result_view, name='result'),  # Include message_id here
    path('detect_scam/', views.detect_scam, name='detect_scam'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
