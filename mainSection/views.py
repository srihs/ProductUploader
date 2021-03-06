from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db import transaction
from django.http import JsonResponse
from django.template.loader import render_to_string
from decimal import *
from django.utils import timezone
from .decorators import office_required
from .forms import CreateShipmentForm, CreateProductForm, CreateShipmentDetails, CreateCostFactorForm, sellingPriceForm, GRNForm, CustomerForm
from .models import Shipment, ProductTypes, ShipmentDetail, Country, Products, ProductSize, ProductColour, ProducBrands, Customer, CustomerType

# global variables
shipment_list = None
shipmentItem_list = None
shipmentTotal = None
shipmentTotalQty = None
selectedShipment = None


########

# global Methods
# This function will accept a shipmentID and return a shipmentItemList


def getShipmentItemsList(shipmentId):
    if shipmentId is None:
        shipmentItem_list = None
    else:
        shipmentItem_list = ShipmentDetail.objects.filter(
            shipment=shipmentId, archived='0').select_related('product').select_related(
            'product__types')
    return shipmentItem_list


@login_required
def home(request):
    order_count = Shipment.objects.filter(buyer=request.user).count()
    products_count = ShipmentDetail.objects.filter(shipment__buyer= request.user).count()
    order_list = ShipmentDetail.objects.filter(shipment__buyer= request.user)#.annotate(total= Sum(F('indPrice') * F('qty')))['total'] or 0
    total_value =0
    for orderitem in order_list:
        total_value += (orderitem.indPrice * orderitem.qty)
    # no_bills = ShipmentDetail.objects.values('billNumber').distinct().count()
    no_bills = ShipmentDetail.objects.filter(shipment__buyer= request.user).values('billNumber').distinct().count()
    return render(request, '../templates/mainSection/home.html', {'order_count': order_count, 'products_count': products_count, 'total_value': total_value, 'no_bills': no_bills})


# This method will handle the create shipment request
@login_required
def createshipment(request):
    if request.method == "GET":

        # clearing the session form the system. so the New id will be facilitated
        request.session['shipmentID'] = None
        request.session.modified = True
        shipmentPointList = Country.objects.all()

        # shipmentNumber is defined by 'SHN-000' + next Id in the shipment Table
        try:
            nextId = Shipment.objects.all().count()   # trying to retrive the next primaryKey
            nextId += 1
        except:
            nextId = 1   # if the next ID is null define the record as the first
        form = CreateShipmentForm(
            initial={'shipmentNumber': 'SHN-000' + str(nextId)})  # creating the form with the shipment ID
    return render(request, '../templates/mainSection/createshipment.html', {'form': form, 'user': request.user, 'shipmentPointList': shipmentPointList})


# This method will handle the Save shipment request
@login_required
def saveshipment(request):
    if request.method == 'POST':
        form = CreateShipmentForm(request.POST)
        if form.is_valid():
            objShipment = form.save(commit=False)
            objCountry = get_object_or_404(Country, pk=request.POST.get('shipmentPointDropDown'))

            objShipment.shippingPoint = objCountry
            objShipment.buyer = request.user
            objShipment.userCreated = request.user
            objShipment.save()
        else:
            messages.error(request, form.errors)
        return redirect('mainSection:fillshipment')


@login_required
def viewshipment(request):
    # Retrieving The shipments which are open to fill.
    if request.user.is_officeUser or request.user.is_storeUser:
        shipment_list = Shipment.objects.all()
    else:
        shipment_list = Shipment.objects.filter(buyer=request.user)

    shipmentItem_list = None

    if request.method == 'GET':
        return render(request, '../templates/mainSection/viewshipment.html', {'shipments': shipment_list})

    if request.method == 'POST':
        # if the request if for a shipment that is selected in the dropdown the the following code block will execute
        if request.POST['shipmentDropDown']:

            # getting the shipmentID
            shipmentID = request.POST.get('shipmentDropDown')
            selectedShipment = Shipment.objects.select_related('shippingPoint').\
                select_related('buyer').get(id=shipmentID)  # Saving the selected Shipment object to passback to the template

            # getting the shipment List
            shipmentItem_list = getShipmentItemsList(shipmentID)
            shipmentTotal = 0
            shipmentTotalQty = 0
            shippingWeight = 0
            for shipment in shipmentItem_list:
                shipmentTotal += shipment.totalAmount
                shipmentTotalQty += shipment.qty
                shippingWeight += shipment.weight * shipment.qty

            shippingWeightKG = shippingWeight/1000

        else:
            messages.error(request, "Something went wrong.")

        return render(request, '../templates/mainSection/viewshipment.html',
                      {'shipments': shipment_list, 'shipmentDetails': shipmentItem_list, 'shipmentTotal': shipmentTotal,
                       'shipmentTotalQty': shipmentTotalQty, 'selectedShipment': selectedShipment,'shippingWeightKG':shippingWeightKG})


