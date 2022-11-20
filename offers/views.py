from django.shortcuts import render
import sweetify
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import OfferForm
from .models import OfferModel
from django.contrib.auth.decorators import login_required
from app.views import is_merchant_or_merchant_staff, is_partner
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail, EmailMessage, BadHeaderError, EmailMultiAlternatives
from email.mime.image import MIMEImage
from users.models import *
from django.http import HttpResponse
from category_and_tags.models import business_category
from app.models import generalSetting
from customer_info.models import Customer_Info_Model
from datetime import date, datetime
from referral_points.models import *

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_offers_old(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    m_logo = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True).m_business_logo
    # print('m_logo',m_logo)

    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    form = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

    merchant_name_object = form.m_business_name
    business_data = form.m_business_category

    merchant_business_name = merchant_name_object
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
            # offer_image = request.POSt['offer_image']
            obj1 = OfferModel.objects.update_or_create(
                id=int(request.POST["offer_id"]), defaults={"Offer_type": Offer_type, "offer_name": offer_name, "offer_caption": offer_caption, "valid_from": valid_from, "valid_through": valid_through, "offer_business_category": offer_business_category})
        else:
            if request.POST['user'] == "Merchant":
                offer_name = request.POST['offer_name']
                offer_caption = request.POST['offer_caption']
                Offer_type = request.POST['user']
                offer_business_category = request.POST.getlist('offer_business_category[]')
                offer_image = request.FILES['offer_image']
            
                valid_from = request.POST['valid_from']
                valid_through = request.POST['valid_through']

                merchant_state = request.POST.getlist('merchant_state[]')
                # merchant_district = request.POST['merchant_district']
                merchant_city = request.POST.getlist('merchant_city[]')
                merchant_area = request.POST.getlist('merchant_area[]')
                # offer_amount = request.POST['offer_amount']
           
                obj2 = OfferModel.objects.create(
                     merchant_state=merchant_state, merchant_city=merchant_city, merchant_area=merchant_area, check_business_category=business_data, merchant_business_name = merchant_business_name, merchant_user=request.user, offer_name=offer_name, merchant_business_id = merchant_business_id, offer_caption=offer_caption, valid_from=valid_from, valid_through=valid_through, offer_image=offer_image, Offer_type=Offer_type, offer_business_category=offer_business_category)
            if request.POST['user'] == "Customer":
                offer_name = request.POST['offer_name']
                offer_caption = request.POST['offer_caption']
                Offer_type = request.POST['user']
                # offer_business_category = request.POST['offer_business_category']
                offer_image = request.FILES['offer_image']
            
                valid_from = request.POST['valid_from']
                valid_through = request.POST['valid_through']
                customer_city = request.POST.getlist('customer_city[]')
                # offer_amount = request.POST['offer_amount']
                
           
                obj2 = OfferModel.objects.create(
                    customer_city=customer_city, merchant_business_name = merchant_business_name, merchant_user=request.user, offer_name=offer_name, merchant_business_id = merchant_business_id, offer_caption=offer_caption, valid_from=valid_from, valid_through=valid_through, offer_image=offer_image, Offer_type=Offer_type)

        if obj1:
            sweetify.success(request, title="Success", icon='success',
                             text='Offers updated Successfully.', timer=1500)

        elif obj2:
            sweetify.success(request, title="Success", icon='success',
                             text='Offers created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...",
                             icon='error', text='Fail to create.', timer=1000)
    
    data = OfferModel.objects.filter().order_by("-id")
    total_count = OfferModel.objects.filter(merchant_business_id = merchant_business_id, offer_panel='merchant').count()
    waiting_count = OfferModel.objects.filter(merchant_business_id = merchant_business_id, offer_panel='merchant', status=0).count()
    approve_count = OfferModel.objects.filter(merchant_business_id = merchant_business_id, offer_panel='merchant', status=1).count()

    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        offer_amount = data.offer_amount
    else:
        offer_amount = 0

    print('offer_amount',offer_amount)

    today = date.today()

    for offer in data:
        if offer.valid_through <= today:
            offer.expire_status=True
        if offer.customer_merchant_count:
            offer.total_amount = int(offer_amount) * int(offer.customer_merchant_count)

    cust_data = GreenBillUser.objects.values('c_area').distinct()
    merchantList1 = MerchantProfile.objects.values('m_state').distinct()
    merchantList2 = MerchantProfile.objects.values('m_district').distinct()
    merchantList3 = MerchantProfile.objects.values('m_city').distinct()
    merchantList4 = MerchantProfile.objects.values('m_area').distinct()

    partner_records = PartnerProfile.objects.values('p_state').distinct()
    print(partner_records)
    context = {
        'total_count': total_count,
        'waiting_count': waiting_count,
        'approve_count': approve_count,
        'partner_records': partner_records,
        'data': data,
        'form': form,
        'cust_data' : cust_data,  
        'merchantList1' : merchantList1,
        'merchantList2' : merchantList2,
        'merchantList3' : merchantList3,
        'merchantList4' : merchantList4,
        'PromotionsNavclass': "active", 
        'ShowPromotionsNavclass': "show",
        'CreateOffersNavclass': "active",
    }
    return render(request, "merchant/merchant_offers/offers.html", context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_offers(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    m_logo = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True).m_business_logo
    # print('m_logo',m_logo)

    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    form = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

    merchant_name_object = form.m_business_name
    business_data = form.m_business_category

    merchant_business_name = merchant_name_object
    if request.method == "POST":
        post_amount = request.POST.get('customer_total_cost')

        if post_amount == "0.00":
            post_offer_status = "1"
        else:
            post_offer_status = "0"

        # print(post_offer_status,'-------------------------------------------')

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
            # offer_image = request.POSt['offer_image']
            
            obj1 = OfferModel.objects.update_or_create(
                id=int(request.POST["offer_id"]), defaults={"offer_amount":post_amount, "status":post_offer_status, "Offer_type": Offer_type, "offer_name": offer_name, "offer_caption": offer_caption, "valid_from": valid_from, "valid_through": valid_through, "offer_business_category": offer_business_category,"customer_merchant_count":customer_count})
        else:
            if request.POST['user'] == "Merchant":
                offer_name = request.POST['offer_name']
                offer_caption = request.POST['offer_caption']
                Offer_type = request.POST['user']

                offer_image = request.FILES['offer_image']
            
                valid_from = request.POST['valid_from']
                valid_through = request.POST['valid_through']

                customer_count = request.POST['customer_count']

                # merchant_district = request.POST['merchant_district']
                # offer_amount = request.POST['offer_amount']

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
                     offer_amount=post_amount, status = post_offer_status, offer_logo = m_logo, merchant_state = merchant_state_value_new, merchant_city = merchant_city_value_new, merchant_area = merchant_area_value_new,
                     check_business_category = business_data, merchant_business_name = merchant_business_name, merchant_user = request.user,
                     offer_name = offer_name, merchant_business_id = merchant_business_id, offer_caption = offer_caption, valid_from = valid_from,
                     valid_through = valid_through, offer_image = offer_image, Offer_type = Offer_type, offer_business_category = business_category_value_new,
                     customer_merchant_count=customer_count
                )
            
            if request.POST['user'] == "Customer":
                offer_name = request.POST['offer_name']
                offer_caption = request.POST['offer_caption']
                Offer_type = request.POST['user']
                # offer_business_category = request.POST['offer_business_category']
                offer_image = request.FILES['offer_image']
                customer_count = request.POST['customer_count']
            
                valid_from = request.POST['valid_from']
                valid_through = request.POST['valid_through']
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
                    offer_amount=post_amount, status = post_offer_status, offer_logo = m_logo, customer_state = customer_state_value_new, customer_city = customer_city_value_new, customer_area = customer_area_value_new, merchant_business_name = merchant_business_name, merchant_user=request.user, offer_name=offer_name, merchant_business_id = merchant_business_id, offer_caption=offer_caption, valid_from=valid_from, valid_through=valid_through, offer_image=offer_image, Offer_type=Offer_type,customer_merchant_count=customer_count)

            if request.POST['user'] == "Partner":
                offer_name = request.POST['offer_name']
                offer_caption = request.POST['offer_caption']
                Offer_type = request.POST['user']

                offer_image = request.FILES['offer_image']
            
                valid_from = request.POST['valid_from']
                valid_through = request.POST['valid_through']

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
                     offer_amount=post_amount, status = post_offer_status, offer_logo = m_logo, partner_state = partner_state_value_new, partner_city = partner_city_value_new, partner_area = partner_area_value_new,
                     check_business_category = business_data, merchant_business_name = merchant_business_name, merchant_user = request.user,
                     offer_name = offer_name, merchant_business_id = merchant_business_id, offer_caption = offer_caption, valid_from = valid_from,
                     valid_through = valid_through, offer_image = offer_image, Offer_type = Offer_type, customer_merchant_count=customer_count
                )
        if obj1:
            sweetify.success(request, title="Success", icon='success',
                             text='Offers updated Successfully.', timer=1500)

        elif obj2:
            sweetify.success(request, title="Success", icon='success',
                             text='Offers created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...",
                             icon='error', text='Fail to create.', timer=1000)
    
    data = OfferModel.objects.filter(merchant_business_id = merchant_business_id).order_by("-id")

    if PromotionsAmount.objects.all():
        amount = PromotionsAmount.objects.latest('id')
        offer_amount = amount.offer_amount
    else:
        offer_amount = 0

    today = date.today()
    for offer in data:
        if offer.valid_through < today:
            offer.expire_status=True
        if offer.customer_merchant_count:
            offer.total_amount = float(offer_amount) * float(offer.customer_merchant_count)

    states = GreenBillUser.objects.values('c_state').distinct()
    merchantList1 = MerchantProfile.objects.values('m_state').distinct()
    merchantList2 = MerchantProfile.objects.values('m_district').distinct()

    mer_states = MerchantProfile.objects.values('m_state').distinct()

    merchantList3 = MerchantProfile.objects.values('m_city').distinct()
    merchantList4 = MerchantProfile.objects.values('m_area').distinct()
    total_count = OfferModel.objects.filter(merchant_business_id = merchant_business_id, offer_panel='merchant').count()
    waiting_count = OfferModel.objects.filter(merchant_business_id = merchant_business_id, offer_panel='merchant', status=0).count()
    approve_count = OfferModel.objects.filter(merchant_business_id = merchant_business_id, offer_panel='merchant', status=1).count()
    disapprove_count = OfferModel.objects.filter(merchant_business_id = merchant_business_id, offer_panel='merchant', status=2).count()
    partner_records = PartnerProfile.objects.values('p_state').distinct()

    context = {
        'total_count': total_count,
        'waiting_count': waiting_count,
        'approve_count': approve_count,
        'disapprove_count':disapprove_count,
        'data': data,
        'form': form,
        'partner_records': partner_records,
        'cust_data': states,
        'merchant_state': mer_states,
        'merchantList1' : merchantList1,
        'merchantList2' : merchantList2,
        'merchantList3' : merchantList3,
        'merchantList4' : merchantList4,
        'PromotionsNavclass': "active", 
        'ShowPromotionsNavclass': "show",
        'CreateOffersNavclass': "active",
        'b_category': str(merchant_business_id.m_business_category),
    }
    return render(request, "merchant/merchant_offers/offers.html", context)

