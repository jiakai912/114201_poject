from django.contrib import admin
from .models import Dream

@admin.register(Dream)
class DreamAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('dream_content', 'interpretation')
    readonly_fields = ('created_at',)