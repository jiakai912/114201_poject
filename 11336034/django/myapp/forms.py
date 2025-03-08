from django import forms
from .models import Dashboard

class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = [
            'kpi_name', 'value', 'date'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'value': forms.NumberInput(attrs={'step': 'any'}),
        }
