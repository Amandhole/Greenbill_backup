from django.shortcuts import render
from .models import *
from .forms import CouponsForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import sweetify
from users.models import Merchant_users, GreenBillUser, MerchantProfile
from referral_points.models import *
from datetime import date, datetime
import ast
from merchant_software_apis.models import DeviceId
from pyfcm import FCMNotification
from django.conf import settings
import socket
# Create your views here.


def add_coupon_view(request):

    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = GreenBillUser.objects.get(id = merchant_users_object.merchant_user_id.id)

    merchant_business_object = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = 1) 
    
    m_logo = MerchantProfile.objects.get(m_user=merchant_object,m_active_account=1).m_business_logo
    
    if request.method == "POST":

        form = CouponsForm(request.POST, request.FILES)
        amount_in = ''
        if form.is_valid():
            coupon_cost = request.POST.get('customer_total_cost')
            coupon_type = request.POST['coupon_type']

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
                customer_area_value_new= ''

            customer_count = request.POST['customer_count']
            if coupon_type == "coupon_value":
                amount_in = request.POST['amount_in']
                if amount_in == "percentage":
                    coupon_val = request.POST['coupon_value_percent']
                    coupon_val_per = coupon_val 
                    status1 = ""
                    status2 = ""
                    
                    if request.POST["coupon_id"] != "":
                        
                        status2 = CouponModel.objects.update_or_create(id=int(request.POST["coupon_id"]),defaults={
                            "coupon_name":request.POST['coupon_name'],
                            "valid_from":request.POST['valid_from'],
                            "valid_through":request.POST['valid_through'],
                            "coupon_code":request.POST['coupon_code'],
                            "coupon_value":coupon_val_per,
                            "green_point":request.POST['green_point'],
                            "coupon_logo": m_logo,
                            "coupon_background_color":"",
                            # "coupon_background_color":request.POST['color'],
                            "coupon_valid_for_user":request.POST['coupon_valid_for_user'],
                            'merchant_business_id': merchant_business_object.id,
                            'customer_state': customer_state_value_new, 
                            'customer_city': customer_city_value_new, 
                            'customer_area': customer_area_value_new,
                            'amount_in':amount_in,
                            'coupon_amount':coupon_cost,
                            })
                        
                    else:
                        status1=CouponModel.objects.create(
                            merchant_id=merchant_object,
                            coupon_name=form.cleaned_data['coupon_name'],
                            valid_from=form.cleaned_data['valid_from'],
                            valid_through=form.cleaned_data['valid_through'],
                            coupon_code=form.cleaned_data['coupon_code'],
                            coupon_value=coupon_val_per+ "%",
                            green_point=form.cleaned_data['green_point'],
                            coupon_logo=m_logo,
                            # coupon_background_color =request.POST['color'],
                            coupon_background_color = "",
                            coupon_valid_for_user = request.POST['coupon_valid_for_user'],
                            merchant_business_id = merchant_business_object.id,
                            customer_state = customer_state_value_new, 
                            customer_city = customer_city_value_new, 
                            customer_area = customer_area_value_new,
                            total_customers = customer_count,
                            amount_in = amount_in,
                            coupon_amount=coupon_cost,
                        )

                    if status1:
                        sweetify.success(request, title="Success", icon='success',
                                         text='Coupon Created Successfully.', timer=1500)
                        
                    elif status2:
                        sweetify.success(request, title="Success", icon='success',
                                         text='Coupon updated Successfully.', timer=1500)
                    else:
                        sweetify.success(request, title="Oops...",
                                 icon='error', text='Fail to create.', timer=1000)

                else:
                    coupon_val = request.POST['coupon_value_fixamount']
                    if request.POST["coupon_id"] != "":
                        CouponModel.objects.update_or_create(id=int(request.POST["coupon_id"]),defaults={

                            "coupon_name":request.POST['coupon_name'],
                            "valid_from":form.cleaned_data['valid_from'],
                            "valid_through":request.POST['valid_through'],
                            "coupon_code":request.POST['coupon_code'],
                            "coupon_value":coupon_val,
                            "green_point":request.POST['green_point'],
                            "coupon_logo":m_logo,
                            # "coupon_background_color" :request.POST['color'],
                            "coupon_background_color":"",
                            "coupon_valid_for_user":request.POST['coupon_valid_for_user'],
                            'merchant_business_id': merchant_business_object.id,
                            'customer_state': customer_state_value_new, 
                            'customer_city': customer_city_value_new, 
                            'customer_area': customer_area_value_new,
                            'amount_in':amount_in,
                            'coupon_amount':coupon_cost,
                            })
                        sweetify.success(request, title="Success", icon="success",
                                         text="Coupon updated Successfully", timer=1500)
                    else:
                        status1 = CouponModel.objects.create(
                            merchant_id=merchant_object,
                            coupon_name=form.cleaned_data['coupon_name'],
                            valid_from=form.cleaned_data['valid_from'],
                            valid_through=form.cleaned_data['valid_through'],
                            coupon_code=form.cleaned_data['coupon_code'],
                            coupon_value=coupon_val,
                            green_point=form.cleaned_data['green_point'],
                            coupon_logo=m_logo,
                            # coupon_background_color =request.POST['color'],
                            coupon_background_color="",
                            coupon_valid_for_user = request.POST['coupon_valid_for_user'],
                            merchant_business_id = merchant_business_object.id,
                            customer_state = customer_state_value_new, 
                            customer_city = customer_city_value_new, 
                            customer_area = customer_area_value_new,
                            total_customers = customer_count,
                            amount_in = amount_in,
                            coupon_amount=coupon_cost,
                        )
                        sweetify.success(request, title="Success", icon="success",
                                         text="Coupon Created Successfully", timer=1500)
            else:
                coupon_caption_name = request.POST['coupon_caption_name']
                if request.POST["coupon_id"] != "":
                    print("abc")
                    # CouponModel.objects.update_or_create(id=int(request.POST["coupon_id"]),defaults={
                    #     "coupon_name":request.POST['coupon_name'],
                    #     "valid_from":request.POST['valid_from'],
                    #     "valid_through":request.POST['valid_through'],
                    #     "coupon_code":request.POST['coupon_code'],
                    #     "green_point":request.POST['green_point'],
                    #     "coupon_logo":m_logo,
                    #     "coupon_caption":coupon_caption_name,
                    #     "coupon_background_color":"",
                    #     "coupon_valid_for_user": request.POST['coupon_valid_for_user'],
                    #     'merchant_business_id': merchant_business_object.id,
                    #     'merchant_business_id': merchant_business_object.id,
                    #     'customer_state': customer_state_value_new, 
                    #     'customer_city': customer_city_value_new, 
                    #     'customer_area': customer_area_value_new,,
                    #     'amount_in':amount_in
                    #     })
                    # sweetify.success(request, title="Success", icon="success",
                    #                  text="Coupon updated Successfully", timer=1500)

                else:
                    status1 = CouponModel.objects.create(
                        merchant_id=merchant_object,
                        coupon_name=form.cleaned_data['coupon_name'],
                        valid_from=form.cleaned_data['valid_from'],
                        valid_through=form.cleaned_data['valid_through'],
                        coupon_code=form.cleaned_data['coupon_code'],
                        green_point=form.cleaned_data['green_point'],
                        coupon_logo=m_logo,
                        coupon_caption=coupon_caption_name,
                        # coupon_background_color =request.POST['color'],
                        coupon_background_color = "",
                        coupon_valid_for_user = request.POST['coupon_valid_for_user'],
                        merchant_business_id = merchant_business_object.id,
                        customer_state = customer_state_value_new, 
                        customer_city = customer_city_value_new, 
                        customer_area = customer_area_value_new,
                        total_customers = customer_count,
                        amount_in = amount_in,
                        coupon_amount=coupon_cost,
                    )
                    sweetify.success(request, title="Success", icon="success",
                                     text="Coupon Created Successfully", timer=1500)

        try:
            coupon_details = CouponModel.objects.get(id = status1.id)

            merchant_business_object = MerchantProfile.objects.get(id = coupon_details.merchant_business_id)

            if coupon_details.customer_state and not coupon_details.customer_city and not coupon_details.customer_area: 

                users = GreenBillUser.objects.filter(c_state__in=ast.literal_eval(coupon_details.customer_state))

                for mobile_no in users:
                    device = DeviceId.objects.filter(mobile_no=mobile_no, user_type = 'customer').first()
                   
                    if device:
                        push_service = FCMNotification(api_key=settings.API_KEY)
                        result = ''

                        if device:
                            registration_id = device.device_id
                        else:
                            registration_id = ""

                        message_title = "New Coupon"

                        message_body = "Hurray, checkout exciting coupons by  " + str(merchant_business_object.m_business_name)

                        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

            elif coupon_details.customer_state and coupon_details.customer_city and not coupon_details.customer_area:

                users = GreenBillUser.objects.filter(c_state__in=ast.literal_eval(coupon_details.customer_state))

                for i in users:

                    if i.c_city:

                        if i.c_city in ast.literal_eval(coupon_details.customer_city):

                            device = DeviceId.objects.filter(mobile_no=i, user_type = 'customer').first()
                    
                            if device:
                                push_service = FCMNotification(api_key=settings.API_KEY)
                                result = ''

                                if device:
                                    registration_id = device.device_id
                                else:
                                    registration_id = ""

                                message_title = "New Coupon uploaded by Merchant"

                                message_body = "Hurray, checkout exciting coupons by  "  + str(merchant_business_object.m_business_name)

                                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

            elif coupon_details.customer_state and coupon_details.customer_city and coupon_details.customer_area:
                    
                users = GreenBillUser.objects.filter(c_state__in=ast.literal_eval(coupon_details.customer_state))

                for i in users:

                    if i.c_city:

                        if i.c_city in ast.literal_eval(coupon_details.customer_city):

                            if i.c_area in ast.literal_eval(coupon_details.customer_area):

                                device = DeviceId.objects.filter(mobile_no=i, user_type = 'customer').first()
                        
                                if device:
                                    push_service = FCMNotification(api_key=settings.API_KEY)
                                    result = ''

                                    if device:
                                        registration_id = device.device_id
                                    else:
                                        registration_id = ""

                                    message_title = "New Coupon uploaded by Merchant"

                                    message_body = "Hurray, checkout exciting coupons by  "  + str(merchant_business_object.m_business_name)

                                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        except:
            pass

    coupon_list = CouponModel.objects.filter(merchant_business_id = merchant_business_object.id, coupon_panel = "merchant").order_by('-id')
    total_count = CouponModel.objects.filter(merchant_business_id = merchant_business_object.id, coupon_panel = "merchant").count()
    # waiting_count = CouponModel.objects.filter(merchant_business_id = merchant_business_object.id, coupon_panel = "merchant").count()
    # approve_count = CouponModel.objects.filter(merchant_business_id = merchant_business_object.id, coupon_panel = "merchant").count()
    cust_data = GreenBillUser.objects.values('c_state').distinct()
    # print('cust_data',cust_data)
    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        coupon_amount = data.coupon_amount
    else:
        coupon_amount = 0

    # print('coupon_amount',coupon_amount)
    today = date.today()
    expired_count = 0
    active_count = 0
    for coupon in coupon_list:
        merchant_object = MerchantProfile.objects.get(id = coupon.merchant_business_id)
        coupon.merchant_business_name = merchant_object.m_business_name

        if coupon.valid_through < today:
            coupon.expiry_status = True
            expired_count = expired_count + 1
        else:
            coupon.expiry_status = False
            active_count = active_count + 1

        if coupon.coupon_logo:
            try:
                coupon.coupon_logo = coupon.coupon_logo.url
            except:
                coupon.coupon_logo = ""
        if coupon.total_customers:
            if coupon.total_customers:
                coupon.total_amount = float(coupon_amount) * float(coupon.total_customers)
        coupon.count_redeem = RedeemCouponModel.objects.filter(coupon_id = coupon.id ).count()



    context = {
        'total_count': total_count,
        "cust_data": cust_data,
        "coupon_list": coupon_list,
        "PromotionsNavclass":"active",
        "ShowPromotionsNavclass":"show",
        'CouponNavclass': 'active',
        'expired_count': expired_count,
        'active_count': active_count,
    }

    return render(request, "merchant/coupon/coupon.html", context)


