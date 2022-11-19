from django.shortcuts import render
from django.http import HttpResponse
from .models import Log
from .filters import LogFilter

# Create your views here.
def dashboard(response):
    
    all_logs = Log.objects.order_by('-datetime').all()
    
    myFilter = LogFilter()
    
    facilities = set(item.facility for item in all_logs)
   
    fac_counter_dict = {}
    for facility in facilities:
        counter = 0
        for log in all_logs:
            if facility in log.facility:
                counter+=1
        fac_counter_dict[facility]=counter        
       
    hosts = set(item.host for item in all_logs)
    last_activity_dict = {}
    for name in hosts:
        last_activity_dict[name]=Log.objects.order_by('-datetime').filter(host=name).first()
    
    
      
    
    context = {"all_logs":all_logs, "fac_counter_dict":fac_counter_dict ,"last_activity_dict":last_activity_dict, 'myFilter':myFilter}
    
    return render(response, 'speedy/dashboard.html', context)