@login_required
@office_required
def reviewShipment(request):
    shipmentTotal = 0
    shipmentTotalQty = 0
    selectedShipment = 0
    shippingWeight = 0
    shippingWeightKG = 0

    shipment_list = Shipment.objects.filter(isCostapplied='False', isFinalized='1', isCostbaseFinalized='1')

    if request.method == 'GET':
        # if the request if for a shipment that is selected in the dropdown the the following code block will execute
        if request.GET.get('shipmentDropDown'):
            # clearing the session form the system. so the New id will be facilitated
            request.session['shipmentID'] = None
            request.session.modified = True
            shipmentID = request.GET.get('shipmentDropDown')  # getting the shipmentID
            shipmentItem_list = getShipmentItemsList(shipmentID)  # getting the shipment List
            selectedShipment = get_object_or_404(Shipment,
                                                 pk=shipmentID)  # Saving the selected Shipment object to passback to the template
            request.session['shipmentID'] = selectedShipment.id  # stroing the shipment Id for the save operation

        # since the session.flush is voided due to the the authentication issue, ShipmentID is set to null in the
        # session variable therefor need to check for null.
        elif request.method == 'GET' and request is not None and 'shipmentID' in request.session and request.session[
            'shipmentID'] is not None:
            print('here')

            shipmentItem_list = getShipmentItemsList(request.session['shipmentID'])
            selectedShipment = Shipment.objects.get(
                id=request.session['shipmentID'])



        else:
            shipmentItem_list = None
            selectedShipment = None

        if(shipmentItem_list is not None):
         for shipment in shipmentItem_list:
            shipmentTotal += shipment.totalAmount
            shipmentTotalQty += shipment.qty
            shippingWeight += shipment.weight * shipment.qty

        shippingWeightKG = shippingWeight / 1000
        print(shipmentTotal)
        print(shipmentTotalQty)
        print(shippingWeight)

        return render(request, '../templates/mainSection/reviewshipment.html',
                      {'shipments': shipment_list, 'shipmentDetails': shipmentItem_list, 'shipmentTotal': shipmentTotal,
                       'shipmentTotalQty': shipmentTotalQty, 'selectedShipment': selectedShipment,
                       'shippingWeightKG': shippingWeightKG})

    if request.method == 'POST':
        # if the request if for a shipment that is selected in the dropdown the the following code block will execute
        if request.POST.get('shipmentDropDown'):
            # getting the shipmentID and store it in sthe seesion
            shipmentID = request.POST.get('shipmentDropDown')
            request.session['shipmentID'] = shipmentID
            # Saving the selected Shipment object to passback to the template
            selectedShipment = Shipment.objects.get(pk=shipmentID)
            shipmentItem_list = getShipmentItemsList(shipmentID)

            shipmentTotal = 0
            shipmentTotalQty = 0
            shippingWeight = 0

            for shipment in shipmentItem_list:
                shipmentTotal += shipment.totalAmount
                shipmentTotalQty += shipment.qty
                shippingWeight += shipment.weight * shipment.qty

            shippingWeightKG = shippingWeight / 1000

    elif request.method == 'POST' and request is not None and 'shipmentID' in request.session and request.session['shipmentID'] is not None:
        shipmentItem_list = getShipmentItemsList(request.session['shipmentID'])
        selectedShipment = Shipment.objects.get(id=request.session['shipmentID'])
    else:
        shipmentItem_list = None
        selectedShipment = None

    return render(request, '../templates/mainSection/reviewshipment.html',
                  {'shipments': shipment_list, 'shipmentDetails': shipmentItem_list, 'shipmentTotal': shipmentTotal,
                   'shipmentTotalQty': shipmentTotalQty, 'selectedShipment': selectedShipment ,'shippingWeightKG':shippingWeightKG})


