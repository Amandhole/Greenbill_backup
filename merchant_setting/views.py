import os
import random
import sweetify

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from django.contrib.auth import update_session_auth_hash
from .forms import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import MerchantProfile
from django.conf import settings
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import get_connection, send_mail, BadHeaderError
from users.models import GreenBillUser, UserProfileImage, Merchant_users
from category_and_tags.models import business_category
from role.models import *
from merchant_role.models import merchant_role, merchant_userrole
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff
from parking_lot_apis.models import ParkingLotPass
from merchant_info.views import *
import json
import os
from io import BytesIO
from django.shortcuts import render
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse

from petrol_pump_apis.models import SavePetrolPumpBill
from parking_lot_apis.models import SaveParkingLotBill

from datetime import datetime

from merchant_role.models import *
from merchant_stamp.models import merchantusagestamp
from owner_stamp.models import *
from django.views.decorators.csrf import csrf_exempt
# SMS
import requests
import time
import pyshorteners

from super_admin_settings.models import notification_settings
from merchant_promotion.models import bulkMailSmsMerchantCustomerModel, smsHeaderModel, templateContentModel
from my_subscription.models import *

from django.db.models import Q

from authentication.models import *

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchantSoftwareInstallationSteps(request):
    return render(request, "merchant/merchant-software-installation-steps.html")


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def select_payment_options(request):
    return render(request, 'merchant/merchant-select-payment-option.html')

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def delete_bills_by_days(request):
    if request.method == "POST":
        delete_days_merchant= request.POST['deletedaysmerchant']
        delete_days_customer= request.POST['deletedayscustomer']
        delete_from = request.POST.getlist("deletedBills")
        # delete_list =[]
        # print(delete_from)
        # if delete_from =="merchant":
        #     delete_from = "merchant"
        #     # delete_list.append(delete_from)
        #     # sweetify.success(request, title="Success1", icon= "success", text="Done")
        # if delete_from == "customer":
        #     delete_from = 'customer'
        #     # delete_list.append(delete_from)
        #  # sweetify.success(request, title="Success2", icon= "success", text="Done")
        # if delete_from == 'both':
        #     delete_from = 'both'
        #     # delete_list.append(delete_from)
        mer = 0
        cust = 0
        for i in delete_from:
            if i =="merchant":
                mer= "1"
            if i =="customer":
                cust ="1"
            if i == "both":
                cust=0
                mer =0
        print("****************")
        print(delete_from,delete_days_merchant,delete_days_customer,cust,mer)
            # sweetify.success(request, title=delete_from, icon= "success", text="Done")
        avaible_user = Deleted_Bills_By_Days_setting.objects.filter(m_user = request.user)

        print(avaible_user)

        if len(list(avaible_user))==0:
            Deleted_Bills_By_Days_setting.objects.create(m_user= request.user,delete_days_merchant=delete_days_merchant,delete_days_customer=delete_days_customer,
            delete_from_merchant=mer,delete_from_customer=cust)
        else:
            avaible_user.update(delete_days_merchant=delete_days_merchant,delete_days_customer=delete_days_customer,
            delete_from_merchant=mer,delete_from_customer=cust)

        print(Deleted_Bills_By_Days_setting)
        sweetify.success(request, title="Success", icon= "success", text="Done")
    try:
        datas = Deleted_Bills_By_Days_setting.objects.filter(m_user = request.user).last()
        data = datas.delete_days_merchant
        data2 = datas.delete_days_customer
        panel = [datas.delete_from_merchant,datas.delete_from_customer]
        print(panel)
        print(datas.date_entered)
        print(data,data2,datas)
    except:
        data = "0"
        data2 = "0"
        panel = ['0','0']
    context = {
        "data" : data,
        "data2":data2,
        "panel": panel, 
    }
    return render(request, 'merchant/delete_old_bills.html', context)


# @login_required(login_url="/merchant-login/")
# @user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
# def delete_bills_by_days(request):
	
# 	if request.method == "POST":
# 		delete_days= request.POST['deletedays']
# 		delete_from = request.POST["deletedBills"]
#         # print("****************")
#         print(delete_from)
# 		if delete_from =="merchant":
# 			delete_from = "merchant"
#             # sweetify.success(request, title="Success1", icon= "success", text="Done")
# 		elif delete_from == "customer":
# 			delete_from = 'customer'
#             # sweetify.success(request, title="Success2", icon= "success", text="Done")
# 		elif delete_from == 'both':
#             delete_from = 'both'

#         print("****************")
#         print(delete_from)
#         # sweetify.success(request, title=delete_from, icon= "success", text="Done")
# 		Deleted_Bills_By_Days_setting.objects.update_or_create(m_user= request.user,defaults={"deleted_days":delete_days, "deleted_from": delete_from})
# 		sweetify.success(request, title="Success", icon= "success", text="Done")
# 	try:
# 		datas = Deleted_Bills_By_Days_setting.objects.filter(m_user = request.user).last()
# 		data = datas.deleted_days
# 		panel = datas.deleted_from     
# 	except:
# 		data = "0"
# 		panel = 'merchant'
# 	context = {
#         "data" : data,
#         "panel": panel, 
#     }
# 	return render(request, 'merchant/delete_old_bills.html', context)
    	
	 




@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_general_setting(request):

    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

    merchant_objects_id = GreenBillUser.objects.get(mobile_no = request.user)

    if request.method == "POST":

        # merchant_stamp_color = request.POST['stamp_color']
        # print('nilesh',merchant_stamp_color)

        try:
            merchant_select_stamp = merchantusagestamp.objects.filter(merchant_user_id=request.user, merchant_business_id = merchant_general_setting.id).last()

            stamp_id = merchant_select_stamp.merchant_stamp_id_one

            merchant_stamp_color = request.POST['stamp_color']

            
        except:
            stamp_id = ''
            merchant_stamp_color = ''

        try:

            latest_stamp_record = wstampmodels.objects.filter(id=stamp_id).update(option_color = merchant_stamp_color)
        except:
            ''

        # print('stamp_id',stamp_id)

        # latest_stamp_record = wstampmodels.objects.filter(id=stamp_id)

        form = MerchnatgeneralSettingForm(request.POST, request.FILES)

        print(form.errors)
        print("AA")

        if form.is_valid():
            print("BB")   
            merchant_setting_id = request.POST["merchant_setting_id"]
            business_name = form.cleaned_data.get("business_name")
            business_category_temp = request.POST["merchant_business_category"]
            pin_code = form.cleaned_data.get("pin_code")

            cust_city = form.cleaned_data.get("city")
            city = cust_city.capitalize()

            cust_area = form.cleaned_data.get("area")
            area = cust_area.capitalize()

            cust_district = form.cleaned_data.get("district")
            district = cust_district.capitalize()

            cust_state = form.cleaned_data.get("state")
            state = cust_state.capitalize()
            
            address = form.cleaned_data.get("address")
            landline_number = form.cleaned_data.get("landline_number")
            alternate_mobile_number = form.cleaned_data.get("alternate_mobile_number")
            company_email = form.cleaned_data.get("company_email")
            alternate_email = form.cleaned_data.get("alternate_email")
            pan_number = form.cleaned_data.get("pan_number")
            print(pan_number)
            aadhaar = form.cleaned_data.get('aadhaar')
            gstin = form.cleaned_data.get("gstin")
            GSTIN_certificate = form.cleaned_data.get("GSTIN_certificate")
            
            cin = form.cleaned_data.get("cin")
            CIN_certificate = form.cleaned_data.get("CIN_certificate")
            profile_image = form.cleaned_data.get("profile_image")
            business_logo = form.cleaned_data.get("business_logo")
            business_stamp = form.cleaned_data.get("business_stamp")
            digital_signature = form.cleaned_data.get("digital_signature")
            bank_account_number = form.cleaned_data.get("bank_account_number")
            bank_IFSC_code = form.cleaned_data.get("bank_IFSC_code")
            bank_name = form.cleaned_data.get("bank_name")
            bank_branch = form.cleaned_data.get("bank_branch")
            tin_vat_number = form.cleaned_data.get("tin_vat_number")
            cancel_bank_cheque_photo = form.cleaned_data.get("cancelled_cheque_certificate")
            
            other_document1 = form.cleaned_data.get("other_document1")
            other_document2 = form.cleaned_data.get("other_document2")
            udyog_adhar_certificate_file = form.cleaned_data.get("udyog_adhar_certificate")
            address_proof = form.cleaned_data.get("address_proof")
            m_bank_account_entry = form.cleaned_data.get("m_bank_account_entry")
            m_address_bank_account = form.cleaned_data.get("m_address_bank_account")
            schedule_pdf_upload = form.cleaned_data.get("schedule_pdf_upload")
            print('aaaa',schedule_pdf_upload)
            bank_account_entity_m1 = form.cleaned_data.get("bank_account_entity_m1")
            bank_account_entity_adress2 = form.cleaned_data.get("bank_account_entity_adress2")
            m_website_url = form.cleaned_data.get("m_website_url")
            m_business_name_for_billing = form.cleaned_data.get("m_business_name_for_billing")
            m_billing_address = form.cleaned_data.get("m_billing_address")
            m_billing_email = form.cleaned_data.get("m_billing_email")
            m_billing_phone = form.cleaned_data.get("m_billing_phone")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            m_company_registration_certificate = form.cleaned_data.get("company_registration_certificate")
            
            GreenBillUser.objects.filter(mobile_no = merchant_general_setting.m_user).update(first_name = first_name, last_name = last_name)
            
            business_category_object = business_category.objects.get(id=business_category_temp)
            
            MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={'m_billing_address': m_billing_address, 'm_billing_email': m_billing_email, 'm_billing_phone': m_billing_phone, 'm_business_name': business_name, 'm_website_url': m_website_url,
                'm_business_category': business_category_object, 'm_pin_code': pin_code, 'm_city': city, 'm_area': area ,
                'm_district': district, 'm_state': state, 'm_address': address, 'm_business_name_for_billing': m_business_name_for_billing, 'm_landline_number': landline_number, })
                # 'm_alternate_mobile_number': alternate_mobile_number, 'm_company_email': company_email, 'm_alternate_email' : alternate_email,
                # 'm_pan_number': pan_number, 'm_gstin': gstin, 'm_cin': cin, 'm_bank_account_number': bank_account_number, 
                # 'm_bank_IFSC_code': bank_IFSC_code, 'm_bank_name' : bank_name, 'm_bank_branch' : bank_branch,'m_vat_tin_number':tin_vat_number,
                # 'm_aadhaar_number':aadhaar,"m_other_document1":other_document1,"m_other_document2":other_document2})
          
            for all in MerchantProfile.objects.filter(m_user=request.user,m_business_name=business_name):
                
                print(all, all.id)

                MerchantProfile.objects.update_or_create(id = all.id, defaults={ 
                'm_alternate_mobile_number': alternate_mobile_number, 'm_company_email': company_email, 'm_alternate_email' : alternate_email,
                'm_pan_number': pan_number, 'm_gstin': gstin, 'm_cin': cin, 'm_bank_account_number': bank_account_number, 
                'm_bank_IFSC_code': bank_IFSC_code, 'm_bank_name' : bank_name, 'm_bank_branch' : bank_branch, 'Entity_Account_m': bank_account_entity_m1, 'Entity_Bank_Account_m': bank_account_entity_adress2, 'm_vat_tin_number':tin_vat_number,
                'm_aadhaar_number':aadhaar,"m_other_document2":other_document2})

            if profile_image:
                UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "m_profile_image" : profile_image })

            if m_company_registration_certificate:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "company_registration_certificate" : m_company_registration_certificate })

            
            if GSTIN_certificate:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_GSTIN_certificate" : GSTIN_certificate })

            if CIN_certificate:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_CIN_certificate" : CIN_certificate })
            
            if business_logo:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_business_logo" : business_logo })

            if business_stamp:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_business_stamp" : business_stamp })

            if digital_signature:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_digital_signature" : digital_signature })

            if cancel_bank_cheque_photo:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_cancel_bank_cheque_photo" : cancel_bank_cheque_photo })

            if udyog_adhar_certificate_file:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_other_document_certificate1" : udyog_adhar_certificate_file })
            
            if address_proof:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "address_proof" : address_proof })

            if m_bank_account_entry:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_bank_account_entry" : m_bank_account_entry })

            if m_company_registration_certificate:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_company_registration_certificate" : m_company_registration_certificate })

            if m_address_bank_account:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_address_bank_account" : m_address_bank_account })
                
            if schedule_pdf_upload:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "schedule_pdf_upload" : schedule_pdf_upload })

            sweetify.success(request, title="Success", icon='success',
                             text='Business Settings Stored Successfully !!!', timer=1000)

            return redirect('/merchant-general-setting/')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!', timer=1000)
            return redirect('/merchant-general-setting/')
    else:
        
        merchnat_business_category = business_category.objects.all()

       
        merchant_select_stamp = merchantusagestamp.objects.filter(merchant_user_id=request.user, merchant_business_id = merchant_general_setting.id).last()

        try:
            stamp_id = merchant_select_stamp.merchant_stamp_id_one
        except:
            stamp_id = ''
        try:
            latest_stamp_record = wstampmodels.objects.filter(id=stamp_id)
        except:
            latest_stamp_record = ''
        try:
            selected_stamp_id = wstampmodels.objects.get(id=stamp_id)

            stamp_design = selected_stamp_id.option_color
        except:
            stamp_design = ''

        # name = latest_stamp_record[0].stamp_name
        
        form = MerchnatgeneralSettingForm()
        print('aa',stamp_design,'bb')
        States = StateCityData.objects.values('state').distinct().order_by('state')
        print(States)
        context = {
            'latest_stamp_record': latest_stamp_record,
            'States': States,
            'form' : form,
            'design' : stamp_design,
            'merchant_general_setting': merchant_general_setting, 
            'merchnat_business_category': merchnat_business_category, 
            'merchant_objects_id': merchant_objects_id,
            "SettingNavclass": 'active',
            "settingsCollapseShow": "show",
            "GeneralSettingsNavclass": "active"
        }
            
        return render(request, "merchant/merchant_general_setting.html", context)


