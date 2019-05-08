from django import forms
from django.forms import ImageField
from django.db import models
from .models import Shipment, Products ,ShipmentDetail, Customer


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
               'required': 'true', 'placeholder': 'Weight in gms','min':1}
    ))

    img = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control', 'id': 'productImage',
               'required': 'false'}
    ))

    productType = forms.CharField(max_length=50, required=True, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'productType',
               'required': 'true', 'placeholder': 'Product Type'}
    ))

    productSize = forms.CharField(max_length=50, required=True, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'productSize',
               'required': 'true', 'placeholder': 'Size'}
    ))

    productColour = forms.CharField(max_length=50, required=True, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'productSize',
               'required': 'true', 'placeholder': 'Colour'}
    ))

    class Meta:
        model = Products
        fields = ['sku', 'vendor', 'weight',
                  'img', 'productType', 'productSize', 'productColour']


class CreateShipmentDetails(forms.ModelForm):
    indPrice = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'indPrice',
               'required': 'true', 'placeholder': 'Price','min':1}
    ))

    qty = forms.DecimalField(max_digits=10, required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'qty',
               'required': 'true', 'placeholder': 'Qty','min':1}
    ))

    billNumber = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'billNumber',
               'placeholder': 'Bill Number', 'min':1}
    ))

    billDate = forms.DateField(required=True, widget=forms.DateInput(
        attrs={'class': 'form-control','style': 'text-align: center;', 'id': 'datepicker2','placeholder': 'Bill Date'}))



    class Meta:
        model = ShipmentDetail
        fields = ['indPrice', 'qty' , 'billDate','billNumber', 'sellingPrice', 'receivedQty']


class CreateCostFactorForm(forms.ModelForm):
    costBase = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'costBase',
               'required': 'true', 'min':1}
    ))

    costFile = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'costFile',
               'required': 'true', 'accept': 'application/xls',  'accept': 'application/xlsx'}
    ))

    class Meta:
        model = Shipment
        fields = ['costBase', 'costFile']


class sellingPriceForm(forms.ModelForm):
    sellingPrice = forms.DecimalField(max_digits=10, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'sellingPrice',
               'required': 'true', 'placeholder': 'Selling Price', 'min': 1}
    ))
    class Meta:
        model = ShipmentDetail
        fields = ['sellingPrice']

class GRNForm(forms.ModelForm):
    receivedQty = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'receivedQty',
               'required': 'true', 'placeholder': 'Received Qty', 'min': 1}
    ))
    class Meta:
        model = ShipmentDetail
        fields = ['receivedQty']


class CustomerForm(forms.ModelForm):
    customerNumber = forms.CharField(max_length=10, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'readonly': 'true',
               'placeholder': 'Customer Number'}))

    customerFirstName = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'customerFirstName',
                'placeholder': 'First Name'}
    ))

    customerLastName = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'customerLastName',
                'placeholder': 'Last Name'}
    ))

    customerAddress1 = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'customerAddress1',
               'placeholder': 'Address Line 1'}
    ))

    customerAddress2 = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'customerAddress2',
                'placeholder': 'Address Line 2'}
    ))

    customerAddress3 = forms.CharField(max_length=150, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'customerAddress3',
                'placeholder': 'Address Line 3'}
    ))

    customerPhone = forms.CharField(max_length=10, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'customerPhone',
                'placeholder': 'Phone'}
    ))

    customerWhatsApp = forms.CharField(max_length=50, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'customerWhatsApp',
                'placeholder': 'WhatsApp number'}
    ))

    customerEmail = forms.CharField(max_length=50, required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'id': 'customerEmail',
                'placeholder': 'Email'}
    ))

    customerCompany = forms.CharField(max_length=150, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'customerCompany',
                'placeholder': 'Comany'}
    ))

    creditPeriod = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'creditPeriod', 'required': 'false',
               'placeholder': 'Credit Period', 'min': 0}
    ))

    class Meta:
        model = Customer
        fields = ['customerFirstName', 'customerLastName', 'customerAddress1', 'customerAddress2', 'customerAddress3', 'customerPhone',
                  'customerWhatsApp', 'customerEmail', 'customerCompany', 'customerType', 'customerNumber', 'customerNumber', 'creditPeriod']
    

