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
    data = Dashboard.objects.filter(kpi_name="產量達成率").order_by('date')
    dates = [entry.date.strftime('%Y-%m-%d') for entry in data]  # 格式化日期
    values = [entry.value for entry in data]

    # 傳遞資料給模板
    return render(request, "dashboard.html", {
        'dates': dates,
        'values': values
    })

# 定義 dashboard 視圖
def dashboard(request):
    kpis = Dashboard.objects.all()
    return render(request, 'SmartDash/dashboard.html', {'kpis': kpis})
