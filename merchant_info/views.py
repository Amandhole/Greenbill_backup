import sweetify
import sys
from django.contrib import messages #import messages
from django.shortcuts import render, redirect, get_object_or_404
from users.models import GreenBillUser, MerchantProfile, Merchant_users, MerchantUniqueIds
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django import template
from django.template import loader
from .forms import *
from merchant_setting.forms import MerchnatgeneralSettingForm
from authentication.forms import MerchantSignUpForm, MerchantSignUpOtherDetailsForm
from category_and_tags.models import business_category
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner, is_merchant_or_merchant_staff
from django.db.models import Subquery
from role.models import userrole 
import random
import string
import time
from customer_info.models import Customer_Info_Model
from django.core.mail import send_mail
from owner_notice_board.sendsms import *
from merchant_role.models import *
from merchant_payment.models import PaymentLinks

from .models import *
from django.utils.html import strip_tags
from django.conf import settings
from owner_notice_board.models import OnwerNoticeBoard,OwnerSentNotice

from users.models import Merchant_users, MerchantProfile, GreenBillUser
from merchant_software_apis.models import *
from petrol_pump_apis.models import SavePetrolPumpBill
from parking_lot_apis.models import SaveParkingLotBill
from datetime import datetime
from django.utils import formats

from bill_design.models import *
from my_subscription.models import *
from django.db.models import Q
from datetime import datetime, timedelta

