from django import forms  # 匯入 Django 的 forms 模組，用來建立表單
from .models import Dashboard  # 匯入 Dashboard 模型，這是表單所關聯的模型

# 定義 DashboardForm，繼承自 ModelForm，表示這是一個基於模型的表單
class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard  # 指定表單對應的模型為 Dashboard
        fields = [  # 定義表單中要包含的欄位
            'kpi_name',  # KPI 指標名稱
            'value',  # KPI 的數值
            'date'  # KPI 的日期
        ]
        widgets = {  # 自訂表單欄位的 HTML 控件
            'date': forms.DateInput(attrs={'type': 'date'}),  # 將 date 欄位的輸入框設定為 HTML5 日期選擇器
            'value': forms.NumberInput(attrs={'step': 'any'}),  # 設定 value 欄位的輸入框可輸入任何數字（允許小數）
        }