def download_merchant_schedule_file(request):
    path = 'merchant_schedule_file/schedule.docx'
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="merchant_schedule_file/schedule.docx")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

     
# @login_required(login_url="/merchant-login/")
# @user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
# def merchant_general_setting(request):

#     if request.method == "POST":
        
#         form = MerchnatgeneralSettingForm(request.POST, request.FILES)

#         print(form.errors)

#         if form.is_valid():
            
#             merchant_setting_id = request.POST["merchant_setting_id"]
#             business_name = form.cleaned_data.get("business_name")
#             business_category_temp = request.POST["merchant_business_category"]
#             pin_code = form.cleaned_data.get("pin_code")
#             city = form.cleaned_data.get("city")
#             area = form.cleaned_data.get("area")
#             district = form.cleaned_data.get("district")
#             state = form.cleaned_data.get("state")
#             address = form.cleaned_data.get("address")
#             landline_number = form.cleaned_data.get("landline_number")
#             alternate_mobile_number = form.cleaned_data.get("alternate_mobile_number")
#             company_email = form.cleaned_data.get("company_email")
#             alternate_email = form.cleaned_data.get("alternate_email")
#             pan_number = form.cleaned_data.get("pan_number")
#             gstin = form.cleaned_data.get("gstin")
#             GSTIN_certificate = form.cleaned_data.get("GSTIN_certificate")
#             cin = form.cleaned_data.get("cin")
#             CIN_certificate = form.cleaned_data.get("CIN_certificate")
#             profile_image = form.cleaned_data.get("profile_image")
#             business_logo = form.cleaned_data.get("business_logo")
#             business_stamp = form.cleaned_data.get("business_stamp")
#             digital_signature = form.cleaned_data.get("digital_signature")
#             bank_account_number = form.cleaned_data.get("bank_account_number")
#             bank_IFSC_code = form.cleaned_data.get("bank_IFSC_code")
#             bank_name = form.cleaned_data.get("bank_name")
#             bank_branch = form.cleaned_data.get("bank_branch")
#             tin_vat_number = form.cleaned_data.get("tin_vat_number")
#             cancel_bank_cheque_photo = form.cleaned_data.get("cancel_bank_cheque_photo")
#             other_document1 = form.cleaned_data.get("other_document1")
#             other_document2 = form.cleaned_data.get("other_document2")
#             other_document_certificate1 = form.cleaned_data.get("other_document_certificate1")
#             other_document_certificate2 = form.cleaned_data.get("other_document_certificate2")
            

#             business_category_object = business_category.objects.get(id=business_category_temp)

#             MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={'m_business_name': business_name, 'm_business_category': business_category_object, 'm_pin_code': pin_code, 'm_city': city, 'm_area': area ,'m_district': district, 'm_state': state, 'm_address': address, 'm_landline_number': landline_number, 'm_alternate_mobile_number': alternate_mobile_number, 'm_company_email': company_email, 'm_alternate_email' : alternate_email, 'm_pan_number': pan_number, 'm_gstin': gstin, 'm_cin': cin, 'm_bank_account_number': bank_account_number, 'm_bank_IFSC_code': bank_IFSC_code, 'm_bank_name' : bank_name, 'm_bank_branch' : bank_branch,'m_vat_tin_number':tin_vat_number,"m_other_document1":other_document1,"m_other_document2":other_document2})

#             if profile_image:
#                 UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "m_profile_image" : profile_image })
            
#             if GSTIN_certificate:
#                 MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_GSTIN_certificate" : GSTIN_certificate })

#             if CIN_certificate:
#                 MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_CIN_certificate" : CIN_certificate })
            
#             if business_logo:
#                 MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_business_logo" : business_logo })

#             if business_stamp:
#                 MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_business_stamp" : business_stamp })

#             if digital_signature:
#                 MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_digital_signature" : digital_signature })

#             if cancel_bank_cheque_photo:
#                 MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_cancel_bank_cheque_photo" : cancel_bank_cheque_photo })

#             if other_document_certificate1:
#                 MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_other_document_certificate1" : other_document_certificate1 })
            
#             if other_document_certificate2:
#                 MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_other_document_certificate2" : other_document_certificate2 })
            
#             sweetify.success(request, title="Success", icon='success',
#                              text='Business Settings Stored Successfully !!!', timer=1000)

#             return redirect('/merchant-general-setting/')
#         else:
#             sweetify.error(request, title="error",
#                            icon='error', text='Failed !!!', timer=1000)
#             return redirect('/merchant-general-setting/')
#     else:
        
#         merchant_users_object = Merchant_users.objects.get(user_id = request.user)

#         merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)
#         print(merchant_general_setting)
#         merchnat_business_category = business_category.objects.all()
        
#         form = MerchnatgeneralSettingForm()

#         context = {
#             'form' : form,
#             'merchant_general_setting': merchant_general_setting, 
#             'merchnat_business_category': merchnat_business_category, 
#             "SettingNavclass": 'active',
#             "settingsCollapseShow": "show",
#             "GeneralSettingsNavclass": "active"
#         }
            
#         return render(request, "merchant/merchant_general_setting.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_general_setting_new(request):

    if request.method == "POST":
        
        form = MerchnatgeneralSettingForm(request.POST, request.FILES)

        if form.is_valid():
            
            merchant_setting_id = request.POST["merchant_setting_id"]
            business_name = form.cleaned_data.get("business_name")
            business_category_temp = request.POST["merchant_business_category"]
            pin_code = form.cleaned_data.get("pin_code")
            city = form.cleaned_data.get("city")
            area = form.cleaned_data.get("area")
            district = form.cleaned_data.get("district")
            state = form.cleaned_data.get("state")
            address = form.cleaned_data.get("address")
            landline_number = form.cleaned_data.get("landline_number")
            alternate_mobile_number = form.cleaned_data.get("alternate_mobile_number")
            company_email = form.cleaned_data.get("company_email")
            alternate_email = form.cleaned_data.get("alternate_email")
            pan_number = form.cleaned_data.get("pan_number")
            gstin = form.cleaned_data.get("gstin")
            GSTIN_certificate = form.cleaned_data.get("GSTIN_certificate")
            cin = form.cleaned_data.get("cin")
            CIN_certificate = form.cleaned_data.get("CIN_certificate")
            profile_image = form.cleaned_data.get("profile_image")
            business_logo = form.cleaned_data.get("business_logo")
            business_stamp = form.cleaned_data.get("business_stamp")
            digital_signature = form.cleaned_data.get("digital_signature")
            bank_account_number = form.cleaned_data.get("bank_account_number")
            bank_IFSC_code = form.cleaned_data.get("bank_IFSC_code")
            bank_name = form.cleaned_data.get("bank_name")
            bank_branch = form.cleaned_data.get("bank_branch")
            tin_vat_number = form.cleaned_data.get("tin_vat_number")
            cancel_bank_cheque_photo = form.cleaned_data.get("cancel_bank_cheque_photo")
            other_document1 = form.cleaned_data.get("other_document1")
            other_document2 = form.cleaned_data.get("other_document2")
            other_document_certificate1 = form.cleaned_data.get("other_document_certificate1")
            other_document_certificate2 = form.cleaned_data.get("other_document_certificate2")
            

            business_category_object = business_category.objects.get(id=business_category_temp)

            MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={'m_business_name': business_name, 'm_business_category': business_category_object, 'm_pin_code': pin_code, 'm_city': city, 'm_area': area ,'m_district': district, 'm_state': state, 'm_address': address, 'm_landline_number': landline_number, 'm_alternate_mobile_number': alternate_mobile_number, 'm_company_email': company_email, 'm_alternate_email' : alternate_email, 'm_pan_number': pan_number, 'm_gstin': gstin, 'm_cin': cin, 'm_bank_account_number': bank_account_number, 'm_bank_IFSC_code': bank_IFSC_code, 'm_bank_name' : bank_name, 'm_bank_branch' : bank_branch,'m_vat_tin_number':tin_vat_number,"m_other_document1":other_document1,"m_other_document2":other_document2})

            if profile_image:
                UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "m_profile_image" : profile_image })
            
            if GSTIN_certificate:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_GSTIN_certificate" : GSTIN_certificate })

            if CIN_certificate:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_CIN_certificate" : CIN_certificate })
            
            if business_logo:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_business_logo" : business_logo })

            if business_stamp:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_business_stamp" : business_stamp })

            if digital_signature:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_digital_signature" : digital_signature })

            if cancel_bank_cheque_photo:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_cancel_bank_cheque_photo" : cancel_bank_cheque_photo })

            if other_document_certificate1:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_other_document_certificate1" : other_document_certificate1 })
            
            if other_document_certificate2:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_other_document_certificate2" : other_document_certificate2 })
            
            sweetify.success(request, title="Success", icon='success',
                             text='Business Settings Stored Successfully !!!', timer=1000)

            return redirect('/merchant-general-setting/')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!', timer=1000)
            return redirect('/merchant-general-setting/')
    else:
        
        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)
        print(merchant_general_setting)
        merchnat_business_category = business_category.objects.all()
        
        form = MerchnatgeneralSettingForm()

        context = {
            'form' : form,
            'merchant_general_setting': merchant_general_setting, 
            'merchnat_business_category': merchnat_business_category, 
            "SettingNavclass": 'active',
            "settingsCollapseShow": "show",
            "GeneralSettingsNavclass": "active"
        }
            
        return render(request, "merchant/merchant_general_setting1.html", context)
