from django import forms
from django.shortcuts import render
from .models import *
from .forms import statusforms
from offers.models import OfferModel
from app.models import generalSetting
from app.forms import generalSettingForm
from offers.forms import OfferForm
from django.http import HttpResponse, JsonResponse
import sweetify
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.views import is_merchant_or_merchant_staff, is_owner
from django.contrib.auth.decorators import login_required, user_passes_test
from offers.views import merchant_offers
from users.models import *
from app.models import generalSetting
import datetime as dt
from customer_info.models import Customer_Info_Model
from referral_points.models import *
from merchant_software_apis.models import *
from pyfcm import FCMNotification
from django.conf import settings
import socket




@login_required(login_url="/login/")
@user_passes_test(is_owner)
def owner_offers(request):
    # owner_object = GreenBillUser.objects.get(id = request.user.id)
    logo = generalSetting.objects.get(id=1) 
    c_logo = logo.o_business_logo
    if request.method == "POST":
        offer_amount_cost = request.POST.get('customer_total_cost')
        form = OfferForm(request.POST, request.FILES)
        obj1 = ""
        obj2 = ""
        if request.POST['offer_id'] != "":
            offer_name = request.POST['offer_name']
            offer_caption = request.POST['offer_caption']
            valid_from = request.POST['valid_from']
            Offer_type = request.POST['user']
            valid_through = request.POST['valid_through']
            offer_business_category = request.POST['offer_business_category']
            customer_count = request.POST['customer_count']
            obj1 = OfferModel.objects.update_or_create(
                id=int(request.POST["offer_id"]), defaults={"Offer_type": Offer_type, "offer_name": offer_name, "offer_caption": offer_caption, "valid_from": valid_from, "valid_through": valid_through, "offer_business_category": offer_business_category,"customer_merchant_count":customer_count})
        else:
            if request.POST['user'] == "Merchant":
                offer_name = request.POST['offer_name']
                add_merchant_name = request.POST['add_merchant_name']
                offer_caption = request.POST['offer_caption']
                # business_name = request.POST['business_name']
            
                Offer_type = request.POST['user']
                
                offer_image = request.FILES['offer_image']
                offer_logo = request.FILES['merchant_offer_logo']
                valid_from = request.POST['valid_from']
                valid_through = request.POST['valid_through']
                status = request.POST['status']
                offer_panel = request.POST['offer_panel']
                o_business_name = request.POST['add_merchant_name']
                customer_count = request.POST['customer_count']

                business_category_value = request.POST['business_category_value']
                business_category_value_new = business_category_value.split(",")

                merchant_state_value = request.POST['merchant_state_value']
                merchant_state_value_new = merchant_state_value.split(",")
                
                merchant_city_value = request.POST['merchant_city_value']

                if merchant_city_value:
                    merchant_city_value_new = merchant_city_value.split(",")
                else:
                    merchant_city_value_new = ''

                merchant_area_value = request.POST['merchant_area_value']

                if merchant_area_value:
                    merchant_area_value_new = merchant_area_value.split(",")
                else:
                    merchant_area_value_new = ''

                obj2 = OfferModel.objects.create(
                    offer_amount = offer_amount_cost,offer_logo = offer_logo, add_merchant_name_by_owner = add_merchant_name, merchant_state=merchant_state_value_new, merchant_city=merchant_city_value_new, merchant_area=merchant_area_value_new,
                    o_business_name=o_business_name, offer_panel=offer_panel, offer_name=offer_name,
                    offer_caption=offer_caption, valid_from=valid_from, valid_through=valid_through, offer_image=offer_image,
                    Offer_type=Offer_type, offer_business_category=business_category_value_new,customer_merchant_count=customer_count)

            if request.POST['user'] == "Customer":
                offer_name = request.POST['offer_name']
                add_merchant_name = request.POST['add_merchant_name']
                offer_caption = request.POST['offer_caption']
                offer_logo = request.FILES['merchant_offer_logo']
                add_merchant_name = request.POST['add_merchant_name']
            
                Offer_type = request.POST['user']
                # offer_business_category = request.POST['offer_business_category']
                offer_image = request.FILES['offer_image']
                # offer_logo = request.FILES['offer_logo']
                valid_from = request.POST['valid_from']
                valid_through = request.POST['valid_through']
                status = request.POST['status']
                offer_panel = request.POST['offer_panel']
                o_business_name = request.POST['add_merchant_name']
                customer_count = request.POST['customer_count']
                
                customer_state_value = request.POST['customer_state_value']
                customer_state_value_new = customer_state_value.split(",")
    
                customer_city_value = request.POST['customer_city_value']
                if customer_city_value:
                    customer_city_value_new = customer_city_value.split(",")
                else:
                    customer_city_value_new = ''

                customer_area_value = request.POST['customer_area_value']
                if customer_area_value:
                    customer_area_value_new = customer_area_value.split(",")
                else:
                    customer_area_value_new = ''

                obj2 = OfferModel.objects.create(
                    offer_amount = offer_amount_cost, offer_logo = offer_logo, add_merchant_name_by_owner = add_merchant_name, customer_state = customer_state_value_new, customer_city = customer_city_value_new, 
                    customer_area = customer_area_value_new, o_business_name=o_business_name,
                    offer_panel=offer_panel, offer_name=offer_name, offer_caption=offer_caption, valid_from=valid_from,
                    valid_through=valid_through, offer_image=offer_image, Offer_type=Offer_type,customer_merchant_count=customer_count)

            if request.POST['user'] == "Partner":
                offer_name = request.POST['offer_name']
                add_merchant_name = request.POST['add_merchant_name']
                offer_caption = request.POST['offer_caption']
                add_merchant_name = request.POST['add_merchant_name']
                offer_logo = request.FILES['merchant_offer_logo']
                Offer_type = request.POST['user']
                offer_image = request.FILES['offer_image']
                valid_from = request.POST['valid_from']
                valid_through = request.POST['valid_through']
                status = request.POST['status']
                offer_panel = request.POST['offer_panel']
                o_business_name = request.POST['add_merchant_name']
                customer_count = request.POST['customer_count']
                
                partner_state_value = request.POST['partner_state_value']
                partner_state_value_new = partner_state_value.split(",")
    
                partner_city_value = request.POST['partner_city_value']
                if partner_city_value:
                    partner_city_value_new = partner_city_value.split(",")
                else:
                    partner_city_value_new = ''

                partner_area_value = request.POST['partner_area_value']
                
                if partner_area_value:
                    partner_area_value_new = partner_area_value.split(",")
                else:
                    partner_area_value_new = ''

                obj2 = OfferModel.objects.create(
                    offer_amount = offer_amount_cost, offer_logo = offer_logo, add_merchant_name_by_owner = add_merchant_name, partner_state = partner_state_value_new, partner_city = partner_city_value_new, 
                    partner_area = partner_area_value_new, o_business_name=o_business_name,
                    offer_panel=offer_panel, offer_name=offer_name, offer_caption=offer_caption, valid_from=valid_from,
                    valid_through=valid_through, offer_image=offer_image, Offer_type=Offer_type,customer_merchant_count=customer_count)

        if obj1:
            sweetify.success(request, title="Success", icon='success',
                             text='Offers updated Successfully.', timer=1500)

        elif obj2:
            sweetify.success(request, title="Success", icon='success',
                             text='Offers created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...",
                             icon='error', text='Fail to create.', timer=1000)

    data = OfferModel.objects.all().order_by("-id")
    if PromotionsAmount.objects.all():
        data1 = PromotionsAmount.objects.latest('id')
        offer_amount = data1.offer_amount
    else:
        offer_amount = 0

    today = dt.date.today()
    for offer in data:

        if offer.customer_merchant_count:
                offer.total_amount = float(offer_amount) * float(offer.customer_merchant_count)

        if offer.valid_through < today:
            offer.expire_status=True
        else:
            offer.expire_status = False
        if offer.Offer_type == 'Customer':
            try:
                cust_state = offer.customer_state
                if cust_state != '':
                    temp_state = ""
                    temp_state = cust_state.replace("[", "")
                    temp_state = temp_state.replace("]", "")
                    temp_state = temp_state.replace("'", "")
                    cust_state = temp_state
                    new_customer_state = cust_state.split(",")

                cust_city = offer.customer_city
                if cust_city != '':
                    temp_city = ""
                    temp_city = cust_city.replace("[", "")
                    temp_city = temp_city.replace("]", "")
                    temp_city = temp_city.replace("'", "")
                    cust_city = temp_city
                    new_customer_city = cust_city.split(",")

                cust_area = offer.customer_area
                if cust_area != '':
                    temp_area = ""
                    temp_area = cust_area.replace("[", "")
                    temp_area = temp_area.replace("]", "")
                    temp_area = temp_area.replace("'", "")
                    cust_area = temp_area
                    new_customer_area = cust_area.split(",")

                offer.total_customers = GreenBillUser.objects.filter(c_state__in=new_customer_state, c_city__in = new_customer_city, c_area__in = new_customer_area).count()
 
            except:
                offer.total_customers = 0
            
        else:
            try:
                mer_state = offer.merchant_state
                if mer_state != '':
                    temp_mer_state = ""
                    temp_mer_state = mer_state.replace("[", "")
                    temp_mer_state = temp_mer_state.replace("]", "")
                    temp_mer_state = temp_mer_state.replace("'", "")
                    mer_state = temp_mer_state
                new_merchant_state = mer_state.split(",")

                mer_city = offer.merchant_city
                if mer_city != '':
                    temp_mer_city = ""
                    temp_mer_city = mer_city.replace("[", "")
                    temp_mer_city = temp_mer_city.replace("]", "")
                    temp_mer_city = temp_mer_city.replace("'", "")
                    mer_city = temp_mer_city
                new_merchant_city = mer_city.split(",")

                mer_area = offer.merchant_area
                if mer_area != '':
                    temp_mer_area = ""
                    temp_mer_area = mer_area.replace("[", "")
                    temp_mer_area = temp_mer_area.replace("]", "")
                    temp_mer_area = temp_mer_area.replace("'", "")
                    mer_area = temp_mer_area
                new_merchant_area = mer_area.split(",")
                offer.total_merchants = MerchantProfile.objects.filter(m_state__in=new_merchant_state, m_city__in=new_merchant_city, m_area__in=new_merchant_area).count()
            except:
                offer.total_merchants = 0
            
           
    record = OfferModel.objects.filter(offer_panel = "owner")

    counter = 0
    for owner in record:
        if owner.valid_through >= today:
            counter = (counter) + 1
            owner.expire_status=True

    owner_business_name = generalSetting.objects.all().order_by("-id")
    states = GreenBillUser.objects.values('c_state').distinct()

    mer_states = MerchantProfile.objects.values('m_state').distinct()

    merchantList1 = MerchantProfile.objects.values('m_state').distinct()
    merchantList2 = MerchantProfile.objects.values('m_district').distinct()
    merchantList3 = MerchantProfile.objects.values('m_city').distinct()
    merchantList4 = MerchantProfile.objects.values('m_area').distinct()

    total_count = OfferModel.objects.filter(offer_panel='owner').count()
    partner_records = PartnerProfile.objects.values('p_state').distinct()
            
    form = generalSettingForm()

    data1 = OfferModel.objects.filter(offer_panel='owner').order_by("-id")
    total_active = OfferModel.objects.filter(offer_panel='owner', status=1).count()
    total_expired = OfferModel.objects.filter(offer_panel='owner', status=0).count()

    context = {
        'total_count': total_count,
        'partner_records': partner_records,
        'data': data,
        'data1':data1,
        'object': object,
        'total_active': total_active,
        'total_expired': total_expired,
        "cust_data": states,
        'merchant_state': mer_states,
        'merchantList1' : merchantList1,
        'merchantList2' : merchantList2,
        'merchantList3' : merchantList3,
        'merchantList4' : merchantList4,
        'owner_business_name': owner_business_name,
        'form': form,
        'PromotionNavclass': "active", 
        'PromotionCollapseShow': "show",
        'CreateOffersNavclass': "active",
        'total_offers' : counter,
        'count':0,
    }
    return render(request, "owner_offerstatus/owner-create-offer.html", context)