def get_city_by_state_ids_in_offers(request):

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
    # print(filtered_city_list)

    return JsonResponse({"data":filtered_city_list})


def get_area_by_city_names_in_offers(request):

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

def GetPartnerCity(request):

    partner_state_value = request.POST['partner_state_value']

    partner_state_value_new = partner_state_value.split(",")

    list1 = []

    filtered_city_list = []

    for state in partner_state_value_new:

        partner_object = PartnerProfile.objects.filter(p_state=state)

        for state in partner_object:
            list1.append({
                "p_city": state.p_city
            })
        
    for x in list1:
        if x['p_city'] not in filtered_city_list:
            filtered_city_list.append(x['p_city'])

    return JsonResponse({"data":filtered_city_list})

def GetPartnerArea(request):

    partner_city_value = request.POST['partner_city_value']

    partner_city_value_new = partner_city_value.split(",")

    list1 = []

    filtered_area_list = []

    for city in partner_city_value_new:

        partner_object = PartnerProfile.objects.filter(p_city=city)

        for city in partner_object:
            list1.append({
                "p_area": city.p_area
            })
        
    for x in list1:
        if x['p_area'] not in filtered_area_list:
            filtered_area_list.append(x['p_area'])

    return JsonResponse({"data":filtered_area_list})


def Delete_Offer(request, id):
    offer_obj = OfferModel.objects.get(id=id).delete()
    if offer_obj:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": False})

