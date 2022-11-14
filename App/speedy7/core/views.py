from django.shortcuts import render
from django.http import HttpResponse
from .models import Logs

# Create your views here.
def dashboard(response):
    
    all_logs = Logs.objects.all
    
    return render(response, 'speedy/dashboard.html', {"all_logs":all_logs})