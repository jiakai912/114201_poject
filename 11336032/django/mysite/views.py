from django.shortcuts import render
from django.http import JsonResponse
from .models import Dashboard
from django.shortcuts import redirect
from .forms import DashboardForm

def home(request):
    # 取得所有 KPI 資料，並按日期排序
    data = Dashboard.objects.all().order_by('date').values('kpi_name', 'date', 'value')

    kpi_data = {
        "產量達成率": {"dates": [], "values": []},
        "工時效率": {"dates": [], "values": []},
        "生產成本偏差率": {"dates": [], "values": []},
        "銷售退貨率": {"dates": [], "values": []},
        "進貨單價": {"dates": [], "values": []},
        "委外加工退貨率": {"dates": [], "values": []},
        "離職率": {"dates": [], "values": []},
        "庫存水位": {"dates": [], "values": []}
    }

    for entry in data:
        kpi_name = entry['kpi_name']
        kpi_data[kpi_name]["dates"].append(entry['date'].strftime('%Y-%m-%d'))  # 格式化日期
        kpi_data[kpi_name]["values"].append(entry['value'])  # KPI 數值

    print("KPI Data:", kpi_data)  # 打印資料來檢查

    return render(request, "index.html", {
        'kpi_data': kpi_data
    })

def dashboard(request):
    return render(request, "index.html")

from django.shortcuts import render, redirect  # 匯入 render 用於渲染模板，redirect 用於重導向
from .forms import DashboardForm  # 匯入剛剛定義的 DashboardForm
from .models import Dashboard  # 匯入 Dashboard 模型

# 定義 components_alerts 視圖函式
def components_alerts(request):
    if request.method == "POST":  # 如果收到 POST 請求，表示用戶提交了表單
        form = DashboardForm(request.POST)  # 用提交的數據建立表單實例
        if form.is_valid():  # 驗證表單數據是否有效
            form.save()  # 將表單數據儲存到資料庫
            return redirect('components-alerts.html')  # 儲存成功後重新導向到 alerts 頁面，避免表單重複提交

    else:  # 如果是 GET 請求，則建立一個空白的表單
        form = DashboardForm()

    # 取得所有 KPI 數據，並按日期排序
    kpi_data = Dashboard.objects.all().order_by('date')

    # 渲染 components-alerts.html 頁面，並傳遞表單和 KPI 數據到模板
    return render(request, 'components-alerts.html', {'form': form, 'kpi_data': kpi_data})


def components_accordion(request):
    return render(request, "components-accordion.html")
def components_badges(request):
    return render(request, "components-badges.html")

def components_breadcrumbs(request):
    return render(request, "components-breadcrumbs.html")

def components_buttons(request):
    return render(request, "components-buttons.html")

def components_cards(request):
    return render(request, "components-cards.html")

def components_carousel(request):
    return render(request, "components-carousel.html")

def components_list_group(request):
    return render(request, "components-list-group.html")

def components_modal(request):
    return render(request, "components-modal.html")

def components_tabs(request):
    return render(request, "components-tabs.html")

def components_pagination(request):
    return render(request, "components-pagination.html")

def components_progress(request):
    return render(request, "components-progress.html")

def components_spinners(request):
    return render(request, "components-spinners.html")

def components_tooltips(request):
    return render(request, "components-tooltips.html")

def users_profile(request):
    return render(request, "users-profile.html")

def pages_faq(request):
    return render(request, "pages-faq.html")

def pages_contact(request):
    return render(request, "pages-contact.html")

def pages_register(request):
    return render(request, "pages-register.html")

def pages_login(request):
    return render(request, "pages-login.html")

def pages_error_404(request):
    return render(request, "pages-error-404.html")

def pages_blank(request):
    return render(request, "pages-blank.html")

def forms_elements(request):
    return render(request, "forms-elements.html")

def forms_layouts(request):
    return render(request, "forms-layouts.html")

def forms_editors(request):
    return render(request, "forms-editors.html")

def forms_validation(request):
    return render(request, "forms-validation.html")

def icons_bootstrap(request):
    return render(request, "icons-bootstrap.html")

def icons_remix(request):
    return render(request, "icons-remix.html")

def icons_boxicons(request):
    return render(request, "icons-boxicons.html")

def charts_chartjs(request):
    return render(request, "charts-chartjs.html")

def charts_apexcharts(request):
    return render(request, "charts-apexcharts.html")

def charts_echarts(request):
    return render(request, "charts-echarts.html")

def tables_general(request):
    return render(request, "tables-general.html")

def tables_data(request):
    return render(request, "tables-data.html")

def student_list(request):
    return render(request, "students.html")