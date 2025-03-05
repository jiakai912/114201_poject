from django import forms
from .models import Dashboard  # ← 這裡改成 DashboardData

class DashboardForm(forms.ModelForm):  # ← 這裡改成 DashboardForm
    class Meta:
        model = Dashboard  # ← 這裡改成 DashboardData
        fields = ['kpi_name', 'value']