# Users

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_register_user_view(request):

    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_users_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    qs = merchant_role.objects.filter(merchant_id = merchant_users_object.merchant_user_id, merchant_business_id = merchant_business_id)

    qs1 = GreenBillUser.objects.all().filter(is_merchant_staff = "1")



    try:
        merchant_user_id = Merchant_users.objects.filter(user_id = request.user).values('merchant_user_id')[0]['merchant_user_id']

        merchant_user_id_object = GreenBillUser.objects.get(id=merchant_user_id)
        
        qs_temp = Merchant_users.objects.filter(merchant_user_id = merchant_user_id_object, m_business_id = merchant_business_id.id).order_by('-id')
        
        total_count = Merchant_users.objects.filter(merchant_user_id = merchant_user_id_object, m_business_id = merchant_business_id.id).count()
    except:
        qs_temp = ""

    startswith = str(merchant_business_id.id) + ','
    endswith = ','+ str(merchant_business_id.id)
    contains = ','+ str(merchant_business_id.id) + ','
    exact = str(merchant_business_id.id)

    try:
        check_subscription_available = merchant_subscriptions.objects.get(
            Q(merchant_id = merchant_object),
            Q(is_active = True),
            Q(business_ids__startswith = startswith) | 
            Q(business_ids__endswith = endswith) | 
            Q(business_ids__contains = contains) | 
            Q(business_ids__exact = exact)
        )
    except:
        check_subscription_available = ""

    # if check_subscription_available:
    #     for object1 in qs_temp:
    #         temp1 = GreenBillUser.objects.get(mobile_no=object.user_id)
    #         qs31 = merchant_userrole.objects.filter(user = temp1)
    #         for oject2 in qs31:
    #             qs4 = merchant_role.objects.filter(role_name= oject2.role, merchant_business_id = merchant_business_id)
    #             for oject3 in qs4:
    #                 role_name = oject3.role_name

    # else:


    # number_of_users = ''
    # if check_subscription_available:
        # if check_subscription_available.no_of_users:
        #     number_of_users = check_subscription_available.no_of_users

    user_data = []

    for object in qs_temp:
        temp = GreenBillUser.objects.get(mobile_no=object.user_id)
        
        qs3 = merchant_userrole.objects.filter(user = temp)
    
        for oject1 in qs3:
            object.user_id.role = oject1.id
            object.user_id.role_name = oject1.role
            
            qs4 = merchant_role.objects.filter(role_name= oject1.role, merchant_business_id = merchant_business_id)
            for oject2 in qs4:
                object.user_id.role_id = oject2.id

                assign_role_name = oject2.role_name

                if assign_role_name == 'Exe User':
                    user_data.append(temp)

    # print(user_data)
    if check_subscription_available:

        planforuser = 0

        if check_subscription_available.no_of_users:

            planforuser = check_subscription_available.no_of_users 

        avialable_exe_user = len(user_data)

        if int(planforuser) < int(avialable_exe_user + 1):

            for mobile_no in user_data:

                not_exist_user = GreenBillUser.objects.get(mobile_no=mobile_no).delete()

    else:
        for mobile_no in user_data:
            print(mobile_no)
            not_exist_user = GreenBillUser.objects.get(mobile_no=mobile_no).delete()


    context  = {
        "role_list": qs,
        "user_list": qs_temp,
        'MyTeamNavclass': 'active',
        "MyTeamCollapsShow": "show",
        "UserNavclass": "active",
        "total_count": total_count,
    }
    
    if request.method == 'POST': 
       
        form = CreateMerchantUserForm(request.POST)

        startswith = str(merchant_business_id.id) + ','
        endswith = ','+ str(merchant_business_id.id)
        contains = ','+ str(merchant_business_id.id) + ','
        exact = str(merchant_business_id.id)

        try:
            check_subscription_available = merchant_subscriptions.objects.get(
                Q(merchant_id = merchant_object),
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )
        except:
            check_subscription_available = ""

        number_of_users = ''
        if check_subscription_available:
            if check_subscription_available.no_of_users:
                number_of_users = check_subscription_available.no_of_users

        if form.is_valid():

            user_object = GreenBillUser.objects.filter(mobile_no = form.cleaned_data['mobile_no'])

            if GreenBillUser.objects.filter(mobile_no = form.cleaned_data['mobile_no']).exists():

                if user_object[0].is_customer and not user_object[0].is_staff and not user_object[0].is_merchant and not user_object[0].is_partner and not user_object[0].is_merchant_staff:

                    role_name_id = form.cleaned_data.get("role_name")

                    role1 = "Exe User"

                    merchant_role1 = merchant_userrole.objects.filter(role_id = role_name_id, role__role_name = role1)
                    
                    if merchant_role1:

                        if number_of_users:
                            
                            all_merchant_users = Merchant_users.objects.filter(merchant_user_id = merchant_user_id_object, m_business_id = merchant_business_id.id)
                        
                            number_of_exe_role = 0
                            
                            for user in all_merchant_users:
                                
                                temp1 = GreenBillUser.objects.get(mobile_no=user.user_id)
                                
                                role_data = merchant_userrole.objects.filter(user = temp1)
        
                                for oject1 in role_data:
                                    
                                    user.user_id.role = oject1.id
                                    
                                    user.user_id.role_name = oject1.role
                                    
                                    roles2 = merchant_role.objects.filter(role_name= oject1.role, merchant_business_id = merchant_business_id)
                                    
                                    for oject2 in roles2:
                                        
                                        role_name1 = oject2.role_name
                                        
                                        if role_name1 == 'Exe User':
                                            
                                            number_of_exe_role = number_of_exe_role + 1
                            
                            if int(number_of_exe_role + 1) < int(number_of_users):

                                temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
                    
                                user = GreenBillUser.objects.create_user(
                                    mobile_no = form.cleaned_data['mobile_no'],
                                    m_email = form.cleaned_data['email'],
                                    first_name = form.cleaned_data['first_name'],
                                    last_name = form.cleaned_data['last_name'],
                                    password = temp_password,
                                    is_merchant_staff = 1
                                )

                                merchant_user_id = Merchant_users.objects.filter(user_id = request.user).values('merchant_user_id')[0]['merchant_user_id']

                                merchant_user_id_object = GreenBillUser.objects.get(id=merchant_user_id)

                                merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_user_id, m_active_account = 1)
                                
                                Merchant_users.objects.create(user_id = user, merchant_user_id = merchant_user_id_object, raw_password= temp_password, m_business_id=merchant_general_setting.id, m_business_name= merchant_general_setting.m_business_name)
                                

                                role_id = form.cleaned_data.get("role_name")

                                merchant_userrole.objects.create(user = user, role_id = role_id)

                                name = form.cleaned_data['first_name']
                                email = form.cleaned_data['email']
                                mobile_no = form.cleaned_data['mobile_no']

                                mobile_no_str = str(merchant_user_id_object.mobile_no) + ',' + str(mobile_no)

                                ts = int(time.time())

                                notification_object = notification_settings.objects.get(id = 5)

                                if notification_object.send_sms:
                                    data_temp = {
                                            "keyword":"Team Login Credentials",
                                            "timeStamp":ts,
                                            "dataSet":
                                                [
                                                    {
                                                        "UNIQUE_ID":"GB-" + str(ts),
                                                        "MESSAGE":"Dear Green Bill user, here is the login credentials for your team. Username: " + mobile_no + " Password: "+ temp_password,
                                                        "OA":"GRBILL", 
                                                        "MSISDN": str(mobile_no_str), # Recipient's Mobile Number
                                                        "CHANNEL":"SMS",
                                                        "CAMPAIGN_NAME":"hind_user",
                                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                        "USER_NAME":"hind_hsi",
                                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                                        "DLT_CT_ID":"1007162098336084141", # Template Id
                                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                    }
                                                ]
                                            }

                                    url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                    response = requests.post(url, json = data_temp)

                                if notification_object.send_email:
                                    subject = 'Team Login Credentials'
                                    message = f'Dear Green Bill user, here is the login credentials for your team.\n Username: {mobile_no} \n Password: {temp_password}'
                                    email_from = settings.EMAIL_HOST_USER 
                                    recipient_list = [email, merchant_user_id_object.m_email] 
                                    send_mail( subject, message, email_from, recipient_list ) 
                                
                                return JsonResponse({'status':'success'})
                            else:
                                return JsonResponse({'status':'limited'})
                        else:
                            return JsonResponse({'status':'limited'})

                    else:

                        temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

                        GreenBilluser = GreenBillUser.objects.filter(
                            mobile_no = form.cleaned_data['mobile_no']).update(
                            email = form.cleaned_data['email'],
                            first_name = form.cleaned_data['first_name'],
                            last_name = form.cleaned_data['last_name'],
                            is_staff = 1
                        )

                        user = GreenBillUser.objects.get(mobile_no = form.cleaned_data['mobile_no'])

                        merchant_user_id = Merchant_users.objects.filter(user_id = request.user).values('merchant_user_id')[0]['merchant_user_id']

                        merchant_user_id_object = GreenBillUser.objects.get(id=merchant_user_id)

                        merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_user_id, m_active_account = 1)
                        
                        Merchant_users.objects.create(user_id = user, merchant_user_id = merchant_user_id_object, raw_password= temp_password, m_business_id=merchant_general_setting.id, m_business_name= merchant_general_setting.m_business_name)

                        role_id = form.cleaned_data.get("role_name")

                        merchant_userrole.objects.create(user = user, role_id = role_id)

                        name = form.cleaned_data['first_name']
                        email = form.cleaned_data['email']
                        mobile_no = form.cleaned_data['mobile_no']

                        mobile_no_str = str(merchant_user_id_object.mobile_no) + ',' + str(mobile_no)

                        ts = int(time.time())

                        notification_object = notification_settings.objects.get(id = 5)

                        if notification_object.send_sms:
                            data_temp = {
                                    "keyword":"Team Login Credentials",
                                    "timeStamp":ts,
                                    "dataSet":
                                        [
                                            {
                                                "UNIQUE_ID":"GB-" + str(ts),
                                                "MESSAGE":"Dear Green Bill user, here is the login credentials for your team. Username: " + mobile_no + " Password is same as their Customer Account ",
                                                "OA":"GRBILL", 
                                                "MSISDN": str(mobile_no_str), # Recipient's Mobile Number
                                                "CHANNEL":"SMS",
                                                "CAMPAIGN_NAME":"hind_user",
                                                "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                "USER_NAME":"hind_hsi",
                                                "DLT_TM_ID":"1001096933494158", # TM ID
                                                "DLT_CT_ID":"1007162098336084141", # Template Id
                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                            }
                                        ]
                                    }

                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                            response = requests.post(url, json = data_temp)

                        if notification_object.send_email:
                            subject = 'Team Login Credentials'
                            message = f'Dear Green Bill user, here is the login credentials for your team.\n Username: {mobile_no} \n Password is same as their Customer Account '
                            email_from = settings.EMAIL_HOST_USER 
                            recipient_list = [email, merchant_user_id_object.m_email] 
                            send_mail( subject, message, email_from, recipient_list ) 
                        
                        return JsonResponse({'status':'success'})

                else:
                    return JsonResponse({'status':'invalid'})
            else:

                role_name_id = form.cleaned_data.get("role_name")

                role1 = "Exe User"

                merchant_role1 = merchant_userrole.objects.filter(role_id = role_name_id, role__role_name = role1)
                
                if merchant_role1:

                    if number_of_users:
                        
                        all_merchant_users = Merchant_users.objects.filter(merchant_user_id = merchant_user_id_object, m_business_id = merchant_business_id.id)
                        
                        number_of_exe_role = 0
                        
                        for user in all_merchant_users:
                            
                            temp1 = GreenBillUser.objects.get(mobile_no=user.user_id)
                            
                            role_data = merchant_userrole.objects.filter(user = temp1)
    
                            for oject1 in role_data:
                                
                                user.user_id.role = oject1.id
                                
                                user.user_id.role_name = oject1.role
                                
                                roles2 = merchant_role.objects.filter(role_name= oject1.role, merchant_business_id = merchant_business_id)
                                
                                for oject2 in roles2:
                                    
                                    role_name1 = oject2.role_name
                                    
                                    if role_name1 == 'Exe User':
                                        
                                        number_of_exe_role = number_of_exe_role + 1

                        if int(number_of_exe_role + 1) < int(number_of_users):

                            temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
                
                            user = GreenBillUser.objects.create_user(
                                mobile_no = form.cleaned_data['mobile_no'],
                                m_email = form.cleaned_data['email'],
                                first_name = form.cleaned_data['first_name'],
                                last_name = form.cleaned_data['last_name'],
                                password = temp_password,
                                is_merchant_staff = 1
                            )

                            merchant_user_id = Merchant_users.objects.filter(user_id = request.user).values('merchant_user_id')[0]['merchant_user_id']

                            merchant_user_id_object = GreenBillUser.objects.get(id=merchant_user_id)

                            merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_user_id, m_active_account = 1)
                            
                            Merchant_users.objects.create(user_id = user, merchant_user_id = merchant_user_id_object, raw_password= temp_password, m_business_id=merchant_general_setting.id, m_business_name= merchant_general_setting.m_business_name)
                            

                            role_id = form.cleaned_data.get("role_name")

                            merchant_userrole.objects.create(user = user, role_id = role_id)

                            name = form.cleaned_data['first_name']
                            email = form.cleaned_data['email']
                            mobile_no = form.cleaned_data['mobile_no']

                            mobile_no_str = str(merchant_user_id_object.mobile_no) + ',' + str(mobile_no)

                            ts = int(time.time())

                            notification_object = notification_settings.objects.get(id = 5)

                            if notification_object.send_sms:
                                data_temp = {
                                        "keyword":"Team Login Credentials",
                                        "timeStamp":ts,
                                        "dataSet":
                                            [
                                                {
                                                    "UNIQUE_ID":"GB-" + str(ts),
                                                    "MESSAGE":"Dear Green Bill user, here is the login credentials for your team. Username: " + mobile_no + " Password: "+ temp_password,
                                                    "OA":"GRBILL", 
                                                    "MSISDN": str(mobile_no_str), # Recipient's Mobile Number
                                                    "CHANNEL":"SMS",
                                                    "CAMPAIGN_NAME":"hind_user",
                                                    "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                    "USER_NAME":"hind_hsi",
                                                    "DLT_TM_ID":"1001096933494158", # TM ID
                                                    "DLT_CT_ID":"1007162098336084141", # Template Id
                                                    "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                }
                                            ]
                                        }

                                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                response = requests.post(url, json = data_temp)

                            if notification_object.send_email:
                                subject = 'Team Login Credentials'
                                message = f'Dear Green Bill user, here is the login credentials for your team.\n Username: {mobile_no} \n Password: {temp_password}'
                                email_from = settings.EMAIL_HOST_USER 
                                recipient_list = [email, merchant_user_id_object.m_email] 
                                send_mail( subject, message, email_from, recipient_list ) 
                            
                            return JsonResponse({'status':'success'})
                        else:
                            return JsonResponse({'status':'limited'})
                    else:
                        return JsonResponse({'status':'limited'})


                else:
                    temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
                    
                    user = GreenBillUser.objects.create_user(
                        mobile_no = form.cleaned_data['mobile_no'],
                        m_email = form.cleaned_data['email'],
                        first_name = form.cleaned_data['first_name'],
                        last_name = form.cleaned_data['last_name'],
                        password = temp_password,
                        is_merchant_staff = 1
                    )

                    merchant_user_id = Merchant_users.objects.filter(user_id = request.user).values('merchant_user_id')[0]['merchant_user_id']

                    merchant_user_id_object = GreenBillUser.objects.get(id=merchant_user_id)

                    merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_user_id, m_active_account = 1)
                    
                    Merchant_users.objects.create(user_id = user, merchant_user_id = merchant_user_id_object, raw_password= temp_password, m_business_id=merchant_general_setting.id, m_business_name= merchant_general_setting.m_business_name)
                    

                    role_id = form.cleaned_data.get("role_name")

                    merchant_userrole.objects.create(user = user, role_id = role_id)

                    name = form.cleaned_data['first_name']
                    email = form.cleaned_data['email']
                    mobile_no = form.cleaned_data['mobile_no']

                    mobile_no_str = str(merchant_user_id_object.mobile_no) + ',' + str(mobile_no)

                    ts = int(time.time())

                    notification_object = notification_settings.objects.get(id = 5)

                    if notification_object.send_sms:
                        data_temp = {
                                "keyword":"Team Login Credentials",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Dear Green Bill user, here is the login credentials for your team. Username: " + mobile_no + " Password: "+ temp_password,
                                            "OA":"GRBILL", 
                                            "MSISDN": str(mobile_no_str), # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098336084141", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                        response = requests.post(url, json = data_temp)

                    if notification_object.send_email:
                        subject = 'Team Login Credentials'
                        message = f'Dear Green Bill user, here is the login credentials for your team.\n Username: {mobile_no} \n Password: {temp_password}'
                        email_from = settings.EMAIL_HOST_USER 
                        recipient_list = [email, merchant_user_id_object.m_email] 
                        send_mail( subject, message, email_from, recipient_list ) 
                    
                    return JsonResponse({'status':'success'})
                    

        else: 
            return JsonResponse({'status':'error'})
    else:
        return render(request, 'accounts/merchant-panel-users.html', context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchantchangeuserpassword(request):
    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_users_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    if request.method == "POST":

        mer_user_id = request.POST['mid']
        new_password = request.POST['edit_password']
        print(new_password)
        if mer_user_id is not None:

            user_object = GreenBillUser.objects.get(id=mer_user_id)
            print(user_object)
            user_object.set_password(new_password)
            user_object.save()
            Merchant_users.objects.filter(user_id=user_object, m_business_id = merchant_business_id.id).update(raw_password=new_password)
            sweetify.success(request, title="Success", icon='success',
                             text='Password Changed SuccessFully', timer=1500)

    try:
        merchant_user_id = Merchant_users.objects.filter(
            user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

        merchant_user_id_object = GreenBillUser.objects.get(
            id=merchant_user_id)

        qs_temp = Merchant_users.objects.filter(
            merchant_user_id=merchant_user_id_object, m_business_id = merchant_business_id.id).order_by('-id')

    except:
        qs_temp = ""

    for object in qs_temp:
        temp = GreenBillUser.objects.get(mobile_no=object.user_id)
    context = {
        "user_list": qs_temp,
        'MyTeamNavclass': 'active',
        "MyTeamCollapsShow": "show",
        "ChangeUserPasswordNavclass": "active"
    }
    return render(request, 'accounts/merchant-change-user-password.html', context)



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_update_user_view(request):

    if request.method == "POST":

        post_data = request.POST or None

        my_form = UpdateMerchantUserForm(request.POST)
        
        if my_form.is_valid():

            user_id = my_form.cleaned_data.get("user_id")

            mobile_no = my_form.cleaned_data.get("edit_mobile_no")
            
            role_name = my_form.cleaned_data.get("edit_role_name")
            
            email1 = my_form.cleaned_data.get("edit_email")

            first_name = my_form.cleaned_data.get("edit_first_name")

            last_name = my_form.cleaned_data.get("edit_last_name")

            if user_id is not None:

                GreenBillUser.objects.filter(id = user_id).update(mobile_no = mobile_no, m_email = email1, first_name = first_name, last_name = last_name)

                merchant_userrole.objects.filter(user = user_id).update(role = role_name)

            return JsonResponse({'success':True})
        else:
            return JsonResponse({'success':False})
    else:
        return JsonResponse({'success':False})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_delete_user_view(request, id):

    instance = GreenBillUser.objects.get(id=id)
    instance.delete()

    userrole.objects.filter(user_id = id).delete()

    return JsonResponse({'success':True})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_disable_user_view(request, id):
    GreenBillUser.objects.filter(id=id).update(is_active = False)
    return JsonResponse({'success':True})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_enable_user_view(request, id):
    GreenBillUser.objects.filter(id=id).update(is_active = True)
    return JsonResponse({'success':True})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_email_setting(request):
    if request.method == "POST":
        
        form = MerchantEmailSettingForm(request.POST)

        if form.is_valid():
           
            from_name = form.cleaned_data.get("from_name")
            from_email = form.cleaned_data.get("from_email")
            footer = form.cleaned_data.get("footer")
            signature = form.cleaned_data.get("signature")

            result = MerchantEmailSetting.objects.update_or_create(from_email=from_email, defaults={'from_name': from_name, 'from_email': from_email, 'footer': footer, 'signature': signature})
            if result:
                sweetify.success(request, title="Success", icon='success',
                                    text='Email Settings Stored Successfully !!!')
                return redirect('/merchant-email-setting/')
            else:
                sweetify.error(request, title="error",
                           icon='error', text='Failed !!!', timer=1000)
            return redirect('/merchant-email-setting/')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!', timer=1000)
            return redirect('/merchant-email-setting/')
    else:

        if MerchantEmailSetting.objects.all():
            data = MerchantEmailSetting.objects.latest('id')
        else:
            data = None

        form = MerchantEmailSettingForm()
        context = {
            'form': form, 
            'data': data,
            'SettingNavclass': "active",
            'settingsCollapseShow': "show",
            'MerchantEmailSettingsNavclass': "active"
        }
        return render(request, "merchant/merchant_email_setting.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchantSmsSetting(request):
    if request.method == "POST":
        # print('check')
        template_header_id = request.POST.get('template_header_id')
        
        if template_header_id == '0':
            type_header = request.POST.get('transactional')

            if type_header == 'transactional':
                request_header = request.POST.get('request_header_trans')
            elif type_header == 'promotional':
                request_header = request.POST.get('request_header_promo')

            sms_header = smsHeaderModel.objects.filter(request_user = request.user, header_content = request_header)
            if sms_header:
                sweetify.error(request, title="error", icon='error', text='Sms Header is already exists !!!', timer=1000)
                return redirect('/merchant-sms-setting/')
            else:
                header = smsHeaderModel.objects.create(header_content= request_header, request_user = request.user, status = 'Approved', Active_status = True, header_type=type_header)
                if header:
                    sweetify.success(request, title="Success", icon='success', text='SMS Header Stored Successfully !!!')
                    return redirect('/merchant-sms-setting/')
                else:
                    sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
                    return redirect('/merchant-sms-setting/')

        else:
            template_content = request.POST.get('template_content')
            sms_template = templateContentModel.objects.filter(request_user = request.user, template_content = template_content)
            if sms_template:
                sweetify.error(request, title="error", icon='error', text='Sms Template is already exists !!!', timer=1000)
                return redirect('/merchant-sms-setting/')
            else:
                sms_header = request.POST['sms_header_value']

                # print('123',sms_header)
                sms_header_new = sms_header.split(",")
                template_id = request.POST['template_id']
                template = templateContentModel.objects.create(template_content= template_content, request_user = request.user, status = 'Approved', sms_header = sms_header_new, template_id=template_id)
                if template:
                    sweetify.success(request, title="Success", icon='success', text='SMS Template Stored Successfully !!!')
                    return redirect('/merchant-sms-setting/')
                else:
                    sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
                    return redirect('/merchant-sms-setting/')
    data = smsHeaderModel.objects.filter(request_user = request.user).order_by('-id')
    Template = templateContentModel.objects.filter(request_user = request.user).order_by('-id')
    for obj in Template:
        if obj.sms_header:
            temp_sms_header = ""
            temp_sms_header = obj.sms_header.replace("[", "")
            temp_sms_header = temp_sms_header.replace("]", "")
            temp_sms_header = temp_sms_header.replace("'", "")
            obj.sms_header = temp_sms_header
    context = {
        'data': data,
        'Template': Template,
        'SettingNavclass': "active",
        'settingsCollapseShow': "show",
        'MerchantSmsSettingsNavclass': "active"
    }
    return render(request, "merchant/merchant_sms_setting.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchantSmstemplateSetting(request):
    if request.method == "POST":
        template_content = request.POST.get('template_content')
        template = templateContentModel.objects.create(template_content= template_content, request_user = request.user)
        if template:
            sweetify.success(request, title="Success", icon='success', text='SMS Header Stored Successfully !!!')
            return redirect('/merchant-sms-setting/')
        else:
            sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
            return redirect('/merchant-sms-setting/')
    Template = templateContentModel.objects.filter(request_user = request.user)
    context = {
        'Template': Template,
        'SettingNavclass': "active",
        'settingsCollapseShow': "show",
        'MerchantSmsSettingsNavclass': "active"
    }
    return render(request, "merchant/merchant_sms_setting.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def changeSmsHeaderStatusDisable(request, id):
    if request.method == "POST":
        result1 = smsHeaderModel.objects.filter(request_user = request.user).update(Active_status = False)
        result2 = smsHeaderModel.objects.filter(id = id).update(Active_status = True)
        return JsonResponse({'status': 'success', 'msg': 'Status change successfully'})
    else:
        return JsonResponse({'status': 'error', 'msg': 'Something went wrong'})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def changeSmsHeaderStatusEnable(request, id):
    if request.method == "POST":
        result1 = smsHeaderModel.objects.filter(request_user = request.user).update(Active_status = False)
        result2 = smsHeaderModel.objects.filter(id = id).update(Active_status = True)
        return JsonResponse({'status': 'success', 'msg': 'Status change successfully'})
    else:
        return JsonResponse({'status': 'error', 'msg': 'Something went wrong'})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def activesmstemplate(request, id):
    if request.method == "POST":
        result1 = templateContentModel.objects.filter(request_user = request.user).update(Active_status = False)
        result2 = templateContentModel.objects.filter(id = id).update(Active_status = True)
        return JsonResponse({'status': 'success', 'msg': 'Status change successfully'})
    else:
        return JsonResponse({'status': 'error', 'msg': 'Something went wrong'})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def deleteSmsHeader(request, id):
    if request.method == "POST":
        instance = smsHeaderModel.objects.get(id=id)
        user = instance.request_user
        header = instance.header_content
        template = templateContentModel.objects.filter(request_user = user)
        for header_template in template:
            if header in header_template.sms_header:
                templates = templateContentModel.objects.get(id = header_template.id)
                templates.delete()
        instance.delete()
        return JsonResponse({'status': 'success', 'msg': 'Header deleted successfully'})
    else:
        return JsonResponse({"status": "error", 'msg': "Something went wrong"})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def deleteSmstemplatebymerchant(request, id):
    if request.method == "POST":
        instance = templateContentModel.objects.get(id=id)
        instance.delete()
        return JsonResponse({'status': 'success', 'msg': 'Template deleted successfully'})
    else:
        return JsonResponse({"status": "error", 'msg': "Something went wrong"})


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def petrolPumpDetails(request):
    if request.method == "POST":
        form = MerchantPetrolPumpProductForm(request.POST)

        if form.is_valid():

            m_business_id = form.cleaned_data.get("m_business_id")
            # product_id = form.cleaned_data.get("product_id")
            product_id = ''
            product_name = form.cleaned_data.get("product_name")
            product_cost = form.cleaned_data.get("product_cost").lstrip('0')
            product_availability = form.cleaned_data.get("product_availability")
            
            # isProductIdExists = MerchantPetrolPump.objects.filter(product_id = product_id, m_business_id= m_business_id)
            isProductIdExists = False
            isProductNameExists = MerchantPetrolPump.objects.filter(m_business_id= m_business_id, product_name = product_name)
            
            if isProductIdExists:
                return JsonResponse({'status': 'errorProductId', 'msg': "Product with same id already exists !"})
            elif isProductNameExists:
                return JsonResponse({'status': 'errorProductName', 'msg': "Product with same name already exists !"})
            elif product_cost == "0" or product_cost == "0.00":
                return JsonResponse({'status': 'errorProductCost', 'msg': "Product Cost Must be greater than Zero !"})
            else:

                result = MerchantPetrolPump.objects.create(user= request.user, m_business_id= m_business_id, product_id= product_id, product_name=product_name, product_cost=product_cost, product_availability= product_availability)

                if result:
                    return JsonResponse({'status': 'success', 'msg': "Product added successfully !!!"})
                else:
                    return JsonResponse({'status': 'error', 'msg': "Failed to add product !!!"})
        else:
            return JsonResponse({'status': 'error', 'msg': "Something went wrong !!!"})
    else:
        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)
        
        form = MerchantPetrolPumpProductForm()
        try:
            data = MerchantPetrolPump.objects.filter(user= request.user,m_business_id= merchant_general_setting.id)
            print('data',data)
        except:
            data = ""
        total_count = MerchantPetrolPump.objects.filter(user= request.user,m_business_id= merchant_general_setting.id).count()
        context = {
            'form': form,
            'product_list': data,
            'PetrolPumpNavclass': "active",
            'PetrolPumpMenuCollapseShow': "show",
            'PetrolPumpMyProductsNavclass': "active",
            'merchant_general_setting_id': merchant_general_setting.id,
            'total_count':total_count
        }
        return render(request, "merchant/petrol_pump_details.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def getPetrolPumpProductDetail(request):
    if request.method == "POST":
        id = request.POST['id']
        data = MerchantPetrolPump.objects.filter(id= id)
       
        return JsonResponse({'status': "success", 'id': id, 'product_id': data[0].product_id, 'product_name': data[0].product_name, 'product_cost': data[0].product_cost, 'product_availability': data[0].product_availability})
    else:
        return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def editPetrolPumpProductDetail(request):
    if request.method == "POST":
        id = request.POST['p_id']
        # product_id = request.POST['edit_product_id']
        product_id = ''
        product_name = request.POST['edit_product_name']
        product_cost = request.POST['edit_product_cost'].lstrip('0')
        product_availability = request.POST['edit_product_availability']

        # isProductIdExists = MerchantPetrolPump.objects.filter(product_id = product_id)
            
        # if isProductIdExists:
        #     sweetify.error(request, title="error", icon='error', text='Product with same id already exists !', timer=1000)
        #     return redirect('/merchant-petrol-pump-details/') 
        # else:
        data = MerchantPetrolPump.objects.filter(id= id).update(product_id= product_id, product_name= product_name, product_cost=product_cost, product_availability=product_availability)
    
        sweetify.success(request, title="Success", icon='success', text='Product updated Successfully !!!', timer=1000)
        return redirect('/merchant-petrol-pump-details/')
    else:
        sweetify.error(request, title="error", icon='error', text='Failed to update product!!!', timer=1000)
        return redirect('/merchant-petrol-pump-details/') 

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deletePetrolPumpProduct(request, id):
    print(request)
    if request.method == "POST":
        data = MerchantPetrolPump.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Product deleted Successfully !!!', timer=1000)
        return redirect('/merchant-petrol-pump-details/')
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete product!!!', timer=1000)
        return redirect('/merchant-petrol-pump-details/')

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def addPetrolNozzle(request):
    if request.method == "POST":
        form = AddPetrolNozzleForm(request.POST)
        if form.is_valid():
            m_business_id = form.cleaned_data.get("m_business_id")
            nozzle = form.cleaned_data.get("nozzle")

            isNozzleExists = MerchantPetrolNozzle.objects.filter(user= request.user, m_business_id= m_business_id, nozzle = nozzle)
            
            if isNozzleExists:
                return JsonResponse({'status': 'errorNozzleExists', 'msg': "Nozzle already exists !"})
            else:
                result = MerchantPetrolNozzle.objects.create(user= request.user, m_business_id= m_business_id, nozzle = nozzle)

                if result:
                    return JsonResponse({'status': 'success', 'msg': "Nozzle added successfully !!!"})
                else:
                    return JsonResponse({'status': 'error', 'msg': "Failed to add Nozzle !!!"})
        else:
            return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})
    else:
        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

        form = AddPetrolNozzleForm()

        try:
            data= MerchantPetrolNozzle.objects.filter(user_id = request.user.id, m_business_id= merchant_general_setting.id)
        except:
            data = ""

        try:
            nozzle_count_temp = NozzleCount.objects.filter(business_id= merchant_general_setting.id)
            nozzle_count = nozzle_count_temp[0].nozzle_count
        except:
            nozzle_count = ""

        context = {
            'form': form,
            'nozzle_list' : data,
            'nozzle_count' : nozzle_count,
            # 'PetrolPumpNavclass': "active",
            # 'PetrolPumpMenuCollapseShow': "show",
            'addNozzleNavClass': "active",
            "SettingNavclass": "active",
            "settingsCollapseShow": "show",
            'merchant_general_setting_id': merchant_general_setting.id
        }

        return render(request, "merchant/add-nozzle.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def addPetrolNozzleCount(request):
    if request.method == "POST":
        nozzle_count = request.POST["nozzle_count"]
        business_id = request.POST["business_id"]
        result = NozzleCount.objects.update_or_create(business_id = business_id, defaults={'nozzle_count': nozzle_count})

        if result:
            sweetify.success(request, title="Success", icon='success', text='Nozzle Count Added Successfully !!!', timer=1500)
            return redirect(addPetrolNozzle)
        else: 
            sweetify.error(request, title="error", icon='error', text='Failed to add Nozzle Count !!!', timer=1500)
    else:
        sweetify.error(request, title="Error", icon='error', text='Failed to update Nozzle Count !!!', timer=1500)
        return redirect(addPetrolNozzle)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def getPetrolNozzleDetail(request):
    if request.method == "POST":
        id = request.POST['id']
        data = MerchantPetrolNozzle.objects.filter(id= id)
        return JsonResponse({'status': "success", 'id': id, 'nozzle': data[0].nozzle})
    else:
        return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def editPetrolNozzle(request):
    if request.method == "POST":
        id = request.POST['n_id']
        edit_nozzle = request.POST['edit_nozzle']

        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        merchant_business_object = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

        m_business_id = merchant_business_object.id

        isNozzleExists = MerchantPetrolNozzle.objects.filter(user= request.user, m_business_id= m_business_id, nozzle = edit_nozzle)
            
        if isNozzleExists:
            sweetify.error(request, title="Error", icon='error', text='Nozzle with same name already exists !', timer=1500)
            return redirect(addPetrolNozzle) 
        else:
            data = MerchantPetrolNozzle.objects.filter(id= id).update(nozzle = edit_nozzle)
    
        sweetify.success(request, title="Success", icon='success', text='Nozzle updated Successfully !!!', timer=1500)
        return redirect(addPetrolNozzle)
    else:
        sweetify.error(request, title="Error", icon='error', text='Failed to update Nozzle!!!', timer=1500)
        return redirect(addPetrolNozzle)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deletePetrolNozzle(request, id):
    if request.method == "POST":
        data = MerchantPetrolNozzle.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Nozzle deleted Successfully !!!', timer=1500)
        return redirect(addPetrolNozzle)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Nozzle!!!', timer=1500)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def addVehicleType(request):
    if request.method == "POST":
        form = MerchantParkingAddVehicleTypeForm(request.POST)
        
        if form.is_valid():
            m_business_id = form.cleaned_data.get("m_business_id")
            vehicle_type = form.cleaned_data.get("vehicle_type")
            isVehicleTypeExists = MerchantParkingAddVehicle.objects.filter(m_business_id= m_business_id,vehicle_type = vehicle_type)
            
            if isVehicleTypeExists:
                return JsonResponse({'status': 'errorVehicleType', 'msg': "Vehicle Type already exists !"})
            else:
                result = MerchantParkingAddVehicle.objects.create(user= request.user, m_business_id= m_business_id, vehicle_type=  vehicle_type)

                if result:
                    return JsonResponse({'status': 'success', 'msg': "Vehicle Type added successfully !!!"})
                else:
                    return JsonResponse({'status': 'error', 'msg': "Failed to add product !!!"})
        else:
            return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})
    else:
        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)
        form = MerchantParkingAddVehicleTypeForm()

        try:
            data= MerchantParkingAddVehicle.objects.filter(m_business_id= merchant_general_setting.id)
        except:
            data = ""

        context = {
            'form': form,
            'vehicle_type_list' : data,
            'ParkingLotManagementNavclass':"active",
            # 'ParkingLotNavclass': "active",
            'ParkingLotManagementCollapseShow': "show",
            # 'ParkingLotCollapseShow': "show",
            'addVehicleTypeNavClass': "active",

            'merchant_general_setting_id': merchant_general_setting.id
        }
        return render(request, "merchant/add_vehicle_type.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deleteVehicleType(request, id):
    if request.method == "POST":
        data = MerchantParkingAddVehicle.objects.get(id= id)

        vehicle = data.vehicle_type

        try:
            MerchantParkingLotSpace.objects.filter(vehicle_type = vehicle).delete()
        except:
            pass

        try:
            MerchantParkingSpaceCharges.objects.filter(vehicle_type = vehicle).delete()
        except:
            pass

        try:
            MerchantParkingLotPassCharges.objects.filter(vehicle_type_id = id).delete()
        except:
            pass

        try:
            data.delete()
        except:
            pass
        return JsonResponse({'status': 'success', 'msg': "Vehicle Type deleted successfully !!!"})


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def addParkingSpace(request):
    if request.method == "POST":
        
        form = MerchantParkingLotSpaceForm(request.POST)
        
        if form.is_valid():
            m_business_id = form.cleaned_data.get("m_business_id")
            entry_gate = form.cleaned_data.get("entry_gate")
            exit_gate = form.cleaned_data.get("exit_gate")
            vehicle_type = form.cleaned_data.get("vehicle_type")
            spaces_count = form.cleaned_data.get("spaces_count").lstrip('0')
            print('spaces_count',spaces_count)
            
            
            vehicle_exists = MerchantParkingLotSpace.objects.filter(user_id = request.user.id, m_business_id= m_business_id, vehicle_type= vehicle_type)
            vehicle_type_arr = MerchantParkingAddVehicle.objects.filter(user_id = request.user.id, m_business_id= m_business_id, vehicle_type= vehicle_type)
            if vehicle_exists:
                return JsonResponse({'status': 'errorSpace', 'msg': "Space already Exists, Please change vehicle type !!!"})
            else:

                result = MerchantParkingLotSpace.objects.create(user= request.user, m_business_id= m_business_id, entry_gate=  entry_gate, exit_gate= exit_gate, vehicle_type_id= vehicle_type_arr[0].id, vehicle_type= vehicle_type, spaces_count= spaces_count)

                if result:
                    return JsonResponse({'status': 'success', 'msg': "Space added successfully !!!"})
                else:
                    return JsonResponse({'status': 'error', 'msg': "Failed to add product !!!"})
        else:
            return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})
    else:
        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)
        form = MerchantParkingLotSpaceForm()
        try:
            data= MerchantParkingLotSpace.objects.filter(m_business_id= merchant_general_setting.id)
        except:
            data = ""

        try: 
            vehicle_type_by_business = MerchantParkingAddVehicle.objects.filter(m_business_id= merchant_general_setting.id)
        except:
            vehicle_type_by_business = ""

        from parking_lot_apis.models import SaveParkingLotBill

        for data_temp in data:

            space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= merchant_general_setting.id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()

            data_temp.space_avilable_count = int(data_temp.spaces_count) - int(space_avilable_count)

            # print(data_temp.space_avilable_count)

        try:
            result = parking_app_setting_model.objects.get(merchant_id = merchant_users_object.merchant_user_id)
            if result.exit_gate:
                exit_gate_status = True
            else:
                exit_gate_status = False
        except:
            exit_gate_status = False

        context = {
            'form': form,
            'space_list' : data,
            'vehicle_by_business': vehicle_type_by_business, 
            # 'ParkingLotNavclass': "active",
            # 'ParkingLotCollapseShow': "show",
            "ParkingLotManagementNavclass": "active",
            "ParkingLotManagementCollapseShow": "show",
            'addParkingSpaceNavClass': "active",
            'merchant_general_setting_id': merchant_general_setting.id,
            'exit_gate_status':exit_gate_status,
        }
        return render(request, "merchant/parking_lot_details.html", context)
    

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def getParkingLotSpaceDetails(request):
    if request.method == "POST":
        id = request.POST['id']
        data = MerchantParkingLotSpace.objects.filter(id= id)
        arr = {
            'id': id,
            'entry_gate': data[0].entry_gate,
            'exit_gate': data[0].exit_gate,
            'vehicle_type_id': data[0].vehicle_type_id,
            'vehicle_type': data[0].vehicle_type,
            'spaces_count': data[0].spaces_count,
        }
        
        return JsonResponse({'status': "success", 'data': arr})
    else:
        return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def editParkingLotSpaceDetails(request):
    # print(request.POST['edit_exit_gate'])
    if request.method == "POST":
        if 'edit_exit_gate' not in request.POST:
            exit_gate = 0
        else:
            exit_gate = request.POST['edit_exit_gate']

        id = request.POST['space_id']

        if 'edit_entry_gate' not in request.POST:
            entry_gate = 0
        else:
            entry_gate = request.POST['edit_entry_gate']
        
        # exit_gate = request.POST['edit_exit_gate']
        vehicle_type = request.POST['edit_vehicle_type']
        spaces_count = request.POST['edit_spaces_count'].lstrip('0')

        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

        vehicle_type_arr = MerchantParkingAddVehicle.objects.filter(user_id = request.user.id, m_business_id= merchant_general_setting.id, vehicle_type= vehicle_type)

        data = MerchantParkingLotSpace.objects.filter(id= id).update(entry_gate= entry_gate, exit_gate= exit_gate, vehicle_type_id=vehicle_type_arr[0].id, vehicle_type= vehicle_type, spaces_count= spaces_count)
       
        sweetify.success(request, title="Success", icon='success', text='Product updated Successfully !!!', timer=1000)
        return redirect('/add-parking-space/')
    else:
        sweetify.error(request, title="error", icon='error', text='Failed to update product!!!', timer=1000)
        return redirect('/add-parking-space/')

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deleteParkingLotSpace(request, id):
    if request.method == "POST":
        data = MerchantParkingLotSpace.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Space deleted Successfully !!!', timer=1000)
        return redirect('/add-parking-space/')
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete product!!!', timer=1000)
        return redirect('/add-parking-space/') 

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def addParkingSpaceCharges(request):
    if request.method == "POST":
        form = MerchantParkingLotSpaceChargesForm(request.POST)
        print(form.errors)
        print(form.is_valid())
        if form.is_valid():

            m_business_id = form.cleaned_data.get("m_business_id")
            vehicle_type = form.cleaned_data.get("vehicle_type")
            charges_by = form.cleaned_data.get("charges_by")
            charges = form.cleaned_data.get("charges").lstrip('0')
            for_hours = form.cleaned_data.get("for_hours")
            for_additional_hours = form.cleaned_data.get("for_additional_hours")
            additional_hours_charges =  form.cleaned_data.get("additional_hours_charges").lstrip('0')

            # additional_hours_charges = form.cleaned_data.get("additional_hours_charges").lstrip('0')

            # additional_hours_charges = ""

            merchant_users_object = Merchant_users.objects.get(user_id = request.user)

            vehicle_exists = MerchantParkingSpaceCharges.objects.filter(user_id = merchant_users_object.merchant_user_id.id, m_business_id= m_business_id, vehicle_type= vehicle_type)
            print('vehicle_exists',vehicle_exists)
            vehicle_type_arr = MerchantParkingAddVehicle.objects.filter(user_id = merchant_users_object.merchant_user_id.id, m_business_id= m_business_id, vehicle_type= vehicle_type)
            print('vehicle_type_arr',vehicle_type_arr)
            if vehicle_exists:
                return JsonResponse({'status': 'errorCharges', 'msg': "Vehicle already Exists, Please change vehicle type !!!"})
            else:

                result = MerchantParkingSpaceCharges.objects.create(user = merchant_users_object.merchant_user_id, m_business_id= m_business_id, vehicle_type_id= vehicle_type_arr[0].id, vehicle_type= vehicle_type, charges_by= charges_by, charges=charges, additional_hours_charges = additional_hours_charges, for_hours = for_hours, for_additional_hours = for_additional_hours)
                # result = 0
                if result:
                    return JsonResponse({'status': 'success', 'msg': "Space Charges added successfully !!!"})
                else:
                    return JsonResponse({'status': 'error', 'msg': "Failed to add charges !!!"})
        else:
            return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})
    else:
        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)
        form = MerchantParkingLotSpaceChargesForm()
        try:
            data= MerchantParkingSpaceCharges.objects.filter(user_id = request.user,m_business_id= merchant_general_setting.id)
        except:
            data = ""

        try: 
            vehicle_type_by_business = MerchantParkingAddVehicle.objects.filter(m_business_id= merchant_general_setting.id)
        except:
            vehicle_type_by_business = ""

        context = {
            'form': form,
            'charges_list' : data,
            'vehicle_by_business': vehicle_type_by_business, 
            # 'ParkingLotNavclass': "active",
            # 'ParkingLotCollapseShow': "show",
            "ParkingLotManagementNavclass": "active",
            "ParkingLotManagementCollapseShow": "show",
            'addParkingSpaceChargesNavClass': "active",

            'merchant_general_setting_id': merchant_general_setting.id
        }
        return render(request, "merchant/add_parking_space_charges.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def getParkingSpaceCharges(request):
    if request.method == "POST":
        id = request.POST['id']
        data = MerchantParkingSpaceCharges.objects.filter(id= id)
        arr = {
            'id': id,
            'vehicle_type_id': data[0].vehicle_type_id,
            'vehicle_type': data[0].vehicle_type,
            'charges_by': data[0].charges_by,
            'charges': data[0].charges,
            'additional_hours_charges': data[0].additional_hours_charges,
            'for_hours' : data[0].for_hours,
            'for_additional_hours' : data[0].for_additional_hours
        }
        
        return JsonResponse({'status': "success", 'data': arr})
    else:
        return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def editParkingSpaceCharges(request):
    
    if request.method == "POST":
        id = request.POST['space_charges_id']
        vehicle_type = request.POST['edit_vehicle_type']
        charges_by = request.POST['edit_charges_by']
        charges = request.POST['edit_charges'].lstrip('0')

        for_hours = request.POST['edit_for_hours']
        
        for_additional_hours = request.POST['edit_for_additional_hours']
        
        additional_hours_charges = request.POST['edit_additional_hours_charges'].lstrip('0')

        # additional_hours_charges = ""

        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

        vehicle_type_arr = MerchantParkingAddVehicle.objects.filter(user_id = merchant_users_object.merchant_user_id, m_business_id= merchant_general_setting.id, vehicle_type= vehicle_type)
       
        data = MerchantParkingSpaceCharges.objects.filter(id= id).update(vehicle_type_id=vehicle_type_arr[0].id, vehicle_type= vehicle_type, charges_by= charges_by, charges= charges, additional_hours_charges = additional_hours_charges, for_additional_hours = for_additional_hours, for_hours = for_hours)
       
        sweetify.success(request, title="Success", icon='success', text='Space Charges updated Successfully !!!', timer=1000)
        return redirect('/add-parking-space-charges/')
    else:
        sweetify.error(request, title="error", icon='error', text='Failed to update Charges!!!', timer=1000)
        return redirect('/add-parking-space-charges/')

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deleteParkingSpaceCharges(request, id):
    if request.method == "POST":
        data = MerchantParkingSpaceCharges.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Space Charge deleted Successfully !!!', timer=1000)
        return redirect('/add-parking-space-charges/')
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete space charge !!!', timer=1000)
        return redirect('/add-parking-space-charges/') 


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_business_logo_remove(request):
    MerchantProfile.objects.update_or_create(m_user = request.user.id, m_active_account = True, defaults={ "m_business_logo" : ""})
    return redirect(merchant_general_setting)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_business_stamp_remove(request):
    MerchantProfile.objects.update_or_create(m_user = request.user.id, m_active_account = True, defaults={ "m_business_stamp" : ""})
    return redirect(merchant_general_setting)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_digital_signature_remove(request):
    MerchantProfile.objects.update_or_create(m_user = request.user.id, m_active_account = True, defaults={ "m_digital_signature" : ""})
    return redirect(merchant_general_setting)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def petrol_pump_app_setting(request):
    
    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)
    print("EW",merchant_object)

    merchant_bussiness = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
    print("QAS",merchant_bussiness)

    if request.method == "POST":

        send_bill = request.POST["send_bill"]
        footer_text1 = request.POST["footer_text1"]
        footer_text2 = request.POST["footer_text2"]
        footer_text3 = request.POST["footer_text3"]
        header_text1 = request.POST["header_text1"]
        header_text2 = request.POST["header_text2"]
        header_text3 = request.POST["header_text3"]


        if send_bill == "digital_bill":
            digital_bill = True
            sms = False
            print("QQ",send_bill)

        elif send_bill == "sms":
            sms = True
            digital_bill = False
            print("WW",send_bill)

        status = petrol_pump_app_setting_model.objects.update_or_create(merchant_id = merchant_object, merchant_bussiness = merchant_bussiness, defaults={ "digital_bill": digital_bill, "sms" : sms, "footer_text1" : footer_text1,"footer_text2" : footer_text2,"footer_text3" : footer_text3,"header_text1":header_text1, "header_text2":header_text2, "header_text3": header_text3})

        if status:
            sweetify.success(request, title="Success", icon='success', text='Updated Successfully', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Fail to Update', timer=1500)


    setting = petrol_pump_app_setting_model.objects.filter(merchant_id = merchant_object, merchant_bussiness = merchant_bussiness).last()
    print("WQ",setting)

    context = {
        'setting':setting,
        'merchant_bussiness_name' : merchant_bussiness.m_business_name,
        # 'PetrolPumpNavclass': "active",
        # 'PetrolPumpMenuCollapseShow': "show",
        # 'PetrolPumpAppSettingNavclass': "active",
        'DesignNavclass': "active",
        'DesignCollapseShow': "show",
        'PetrolPumpAppSettingNavclass': "active",
    }

    return render(request, "merchant/petrol-pump-app-setting.html", context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def parking_app_setting(request):
    
    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    merchant_bussiness = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    if request.method == "POST":

        send_bill = request.POST["send_bill"]
        footer_text1 = request.POST["footer_text1"]
        footer_text2 = request.POST["footer_text2"]
        footer_text3 = request.POST["footer_text3"]
        header_text1 = request.POST["header_text1"]
        header_text2 = request.POST["header_text2"]
        header_text3 = request.POST["header_text3"]

        try:
            exit_gate =  request.POST["exit_gate"]
            if exit_gate == "exit_gate":
                exit_gate = True
            else:
                exit_gate = False
        except:
            exit_gate = False

        if send_bill == "digital_bill":
            digital_bill = True
            sms = False

        elif send_bill == "sms":
        	sms = True
        	digital_bill = False
            
        try:
            manage_space = request.POST['manage_space']
            if manage_space == "yes":
                manage_space=True
            else:
                manage_space=False
        except:
            manage_space=False



        try:
            pay_bill_at_exit_gate =  request.POST["pay_bill_at_exit_gate"]
            if pay_bill_at_exit_gate == "pay_bill_at_exit_gate":
                pay_bill_at_exit_gate_status = True
            else:
                pay_bill_at_exit_gate_status = False
        except:
            pay_bill_at_exit_gate_status = False

        status = parking_app_setting_model.objects.update_or_create(merchant_id = merchant_object, merchant_bussiness = merchant_bussiness, defaults={ "digital_bill": digital_bill, "sms" : sms, "footer_text1" : footer_text1, "footer_text2" : footer_text2, "footer_text3" : footer_text3, "header_text1" : header_text1, "header_text2" : header_text2, "header_text3" : header_text3, "exit_gate" : exit_gate, "pay_bill_at_exit_gate" : pay_bill_at_exit_gate_status,"manage_space":manage_space})

        if status:
            sweetify.success(request, title="Success", icon='success', text='Updated Successfully', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Fail to Update', timer=1500)

    
    setting = parking_app_setting_model.objects.filter(merchant_id = merchant_object, merchant_bussiness = merchant_bussiness).last()
    print("PRA",setting)
        

    context = {
            'setting':setting,
            'merchant_bussiness_name' : merchant_bussiness.m_business_name,
            # 'ParkingLotNavclass': "active",
            # 'ParkingLotCollapseShow': "show",
            'DesignNavclass': "active",
            'DesignCollapseShow': "show",
            'ParkingAppSettingNavClass': "active",
        }

    return render(request, "merchant/parking-app-setting.html", context)
    

@login_required(login_url="/merchant-login/")
def addonPetrolPumpDetails(request):
    if request.method == "POST":
        form = MerchantAddonPetrolPumpProductForm(request.POST)

        if form.is_valid():

            m_business_id = form.cleaned_data.get("m_business_id")
            # product_id = form.cleaned_data.get("product_id")
            product_id = ''
            product_name = form.cleaned_data.get("product_name")
            product_cost = form.cleaned_data.get("product_cost").lstrip('0')
            product_availability = form.cleaned_data.get("product_availability")
            
            # isProductIdExists = AddonPetrolPump.objects.filter(m_business_id= m_business_id, product_id = product_id)
            isProductIdExists = False
            isProductNameExists = AddonPetrolPump.objects.filter(m_business_id= m_business_id, product_name = product_name)
            
            if isProductIdExists:
                return JsonResponse({'status': 'errorProductId', 'msg': "Product with same id already exists !"})
            elif isProductNameExists:
                return JsonResponse({'status': 'errorProductName', 'msg': "Product with same name already exists !"})
            elif product_cost == "0" or product_cost == "0.00":
                return JsonResponse({'status': 'errorProductCost', 'msg': "Product Cost Must be greater than Zero !"})
            else:

                result = AddonPetrolPump.objects.create(user= request.user, m_business_id= m_business_id, product_id= product_id, product_name=product_name, product_cost=product_cost, product_availability= product_availability)

                if result:
                    return JsonResponse({'status': 'success', 'msg': "Product added successfully !!!"})
                else:
                    return JsonResponse({'status': 'error', 'msg': "Failed to add product !!!"})
        else:
            return JsonResponse({'status': 'error', 'msg': "Something went wrong !!!"})
    else:
        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)
        
        form = MerchantAddonPetrolPumpProductForm()
        try:
            data = AddonPetrolPump.objects.filter(m_business_id= merchant_general_setting.id)
        except:
            data = ""
        total_count = AddonPetrolPump.objects.filter(m_business_id= merchant_general_setting.id).count()
        context = {
            'form': form,
            'product_list': data,
            "PetrolPumpNavclass":"active",
            "PetrolPumpMenuCollapseShow": "show",
            "AddonPetrolPumpNavclass": "active",
            'merchant_general_setting_id': merchant_general_setting.id,
            'total_count': total_count,
        }
    return render(request,"merchant/addon_petrol_pump_details.html",context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def getAddonPetrolPumpProductDetail(request):
    if request.method == "POST":
        id = request.POST['id']
        data = AddonPetrolPump.objects.filter(id= id)
       
        return JsonResponse({'status': "success", 'id': id, 'product_id': data[0].product_id, 'product_name': data[0].product_name, 'product_cost': data[0].product_cost, 'product_availability': data[0].product_availability})
    else:
        return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def editAddonPetrolPumpProductDetail(request):
    if request.method == "POST":
        id = request.POST['p_id']
        # product_id = request.POST['edit_product_id']
        product_id = ''
        product_name = request.POST['edit_product_name']
        product_cost = request.POST['edit_product_cost'].lstrip('0')
        product_availability = request.POST['edit_product_availability']

        # isProductIdExists = MerchantPetrolPump.objects.filter(product_id = product_id)
            
        # if isProductIdExists:
        #     sweetify.error(request, title="error", icon='error', text='Product with same id already exists !', timer=1000)
        #     return redirect('/merchant-petrol-pump-details/') 
        # else:
        data = AddonPetrolPump.objects.filter(id= id).update(product_id= product_id, product_name= product_name, product_cost=product_cost, product_availability=product_availability)
    
        sweetify.success(request, title="Success", icon='success', text='Product updated Successfully !!!', timer=1000)
        return redirect('/addon-petrol-pump-details/')
    else:
        sweetify.error(request, title="error", icon='error', text='Failed to update product!!!', timer=1000)
        return redirect('/addon-petrol-pump-details/') 

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deleteAddonPetrolPumpProduct(request, id):
    print(request)
    if request.method == "POST":
        data = AddonPetrolPump.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Product deleted Successfully !!!', timer=1000)
        return redirect('/merchant-petrol-pump-details/')
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete product!!!', timer=1000)
        return redirect('/merchant-petrol-pump-details/')



# upload Logo/stamp/signature
@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_cropped_logo_upload(request):

    if request.method == 'POST':

        form = merchantuploadlogoForm(data=request.POST, files=request.FILES)
        if form.is_valid():

            setting_id = request.POST['merchant_setting_modal_id']
            img_data = dict(request.POST.items())
            # print(img_data)

            x = None  # Coordinate x
            y = None  # Coordinate y
            w = None  # Width
            h = None  # Height
            rotate = None  # Rotate
            for key, value in img_data.items():
                if key == "avatar_data":
                    str_value = json.loads(value)
                    # print(str_value)
                    x = str_value.get('x')
                    y = str_value.get('y')
                    w = str_value.get('width')
                    h = str_value.get('height')
                    rotate = str_value.get('rotate')

            # print('x: {}, y: {}, w: {}, h: {}, rotate: {}'.format(
            #     x, y, w, h, rotate))

            im = Image.open(
                request.FILES['merchantlogofile']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            newdoc = MerchantProfile.objects.get(id=setting_id)
            newdoc.m_business_logo.save('merchant_logo.png', image_file)
            newdoc.save()
            # data = {
            #     'result': True,
            #     'state': 200,
            #     'message': 'Success',
            # }

            # # redirect("/general-setting/")

            # return JsonResponse({'data': data})
            sweetify.success(request, title="Success...", icon='success', text='Logo updated successfully...', timer=1500)
            return redirect(merchant_general_setting)
    

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_cropped_stamp_upload(request):
    if request.method == 'POST':

        form = merchantuploadstampForm(data=request.POST, files=request.FILES)
        print(form)
        if form.is_valid():

            setting_id = request.POST['merchant_setting_stamp_modal_id']

            img_data = dict(request.POST.items())
            # print(img_data)

            x = None  # Coordinate x
            y = None  # Coordinate y
            w = None  # Width
            h = None  # Height
            rotate = None  # Rotate
            for key, value in img_data.items():
                if key == "avatar_data":
                    str_value = json.loads(value)
                    print(str_value)
                    x = str_value.get('x')
                    y = str_value.get('y')
                    w = str_value.get('width')
                    h = str_value.get('height')
                    rotate = str_value.get('rotate')

            # print('x: {}, y: {}, w: {}, h: {}, rotate: {}'.format(
            #     x, y, w, h, rotate))

            im = Image.open(
                request.FILES['merchantstampfile']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            newdoc = MerchantProfile.objects.get(id=setting_id)
            newdoc.m_business_stamp.save('profile_image.png', image_file)
            newdoc.save()
            data = {
                'result': True,
                'state': 200,
                'message': 'Success',
            }

            # redirect("/general-setting/")

            return JsonResponse({'data': data})


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_cropped_signature_upload(request):
    if request.method == 'POST':
        form = merchantuploadsignatureForm(
            data=request.POST, files=request.FILES)
        if form.is_valid():
            img_data = dict(request.POST.items())
            setting_id = request.POST['merchant_setting_signature_modal_id']
            # print(img_data)

            x = None  # Coordinate x
            y = None  # Coordinate y
            w = None  # Width
            h = None  # Height
            rotate = None  # Rotate
            for key, value in img_data.items():
                if key == "avatar_data":
                    str_value = json.loads(value)
                    print(str_value)
                    x = str_value.get('x')
                    y = str_value.get('y')
                    w = str_value.get('width')
                    h = str_value.get('height')
                    rotate = str_value.get('rotate')

            # print('x: {}, y: {}, w: {}, h: {}, rotate: {}'.format(
            #     x, y, w, h, rotate))

            im = Image.open(request.FILES['merchantsignaturefile']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            newdoc = MerchantProfile.objects.get(id=setting_id)
            newdoc.m_digital_signature.save('profile_image.png', image_file)
            newdoc.save()
            # data = {
            #     'result': True,
            #     'state': 200,
            #     'message': 'Success',
            # }

            # # redirect("/general-setting/")

            # return JsonResponse({'data': data})
            sweetify.success(request, title="Success...", icon='success', text='Signature updated successfully...', timer=1500)
            return redirect(merchant_general_setting)
    
@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def petrol_pump_flag_bills(request):
    
    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    merchant_profile = MerchantProfile.objects.get(m_user = merchant_object.id, m_active_account = 1)

    merchant_business_id = merchant_profile.id

    merchant_user = []

    merchant_user.append({
        'user_id': merchant_object
    })

    merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = merchant_business_id)

    flag_reasons = flagbillreason.objects.filter(m_business_id = merchant_business_id)

    bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile.id, bill_flag = True).order_by('-id')

    bills_count = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile.id, bill_flag = True).count()

    

    selected_reason_id = 0
    total_bills_amount = 0
    for bill in bills:
        if bill.total_amount:
            total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

        try:
            user_object = GreenBillUser.objects.get(id = bill.flag_by)
            flag_by_name = user_object.first_name + ' ' + user_object.last_name
        except:
            flag_by_name = ""

        # print(flag_by_name)
        bill.flag_by_name = flag_by_name

    if request.method == "POST":
        user = request.POST['user']
        from_date = request.POST['from_date']
        from_date_temp = from_date
        to_date = request.POST['to_date']
        to_date_temp = to_date
        reason_id = request.POST['reason_id']

        new_data = []

        if reason_id:
            bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile.id, bill_flag = True, reason_id = reason_id).order_by('-id')
            bills_count = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile.id, bill_flag = True, reason_id = reason_id).count()
            selected_reason_id = reason_id
        else:
            selected_reason_id = 0

        # if bills:

        if from_date:
            from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')

        if to_date:
            to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%d-%m-%Y')

        total_bills_amount = 0

        for bill in bills:

            if user or from_date or to_date:

                if user and from_date and to_date:
                    if bill.flag_by == user:
                        if bill.date >= from_date and bill.date <= to_date:
                            new_data.append(bill)
                            if bill.total_amount:
                                total_bills_amount = float(total_bills_amount) + float(bill.total_amount)


                elif from_date and to_date:
                    if bill.date >= from_date and bill.date <= to_date:
                        new_data.append(bill)
                        if bill.total_amount:
                            total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

                elif user and from_date :
                    if bill.flag_by == user and bill.date >= from_date:
                        new_data.append(bill)
                        if bill.total_amount:
                            total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

                elif user and to_date:
                    if bill.flag_by == user and bill.date <= to_date:
                        new_data.append(bill)
                        if bill.total_amount:
                            total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

                elif from_date:
                    if bill.date >= from_date:
                        new_data.append(bill)
                        if bill.total_amount:
                            total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

                elif to_date:
                    if bill.date <= to_date:
                        new_data.append(bill)
                        if bill.total_amount:
                            total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

                elif user:
                    if bill.flag_by == user:
                        new_data.append(bill)
                        if bill.total_amount:
                            total_bills_amount = float(total_bills_amount) + float(bill.total_amount)
            else:
                new_data.append(bill)
                if bill.total_amount:
                    total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

        total_flag_bills = 0

        if user:
            for bill in new_data:
                if bill.bill_flag == True:
                    total_flag_bills = total_flag_bills + 1

            context = {
                'flag_bills':new_data,
                'total_bills_amount': total_bills_amount,
                'bills_count': bills_count,
                'BillInfoNavClass':'active',
                "BillInfoCollapseShow": "show",
                'PetrolPumpFlagBillsNavClass': "active",
                'merchant_user': merchant_user,
                'total_flag_bills':total_flag_bills,
                'custom_user':int(user),
                'from_date': from_date_temp,
                'to_date': to_date_temp,
                'flag_reasons': flag_reasons,
                'selected_reason_id' : int(selected_reason_id),
            }

        else:
            context = {
                'flag_bills':new_data,
                'total_bills_amount': total_bills_amount,
                'bills_count': bills_count,
                'BillInfoNavClass':'active',
                "BillInfoCollapseShow": "show",
                'PetrolPumpFlagBillsNavClass': "active",
                'merchant_user': merchant_user,
                'from_date': from_date_temp,
                'to_date': to_date_temp,
                'flag_reasons': flag_reasons,
                'selected_reason_id' : int(selected_reason_id),
            }
        
    else:

        context = {
                'flag_bills':bills,
                'total_bills_amount': total_bills_amount,
                'bills_count': bills_count,
                'BillInfoNavClass':'active',
                "BillInfoCollapseShow": "show",
                'PetrolPumpFlagBillsNavClass': "active",
                'merchant_user': merchant_user,
                'flag_reasons': flag_reasons,
                'selected_reason_id' : selected_reason_id,
            }

    return render(request, "merchant/petrol-pump-flag-bills.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deletePetrolPumpFlagBill(request, id):
    if request.method == "POST":
        data = SavePetrolPumpBill.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Bill deleted Successfully !!!', timer=1500)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Bill!!!', timer=1500)
        
    return redirect(petrol_pump_flag_bills)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deleteSelectedPetrolPumpFlagBills(request):

    if request.method == "POST":

        bill_ids = request.POST.getlist('bill_id[]')
        
        if bill_ids:
            for bill_id in bill_ids:
                result = SavePetrolPumpBill.objects.filter(id = bill_id).delete()
                result = True
        else:
            result = False
        
        if result:
            sweetify.success(request, title="Success", icon='success', text='Bills deleted Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="error", icon='error', text='Please Select Bill !!!', timer=1500)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Bill!!!', timer=1500)
        
    return redirect(petrol_pump_flag_bills)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def parking_flag_bills(request):
    
    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    merchant_profile = MerchantProfile.objects.get(m_user = merchant_object.id, m_active_account = 1)

    merchant_business_id = merchant_profile.id

    merchant_user = []

    merchant_user.append({
        'user_id': merchant_object
    })

    merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = merchant_business_id)

    for user in merchant_user_temp:
        merchant_user.append({
            'user_id': user.user_id
            })

    flag_reasons = flagbillreason.objects.filter(m_business_id = merchant_business_id)

    bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile.id, bill_flag = True).order_by('-id')
    bills_count = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile.id, bill_flag = True).count()

    selected_reason_id = 0
    total_bills_amount= 0
    for bill in bills:
        if bill.total_amount:
            total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

        try:
            user_object = GreenBillUser.objects.get(id = bill.flag_by)
            flag_by_name = user_object.first_name + ' ' + user_object.last_name
        except:
            flag_by_name = ""

        # print(flag_by_name)
        bill.flag_by_name = flag_by_name

    if request.method == "POST":
        # print('check')
        user = request.POST['user']
        from_date = request.POST['from_date']
        from_date_temp = from_date
        to_date = request.POST['to_date']
        to_date_temp = to_date
        reason_id = request.POST['reason_id']

        new_data = []

        if reason_id:
            bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile.id, bill_flag = True, reason_id = reason_id).order_by('-id')
            bills_count = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile.id, bill_flag = True, reason_id = reason_id).count()
            selected_reason_id = reason_id
        else:
            selected_reason_id = 0
        # print('okkkkkkkkkkkk')
        if bills:
            # print('check1')

            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')

            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            total_bills_amount = 0
            for bill in bills:

                if user or from_date or to_date:

                    if user and from_date and to_date:
                        if bill.flag_by == user:
                            if bill.date >= from_date and bill.date <= to_date:
                                new_data.append(bill)
                                if bill.total_amount:
                                   total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

                    elif from_date and to_date:
                        if bill.date >= from_date and bill.date <= to_date:
                            new_data.append(bill)
                            if bill.total_amount:
                                total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

                    elif user and from_date :
                        if bill.flag_by == user and bill.date >= from_date:
                            new_data.append(bill)
                            if bill.total_amount:
                                total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

                    elif user and to_date:
                        if bill.flag_by == user and bill.date <= to_date:
                            new_data.append(bill)
                            if bill.total_amount:
                                total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

                    elif from_date:
                        if bill.date >= from_date:
                            new_data.append(bill)
                            if bill.total_amount:
                                total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

                    elif to_date:
                        if bill.date <= to_date:
                            new_data.append(bill)
                            if bill.total_amount:
                                total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

                    elif user:
                        if bill.flag_by == user:
                            new_data.append(bill)
                            if bill.total_amount:
                                total_bills_amount = float(total_bills_amount) + float(bill.total_amount)

                else:
                    new_data.append(bill)
                    if bill.total_amount:
                                total_bills_amount = float(total_bills_amount) + float(bill.total_amount)


            total_flag_bills = 0

            if user:
                # print('333')
                for bill in new_data:
                    if bill.bill_flag == True:
                        total_flag_bills = total_flag_bills + 1

                context = {
                    'flag_bills':new_data,
                    'total_bills_amount': total_bills_amount,
                    'bills_count': bills_count,
                    # 'ParkingLotNavclass': "active",
                    # 'ParkingLotCollapseShow': "show",
                    'BillInfoNavClass':'active',
                    "BillInfoCollapseShow": "show",
                    'ParkingFlagBillsNavClass': "active",
                    'merchant_user': merchant_user,
                    'total_flag_bills':total_flag_bills,
                    'custom_user':int(user),
                    'from_date': from_date_temp,
                    'to_date': to_date_temp,
                    'flag_reasons': flag_reasons,
                    'selected_reason_id' : int(selected_reason_id),
                }
                return render(request, "merchant/parking-flag-bills.html", context)

            else:
                # print('222')
                context = {
                    'flag_bills':new_data,
                    'total_bills_amount': total_bills_amount,
                    'bills_count': bills_count,
                    # 'ParkingLotNavclass': "active",
                    # 'ParkingLotCollapseShow': "show",
                    'BillInfoNavClass':'active',
                    "BillInfoCollapseShow": "show",
                    'ParkingFlagBillsNavClass': "active",
                    'merchant_user': merchant_user,
                    'from_date': from_date_temp,
                    'to_date': to_date_temp,
                    'flag_reasons': flag_reasons,
                    'selected_reason_id' : int(selected_reason_id),
                }
                return render(request, "merchant/parking-flag-bills.html", context)

        return render(request, "merchant/parking-flag-bills.html")
    else:
        # print('111')

        context = {
                'flag_bills':bills,
                'total_bills_amount': total_bills_amount,
                'bills_count': bills_count,
                # 'ParkingLotNavclass': "active",
                # 'ParkingLotCollapseShow': "show",
                'BillInfoNavClass':'active',
                "BillInfoCollapseShow": "show",
                'ParkingFlagBillsNavClass': "active",
                'merchant_user': merchant_user,
                'flag_reasons': flag_reasons,
                'selected_reason_id' : selected_reason_id,
            }

        return render(request, "merchant/parking-flag-bills.html", context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deletePArkingFlagBill(request, id):
    if request.method == "POST":
        data = SaveParkingLotBill.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Bill deleted Successfully !!!', timer=1500)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Bill!!!', timer=1500)
        
    return redirect(parking_flag_bills)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deleteSelectedParkingFlagBills(request):

    if request.method == "POST":

        bill_ids = request.POST.getlist('bill_id[]')
        
        if bill_ids:
            for bill_id in bill_ids:
                result = SaveParkingLotBill.objects.filter(id = bill_id).delete()
                result = True
        else:
            result = False
        
        if result:
            sweetify.success(request, title="Success", icon='success', text='Bills deleted Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="error", icon='error', text='Please Select Bill !!!', timer=1500)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Bill!!!', timer=1500)
        
    return redirect(parking_flag_bills)

