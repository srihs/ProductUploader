from django.contrib import admin
from django.urls import path,include

from . import views

app_name = 'mainSection'

urlpatterns = [
    path('home/', views.home,name="home"),
    path('createshipment/',views.createshipment,name="createshipment"),
    path('home/createshipment/saveshipment/',views.saveshipment,name="saveshipment"),
    path('fillshipment/',views.fillshipment,name="fillshipment"),
    path('saveproduct/',views.saveproduct,name="saveproduct"),
    path('viewhipment/',views.viewshipment,name="viewshipment"),
] 

