import re
from django.shortcuts import render
from .models import OwnerCouponModel
from .forms import OwnerCouponsForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import sweetify
from users.models import Merchant_users, GreenBillUser, MerchantProfile
from app.models import generalSetting
from coupon.models import CouponModel
from datetime import date, datetime

from referral_points.models import *

# Create your views here.


def add_coupon_owner_view(request):

    
    merchant_object = GreenBillUser.objects.get(id = request.user.id)
    logo = generalSetting.objects.get(id=1) 
    c_logo = logo.o_business_logo
    business = logo.business_name
    
    if request.method == "POST":

        form = OwnerCouponsForm(request.POST, request.FILES)
        amount_in = ''
        if form.is_valid():
            coupon_amount_cost = request.POST.get('customer_total_cost')
            owner_panel="owner"
            coupon_type = request.POST['coupon_type']

            add_merchant_name = request.POST['add_merchant_name']

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
                
            coupon_type = request.POST['coupon_type']
            coupon_logo = request.FILES['merchant_coupon_logo']
            customer_count = request.POST['customer_count']
           
            if coupon_type == "coupon_value":
                amount_in = request.POST['amount_in']
                if amount_in == "percentage":
                    coupon_val = request.POST['coupon_value_percent']
                    coupon_val_per = coupon_val 
                    status1 = ""
                    status2 = ""
                    print(request.POST['coupon_id'])
                    if request.POST["coupon_id"] != "":
                        status1 = CouponModel.objects.update_or_create(id=int(request.POST["coupon_id"]),defaults={
                            "coupon_name":request.POST['coupon_name'],
                            "valid_from":request.POST['valid_from'],
                            "valid_through":request.POST['valid_through'],
                            "coupon_code":request.POST['coupon_code'],
                            "coupon_value":coupon_val_per,
                            "green_point":request.POST['green_point'],
                            "coupon_logo":coupon_logo,
                            "coupon_background_color":"",
                            # "coupon_background_color":request.POST['color'],
                            "coupon_valid_for_user":request.POST['coupon_valid_for_user'],
                            'merchant_business_id': merchant_business_object.id,
                            'customer_state': customer_state_value_new, 
                            'customer_city': customer_city_value_new, 
                            'customer_area': customer_area_value_new,
                            'owner_name': add_merchant_name,
                            'add_merchant_name_by_owner': add_merchant_name,
                            'amount_in':amount_in,
                            'coupon_amount':coupon_amount_cost,
                            })
                        
                    else:
                        status2=CouponModel.objects.create(
                            coupon_name=form.cleaned_data['coupon_name'],
                            valid_from=form.cleaned_data['valid_from'],
                            valid_through=form.cleaned_data['valid_through'],
                            coupon_code=form.cleaned_data['coupon_code'],
                            coupon_value=coupon_val_per+ "%",
                            green_point=form.cleaned_data['green_point'],
                            coupon_logo=  coupon_logo,
                            # coupon_background_color =request.POST['color'],
                            coupon_background_color = "",
                            coupon_valid_for_user = request.POST['coupon_valid_for_user'],
                            # merchant_business_id = merchant_business_object.id,
                            customer_state = customer_state_value_new, 
                            customer_city = customer_city_value_new, 
                            customer_area = customer_area_value_new,
                            coupon_panel = owner_panel,
                            owner_name = add_merchant_name,
                            merchant_id = request.user,
                            add_merchant_name_by_owner = add_merchant_name,
                            total_customers = customer_count,
                            amount_in = amount_in,
                            coupon_amount = coupon_amount_cost,
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
                            "coupon_logo": coupon_logo,
                            # "coupon_background_color" :request.POST['color'],
                            "coupon_background_color":"",
                            "coupon_valid_for_user":request.POST['coupon_valid_for_user'],
                            'customer_state': customer_state_value_new, 
                            'customer_city': customer_city_value_new, 
                            'customer_area': customer_area_value_new,
                            # 'merchant_business_id': merchant_business_object.id,
                            'owner_name': add_merchant_name,
                            'add_merchant_name_by_owner': add_merchant_name,
                            'amount_in':amount_in,
                            'coupon_amount':coupon_amount_cost,
                            })
                        sweetify.success(request, title="Success", icon="success",
                                         text="Coupon updated Successfully", timer=1500)
                    else:
                        CouponModel.objects.create(
                            coupon_name=form.cleaned_data['coupon_name'],
                            valid_from=form.cleaned_data['valid_from'],
                            valid_through=form.cleaned_data['valid_through'],
                            coupon_code=form.cleaned_data['coupon_code'],
                            coupon_value=coupon_val,
                            green_point=form.cleaned_data['green_point'],
                            coupon_logo= coupon_logo,
                            # coupon_background_color =request.POST['color'],
                            coupon_background_color="",
                            coupon_valid_for_user = request.POST['coupon_valid_for_user'],
                            # merchant_business_id = merchant_business_object.id,
                            customer_state = customer_state_value_new, 
                            customer_city = customer_city_value_new, 
                            customer_area = customer_area_value_new,
                            coupon_panel = owner_panel,
                            owner_name = add_merchant_name,
                            merchant_id = request.user,
                            add_merchant_name_by_owner = add_merchant_name,
                            total_customers = customer_count,
                            amount_in = amount_in,
                            coupon_amount = coupon_amount_cost,
                        )
                        sweetify.success(request, title="Success", icon="success",
                                         text="Coupon Created Successfully", timer=1500)
            else:
                coupon_caption_name = request.POST['coupon_caption_name']
                if request.POST.get("coupon_id") != "":
                    CouponModel.objects.update_or_create(id=request.POST.get("coupon_id"),defaults={
                        "coupon_name":request.POST['coupon_name'],
                        "valid_from":request.POST['valid_from'],
                        "valid_through":request.POST['valid_through'],
                        "coupon_code":request.POST['coupon_code'],
                        "green_point":request.POST['green_point'],
                        "coupon_logo": coupon_logo,
                        "coupon_caption":coupon_caption_name,
                        "coupon_background_color":"",
                        "coupon_valid_for_user": request.POST.get('coupon_valid_for_user'),
                        # 'merchant_business_id': merchant_business_object.id,
                        'customer_state': customer_state_value_new, 
                        'customer_city': customer_city_value_new, 
                        'customer_area': customer_area_value_new,
                        'owner_name': add_merchant_name,
                        'add_merchant_name_by_owner': add_merchant_name,
                        'amount_in':amount_in,
                        'coupon_amount':coupon_amount_cost,
                        })
                    sweetify.success(request, title="Success", icon="success",
                                     text="Coupon updated Successfully", timer=1500)

                else:
                    CouponModel.objects.create(
                        coupon_name=form.cleaned_data['coupon_name'],
                        valid_from=form.cleaned_data['valid_from'],
                        valid_through=form.cleaned_data['valid_through'],
                        coupon_code=form.cleaned_data['coupon_code'],
                        green_point=form.cleaned_data['green_point'],
                        coupon_caption=coupon_caption_name,
                        coupon_logo= coupon_logo,
                        coupon_background_color = "",
                        coupon_valid_for_user = request.POST['coupon_valid_for_user'],\
                        customer_state = customer_state_value_new, 
                        customer_city = customer_city_value_new, 
                        customer_area = customer_area_value_new,
                        coupon_panel = owner_panel,
                        owner_name = add_merchant_name,
                        merchant_id = request.user,
                        add_merchant_name_by_owner = add_merchant_name,
                        total_customers = customer_count,
                        amount_in = amount_in,
                        coupon_amount = coupon_amount_cost,
                    )
                    sweetify.success(request, title="Success", icon="success",
                                     text="Coupon Created Successfully", timer=1500)

    coupon_list = CouponModel.objects.filter(coupon_panel = "owner").order_by('-id')
    total_count = CouponModel.objects.filter(coupon_panel = "owner").count()
    
    cust_data = GreenBillUser.objects.values('c_state').distinct()
    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        coupon_amount = data.coupon_amount
    else:
        coupon_amount = 0

    today = date.today()

    total_active = 0
    total_expired = 0

    for coupon in coupon_list:
        
        if coupon.valid_through < today:
            coupon.expiry_status = True
            total_expired = total_expired + 1
        else:
            coupon.expiry_status = False
            total_active = total_active + 1

        if coupon.total_customers:
            coupon.total_amount = float(coupon_amount) * float(coupon.total_customers)
    #     merchant_object = MerchantProfile.objects.get(id = coupon.merchant_business_id)
    #     coupon.merchant_business_name = merchant_object.m_business_name

    print("cust_data",cust_data)

    context = {
        "cust_data": cust_data,
        'total_count': total_count,
        'total_active':total_active,
        'total_expired': total_expired,
        "coupon_list": coupon_list,
        # 'logo':logo,
        'CouponNavclass': 'active',
        'PromotionNavclass':'active',
        "PromotionCollapseShow":'show'
    }

    return render(request, "super_admin/owner_coupon.html", context)


# def owner_coupon_list(request):

#     coupon_list = OwnerCouponModel.objects.all()

#     context = {
#     'coupon_list':coupon_list,
    
#     }


def Delete_Coupon(request, id):
    coupon_obj = OwnerCouponModel.objects.get(id=id).delete()
    if coupon_obj:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})

def get_city_by_state_ids_in_owner(request):

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


def get_area_by_city_names_in_owner_coupon(request):

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