def Delete_Offer(request, id):
    offer_obj = OfferModel.objects.get(id=id).delete()
    if offer_obj:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": False})


def merchant_offer_view(request):
    view_offer = OfferModel.objects.all().order_by("-id")
    merchant_users_object = Merchant_users.objects.get(user_id = request.user)
    form = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

    merchant_name_object = form.m_business_name 
    # print(merchant_name_object)
    context = {
    "view_offer" : view_offer,
    "form": form,
    'OffersNavclass': "active", 
    'ShowOffersNavclass': "show",
    'ViewOffersNavclass': "active",
    }
    return render(request, "merchant/merchant_offers/offers.html", context)


def merchant_view_offer(request):
    merchant_users_object = Merchant_users.objects.get(user_id = request.user)
    business_name= MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)
    merchant_name_object = business_name.m_business_name 
    # print('merchant_name_object',merchant_name_object)
    merchant_state_object = business_name.m_state
    # print('merchant_state_object',merchant_state_object)
    merchant_city_object = business_name.m_city
    # print('merchant_city_object',merchant_city_object)
    merchant_area_object = business_name.m_area
    # print('merchant_area_object',merchant_area_object)
    merchant_business_category_id = business_name.m_business_category.id
    # print('merchant_business_category_id',merchant_business_category_id)
    
    if request.method == "POST":
        offer_business_categories = request.POST['offer_business_category']
        if request.POST['offer_business_category'] == "All":
            view_offer = OfferModel.objects.all().order_by("-id")
            offer_new = []
            for offer in view_offer:
                if datetime.strptime(str(offer.valid_through), "%Y-%m-%d").date() >= datetime.strptime(str(today_date), "%Y-%m-%d").date():
                    if merchant_name_object != offer.merchant_business_name:
                        if offer.offer_business_category:
                            if str(merchant_business_category_id) in offer.offer_business_category:
                                if offer.merchant_state:
                                    if merchant_state_object in offer.merchant_state:
                                        if offer.merchant_city:
                                            if merchant_city_object in offer.merchant_city:
                                                if offer.merchant_area:
                                                    if merchant_area_object in offer.merchant_area:
                                                        offer_new.append(offer)
                                                else:
                                                    offer_new.append(offer)
                                        else:
                                            offer_new.append(offer)
        else:
            view_offer = OfferModel.objects.filter(offer_business_category=offer_business_categories)
            offer_new = []
            for offer in view_offer:
                if datetime.strptime(str(offer.valid_through), "%Y-%m-%d").date() >= datetime.strptime(str(today_date), "%Y-%m-%d").date():
                    if merchant_name_object != offer.merchant_business_name:
                        if offer.offer_business_category:
                            if str(merchant_business_category_id) in offer.offer_business_category:
                                if offer.merchant_state:
                                    if merchant_state_object in offer.merchant_state:
                                        if offer.merchant_city:
                                            if merchant_city_object in offer.merchant_city:
                                                if offer.merchant_area:
                                                    if merchant_area_object in offer.merchant_area:
                                                        offer_new.append(offer)
                                                else:
                                                    offer_new.append(offer)
                                        else:
                                            offer_new.append(offer)
    else:

        view_offer = OfferModel.objects.all().order_by("-id") 
        
        offer_new = []

        today = date.today()
        today_date = today.strftime("%Y-%m-%d")

        for offer in view_offer:
            if datetime.strptime(str(offer.valid_through), "%Y-%m-%d").date() >= datetime.strptime(str(today_date), "%Y-%m-%d").date():
                if merchant_name_object != offer.merchant_business_name:
                    if offer.offer_business_category:
                        if str(merchant_business_category_id) in offer.offer_business_category:
                            if offer.merchant_state:
                                if merchant_state_object in offer.merchant_state:
                                    if offer.merchant_city:
                                        if merchant_city_object in offer.merchant_city:
                                            if offer.merchant_area:
                                                if merchant_area_object in offer.merchant_area:
                                                    offer_new.append(offer)

    view_owner_offer = generalSetting.objects.all().order_by("-id")
    business_name_data = OfferModel.objects.values('merchant_business_name').distinct()
    
    context = {
    "offer_new" : offer_new,
    "business_name_data" : business_name_data,
    "view_owner_offer" : view_owner_offer,
    "business_name": business_name,
     'OffersNavclass': "active", 
    'ShowOffersNavclass': "show",
    'ViewOffersNavclass': "active",
    }

    return render(request, "merchant/merchant_offers/merchant-offer-status.html", context)