def Delete_Coupon_by_id(request, id):
    # print('delete',id)
    # coupon_obj = CouponModel.objects.get(id=id).delete()
    # if coupon_obj:
    #   return JsonResponse({"success": True})
    # else:
    #   return JsonResponse({"success": False})
    if request.method == "POST":
        coupon_obj = CouponModel.objects.get(id= id).delete()
        sweetify.success(request, title="success", icon='success', text='Coupon deleted Successfully !!!', timer=1500)
        return redirect(add_coupon_view)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Coupon!!!', timer=1500)
        return redirect(add_coupon_view)




def coupon_list(request):
    coupon_list = CouponModel.objects.filter(coupon_panel='merchant').order_by('-id')
    total_count = CouponModel.objects.filter(coupon_panel='merchant').count()
    today = date.today()
    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        coupon_amount = data.coupon_amount
    else:
        coupon_amount = 0
    total_active = 0 
    total_expired = 0   
    for coupon in coupon_list:

        if coupon.valid_through < today:
            coupon.expiry_status = True
            total_expired = total_expired + 1
        else:
            coupon.expiry_status = False
            total_active= total_active + 1
            
        coupon.coupon_redeem_count = RedeemCouponModel.objects.filter(coupon_id=coupon.id).count()
        # print('ID',coupon.merchant_business_id)
        merchant_business = MerchantProfile.objects.filter(id=coupon.merchant_business_id)  #id=coupon.merchant_business_id
        for m in merchant_business:
            coupon.m_business_name = m.m_business_name
            coupon.m_business_category = m.m_business_category
            if m.m_business_logo:
                try:
                    coupon.coupon_logo = m.m_business_logo
                except:
                    coupon.coupon_logo = ""

            if coupon.total_customers:
                coupon.total_amount = float(coupon_amount) * float(coupon.total_customers)

            
    # if coupon.coupon_logo:
    #         try:
    #             coupon.coupon_logo = coupon.coupon_logo.url
    #         except:
    #             coupon.coupon_logo = ""

