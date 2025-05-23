import markdown  # 匯入 markdown 套件，用於解析 Markdown 語法

from django import template  # 匯入 Django 的 template 模組，用於建立自訂模板過濾器
from django.template.defaultfilters import stringfilter  # 匯入 stringfilter，用於確保輸入是字串

# 註冊自訂模板過濾器
register = template.Library()

@register.filter  # 使用 @register.filter 裝飾器來註冊此函式為模板過濾器
@stringfilter  # 確保輸入是字串，避免類型錯誤
def convert_markdown(text):
    """將 Markdown 文字轉換為 HTML"""
    return markdown.markdown(text)  # 使用 markdown 函式解析並轉換 Markdown 為 HTML
