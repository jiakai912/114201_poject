import json
from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet # 引入 QuerySet

register = template.Library()

@register.filter
def safe_json_dumps(value):
    """
    安全地將 Python 對象轉化為 JSON 字串，
    並將 UserAchievement 對象的相關屬性序列化。
    此過濾器用於將複雜的 Django 模型對象轉換為 JSON，以便在 HTML 的 data- 屬性中使用。
    """
    if not value:
        return "[]"
    
    # 確保 value 是一個列表或 QuerySet，以便進行迭代
    if isinstance(value, QuerySet):
        value = list(value)
    elif not isinstance(value, (list, tuple)):
        # 如果不是列表或 QuerySet，嘗試將其轉換為列表
        try:
            value = list(value)
        except TypeError:
            # 如果無法轉換，則返回空列表的 JSON
            return "[]" 

    # 自定義 JSON 編碼器來處理 UserAchievement 實例
    class CustomEncoder(DjangoJSONEncoder):
        def default(self, obj):
            if isinstance(obj, QuerySet): # 處理 QuerySet (雖然上面已經轉為 list，但以防萬一)
                return list(obj)
            elif hasattr(obj, 'achievement') and hasattr(obj.achievement, 'name'): # 處理 UserAchievement 物件
                # 確保 achievement 物件存在且有這些屬性
                achievement = obj.achievement
                return {
                    'name': achievement.name,
                    'description': achievement.description,
                    'title': achievement.title, # 成就的稱號文本
                    'badge_icon': achievement.badge_icon, # 成就的徽章圖標類名
                    'unlocked_at': obj.unlocked_at.isoformat() if obj.unlocked_at else None # 將日期時間轉換為 ISO 格式
                }
            # 其他類型交給父類處理
            return super().default(obj) 
    
    # ensure_ascii=False 確保中文正常顯示，indent=2 增加可讀性 (可選)
    return json.dumps(value, cls=CustomEncoder, ensure_ascii=False)



from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''