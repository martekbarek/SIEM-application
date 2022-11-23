from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Log
from .filters import LogFilter
from dateutil import tz
from datetime import datetime,timedelta
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout 
from .forms import *
from .templatetags.activityfilter import activityfilter

from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def dashboard(response):

    all_logs_query = Log.objects.order_by('-datetime').all
    all_logs = all_logs_query()

    # get all facilities
    facilities = set(item.facility for item in all_logs)

    # Get count of facilities
    fac_counter_dict = {}
    for facility in facilities:
        counter = 0
        for log in all_logs:
            if facility in log.facility:
                counter += 1
        fac_counter_dict[facility] = counter

    # get last activities and number of events per host
    hosts = set(item.host for item in all_logs)
    last_activity_dict = {}
    host_counter_dict = {}
    for name in hosts:
        last_activity_dict[name] = Log.objects.order_by(
            '-datetime').filter(host=name).first()
        counter = 0
        for log in all_logs:
            if name in log.host:
                counter += 1
        host_counter_dict[name] = counter

    # sort last_activity_dict by date
    sorted_last_activity_dict = dict(sorted(last_activity_dict.items(), key=lambda x : x[1].datetime, reverse=True))

    
    # filter urgent logs
    incidents = tuple(log for log in Log.objects.order_by(
        'level') if int(log.level[-1]) <= 3)
    logFilter = LogFilter(response.GET, queryset=all_logs)
    filteredLogs = logFilter.qs

    if 'time' in (req := response.GET) and req['time'] != '':
        minutes = req['time']
        filteredLogs = tuple(filter(lambda x: activityfilter(
            x.datetime, int(minutes)), filteredLogs))


    # prepare timechart values
    now = (n:=datetime.now(tz=tz.gettz("UTC"))).replace(minute=(30 if n.minute > 30 else 0), second=0, microsecond=0)
    chart_hours = sorted(tuple(((now - timedelta(minutes=(x-2)*30)) for x in range(24))))
    activity_hours = dict(zip(chart_hours, [tuple()]*len(chart_hours)))
    for log in all_logs :
        if (time:=log.datetime.replace(minute=(30 if log.datetime.minute > 30 else 0), second=0, microsecond=0)) in chart_hours:
            activity_hours[time]+=(log,)


    context = {"all_logs": filteredLogs, "facilities": facilities,
               "hosts": hosts,
               "host_counter_dict": host_counter_dict,
               "fac_counter_dict": fac_counter_dict,
               "incidents": incidents,
               "activity_hours": activity_hours,
               "last_activity_dict": sorted_last_activity_dict,
               "myFilter": logFilter}

    return render(response, 'speedy/dashboard.html', context)


def registerPage(request):
    
    if request.user.is_authenticated:
        return redirect('dashboard/')

    form = RegisterForm()
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for " + user)

            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/register.html', context=context)

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('dashboard/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard/')
        else:
            messages.info(request, 'Username OR password is incorrect')
        
    context = {}
    return render(request, 'accounts/login.html', context=context)


def logoutUser(request):
    logout(request)
    return redirect('/')