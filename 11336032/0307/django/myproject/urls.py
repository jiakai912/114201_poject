from django.contrib import admin
from django.urls import path
from mysite.views import home, components_alerts, dashboard, components_accordion, components_badges, components_breadcrumbs, \
    components_buttons, components_cards, components_carousel, components_list_group, components_modal, components_tabs, \
    components_pagination, components_progress, components_spinners, components_tooltips, users_profile, pages_faq, \
    pages_contact, pages_register, pages_login, pages_error_404, pages_blank, forms_elements, forms_layouts, \
    forms_editors, forms_validation, icons_bootstrap, icons_remix, icons_boxicons, charts_chartjs, charts_apexcharts, \
    charts_echarts, tables_general, tables_data

urlpatterns = [
    # Add this line to include Django admin URLs
    path('admin/', admin.site.urls),  # This will allow access to the Django admin panel

    # Your custom URLs
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