def view_offer_details(request, id):
    data = []

    base_url = "http://157.230.228.250/"

   
    view_offer = OfferModel.objects.filter(id = id)
    object = OfferModel.objects.get(id=id)
    object.cout = object.cout + 1
    object.save()
    # print(view_offer)
    context = {
        "view_offer" : view_offer,
        'OffersNavclass': "active", 
        'ShowOffersNavclass': "show",
        'ViewOffersNavclass': "active",
        
    }
    return render(request, "merchant/merchant_offers/view-offer-details.html", context)




    # merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    # merchant_object = merchant_user_object.merchant_user_id

    # merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
    
    # view_offer = OfferModel.objects.filter(merchant_business_id = merchant_business_id).order_by("-id")



@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_offer_view(request):
    partner_users_object = Partner_users.objects.get(user_id = request.user)
    business_name= PartnerProfile.objects.get(p_user = partner_users_object.partner_user_id, p_active_account = 1)

    view_offer = OfferModel.objects.filter(Offer_type = "Partner").order_by("-id") 

    today = date.today()

    today_date = today.strftime("%Y-%m-%d")

    offer_new = []

    for offer in view_offer:

        if datetime.strptime(str(offer.valid_through), "%Y-%m-%d").date() >= datetime.strptime(str(today_date), "%Y-%m-%d").date(): 

            if offer.partner_state:
                if business_name.p_state in offer.partner_state:

                    if offer.partner_city:

                        if business_name.p_city in offer.partner_city:

                            if offer.partner_area:

                                if business_name.p_area in offer.partner_area:

                                    offer_new.append(offer)
                            else:
                                offer_new.append(offer)
                    else:
                        offer_new.append(offer)
    context = {
        "data_offer" : offer_new,
        'OffersNavclass': "active",
    }
    return render(request, "partner/partner_offers/partner-offers.html", context)

