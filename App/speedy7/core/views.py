from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Log
from .filters import LogFilter
from dateutil import tz
import logging
import os
from datetime import datetime,timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout 
from .forms import *
from .templatetags.activityfilter import activityfilter

from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def dashboard(request):
    try:
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

        
        # tz = pytz.timezone("Europe/Warsaw")  -  set proper time zone

        # filter urgent logs
        incidents = tuple(log for log in Log.objects.order_by(
            'level') if (log.level in ['emerg','alert','crit','err'] ))
        logFilter = LogFilter(request.GET, queryset=all_logs)
        filteredLogs = logFilter.qs

        if 'time' in (req := request.GET) and req['time'] != '':
            minutes = req['time']
            filteredLogs = tuple(filter(lambda x: activityfilter(
                x.datetime, int(minutes)), filteredLogs))


        # prepare timechart values
        now = (n:=datetime.now()).replace(minute=(30 if n.minute > 30 else 0), second=0, microsecond=0)
        chart_hours = sorted(tuple(((now - timedelta(minutes=(x-1)*30)) for x in range(24))))
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

        
        return render(request, 'speedy/dashboard.html', context)
    except Exception:
        logging.info('No messages')
        return render(request, 'speedy/dashboard.html', {})
        

@login_required(login_url='/')
def users(request):
    users = User.objects.all()
    context = {'users':users}
    return render(request, 'accounts/users.html',context)
    
@login_required(login_url='/')
def assets(request):

    all_logs = Log.objects.all()
    hosts = set(item.host for item in all_logs)
    
    host_info_dict = {}
    # host_counter_dict = {}
    for name in hosts:
        last_activity = var if (var:=Log.objects.order_by('-datetime').filter(host=name).first().datetime) else None
        counter = 0
        for log in all_logs:
            if name in log.host:
                counter += 1
        host_info_dict[name]=(last_activity,counter)

    if request.method == "POST":
        hostname = request.POST.get('host')
        is_online = True if os.system("ping -c 1 " + hostname) == 0 else False
        context = {'host':hostname,'hosts':host_info_dict, 'is_online':is_online}
        return render(request, 'speedy/assets.html',context)
     
    context = {'hosts':host_info_dict}
    return render(request, 'speedy/assets.html',context)


@login_required(login_url='/')
def help(request):
   
    context = {}
    return render(request, 'speedy/help.html',context) 


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

@login_required(login_url='/')
def userView(request):
    user = User.objects.get(pk=request.user.id)
    context = {'user':user}
    return render(request, 'accounts/me.html', context=context)

@login_required(login_url='/')
def editUser(request,id):
    return redirect('/admin/auth/user/%s/change/' % (id,))
    
@login_required(login_url='/')
def deleteUser(request,id):
    return redirect('/admin/auth/user/%s/delete/' % (id,))

@login_required(login_url='/')
def changePass(request):
    id = request.user.id
    return redirect('/admin/auth/user/%s/password/' % (id,))

@login_required(login_url='/')
def logoutUser(request):
    logout(request)
    return redirect('/')


    # user = User.objects.get(pk=id)
    # userToEdit = EditUserForm(instance = user)

    # if request.method == 'POST':
    #     user = User.objects.get(username=request.POST.get('username'))
    #     edit_user_form = EditUserForm(request.POST, instance = user)
    #     if edit_user_form.is_valid:
    #         # user_to_edit = User.objects.get(username=request.POST['username'])
    #         edit_user_form.save(commit=False)
    #         messages.success(request, "Account was edited for ")
    #         return redirect('/users')
    
    # context = {'form':userToEdit}
    
    # return render(request, 'accounts/edit.html', context=context)