from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from .models import Shipment, ProductTypes, ShipmentDetail, Products
from django.utils import timezone
import json as simplejson
from .forms import CreateShipmentForm, CreateProductForm, CreateShipmentDetails
from django.contrib.auth.models import AbstractUser
from  django.http import QueryDict

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)


@login_required
def home(request):
    #clearing the session form the system. so the New id will be facilitated
    return render(request, '../templates/mainSection/home.html')


#This method will handle the createshipment request
@login_required
def createshipment(request):
    if request.method == "GET":
        print(request.user)
          #clearing the session form the system. so the New id will be facilitated
        request.session['shipmentID'] =None
        request.session.modified = True

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

    return render(request, '../templates/mainSection/createshipment.html', {'form': form,'user': request.user})



#This method will handle the Save shipment request
@login_required
def saveshipment(request):
    if request.method == 'POST':
        form = CreateShipmentForm(request.POST)
        if form.is_valid():
            objShipment = form.save(commit=False)
            print(request.user.id)
            objShipment.buyer = request.user
            objShipment.save()
        else:
            messages.error(request, form.errors)
        return redirect('mainSection:fillshipment')


@login_required
def viewshipment(request):
    # Retrieving The shipments which are open to fill.
    shipment_list = Shipment.objects.filter(buyer=request.user)
    shipmentItem_list =None

    if request.method == 'GET':
        return render(request, '../templates/mainSection/viewshipment.html',{'shipments': shipment_list})

    if request.method=='POST':
        # if the request if for a shipment that is selected in the dropdown the the following code block will execute
        if request.POST['shipmentDropDown']: 
           
            #getting the shipmentID
            shipmentID = request.POST['shipmentDropDown']
              
            #getting the shipment List
            shipmentItem_list = getShipmentItemsList(shipmentID)
            
        else:
            messages.error(request,"Something went wrong.")
        
        return render(request, '../templates/mainSection/viewshipment.html',{'shipments': shipment_list, 'shipmentDetails': shipmentItem_list })




#This method will handle the fillshipment request
@login_required
def fillshipment(request):
    #initializing objects
    productForm = CreateProductForm()
    shipmentDetailForm = CreateShipmentDetails()
    shipmentItem_list = None
    selectedShipment = None
    
    # Retrieving The Product types for the ShipmentForm
    productType_list = ProductTypes.objects.all()
    

    # Retrieving The shipments which are open to fill. Only loged in users orders will be listed.
    shipment_list = Shipment.objects.filter(isClosed='False',isFinalized='0',buyer=request.user)

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
    elif request.method =='GET' and request is not None and 'shipmentID' in request.session and request.session['shipmentID'] is not None :
        shipmentItem_list = getShipmentItemsList(request.session['shipmentID'])
        #since the session.flush is voided due to the the authentication issue, ShipmentID is set to null in the sessio variable
        #therefor need to check for null.
        selectedShipment = Shipment.objects.get(id=request.session['shipmentID'])
    else:
        shipmentItem_list = None
        selectedShipment = None

    return render(request, '../templates/mainSection/fillshipment.html', {'selectedShipment':selectedShipment, 'productTypes': productType_list, 'shipments': shipment_list, 'productForm': productForm, 'shipmentDetails': shipmentItem_list, 'ShipmentForm': shipmentDetailForm})



#This function will accept a shipmentID and return a shipmentItemList
def getShipmentItemsList(shipmentId):
    
    if shipmentId is None:
        shipmentItem_list = None
    else:
        shipmentItem_list = ShipmentDetail.objects.filter(shipment=shipmentId,archived='0').select_related('product').select_related('product__types')
    return shipmentItem_list

    
#This method will handle the save product request
@login_required
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
            productObj = form.save(commit=False)
            
            # assigning the product Type
            productObj.types = productType

            # assigning the product image
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


#This method will handle the delete shipmentdetail request
@login_required
def deleteshipmentdetail(request,pk):
    objShipmentDetail= get_object_or_404(ShipmentDetail, pk=pk)    
    if request.method=='GET':
        # we are setting a parameter to mark the item as deleted.
        objShipmentDetail.archived = True
        objShipmentDetail.save()
        
    return redirect('mainSection:fillshipment')


#This method will handle the finalize shipment Request
@login_required
def finalizeshipment(request):
    if 'shipmentID' in request.session:
        objShipment = get_object_or_404(Shipment, pk=request.session['shipmentID'])

    if request.method=="POST":
        shipmentItem_list = getShipmentItemsList(objShipment.id)
        if shipmentItem_list.count() > 0:
         objShipment.isFinalized= True
         objShipment.save()
         #clearing the session form the system. so the New id will be facilitated
         request.session['shipmentID'] =None
         request.session.modified = True
        else:
            messages.error(request,'This Shipment has no products assigned. Please add products before finalize the shipment.')

    return redirect('mainSection:fillshipment')

