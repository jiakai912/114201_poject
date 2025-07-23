import pymysql
pymysql.install_as_MySQLdb()
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-nki#eltx@^yo5b4woq3d=dg0n&yt3a=0(v=pjvw%6xzf6%6m6q'
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dreams',
    'django_crontab',  # 添加 crontab 支持
    'django.contrib.sites',  # 必要
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # Google 驗證
]

# google驗證
SITE_ID = 1
LOGIN_REDIRECT_URL = '/dream_form/'  # 成功登入後導向的頁面
LOGOUT_REDIRECT_URL = '/logout_success/'  # 登出後導向頁面

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #'allauth.account.auth_backends.AuthenticationBackend',
)



CRONJOBS = [
    ('0 0 * * *', 'dreams.cron.update_dream_trends'),  # 每天午夜執行趨勢更新
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'dreamweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Path to the templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dreamweb.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 使用 MySQL
        'NAME': 'DreamEcho',                    # 資料庫名稱
        'USER': 'root',                         # MySQL 帳號
        'PASSWORD': '123456',                   # MySQL 密碼
        'HOST': 'localhost',                    # 伺服器名稱
        'PORT': '3306',                         # MySQL Port
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# settings.py AI審核貼文
DANGEROUS_KEYWORDS = ['自殺', '殺人', '輕生', '毒品', '割腕','災難', '虐待', '性暴力', '性侵害', '性騷擾','末日','地震','海嘯']


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Taipei'



USE_I18N = True
USE_TZ = True

LOGIN_URL = '/login/'  # 登入頁面路徑
LOGIN_REDIRECT_URL = '/profile/'  # 登錄後的重定向頁面
LOGOUT_REDIRECT_URL = '/'  # 登出後的重定向頁面

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