def get_city_by_state_ids_in_owner_offers(request):

    customer_state_value = request.POST['customer_state_value']

    customer_state_value_new = customer_state_value.split(",")

    list1 = []

    filtered_city_list = []

    for cust_state in customer_state_value_new:

        cus_state_id = GreenBillUser.objects.filter(c_state = cust_state)

        for city in cus_state_id:
            list1.append({
                "c_city": city.c_city
            })
        
    for x in list1:
        if x['c_city'] not in filtered_city_list:
            if x['c_city'] != '':
                filtered_city_list.append(x['c_city'])

    return JsonResponse({"data":filtered_city_list})


def get_area_by_city_names_in_owner_offers(request):

    customer_city_value = request.POST['customer_city_value']

    customer_city_value_new = customer_city_value.split(",")

    list1 = []

    filtered_area_list = []

    for area in customer_city_value_new:

        cust_id = GreenBillUser.objects.filter(c_city=area)

        for area in cust_id:
            list1.append({
                "c_area": area.c_area
            })
        
    for x in list1:
        if x['c_area'] not in filtered_area_list:
            filtered_area_list.append(x['c_area'])

    return JsonResponse({"data":filtered_area_list})

def Owner_offers(request):
    data_status = OfferModel.objects.all().order_by('-id')
    data_status1 = OfferModel.objects.filter(offer_panel = "merchant").order_by('-id')
    total_offers = OfferModel.objects.filter(offer_panel='merchant').count()
    
    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        offer_amount = data.offer_amount
    else:
        offer_amount = 0
    waiting_offers = OfferModel.objects.filter(offer_panel='merchant', status=0).count()
    approve_offers = OfferModel.objects.filter(offer_panel='merchant', status=1).count()
    disaproved_offers=OfferModel.objects.filter(offer_panel='merchant',status=2).count()
    
    today = dt.date.today()
    for offer in data_status:
        if offer.valid_through < today:

            offer.expire_status=True
        else:
            offer.expire_status=False

        if offer.customer_merchant_count:
                offer.total_amount = float(offer_amount) * float(offer.customer_merchant_count)
            

    context = {
    "data_status" : data_status,
    "data_status1": data_status1,
    'total_offers': total_offers,
    'waiting_offers': waiting_offers,
    'approve_offers': approve_offers,
    # 'form': form,
    'PromotionNavclass': "active", 
    'PromotionCollapseShow': "show",
    'OfferstatusNavclass': "active",
    'disaproved_offers': disaproved_offers,
    }
    return render(request, "owner_offerstatus/status.html", context)