def view_partner_offer_record(request, id):
    data = []

    base_url = "http://157.230.228.250/"

   
    data_offer = OfferModel.objects.filter(id = id)
    object = OfferModel.objects.get(id=id)
    object.cout = object.cout + 1
    object.save()
    # print(data_offer)
    context = {
        "data_offer" : data_offer,
        'OffersNavclass': "active",
    }
    return render(request, "partner/partner_offers/view-partner-offer-details.html", context)



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def Business_category_filters(request, id):
    
    business_id = MerchantProfile.objects.filter(m_business_category = id)

    list1 = []
    for state in business_id:
        
        list1.append({
            "id": state.id,
            "m_state": state.m_state
        })
    
    filtered_state_list = []
    for x in list1:
        if x['m_state'] not in filtered_state_list:
            filtered_state_list.append(x['m_state'])
    
    list2 = []
    for cities in filtered_state_list:
        city = MerchantProfile.objects.filter(m_business_category=id, m_state=cities)
        for offer_city in city:
            var=offer_city.m_city
            list2.append({
                "m_city": offer_city.m_city
            })
    
    filtered_city_list = []
    for y in list2:
        if y['m_city'] not in filtered_city_list:
            filtered_city_list.append(y['m_city'])


    list3 = []
    for Areas in list2:
        area = MerchantProfile.objects.filter(m_business_category=id, m_state=cities)
        for offer_area in area:
            var1=offer_area.m_area
            list3.append({
             "m_area": offer_area.m_area
            })    
    
    filtered_area_list = []
    for z in list3:
        if z['m_area'] not in  filtered_area_list:
            filtered_area_list.append(z['m_area'])

    return JsonResponse({"data1": filtered_state_list , "data2": filtered_city_list , "data3": filtered_area_list})


def get_business_by_state_ids_for_merchant(request):
    merchant_state_value = request.POST['merchant_state_value']
    
    merchant_category_value = request.POST['merchant_category']

    merchant_state_value_new = merchant_state_value.split(",")

    list1 = []

    filtered_city_list = []

    for state in merchant_state_value_new:
        business_id = MerchantProfile.objects.filter(m_state=state).distinct()

        for category in business_id:
            list1.append({
                "b_id": category.m_business_category.id,
                "category": category.m_business_category.business_category_name
            })

    list_of_bool = [True for d in filtered_city_list if d['category'] == x['category']]

    for x in list1:
        if not any(d['category'] == x['category'] for d in filtered_city_list):
            if x['category'] != merchant_category_value:
                filtered_city_list.append({
                    "b_id": x['b_id'],
                    "category": x['category'],
                    })

    return JsonResponse({"data":filtered_city_list})

