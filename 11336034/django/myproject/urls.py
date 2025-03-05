# myproject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 這是將前端頁面的路由指向 myapp
    path('', include('myapp.urls')),  # 前端頁面配置
    path('SmartDash/', include('SmartDash.urls')),  # 後台學生頁面配置
]
