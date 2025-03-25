from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Dream

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DreamForm(forms.ModelForm):
    class Meta:
        model = Dream
        fields = ['dream_content']
        widgets = {
            'dream_content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '請詳細描述您的夢境...',
                'rows': 8
            })
        }