def get_business_by_state_ids(request):
    merchant_state_value = request.POST['merchant_state_value']

    merchant_state_value_new = merchant_state_value.split(",")

    list1 = []

    filtered_city_list = []

    for state in merchant_state_value_new:
        business_id = MerchantProfile.objects.filter(m_state=state).distinct()

        for category in business_id:
            list1.append({
                "b_id": category.m_business_category.id,
                "category": category.m_business_category.business_category_name
            })

    list_of_bool = [True for d in filtered_city_list if d['category'] == x['category']]

    for x in list1:
        if not any(d['category'] == x['category'] for d in filtered_city_list):
            filtered_city_list.append({
                "b_id": x['b_id'],
                "category": x['category'],
                })

    return JsonResponse({"data":filtered_city_list})
    

    # # business_category_value = request.POST['business_category_value']

    # state_value_new = state_id.split(",")

    # # business_category_value_new = business_category_value.split(",")

    # list1 = []

    # filtered_state_list = []

    # for state in state_value_new:
    #     business_id = MerchantProfile.objects.filter(m_state=state)

    #     for business in business_id:
    #         list1.append({
    #             "m_business_category":business.m_business_category 
    #             })

    # for x in list1:
    #     if x['m_business_category'] not in filtered_business_list:
    #         filtered_business_list.append(x['m_business_category'])

    # return JsonResponse({"data":filtered_state_list})


def get_state_by_business_ids(request):

    business_category_value = request.POST['business_category_value']

    business_category_value_new = business_category_value.split(",")

    list1 = []

    filtered_state_list = []

    for business_category in business_category_value_new:

        business_id = MerchantProfile.objects.filter(m_business_category__id = business_category)

        for state in business_id:
            list1.append({
                "m_state": state.m_state
            })
        
    for x in list1:
        if x['m_state'] not in filtered_state_list:
            filtered_state_list.append(x['m_state'])

    return JsonResponse({"data":filtered_state_list})


def get_city_by_state_names(request):

    merchant_state_value = request.POST['merchant_state_value']

    merchant_state_value_new = merchant_state_value.split(",")

    list1 = []

    filtered_city_list = []

    for state in merchant_state_value_new:

        business_id = MerchantProfile.objects.filter(m_state=state)

        for city in business_id:
            list1.append({
                "m_city": city.m_city
            })
        
    for x in list1:
        if x['m_city'] not in filtered_city_list:
            filtered_city_list.append(x['m_city'])

    return JsonResponse({"data":filtered_city_list})


def get_area_by_city_names(request):

    merchant_city_value = request.POST['merchant_city_value']

    merchant_city_value_new = merchant_city_value.split(",")

    list1 = []

    filtered_city_list = []

    for city in merchant_city_value_new:

        business_id = MerchantProfile.objects.filter(m_city=city)

        for area in business_id:
            list1.append({
                "m_area": area.m_area
            })
        
    for x in list1:
        if x['m_area'] not in filtered_city_list:
            filtered_city_list.append(x['m_area'])

    return JsonResponse({"data":filtered_city_list})

def Number_of_views_in_merchant(request):
    if request.method == "POST":
        id = request.POST["offers_id"]
        print(id)
        object = OfferModel.objects.get(id=id)
        object.cout = object.cout + 1
        object.save()
    return redirect(merchant_view_offer)

def get_customers_by_city(request):
    get_filter_by_customer_state = request.POST['get_filter_by_customer_state']
    get_filter_by_customer_city = request.POST['get_filter_by_customer_city']
    print('aaa',get_filter_by_customer_city)
    splitted_customer_state = get_filter_by_customer_state.split(",")
    splitted_customer_city = get_filter_by_customer_city.split(",")
    cust_count = 0

    list1 =[]
    filtered_cust_list =[]

    customers = GreenBillUser.objects.filter(c_state__in=splitted_customer_state)
    for i in customers:
        print(i.c_area)
        if i.c_city:

            if i.c_city in splitted_customer_city:

                cust_count = cust_count + 1
                    
    
    list1.append({
        "customer_count": cust_count
    })

    for x in list1:
        if x['customer_count'] not in filtered_cust_list:
            filtered_cust_list.append(x['customer_count'])
    
    return JsonResponse({"data":cust_count})

def get_customers_by_state(request):
    get_filter_by_customer_state = request.POST['get_filter_by_customer_state']
    splitted_customer_state = get_filter_by_customer_state.split(",")

    customers = GreenBillUser.objects.filter(c_state__in=splitted_customer_state).count()

    return JsonResponse({"data":customers})


def get_customers_by_area(request):
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
                if i.c_city:
                    if i.c_city in splitted_customer_city:
                        if get_filter_by_customer_area:
                            if i.c_area in splitted_customer_area:
                                cust_count = cust_count + 1
                        else:
                            cust_count = cust_count + 1
            else:
                cust_count = cust_count + 1
    
    list1.append({
        "customer_count": cust_count
    })

    for x in list1:
        if x['customer_count'] not in filtered_cust_list:
            filtered_cust_list.append(x['customer_count'])
    
    return JsonResponse({"data":filtered_cust_list})


