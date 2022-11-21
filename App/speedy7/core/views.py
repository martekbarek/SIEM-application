from django.shortcuts import render
from django.http import HttpResponse
from .models import Log
from .filters import LogFilter

# Create your views here.
def dashboard(response):
    

    all_logs_query = Log.objects.order_by('-datetime').all
    all_logs = all_logs_query()
     
    myFilter = LogFilter()
    
    # get all facilities
    facilities = set(item.facility for item in all_logs)

    # Get count of facilities
    fac_counter_dict = {}
    for facility in facilities:
        counter = 0
        for log in all_logs:
            if facility in log.facility:
                counter+=1
        fac_counter_dict[facility]=counter     

    # get last activities and number of events per host
    hosts = set(item.host for item in all_logs)
    last_activity_dict = {}
    host_counter_dict = {}
    for name in hosts:
        last_activity_dict[name]=Log.objects.order_by('-datetime').filter(host=name).first()
        counter = 0
        for log in all_logs:
            if name in log.host:
                counter+=1
        host_counter_dict[name]=counter 
    
    # filter urgent logs   
    incidents = tuple(log for log in Log.objects.order_by('level') if int(log.level[-1]) <= 3)

    context = {"all_logs":all_logs, "facilities":facilities,"hosts":hosts,"host_counter_dict":host_counter_dict ,"incidents":incidents,"last_activity_dict":last_activity_dict, 'myFilter':myFilter}
    
    if response.method == "GET":
        filteredLogs = LogFilter(response.GET, queryset=all_logs)
        context = {"all_logs":filteredLogs.qs, "facilities":facilities,"hosts":hosts,"host_counter_dict":host_counter_dict,"fac_counter_dict":fac_counter_dict ,"incidents":incidents,"last_activity_dict":last_activity_dict, 'myFilter':myFilter}
        return render(response, 'speedy/dashboard.html', context)

    
    return render(response, 'speedy/dashboard.html', context)
    
    
    
    
    
    
    
    
    
    
    
    
    
  
    
   
    