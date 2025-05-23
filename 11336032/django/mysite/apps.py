from django.apps import AppConfig # 匯入 AppConfig 類別


class MysiteConfig(AppConfig): # 定義 MysiteConfig 類別
    default_auto_field = 'django.db.models.BigAutoField' # 設定主鍵類型
    name = 'mysite' # 指定應用程式名稱
