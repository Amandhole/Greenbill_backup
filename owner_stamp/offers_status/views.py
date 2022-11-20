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




@login_required(login_url="/login/")
@user_passes_test(is_owner)
def owner_offers(request):
    if request.method == "POST":
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
            obj1 = OfferModel.objects.update_or_create(
                id=int(request.POST["offer_id"]), defaults={"Offer_type": Offer_type, "offer_name": offer_name, "offer_caption": offer_caption, "valid_from": valid_from, "valid_through": valid_through, "offer_business_category": offer_business_category})
        else:
            if request.POST['user'] == "Merchant":
                offer_name = request.POST['offer_name']
                offer_caption = request.POST['offer_caption']
                # business_name = request.POST['business_name']
            
                Offer_type = request.POST['user']
                
                offer_image = request.FILES['offer_image']
                # offer_logo = request.FILES['offer_logo']
                valid_from = request.POST['valid_from']
                valid_through = request.POST['valid_through']
                status = request.POST['status']
                offer_panel = request.POST['offer_panel']
                o_business_name = request.POST['o_business_name']

                business_category_value = request.POST['business_category_value']
                business_category_value_new = business_category_value.split(",")

                merchant_state_value = request.POST['merchant_state_value']
                merchant_state_value_new = merchant_state_value.split(",")
                
                merchant_city_value = request.POST['merchant_city_value']
                merchant_city_value_new = merchant_city_value.split(",")

                merchant_area_value = request.POST['merchant_area_value']
                merchant_area_value_new = merchant_area_value.split(",")

                obj2 = OfferModel.objects.create(
                    merchant_state=merchant_state_value_new, merchant_city=merchant_city_value_new, merchant_area=merchant_area_value_new,
                    o_business_name=o_business_name, offer_panel=offer_panel, status=status, offer_name=offer_name,
                    offer_caption=offer_caption, valid_from=valid_from, valid_through=valid_through, offer_image=offer_image,
                    Offer_type=Offer_type, offer_business_category=business_category_value_new)

            if request.POST['user'] == "Customer":
                offer_name = request.POST['offer_name']
                offer_caption = request.POST['offer_caption']
                # business_name = request.POST['business_name']
            
                Offer_type = request.POST['user']
                # offer_business_category = request.POST['offer_business_category']
                offer_image = request.FILES['offer_image']
                # offer_logo = request.FILES['offer_logo']
                valid_from = request.POST['valid_from']
                valid_through = request.POST['valid_through']
                status = request.POST['status']
                offer_panel = request.POST['offer_panel']
                o_business_name = request.POST['o_business_name']
                
                customer_city_value = request.POST['customer_city_value']
                customer_city_value_new = customer_city_value.split(",")

                obj2 = OfferModel.objects.create(
                    customer_city=customer_city_value_new, o_business_name=o_business_name,
                    offer_panel=offer_panel, status=status, offer_name=offer_name, offer_caption=offer_caption, valid_from=valid_from,
                    valid_through=valid_through, offer_image=offer_image, Offer_type=Offer_type)

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
    today = dt.date.today()
    for offer in data:
        if offer.valid_through <= today:
            offer.expire_status=True
           
    record = OfferModel.objects.filter(offer_panel = "owner")
    print('record', record)
    counter = 0
    for owner in record:
        if owner.valid_through >= today:
            counter = (counter) + 1
            owner.expire_status=True
            print("BB",counter)
            
            
    print("AA",counter)
    owner_business_name = generalSetting.objects.all().order_by("-id")
    cust_data = GreenBillUser.objects.values('c_area').distinct()
    merchantList1 = MerchantProfile.objects.values('m_state').distinct()
    merchantList2 = MerchantProfile.objects.values('m_district').distinct()
    merchantList3 = MerchantProfile.objects.values('m_city').distinct()
    merchantList4 = MerchantProfile.objects.values('m_area').distinct()
            
    form = generalSettingForm()

    context = {
        'data': data,
        'object': object,
        'cust_data':cust_data,
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
    }
    return render(request, "owner_offerstatus/owner-create-offer.html", context)



def Owner_offers(request):
    data_status = OfferModel.objects.all().order_by('-id')
    print(data_status)
    context = {
    "data_status" : data_status,
    # 'form': form,
    'PromotionNavclass': "active", 
    'PromotionCollapseShow': "show",
    'OfferstatusNavclass': "active",
    }
    return render(request, "owner_offerstatus/status.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner)
def approve_offer_by_id(request, id):
    print("szc")
    if request.method == "POST":
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

