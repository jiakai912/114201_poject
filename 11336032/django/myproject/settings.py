"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path  # 匯入 Path 來處理檔案與目錄的路徑

# 設定專案的基礎目錄路徑（專案根目錄）
# __file__ 代表當前檔案的路徑，resolve() 取得絕對路徑，parent.parent 取得專案根目錄
BASE_DIR = Path(__file__).resolve().parent.parent

# ======== 快速啟動開發設定（不適用於正式環境）========

# 【安全性警告】正式環境中應該將 SECRET_KEY 設為環境變數，避免暴露
SECRET_KEY = 'django-insecure-^i=8_x$vqp60+@k_27pbz&r#d80j1beoro3xbm38vyy*1z%jap'

# 【安全性警告】正式環境中請關閉 DEBUG，以避免洩漏敏感資訊
DEBUG = True  # 設為 False 以提升安全性（正式環境應該關閉）

# 允許存取此 Django 專案的主機名稱或 IP 地址
# '*' 代表允許所有來源，適合開發階段，但正式環境應該設定為特定的主機名稱
ALLOWED_HOSTS = ['*']



# Application definition

# 已安裝並啟用的 Django 應用程式
INSTALLED_APPS = [
    # Django 內建應用程式：
    'django.contrib.admin',        # Django 管理後台
    'django.contrib.auth',         # 驗證與授權系統（用戶管理）
    'django.contrib.contenttypes', # 內容類型框架，處理模型的多型關聯
    'django.contrib.sessions',     # 會話管理（存儲用戶狀態）
    'django.contrib.messages',     # 訊息框架（用於顯示通知訊息）
    'django.contrib.staticfiles',  # 靜態檔案管理（CSS、JS、圖片等）

    # 自訂應用程式：
    'mysite',  # 這是專案內自訂的應用程式，應該對應 `mysite` 資料夾
]


# 中介軟體 (Middleware) 設定 - 這些函式會在請求與回應處理過程中運行
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  
    # 提供額外的安全性功能，如 HTTPS 重定向、HSTS（HTTP 严格传输安全）

    'django.contrib.sessions.middleware.SessionMiddleware',  
    # 啟用會話功能（用於存儲用戶登入狀態）

    'django.middleware.common.CommonMiddleware',  
    # 處理通用請求，包括 URL 正規化、GZip 壓縮等

    'django.middleware.csrf.CsrfViewMiddleware',  
    # 防禦 CSRF（跨站請求偽造）攻擊

    'django.contrib.auth.middleware.AuthenticationMiddleware',  
    # 啟用用戶驗證與登入狀態管理

    'django.contrib.messages.middleware.MessageMiddleware',  
    # 處理 Django 訊息框架（用於顯示通知）

    'django.middleware.clickjacking.XFrameOptionsMiddleware',  
    # 防禦 Clickjacking（點擊劫持）攻擊，預防網站被嵌入 iframe
]


# 設定 Django 專案的 URL 配置檔案
# 這裡指定 `myproject.urls`，表示 Django 會從 `myproject/urls.py` 加載 URL 路由
ROOT_URLCONF = 'myproject.urls'

# ==================== Django 模板設定 ====================
TEMPLATES = [
    {
        # 指定模板引擎，Django 預設使用 DjangoTemplates
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # 指定 Django 會在哪些資料夾尋找模板
        'DIRS': [BASE_DIR / "templates"],  # 預設會尋找專案內的 `templates/` 資料夾

        # 設定為 `True`，Django 會自動在每個應用程式內的 `templates/` 資料夾尋找模板
        'APP_DIRS': True,

        # 模板的額外選項
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # 附加 debug 相關資訊到模板
                'django.template.context_processors.request',  # 讓 request 變數可在模板中使用
                'django.contrib.auth.context_processors.auth',  # 提供 user 變數，用於驗證狀態
                'django.contrib.messages.context_processors.messages',  # 讓 Django 訊息框架可用於模板
            ],
        },
    },
]

# WSGI 應用程式的入口點
# Django 會使用 `myproject.wsgi.application` 來啟動 WSGI 伺服器（如 Gunicorn、uWSGI）
WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # ✅ 指定 Django 使用 MySQL 資料庫
        'NAME': 'NiceAdmin',                  # ✅ 你的 MySQL 資料庫名稱
        'USER': 'root',                        # ✅ 你的 MySQL 帳號
        'PASSWORD': 'ch0912979127',            # ⚠️ 你的 MySQL 密碼（勿公開）
        'HOST': 'localhost',                   # ✅ 伺服器位址，若 MySQL 與 Django 在同一台機器上，使用 'localhost'
        'PORT': '3306',                        # ✅ MySQL 預設連接埠號 (3306)
        'OPTIONS': {
            'charset': 'utf8mb4',              # ✅ 設定 MySQL 的字元編碼為 `utf8mb4`（支援 Emoji）
        },
    }
}


\



# 密碼驗證器設定 - 用於強化密碼安全性
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        # 防止使用者設置與個人資訊（如姓名、用戶名、Email）相似的密碼
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # 強制密碼達到最小長度（預設為 8 個字元）
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # 禁止使用常見的弱密碼（如 "password123", "12345678"）
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # 防止使用純數字密碼（如 "12345678"）
    },
]




# 設定 Django 專案的語言（使用繁體中文）
LANGUAGE_CODE = 'zh-hant'  # 'zh-hant' 表示繁體中文（台灣）

# 設定時區為台北（UTC+8）
TIME_ZONE = 'Asia/Taipei'  # 確保 Django 使用台灣當地時間

# 啟用 Django 的國際化（i18n）功能
USE_I18N = True  # 設為 True 允許 Django 根據不同語言進行翻譯（例如 admin 介面）

# 啟用時區支援
USE_TZ = True  # 設為 True 時，Django 會將時間存儲為 UTC，並根據 TIME_ZONE 轉換顯示


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

import os

# 設置靜態文件的 URL
STATIC_URL = '/static/'

# 在開發模式下，Django 會從這些目錄載入靜態文件
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # 確保有這個目錄
]

# collectstatic 指令會把所有靜態文件收集到這個目錄（僅用於正式環境）
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  




# 設定 Django 在創建 Model 時，預設使用 BigAutoField 作為主鍵類型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