# print(coup)

    context = {
        
        'total_count': total_count,
       'coupon_list':coupon_list,
       'total_active': total_active,
       'total_expired': total_expired,
       'PromotionNavclass':'active',
       'PromotionCollapseShow':'show',
       'CouponListNavclass':'active',
    }


    return render(request, "coupon_list.html", context)

def get_city_by_state_ids(request):

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
    print(filtered_city_list)

    return JsonResponse({"data":filtered_city_list})


def get_area_by_city_names_in_coupon(request):

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

def get_number_of_users_by_sutomer(request):
    get_filter_by_customer_state = request.POST.get('get_filter_by_customer_state')
    if get_filter_by_customer_state:
        splitted_customer_state = get_filter_by_customer_state.split(",")

        customers = GreenBillUser.objects.filter(c_state__in=splitted_customer_state).count()
    else:
        customers = 0
    return JsonResponse({"data":customers})

def get_cost_by_cutomer_state(request):
    get_filter_by_customer_state = request.POST.get('get_filter_by_customer_state')
    if get_filter_by_customer_state:
        splitted_customer_state = get_filter_by_customer_state.split(",")

        customers = GreenBillUser.objects.filter(c_state__in=splitted_customer_state).count()
    else:
        customers = 0

    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        coupon_amount = data.coupon_amount
    else:
        coupon_amount = 0

    total_cost1 = float(customers) * float(coupon_amount)

    total_cost = "{:.2f}".format(total_cost1)

    return JsonResponse({"data":total_cost})

