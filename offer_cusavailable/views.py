from django import forms
from django.shortcuts import render
from .models import availmodels
from .forms import availforms
from offers.models import OfferModel
from users.models import *
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
import time

# Create your views here.

# def availview(request):
#     if request.method == "POST":

#         lover_price = request.POST['lover_price']

#     return render(request, "customer/offer_cusavailable/avail.html", context)




# def availview(request):
#     if request.method == "POST":
#         offer_business_category = request.POST['offer_business_category']
#         if request.POST['offer_business_category'] == "All":
#             data_offer = OfferModel.objects.all().order_by("-id")
#         else:
#             data_offer = OfferModel.objects.filter(offer_business_category=offer_business_category)
#     else:
#         data_offer = OfferModel.objects.all().order_by("-id")
        
#     merchant_user_object = Merchant_users.objects.get(user_id = request.user)

#     merchant_object = merchant_user_object.merchant_user_id

#     merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
#     merchant_users_object = Merchant_users.objects.get(user_id = request.user)
#     form = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)
#     print(data_offer)
#     print(form)
#     context = {
#         "data_offer" : data_offer,
#         "form" : form,
#         'OffersNavclass': "active",
#     }
#     return render(request, "customer/offer_cusavailable/customer-offer.html", context)




# def availview(request):
#     customer_data_object = GreenBillUser.objects.get(mobile_no=request.user)
#     customer_state = customer_data_object.c_state
#     customer_city = customer_data_object.c_city
#     customer_area = customer_data_object.c_area
#     if request.method == "POST":
#         offer_business_category = request.POST['offer_business_category']
#         if request.POST['offer_business_category'] == "All":
#             data_offer = OfferModel.objects.all().order_by("-id")
#             offer_new=[]
#             for cust_offer_data in data_offer:
#                 if cust_offer_data.customer_city:
#                     if customer_area in cust_offer_data.customer_city:
#                         offer_new.append(cust_offer_data)
#         else:
#             data_offer = OfferModel.objects.filter(offer_business_category=offer_business_category)
#             offer_new=[]
#             for cust_offer_data in data_offer:
#                 if cust_offer_data.customer_city:
#                     if customer_area in cust_offer_data.customer_city:
#                         offer_new.append(cust_offer_data)
#     else:
#         data_offer = OfferModel.objects.all().order_by("-id")
#         offer_new=[]
#         today = date.today()
#         print('today',today)

#         for cust_offer_data in data_offer:
#             if cust_offer_data.valid_through >= today:
#                 if cust_offer_data.customer_state:
#                     if customer_state in cust_offer_data.customer_state:
#                         if cust_offer_data.customer_city:
#                             if customer_city in cust_offer_data.customer_city:
#                                 if cust_offer_data.customer_area:
#                                     if customer_area in cust_offer_data.customer_area:
#                                         offer_new.append(cust_offer_data)
                
           
#     context = {
#         "data_offer" : offer_new,
#         'OffersNavclass': "active",
#     }
#     return render(request, "customer/offer_cusavailable/customer-offer.html", context)

def availview(request):
    customer_data_object = GreenBillUser.objects.get(mobile_no=request.user)
    customer_state = customer_data_object.c_state
    customer_city = customer_data_object.c_city
    customer_area = customer_data_object.c_area
    
    data_offer = OfferModel.objects.filter(Offer_type = "Customer", status = "1").order_by("-id")

    offer_new=[]
    today = date.today()

    for cust_offer_data in data_offer:
        if cust_offer_data.valid_through >= today:

            if cust_offer_data.customer_state:
                if customer_state in cust_offer_data.customer_state:
                    if cust_offer_data.customer_city:
                        if customer_city in cust_offer_data.customer_city:
                            if cust_offer_data.customer_area:
                                if customer_area in cust_offer_data.customer_area:
                                    offer_new.append(cust_offer_data)
                            else:
                                offer_new.append(cust_offer_data)
                    else:
                        offer_new.append(cust_offer_data)
                
           
    context = {
        "data_offer" : offer_new,
        'OffersNavclass': "active",
    }
    return render(request, "customer/offer_cusavailable/customer-offer.html", context)



def view_offer_record(request, id):
    data = []

    base_url = "http://157.230.228.250/"

   
    data_offer = OfferModel.objects.filter(id = id)
    object = OfferModel.objects.get(id=id)
    object.cout = object.cout + 1
    object.save()
    print(data_offer)
    context = {
        "data_offer" : data_offer,
        'OffersNavclass': "active",
    }
    return render(request, "customer/offer_cusavailable/view-offer-record.html", context)
    # return redirect('https://www.google.com/')

def Number_of_views(request):
    if request.method == "POST":
        id = request.POST["offers_id"]
        print(id)
        object = OfferModel.objects.get(id=id)
        object.cout = object.cout + 1
        object.save()
    return redirect(availview)

