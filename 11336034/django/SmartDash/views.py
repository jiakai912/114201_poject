from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Dashboard
from datetime import datetime

# 定義新增 KPI 的視圖
def add_kpi(request):
    if request.method == "POST":
        kpi_name = request.POST.get('kpi_name')
        value = request.POST.get('value')
        if kpi_name and value:
            # 創建一條新的 KPI 數據並保存
            Dashboard.objects.create(kpi_name=kpi_name, value=float(value))
            return HttpResponse("KPI 添加成功")
    return render(request, 'add_kpi.html')

# 這個視圖會返回給定 KPI 名稱的所有數據
def get_kpi_data(request):
    kpi_name = request.GET.get('kpi_name')
    kpi_data = Dashboard.objects.filter(kpi_name=kpi_name).order_by('date')  # 根據日期排序
    labels = [data.date.strftime('%Y-%m-%d') for data in kpi_data]  # 日期作為 x 軸
    values = [data.value for data in kpi_data]  # KPI 數值作為 y 軸
    return JsonResponse({'labels': labels, 'values': values})

# 定義 dashboard 視圖
def dashboard(request):
    kpis = Dashboard.objects.all()
    return render(request, 'SmartDash/dashboard.html', {'kpis': kpis})