# SMS
import requests
import time
import pyshorteners
from offers.models import OfferModel 
from coupon.models import *
from role.models import role, userrole
from merchant_cashmemo_design.models import *
from authentication.models import *
from referral_points.models import *


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Edit_all_merchant_information(request):
    
    if request.method == "POST":
        form = merchantEditBusinessesForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            user_id = request.POST['user_id']
            business_id = request.POST['merchant_setting_id']
            
            m_business_name = form.cleaned_data.get("m_business_name")
            m_business_category = form.cleaned_data.get("m_business_category")
            m_pin_code = form.cleaned_data.get("m_pin_code")
            m_state = form.cleaned_data.get("m_state")
            m_district = form.cleaned_data.get("m_district")
            m_city = form.cleaned_data.get("m_city")
            m_area = form.cleaned_data.get("m_area")
            m_address = form.cleaned_data.get("m_address")
            m_landline_number = form.cleaned_data.get("m_landline_number")
            m_alternate_mobile_number = form.cleaned_data.get("m_alternate_mobile_number")
            m_company_email = form.cleaned_data.get("m_company_email")
            m_alternate_email = form.cleaned_data.get("m_alternate_email")
            m_pan_number = form.cleaned_data.get("m_pan_number")
            m_gstin = form.cleaned_data.get("m_gstin")
            m_cin = form.cleaned_data.get("m_cin")
            m_bank_account_number = form.cleaned_data.get("m_bank_account_number")
            m_bank_IFSC_code = form.cleaned_data.get("m_bank_IFSC_code")
            m_bank_name = form.cleaned_data.get("m_bank_name")
            m_bank_branch = form.cleaned_data.get("m_bank_branch")
            m_GSTIN_certificate = form.cleaned_data.get("m_GSTIN_certificate")
            m_CIN_certificate = form.cleaned_data.get("m_CIN_certificate")
            m_business_logo = form.cleaned_data.get("m_business_logo")
            m_business_stamp = form.cleaned_data.get("m_business_stamp")
            m_digital_signature = form.cleaned_data.get("m_digital_signature")
            
            result = MerchantProfile.objects.filter(id=business_id, m_user_id=user_id).update(m_business_name = m_business_name, m_business_category_id = m_business_category, m_city = m_city, m_district = m_district, m_state = m_state, m_pin_code = m_pin_code, m_area= m_area, m_address=m_address, m_landline_number=m_landline_number, m_alternate_mobile_number=m_alternate_mobile_number, m_company_email=m_company_email, m_alternate_email=m_alternate_email, m_pan_number=m_pan_number, m_gstin=m_gstin, m_cin=m_cin, m_bank_account_number=m_bank_account_number, m_bank_IFSC_code=m_bank_IFSC_code, m_bank_name=m_bank_name, m_bank_branch=m_bank_branch)

            if m_GSTIN_certificate:
                MerchantProfile.objects.update_or_create(id = business_id, defaults={ "m_GSTIN_certificate" : m_GSTIN_certificate })

            if m_CIN_certificate:
                MerchantProfile.objects.update_or_create(id = business_id, defaults={ "m_CIN_certificate" : m_CIN_certificate })
            
            if m_business_logo:
                MerchantProfile.objects.update_or_create(id = business_id, defaults={ "m_business_logo" : m_business_logo })

            if m_business_stamp:
                MerchantProfile.objects.update_or_create(id = business_id, defaults={ "m_business_stamp" : m_business_stamp })

            if m_digital_signature:
                MerchantProfile.objects.update_or_create(id = business_id, defaults={ "m_digital_signature" : m_digital_signature })
        
            if result:
                sweetify.success(request, title="Success", icon='success', text='Merchant business information updated sucessfully. !!!')
                return redirect('/view-all-merchant-info-record/'+user_id+'/')
                # return JsonResponse({'status':'success', 'msg': "Merchant business information updated sucessfully."})
            else:
                sweetify.error(request, title="error", icon='error', text='Unable to update business information.', timer=1000)
                return redirect('/view-all-merchant-info-record/'+user_id+'/')
                # return JsonResponse({'status':'error', 'msg': "Unable to update business information."})
        else:
            sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
            return redirect('/view-all-merchant-info-record/'+user_id+'/')
            # return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})
    else:
        sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
        return redirect('/view-all-merchant-info-record/'+user_id+'/')
        # return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def view_all_Merchant_Details(request, id=None):
    if request.method == "GET":
        merchantBusinessesList = MerchantProfile.objects.get(id=id)
        form = merchantEditBusinessesForm()
        print('list',merchantBusinessesList.m_user)
        print(id)
        merchnat_business_category = business_category.objects.all()

    if request.method == "POST":
        
        form = MerchnatgeneralSettingForm(request.POST, request.FILES)
        merchantBusinessesList = MerchantProfile.objects.get(id=id)
        print(form.errors)

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
            # cancel_bank_cheque_photo = form.cleaned_data.get("cancelled_cheque_certificate")
            other_document1 = form.cleaned_data.get("other_document1")
            other_document2 = form.cleaned_data.get("other_document2")
            other_document_certificate2 = form.cleaned_data.get("other_document_certificate2")
            udyog_adhar_certificate = request.FILES.get('udyog_adhar_certificate')
            cancel_bank_cheque_photo = request.FILES.get('cancelled_cheque_certificate')
            address_proof = request.FILES.get('address_proof')
            m_bank_account_entry = form.cleaned_data.get("m_bank_account_entry")
            m_address_bank_account = form.cleaned_data.get("m_address_bank_account")
            schedule_pdf_upload = form.cleaned_data.get("schedule_pdf_upload")
            bank_account_entity_m1 = form.cleaned_data.get("bank_account_entity_m1")
            bank_account_entity_adress2 = form.cleaned_data.get("bank_account_entity_adress2")

            print('cancel_bank_cheque_photo')
            print(cancel_bank_cheque_photo)
            print('GSTIN_certificate',GSTIN_certificate)

            business_category_object = business_category.objects.get(id=business_category_temp)
            print('xvc')
            print(business_name)
            # print(MerchantProfile.objects.get(m_user=merchantBusinessesList.m_user,m_business_name=business_name))
            MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={'m_business_name': business_name, 
                'm_business_category': business_category_object, 'm_pin_code': pin_code, 'm_city': city, 'm_area': area ,
                'm_district': district, 'm_state': state, 'm_address': address, 'm_landline_number': landline_number,
                'm_alternate_mobile_number': alternate_mobile_number, 'm_company_email': company_email, 'm_alternate_email' : alternate_email,
                'm_pan_number': pan_number, 'm_gstin': gstin, 'm_cin': cin, 'm_bank_account_number': bank_account_number, 
                # 'm_other_document_certificate1':udyog_adhar_certificate,
                # 'm_GSTIN_certificate':GSTIN_certificate, 'm_CIN_certificate':CIN_certificate,'m_cancel_bank_cheque_photo':cancel_bank_cheque_photo,
                'm_bank_IFSC_code': bank_IFSC_code, 'm_bank_name' : bank_name, 'm_bank_branch' : bank_branch, 'Entity_Account_m': bank_account_entity_m1, 'Entity_Bank_Account_m': bank_account_entity_adress2, 'm_vat_tin_number':tin_vat_number,
                'm_aadhaar_number':aadhaar,"m_other_document1":other_document1,"m_other_document2":other_document2})
           
           
            # for all in MerchantProfile.objects.filter(m_user=merchantBusinessesList.m_user,m_business_name=business_name):
                
            #     print(all, all.id)

            #     MerchantProfile.objects.update_or_create(id = all.id, defaults={ 
            #     'm_alternate_mobile_number': alternate_mobile_number, 'm_company_email': company_email, 'm_alternate_email' : alternate_email,
            #     'm_pan_number': pan_number, 'm_gstin': gstin, 'm_cin': cin, 'm_bank_account_number': bank_account_number, 
            #     'm_bank_IFSC_code': bank_IFSC_code, 'm_bank_name' : bank_name, 'm_bank_branch' : bank_branch,'m_vat_tin_number':tin_vat_number,
            #     'm_aadhaar_number':aadhaar,"m_other_document1":other_document1,"m_other_document2":other_document2})

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

            if udyog_adhar_certificate:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_other_document_certificate1" : udyog_adhar_certificate })
            
            if address_proof:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "address_proof" : address_proof })

            if m_bank_account_entry:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_bank_account_entry" : m_bank_account_entry })

            if m_address_bank_account:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_address_bank_account" : m_address_bank_account })

            if schedule_pdf_upload:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "schedule_pdf_upload" : schedule_pdf_upload })

             
            sweetify.success(request, title="Success", icon='success',
                             text='General Setting Stored Successfully !!!', timer=1000)

            return HttpResponseRedirect('/view-all-merchant-info-record/'+str(id)+'/')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!', timer=1000)
            return HttpResponseRedirect('/view-all-merchant-info-record/'+str(id)+'/')
    else:
        
        # merchant_users_object = Merchant_users.objects.get(user_id = merchantBusinessesList.m_user  )
        # print('obj',merchant_users_object.id)
        print('QQQ')
        print(id)
        merchant_general_setting = MerchantProfile.objects.get(id = id)
        print(merchant_general_setting)
        merchnat_business_category = business_category.objects.all()
        States = StateCityData.objects.values('state').distinct().order_by('state')
        form1 = MerchnatgeneralSettingForm()
        context = {
            # 'merchantBusinessesList' : merchantBusinessesList,
            'merchantBusinessCategory' : merchnat_business_category,
            'merchantBusinessCategory' : merchnat_business_category,
            'form': form1,
            'States': States,
            'merchantNavActiveClass': "active", 
            'MerchantInfoCollapseShow': "show",
            'MerchantLatestNavclass': "active",
            'merchant_general_setting': merchant_general_setting, 
            'merchnat_business_category': merchnat_business_category, 
        }
        return render(request, "super_admin/edit-all-details-of-merchant.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def merchant_info(request):
    
    if request.method == "GET":
        qs = business_category.objects.all().order_by('business_category_name')
        
        form = MerchantSignUpForm(request.POST)
        form1 = MerchantSignUpOtherDetailsForm(request.POST)
        
        # To get only unique values
        merchantList = MerchantProfile.objects.all().distinct().order_by('-id')
        data = MerchantDisablereasons.objects.all()
        Partner = PartnerProfile.objects.all()
        # Partner_Software = PartnerProfile.objects.values('Software Partner')
        # Partner_Marketing = PartnerProfile.objects.values('Marketing Partner')
        print("**************************************")
        # print(Partners)
        # To avoid duplicates entries by m_user
        newMerchantList = MerchantProfile.objects.filter(m_user_id__isnull = False,m_disabled_account=False )

        total_merchant_count = MerchantProfile.objects.filter(m_user_id__isnull=False,m_disabled_account=False).count() #.exclude(id__in=Subquery(merchantList.values('m_user_id')[1:])).count()
        # total_merchant_count = MerchantProfile.objects.all().count()
        States = StateCityData.objects.values('state').distinct().order_by('state')

        data = []
        parnter_name = '----'

        for merchant in newMerchantList:
            try:
                recharge_his = recharge_history.objects.filter(merchant_id = merchant.m_user).last()
                merchant.subscription_type = recharge_his.subscription_name
            except:
                merchant.subscription_type = "----------"
            
            merchant_object = GreenBillUser.objects.get(mobile_no = merchant.m_user)
            merchant.date_joined = merchant_object.date_joined
            if merchant.merchant_by_partner:
                continue
                # merchant.parnter_name = PartnerProfile.objects.get(p_user=merchant.merchant_by_partner).p_business_name
            else:
                merchant.parnter_name = '----'

            # print("(***W27777777")
            # print(merchant.m_user)
            # if merchant_object.mobile_no == "9970777739":
            #     print("(***W27777777")
            #     merchant.m_user.m_email = "aniketa2@gmail.com"
            #     merchant.m_user.save()

        # partner_type = ['Marketing Partner','Software Partner']
        partner_type = ['Software Partner','Marketing Partner']

        context = {
         'merchant_list': list(newMerchantList)[::-1] ,
         'merchantNavActiveClass': "active", 
         'MerchantInfoCollapseShow': "show",
         'MerchantListNavclass': "active",
         'form': form,
         'form1': form1, 
         'business_category_list' : qs,
         "total_merchant": total_merchant_count,
         "data" : data,
         "States": States,
         'bulkMailSmsMerchantForm':bulkMailSmsMerchantForm,
         'Partner_type':partner_type
         }

        return render(request, "super_admin/merchant-info.html", context)
    else: 
    
        return JsonResponse({'success': False})


def ViewMerchantOffers(request, id):

    merchant_business_id = MerchantProfile.objects.get(id = id)

    data_status = OfferModel.objects.filter(merchant_business_id = merchant_business_id).order_by('-id')

    total_offers = OfferModel.objects.filter(offer_panel='merchant', merchant_business_id = merchant_business_id).count()
    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        offer_amount = data.offer_amount
    else:
        offer_amount = 0
    waiting_offers = OfferModel.objects.filter(offer_panel='merchant', status=0, merchant_business_id = merchant_business_id).count()
    approve_offers = OfferModel.objects.filter(offer_panel='merchant', status=1, merchant_business_id = merchant_business_id).count()
    today = date.today()
    for offer in data_status:
        if offer.valid_through < today:

            offer.expire_status=True
        else:
            offer.expire_status=False

        if offer.customer_merchant_count:
                offer.total_amount = int(offer_amount) * int(offer.customer_merchant_count)

    context = {
    "data_status" : data_status,
    'total_offers': total_offers,
    'waiting_offers': waiting_offers,
    'approve_offers': approve_offers,
    'PromotionNavclass': "active", 
    'PromotionCollapseShow': "show",
    'OfferstatusNavclass': "active",
    }
    return render(request, "owner_offerstatus/status.html", context)


def ViewMerchant_couponList(request, id):

    coupon_list = CouponModel.objects.filter(coupon_panel='merchant', merchant_business_id = id).order_by('-id')
    total_count = CouponModel.objects.filter(coupon_panel='merchant', merchant_business_id = id).count()
    today = date.today()
    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        coupon_amount = data.coupon_amount
    else:
        coupon_amount = 0
    for coupon in coupon_list:

        if coupon.valid_through < today:
            coupon.expiry_status = True
        else:
            coupon.expiry_status = False
            
        coupon.coupon_redeem_count = RedeemCouponModel.objects.filter(coupon_id=coupon.id).count()

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
                coupon.total_amount = int(coupon_amount) * int(coupon.total_customers)


    context = {
        
        'total_count': total_count,
       'coupon_list':coupon_list,
       'PromotionNavclass':'active',
       'PromotionCollapseShow':'show',
       'CouponListNavclass':'active',
    }


    return render(request, "coupon_list.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def sendMechantNotice(request):
    if request.method == "POST":
        title = request.POST.get('title')
        message = request.POST.get('message')
        # mobile_no = request.POST.get('mobile_number')
        # email = request.POST.get('email_id')
        smsheader = request.POST.get('smsheader')
        template_id = request.POST.get('template')
        id = request.POST.get('id')
        number = MerchantProfile.objects.get(id =id).m_user
       
       
        individual = GreenBillUser.objects.get(mobile_no=number, is_merchant=True)

        email = individual.email
        print('EMAIL',email)
        sent_notice = request.POST.getlist('sentnotice')
        print('sent_notice',sent_notice)
        individual_user = number
        print('individual user', individual_user)
        print('title',title)
     
        print('message',message)
       
        
        print(individual_user)  
        if individual_user :
            print('OWNER')
            
       
         
            for notice in sent_notice:
                    # if notice == "sms":
                    #     notice_id = bulkMailSmsMerchantModel.objects.create(
                    #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_sent_sms=True)

                    # elif notice == "sent_mail":
                    #     notice_id = bulkMailSmsMerchantModel.objects.create(
                    #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_sent_mail=True)

                    # else:
                    #     notice_id = bulkMailSmsMerchantModel.objects.create(
                    #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_notification=True)

                if notice == "sms":
                        
                        notice_id = bulkMailSmsMerchantModel.objects.update_or_create(owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template_id, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template,'o_sent_sms':True })

                elif notice == "sent_mail":
                        
                        notice_id = bulkMailSmsMerchantModel.objects.update_or_create(owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template_id, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template, 'o_sent_mail':True })

                else:
                    notice_id = OnwerNoticeBoard.objects.update_or_create(owner_id=request.user, notice_title=title, message=message, defaults= { 'notice_title':title,  'message':message, 'o_notification':True })

                    print(notice_id[0].id)

                    notice_object = OnwerNoticeBoard.objects.get(id= notice_id[0].id)
                    print('notice_object::',notice_object)
          

                             
            if individual_user:
                    for notice in sent_notice:
                            
                            if notice == "sms":
                                contact = number
                                # contact = 7387810242
                                message = strip_tags(message)
                                # message = 'Thank you for registering on Green Bill. Welcome to the Green Bill Community. Feel free to get in touch with us at www.greenbill.in'
                                if contact:
    
                                    ts = int(time.time())

                                    data_temp = {
                                            "keyword":"Bill Delivery SMS",
                                            "timeStamp":ts,
                                            "dataSet":
                                                [
                                                    {
                                                        "UNIQUE_ID":"GB-" + str(ts),
                                                        "MESSAGE": message,
                                                        "OA":smsheader,
                                                        "MSISDN": contact, # Recipient's Mobile Number
                                                        "CHANNEL":"SMS",
                                                        "CAMPAIGN_NAME":"hind_user",
                                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                        "USER_NAME":"hind_hsi",
                                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                                        "DLT_CT_ID":template_id, # Template Id
                                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                    }
                                                ]
                                            }

                                    url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                    response = requests.post(url, json = data_temp)

                                    print(data_temp)
                                    print(response)
                                    # import urllib
                                    # username = "sanjog1"
                                    # Password = "123456"
                                    # sender = "HINDAG"
                                    # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                    # temp_dict = {"text": temp_message}
                                    # message= urllib.parse.urlencode(temp_dict)
                                    # priority='ndnd'
                                    # stype='normal'

                                    # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                    # import requests

                                    # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                    # res = requests.get(url)

                                    # if response.status_code == 200:
                                    #     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                    # else:
                                    #     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                    # return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                    # print(sms_response)
                                sms_response = sendSMS(str(contact), message)
                                print(sms_response)
                                try:
                                    print('success')
                                        # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        # message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
                                except:
                                        owner_notice_sent_save = ""
                            elif notice == "sent_mail":
                                try:
                                    print("********************")
                                    print("In try")
                                    email_id = email
                                    print(email_id)
                                    email_from = settings.EMAIL_HOST_USER
                                    print('email from',email_from)
                                    recipient_list = [email_id, 'shreyash.t@zappkode.com' ]
                                    # recipient_list = ['shreyash.t@zappkode.com']
                                    print('email to',recipient_list)
                                    message = message
                                   
                                    plain_message = strip_tags(message)
                                    print('sent message:',plain_message)
                                    # print('file',notice_file)
                                    # sendmail = EmailMessage(
                                    #     title, message, email_from, recipient_list)

                                    # sendmail.attach(notice_file.name,
                                    #                 notice_file.read(), notice_file.content_type)

                                    # response = sendmail.send()
                                    send_mail( title, plain_message, email_from, recipient_list)
                                    # print(response)

                                    # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                    #     notice_id=notice_object, user_id=user_object, defaults = {'sent_mail':True})

                                except:
                                    
                                    owner_notice_sent_save = ""
                            else:
                                try:
                                    print('owner_notice_sent_saveowner_notice_sent_save',individual_user)
                                    individual_user_object = GreenBillUser.objects.get(mobile_no=individual_user)
                                    owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                    notice_id=notice_object, user_id=individual_user_object, defaults = {'notification':True})

                                    print('owner_notice_sent_save',owner_notice_sent_save)
                                except:
                                    owner_notice_sent_save = ""


            
            
            sweetify.success(request, title="Success", icon='success',
                                text='Notice Send successfully!', timer=5500)
                # return redirect("/owner_notice_board/")
        else:
                sweetify.error(request, title="Error", icon='error',
                                text="Something Went Wrong!!!", timer=5500)
        # else:
        #     sweetify.error(request, "Please Provide Valid Data")    

    return redirect('merchant-info')







