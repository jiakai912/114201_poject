from django.shortcuts import render
from django.http import JsonResponse
from .models import Dashboard  # 引入 Dashboard 模型
from django.shortcuts import redirect
from .forms import DashboardForm

def home(request):
    analysis_result = None
    error_message = None
    dream_text = ""  # 新增變數來保存使用者輸入的文字

    keywords_set = {
        "掉牙": {"keywords": ["掉牙", "變化", "焦慮"], "sentiment": "焦慮", "interpretation": "掉牙夢境可能代表焦慮或即將發生的變化。"},
        "飛行": {"keywords": ["飛行", "自由", "快樂"], "sentiment": "興奮", "interpretation": "飛行夢境通常象徵自由與掌控能力的提升。\
               處於成長階段時，夢見自己飛翔是正在長高這種生理現象的反映。成人夢見飛上天空則大多象徵著自由和成功，是自信的表現。\
               如果夢見自己飛起來的時候心情是愉快的，應該是近期在生活中有很多收穫，如果夢見自己飛翔時心情是緊張的或憂鬱的，\
               那麼應該是在潛意識裡對現實的一種逃避。另外印度古人認為效能量沿通道到達頭頂就會夢見飛，中國古人認為“上盛則夢飛”。\
               中醫認為上焦即頭到胃口這一部位，包括胸、頭、心肺處有病，病屬於實癥，則容易夢見飛。"},
        "蛇": {"keywords": ["蛇", "恐懼", "潛在危險"], "sentiment": "恐懼", "interpretation": "夢見蛇可能象徵潛在的威脅或內心的恐懼。"}
    }

    if request.method == 'POST':
        dream_text = request.POST.get('dream_input', '').strip()  # 取得使用者輸入的夢境內容

        if dream_text:
            for key, result in keywords_set.items():
                if key in dream_text:
                    analysis_result = result
                    break

            if not analysis_result:
                error_message = "未找到相關夢境分析結果。"
    return render(request, 'index.html', {'analysis_result': analysis_result, 'error_message': error_message, 'dream_text': dream_text})

def dashboard(request):
    return render(request, "index.html")

def components_alerts(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            form.save()  # 儲存到資料庫
            return redirect('components-alerts.html')  # 儲存後重新導向到 alerts 頁面
    else:
        form = DashboardForm()

    # 取得所有 KPI 數據
    kpi_data = Dashboard.objects.all().order_by('date')

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

    return render(request, "components-tooltips.html", {
        'kpi_data': kpi_data
    })

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
    # 取得所有的 "產量達成率" 資料
    data = Dashboard.objects.filter(kpi_name='產量達成率').values('date', 'value')  # 根據 kpi_name 篩選資料
    
    dates = []
    values = []

    # 填充資料列表
    for entry in data:
        dates.append(entry['date'].strftime('%Y-%m-%d'))  # 格式化日期為字符串
        values.append(entry['value'])  # 取得 KPI 值

    # 檢查數據是否正確
    print("Dates:", dates)
    print("Values:", values)

    # 傳遞資料給模板
    return render(request, "charts-chartjs.html", {
        'dates': dates,
        'values': values
    })

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
