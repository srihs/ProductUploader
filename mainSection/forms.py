from django import forms
from django.forms import ImageField
from django.db import models
from .models import Shipment, Products ,ShipmentDetail


# CreateShipmentForm
class CreateShipmentForm(forms.ModelForm):

    shipmentNumber = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'readonly': 'true',
               'placeholder': 'Shipment Number'}))

    shipmentDate = forms.DateField(required=True, widget=forms.DateInput(
        attrs={'style': 'margin-right: auto; margin-left: auto; text-align: center;margin-bottom: 2em', 'id': 'datepicker'}))

    class Meta:
        model = Shipment
        fields = ('shipmentNumber', 'shipmentDate')


class CreateProductForm(forms.ModelForm):

    sku = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'sku',
               'required': 'true', 'placeholder': 'SKU'}
    ))

    vendor = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'vendor',
               'required': 'true', 'placeholder': 'Vendor'}
    ))

    weight = forms.DecimalField(max_digits=10, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'weight',
               'required': 'true', 'placeholder': 'Weight in gms'}
    ))

    img = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control', 'id': 'productImage',
               'required': 'false'}
    ))

    productType = forms.CharField(max_length=50, required=True, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'productType',
               'required': 'true', 'placeholder': 'Product Type'}
    ))

    class Meta:
        model = Products
        fields = ['sku', 'vendor', 'weight',
                  'img', 'productType']


class CreateShipmentDetails(forms.ModelForm):
    indPrice = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'indPrice',
               'required': 'true', 'placeholder': 'Ind. Price'}
    ))

    qty = forms.DecimalField(max_digits=10, required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'qty',
               'required': 'true', 'placeholder': 'Qty'}
    ))

    class Meta:
        model = ShipmentDetail
        fields = ['indPrice', 'qty']
