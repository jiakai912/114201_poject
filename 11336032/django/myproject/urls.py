# 引入 Django 的 admin 模組，用來在後台管理模型
from django.contrib import admin

# 引入 Django 的 URL 路由模組，用來設定 URL 配置
from django.urls import path

# 引入專案內的視圖函式
# 這些視圖函式處理各個頁面的顯示邏輯，通常會對應到 templates 中的 HTML 頁面
from mysite.views import (
    home,  # 主頁
    components_alerts,  # 元件：提示訊息
    dashboard,  # 儀表板頁面
    components_accordion,  # 元件：手風琴
    components_badges,  # 元件：徽章
    components_breadcrumbs,  # 元件：麵包屑
    components_buttons,  # 元件：按鈕
    components_cards,  # 元件：卡片
    components_carousel,  # 元件：輪播圖
    components_list_group,  # 元件：列表群組
    components_modal,  # 元件：模態框
    components_tabs,  # 元件：標籤頁
    components_pagination,  # 元件：分頁
    components_progress,  # 元件：進度條
    components_spinners,  # 元件：旋轉圖標
    components_tooltips,  # 元件：工具提示
    users_profile,  # 使用者資料頁面
    pages_faq,  # 常見問題頁面
    pages_contact,  # 聯絡我們頁面
    pages_register,  # 註冊頁面
    pages_login,  # 登入頁面
    pages_error_404,  # 404 錯誤頁面
    pages_blank,  # 空白頁面
    forms_elements,  # 表單：表單元素
    forms_layouts,  # 表單：佈局
    forms_editors,  # 表單：編輯器
    forms_validation,  # 表單：驗證
    icons_bootstrap,  # 圖示：Bootstrap 圖示
    icons_remix,  # 圖示：Remix 圖示
    icons_boxicons,  # 圖示：Boxicons 圖示
    charts_chartjs,  # 圖表：Chart.js 圖表
    charts_apexcharts,  # 圖表：ApexCharts 圖表
    charts_echarts,  # 圖表：ECharts 圖表
    tables_general,  # 表格：一般表格
    tables_data  # 表格：數據表格
)


urlpatterns = [
    # 設定 Django 內建的 admin URL
    path('admin/', admin.site.urls), # 這行會讓你能夠通過 /admin 訪問 Django 的後台管理介面
    
     # 自定義的 URL 配置，將不同路徑映射到對應的視圖函式
    path('', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('components-alerts', components_alerts, name='alert'),
    path('components-accordion', components_accordion, name='accordion'),
    path('components-badges', components_badges, name='badges'),
    path('components-breadcrumbs', components_breadcrumbs, name='breadcrumbs'),
    path('components-buttons', components_buttons, name='buttons'),
    path('components-cards', components_cards, name='cards'),
    path('components-carousel', components_carousel, name='carousel'),
    path('components-list-group', components_list_group, name='list_group'),
    path('components-modal', components_modal, name='modal'),
    path('components-tabs', components_tabs, name='tabs'),
    path('components-pagination', components_pagination, name='pagination'),
    path('components-progress', components_progress, name='progress'),
    path('components-spinners', components_spinners, name='spinners'),
    path('components-tooltips', components_tooltips, name='tooltips'),
    path('users-profile', users_profile, name='users_profile'),
    path('pages-faq', pages_faq, name='faq'),
    path('pages-contact', pages_contact, name='contact'),
    path('pages-register', pages_register, name='register'),
    path('pages-login', pages_login, name='login'),
    path('pages-error-404', pages_error_404, name='error_404'),
    path('pages-blank', pages_blank, name='blank'),
    path('forms-elements', forms_elements, name='forms_elements'),
    path('forms-layouts', forms_layouts, name='forms_layouts'),
    path('forms-editors', forms_editors, name='forms_editors'),
    path('forms-validation', forms_validation, name='forms_validation'),
    path('icons-bootstrap', icons_bootstrap, name='icons_bootstrap'),
    path('icons-remix', icons_remix, name='icons_remix'),
    path('icons-boxicons', icons_boxicons, name='icons_boxicons'),
    path('charts-chartjs', charts_chartjs, name='charts_chartjs'),
    path('charts-apexcharts', charts_apexcharts, name='charts_apexcharts'),
    path('charts-echarts', charts_echarts, name='charts_echarts'),
    path('tables-general', tables_general, name='tables_general'),
    path('tables-data', tables_data, name='tables_data'),

    # HTML page routing
    path('index.html', home, name='index_html'),
    path('components-alerts.html', components_alerts, name='alert_html'),
    path('dashboard.html', dashboard, name='dashboard_html'),
    path('components-accordion.html', components_accordion, name='accordion_html'),
    path('components-badges.html', components_badges, name='badges_html'),
    path('components-breadcrumbs.html', components_breadcrumbs, name='breadcrumbs_html'),
    path('components-buttons.html', components_buttons, name='buttons_html'),
    path('components-cards.html', components_cards, name='cards_html'),
    path('components-carousel.html', components_carousel, name='carousel_html'),
    path('components-list-group.html', components_list_group, name='list_group_html'),
    path('components-modal.html', components_modal, name='modal_html'),
    path('components-tabs.html', components_tabs, name='tabs_html'),
    path('components-pagination.html', components_pagination, name='pagination_html'),
    path('components-progress.html', components_progress, name='progress_html'),
    path('components-spinners.html', components_spinners, name='spinners_html'),
    path('components-tooltips.html', components_tooltips, name='tooltips_html'),
    path('users-profile.html', users_profile, name='users_profile_html'),
    path('pages-faq.html', pages_faq, name='faq_html'),
    path('pages-contact.html', pages_contact, name='contact_html'),
    path('pages-register.html', pages_register, name='register_html'),
    path('pages-login.html', pages_login, name='login_html'),
    path('pages-error-404.html', pages_error_404, name='error_404_html'),
    path('pages-blank.html', pages_blank, name='blank_html'),
    path('forms-elements.html', forms_elements, name='forms_elements_html'),
    path('forms-layouts.html', forms_layouts, name='forms_layouts_html'),
    path('forms-editors.html', forms_editors, name='forms_editors_html'),
    path('forms-validation.html', forms_validation, name='forms_validation_html'),
    path('icons-bootstrap.html', icons_bootstrap, name='icons_bootstrap_html'),
    path('icons-remix.html', icons_remix, name='icons_remix_html'),
    path('icons-boxicons.html', icons_boxicons, name='icons_boxicons_html'),
    path('charts-chartjs.html', charts_chartjs, name='charts_chartjs_html'),
    path('charts-apexcharts.html', charts_apexcharts, name='charts_apexcharts_html'),
    path('charts-echarts.html', charts_echarts, name='charts_echarts_html'),
    path('tables-general.html', tables_general, name='tables_general_html'),
    path('tables-data.html', tables_data, name='tables_data_html'),
]
