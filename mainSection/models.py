from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from decimal import *
import math


class User(AbstractUser):
    is_buyer = models.BooleanField(default=False)
    is_officeUser = models.BooleanField(default=False)
    is_storeUser = models.BooleanField(default=False)
    productCode  = models.CharField(max_length=50)


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    shippingPoint = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "ShippingPoints"

    def __str__(self):
        return self.shippingPoint


class Shipment(models.Model):
    id = models.AutoField(primary_key=True)
    shipmentNumber = models.CharField(max_length=50)
    shipmentDate = models.DateField()
    isClosed = models.BooleanField(default='False')
    isFinalized = models.BooleanField(default='False')
    isCostapplied = models.BooleanField(default='False')
    isCostbaseFinalized = models.BooleanField(default='False')
    costBase = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True)
    costFile = models.FileField(
        upload_to='Costing/%Y/%m/%d/', null=True, blank=True, max_length=5000)
    shippingPoint = models.ForeignKey(Country, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True)
    userCreated = models.CharField(max_length=500)
    dateModified = models.DateTimeField(auto_now=True)
    userModified = models.CharField(max_length=500)

    @property
    def __str__(self):
        return self.shipmentNumber


class ProductTypes(models.Model):
    id = models.AutoField(primary_key=True)
    productType = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "ProductTypes"

    def __str__(self):
        return self.productType


class ProductColour(models.Model):
    id = models.AutoField(primary_key=True)
    productColour = models.CharField(max_length=100)
    colourImg = models.ImageField(
        upload_to='images/%Y/%m/%d/', null=True, blank=True, max_length=5000)

    class Meta:
        verbose_name_plural = "ProductColours"

    def __str__(self):
        return self.productColour


class ProductSize(models.Model):
    id = models.AutoField(primary_key=True)
    productSize = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "ProductSize"

    def __str__(self):
        return self.productSize


class ProducBrands(models.Model):
    id = models.AutoField(primary_key=True)
    productBrand = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "ProductBrand"

    def __str__(self):
        return self.productBrand


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=100)
    brand = models.ForeignKey(ProducBrands, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.CharField(max_length=500, blank=True)
    weight = models.PositiveIntegerField()
    sellingPrice = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True)
    productImg = models.ImageField(
        upload_to='images/%Y/%m/%d/', null=True, blank=True, max_length=5000)
    types = models.ForeignKey(ProductTypes, on_delete=models.CASCADE, null=True, blank=True)
    colour = models.ForeignKey(ProductColour, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True, blank=True)
    archived = models.BooleanField(default='False')
    dateCreated = models.DateTimeField(auto_now_add=True)
    userCreated = models.CharField(max_length=500)
    dateModified = models.DateTimeField(auto_now=True)
    userModified = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "Products"

    @property
    def productName(self):
        return str(self.brand) + " " + str(self.types)

    def __str__(self):
        return self.sku


class ShipmentDetail(models.Model):
    id = models.AutoField(primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    indPrice = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True)
    qty = models.PositiveIntegerField(null=True, blank=True)
    receivedQty = models.PositiveIntegerField(null=True, blank=True, default=0)
    weight = models.PositiveIntegerField()
    totalAmount = models.PositiveIntegerField(null=True, blank=True)
    costBase = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True)
    cost = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True)
    sellingPrice50 = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True)
    sellingPrice75 = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True)
    sellingPrice = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True)
    billDate = models.DateField(default=timezone.now)
    billNumber = models.PositiveIntegerField(null=True, blank=True)
    is_checked = models.BooleanField(default='False') # occured when the shipment item is checked and selling price set
    is_completeReceive = models.BooleanField(default='False') # if the qty= receivedQty this will be true
    is_grn = models.BooleanField(default='False') # checked from the stores
    archived = models.BooleanField(default='False')
    dateCreated = models.DateTimeField(auto_now_add=True)
    userCreated = models.CharField(max_length=500)
    dateModified = models.DateTimeField(auto_now=True)
    userModified = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "ShipmentDetails"

    @property
    def totalAmount(self):
        return self.indPrice * self.qty

    @property
    def cost(self):
        # CONVERTED TO DECIMAL TO AVOID unsupported operand type(s) for *: 'decimal.Decimal' and 'float'
        cost = Decimal(self.costBase) * Decimal(self.indPrice)
        return cost
    
    @property
    def sellingPrice50(self):
        # Roundin upo to highest 10
        return int(math.ceil((Decimal(Decimal(self.cost) +  Decimal(self.cost * Decimal(0.5)))/10)))*10

    @property
    def sellingPrice75(self):
        # Rounding upo to highest 10
        return int(math.ceil((Decimal(Decimal(self.cost) +  Decimal(self.cost * Decimal(0.75)))/10)))*10
