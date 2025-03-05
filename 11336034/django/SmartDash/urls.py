from django.urls import path
from .views import add_kpi, dashboard, get_kpi_data  # 確保導入所需的視圖函數

urlpatterns = [
    path('add_kpi/', add_kpi, name='add_kpi'),  # 新增 KPI 的路由
    path('dashboard/', dashboard, name='dashboard'),  # 儀表板的路由
    path('get_kpi_data/', get_kpi_data, name='get_kpi_data'),  # 處理 KPI 數據的請求
]