# This method will handle the fillshipment request
@login_required
def fillshipment(request):
    productCode = request.user.productCode
    nextId =None

    # shipmentNumber is defined by 'NuyerCode-000' + next Id in the shipment Table
    try:
        nextId = ShipmentDetail.objects.filter(shipment__buyer= request.user).count() # trying to retrive the next primaryKey
        nextId += 1
    except:
        nextId = 1     # if the next ID is null define the record as the first

    # initializing objects
    shipmentDetailForm = CreateShipmentDetails()
    productForm = CreateProductForm(
        initial={'sku': productCode + '-000' + str(nextId)})  # creating the form with the product ID

    productType_list = ProductTypes.objects.all()     # Retrieving The Product types for the ShipmentForm
    productsize_list = ProductSize.objects.all()  # Retreving all prouct Sizes
    productColor_list = ProductColour.objects.all()  # Retreving all prouct Sizes
    productBrand_list = ProducBrands.objects.all()  # Retreving all prouct Brands

    shipment_list = Shipment.objects.filter(
        isClosed='False', isFinalized='0', buyer=request.user)     # Retrieving The shipments which are open to fill. Only loged in users orders will be listed.

    # if the request if for a shipment that is selected in the dropdown the the following code block will execute
    if request.GET.get('shipmentDropDown'):
        shipmentID = request.GET.get('shipmentDropDown')   # getting the shipmentID
        shipmentItem_list = getShipmentItemsList(shipmentID)  # getting the shipment List
        selectedShipment = get_object_or_404(Shipment, pk=shipmentID)         # Saving the selected Shipment object to passback to the template
        request.session['shipmentID'] = selectedShipment.id         # stroing the shipment Id for the save operation

    # since the session.flush is voided due to the the authentication issue, ShipmentID is set to null in the
    # session variable therefor need to check for null.
    elif request.method == 'GET' and request is not None and 'shipmentID' in request.session and request.session['shipmentID'] is not None:
        shipmentItem_list = getShipmentItemsList(request.session['shipmentID'])
        selectedShipment = Shipment.objects.get(
            id=request.session['shipmentID'])
    else:

        shipmentItem_list = None
        selectedShipment = None

    return render(request, '../templates/mainSection/fillshipment.html',
                  {'selectedShipment': selectedShipment, 'productBrands': productBrand_list,  'productColours': productColor_list, 'productTypes': productType_list, 'productSizes': productsize_list, 'shipments': shipment_list,
                   'productForm': productForm, 'shipmentDetails': shipmentItem_list,
                   'ShipmentForm': shipmentDetailForm})


# This method will handle the save product request
@login_required
@transaction.atomic
def saveproduct(request):
    if request.method == 'POST':

        form = CreateProductForm(request.POST, request.FILES)
        shipmentDetialForm = CreateShipmentDetails(request.POST)

        productType = get_object_or_404(
            ProductTypes, pk=request.POST['productType'])  # loading the product type that was assigned to the product

        productSize = get_object_or_404(
            ProductSize, pk=request.POST['productSize'])

        productColour = get_object_or_404(
            ProductColour, pk=request.POST['productColour'])

        productBrand = get_object_or_404(
            ProducBrands, pk=request.POST['productBrand'])

        shipmentID = request.session['shipmentID']   # loading the ShipmentID

        try:
            if form.is_valid() and shipmentDetialForm.is_valid():
                productObj = form.save(commit=False)
                productObj.types = productType # assigning the product Type
                productObj.productImg = request.FILES['img']  # assigning the product image.
                productObj.size = productSize
                productObj.colour = productColour
                productObj.brand = productBrand
                productObj.userCreated = request.user
                productObj.save()

                # creating the shipment detail Object
                shipmentDetailObj = shipmentDetialForm.save(commit=False)
                shipmentDetailObj.product = productObj
                shipmentDetailObj.weight = productObj.weight
                shipmentDetailObj.shipment = Shipment.objects.get(id=shipmentID)
                shipmentDetailObj.userCreated = request.user
                shipmentDetailObj.save()

            else:
                messages.error(request, form.errors)
        except Exception as e:
            raise e

    return redirect('mainSection:fillshipment')