def update_parking_rating_view(request, id):
    rating = request.POST["rating"]
    bill_details = SaveParkingLotBill.objects.filter(bill_url=id).update(rating = rating)
    return JsonResponse({'status':'success'})

def update_petrol_rating_view(request, id):
    rating = request.POST["rating"]
    bill_details = SavePetrolPumpBill.objects.filter(bill_url=id).update(rating = rating)
    return JsonResponse({'status':'success'})


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def exitParkedVehicles(request):

    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    if request.method == "POST":

        bill_ids = request.POST.getlist('bill_id[]')
        
        if bill_ids:
            for bill_id in bill_ids:
                result = SaveParkingLotBill.objects.filter(id = bill_id).update(exit_check = True)
                result = True
        else:
            result = False
        
        if result:
            sweetify.success(request, title="Success", icon='success', text='Vehicle Exited Successfully  !!!', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Failed to Set !!!', timer=1500)

    # parking_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id.id, exit_check = False, exit_gate = 'true').order_by('-id')
    parking_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id.id, exit_check = False, manage_space = True).order_by('-id')


    context = {
        'parking_bills' : parking_bills,
        'ParkingLotNavclass': "active",
        'ParkingLotCollapseShow': "show",
        'ExitParkedVehiclesNavclass': "active"
    }
    
    return render(request, "merchant/exit-parked-vehicles.html", context)



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def addParkingPassCharges(request):
    
    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

    form = MerchantParkingLotPassChargesForm()

    business_logo = merchant_general_setting.m_business_logo

    business_name = merchant_general_setting.m_business_name

    parking_lot_passes = ParkingLotPass.objects.filter(m_business_id = merchant_general_setting.id).order_by('-id')
    total_count = ParkingLotPass.objects.filter(m_business_id = merchant_general_setting.id).count()

    for parking_pass in parking_lot_passes:

        try:
            user_object = GreenBillUser.objects.get(id = parking_pass.m_user_id)
            parking_pass.created_by = user_object.first_name + ' ' + user_object.last_name
        except:
            parking_pass.created_by = ""

        parking_pass.qr_code = "GreenBill~Parking Pass~" + str(parking_pass.id)

    context = {
        'form': form,
        'merchant_general_setting_id': merchant_general_setting.id,
        'parking_lot_passes':parking_lot_passes,
        # 'ParkingLotNavclass': 'active',
        # "ParkingLotCollapseShow": "show",
        # "PassExpanded" : "true",
        # "PassCollpseShow" : "show",
        'ParkingPassesNavclass':'active',
        'PassesCollapseShow':'show',
        "MerchantPassNavclass": "active",
        "business_logo": business_logo,
        "business_name": business_name,
        'total_count': total_count,
    }
    return render(request, "merchant/merchant_pass/merchant_passes.html", context)


