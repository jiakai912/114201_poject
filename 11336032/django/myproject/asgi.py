"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os  # 匯入 os 模組，用於操作環境變數

from django.core.asgi import get_asgi_application  # 匯入 Django 的 ASGI 應用程式獲取函式

# 設定 Django 專案的設定模組環境變數，這裡指定為 'myproject.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# 獲取 ASGI 應用程式實例，讓 ASGI 伺服器（如 Daphne、Uvicorn）使用
application = get_asgi_application()