# This method will handle the delete shipmentdetail request
@login_required
def deleteshipmentdetail(request, pk):
    objShipmentDetail = get_object_or_404(ShipmentDetail, pk=pk)
    if request.method == 'GET':
        objShipmentDetail.archived = True  # we are setting a parameter to mark the item as deleted.
        objShipmentDetail.userModified = str(request.user.username)

        objShipmentDetail.save()
    return redirect('mainSection:fillshipment')


# This method will handle the finalize shipment Request
@login_required
def finalizeshipment(request):
    if 'shipmentID' in request.session:
        objShipment = get_object_or_404(
            Shipment, pk=request.session['shipmentID'])

    if request.method == "POST":
        shipmentItem_list = getShipmentItemsList(objShipment.id)
        if shipmentItem_list.count() > 0:
            objShipment.isFinalized = True
            objShipment.userModified = str(request.user.username)
            objShipment.save()
            # clearing the session form the system. so the New id will be facilitated
            request.session['shipmentID'] = None
            request.session.modified = True
        else:
            messages.error(
                request, 'This Shipment has no products assigned. Please add products before finalize the shipment.')

    return redirect('mainSection:fillshipment')


@login_required
@transaction.atomic
def generateCostFactor(request):

    shipment_list = None
    shipment_list = Shipment.objects.filter(isClosed='0', isFinalized='1', isCostbaseFinalized='False')
    form = CreateCostFactorForm()
    if request.method == 'GET':
        return render(request, '../templates/mainSection/costfactor.html', {'form': form, 'shipments': shipment_list})

    if request.method == 'POST':
            # if the request if for a shipment that is selected in the dropdown the the following code block will execute
            if request.POST.get('shipmentDropDown'):
                # getting the shipmentID
                shipmentID = request.POST.get('shipmentDropDown')
                request.session['shipmentID'] = shipmentID
                selectedShipment = Shipment.objects.get(pk=shipmentID) # Saving the selected Shipment object to passback to the template
                shipmentItem_list = getShipmentItemsList(shipmentID)
                shipmentTotal = 0
                shipmentTotalQty = 0
                shippingWeight=0

                for shipment in shipmentItem_list:
                    shipmentTotal += shipment.totalAmount
                    shipmentTotalQty += shipment.qty
                    shippingWeight += shipment.weight * shipment.qty

                shippingWeightKG = shippingWeight / 1000

            else:
                form = CreateCostFactorForm(request.POST, request.FILES)
                if form.is_valid():
                    shipmnetID = request.session['shipmentID']
                    objShipment = get_object_or_404(Shipment, pk=request.session['shipmentID'])
                    objShipment.isCostbaseFinalized = True
                    objShipment.costBase = form.cleaned_data['costBase']
                    # assigning the cost file
                    objShipment.costFile = form.cleaned_data['costFile']
                    objShipment.userModified = str(request.user.username)

                    shipmentItem_list = getShipmentItemsList(shipmnetID)

                    for shipmentItem in shipmentItem_list:
                        shipmentItem.costBase = objShipment.costBase
                        shipmentItem.userModified = str(request.user.username)

                        shipmentItem.save()

                    objShipment.save()
                    form = CreateCostFactorForm()  # Added this to clear the previous values for fields
                    messages.success(request, "Cost base updated for the Shipment. Please verify the Shipment.")
                    # clearing the session form the system. so the New id will be facilitated
                    request.session['shipmentID'] = None
                    request.session.modified = True
                    return render(request, '../templates/mainSection/costfactor.html',
                                  {'form': form, 'shipments': shipment_list})



                else:
                        messages.error(request, "Something went wrong.")

                # clearing the session form the system. so the New id will be facilitated

    return render(request, '../templates/mainSection/costfactor.html',
                  {'form': form, 'shipments': shipment_list,'shipmentTotal': shipmentTotal,
                   'shipmentTotalQty': shipmentTotalQty, 'selectedShipment': selectedShipment,'shippingWeightKG':shippingWeightKG})