def get_number_of_users_per_coupon(request):
    get_filter_by_customer_state = request.POST.get('get_filter_by_customer_state')
    get_filter_by_customer_city = request.POST.get('get_filter_by_customer_city')
    get_filter_by_customer_area = request.POST.get('get_filter_by_customer_area')
    
    if get_filter_by_customer_state:
        splitted_customer_state = get_filter_by_customer_state.split(",")

    if get_filter_by_customer_city:
        splitted_customer_city = get_filter_by_customer_city.split(",")

    if get_filter_by_customer_area:
        splitted_customer_area = get_filter_by_customer_area.split(",")

    cust_count = 0

    list1 =[]
    filtered_cust_list =[]
    if get_filter_by_customer_state:
        customers = GreenBillUser.objects.filter(c_state__in=splitted_customer_state)
        for i in customers:
            if i.c_city != '' and i.c_area != '':
                if get_filter_by_customer_city:
                    if i.c_city in splitted_customer_city:
                        if get_filter_by_customer_area:
                            if i.c_area in splitted_customer_area:
                                cust_count = cust_count + 1
                        else:
                            cust_count = cust_count + 1
                else:
                    cust_count = cust_count + 1
                    
    # print('cust_count1',cust_count)

    
    list1.append({
        "customer_count": cust_count
    })

    for x in list1:
        if x['customer_count'] not in filtered_cust_list:
            filtered_cust_list.append(x['customer_count'])
    
    # print('filtered_cust_list',filtered_cust_list)
    return JsonResponse({"data":filtered_cust_list})


def get_total_cost_per_user(request):
    get_filter_by_customer_state = request.POST.get('get_filter_by_customer_state')
    get_filter_by_customer_city = request.POST.get('get_filter_by_customer_city')
    get_filter_by_customer_area = request.POST.get('get_filter_by_customer_area')

    if get_filter_by_customer_state:
        splitted_customer_state = get_filter_by_customer_state.split(",")

    if get_filter_by_customer_city:
        splitted_customer_city = get_filter_by_customer_city.split(",")

    if get_filter_by_customer_area:
        splitted_customer_area = get_filter_by_customer_area.split(",")

    cust_count = 0

    list1 =[]
    filtered_cust_list =[]

    if get_filter_by_customer_state:
        customers = GreenBillUser.objects.filter(c_state__in=splitted_customer_state)
        for i in customers:
            if get_filter_by_customer_city:
                if i.c_city != '' and i.c_area != '':
                    if i.c_city in splitted_customer_city:
                        if get_filter_by_customer_area:
                            if i.c_area in splitted_customer_area:
                                cust_count = cust_count + 1
                        else:
                            cust_count = cust_count + 1
            else:
                cust_count = cust_count + 1
                    
    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        coupon_amount = data.coupon_amount
    else:
        coupon_amount = 0

    total_cost1 = float(cust_count) * float(coupon_amount)

    total_cost = "{:.2f}".format(total_cost1)   
    
    list1.append({
        "customer_count": total_cost
    })

    for x in list1:
        if x['customer_count'] not in filtered_cust_list:
            filtered_cust_list.append(x['customer_count'])
    
    # print('filtered_cust_list',filtered_cust_list)
    return JsonResponse({"data":filtered_cust_list})