@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def changeStatus(request):
    if request.method == "POST":
        
        user_id = request.POST['id']
        status = request.POST['status']

        GreenBillUser.objects.filter(id=user_id).update(is_active=status)
        return JsonResponse({'status': 1, 'msg': 'Status change successfully'})
        
    else:
        return JsonResponse({'status': 0, 'msg': 'Something went wrong'})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def addMerchantByAdmin(request):
    # print(request.POST)
    # sys.exit()
    if request.method == "POST":

        print("Starting the process......................")
        form = MerchantSignUpForm1(request.POST)

        form1 = MerchantSignUpOtherDetailsForm(request.POST)

        if form.is_valid() and form1.is_valid():
            mobile_no = form.cleaned_data.get("mobile_no")
            try:
                is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
            except:
                is_merchant = ""
            
            if is_merchant:
                return JsonResponse({'status':'error', 'msg': "Merchant with this number is already exists."})
            else:

                try:
                    userRoleDetails = userrole.objects.filter(user = request.user.id)
                except:
                    userRoleDetails[0].role = "Super Admin"

                temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

                user_id = GreenBillUser.objects.create_user(
                    mobile_no = mobile_no,
                    m_email = form.cleaned_data.get('m_email'),
                    password = temp_password,
                )

                if userRoleDetails[0].role == "Sales" :
                    GreenBillUser.objects.filter(mobile_no = user_id).update(is_active=False, created_by= userRoleDetails[0].role)
                else:
                    GreenBillUser.objects.filter(mobile_no = user_id).update(is_active= True)

                letters = string.ascii_letters
                digit = string.digits

                random_string = str(user_id.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
            
                GreenBillUser.objects.filter(mobile_no = user_id).update(is_merchant = 1, is_merchant_staff = 1, merchant_referral_code = random_string)

                # Unique Id Start

                try:
                    last_unique_id = MerchantUniqueIds.objects.all().last()
                except:
                    last_unique_id = ""

                if not last_unique_id:
                    m_unique_id = str("GBM") + str("01").zfill(6)
                    no = 1
                else:
                    last_no = last_unique_id.m_unique_no
                    no = int(last_no) + 1
                    m_unique_id = str("GBM") + str(no).zfill(6)

                unique_id_status = GreenBillUser.objects.filter(mobile_no = user_id).update(m_unique_id = m_unique_id)

                if unique_id_status:
                    MerchantUniqueIds.objects.create(m_unique_no = no)

                # Unique Id End
                
                Merchant_users.objects.create(user_id = user_id, merchant_user_id = user_id)

                m_email = form.cleaned_data.get("m_email")
                print("Moving for 1st sms ........................")
                if m_email:
                    random_string = str(user_id.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(5))
                    email_verification_status = GreenBillUser.objects.filter(mobile_no = user_id).update(email_verification_url = random_string)
                    s = pyshorteners.Shortener()
                    email_verification_url = "http://157.230.228.250/email-verification/"+str(random_string)+"/"
                    short_url = s.tinyurl.short(email_verification_url)
                    # if email_verification_status and short_url:
                    #     subject = 'Account Verification'
                    #     message = f'Thank you for choosing GreenBill. Please click on below link to verify Email Id,\n' + str(short_url) + '\n\nTeam GreenBill'
                    #     email_from = settings.EMAIL_HOST_USER
                    #     recipient_list = [m_email,]
                    #     send_mail( subject, message, email_from, recipient_list)

                m_business_name = form1.cleaned_data.get("m_business_name")
                m_business_category = form1.cleaned_data.get("m_business_category")

                cust_city = form1.cleaned_data.get("m_city")
                m_city = cust_city.capitalize()

                cust_district = form1.cleaned_data.get("m_district")
                m_district = cust_district.capitalize()

                cust_state = form1.cleaned_data.get("m_state")
                m_state = cust_state.capitalize()

                m_pin_code = form1.cleaned_data.get("m_pin_code")

                cust_area = form1.cleaned_data.get("m_area")
                m_area = cust_area.capitalize()
                loyalti_point_status = form1.cleaned_data.get("loyalty_point")

                MerchantProfile.objects.create(m_user = user_id, m_business_name = m_business_name, 
                    m_business_category = m_business_category, m_city = m_city, m_district = m_district,
                    m_state = m_state, m_pin_code = m_pin_code, m_area= m_area, m_disabled_account = False,m_latest_account=True, m_unique_id = m_unique_id,loyalty_point=loyalti_point_status) 
                
                try:

                    mobile_no = form.cleaned_data.get("mobile_no")
                    email = form.cleaned_data.get('m_email')
                    raw_password = temp_password
                    user = authenticate(mobile_no=mobile_no, password=raw_password)
                    print(mobile_no)
                    print("User done "+str(user.mobile_no)+str(user.password))
                    subject = 'GreenBill Account Credentials'
                    message = f'Dear {mobile_no}, Your new GreenBill account has been created. Welcome to GreenBill! We’re glad that you have chosen GreenBill as your digital Billing Buddy. Please use below credentials to login:\n Mobile Number: {mobile_no} \n Password: {raw_password} . To sign in to your account, please visit https://www.greenbill.com . If you have any questions regarding your account, Kindly email us on mailto:support@greenbill.in we will be more than happy to help you.'
                    # message = f'Hi {mobile_no}, thank you for registering in Green Bill.\n Please use below credentials to login:\n Mobile Number: {mobile_no} \n Password: {raw_password}'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [m_email,]
                    send_mail( subject, message, email_from, recipient_list)

                    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Everything done")
                # import urllib
                # username = "sanjog1"
                # Password = "123456"
                # sender = "HINDAG"
                # temp_message = f'Hi {mobile_no}, thank you for registering in Green Bill.\n Please use below credentials to login:\n Mobile Number: {mobile_no} \n Password: {raw_password}'
                # temp_dict = {"text": temp_message}
                # message= urllib.parse.urlencode(temp_dict)
                # priority='ndnd'
                # stype='normal'
                
                # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                # import requests

                # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                # res = requests.get(url)
                
                
                    return JsonResponse({'status':'success', 'msg': 'Merchant Added Successfully !!!.'})
                except:
                    return JsonResponse({'status':'error', 'msg': "Failed to add merchant."})
        else:
            return JsonResponse({'status':'error', 'msg': "User already Exists."})
    else:
        return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})