@transaction.atomic
@login_required
@office_required
def updateproduct(request, pk):
    data = dict()

    if request.method == 'POST':
        objShipmentDetail = ShipmentDetail.objects.get(pk=pk)

        if objShipmentDetail is not None:
            objShipmentDetail.sellingPrice = request.POST['sellingPrice']
            if Decimal(objShipmentDetail.cost) > Decimal(objShipmentDetail.sellingPrice):
                messages.error(request, "Cost for the item is  Rs." + str(round(objShipmentDetail.cost,2)) +" . You have entered a price less than the cost.")
            else:
                objShipmentDetail.is_checked = True
                objShipmentDetail.userModified = str(request.user.username)

                # productObj.productImage=file
                objShipmentDetail.save()
                objProject = Products.objects.get(pk=objShipmentDetail.product.id)
                objProject.sellingPrice = request.POST['sellingPrice']
                objProject.userModified = str(request.user.username)

                objProject.save()

    else:
        objShipmentDetail = ShipmentDetail.objects.get(pk=pk)
        form = sellingPriceForm(instance=objShipmentDetail)
        context = {'form': form}
        data['html_form'] = render_to_string('../templates/mainSection/partials/editproduct.html', context, request=request)
        return JsonResponse(data)

    return redirect('mainSection:reviewshipment')

@login_required
@office_required
def applyCost(request):
    if request.method == 'POST':
        shipmentItem_list = ShipmentDetail.objects.filter(shipment=request.session['shipmentID'], archived='0',is_checked='0')
        if shipmentItem_list.count() > 0 :
            messages.error(request, "There are " + str(shipmentItem_list.count()) + " item(s) that need to be review. Please make sure all the items are reviewed. ")
        else:
            objShipment = Shipment.objects.get(pk=request.session['shipmentID'])
            objShipment.isCostapplied = True
            objShipment.userModified = str(request.user.username)

            objShipment.save()
            # clearing the session form the system. so the New id will be facilitated
            request.session['shipmentID'] = None
            request.session.modified = True
            messages.success(request, "Shipment " + objShipment.shipmentNumber +  " Closed.")

    return redirect('mainSection:reviewshipment')


def viewproduct(request):
    objProduct = None
    objShipping_list = None
    # clearing the session form the system. so the New id will be facilitated
    request.session['shipmentID'] = None
    request.session.modified = True

    if request.method =='GET':
        return render(request, '../templates/mainSection/viewitem.html')

    if request.method == 'POST':
        sku = request.POST['SKU']

        try:
            objProduct = Products.objects.select_related('types').get(sku=sku)
            objShipping_list = ShipmentDetail.objects.filter(product__id=objProduct.id).select_related('shipment')

        except Products.DoesNotExist:
            messages.warning(request,"No records found.")

    return render(request, '../templates/mainSection/viewitem.html', {'Product': objProduct, 'objShipping_list': objShipping_list})

@login_required
def grnstore(request):
    shipmentTotal = 0
    shipmentTotalQty = 0
    selectedShipment = 0
    shippingWeight = 0
    shippingWeightKG = 0
    shipmentItem_list = None
    shipment_list = Shipment.objects.filter(isCostapplied='1', isFinalized='1', isCostbaseFinalized='1', isClosed='0')

    if request.method == 'GET':
        # since the session.flush is voided due to the the authentication issue, ShipmentID is set to null in the
        # session variable therefor need to check for null.
        if request.method == 'GET' and request is not None and 'shipmentID' in request.session and request.session['shipmentID'] is not None:
            shipmentItem_list = getShipmentItemsList(request.session['shipmentID'])
            selectedShipment = Shipment.objects.get(
            id=request.session['shipmentID'])

            for shipment in shipmentItem_list:
                shipmentTotal += shipment.totalAmount
                shipmentTotalQty += shipment.qty
                shippingWeight += shipment.weight * shipment.qty

            shippingWeightKG = shippingWeight / 1000

            for shipment in shipmentItem_list:
                shipmentTotal += shipment.totalAmount
                shipmentTotalQty += shipment.qty
                shippingWeight += shipment.weight * shipment.qty

            shippingWeightKG = shippingWeight / 1000

            return render(request, '../templates/mainSection/reviewgoodrecived.html',
                          {'shipments': shipment_list, 'shipmentDetails': shipmentItem_list,
                           'shipmentTotal': shipmentTotal,
                           'shipmentTotalQty': shipmentTotalQty, 'selectedShipment': selectedShipment,
                           'shippingWeightKG': shippingWeightKG})

    # if the request if for a shipment that is selected in the dropdown the the following code block will execute
    if request.POST.get('shipmentDropDown'):
        shipmentID = request.POST.get('shipmentDropDown')
        request.session['shipmentID'] = shipmentID
        # Saving the selected Shipment object to passback to the template
        selectedShipment = Shipment.objects.get(pk=shipmentID)
        shipmentItem_list = getShipmentItemsList(shipmentID)
        shipmentTotal = 0
        shipmentTotalQty = 0
        shippingWeight = 0

        for shipment in shipmentItem_list:
            shipmentTotal += shipment.totalAmount
            shipmentTotalQty += shipment.qty
            shippingWeight += shipment.weight * shipment.qty

        shippingWeightKG = shippingWeight / 1000

    return render(request, '../templates/mainSection/reviewgoodrecived.html',
              {'shipments': shipment_list, 'shipmentDetails': shipmentItem_list, 'shipmentTotal': shipmentTotal,
               'shipmentTotalQty': shipmentTotalQty, 'selectedShipment': selectedShipment,
               'shippingWeightKG': shippingWeightKG})

