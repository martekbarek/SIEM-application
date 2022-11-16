from django.shortcuts import render
from django.http import HttpResponse
from .models import Log
from .filters import LogFilter

# Create your views here.
def dashboard(response):
    
    all_logs = Log.objects.all
    
    myFilter = LogFilter()
    
    
    
    context = {"all_logs":all_logs, 'myFilter':myFilter}
    
    return render(response, 'speedy/dashboard.html', context)


def dashboardFilter(request):
    
    all_logs = Log.objects.all
    
    myFilter = LogFilter(request.GET, queryset=all_logs)
    all_logs = myFilter.qs
    
    context = {"all_logs":all_logs, 'myFilter':myFilter}
    
    return render(request, 'speedy/dashboard.html', context)