@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def viewMerchantInfo(request, id=None):
    print("okkkk")
    if request.method == "GET":
        merchantBusinessesList = MerchantProfile.objects.get(id=id)
        merchant_objects_id = GreenBillUser.objects.get(mobile_no = merchantBusinessesList.m_user)
        form = MerchnatgeneralSettingForm()
        # print('list',merchantBusinessesList.m_user)
        # print(id)
        merchnat_business_category = business_category.objects.all()

    if request.method == "POST":
        # 
        form = MerchnatgeneralSettingForm(request.POST, request.FILES)
        merchantBusinessesList = MerchantProfile.objects.get(id=id)
        
        # print(form.errors)

        if form.is_valid():
            
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
            # print(pan_number)
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
            bank_account_entity_m1 = form.cleaned_data.get("bank_account_entity_m1")
            bank_account_entity_adress2 = form.cleaned_data.get("bank_account_entity_adress2")
            m_website_url = form.cleaned_data.get("m_website_url")
            m_business_name_for_billing = form.cleaned_data.get("m_business_name_for_billing")
            m_billing_address = form.cleaned_data.get("m_billing_address")
            m_billing_email = form.cleaned_data.get("m_billing_email")
            m_billing_phone = form.cleaned_data.get("m_billing_phone")
            first_name1 = request.POST.get("first_name")
            last_name1 = request.POST.get("last_name")
            print(first_name1)
            print(last_name1)

            business_category_object = business_category.objects.get(id=business_category_temp)

            print('ba',merchantBusinessesList.m_user)
            
            result = GreenBillUser.objects.filter(mobile_no = merchantBusinessesList.m_user).update(first_name = first_name1, last_name = last_name1)
            print(result)
            
            MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={'m_business_name_for_billing': m_business_name_for_billing, 'm_billing_address': m_billing_address, 'm_billing_email': m_billing_email, 'm_billing_phone': m_billing_phone, 'm_business_name': business_name, 'm_website_url': m_website_url, 'm_business_name': business_name, 
                'm_business_category': business_category_object, 'm_pin_code': pin_code, 'm_city': city, 'm_area': area ,
                'm_district': district, 'm_state': state, 'm_address': address, 'm_landline_number': landline_number,
                'm_alternate_mobile_number': alternate_mobile_number, 'm_company_email': company_email, 'm_alternate_email' : alternate_email,
                'm_pan_number': pan_number, 'm_gstin': gstin, 'm_cin': cin, 'm_bank_account_number': bank_account_number, 
                # 'm_other_document_certificate1':other_document_certificate1,
                # 'm_GSTIN_certificate':GSTIN_certificate, 'm_CIN_certificate':CIN_certificate,'m_cancel_bank_cheque_photo':cancel_bank_cheque_photo,
                'm_bank_IFSC_code': bank_IFSC_code, 'm_bank_name' : bank_name, 'm_bank_branch' : bank_branch,'Entity_Account_m': bank_account_entity_m1, 'Entity_Bank_Account_m': bank_account_entity_adress2,'m_vat_tin_number':tin_vat_number,
                'm_aadhaar_number':aadhaar,"m_other_document1":other_document1,"m_other_document2":other_document2})
           
           
            # for all in MerchantProfile.objects.filter(m_user=merchantBusinessesList.m_user,m_business_name=business_name):
                
            #     print(all, all.id)

            #     MerchantProfile.objects.update_or_create(id = all.id, defaults={ 
            #     'm_alternate_mobile_number': alternate_mobile_number, 'm_company_email': company_email, 'm_alternate_email' : alternate_email,
            #     'm_pan_number': pan_number, 'm_gstin': gstin, 'm_cin': cin, 'm_bank_account_number': bank_account_number, 
            #     'm_bank_IFSC_code': bank_IFSC_code, 'm_bank_name' : bank_name, 'm_bank_branch' : bank_branch,'m_vat_tin_number':tin_vat_number,
            #     'm_aadhaar_number':aadhaar,"m_other_document1":other_document1,"m_other_document2":other_document2})

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

            if udyog_adhar_certificate_file:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_other_document_certificate1" : udyog_adhar_certificate_file })
            
            if address_proof:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "address_proof" : address_proof })

            if m_bank_account_entry:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_bank_account_entry" : m_bank_account_entry })

            if m_address_bank_account:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "m_address_bank_account" : m_address_bank_account })

            if schedule_pdf_upload:
                MerchantProfile.objects.update_or_create(id = merchant_setting_id, defaults={ "schedule_pdf_upload" : schedule_pdf_upload })

            
            sweetify.success(request, title="Success", icon='success',
                             text='General Setting Stored Successfully !!!', timer=1000)

            return HttpResponseRedirect('/merchant-info-view/'+str(id)+'/')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!', timer=1000)
            return HttpResponseRedirect('/merchant-info-view/'+str(id)+'/')
    else:
        
        # merchant_users_object = Merchant_users.objects.get(user_id = merchantBusinessesList.m_user  )
        # print('obj',merchant_users_object.id)
        # print('QQQ')
        # print(id)
        merchant_general_setting = MerchantProfile.objects.get(id = id)
        # print(merchant_general_setting)
        merchnat_business_category = business_category.objects.all()
        States = StateCityData.objects.values('state').distinct().order_by('state')
        form1 = MerchnatgeneralSettingForm()
        context = {
            # 'merchantBusinessesList' : merchantBusinessesList,
            'merchantBusinessCategory' : merchnat_business_category,
            'merchantBusinessCategory' : merchnat_business_category,
            'merchant_b_id': id,
            'States': States,
            'merchantNavActiveClass': "active", 
            'MerchantInfoCollapseShow': "show",
            'MerchantListNavclass': "active",
            'merchant_objects_id': merchant_objects_id,
            'form': form1,
            'merchant_general_setting': merchant_general_setting, 
            'merchnat_business_category': merchnat_business_category, 
        }
        return render(request, "super_admin/merchant-info-view.html", context)
    # else:
    #     return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def merchantDetailView(request, id=None):
    merchant_business_object = MerchantProfile.objects.get(id=id)

    merchant_nubmer_id = merchant_business_object.m_user

    merchant_business_id = merchant_business_object.id

    # print("merchant_business_object",merchant_business_object)
    # print("merchant_nubmer_id",merchant_nubmer_id)
    # print("merchant_business_id",merchant_business_id)
    from_date1 = ''
    to_date = ''

    if request.method == 'POST':
        DATE_FORMAT = '%Y-%m-%d'
        from_date1 = request.POST['from_date']
        to_date = request.POST['to_date']

        date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
        day_later = date_time_obj + timedelta(days=1)
        x = day_later.date()
        ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

        from_date = datetime.strptime(str(from_date1), '%Y-%m-%d').strftime('%d-%m-%Y')
        start_date = from_date.split('-')
        start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
        sd_filter = start_date.strftime(DATE_FORMAT)

        print(ed_filter,sd_filter)

    merchant_user_list = []

    offers = OfferModel.objects.filter(merchant_user = merchant_nubmer_id)

    offers_count = OfferModel.objects.filter(merchant_user = merchant_nubmer_id, merchant_business_id = merchant_business_object).count()

    coupon = CouponModel.objects.filter(merchant_id = merchant_nubmer_id, merchant_business_id = merchant_business_object.id)

    coupon_count = CouponModel.objects.filter(merchant_id = merchant_nubmer_id, merchant_business_id = merchant_business_object.id).count()
    coupon_redeem_count = RedeemCouponModel.objects.filter(merchant_id = merchant_nubmer_id, merchant_business_id = merchant_business_object.id).count()


    try:
        merchant_user_record_id = Merchant_users.objects.filter(user_id = merchant_nubmer_id).values('merchant_user_id')[0]['merchant_user_id']

        merchant_user_id_object = GreenBillUser.objects.get(id=merchant_user_record_id)

        total_users = Merchant_users.objects.filter(merchant_user_id = merchant_user_id_object,m_business_id = merchant_business_object.id).count()
    except:
        total_users = ""

    try:
        mer_user_data_id = Merchant_users.objects.get(user_id=merchant_nubmer_id)
        merchant_data_object = mer_user_data_id.merchant_user_id
        merchant_business_data_object = MerchantProfile.objects.get(m_user = merchant_data_object, m_active_account = True)
        merchant_business_data_id = merchant_business_data_object.id
        
        parking_bill_lists = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_data_id, is_pass = False).order_by('-id')
        petrol_bill_lists = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_data_id).order_by('-id')
        customer_bill_lists = CustomerBill.objects.filter(business_name = merchant_business_data_object, customer_added = False).order_by('-id')
        merchant_bill_lists = MerchantBill.objects.filter(business_name = merchant_business_data_object, customer_added = False).order_by('-id').distinct()

        unique_mobile_no = []

        for parking_bills in parking_bill_lists:
            if parking_bills.mobile_no in unique_mobile_no:
                pass
            else:
               unique_mobile_no.append(parking_bills.mobile_no)
        
        for petrol_bills in petrol_bill_lists:
            if petrol_bills.mobile_no in unique_mobile_no:
                pass
            else:
               unique_mobile_no.append(petrol_bills.mobile_no)

        for customer_bills in customer_bill_lists:
            if customer_bills.mobile_no in unique_mobile_no:
                pass
            else:
               unique_mobile_no.append(customer_bills.mobile_no)

        for merchant_bills in merchant_bill_lists:
            if merchant_bills.mobile_no in unique_mobile_no:
                pass
            else:
               unique_mobile_no.append(merchant_bills.mobile_no)
        total_customer = 0
        for mobile_no in unique_mobile_no:
            total_customer = total_customer + 1
    except:
        total_customer = 0

    refferal_code = GreenBillUser.objects.get(mobile_no = merchant_nubmer_id)
    check_refferal_code = refferal_code.merchant_referral_code

    reffer_count = GreenBillUser.objects.filter(m_used_referral_code=check_refferal_code).count()

    # print('user_count', user_count)

    merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = request.user, m_business_id = merchant_business_id)

    for user in merchant_user_temp:
        merchant_user_list.append({
            'user_id': user.user_id
            })

    data = []

    base_url = "http://157.230.228.250/"

    try:
        bill_design = bill_designs.objects.get(merchant_business_id = merchant_business_object)
        bill_rating_emoji = bill_design.rating_emoji
    except:
        bill_rating_emoji = ""

    if request.method == 'POST':

        parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False, created_at__gte = sd_filter, created_at__lte = ed_filter).order_by('-id')
        parking_bill_count = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False, created_at__gte = sd_filter, created_at__lte = ed_filter).count()
        

        petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, created_at__gte = sd_filter, created_at__lte = ed_filter).order_by('-id')
        petrol_bill_count = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, created_at__gte = sd_filter, created_at__lte = ed_filter).count()

        customer_bill_list = CustomerBill.objects.filter(business_name_id=merchant_business_id,customer_added = False, created_at__gte = sd_filter, created_at__lte = ed_filter).order_by('-id')
        customer_bill_count = CustomerBill.objects.filter(business_name_id=merchant_business_id,customer_added = False, created_at__gte = sd_filter, created_at__lte = ed_filter).count()

        merchant_bill_list = MerchantBill.objects.filter(business_name=merchant_business_id, created_at__gte = sd_filter, created_at__lte = ed_filter)
        merchant_bill_count = MerchantBill.objects.filter(business_name=merchant_business_id, created_at__gte = sd_filter, created_at__lte = ed_filter).count()
    else:
        parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False, created_at__date = timezone.now()).order_by('-id')
        parking_bill_count = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False, created_at__date = timezone.now()).count()
        

        petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, created_at__date = timezone.now()).order_by('-id')
        petrol_bill_count = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, created_at__date = timezone.now()).count()

        customer_bill_list = CustomerBill.objects.filter(business_name_id=merchant_business_id,customer_added = False, created_at__date = timezone.now()).order_by('-id')
        customer_bill_count = CustomerBill.objects.filter(business_name_id=merchant_business_id,customer_added = False, created_at__date = timezone.now()).count()

        merchant_bill_list = MerchantBill.objects.filter(business_name=merchant_business_id, created_at__date = timezone.now())
        merchant_bill_count = MerchantBill.objects.filter(business_name=merchant_business_id, created_at__date = timezone.now()).count()

    data = []
    for bill in parking_bill_list:
        data.append({
            'mobile_no': bill.mobile_no,
            'amount' : float(bill.amount),


        })
    for bill in petrol_bill_list:
        data.append({
            'mobile_no': bill.mobile_no,
            'amount' : bill.amount,
        })
    for bill in customer_bill_list:
        data.append({
            'mobile_no': bill.mobile_no,
            'amount' : bill.bill_amount,


        })
    for bill in merchant_bill_list:
        data.append({
            'mobile_no': bill.mobile_no,
            'amount' : bill.bill_amount,


        })

    total_transaction = 0

    total_transaction = customer_bill_count + merchant_bill_count

    parking_bill_lists1 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_object.id, is_pass = False).order_by('-id')
    petrol_bill_lists1 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_object.id).order_by('-id')
    customer_bill_lists1 = CustomerBill.objects.filter(business_name = merchant_business_object, customer_added = False).order_by('-id')
    merchant_bill_lists1 = MerchantBill.objects.filter(business_name = merchant_business_object, customer_added = False).order_by('-id')
    customer_receipt = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_object).order_by('-id')
    customer_cash_memo = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_object).order_by('-id')


    data1 = []

    for bill in parking_bill_lists1:
        data1.append({
            'mobile_no': bill.mobile_no,
        })
    for bill in petrol_bill_lists1:
        data1.append({
            'mobile_no': bill.mobile_no,
        })
    for bill in customer_bill_lists1:
        data1.append({
            'mobile_no': bill.mobile_no,
        })
    for bill in merchant_bill_lists1:
        data1.append({
            'mobile_no': bill.mobile_no,
        })
    for bill in customer_receipt:
        data1.append({
            'mobile_no': bill.mobile_number,
        })
    for bill in customer_cash_memo:
        data1.append({
            'mobile_no': bill.mobile_number,
        })

    filtered_list2 = []

    for unique in data1:
        if unique['mobile_no'] not in filtered_list2:
            filtered_list2.append(unique['mobile_no'])
            
    
    
    unique_customer_count = []
    for data_list in data:
        if data_list['mobile_no'] not in unique_customer_count:
            unique_customer_count.append(data_list['mobile_no'])
    
    customer_count = len(filtered_list2)
    
    bill_sent_count = parking_bill_count + petrol_bill_count + customer_bill_count + merchant_bill_count

    digital_sent = 0
    for bill in customer_bill_list:
        if bill.greenbill_digital_bill == "True":
            digital_sent = digital_sent + 1

    for bill in merchant_bill_list:
        if bill.greenbill_digital_bill == "True":
            digital_sent = digital_sent + 1

    for bill in parking_bill_list:
        if bill.greenbill_digital_bill == "True":
            digital_sent = digital_sent + 1

    for bill in parking_bill_list:
        if bill.greenbill_digital_bill == "True":
            digital_sent = digital_sent + 1

    sms_sent = 0
    for bill in customer_bill_list:
        if bill.greenbill_sms_bill == "True":
            sms_sent = sms_sent + 1

    for bill in merchant_bill_list:
        if bill.greenbill_sms_bill == "True":
            sms_sent = sms_sent + 1

    for bill in parking_bill_list:
        if bill.greenbill_sms_bill == "True":
            sms_sent = sms_sent + 1

    for bill in parking_bill_list:
        if bill.greenbill_sms_bill == "True":
            sms_sent = sms_sent + 1
    
    total_bill_sent = digital_sent + sms_sent

            
    active_subs = getActiveSubscriptionPlan(request,merchant_business_id)
    active_transactional_subs = getActiveTransactionalSubscriptionPlan(request,merchant_business_id)
    active_promotional_subs = getActivePromotionalSubscriptionPlan(request,merchant_business_id)

    if request.method == 'POST':

        exe_send_and_print_bill_status1 = CustomerBill.objects.filter(business_name_id=merchant_business_id, exe_bill_type = 2, created_at__gte = sd_filter, created_at__lte = ed_filter).count()

        exe_send_and_print_bill_status2 = MerchantBill.objects.filter(business_name=merchant_business_id, exe_bill_type = 2, created_at__gte = sd_filter, created_at__lte = ed_filter).count()

        exe_send_bill_status1 = CustomerBill.objects.filter(business_name_id=merchant_business_id, exe_bill_type = 1, created_at__gte = sd_filter, created_at__lte = ed_filter).count()

        exe_send_bill_status2 = MerchantBill.objects.filter(business_name=merchant_business_id, exe_bill_type = 1, created_at__gte = sd_filter, created_at__lte = ed_filter).count()

        exe_print_bill_status = ExePrintStatus.objects.filter(business_id = merchant_business_object.id, created_at__gte = sd_filter, created_at__lte = ed_filter).count()
    else:
        exe_send_and_print_bill_status1 = CustomerBill.objects.filter(business_name_id=merchant_business_id, exe_bill_type = 2, created_at__date = timezone.now()).count()

        exe_send_and_print_bill_status2 = MerchantBill.objects.filter(business_name=merchant_business_id, exe_bill_type = 2, created_at__date = timezone.now()).count()

        exe_send_bill_status1 = CustomerBill.objects.filter(business_name_id=merchant_business_id, exe_bill_type = 1, created_at__date = timezone.now()).count()

        exe_send_bill_status2 = MerchantBill.objects.filter(business_name=merchant_business_id, exe_bill_type = 1, created_at__date = timezone.now()).count()

        exe_print_bill_status = ExePrintStatus.objects.filter(business_id = merchant_business_object.id, created_at__date = timezone.now()).count()

    send_print_bill_count = int(exe_send_and_print_bill_status1) + int(exe_send_and_print_bill_status2)

    send_bill_count = int(exe_send_bill_status1) + int(exe_send_bill_status2)

    if request.method == 'POST':
        received_payments = PaymentLinks.objects.filter(m_business_id = merchant_business_object.id, payment_done = True, payment_date__gte = sd_filter, payment_date__lte = ed_filter)
    else:
        received_payments = PaymentLinks.objects.filter(m_business_id = merchant_business_object.id, payment_done = True, payment_date__date = timezone.now())
    data = []
    for payment in received_payments:
        data.append({
            'mobile_no': payment.mobile_no,
            'amount' : payment.amount,
            'payment_date' : payment.payment_date,
            'transaction_id' : payment.transaction_id,
            'created_at' : payment.created_at,
            'payment_date_new':datetime.strptime(str(payment.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d')
        })
        payment.payment_date = datetime.strptime(str(payment.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d')

    if request.method == 'POST':
        customer_bill = CustomerBill.objects.filter(business_name = merchant_business_object,payment_done = True, created_at__gte = sd_filter, created_at__lte = ed_filter)
    else:
        customer_bill = CustomerBill.objects.filter(business_name = merchant_business_object,payment_done = True, created_at__date = timezone.now())

    for customer in customer_bill:
        data.append({
            'mobile_no': customer.mobile_no,
            'amount' : customer.bill_amount,
            'payment_date' : customer.payment_date,
            'transaction_id' : customer.transaction_id,
            'created_at' : customer.created_at,
            'payment_date_new':datetime.strptime(str(customer.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d')
        })

    if request.method == 'POST':
        merchant_bill = MerchantBill.objects.filter(business_name = merchant_business_object,payment_done = True, created_at__gte = sd_filter, created_at__lte = ed_filter)
    else:
        merchant_bill = MerchantBill.objects.filter(business_name = merchant_business_object,payment_done = True, created_at__date = timezone.now())

    for merchant in merchant_bill:
        data.append({
            'mobile_no': merchant.mobile_no,
            'amount' : merchant.bill_amount,
            'payment_date' : merchant.payment_date,
            'transaction_id' : merchant.transaction_id,
            'created_at' : merchant.created_at,
            'payment_date_new':datetime.strptime(str(merchant.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d') if merchant.payment_date else ""
        })

    if request.method == 'POST':
        parking_bill = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_object.id, payment_done = True, created_at__gte = sd_filter, created_at__lte = ed_filter) 
    else:
        parking_bill = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_object.id, payment_done = True, created_at__date = timezone.now()) 

    for parking in parking_bill:
        data.append({
            'mobile_no': parking.mobile_no,
            'amount' : parking.amount,
            'payment_date' : parking.payment_date,
            'transaction_id' : parking.transaction_id,
            'created_at' : parking.created_at,
            'payment_date_new':datetime.strptime(str(parking.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d')
        })

    if request.method == 'POST':
        petrol_bill = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_object.id, payment_done=True, created_at__gte = sd_filter, created_at__lte = ed_filter)
    else:
        petrol_bill = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_object.id, payment_done=True, created_at__date = timezone.now())
    for petrol in petrol_bill:
        data.append({
            'mobile_no': petrol.mobile_no,
            'amount' : petrol.amount,
            'payment_date' : petrol.payment_date,
            'transaction_id' : petrol.transaction_id,
            'created_at' : petrol.created_at,
            'payment_date_new' : datetime.strptime(str(petrol.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d')
        })

    total_payment = 0.00
    for payment in data:
        total_payment = total_payment + float(payment['amount'])
        
    total_transaction_count = 0
    count1 = 0
    count2 = 0

    startswith = str(merchant_business_id) + ','
    endswith = ','+ str(merchant_business_id)
    contains = ','+ str(merchant_business_id) + ','
    exact = str(merchant_business_id)
    if request.method == 'POST':
        payment_history = recharge_history.objects.filter(
            Q(merchant_id = merchant_nubmer_id),
            Q(purchase_date__gte = sd_filter),
            Q(purchase_date__lte = ed_filter),
            Q(business_ids__startswith = startswith) | 
            Q(business_ids__endswith = endswith) | 
            Q(business_ids__contains = contains) | 
            Q(business_ids__exact = exact)
        ).order_by('-id')
    else:       
        payment_history = recharge_history.objects.filter(
            Q(merchant_id = merchant_nubmer_id),
            Q(purchase_date__date = timezone.now()),
            Q(business_ids__startswith = startswith) | 
            Q(business_ids__endswith = endswith) | 
            Q(business_ids__contains = contains) | 
            Q(business_ids__exact = exact)
        ).order_by('-id')

    payment_history_new = []

    for history in payment_history:
        count1 = count1 + 1
        history.pay_business_name = "Green Bill"
        payment_history_new.append(history)
        
        
    if request.method == 'POST':    
        merchant_bill = MerchantBill.objects.filter(business_name = merchant_business_object.id, payment_done = True, created_at__gte = sd_filter, created_at__lte = ed_filter).order_by('-id')
    else:
        merchant_bill = MerchantBill.objects.filter(business_name = merchant_business_object.id, payment_done = True, created_at__date = timezone.now()).order_by('-id')
    
    for bill in merchant_bill:
        count2 = count2 + 1
        # print('merchant_bill',bill.mode)
        if bill.payment_date:
            try:
                bill.pay_business_name = bill.business_name
            except:
                bill.pay_business_name = ""
                
            bill.subscription_name = "Bill Payment"

            try:
                bill.purchase_date = bill.payment_date
            except:
                bill.purchase_date = ""

            bill.cost = bill.bill_amount
            
            payment_history_new.append(bill)

    
    total_transaction_count = count1 + count2
    # sorted_payment_history = sorted(payment_history_new, key=lambda object1: object1.purchase_date, reverse=True)
    
    total_amount_spent = 0.0

    for payment in payment_history_new:
        if payment.cost:
            total_amount_spent = total_amount_spent + float(payment.cost)
            total_transaction_count = total_transaction_count + 1
            
    self_add_customer = Customer_Info_Model.objects.filter(merchant_business_id = merchant_business_object.id ).order_by('-id')
    self_add_customer_count = Customer_Info_Model.objects.filter(merchant_business_id = merchant_business_object.id ).count()
    
    total_customer_count = customer_count + self_add_customer_count
    
    # print("total_customer_count",total_customer_count)
    
    # print("self_add_customer",self_add_customer)
    # print("self_add_customer_count",self_add_customer_count)
    context = {
            'total_customer_count':total_customer_count,
            'self_add_customer_count':self_add_customer_count,
            'sms_sent':sms_sent,
            'merchant_id': id,
            'from_date': from_date1,
            'to_date': to_date,
            'digital_sent':digital_sent,
            'total_bill_sent':total_bill_sent,
            'total_payment': total_payment,
            'total_amount_spent':total_amount_spent,
            'send_bill_count':send_bill_count,
            'send_print_bill_count':send_print_bill_count,
            'exe_print_bill_status':exe_print_bill_status,
            'total_users': total_users,
            'reffer_count': reffer_count,
            'total_customer': total_customer,
            'coupon_redeem_count': coupon_redeem_count,
            'offers_count': offers_count,
            'coupon_count': coupon_count,
            'bill_sent_count':bill_sent_count,
            # 'all_bill_amount_sum':"{:.2f}".format(all_bill_amount_sum),
            'total_transaction':total_transaction,
            # 'average_bill_amount' : "{:.2f}".format(average_bill_amount),
            'customer_count':customer_count,
            'active_subscription': active_subs,
            'active_transactional_subscription':active_transactional_subs,
            'active_promotional_subscription':active_promotional_subs,
            'merchantNavActiveClass': "active", 
            'MerchantInfoCollapseShow': "show",
            'MerchantListNavclass': "active",
        }
    return render(request, 'super_admin/merchant-detail-view.html', context)



def getActiveSubscriptionPlan(request, business_id):

    subscription_object = ""
    print('business_id',business_id)
    if business_id:
        startswith = str(business_id) + ','
        endswith = ','+ str(business_id)
        contains = ','+ str(business_id) + ','
        exact = str(business_id)
        
        try:
            subscription_object = merchant_subscriptions.objects.get(
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )

            return subscription_object

        except:
            return subscription_object
    else:
        return subscription_object


def getActivePromotionalSubscriptionPlan(request, business_id):

    subscription_object = ""

    if business_id:
        startswith = str(business_id) + ','
        endswith = ','+ str(business_id)
        contains = ','+ str(business_id) + ','
        exact = str(business_id)
        
        try:
            subscription_object = promotional_sms_subscriptions.objects.get(
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )

            return subscription_object

        except:
            return subscription_object
    else:
        return subscription_object


def getActiveTransactionalSubscriptionPlan(request, business_id):

    subscription_object = ""

    if business_id:
        startswith = str(business_id) + ','
        endswith = ','+ str(business_id)
        contains = ','+ str(business_id) + ','
        exact = str(business_id)
        
        try:
            subscription_object = transactional_sms_subscriptions.objects.get(
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )

            return subscription_object

        except:
            return subscription_object
    else:
        return subscription_object



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def getMerchantBusinessDetails(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        merchant_setting_id = request.POST['merchant_setting_id']
        
        merchantBusinessDetail = MerchantProfile.objects.filter(id=merchant_setting_id, m_user=user_id)
        if merchantBusinessDetail:
            business_dict = {
                'user_id': user_id,
                'merchant_setting_id': merchant_setting_id,
                'm_business_name': merchantBusinessDetail[0].m_business_name,
                'm_business_category': merchantBusinessDetail[0].m_business_category_id,
                'm_pin_code': merchantBusinessDetail[0].m_pin_code,
                'm_state': merchantBusinessDetail[0].m_state,
                'm_district': merchantBusinessDetail[0].m_district,
                'm_city': merchantBusinessDetail[0].m_city,
                'm_area': merchantBusinessDetail[0].m_area,
                'm_address': merchantBusinessDetail[0].m_address,
                'm_landline_number': merchantBusinessDetail[0].m_landline_number,
                'm_alternate_mobile_number': merchantBusinessDetail[0].m_alternate_mobile_number,
                'm_company_email': merchantBusinessDetail[0].m_company_email,
                'm_alternate_email': merchantBusinessDetail[0].m_alternate_email,
                'm_pan_number': merchantBusinessDetail[0].m_pan_number,
                'm_gstin': merchantBusinessDetail[0].m_gstin,
                'm_cin': merchantBusinessDetail[0].m_cin,
                'm_bank_account_number': merchantBusinessDetail[0].m_bank_account_number,
                'm_bank_IFSC_code': merchantBusinessDetail[0].m_bank_IFSC_code,
                'm_bank_name': merchantBusinessDetail[0].m_bank_name,
                'm_bank_branch': merchantBusinessDetail[0].m_bank_branch,

            }
        else:
            business_dict = ""
        return JsonResponse({'status':'success', 'business_data': business_dict})
    else:
        return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})



#DISABLED MERCHANT FUNCTION
@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def disabledMerchant(request):
    qs = business_category.objects.all().order_by('-id')
    
    merchantList = MerchantProfile.objects.all().filter(m_disabled_account=True).distinct().order_by('-id')
    count = MerchantProfile.objects.all().filter(m_disabled_account=True).count()
    print(count)
    context = {
        'qs': qs,
        'merchantList' : merchantList,
        'count' : count,
        'merchantNavActiveClass': "active", 
         'MerchantInfoCollapseShow': "show",
         'MerchantDisabledNavclass': "active",
    }
    return render(request, 'super_admin/disabled-merchant.html', context)



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Delete_Disabled_Merchant(request,id):
    try:
        merchantList = MerchantProfile.objects.get(id=id)
        if merchantList.m_disabled_account ==True :
            merchantList.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': True})

    except:
        return JsonResponse({'success': False})















#LATEST MERCHANT LIST
@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def latestMerchant(request):
    qs = business_category.objects.all()
    merchatList = MerchantProfile.objects.filter(m_latest_account=True, status = "0").order_by('-id')
    merchatListCount = MerchantProfile.objects.filter(m_latest_account=True, status = "0").count()
    # for merchant in merchatList:
    #         merchant_object = GreenBillUser.objects.get(mobile_no = merchant.m_user)
    #         merchant.first_name = merchant_object.first_name
    #         merchant.last_name = merchant_object.last_name
    context = {
        'qs' : qs,
        'merchantList' : merchatList,
        'merchatListCount' : merchatListCount,
        'merchantNavActiveClass': "active", 
        'MerchantInfoCollapseShow': "show",
        'MerchantLatestNavclass': "active",
    }
    return render(request, 'super_admin/latest-merchant.html', context)


# disable reason

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def disabledMerchantReason(request):
    if request.method == "POST":
        form = merchantDisablereasonForm(request.POST, request.FILES)
        obj1 = ""
        obj2 = ""
        if request.POST['reason_id'] != "":
            merchant_reason = request.POST['merchant_reason']
            obj1 = MerchantDisablereasons.objects.update_or_create(
                id=int(request.POST["reason_id"]), defaults={"merchant_reason": merchant_reason})
        else:
            merchant_reason = request.POST['merchant_reason']
            if not MerchantDisablereasons.objects.filter(merchant_reason = merchant_reason).exists():
                obj2 = MerchantDisablereasons.objects.create(merchant_reason=merchant_reason)
            else:
                sweetify.success(request, title="Oops...",
                             icon='error', text='Reason is already exists.', timer=1000)
        if obj1:
            sweetify.success(request, title="Success", icon='success',
                             text='Reason updated Successfully.', timer=1500)

        elif obj2:
            sweetify.success(request, title="Success", icon='success',
                             text='Reason created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...",
                             icon='error', text='Reason is already exists.', timer=1000)
    
    data = MerchantDisablereasons.objects.all().order_by('-id')
    context = {
    'data': data,   
    'merchantNavActiveClass': "active", 
         'MerchantInfoCollapseShow': "show",
         'MerchantDisableNavclass': "active",
    }
    return render(request, "super_admin/disable-mer-reason.html", context)
def Delete_Reason(request, id):
    status = MerchantDisablereasons.objects.get(id=id).delete()
    if status:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": False})




@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def editMerchantBusinessInfo(request):
    
    if request.method == "POST":
        form = merchantEditBusinessesForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            user_id = request.POST['user_id']
            business_id = request.POST['merchant_setting_id']
            
            m_business_name = form.cleaned_data.get("m_business_name")
            m_business_category = form.cleaned_data.get("m_business_category")
            m_pin_code = form.cleaned_data.get("m_pin_code")
            m_state = form.cleaned_data.get("m_state")
            m_district = form.cleaned_data.get("m_district")
            m_city = form.cleaned_data.get("m_city")
            m_area = form.cleaned_data.get("m_area")
            m_address = form.cleaned_data.get("m_address")
            m_landline_number = form.cleaned_data.get("m_landline_number")
            m_alternate_mobile_number = form.cleaned_data.get("m_alternate_mobile_number")
            m_company_email = form.cleaned_data.get("m_company_email")
            m_alternate_email = form.cleaned_data.get("m_alternate_email")
            m_pan_number = form.cleaned_data.get("m_pan_number")
            m_gstin = form.cleaned_data.get("m_gstin")
            m_cin = form.cleaned_data.get("m_cin")
            m_bank_account_number = form.cleaned_data.get("m_bank_account_number")
            m_bank_IFSC_code = form.cleaned_data.get("m_bank_IFSC_code")
            m_bank_name = form.cleaned_data.get("m_bank_name")
            m_bank_branch = form.cleaned_data.get("m_bank_branch")
            m_GSTIN_certificate = form.cleaned_data.get("m_GSTIN_certificate")
            m_CIN_certificate = form.cleaned_data.get("m_CIN_certificate")
            m_business_logo = form.cleaned_data.get("m_business_logo")
            m_business_stamp = form.cleaned_data.get("m_business_stamp")
            m_digital_signature = form.cleaned_data.get("m_digital_signature")
            
            result = MerchantProfile.objects.filter(id=business_id, m_user_id=user_id).update(m_business_name = m_business_name, m_business_category_id = m_business_category, m_city = m_city, m_district = m_district, m_state = m_state, m_pin_code = m_pin_code, m_area= m_area, m_address=m_address, m_landline_number=m_landline_number, m_alternate_mobile_number=m_alternate_mobile_number, m_company_email=m_company_email, m_alternate_email=m_alternate_email, m_pan_number=m_pan_number, m_gstin=m_gstin, m_cin=m_cin, m_bank_account_number=m_bank_account_number, m_bank_IFSC_code=m_bank_IFSC_code, m_bank_name=m_bank_name, m_bank_branch=m_bank_branch)

            if m_GSTIN_certificate:
                MerchantProfile.objects.update_or_create(id = business_id, defaults={ "m_GSTIN_certificate" : m_GSTIN_certificate })

            if m_CIN_certificate:
                MerchantProfile.objects.update_or_create(id = business_id, defaults={ "m_CIN_certificate" : m_CIN_certificate })
            
            if m_business_logo:
                MerchantProfile.objects.update_or_create(id = business_id, defaults={ "m_business_logo" : m_business_logo })

            if m_business_stamp:
                MerchantProfile.objects.update_or_create(id = business_id, defaults={ "m_business_stamp" : m_business_stamp })

            if m_digital_signature:
                MerchantProfile.objects.update_or_create(id = business_id, defaults={ "m_digital_signature" : m_digital_signature })
        
            if result:
                sweetify.success(request, title="Success", icon='success', text='Merchant business information updated sucessfully. !!!')
                return redirect('/merchant-info-view/'+user_id+'/')
                # return JsonResponse({'status':'success', 'msg': "Merchant business information updated sucessfully."})
            else:
                sweetify.error(request, title="error", icon='error', text='Unable to update business information.', timer=1000)
                return redirect('/merchant-info-view/'+user_id+'/')
                # return JsonResponse({'status':'error', 'msg': "Unable to update business information."})
        else:
            sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
            return redirect('/merchant-info-view/'+user_id+'/')
            # return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})
    else:
        sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
        return redirect('/merchant-info-view/'+user_id+'/')
        # return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_edit(request, id):
    if request.method == "GET":
        try:
            instance = get_object_or_404(Merchant, id=id)
            
            return JsonResponse({'merchantId':id, 'merchantName':instance.merchantName, 'merchantDesc':instance.merchantDesc})

        except Merchant.DoesNotExist:
            return render(request, 'error-404.html')
    else :
        post_data = request.POST or None
        
        if post_data != None:
            my_form = MerchantForm_edit(request.POST)
            if my_form.is_valid():
                merchantName = my_form.cleaned_data.get("edit_merchantName")
                merchantDesc = my_form.cleaned_data.get("edit_merchantDesc")
                Merchant.objects.filter(id=id).update(merchantName= merchantName, merchantDesc = merchantDesc)
                return JsonResponse({'success':True})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_delete(request, id, *args, **kwargs):
    
    instance = MerchantProfile.objects.get(id=id)
    instance.delete()
    return JsonResponse({'success':True})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def disableMerchantFromAdmin(request):
    if request.method == "POST":

        disable_mobile_no = request.POST['disable_mobile_no']
        
        merchant_id = request.POST['merchant_id']
        print(merchant_id)
        reason = request.POST['reason']
        print("DISABLED")
        MerchantProfile.objects.filter(id=merchant_id).update(m_disabled_account=True, disable_reason= reason)
        #GreenBillUser.objects.filter(id= merchant_id).update(is_active=False, disable_reason= reason)
        GreenBillUser.objects.filter(mobile_no= disable_mobile_no).update(is_merchant=False , is_merchant_staff=False)

        return JsonResponse({'status': 1, 'msg': 'Status change successfully'})
        
    else:
        return JsonResponse({'status': 0, 'msg': 'Something went wrong'})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def disapproveMerchant(request):
    if request.method == "POST":
        
        merchant_id = request.POST['merchant_id']
        
        reason = request.POST['reason']
        MerchantProfile.objects.filter(id=merchant_id).update(m_disabled_account=True, disapprove_reason= reason,status=2)
        # GreenBillUser.objects.filter(id= merchant_id).update(is_active=False, disable_reason= reason)
        return JsonResponse({'status': 1, 'msg': 'Status change successfully'})
        
    else:
        return JsonResponse({'status': 0, 'msg': 'Something went wrong'})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def enableMerchantFromAdmin(request, id):
    if request.method == "POST":

        merchant_object = MerchantProfile.objects.filter(id=id).update(m_disabled_account= False, m_latest_account=False, status=1)

        merchant_id = MerchantProfile.objects.get(id=id).m_user

        GreenBillUser.objects.filter(mobile_no=merchant_id).update(is_merchant = True, is_merchant_staff = True)

        user = MerchantProfile.objects.filter(id=id).values('m_user')[0]['m_user']

        notification_object = notification_settings.objects.get(id = 9)

        if notification_object.send_sms:

            ts = int(time.time())

            data_temp = {
                    "keyword":"New Merchant Registration Completed",
                    "timeStamp":ts,
                    "dataSet":
                        [
                            {
                                "UNIQUE_ID":"GB-" + str(ts),
                                "MESSAGE":"Thank you for choosing GreenBill as your digital billing buddy. Your registration is complete please visit website or download GB Merchant App to login",
                                "OA":"GBBILL",
                                "MSISDN":str(user.mobile_no), # Recipient's Mobile Number
                                "CHANNEL":"SMS",
                                "CAMPAIGN_NAME":"hind_user",
                                "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                "USER_NAME":"hind_hsi",
                                "DLT_TM_ID":"1001096933494158", # TM ID
                                "DLT_CT_ID":"1007161814117326730", # Template Id
                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                            }
                        ]
                    }

            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

            response = requests.post(url, json = data_temp)

        if notification_object.send_email:
            subject = 'New Merchant Registration'
            message = f'Thank you for choosing GreenBill as your digital billing buddy. Your registration is complete please visit website or download GB Merchant App to login'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail( subject, message, email_from, recipient_list)

        # GreenBillUser.objects.filter(id= id).update(is_active=True)
        return JsonResponse({'status': 1, 'msg': 'Status change successfully'})
        
    else:
        return JsonResponse({'status': 0, 'msg': 'Something went wrong'})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def merchantBySales(request):
    if request.method == "GET":
        merchantList = MerchantProfile.objects.all()
        # for partner in partnerList:
        #     if partner.p_user.is_staff == True and partner.p_user.created_by == "Sales":
                
        context = {
            'merchant_list': merchantList, 
            'merchantNavActiveClass': "active", 
            'MerchantInfoCollapseShow': "show",
            'MerchantBySalesNavClass': "active",
        }
        return render(request, "super_admin/merchant-by-sales.html", context)

# def merchant_add(request, id=0):
    
#     if request.method == "GET":
#         if id == 0:
#             form = MerchantForm()
#         else:
#             merchant = Merchant.objects.get(pk=id)
            
#             form = MerchantForm(instance=merchant)    
#         return render(request, "merchant/add.html", {'form' : form})
#     else:
#         if id == 0:
#             form = MerchantForm(request.POST)
#             msg = "Merchant Added Successfully !!!"
#         else:
#             merchant = Merchant.objects.get(pk=id)
#             form = MerchantForm(request.POST, instance=merchant)
#             msg = "Merchant's Information Edited Successfully !!!"
#         if form.is_valid():
#             form.save()

#         messages.success(request, msg)
#         return redirect('/list/')


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchantBusinesses(request):
    try:
        last_unique_id = MerchantUniqueIds.objects.all().last()
    except:
        last_unique_id = ""

    if not last_unique_id:
        m_unique_id = str("GBM") + str("01").zfill(6)
        no = 1
    else:
        last_no = last_unique_id.m_unique_no
        no = int(last_no) + 1
        m_unique_id = str("GBM") + str(no).zfill(6)

    MerchantUniqueIds.objects.create(m_unique_no = no)

    if request.method == "POST":
        form = merchantBusinessesForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            
            m_business_name = form.cleaned_data.get("m_business_name")
            m_business_category = form.cleaned_data.get("m_business_category")
            # m_city = form.cleaned_data.get("m_city")
            # m_district = form.cleaned_data.get("m_district")
            # m_state = form.cleaned_data.get("m_state")
            m_pin_code = form.cleaned_data.get("m_pin_code")
            # m_area = form.cleaned_data.get("m_area")
            m_landline_number = form.cleaned_data.get('m_landline_number')
            m_address = form.cleaned_data.get('m_address')

            cust_city = form.cleaned_data.get("m_city")
            m_city = cust_city.capitalize()

            cust_district = form.cleaned_data.get("m_district")
            m_district = cust_district.capitalize()

            cust_state = form.cleaned_data.get("m_state")
            m_state = cust_state.capitalize()

            cust_area = form.cleaned_data.get("m_area")
            m_area = cust_area.capitalize()

            # merchant_user = Merchant_users.objects.create(user_id = GreenBillUser.objects.get(id = user_id) , merchant_user_id = GreenBillUser.objects.get(id = user_id))

            merchant_profile_id = MerchantProfile.objects.create(m_user_id = user_id, m_business_name = m_business_name,
             m_business_category = m_business_category, m_city = m_city, m_district = m_district,
              m_state = m_state, m_pin_code = m_pin_code, m_area = m_area,
               m_landline_number=m_landline_number, m_address=m_address,
                m_latest_account=1, m_unique_id = m_unique_id)


            role_name1 = 'Admin'

            role_name2 = 'Exe User'

            role_name3 = 'Operator'


            merchant_user = GreenBillUser.objects.get(id = user_id)
            print('merchant_user',merchant_user)

            if merchant_profile_id.m_business_category.id != 11 and merchant_profile_id.m_business_category.id != 12:
                merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user, role_name = role_name1)

                merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user, role_name = role_name2)

            if merchant_profile_id.m_business_category.id == 11 or merchant_profile_id.m_business_category.id == 12:
                merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user, role_name = role_name1)

                merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user, role_name = role_name3)

            sweetify.success(request, title="Success", icon='success', text='Business Stored Successfully !!!')
            return redirect('/merchant-business/')
        else:
            sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
            return redirect('/merchant-business/')
    else:

        form = merchantBusinessesForm()
        
        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        States = StateCityData.objects.values('state').distinct().order_by('state')

        data = MerchantProfile.objects.filter(m_user_id = merchant_users_object.merchant_user_id.id)
        context = {
            'form': form,
            'States': States,
            'data': data,
            'merchantNavClass': "active", 
            "SettingNavclass": 'active',
            "settingsCollapseShow": "show",
            
        }
        if data:
            return render(request, "merchant/merchant_business.html",context)
        else:
            data = ""
            return render(request, "merchant/merchant_business.html",context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchantBusinessesBranch(request):
    if request.method == "POST":
        form1 = merchantBusinessesBranchForm(request.POST, request.FILES)
        
        if form1.is_valid():
            user_id = request.user.id
            
            m_business_name = form1.cleaned_data.get("m_business_name")
            m_business_category = form1.cleaned_data.get("m_business_category")
            # m_city = form1.cleaned_data.get("m_city")
            m_landline_number = form1.cleaned_data.get("m_landline_number")
            # m_district = form1.cleaned_data.get("m_district")
            # m_state = form1.cleaned_data.get("m_state")
            m_pin_code = form1.cleaned_data.get("m_pin_code")
            # m_area = form1.cleaned_data.get("m_area")
            m_address = form1.cleaned_data.get('m_address')
            m_pan_number = request.POST['m_pan_number']
            m_aadhaar_number = request.POST['m_aadhaar_number']
            m_gstin = request.POST['m_gstin']
            m_cin = request.POST.get('m_cin')
            # m_CIN_certificate = request.POST['m_CIN_certificate']
            m_bank_account_number = request.POST.get('m_bank_account_number')
            m_bank_IFSC_code = request.POST.get('m_bank_IFSC_code')
            m_bank_name = request.POST.get('m_bank_name')
            m_bank_branch = request.POST.get('m_bank_branch')
            m_vat_tin_number = request.POST.get('m_vat_tin_number')
            m_GSTIN_certificate = request.POST.get('m_GSTIN_certificate')


            cust_city = form1.cleaned_data.get("m_city")
            m_city = cust_city.capitalize()

            cust_district = form1.cleaned_data.get("m_district")
            m_district = cust_district.capitalize()

            cust_state = form1.cleaned_data.get("m_state")
            m_state = cust_state.capitalize()

            cust_area = form1.cleaned_data.get("m_area")
            m_area = cust_area.capitalize()

            # m_digital_signature = request.POST['m_digital_signature']
            # m_business_logo = request.POST['m_business_logo']
            # m_business_stamp = request.POST['m_business_stamp']
            # m_cancel_bank_cheque_photo = request.POST['m_cancel_bank_cheque_photo']
            # m_other_document_certificate1 = request.POST['m_other_document_certificate1']
            # m_other_document_certificate2 = request.POST['m_other_document_certificate2']
            # m_other_document1 = request.POST['m_other_document1']
            # m_other_document2 = request.POST['m_other_document2']
            # m_business_name = request.POST['m_business_name']
            # m_business_category = request.POST['m_business_category']
            # m_city = request.POST['m_city']
            # m_landline_number = request.POST['m_landline_number']
            # m_district = request.POST['m_district']
            # m_state = request.POST['m_state']
            # m_pin_code = request.POST['m_pin_code']
            # m_area = request.POST['m_area']

            business_category_object = business_category.objects.get(id=m_business_category.id)

            MerchantProfile.objects.create(m_user_id = user_id, m_business_name = m_business_name, 
            m_business_category = business_category_object, m_city = m_city, m_district = m_district, 
            m_state = m_state, m_pin_code = m_pin_code, m_area = m_area, m_landline_number = m_landline_number,
            m_address=m_address, m_pan_number=m_pan_number, m_gstin=m_gstin,
            m_cin = m_cin,
            m_bank_account_number = m_bank_account_number,
            m_bank_IFSC_code = m_bank_IFSC_code,
            m_bank_name = m_bank_name,
            m_bank_branch = m_bank_branch,
            m_vat_tin_number=m_vat_tin_number,
            m_aadhaar_number=m_aadhaar_number)

           
            print('xvc')
            print(m_business_category)
            sweetify.success(request, title="Success", icon='success', text='Business Stored Successfully !!!')
            return redirect('/merchant-business/')
        
        else:
            print('avc')
            print(form1.errors)
            print(request.POST.get('m_business_category'))
            sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
            return redirect('/merchant-business/')
    else:
        
        form1 = merchantBusinessesBranchForm()
        
        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        data = MerchantProfile.objects.filter(m_user_id = merchant_users_object.merchant_user_id.id)
        context = {
            'form1': form1,
            'data': data,
            'merchantNavClass': "active", 
            "SettingNavclass": 'active',
            "settingsCollapseShow": "show",
            
        }
        if data:
            return render(request, "merchant/merchant_business.html",context)
        else:
            data = ""
            return render(request, "merchant/merchant_business.html",context)




@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def deleteMerchantBusiness(request, id):
    instance = MerchantProfile.objects.get(id=id)
    print('inside delete')
    print(id)
    print(instance)
    instance.delete()
    return JsonResponse({'success': True})


def deleteMerchantBusinessOwner(request, id):
    instance = MerchantProfile.objects.get(id=id)
    print('inside delete')
    print(id)
    print(instance)
    instance.delete()
    return JsonResponse({'success': True})



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def EditMyBussiness(request):
    if request.method == "POST":
        buss_id = request.POST['mid']
        bussinessname = request.POST['edit_bussiness_name']
        #bussiness_category = request.POST['edit_bussiness_category']
        pin_code = request.POST['edit_pin_code']
        state = request.POST['edit_state']
        district = request.POST['edit_district']
        city = request.POST['edit_city']                                  
        obj = MerchantProfile.objects.filter(id=buss_id).update(m_business_name=bussinessname,
                                           m_city=city, m_district=district, m_state=state, m_pin_code=pin_code)
        print(obj)
        sweetify.success(request, title="Success", icon='success', text='Business Updated Successfully !!!')
        return redirect('/merchant-business/')
    # else:
    #     sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
    #     return redirect('/merchant-business/')
