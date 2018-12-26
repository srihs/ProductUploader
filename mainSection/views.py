from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from .models import Shipment, ProductTypes, ShipmentDetail, Products
from django.utils import timezone
import json as simplejson
from .forms import CreateShipmentForm, CreateProductForm, CreateShipmentDetails

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)


@login_required
def home(request):
    #clearing the session form the system. so the New id will be facilitated
    request.session.flush()
    return render(request, '../templates/mainSection/home.html')


def createshipment(request):
    #clearing the session form the system. so the New id will be facilitated
    request.session.flush()

    if request.method == "GET":
        # shipmentNumber is defined by 'SHN-000' + next Id in the shipment Table
        try:
             # trying to retrive the next primaryKey
            nextId = Shipment.objects.all().count()
            nextId += 1
        except:
            # if the next ID is null define the record as the first
            nextId = 1
        # creating the form with the shipment ID
        form = CreateShipmentForm(
            initial={'shipmentNumber': 'SHN-000' + str(nextId)})

    return render(request, '../templates/mainSection/createshipment.html', {'form': form})


def saveshipment(request):
    if request.method == 'POST':
        form = CreateShipmentForm(request.POST)
        if form.is_valid():
            instance = form.save()
        else:
            messages.error(request, form.errors)
        return redirect('mainSection:fillshipment')


def viewshipment(request):
    return render(request, '../templates/mainSection/viewshipment.html')


def fillshipment(request):
    
    #initializing objects
    productForm = CreateProductForm()
    shipmentDetailForm = CreateShipmentDetails()
    shipmentItem_list = None
    selectedShipment = None
    
    # Retrieving The Product types for the ShipmentForm
    productType_list = ProductTypes.objects.all()
    

    # Retrieving The shipments which are open to fill.
    shipment_list = Shipment.objects.all()

    # if the request if for a shipment that is selected in the dropdown the the following code block will execute
    if request.GET.get('shipmentDropDown'):
 
        #getting the shipmentID
        shipmentID = request.GET.get('shipmentDropDown')
 
        #getting the shipment List
        shipmentItem_list = getShipmentItemsList(shipmentID)
    
        #Saving the selected Shipment object to passback to the template
        selectedShipment = get_object_or_404(Shipment,pk=shipmentID)

        #stroing the shipment Id for the save operation
        request.session['shipmentID'] = selectedShipment.id
        
    # This block will handel the requests with out shipping Id
    elif request.method =='GET' and 'shipmentID' in request.session:
        shipmentItem_list = getShipmentItemsList(request.session['shipmentID'])
        selectedShipment = get_object_or_404(Shipment,pk=request.session['shipmentID'])

    return render(request, '../templates/mainSection/fillshipment.html', {'selectedShipment':selectedShipment, 'productTypes': productType_list, 'shipments': shipment_list, 'productForm': productForm, 'shipmentDetails': shipmentItem_list, 'ShipmentForm': shipmentDetailForm})

#This function will accept a shipmentID and return a shipmentItemList
def getShipmentItemsList(shipmentId):
    
    if shipmentId is None:
        shipmentItem_list = None
    else:
        shipmentItem_list = ShipmentDetail.objects.filter(shipment=shipmentId).select_related('product').select_related('product__types')
    return shipmentItem_list

    

def saveproduct(request):
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES )
        shipmentDetialForm = CreateShipmentDetails(request.POST)
        
       
        # loading the product type that was assigned to the product
        productType = get_object_or_404(
            ProductTypes, pk=request.POST['productType'])

        # loading the ShipmentID
        shipmentID = request.session['shipmentID']

        if form.is_valid() and shipmentDetialForm.is_valid():
            file = form.cleaned_data['img']
            productObj = form.save(commit=False)
            
            # assigning the product Type
            productObj.types = productType
            productObj.productImg = request.FILES['img']
            # productObj.productImage=file
            productObj.save()
           
            # creating the shipment detail Object
            shipmentDetailObj= shipmentDetialForm.save(commit=False)
            shipmentDetailObj.product = productObj
            shipmentDetailObj.shipment = Shipment.objects.get(id=shipmentID)
            shipmentDetailObj.save()
            

        else:
            messages.error(request, form.errors)

        return redirect('mainSection:fillshipment')
