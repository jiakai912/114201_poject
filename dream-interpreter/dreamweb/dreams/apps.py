from django.apps import AppConfig


class DreamsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dreams'
    def ready(self):
        import dreams.signals  # 🔁 確保引入 signals