import ast

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def ApproveOwnerOfferById(request, id):
    if request.method == "POST":

        offer_details = OfferModel.objects.get(id = id)
        merchant_name = offer_details.merchant_business_id.m_business_name



@login_required(login_url="/login/")
@user_passes_test(is_owner)
def approve_offer_by_id(request, id):
    if request.method == "POST":

        offer_details = OfferModel.objects.get(id = id)
        

        try:

            merchant_name = offer_details.merchant_business_id.m_business_name

            device = DeviceId.objects.filter(mobile_no=offer_details.merchant_user, user_type = 'merchant').first()

            if device:

                push_service = FCMNotification(api_key=settings.API_KEY)

                result = ''

                if device:
                    registration_id = device.device_id
                else:
                    registration_id = ""

                message_title = "Approved Offers"

                message_body = "Offer " + str(offer_details.offer_name) + " is approved. Pay now to publish it."

                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        except:
            merchant_name = offer_details.add_merchant_name_by_owner

                

        if offer_details.Offer_type == 'Merchant':

            if offer_details.merchant_state and not offer_details.merchant_city and not offer_details.merchant_area:

                users = MerchantProfile.objects.filter(m_state__in=ast.literal_eval(offer_details.merchant_state))

                for i in users:

                    if i.m_business_category:

                        if str(i.m_business_category.id) in ast.literal_eval(offer_details.offer_business_category):

                            device = DeviceId.objects.filter(mobile_no=i.m_user, user_type = 'merchant').first()

                            if device:

                                push_service = FCMNotification(api_key=settings.API_KEY)

                                result = ''

                                if device:
                                    registration_id = device.device_id
                                else:
                                    registration_id = ""

                                message_title = "New Offer uploaded by Merchant"

                                message_body = "Hurray, checkout exciting offers by " + str(merchant_name)

                                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

            elif offer_details.merchant_state and offer_details.merchant_city and not offer_details.merchant_area:

                users = MerchantProfile.objects.filter(m_state__in=ast.literal_eval(offer_details.merchant_state))

                for i in users:

                    if i.m_business_category:

                        if str(i.m_business_category.id) in ast.literal_eval(offer_details.offer_business_category):

                            if i.m_city:

                                if i.m_city in ast.literal_eval(offer_details.merchant_city):

                                    device = DeviceId.objects.filter(mobile_no=i.m_user, user_type = 'merchant').first()

                                    if device:

                                        push_service = FCMNotification(api_key=settings.API_KEY)

                                        result = ''

                                        if device:
                                            registration_id = device.device_id
                                        else:
                                            registration_id = ""

                                        message_title = "New Offer uploaded by Merchant"

                                        message_body = "Hurray, checkout exciting offers by " + str(merchant_name)

                                        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

            elif offer_details.merchant_state and offer_details.merchant_city and offer_details.merchant_area:

                users = MerchantProfile.objects.filter(m_state__in=ast.literal_eval(offer_details.merchant_state))

                for i in users:

                    if i.m_business_category:

                        if str(i.m_business_category.id) in ast.literal_eval(offer_details.offer_business_category):

                            if i.m_city:

                                if i.m_city in ast.literal_eval(offer_details.merchant_city):

                                    if i.m_area:

                                        if i.m_area in ast.literal_eval(offer_details.merchant_area):

                                            device = DeviceId.objects.filter(mobile_no=i.m_user, user_type = 'merchant').first()

                                            if device:

                                                push_service = FCMNotification(api_key=settings.API_KEY)

                                                result = ''

                                                if device:
                                                    registration_id = device.device_id
                                                else:
                                                    registration_id = ""

                                                message_title = "New Offer uploaded by Merchant"

                                                message_body = "Hurray, checkout exciting offers by " + str(merchant_name)

                                                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        elif offer_details.Offer_type == 'Customer':

            if offer_details.customer_state and not offer_details.customer_city and not offer_details.customer_area: 
                
                users = GreenBillUser.objects.filter(c_state__in=ast.literal_eval(offer_details.customer_state))

                for mobile_no in users:
                    device = DeviceId.objects.filter(mobile_no=mobile_no, user_type = 'customer').first()
                   
                    if device:
                        push_service = FCMNotification(api_key=settings.API_KEY)
                        result = ''

                        if device:
                            registration_id = device.device_id
                        else:
                            registration_id = ""

                        message_title = "New Offer uploaded by Merchant"

                        message_body = "Hurray, checkout exciting offers by " + str(merchant_name)

                        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

            elif offer_details.customer_state and offer_details.customer_city and not offer_details.customer_area:

                users = GreenBillUser.objects.filter(c_state__in=ast.literal_eval(offer_details.customer_state))

                for i in users:

                    if i.c_city:

                        if i.c_city in ast.literal_eval(offer_details.customer_city):

                            device = DeviceId.objects.filter(mobile_no=i, user_type = 'customer').first()
                    
                            if device:
                                push_service = FCMNotification(api_key=settings.API_KEY)
                                result = ''

                                if device:
                                    registration_id = device.device_id
                                else:
                                    registration_id = ""

                                message_title = "New Offer uploaded by Merchant"

                                message_body = "Hurray, checkout exciting offers by "  + str(merchant_name)

                                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

            elif offer_details.customer_state and offer_details.customer_city and offer_details.customer_area:
                
                users = GreenBillUser.objects.filter(c_state__in=ast.literal_eval(offer_details.customer_state))

                for i in users:

                    if i.c_city:

                        if i.c_city in ast.literal_eval(offer_details.customer_city):

                            if i.c_area in ast.literal_eval(offer_details.customer_area):

                                device = DeviceId.objects.filter(mobile_no=i, user_type = 'customer').first()
                        
                                if device:
                                    push_service = FCMNotification(api_key=settings.API_KEY)
                                    result = ''

                                    if device:
                                        registration_id = device.device_id
                                    else:
                                        registration_id = ""

                                    message_title = "New Offer uploaded by Merchant"

                                    message_body = "Hurray, checkout exciting offers by "  + str(merchant_name)

                                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        
        data_status = OfferModel.objects.filter(id = id).update(status = "1")
        sweetify.success(request, title="success", icon='success', text='Offer Approved Successfully !!!', timer=1500)
        return redirect(merchant_offers)
    else:
        sweetify.error(request, title="error", icon='error', text='Failed to Approved offer!!!', timer=1500)
        return redirect(merchant_offers)



