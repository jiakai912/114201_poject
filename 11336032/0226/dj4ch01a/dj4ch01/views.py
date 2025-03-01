from django.shortcuts import render

def my_view(request):
    return render(request, 'charts-chartjs.html')  # 確保這裡的樣板名稱正確