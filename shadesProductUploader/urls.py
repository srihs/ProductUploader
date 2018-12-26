from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('',include('mainSection.urls')),
    path('admin/', admin.site.urls),
    path('',include('authSection.urls')),
    
] 
