from django.contrib import admin
from django.urls import path,include
from django.conf import settings


urlpatterns = [
    path('',include('mainSection.urls')),
    path('admin/', admin.site.urls),
    path('',include('authSection.urls')),
    
] 