@login_required(login_url="/login/")
@user_passes_test(is_owner)
def disapprove_offer_by_id(request):
    if request.method == "POST":
        id = request.POST["disapprove_offer_id"]
        reason = request.POST["reason"] 

        offer_details = OfferModel.objects.get(id = id)

        try:

            device = DeviceId.objects.filter(mobile_no=offer_details.merchant_user, user_type = 'merchant').first()

            if device:

                push_service = FCMNotification(api_key=settings.API_KEY)

                result = ''

                if device:
                    registration_id = device.device_id
                else:
                    registration_id = ""

                message_title = "Rejected Offer"

                message_body = "Offer " + str(offer_details.offer_name) + " is Rejected. Check Reason."

                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        except:
            pass

        data_status = OfferModel.objects.filter(id = id).update(status = "2", disapproved_reason = reason)
        sweetify.success(request, title="success", icon='success', text='Offers Disapproved Successfully !!!', timer=1500)
        return redirect(merchant_offers)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Disapproved Offers!!!', timer=1500)
        return redirect(merchant_offers)


def Delete_owner_Offer(request, id):
    offer_obj = OfferModel.objects.get(id=id).delete()
    if offer_obj:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": False})


@login_required(login_url="/login/")
@user_passes_test(is_owner)
def add_offer_Amount_by_id(request):
    if request.method == "POST":
        id = request.POST["offer_amount_id"]
        offer_amount = request.POST["offer_amount"] 
        data_status = OfferModel.objects.filter(id = id).update(offer_amount = offer_amount)
        sweetify.success(request, title="success", icon='success', text='Amount Added Successfully !!!', timer=1500)
        return redirect(merchant_offers)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Add Amount!!!', timer=1500)
        return redirect(merchant_offers)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def add_offer_Amount_for_merchant(request):
    if request.method == "POST":
        id = request.POST["offer_amount_id"]
        offer_amount = request.POST["offer_amount"] 
        data_status = OfferModel.objects.filter(id = id).update(offer_amount = offer_amount)
        sweetify.success(request, title="success", icon='success', text='Amount Added Successfully !!!', timer=1500)
        return redirect(merchant_offers)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Add Amount!!!', timer=1500)
        return redirect(merchant_offers)


