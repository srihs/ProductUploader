from django.contrib import admin
from .models import Shipment,Products,ProductTypes


admin.site.register(Shipment)
admin.site.register(Products)
admin.site.register(ProductTypes)

