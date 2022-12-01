from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name ='speedy'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assets/', views.assets, name='assets'),
    path('help/', views.help, name='help'),

    path('register/', views.registerPage, name='registerPage'),
    path('', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logoutUser'),
    
    path('users/', views.users, name='users'),
    path('user/', views.userView, name='userView'),
    path('user/edit/<int:id>', views.editUser, name='editUser'),
    path('user/delete/<int:id>', views.deleteUser, name='deleteUser'),
    path('user/password/change', views.changePass, name='changePass'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
