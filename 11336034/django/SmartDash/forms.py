# forms.py
from django import forms
from .models import ScamMessage

class ScamMessageForm(forms.ModelForm):
    class Meta:
        model = ScamMessage
        fields = ['text']  # 您的表單應該只包含 "text" 欄位
    
