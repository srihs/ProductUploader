from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Shipment, Products, ProductTypes, User


admin.site.register(Shipment)
admin.site.register(Products)
admin.site.register(ProductTypes)



# adding custom fields to the admin
UserAdmin.list_display += ('is_buyer','is_officeUser','is_storeUser',)  # don't forget the commas
UserAdmin.list_filter += ('is_buyer','is_officeUser','is_storeUser',)
UserAdmin.fieldsets += (('Roles', {'fields': ('is_buyer','is_officeUser','is_storeUser')}),)


admin.site.register(User,UserAdmin)