def DeletePass(request,id):
    if request.method == "POST":
        data = ParkingLotPass.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Pass deleted Successfully !!!', timer=1000)
        return redirect('/merchant-passes/')
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete pass !!!', timer=1000)
        return redirect('/merchant-passes/')



def DeleteParkingPassCharges(request,id):
    if request.method == "POST":
        data = MerchantParkingLotPassCharges.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Pass Charge deleted Successfully !!!', timer=1000)
        return redirect('/merchant-passes/')
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete pass charge !!!', timer=1000)
        return redirect('/merchant-passes/')

# def GetAllParkingPassCharges(request):

#     if request.method == "POST":
#         form = MerchantParkingLotPassChargesForm(request.POST)
#         if form.is_valid():
#             m_business_id = form.cleaned_data.get("m_business_id")
#             #vehicle_type = form.cleaned_data.get('vehicle_type')
#             # per_visit_charges = form.cleaned_data.get('per_visit_charges')
#             monthly_charges = form.cleaned_data.get('monthly_charges')
#             half_yearly_charges = form.cleaned_data.get('half_yearly_charges')
#             quarterly_charges = form.cleaned_data.get('quarterly_charges')
#             yearly_charges = form.cleaned_data.get('yearly_charges')
#             per_visit_charges = ""

