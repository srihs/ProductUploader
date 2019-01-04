from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'mainSection'

urlpatterns = [
    path('home/', views.home, name="home"),
    path('createshipment/', views.createshipment, name="createshipment"),
    path('home/createshipment/saveshipment/', views.saveshipment, name="saveshipment"),
    path('fillshipment/', views.fillshipment, name="fillshipment"),
    path('saveproduct/', views.saveproduct, name="saveproduct"),
    path('viewhipment/', views.viewshipment, name="viewshipment"),
    path('reviewshipment/', views.reviewShipment, name="reviewshipment"),
    path('costfactor/', views.generateCostFactor, name="costfactor"),
    path('delete/<int:pk>', views.deleteshipmentdetail, name="deleteshipmentdetail"),
    path('finalizeshipment/', views.finalizeshipment, name="finalizeshipment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