def get_merchants_by_area(request):
    get_filter_by_merchant_state = request.POST.get('get_filter_by_merchant_state')
    get_filter_by_merchant_city = request.POST.get('get_filter_by_merchant_city')
    get_filter_by_merchant_area = request.POST.get('get_filter_by_merchant_area')
    get_filter_by_business_category = request.POST['get_filter_by_business_category']

    if get_filter_by_merchant_state:
        splitted_merchant_state = get_filter_by_merchant_state.split(",")

    if get_filter_by_merchant_city:    
        splitted_merchant_city = get_filter_by_merchant_city.split(",")

    if get_filter_by_merchant_area:
        splitted_merchant_area = get_filter_by_merchant_area.split(",")

    splitted_business_category = get_filter_by_business_category.split(",")
    cust_count = 0

    list1 =[]
    filtered_cust_list =[]

    if get_filter_by_merchant_state:

        merchants = MerchantProfile.objects.filter(m_state__in=splitted_merchant_state)

        for i in merchants:
            if i.m_business_category:
                if str(i.m_business_category.id) in splitted_business_category:
                    if i.m_city != '' and i.m_area != '':
                        if get_filter_by_merchant_city:
                            if i.m_city in splitted_merchant_city:
                                if get_filter_by_merchant_area:
                                    if i.m_area in splitted_merchant_area:
                                        cust_count = cust_count + 1
                                else:
                                    cust_count = cust_count + 1
                        else:
                            cust_count = cust_count + 1
                    
    
    list1.append({
        "merchant_count": cust_count
    })


    for x in list1:
        if x['merchant_count'] not in filtered_cust_list:
            filtered_cust_list.append(x['merchant_count'])
    
    return JsonResponse({"data":filtered_cust_list})

def get_all_merchants_by_state(request):
    get_filter_by_merchant_state = request.POST['get_filter_by_merchant_state']
    business_category_value = request.POST['business_category_value']
    splitted_merchant_state = get_filter_by_merchant_state.split(",")
    splitted_business_category = business_category_value.split(",")

    merchants = MerchantProfile.objects.filter(m_state__in=splitted_merchant_state)

    count = 0
    for i in merchants:
        if i.m_business_category:
            if str(i.m_business_category.id) in splitted_business_category:
                count = count + 1
    return JsonResponse({"data":count})


def get_merchant_cost_by_state(request):
    get_filter_by_merchant_state = request.POST['get_filter_by_merchant_state']
    splitted_merchant_state = get_filter_by_merchant_state.split(",")
    business_category_value = request.POST['business_category_value']
    splitted_business_category = business_category_value.split(",")

    merchants = MerchantProfile.objects.filter(m_state__in=splitted_merchant_state)
    count = 0
    for i in merchants:
        if i.m_business_category:
            if str(i.m_business_category.id) in splitted_business_category:
                count = count + 1

    if PromotionsAmount.objects.all():
        amount = PromotionsAmount.objects.latest('id')
        offer_amount = amount.offer_amount
    else:
        offer_amount = 0
    
    total_cost1 = float(count) * float(offer_amount)

    total_cost = "{:.2f}".format(total_cost1)

    return JsonResponse({"data":total_cost})

  


def get_customers_cost_by_area(request):
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
        amount = PromotionsAmount.objects.latest('id')
        offer_amount = amount.offer_amount
    else:
        offer_amount = 0
    
    total_cost1 = float(cust_count) * float(offer_amount)

    total_cost = "{:.2f}".format(total_cost1)
    
    list1.append({
        "customer_total_cost": total_cost
    })

    for x in list1:
        if x['customer_total_cost'] not in filtered_cust_list:
            filtered_cust_list.append(x['customer_total_cost'])
    
    return JsonResponse({"data":filtered_cust_list})

def get_customers_cost_by_state(request):
    get_filter_by_customer_state = request.POST['get_filter_by_customer_state']
    get_filter_by_customer_state = request.POST['get_filter_by_customer_state']
    splitted_customer_state = get_filter_by_customer_state.split(",")

    customers = GreenBillUser.objects.filter(c_state__in=splitted_customer_state).count()

    if PromotionsAmount.objects.all():
        amount = PromotionsAmount.objects.latest('id')
        offer_amount = amount.offer_amount
    else:
        offer_amount = 0
    
    total_cost1 = float(customers) * float(offer_amount)

    total_cost = "{:.2f}".format(total_cost1)

    return JsonResponse({"data":total_cost})

        