#             result = MerchantParkingLotPassCharges.objects.update_or_create(m_business_id = m_business_id, defaults={'per_visit_charges' : per_visit_charges,'monthly_charges' : monthly_charges,"quarterly_charges" : quarterly_charges,'half_yearly_charges':half_yearly_charges,"yearly_charges":yearly_charges})

#             if result:
#                 sweetify.success(request, title="Success", icon='success',
#                              text='Pass Charges added successfully !!!')
#             else:
#                 sweetify.error(request, title="Error", icon='error',
#                              text='Failed to add charges')
#         else:
#             sweetify.error(request, title="Error", icon='error',
#                              text='Something went to wrong')

#     form = MerchantParkingLotPassChargesForm()

#     merchant_users_object = Merchant_users.objects.get(user_id = request.user)

#     merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

#     print(merchant_general_setting)

#     try:
#         passcharges = MerchantParkingLotPassCharges.objects.filter(m_business_id = merchant_general_setting.id)
#         per_visit_charges = passcharges[0].per_visit_charges
#         monthly_charges = passcharges[0].monthly_charges
#         quarterly_charges = passcharges[0].quarterly_charges
#         half_yearly_charges = passcharges[0].half_yearly_charges
#         yearly_charges = passcharges[0].yearly_charges

#     except:
#         passcharges = ""
#         per_visit_charges = ""
#         monthly_charges = ""
#         quarterly_charges = ""
#         half_yearly_charges = ""
#         yearly_charges = ""

