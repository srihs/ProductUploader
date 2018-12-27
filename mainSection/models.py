from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import RegexValidator




class Shipment(models.Model):
    id = models.AutoField(primary_key=True)
    shipmentNumber = models.CharField(max_length=50)
    shipmentDate = models.DateField()
    isClosed = models.BooleanField(default='False')
    dateCreated = models.DateTimeField(default=timezone.now)
    dateModified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.shipmentNumber

 
class ProductTypes(models.Model):
   id = models.AutoField(primary_key=True)
   productType=models.CharField(max_length=100)

   class Meta:
        verbose_name_plural = "ProductTypes"
   
   def __str__(self):
        return self.productType   

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    sku= models.CharField(max_length=100)
    vendor= models.CharField(max_length=500, blank=True)
    weight = models.PositiveIntegerField()
    sellingPrice  = models.DecimalField(decimal_places=2,max_digits=10,null=True, blank=True)
    productImg = models.ImageField(upload_to=settings.MEDIA_ROOT+'/%Y/%m/%d/', null=True, blank=True, max_length=5000)
    types= models.ForeignKey(ProductTypes, on_delete=models.CASCADE)
    archived = models.BooleanField(default='False')
    dateCreated = models.DateTimeField(default=timezone.now)
    dateModified = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.sku
    

   
class ShipmentDetail(models.Model):
    id = models.AutoField(primary_key=True)
    shipment = models.ForeignKey(Shipment,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    indPrice = models.DecimalField(decimal_places=2,max_digits=10,null=True, blank=True)
    qty  = models.PositiveIntegerField(null=True, blank=True)
    totalAmount  = models.PositiveIntegerField(null=True, blank=True)
    cost= models.DecimalField(decimal_places=2,max_digits=10,null=True, blank=True)
    billDate = models.DateField(default=timezone.now)
    billNumber = models.PositiveIntegerField(null=True, blank=True)
    archived = models.BooleanField(default='False')
    dateCreated = models.DateTimeField(default=timezone.now)
    dateModified = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "ShipmentDetails"

    @property
    def totalAmount(self):
        return self.indPrice * self.qty
        

    
   