def get_merchants_cost_by_area(request):
    get_filter_by_merchant_state = request.POST.get('get_filter_by_merchant_state')
    get_filter_by_merchant_city = request.POST.get('get_filter_by_merchant_city')
    get_filter_by_merchant_area = request.POST.get('get_filter_by_merchant_area')
    get_filter_by_business_category = request.POST['get_filter_by_business_category']
   
    if get_filter_by_merchant_state:
        splitted_merchant_state = get_filter_by_merchant_state.split(",")

    if get_filter_by_merchant_city:
        splitted_merchant_city = get_filter_by_merchant_city.split(",")

    if get_filter_by_merchant_area:
        splitted_merchant_area = get_filter_by_merchant_area.split(",")

    splitted_business_category = get_filter_by_business_category.split(",")
    cust_count = 0

    list1 =[]
    filtered_cust_list =[]

    if get_filter_by_merchant_state:
        merchants = MerchantProfile.objects.filter(m_state__in=splitted_merchant_state)
        for i in merchants:
            if i.m_business_category:
                if str(i.m_business_category.id) in splitted_business_category:
                    if i.m_city != '' and i.m_area != '':
                        if get_filter_by_merchant_city:
                            if i.m_city in splitted_merchant_city:
                                if get_filter_by_merchant_area:
                                    if i.m_area in splitted_merchant_area:
                                        cust_count = cust_count + 1
                                else:
                                    cust_count = cust_count + 1
                        else:
                            cust_count = cust_count + 1
                         
    if PromotionsAmount.objects.all():
        amount = PromotionsAmount.objects.latest('id')
        offer_amount = amount.offer_amount
    else:
        offer_amount = 0
    
    total_cost1 = float(cust_count) * float(offer_amount)

    total_cost = "{:.2f}".format(total_cost1)

    list1.append({
        "customer_total_cost": total_cost
    })


    for x in list1:
        if x['customer_total_cost'] not in filtered_cust_list:
            filtered_cust_list.append(x['customer_total_cost'])
    
    return JsonResponse({"data":filtered_cust_list})


def GetPartnersCountByState(request):
    partner_state_value = request.POST.get('partner_state_value')
    partner_city_value = request.POST.get('partner_city_value')
    partner_area_value = request.POST.get('partner_area_value')

    if partner_state_value:
        partner_state_value_new = partner_state_value.split(",")

    if partner_city_value:
        partner_city_value_new = partner_city_value.split(",")

    if partner_area_value:
        partner_area_value_new = partner_area_value.split(",")
    cust_count = 0

    list1 =[]

    if partner_state_value:
        partners = PartnerProfile.objects.filter(p_state__in=partner_state_value_new)

        for i in partners:
            if partner_city_value:
                if i.p_city:
                    if i.p_city in partner_city_value_new:
                        if partner_area_value:
                            if i.p_area in partner_area_value_new:
                                cust_count = cust_count + 1
                        else:
                            cust_count = cust_count + 1
            else:
                cust_count = cust_count + 1
    

    
    return JsonResponse({"data":cust_count})

def GetPartnerCost(request):
    partner_state_value = request.POST.get('partner_state_value')
    partner_city_value = request.POST.get('partner_city_value')
    partner_area_value = request.POST.get('partner_area_value')

    if partner_state_value:
        partner_state_value_new = partner_state_value.split(",")

    if partner_city_value:
        partner_city_value_new = partner_city_value.split(",")

    if partner_area_value:
        partner_area_value_new = partner_area_value.split(",")
    cust_count = 0

    list1 =[]

    if partner_state_value:
        partners = PartnerProfile.objects.filter(p_state__in=partner_state_value_new)

        for i in partners:
            if partner_city_value:
                if i.p_city:
                    if i.p_city in partner_city_value_new:
                        if partner_area_value:
                            if i.p_area in partner_area_value_new:
                                cust_count = cust_count + 1
                        else:
                            cust_count = cust_count + 1
            else:
                cust_count = cust_count + 1

    if PromotionsAmount.objects.all():
        amount = PromotionsAmount.objects.latest('id')
        offer_amount = amount.offer_amount
    else:
        offer_amount = 0
    
    total_cost1 = float(cust_count) * float(offer_amount)

    total_cost = "{:.2f}".format(total_cost1)

    
    return JsonResponse({"data":total_cost})