#     context = {
#                 "passcharges":passcharges,
#                 "per_visit_charges": per_visit_charges,
#                 "monthly_charges" : monthly_charges,
#                 "quarterly_charges" : quarterly_charges,
#                 "half_yearly_charges" : half_yearly_charges,
#                 "yearly_charges" : yearly_charges,
#                 'ParkingPassChargesForm': form,
#                 'merchant_general_setting_id': merchant_general_setting.id,
#                 # 'ParkingLotNavclass': 'active',
#                 # "ParkingLotCollapseShow": "show",
#                 # "PassExpanded" : "true",
#                 # "PassCollpseShow" : "show",
#                 'ParkingPassesNavclass':'active',
#                 'PassesCollapseShow':'show',
#                 "ParkingPassChargesNavclass": "active"
#                }

#     return render(request,"merchant/merchant_parking_pass_charge_list.html", context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def GetAllParkingPassCharges(request):

    if request.method == "POST":

        m_business_id = request.POST["m_business_id"]

        vehicle_type_id = request.POST["vehicle_type"]

        pass_type = request.POST["pass_type"]

        charges = request.POST["charges"]

        charges_available = MerchantParkingLotPassCharges.objects.filter(m_business_id = m_business_id, vehicle_type_id = vehicle_type_id, pass_type = pass_type)

        if charges_available:
            sweetify.error(request, title="Error", icon='error', text='Charges already Available !!!')

        else:
            vehicle_type_temp = MerchantParkingAddVehicle.objects.filter(id = vehicle_type_id)
            vehicle_type_name = vehicle_type_temp[0].vehicle_type
            result = MerchantParkingLotPassCharges.objects.create(m_business_id = m_business_id, vehicle_type_id = vehicle_type_id, vehicle_type = vehicle_type_name, pass_type = pass_type, charges = charges)

            if result:
                sweetify.success(request, title="Success", icon='success', text='Pass Charges added Successfully !!!')
            else:
                sweetify.error(request, title="Error", icon='error', text='Failed to add charges')

    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

    m_business_id = merchant_general_setting.id

    vehicle_type_list = MerchantParkingAddVehicle.objects.filter(m_business_id = m_business_id)

    pass_type_list = []

    pass_type_list.append({'name': 'Monthly Pass'})

    pass_type_list.append({'name': 'Quarterly Pass'})

    pass_type_list.append({'name': 'Half Yearly Pass'})

    pass_type_list.append({'name': 'Yearly Pass'})

    pass_type_list.append({'name': 'Employee Pass'})

    pass_type_list.append({'name': 'Visitor Pass'})

    pass_charges_list = MerchantParkingLotPassCharges.objects.filter(m_business_id = m_business_id)

    context = {
        'merchant_general_setting_id': merchant_general_setting.id,
        "vehicle_type_list":vehicle_type_list,
        "pass_type_list": pass_type_list,
        "pass_charges_list" : pass_charges_list,
        'ParkingPassesNavclass':'active',
        'PassesCollapseShow':'show',
        "ParkingPassChargesNavclass": "active",
    }    

    return render(request,"merchant/merchant-parking-pass-charges.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deleteParkingPassCharges(request, id):
    if request.method == "POST":
        data = MerchantParkingLotPassCharges.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Charges deleted Successfully !!!', timer=1000)
        return redirect(GetAllParkingPassCharges)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Charges !!!', timer=1000)
        return redirect(GetAllParkingPassCharges)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def getHeaderFooterDetail(request):

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    merchant_bussiness = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    if request.method == "POST":

        try: 
            data = petrol_pump_app_setting_model.objects.get(merchant_id = merchant_object, merchant_bussiness = merchant_bussiness)
            arr = {
                'header1': data.header_text1,
                'header2': data.header_text2,
                'header3': data.header_text3,
                'footer1': data.footer_text1,
                'footer2': data.footer_text2,
                'footer3': data.footer_text3,
            }
        except: 
            arr = ""

        return JsonResponse({'status': "success",'arr':arr})
    else:
        return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def addFlagReason(request):

    if request.method == "POST":

        reason = request.POST["reason"]

        m_business_id = request.POST["m_business_id"]

        check = flagbillreason.objects.filter(m_business_id= m_business_id, reason = reason)

        if check:
            return JsonResponse({'status': 'error', 'msg': "Reason already exists !!!"})

        else:
        
            result = flagbillreason.objects.create(m_business_id= m_business_id, reason = reason)

            if result:
                return JsonResponse({'status': 'success', 'msg': "Reason added successfully !!!"})
        
    else:

        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

        try:
            data= flagbillreason.objects.filter(m_business_id = merchant_general_setting.id)
        except:
            data = ""

        context = {
            'flag_msg_list' : data,
            'SettingNavclass': "active",
            'settingsCollapseShow': "show",
            'FlagReasonsNavClass': "active",
            'merchant_general_setting_id': merchant_general_setting.id
        }

        return render(request, "merchant/add-flag-reason.html", context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deleteFlagReason(request, id):
    if request.method == "POST":
        data = flagbillreason.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Reason deleted Successfully !!!', timer=1000)
        return redirect(addFlagReason)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Reason !!!', timer=1000)
        return redirect(addFlagReason)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def addPassCompaniesName(request):

    if request.method == "POST":
        max_length = 30
        company_name = request.POST["company_name"]

        m_business_id = request.POST["m_business_id"]
        if company_name:
            if len(company_name) <= max_length:
                result = CompniesName.objects.create(m_business_id= m_business_id, company_name = company_name)

                if result:
                    return JsonResponse({'status': 'success', 'msg': "Company added successfully !!!"})
                else:
                    return JsonResponse({'status': 'error', 'msg': "Failed to add Company !!!"})
            else:
                msg = "Please add company name with 12 characters."
    else:

        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

        try:
            data= CompniesName.objects.filter(m_business_id = merchant_general_setting.id)
        except:
            data = ""

        context = {
            'companies_list' : data,
            'ParkingPassesNavclass': "active",
            'PassesCollapseShow': "show",
            'ManageCompaniesNavClass': "active",
            'merchant_general_setting_id': merchant_general_setting.id
        }

        return render(request, "merchant/add-companies.html", context)

# @login_required(login_url="/merchant-login/")
# @user_passes_test(is_merchant_or_merchant_staff)
# def addPassCompaniesName(request):

#     if request.method == "POST":
#         max_length = 13
#         company_name = request.POST["company_name"]

#         m_business_id = request.POST["m_business_id"]
        
#         result = CompniesName.objects.create(m_business_id= m_business_id, company_name = company_name)

#         if result:
#             return JsonResponse({'status': 'success', 'msg': "Company added successfully !!!"})
#         else:
#             return JsonResponse({'status': 'error', 'msg': "Failed to add Company !!!"})
#     else:

#         merchant_users_object = Merchant_users.objects.get(user_id = request.user)

#         merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

#         try:
#             data= CompniesName.objects.filter(m_business_id = merchant_general_setting.id)
#         except:
#             data = ""

#         context = {
#             'companies_list' : data,
#             'ParkingPassesNavclass': "active",
#             'PassesCollapseShow': "show",
#             'ManageCompaniesNavClass': "active",
#             'merchant_general_setting_id': merchant_general_setting.id
#         }

#         return render(request, "merchant/add-companies.html", context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def deletePassCompany(request, id):
    if request.method == "POST":
        data = CompniesName.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Company deleted Successfully !!!', timer=1000)
        return redirect(addPassCompaniesName)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Company !!!', timer=1000)
        return redirect(addPassCompaniesName)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_payment_setting(request):

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']
    print(merchant_id)
    business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)
    print(business_object.id)
    try:

        data_avaible = MerchantPaymentSetting.objects.get(m_business_id = business_object.id)

        print(data_avaible)
    except:
        data_avaible = ""

    print(data_avaible)
    # choice_temp = data.option
    
    if request.method == "POST":
        choice = ""
        payu_key = request.POST['payu_key']
        payu_salt = request.POST['payu_salt']
        upi_id = request.POST['upi_id']
        choice= request.POST['choices']
        
        # print("(****************************)")
        # print(payu_key,payu_salt,upi_id,upi_check,payu_check,choice)


        if 1==1:
            if request.user.is_merchant_staff == True :
                if data_avaible == "":
                    print("In if")
                    print(choice,upi_id,payu_key)
                    MerchantPaymentSetting.objects.create(m_business_id = business_object.id,payu_key= payu_key, payu_salt= payu_salt, upi_id= upi_id ,option = choice) 
                else:
                    print("In else")
                    data_avaible = MerchantPaymentSetting.objects.get(m_business_id = business_object.id)
                    print(data_avaible)
                    data_avaible.upi_id = upi_id
                    data_avaible.payu_key = payu_key
                    data_avaible.payu_salt = payu_salt
                    data_avaible.option = choice
                    data_avaible.save()
                    # data_avaible.objects.update( payu_key=payu_key, payu_salt= payu_salt, upi_id=upi_id)

                sweetify.success(request, title="Success", icon='success', text='Payment Setting Stored Successfully !!!')
                return redirect('/merchant-payment-settings/')

            else:
                sweetify.error(request, title="error", icon='error', text='You do not have sufficient priviledge to change these settings')
                return redirect('/merchant-payment-settings/')
        
    else:

        try:
            print("inn try ")
            data = MerchantPaymentSetting.objects.get(m_business_id = business_object.id)
            print(data)
            choice = data.option
            print("Done SuccessFully")
        except:
            data = ""
           
            print("Problem saving data")

        # form = PaymentSettingForm(initial={"payu_key": "-1","payu_salt":"-1","upi_id":"-1"})

        context = {
            # 'form' : form, 
            'data' : data,
            'option':choice,
            "SettingNavclass": "active",
            "settingsCollapseShow": "show",
            'paymentSettingActiveClass': "active"
        }
        print(context)
        return render(request, "merchant/payment_setting.html", context)