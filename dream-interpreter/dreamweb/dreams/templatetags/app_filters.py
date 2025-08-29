import json
from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

register = template.Library()

@register.filter(name='safe_json')
def safe_json(value):
    """
    Safely converts a Python object to a JSON string for use in HTML attributes.
    Handles QuerySets of model instances by converting them to dicts first.
    """
    if isinstance(value, (models.QuerySet, list)):
        processed_value = []
        for item in value:
            if hasattr(item, 'achievement'): # Assuming UserAchievement instance
                processed_value.append({
                    'name': item.achievement.name,
                    'badge_icon': item.achievement.badge_icon
                })
            elif hasattr(item, 'name') and hasattr(item, 'badge_icon'): # Assuming Achievement instance
                 processed_value.append({
                    'name': item.name,
                    'badge_icon': item.badge_icon
                })
            else: # Fallback for other types of objects
                processed_value.append(item)
        value_to_encode = processed_value
    else:
        value_to_encode = value

    return json.dumps(value_to_encode, cls=DjangoJSONEncoder).replace("'", "&#39;")