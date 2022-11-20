from django import forms
# from .forms import partnerforms
import sweetify
import sys
from django.contrib import messages #import messages
from django.shortcuts import render, redirect, get_object_or_404
from users.models import GreenBillUser, PartnerProfile, Partner_users
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django import template
from django.template import loader
from .forms import *
from merchant_setting.forms import MerchnatgeneralSettingForm
from authentication.forms import MerchantSignUpForm, MerchantSignUpOtherDetailsForm
from category_and_tags.models import business_category
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Subquery
from role.models import userrole 
import random
import string
from app.views import is_partner




# def partnerbusiness(request):
#     data = MerchantProfile.objects.all()
#     print(data)
#     return render(request, "partner/partner-merchant.html", {'data': data})



@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def deletePartnerBusiness(request, id):
    instance = PartnerProfile.objects.get(id=id)
    
    instance.delete()
    return JsonResponse({'success': True})



# @login_required(login_url="/partner-login/")
# @user_passes_test(is_partner, login_url="/partner-login/")
# def partnerbusiness(request):
#     if request.method == "POST":
#         form = partnerBusinessesForm(request.POST)
#         if form.is_valid():
#             user_id = request.user.id
            
#             m_business_name = form.cleaned_data.get("m_business_name")
#             m_business_category = form.cleaned_data.get("m_business_category")
#             m_city = form.cleaned_data.get("m_city")
#             m_district = form.cleaned_data.get("m_district")
#             m_state = form.cleaned_data.get("m_state")
#             m_pin_code = form.cleaned_data.get("m_pin_code")
#             m_area = form.cleaned_data.get("m_area")

#             MerchantProfile.objects.create(m_user_id = user_id, m_business_name = m_business_name, m_business_category = m_business_category, m_city = m_city, m_district = m_district, m_state = m_state, m_pin_code = m_pin_code, m_area = m_area)

#             sweetify.success(request, title="Success", icon='success', text='Business Stored Successfully !!!')
#             return redirect('/partner-business/')
#         else:
#             sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
#             return redirect('/partner-business/')
#     else:

#         form = merchantBusinessesForm()
        
#         merchant_users_object = Merchant_users.objects.get(user_id = request.user)

#         data = MerchantProfile.objects.filter(m_user_id = merchant_users_object.merchant_user_id.id)
#         context = {
#             'form': form,
#             'data': data,
#         }
#         if data:
#             return render(request, "partner/partner-merchant.html",context)
#         else:
#             data = ""
#             return render(request, "partner/partner-merchant.html",context)


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partnerbusiness(request):
    if request.method == "POST":
        
        form = PartnerBusinessForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            
            p_business_name = form.cleaned_data.get("p_business_name")
            p_business_category = form.cleaned_data.get("p_business_category")
            p_city = form.cleaned_data.get("p_city")
            p_district = form.cleaned_data.get("p_district")
            p_state = form.cleaned_data.get("p_state")
            p_pin_code = form.cleaned_data.get("p_pin_code")
            p_area = form.cleaned_data.get("p_area")
            p_landline_number = form.cleaned_data.get("p_landline_number")
            p_company_email = form.cleaned_data.get("p_company_email")

            PartnerProfile.objects.create(p_company_email = p_company_email, p_landline_number = p_landline_number, p_user_id = user_id, p_business_name = p_business_name, p_business_category = p_business_category, p_city = p_city, p_district = p_district, p_state = p_state, p_pin_code = p_pin_code, p_area = p_area)

            sweetify.success(request, title="Success", icon='success', text='Business Stored Successfully !!!')
            return redirect('/partner-business/')
        else:
            sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
            return redirect('/partner-business/')
    else:

        form = PartnerBusinessForm()
        partner_users_object = Partner_users.objects.get(user_id = request.user)

        data = PartnerProfile.objects.filter(p_user_id = partner_users_object.partner_user_id.id).order_by('-id')
        context = {
            'form': form,
            'data': data,
            # 'merchantNavClass': "active", 
            # "SettingNavclass": 'active',
            # "settingsCollapseShow": "show",
            
        }
        if data:
            return render(request, "partner/partner-merchant.html",context)
        else:
            data = ""
            return render(request, "partner/partner-merchant.html",context)