@login_required
def updateproductgrn(request, pk):
    data = dict()

    if request.method == 'POST':
        objShipmentDetail = ShipmentDetail.objects.get(pk=pk)
        if objShipmentDetail is not None:
            objShipmentDetail.receivedQty = request.POST['receivedQty']
            objShipmentDetail.is_grn = True
            objShipmentDetail.userUpdated = str(request.user.username)

            if int(objShipmentDetail.receivedQty) < int(objShipmentDetail.qty):
                objShipmentDetail.is_completeReceive = False
                messages.warning(request, "Item Received qty is less than the shipped Qty. "
                                          "If this is a mistake you can edit again and correct it.")

            if int(objShipmentDetail.receivedQty) > int(objShipmentDetail.qty):
                objShipmentDetail.is_completeReceive = False
                messages.warning(request,"Item Received qty is greater than the shipped Qty. ")
            else:
                objShipmentDetail.is_completeReceive = True
                objShipmentDetail.save()
    else:
        objShipmentDetail = ShipmentDetail.objects.get(pk=pk)
        form = GRNForm(instance=objShipmentDetail)
        context = {'form': form}
        data['html_form'] = render_to_string('../templates/mainSection/partials/grn.html', context,
                                             request=request)
        return JsonResponse(data)

    return redirect('mainSection:grnstore')


@login_required
def closeshipment(request):
    if request.method == 'POST':
        shipmentItem_list = ShipmentDetail.objects.filter(shipment=request.session['shipmentID'], archived='0',is_grn='0')
        if shipmentItem_list.count() > 0 :
            messages.error(request, "There are " + str(shipmentItem_list.count()) + " item(s) that need to be GRN. Please make sure all the items are reviewed.")
        else:
            objShipment = Shipment.objects.get(pk=request.session['shipmentID'])
            objShipment.isClosed = True
            objShipment.userModified = str(request.user.username)

            objShipment.save()
            # clearing the session form the system. so the New id will be facilitated
            request.session['shipmentID'] = None
            request.session.modified = True
            messages.success(request, "Shipment " + objShipment.shipmentNumber +  " Closed.")

    return redirect('mainSection:grnstore')


@login_required
def loadCustomer(request):
    customer_list = Customer.objects.filter(archived='0')
    customerTypes_list = CustomerType.objects.all()
    nextId =0

    if request.method == 'GET':
        # Setting Customer Number
        try:
            nextId = Customer.objects.all().count()  # trying to retrive the next primaryKey
            nextId += 1
        except:
            nextId = 1  # if the next ID is null define the record as the first

    form = CustomerForm(initial={'customerNumber': 'CUS-000' + str(nextId), 'creditPeriod' : '0'})
    return render(request, '../templates/mainSection/createcustomer.html', {'form': form, 'customers': customer_list, 'customerTypes': customerTypes_list})


@login_required
def savecustomers(request):
    if request.method == 'POST':
        cusType = get_object_or_404(CustomerType, pk=request.POST.get('ddcustomerType'))
        form = CustomerForm(request.POST)
        if form.is_valid():
            objCustomer = form.save(commit=False)
            print(objCustomer)
            objCustomer.userCreated = request.user
            objCustomer.customerType = cusType
            objCustomer.save()
        else:
            messages.error(request, form.errors)

    return redirect('mainSection:loadCustomer')
