from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Shipment, Products, ProductTypes, User, Country, ProductColour, ProductSize, ProducBrands, CutomerType


admin.site.register(Shipment)
admin.site.register(Products)
admin.site.register(ProductTypes)
admin.site.register(ProductColour)
admin.site.register(ProductSize)
admin.site.register(ProducBrands)
admin.site.register(CutomerType)


admin.site.register(Country)

# adding custom fields to the admin
UserAdmin.list_display += ('is_buyer', 'is_officeUser', 'is_storeUser', 'productCode',)  # don't forget the commas
UserAdmin.list_filter += ('is_buyer', 'is_officeUser', 'is_storeUser',)
UserAdmin.fieldsets += (('Roles', {'fields': ('is_buyer', 'is_officeUser', 'is_storeUser')}),)
UserAdmin.fieldsets += (('Product Code', {'fields': ('productCode',)}),)  # default product Code for the User

admin.site.register(User, UserAdmin)


