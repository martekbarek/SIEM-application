from django.urls import path

from . import views

app_name ='speedy'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.registerPage, name='registerPage'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('', views.loginPage, name='loginPage'),
]
