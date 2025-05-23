"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os  # 匯入 os 模組，用於與作業系統互動

from django.core.wsgi import get_wsgi_application  # 匯入 Django 的 WSGI 應用函式

# 設定 Django 專案的環境變數，指定 settings 檔案的位置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# 建立 WSGI 應用程式，讓伺服器能夠與 Django 專案溝通
application = get_wsgi_application()

