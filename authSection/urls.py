from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'authSection'

urlpatterns = [
    path('', views.login_view, name='login'),
    
]

