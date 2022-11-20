from payments.models import *
from partner_payment.models import *
import sweetify
import sys
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.core.mail import get_connection, send_mail, BadHeaderError, EmailMessage
from .models import *
from users.models import GreenBillUser, PartnerProfile, MerchantProfile, Partner_users
from authentication.forms import SoftwarePartnerSignUpForm, SoftwarePartnerOtherDetailsForm, SoftwareCommisionDetailsForm, SoftwarePartnerCommisionPerBillsDetailsForm, MarketingPartnerCommisionDetailsForm
from super_admin_settings.models import notification_settings
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner
from category_and_tags.models import business_category
from .forms import *
from role.models import userrole

from app.views import is_owner,is_partner,getPartnerActivePromotionalSubscriptionPlan, getPartnerActiveTransactionalSubscriptionPlan
from django.core.mail import send_mail
from owner_notice_board.sendsms import *
from .models import bulkMailSmsPartnerModel
from django.utils.html import strip_tags
from django.conf import settings
from subscription_plan.models import *
from owner_notice_board.models import OnwerNoticeBoard,OwnerSentNotice
from merchant_payment.models import PaymentLinks

import time

from merchant_setting.forms import MerchnatgeneralSettingForm

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect

from customer_info.models import Customer_Info_Model
from django.contrib import messages
import csv
import io
from django.contrib.auth.decorators import login_required, user_passes_test
import sweetify
from users.models import Merchant_users, GreenBillUser, MerchantProfile, Partner_users, PartnerUniqueIds, MerchantUniqueIds

from merchant_software_apis.models import *
from petrol_pump_apis.models import SavePetrolPumpBill
from parking_lot_apis.models import SaveParkingLotBill

from datetime import datetime, timedelta

from app.views import is_merchant_or_merchant_staff

from .forms import bulkMailSmsPartnerForm
from .models import bulkMailSmsPartnerModel
from merchant_notice.models import *
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail
from owner_notice_board.sendsms import *

from customer_info.models import Customer_Info_Model
from customer_info.forms import Customer_Info_Form, Edit_Customer_Info_Form
from authentication.forms import MerchantSignUpForm, MerchantSignUpOtherDetailsForm
from authentication.models import *
from merchant_info.models import *
from merchant_info.forms import *
from django.db.models import Subquery
from role.models import userrole
import random
import string 
from partner_setting.forms import *

from merchant_software_apis.models import CustomerBill,MerchantBill
from bill_design.models import *
from my_subscription.models import *
from django.db.models import Q
from app.views import is_owner,is_partner,getPartnerActivePromotionalSubscriptionPlan, getPartnerActiveTransactionalSubscriptionPlan

from merchant_promotion.models import bulkMailSmsMerchantCustomerModel, smsHeaderModel, templateContentModel

from offers.models import *
from coupon.models import *

from django.utils import timezone

from partner_info.models import *

import csv

import requests
import xlrd
import urllib
from merchant_cashmemo_design.models import *


# call merchant_info 

from merchant_info.views import *

# Create your views here.
@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def SoftwareList(request):
    softwarelist = PartnerProfile.objects.filter(p_category="Software Partner" , p_disabled_account=False).order_by('-id')
    softwarePartnercount = PartnerProfile.objects.filter(p_category="Software Partner", p_disabled_account=False).count()
    partnerListcount = PartnerProfile.objects.all().filter(p_disabled_account=False).count()
    temp = PartnerdiasbleReasons.objects.all().order_by('-id')

    States = StateCityData.objects.values('state').distinct().order_by('state')

    form = SoftwarePartnerSignUpForm()
    form1 = SoftwarePartnerOtherDetailsForm()
    form2 = SoftwarePartnerCommisionPerBillsDetailsForm()
        
    qs = business_category.objects.all()


    bill_commission_count = ''
    # for i in softwarelist:
    #     try:
    #         customer_object1 = GreenBillUser.objects.get(mobile_no = i.p_user)
    #         # print('customer_object1',customer_object1)
    #         partner_customer_data = Customer_Info_Model.objects.filter(per_id=customer_object1).order_by('-id')
    #         # print('partner_customer_data',partner_customer_data)
    #     # partner_customer_data = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_disabled_account=False).order_by('-id')
    #     except:
    #         customer_object1 = ""
    #         partner_customer_data = ""

    #     for bills in partner_customer_data:
    #         customer_bills = CustomerBill.objects.filter(mobile_no = bills.per_id).count()
    #         i.bill_commission_count = customer_bills * i.p_commission_per_bill

    # for i in softwarelist:
    #     if i.p_user:
    #         customer_object1 = GreenBillUser.objects.get(mobile_no = i.p_user)
    #         partner_merchants_data = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_disabled_account=False).order_by('-id')
    #         for bills in partner_merchants_data:
    #             merchant_bills = MerchantBill.objects.filter(mobile_no = bills.m_user).count()
    #             parking_bills = SaveParkingLotBill.objects.filter(mobile_no = bills.m_user).count()
    #             petrol_bills = SavePetrolPumpBill.objects.filter(mobile_no = bills.m_user).count()
    #             merchant_bills_count = merchant_bills + parking_bills + petrol_bills
    #             i.bill_commission_count = int(merchant_bills_count) * int(i.p_commission_per_bill)
            

    context = {
    'Softwarelist' : softwarelist,
    'partnerNavActiveClass': "active",
    'PartnerInfoCollapseShow': "show",
    'PartnerSoftwareNavClass' : "active",
    'software_count' : softwarePartnercount,
    'partnerListcount':partnerListcount,
    'temp':temp,
    'form': form, 
    'form1': form1,
    'form2': form2,
    'States': States,
    'business_category_list' : qs,
    }
    return render(request, "super_admin/SoftwarePartner.html", context)


# add-merchant-field-by-partner
@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def addmerchantfieldbypartner(request):
    pass



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def softwarePartnerList(request):
    if request.method == "GET":
        partnerList = PartnerProfile.objects.all().filter(p_category="Marketing Partner",p_disabled_account=False).order_by('-id')
        partnerListcount = PartnerProfile.objects.all().filter(p_disabled_account=False).count()
        
        marketingPartnercount = PartnerProfile.objects.filter(p_category="Marketing Partner", p_disabled_account=False).count()

        temp = PartnerdiasbleReasons.objects.all().order_by('-id')

        States = StateCityData.objects.values('state').distinct().order_by('state')

        form = SoftwarePartnerSignUpForm()
        form1 = SoftwarePartnerOtherDetailsForm()
        form3 = SoftwareCommisionDetailsForm()
        form4 = MarketingPartnerCommisionDetailsForm()

        partners_merchant_count = ''
        merchant_commission_count = ''
        for i in partnerList:
            try:
                customer_object1 = GreenBillUser.objects.get(mobile_no = i.p_user)
                partners_merchant_count = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_disabled_account=False).count()
            except:
                pass
            


        bill_commission_count = ''
        for i in partnerList:
            try:
                customer_object1 = GreenBillUser.objects.get(mobile_no = i.p_user)
                partner_merchants_data = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_disabled_account=False).order_by('-id')
            except:
                pass
            


        qs = business_category.objects.all()
        context = {
            'partnerListcount':partnerListcount,
            'merchant_commission_count':merchant_commission_count,
            'bill_commission_count':bill_commission_count,
            'partner_list': partnerList, 
            'partnerNavActiveClass': "active",
            'PartnerInfoCollapseShow': "show",
            'PartnerListNavclass': "active",
            'form': form, 
            'form1': form1,
            'form3': form3,
            'form4': form4,
            'business_category_list' : qs,
            'States': States,
            'temp':temp,
             'bulkMailSmsPartnerForm':bulkMailSmsPartnerForm,
            'marketing_count' : marketingPartnercount,
           
        }
        return render(request, "super_admin/software-partner-info.html", context)




@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def sendPartnerNotice(request):
    if request.method == "POST":
        title = request.POST.get('title')
        message = request.POST.get('message')
        # mobile_no = request.POST.get('mobile_number')
        # email = request.POST.get('email_id')
        smsheader = request.POST.get('smsheader')
        template_id = request.POST.get('template')
        id = request.POST.get('id')
        number = PartnerProfile.objects.get(id =id).p_user
        print('ID',id)
        print('NUMBER',number)
        # print('Mmobile', mobile_no)
        # print('Memail',email)
        print('Msmsheader',smsheader)
        print('Mtemplate',template_id)
       
        individual = GreenBillUser.objects.get(mobile_no=number, is_partner=True)
        print(individual)
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
                        
                        notice_id = bulkMailSmsPartnerModel.objects.update_or_create(owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template_id, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template_id, 'o_sent_sms':True })

                elif notice == "sent_mail":
                        
                        notice_id = bulkMailSmsPartnerModel.objects.update_or_create(owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template_id, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template_id, 'o_sent_mail':True })

                else:
                    notice_id = OnwerNoticeBoard.objects.update_or_create(owner_id=request.user, notice_title=title, message=message, defaults= { 'notice_title':title,  'message':message, 'o_notification':True })

                    print(notice_id[0].id)

                    notice_object = OnwerNoticeBoard.objects.get(id= notice_id[0].id)
                    print('notice_object::',notice_object)
          

                             
            if individual_user:
                    for notice in sent_notice:
                            
                            if notice == "sms":
                                contact = number
                                message = strip_tags(message)
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

                                    if response.status_code == 200:
                                        return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                    else:
                                        return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                    return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                    print(sms_response)
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
                                text='Notice Send successfully', timer=5500)
                # return redirect("/owner_notice_board/")
        else:
                sweetify.error(request, title="Error", icon='error',
                                text="Something Went Wrong!!!", timer=5500)
        # else:
        #     sweetify.error(request, "Please Provide Valid Data")    

    return redirect('software-partner-info')



#EDIT PARTNER

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def edit_records_of_software_partner(request, id=None):

    if request.method == "POST":

        partner_general_setting = PartnerProfile.objects.get(id = id, p_active_account = 1)

        form = PartnergeneralSettingForm(request.POST, request.FILES)

        if form.is_valid():
            partner_setting_id = request.POST["partner_setting_id"]
            business_name = form.cleaned_data.get("business_name")
            business_category_temp = request.POST.get("partner_business_category")
            pin_code = form.cleaned_data.get("pin_code")
            city = form.cleaned_data.get("city")
            area = form.cleaned_data.get('area')
            district = form.cleaned_data.get("district")
            state = form.cleaned_data.get("state")
            address = form.cleaned_data.get("address")
            landline_number = form.cleaned_data.get("landline_number")
            alternate_mobile_number = form.cleaned_data.get("alternate_mobile_number")
            p_website_url = form.cleaned_data.get("p_website_url")
            company_email = form.cleaned_data.get("company_email")
            alternate_email = form.cleaned_data.get("alternate_email")
            pan_number = form.cleaned_data.get("pan_number")
            aadhaar_number = form.cleaned_data.get('aadhaar_number')
            tin_vat_number = form.cleaned_data.get('tin_vat_number')
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
            cancel_bank_cheque_photo = form.cleaned_data.get("cancelled_cheque_certificate")
            udyog_adhar_certificate_file = form.cleaned_data.get("udyog_adhar_certificate")
            address_proof_file = form.cleaned_data.get("address_proof")
            p_business_name_for_billing = form.cleaned_data.get("p_business_name_for_billing")
            p_billing_phone = form.cleaned_data.get("p_billing_phone")
            p_billing_address = form.cleaned_data.get("p_billing_address")
            p_billing_email = form.cleaned_data.get("p_billing_email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            p_bank_account_entity = form.cleaned_data.get("p_bank_account_entity")
            p_adress_account_entity = form.cleaned_data.get("p_adress_account_entity")

            p_pan_legal_entity = form.cleaned_data.get("p_pan_legal_entity")
            p_signature_proof = form.cleaned_data.get("p_signature_proof")
            p_company_registration_certificate = form.cleaned_data.get("p_company_registration_certificate")
            p_payu_schedule_upload = form.cleaned_data.get("p_payu_schedule_upload")

            business_category_object = business_category.objects.get(id=business_category_temp)
            # business_category_object = business_category.objects.get(id=business_category_temp)

            GreenBillUser.objects.filter(mobile_no = partner_general_setting.p_user).update(first_name = first_name, last_name = last_name)

            PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={'p_business_name_for_billing': p_business_name_for_billing, 
            'p_business_name': business_name, 'p_business_category': business_category_object, 'p_pin_code': pin_code, 'p_city': city, 'p_area':area,
            'p_district': district, 'p_state': state, 'p_address': address, 'p_landline_number': landline_number, 'p_alternate_mobile_number': alternate_mobile_number,
            'p_company_email': company_email, 'p_alternate_email' : alternate_email, 'p_pan_number': pan_number, 'p_gstin': gstin, 'p_cin': cin, 'p_website_url': p_website_url,
            'p_bank_account_number': bank_account_number, 'p_bank_IFSC_code': bank_IFSC_code, 'p_bank_name' : bank_name, 'p_bank_branch' : bank_branch, 'p_aadhaar_number':aadhaar_number,
            'p_vat_tin_number':tin_vat_number, 'p_billing_phone':p_billing_phone, 'p_billing_address':p_billing_address, 'p_billing_email':p_billing_email,
            'p_bank_account_entity':p_bank_account_entity, 'p_adress_account_entity':p_adress_account_entity})

            for all in PartnerProfile.objects.filter(p_user=request.user,p_business_name=business_name):

                if profile_image:
                    UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "p_profile_image" : profile_image })
                
                if GSTIN_certificate:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_GSTIN_certificate" : GSTIN_certificate })

                if CIN_certificate:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_CIN_certificate" : CIN_certificate })
                
                if business_logo:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_business_logo" : business_logo })

                if business_stamp:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_business_stamp" : business_stamp })

                if digital_signature:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_digital_signature" : digital_signature })

                if cancel_bank_cheque_photo:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_cancelled_cheque_certificate" : cancel_bank_cheque_photo })


                if udyog_adhar_certificate_file:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_udyog_adhar_certificate" : udyog_adhar_certificate_file })
                
                if address_proof_file:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "address_proof" : address_proof_file })

                if p_pan_legal_entity:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_pan_legal_entity" : p_pan_legal_entity })

                if p_signature_proof:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_signature_proof" : p_signature_proof })

                if p_company_registration_certificate:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_company_registration_certificate" : p_company_registration_certificate })

                if p_payu_schedule_upload:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_payu_schedule_upload" : p_payu_schedule_upload })
            

            sweetify.success(request, title="Success", icon='success',
                             text='Business Settings Stored Successfully !!!', timer=1000)

            return HttpResponseRedirect('/partner-info-edit-software-record/'+str(id)+'/')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!', timer=1000)
            return HttpResponseRedirect('/partner-info-edit-software-record/'+str(id)+'/')
    else:
        partner_general_setting = PartnerProfile.objects.get(id = id)
        partner_objects_id = GreenBillUser.objects.get(mobile_no = partner_general_setting.p_user)
        partner_business_category = business_category.objects.all()
        States = StateCityData.objects.values('state').distinct().order_by('state')
        
        form = PartnergeneralSettingForm()

        context = {
            'partnerNavActiveClass': "active",
            'PartnerInfoCollapseShow': "show",
            'States': States,
            'PartnerSoftwareNavClass' : "active",
            'partner_objects_id':partner_objects_id,
            'form' : form,
            'partner_general_setting': partner_general_setting,
            'partner_business_category': partner_business_category,
        }
            
        return render(request, "super_admin/edit-all-details-of-partner.html", context)



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def edit_records_of_partner(request, id=None):

    if request.method == "POST":
        partner_general_setting = PartnerProfile.objects.get(id = id, p_active_account = 1)

        form = PartnergeneralSettingForm(request.POST, request.FILES)

        if form.is_valid():
            partner_setting_id = request.POST["partner_setting_id"]
            business_name = form.cleaned_data.get("business_name")
            business_category_temp = request.POST.get("partner_business_category")
            pin_code = form.cleaned_data.get("pin_code")
            city = form.cleaned_data.get("city")
            area = form.cleaned_data.get('area')
            district = form.cleaned_data.get("district")
            state = form.cleaned_data.get("state")
            address = form.cleaned_data.get("address")
            landline_number = form.cleaned_data.get("landline_number")
            alternate_mobile_number = form.cleaned_data.get("alternate_mobile_number")
            p_website_url = form.cleaned_data.get("p_website_url")
            company_email = form.cleaned_data.get("company_email")
            alternate_email = form.cleaned_data.get("alternate_email")
            pan_number = form.cleaned_data.get("pan_number")
            aadhaar_number = form.cleaned_data.get('aadhaar_number')
            tin_vat_number = form.cleaned_data.get('tin_vat_number')
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
            cancel_bank_cheque_photo = form.cleaned_data.get("cancelled_cheque_certificate")
            udyog_adhar_certificate_file = form.cleaned_data.get("udyog_adhar_certificate")
            address_proof_file = form.cleaned_data.get("address_proof")
            p_business_name_for_billing = form.cleaned_data.get("p_business_name_for_billing")
            p_billing_phone = form.cleaned_data.get("p_billing_phone")
            p_billing_address = form.cleaned_data.get("p_billing_address")
            p_billing_email = form.cleaned_data.get("p_billing_email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            p_bank_account_entity = form.cleaned_data.get("p_bank_account_entity")
            p_adress_account_entity = form.cleaned_data.get("p_adress_account_entity")

            p_pan_legal_entity = form.cleaned_data.get("p_pan_legal_entity")
            p_signature_proof = form.cleaned_data.get("p_signature_proof")
            p_company_registration_certificate = form.cleaned_data.get("p_company_registration_certificate")
            p_payu_schedule_upload = form.cleaned_data.get("p_payu_schedule_upload")

            business_category_object = business_category.objects.get(id=business_category_temp)
            # business_category_object = business_category.objects.get(id=business_category_temp)

            GreenBillUser.objects.filter(mobile_no = partner_general_setting.p_user).update(first_name = first_name, last_name = last_name)

            PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={'p_business_name_for_billing': p_business_name_for_billing, 
            'p_business_name': business_name, 'p_business_category': business_category_object, 'p_pin_code': pin_code, 'p_city': city, 'p_area':area,
            'p_district': district, 'p_state': state, 'p_address': address, 'p_landline_number': landline_number, 'p_alternate_mobile_number': alternate_mobile_number,
            'p_company_email': company_email, 'p_alternate_email' : alternate_email, 'p_pan_number': pan_number, 'p_gstin': gstin, 'p_cin': cin, 'p_website_url': p_website_url,
            'p_bank_account_number': bank_account_number, 'p_bank_IFSC_code': bank_IFSC_code, 'p_bank_name' : bank_name, 'p_bank_branch' : bank_branch, 'p_aadhaar_number':aadhaar_number,
            'p_vat_tin_number':tin_vat_number, 'p_billing_phone':p_billing_phone, 'p_billing_address':p_billing_address, 'p_billing_email':p_billing_email,
            'p_bank_account_entity':p_bank_account_entity, 'p_adress_account_entity':p_adress_account_entity})

            for all in PartnerProfile.objects.filter(p_user=request.user,p_business_name=business_name):

                if profile_image:
                    UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "p_profile_image" : profile_image })
                
                if GSTIN_certificate:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_GSTIN_certificate" : GSTIN_certificate })

                if CIN_certificate:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_CIN_certificate" : CIN_certificate })
                
                if business_logo:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_business_logo" : business_logo })

                if business_stamp:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_business_stamp" : business_stamp })

                if digital_signature:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_digital_signature" : digital_signature })

                if cancel_bank_cheque_photo:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_cancelled_cheque_certificate" : cancel_bank_cheque_photo })


                if udyog_adhar_certificate_file:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_udyog_adhar_certificate" : udyog_adhar_certificate_file })
                
                if address_proof_file:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "address_proof" : address_proof_file })

                if p_pan_legal_entity:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_pan_legal_entity" : p_pan_legal_entity })

                if p_signature_proof:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_signature_proof" : p_signature_proof })

                if p_company_registration_certificate:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_company_registration_certificate" : p_company_registration_certificate })

                if p_payu_schedule_upload:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_payu_schedule_upload" : p_payu_schedule_upload })



            msg = 'success'
            # return redirect('/partner-info-edit-record/'+str(id)+'/')
        else:
            msg = 'error'
            # sweetify.error(request, title="error",
            #                icon='error', text='Failed !!!', timer=1000)
            # return redirect('/partner-info-edit-record/'+str(id)+'/')
        partner_general_setting = PartnerProfile.objects.get(id=id)

        partner_objects_id = GreenBillUser.objects.get(mobile_no = partner_general_setting.p_user)

        partner_business_category = business_category.objects.all()
        States = StateCityData.objects.values('state').distinct().order_by('state')
        form = PartnergeneralSettingForm()

        context = {
            'msg' : msg,
            'form' : form,
            'States': States,
            'partner_general_setting': partner_general_setting,
            'partner_business_category': partner_business_category,
            'partner_objects_id': partner_objects_id,
            "SettingNavclass": 'active',
            "settingsCollapseShow": "show",
            "GeneralSettingsNavclass": 'active'
        }

        return render(request, "super_admin/edit-all-details-of-partner.html", context)

        # form = MarketingPartnergeneralSettingForm(request.POST, request.FILES)

        # if form.is_valid():
        #     partner_setting_id = request.POST["partner_setting_id"]
        #     business_name = form.cleaned_data.get("business_name")
        #     business_category_temp = request.POST.get("p_category")
        #     pin_code = form.cleaned_data.get("pin_code")
        #     city = form.cleaned_data.get("city")
        #     area = form.cleaned_data.get('area')
        #     district = form.cleaned_data.get("district")
        #     state = form.cleaned_data.get("state")
        #     address = form.cleaned_data.get("address")
        #     landline_number = form.cleaned_data.get("landline_number")
        #     alternate_mobile_number = form.cleaned_data.get("alternate_mobile_number")
        #     company_email = form.cleaned_data.get("company_email")
        #     alternate_email = form.cleaned_data.get("alternate_email")
        #     pan_number = form.cleaned_data.get("pan_number")
        #     aadhaar_number = form.cleaned_data.get('aadhaar_number')
        #     tin_vat_number = form.cleaned_data.get('tin_vat_number')
        #     gstin = form.cleaned_data.get("gstin")
        #     GSTIN_certificate = form.cleaned_data.get("GSTIN_certificate")
        #     cin = form.cleaned_data.get("cin")
        #     CIN_certificate = form.cleaned_data.get("CIN_certificate")
        #     profile_image = form.cleaned_data.get("profile_image")
        #     business_logo = form.cleaned_data.get("business_logo")
        #     business_stamp = form.cleaned_data.get("business_stamp")
        #     digital_signature = form.cleaned_data.get("digital_signature")
        #     bank_account_number = form.cleaned_data.get("bank_account_number")
        #     bank_IFSC_code = form.cleaned_data.get("bank_IFSC_code")
        #     bank_name = form.cleaned_data.get("bank_name")
        #     bank_branch = form.cleaned_data.get("bank_branch")
        #     cancel_bank_cheque_photo = form.cleaned_data.get("cancel_bank_cheque_photo")
        #     udyog_adhar_certificate_file = form.cleaned_data.get("udyog_adhar_certificate_file")
        #     p_commission_per_sms_bill = form.cleaned_data.get("p_commission_per_sms_bill")
        #     p_commission_per_digital_bill = form.cleaned_data.get("p_commission_per_digital_bill")
        #     merchant_commission = form.cleaned_data.get("merchant_commission")

            
        #     # business_category_object = business_category.objects.get(id=business_category_temp)

        #     PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={'merchant_commission': merchant_commission, 'p_commission_per_digital_bill': p_commission_per_digital_bill, 'p_commission_per_sms_bill' : p_commission_per_sms_bill, 'p_business_name': business_name, 'p_pin_code': pin_code, 'p_city': city, 'p_area':area, 'p_district': district, 'p_state': state, 'p_address': address, 'p_landline_number': landline_number, 'p_alternate_mobile_number': alternate_mobile_number, 'p_company_email': company_email, 'p_alternate_email' : alternate_email, 'p_pan_number': pan_number, 'p_gstin': gstin, 'p_cin': cin, 'p_bank_account_number': bank_account_number, 'p_bank_IFSC_code': bank_IFSC_code, 'p_bank_name' : bank_name, 'p_bank_branch' : bank_branch, 'p_aadhaar_number':aadhaar_number,'p_vat_tin_number':tin_vat_number})

        #     if profile_image:
        #         UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "p_profile_image" : profile_image })
            
        #     if GSTIN_certificate:
        #         PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_GSTIN_certificate" : GSTIN_certificate })

        #     if CIN_certificate:
        #         PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_CIN_certificate" : CIN_certificate })
            
        #     if business_logo:
        #         PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_business_logo" : business_logo })

        #     if business_stamp:
        #         PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_business_stamp" : business_stamp })

        #     if digital_signature:
        #         PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_digital_signature" : digital_signature })

        #     if cancel_bank_cheque_photo:
        #         PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_cancelled_cheque_certificate" : cancel_bank_cheque_photo })


        #     if udyog_adhar_certificate_file:
        #         PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "m_udyog_adhar_certificate" : udyog_adhar_certificate_file })
            

        #     sweetify.success(request, title="Success", icon='success',
        #                      text='Business Settings Stored Successfully !!!', timer=1000)

        #     return HttpResponseRedirect('/partner-info-edit-record/'+str(id)+'/')
        # else:
        #     sweetify.error(request, title="error",
        #                    icon='error', text='Failed !!!', timer=1000)
        #     return HttpResponseRedirect('/partner-info-edit-record/'+str(id)+'/')
    else:
        partner_general_setting = PartnerProfile.objects.get(id=id)

        partner_objects_id = GreenBillUser.objects.get(mobile_no = partner_general_setting.p_user)

        partner_business_category = business_category.objects.all()
        States = StateCityData.objects.values('state').distinct().order_by('state')
        form = PartnergeneralSettingForm()

        context = {
            'msg': None,
            'form' : form,
            'States': States,
            'partner_general_setting': partner_general_setting,
            'partner_business_category': partner_business_category,
            'partner_objects_id': partner_objects_id,
            "SettingNavclass": 'active',
            "settingsCollapseShow": "show",
            "GeneralSettingsNavclass": 'active'
        }
            
        return render(request, "super_admin/edit-all-details-of-partner.html", context)


#DISABLED Partner FUNCTION
@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def disabledPartner(request):
    qs = business_category.objects.all()
    
    partnerList = PartnerProfile.objects.all().filter(p_disabled_account=True).distinct().order_by('-id')
    partnerListcount = PartnerProfile.objects.all().filter(p_disabled_account=True).count()
    context = {
        'qs': qs,
        'partnerList' : partnerList,
        'partnerListcount' : partnerListcount,
        'partnerNavActiveClass': "active", 
         'PartnerInfoCollapseShow': "show",
         'PartnerDisabledNavclass': "active",
    }
    return render(request, 'super_admin/disabled-partner.html', context)





# #LATEST PARTNER FUNCTION
# def latestPartner(request):
#     qs = business_category.objects.all()

#     partnerList = PartnerProfile.objects.filter(p_latest_account=True,p_disabled_account=True).order_by('-id')
#     partnerListCount = PartnerProfile.objects.filter(p_latest_account=True,p_disabled_account=True).count()
#     context = {
#         'qs': qs,
#         'partnerList' : partnerList,
#         'partnerListCount' : partnerListCount,
#         'partnerNavActiveClass': "active", 
#         'PartnerInfoCollapseShow': "show",
#         'PartnerLatestNavclass': "active",
#     }
#     return render(request, 'super_admin/latest-partner.html', context)


def deletePartner(request,id):
    if request.method == "POST":
        instance = PartnerProfile.objects.get(id=id)
        instance.delete()
        return JsonResponse({'success': True})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def disablePartnerFromAdmin(request):
    if request.method == "POST":
        disable_partner_mobile_no = request.POST['disable_partner_mobile_no']
        partner_id = request.POST['partner_id']
        reason = request.POST['reason']
        print(partner_id)
        PartnerProfile.objects.filter(id= partner_id).update(p_disabled_account=True, disapprove_reason= reason)
        #GreenBillUser.objects.filter(id= partner_id, is_partner=True).update(is_active=False)
        GreenBillUser.objects.filter(mobile_no= disable_partner_mobile_no).update(is_partner=False)
        return JsonResponse({'status': 1, 'msg': 'Status change successfully'})
        
    else:
        return JsonResponse({'status': 0, 'msg': 'Something went wrong'})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def disapprovePartner(request):
    if request.method == "POST":
        
        partner_id = request.POST['partner_id']
        print(partner_id)
        reason = request.POST['reason']
        PartnerProfile.objects.filter(id=partner_id).update(p_disabled_account=True, disapprove_reason= reason,status=2)
        GreenBillUser.objects.filter(id= partner_id, is_partner=True).update(is_active=False)
        return JsonResponse({'status': 1, 'msg': 'Status change successfully'})
        
    else:
        return JsonResponse({'status': 0, 'msg': 'Something went wrong'})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def enablePartnerFromAdmin(request, id):
    if request.method == "POST":

    	partner_id = PartnerProfile.objects.get(id=id).p_user

    	GreenBillUser.objects.filter(mobile_no=partner_id).update(is_partner = True)

    	PartnerProfile.objects.filter(id= id).update(p_disabled_account=False,status=1)

    	GreenBillUser.objects.filter(id= partner_id).update(is_active=True)
    	return JsonResponse({'status': 1, 'msg': 'Status change successfully'})
        
    else:
        return JsonResponse({'status': 0, 'msg': 'Something went wrong'})



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def addsoftwarePartnerByAdmin(request):
    
    if request.method == "POST":
        form = SoftwarePartnerSignUpForm1(request.POST)
        form1 = SoftwarePartnerOtherDetailsForm(request.POST)
        form2 = SoftwarePartnerCommisionPerBillsDetailsForm(request.POST)

        if form.is_valid() and form1.is_valid() and form2.is_valid():
            mobile_no = form.cleaned_data.get("mobile_no")
            try:
                is_partner = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_partner')[0]['is_partner']
            except:
                is_partner = ""
            
            if is_partner:

                return JsonResponse({'status':'error', 'msg': "Partner with this number is already exists."})
            else:
                try:
                    userRoleDetails = userrole.objects.filter(user = request.user.id)
                except:
                    userRoleDetails[0].role = "Super Admin"

                p_category="Software Partner",

                temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

                user_id = GreenBillUser.objects.create_user(
                    mobile_no = mobile_no,
                    p_email = form.cleaned_data.get('p_email'),
                    password = temp_password,
                )
                
                GreenBillUser.objects.filter(mobile_no = user_id).update(is_partner = 1)

                # Unique Id Start

                try:
                    last_unique_id = PartnerUniqueIds.objects.all().last()
                except:
                    last_unique_id = ""

                if not last_unique_id:
                    p_unique_id = str("GBP") + str("01").zfill(6)
                    no = 1
                else:
                    last_no = last_unique_id.p_unique_no
                    no = int(last_no) + 1
                    p_unique_id = str("GBP") + str(no).zfill(6)

                unique_id_status = GreenBillUser.objects.filter(mobile_no = user_id).update(p_unique_id = p_unique_id)

                if unique_id_status:
                    PartnerUniqueIds.objects.create(p_unique_no = no)

                # Unique Id End

                if userRoleDetails[0].role == "Sales" :
                    GreenBillUser.objects.filter(mobile_no = user_id).update(is_active=False, created_by= userRoleDetails[0].role)
                else:
                    GreenBillUser.objects.filter(mobile_no = user_id).update(is_active= True)
                
                p_email = form.cleaned_data.get("p_email")
                p_business_name = form1.cleaned_data.get("p_business_name")
                p_business_description = form1.cleaned_data.get("p_business_description")
                p_business_category = form1.cleaned_data.get("p_business_category")
                
                p_pin_code = form1.cleaned_data.get("p_pin_code")
                p_commission_per_bill = form2.cleaned_data.get("p_commission_per_bill")
                p_commission_per_sms_bill = form2.cleaned_data.get("p_cost_per_sms")
                p_category = form1.cleaned_data.get("p_category")
                merchant_commission = form1.cleaned_data.get("merchant_commission")

                loyalti_point_status = form1.cleaned_data.get("loyalty_point")

                par_city = form1.cleaned_data.get("p_city")
                p_city = par_city.capitalize()

                par_district = form1.cleaned_data.get("p_district")
                p_district = par_district.capitalize()

                par_state = form1.cleaned_data.get("p_state")
                p_state = par_state.capitalize()

                PartnerProfile.objects.create(p_user = user_id, p_business_name = p_business_name, 
                    p_business_description= p_business_description, p_business_category = p_business_category, 
                    p_city = p_city, p_district = p_district, 
                    p_state = p_state, p_pin_code = p_pin_code, p_commission_per_bill= p_commission_per_bill, 
                    p_commission_per_sms_bill = p_commission_per_sms_bill,
                    p_category="Software Partner", p_active_account=1, p_disabled_account= False,loyalty_point=loyalti_point_status)

                partner_users_object = Partner_users.objects.create(partner_user_id = user_id, user_id = user_id)
                
                mobile_no = form.cleaned_data.get("mobile_no")
                raw_password = temp_password
                user = authenticate(mobile_no=mobile_no, password=raw_password)

                subject = 'Thank You For Registration.'
                message = f' Dear Valued Partner, \n Warm Greetings from Green Bill Team!!! \n We are glad to see you chose Green Bill as Software Partner and below are your login credentials for the same \n URL: http://157.230.228.250/partner-login/ \n Username: {mobile_no} \n Password: {raw_password} \n You are advised to login and complete your profile and business details for better coordination.'
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [user_id.p_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()

                return JsonResponse({'status': 'success', 'msg': 'Partner added successfully !!!'})
        else:
            mobile_no = request.POST['mobile_no']
            p_email = request.POST['p_email']
            p_category="Software Partner",
            try:
                is_customer = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_customer')[0]['is_customer']
            except:
                is_customer = ''

            user_object = GreenBillUser.objects.filter(mobile_no = mobile_no)

            if user_object[0].is_staff:
                return JsonResponse({'status':'error', 'msg': "User already Exists."})
            elif (user_object[0].is_merchant or user_object[0].is_merchant_staff):
                return JsonResponse({'status':'error', 'msg': "User already Exists."})
            elif user_object[0].is_partner:
                return JsonResponse({'status':'error', 'msg': "User already Exists."})
            elif user_object[0].is_customer:

                try:
                    userRoleDetails = userrole.objects.filter(user = request.user.id)
                except:
                    userRoleDetails[0].role = "Super Admin"

                # temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

                GreenBillUser.objects.filter(
                    mobile_no = mobile_no).update(p_email = p_email)

                user_id = GreenBillUser.objects.get(mobile_no = mobile_no)

                password = user_id.password
                
                
                GreenBillUser.objects.filter(mobile_no = user_id).update(is_partner = 1)

                # Unique Id Start

                try:
                    last_unique_id = PartnerUniqueIds.objects.all().last()
                except:
                    last_unique_id = ""

                if not last_unique_id:
                    p_unique_id = str("GBP") + str("01").zfill(6)
                    no = 1
                else:
                    last_no = last_unique_id.p_unique_no
                    no = int(last_no) + 1
                    p_unique_id = str("GBP") + str(no).zfill(6)

                unique_id_status = GreenBillUser.objects.filter(mobile_no = user_id).update(p_unique_id = p_unique_id)

                if unique_id_status:
                    PartnerUniqueIds.objects.create(p_unique_no = no)

                # Unique Id End

                if userRoleDetails[0].role == "Sales" :
                    GreenBillUser.objects.filter(mobile_no = user_id).update(is_active=False, created_by= userRoleDetails[0].role)
                else:
                    GreenBillUser.objects.filter(mobile_no = user_id).update(is_active= True)
                
                p_email = request.POST['p_email']
                p_business_name = request.POST["p_business_name"]
                p_business_description = request.POST["p_business_description"]
                # p_business_category = request.POST["p_business_category"]
                par_city = request.POST["p_city"]
                p_city = par_city.capitalize()

                par_district = request.POST["p_district"]
                p_district = par_district.capitalize()

                par_state = request.POST["p_state"]
                p_state = par_state.capitalize()
                
                p_pin_code = request.POST["p_pin_code"]
                p_commission_per_bill = request.POST["p_commission_per_bill"]
                p_commission_per_sms_bill = request.POST["p_cost_per_sms"]
                p_category = request.POST["p_category"]
                merchant_commission = request.POST['merchant_commission']

                PartnerProfile.objects.create(p_user = user_id, p_business_name = p_business_name, 
                    p_business_description= p_business_description, 
                    p_city = p_city, p_district = p_district, 
                    p_state = p_state, p_pin_code = p_pin_code, p_commission_per_bill= p_commission_per_bill,
                    p_commission_per_sms_bill = p_commission_per_sms_bill,
                     p_category="Software Partner", p_active_account=1, p_disabled_account= False)

                partner_users_object = Partner_users.objects.create(partner_user_id = user_id, user_id = user_id)
                
                # mobile_no = form.cleaned_data.get("mobile_no")
                # raw_password = temp_password
                # user = authenticate(mobile_no=mobile_no, password=raw_password)

                raw_password = 0

                subject = 'Thank You For Registration.'
                message = f' Dear Valued Partner, \n Warm Greetings from Green Bill Team!!! \n We are glad to see you chose Green Bill as Software Partner and below are your login credentials for the same \n URL: http://157.230.228.250/partner-login/ \n Username: {mobile_no} \n Password is same as your Customer Account \n You are advised to login and complete your profile and business details for better coordination.'
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [user_id.p_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()

                return JsonResponse({'status': 'success', 'msg': 'Partner added successfully !!!'})
            
            else:
                return JsonResponse({'status':'error', 'msg': "User already Exists."})
    else:
        return JsonResponse({'status': 'error', 'msg': 'Something went wrong !!!'})




@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def addPartnerByAdmin(request):
    
    if request.method == "POST":
        form = SoftwarePartnerSignUpForm1(request.POST)
        form1 = SoftwarePartnerOtherDetailsForm(request.POST)
        form2 = SoftwareCommisionDetailsForm(request.POST)
        form3 = MarketingPartnerCommisionDetailsForm(request.POST)
        
        
        if form.is_valid() and form1.is_valid() and form2.is_valid() and form3.is_valid():
            mobile_no = form.cleaned_data.get("mobile_no")
            try:
                is_partner = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_partner')[0]['is_partner']
            except:
                is_partner = ""
            
            if is_partner:

                return JsonResponse({'status':'error', 'msg': "Partner with this number is already exists."})
            else:
                try:
                    userRoleDetails = userrole.objects.filter(user = request.user.id)
                except:
                    userRoleDetails[0].role = "Super Admin"

                p_category="Marketing Partner"


                temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

                user_id = GreenBillUser.objects.create_user(
                    mobile_no = mobile_no,
                    p_email = form.cleaned_data.get('p_email'),
                    password = temp_password,
                )
                
                GreenBillUser.objects.filter(mobile_no = user_id).update(is_partner = 1)

                # Unique Id Start

                try:
                    last_unique_id = PartnerUniqueIds.objects.all().last()
                except:
                    last_unique_id = ""

                if not last_unique_id:
                    p_unique_id = str("GBP") + str("01").zfill(6)
                    no = 1
                else:
                    last_no = last_unique_id.p_unique_no
                    no = int(last_no) + 1
                    p_unique_id = str("GBP") + str(no).zfill(6)

                unique_id_status = GreenBillUser.objects.filter(mobile_no = user_id).update(p_unique_id = p_unique_id)

                if unique_id_status:
                    PartnerUniqueIds.objects.create(p_unique_no = no)

                # Unique Id End

                if userRoleDetails[0].role == "Sales" :
                    GreenBillUser.objects.filter(mobile_no = user_id).update(is_active=False, created_by= userRoleDetails[0].role)
                else:
                    GreenBillUser.objects.filter(mobile_no = user_id).update(is_active= True)
                
                p_email = form.cleaned_data.get("p_email")
                p_business_name = form1.cleaned_data.get("p_business_name")
                p_business_description = form1.cleaned_data.get("p_business_description")
                p_business_category = form1.cleaned_data.get("p_business_category")

                par_city = form1.cleaned_data.get("p_city")
                p_city = par_city.capitalize()

                par_district = form1.cleaned_data.get("p_district")
                p_district = par_district.capitalize()

                par_state = form1.cleaned_data.get("p_state")
                p_state = par_state.capitalize()

                p_pin_code = form1.cleaned_data.get("p_pin_code")
                p_commission_per_sms_bill = form3.cleaned_data.get("p_commission_per_sms_bill")
                p_commission_per_digital_bill = form3.cleaned_data.get("p_commission_per_digital_bill")
                p_commission_per_other_services = form3.cleaned_data.get("p_commission_per_other_services")
                p_category = form1.cleaned_data.get("p_category")
                merchant_commission = form2.cleaned_data.get("merchant_commission")

                PartnerProfile.objects.create(p_user = user_id, p_business_name = p_business_name, 
                    p_business_description= p_business_description, p_business_category = p_business_category, 
                    p_city = p_city, p_district = p_district, 
                    p_state = p_state, p_pin_code = p_pin_code, p_commission_per_sms_bill= p_commission_per_sms_bill,
                     p_commission_per_digital_bill= p_commission_per_digital_bill, p_commission_per_other_services = p_commission_per_other_services,
                     p_category="Marketing Partner", p_active_account=1, p_disabled_account= False,merchant_commission=merchant_commission)

                partner_users_object = Partner_users.objects.create(partner_user_id = user_id, user_id = user_id)
                
                mobile_no = form.cleaned_data.get("mobile_no")
                raw_password = temp_password
                user = authenticate(mobile_no=mobile_no, password=raw_password)

                subject = 'Thank You For Registration.'
                message = f' Dear Valued Partner, \n Warm Greetings from Green Bill Team!!! \n We are glad to see you chose Green Bill as Marketing Partner and below are your login credentials for the same \n URL: http://157.230.228.250/partner-login/ \n Username: {mobile_no} \n Password: {raw_password} \n You are advised to login and complete your profile and business details for better coordination.'
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [user_id.p_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()

                return JsonResponse({'status': 'success', 'msg': 'Partner added successfully !!!'})
        else:
            mobile_no = request.POST['mobile_no']
            p_email = request.POST['p_email']
            p_category="Marketing Partner"

            # mobile_no = form.cleaned_data.get("mobile_no")
            try:
                is_partner = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_partner')[0]['is_partner']
            except:
                is_partner = ""
            
            if is_partner:

                return JsonResponse({'status':'error', 'msg': "Partner with this number is already exists."})
            else:
                try:
                    userRoleDetails = userrole.objects.filter(user = request.user.id)
                except:
                    userRoleDetails[0].role = "Super Admin"

                p_category="Marketing Partner"


                temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

                user_id = GreenBillUser.objects.create_user(
                    mobile_no = mobile_no,
                    p_email = p_email,
                    password = temp_password,
                )
                
                GreenBillUser.objects.filter(mobile_no = user_id).update(is_partner = 1)

                # Unique Id Start

                try:
                    last_unique_id = PartnerUniqueIds.objects.all().last()
                except:
                    last_unique_id = ""

                if not last_unique_id:
                    p_unique_id = str("GBP") + str("01").zfill(6)
                    no = 1
                else:
                    last_no = last_unique_id.p_unique_no
                    no = int(last_no) + 1
                    p_unique_id = str("GBP") + str(no).zfill(6)

                unique_id_status = GreenBillUser.objects.filter(mobile_no = user_id).update(p_unique_id = p_unique_id)

                if unique_id_status:
                    PartnerUniqueIds.objects.create(p_unique_no = no)

                # Unique Id End

                if userRoleDetails[0].role == "Sales" :
                    GreenBillUser.objects.filter(mobile_no = user_id).update(is_active=False, created_by= userRoleDetails[0].role)
                else:
                    GreenBillUser.objects.filter(mobile_no = user_id).update(is_active= True)
                
                p_email = request.POST['p_email']
                p_business_name = request.POST["p_business_name"]
                p_business_description = request.POST["p_business_description"]
                # p_business_category = request.POST["p_business_category"]
                # p_city = request.POST["p_city"]
                # p_district = request.POST["p_district"]
                # p_state = request.POST["p_state"]
                par_city = request.POST["p_city"]
                p_city = par_city.capitalize()

                par_district = request.POST["p_district"]
                p_district = par_district.capitalize()

                par_state = request.POST["p_state"]
                p_state = par_state.capitalize()

                p_pin_code = request.POST["p_pin_code"]
                p_commission_per_sms_bill = request.POST["p_commission_per_sms_bill"]
                p_commission_per_digital_bill = request.POST["p_commission_per_digital_bill"]
                p_commission_per_other_services = request.POST["p_commission_per_other_services"]
                # p_category = request.POST["p_category"]
                merchant_commission = request.POST['merchant_commission']

                PartnerProfile.objects.create(p_user = user_id, p_business_name = p_business_name, 
                    p_business_description= p_business_description, 
                    p_city = p_city, p_district = p_district, 
                    p_state = p_state, p_pin_code = p_pin_code, p_commission_per_sms_bill= p_commission_per_sms_bill,
                     p_commission_per_digital_bill= p_commission_per_digital_bill, p_commission_per_other_services = p_commission_per_other_services ,
                     p_category="Marketing Partner", p_active_account=1, p_disabled_account= False,merchant_commission=merchant_commission)

                partner_users_object = Partner_users.objects.create(partner_user_id = user_id, user_id = user_id)

                # partner_users_object = Partner_users.objects.create(partner_user_id = user_id, user_id = user_id)
                
                mobile_no = mobile_no
                raw_password = temp_password
                user = authenticate(mobile_no=mobile_no, password=raw_password)

                subject = 'Thank You For Registration.'
                message = f' Dear Valued Partner, \n Warm Greetings from Green Bill Team!!! \n We are glad to see you chose Green Bill as Marketing Partner and below are your login credentials for the same \n URL: http://157.230.228.250/partner-login/ \n Username: {mobile_no} \n Password: {raw_password} \n You are advised to login and complete your profile and business details for better coordination.'
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [user_id.p_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()

                sweetify.success(request, title="Success", icon='success', text='Partner business information updated sucessfully.')
                # return JsonResponse({'status': 'success', 'msg': 'Partner added successfully !!!'})
                return redirect("/software-partner-info/")
            
        sweetify.error(request, title="Error", icon='error', text='User already Exists.')
        return redirect("/software-partner-info/")
            # else:
        # return JsonResponse({'status':'error', 'msg': "User already Exists."})
    else:
        sweetify.error(request, title="Error", icon='error', text='User already Exists.')
        return redirect("/software-partner-info/")
        # return JsonResponse({'status': 'error', 'msg': 'Something went wrong !!!'})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def getPartnerBusinessDetails(request):
    
    if request.method == "POST":
        user_id = request.POST['user_id']
        partner_setting_id = request.POST['partner_setting_id']

        partnerBusinessDetail = PartnerProfile.objects.filter(id=partner_setting_id, p_user_id=user_id)
       
        if partnerBusinessDetail:
            
            newDict = {
                'user_id': user_id,
                'partner_setting_id': partner_setting_id,
                'p_category': partnerBusinessDetail[0].p_category,
                'p_business_name': partnerBusinessDetail[0].p_business_name,
                'p_business_description': partnerBusinessDetail[0].p_business_description,
                # 'p_business_category': partnerBusinessDetail[0].p_business_category_id,
                'p_pin_code': partnerBusinessDetail[0].p_pin_code,
                'p_state': partnerBusinessDetail[0].p_state,
                'p_district': partnerBusinessDetail[0].p_district,
                'p_city': partnerBusinessDetail[0].p_city,
                'p_address': partnerBusinessDetail[0].p_address,
                'p_landline_number': partnerBusinessDetail[0].p_landline_number,
                'p_alternate_mobile_number': partnerBusinessDetail[0].p_alternate_mobile_number,
                'p_company_email': partnerBusinessDetail[0].p_company_email,
                'p_alternate_email': partnerBusinessDetail[0].p_alternate_email,
                'p_pan_number': partnerBusinessDetail[0].p_pan_number,
                'p_gstin': partnerBusinessDetail[0].p_gstin,
                'p_cin': partnerBusinessDetail[0].p_cin,
                'p_bank_account_number': partnerBusinessDetail[0].p_bank_account_number,
                'p_bank_IFSC_code': partnerBusinessDetail[0].p_bank_IFSC_code,
                'p_bank_name': partnerBusinessDetail[0].p_bank_name,
                'p_bank_branch': partnerBusinessDetail[0].p_bank_branch,
            }
            
        else:
            newDict = ""

        return JsonResponse({'status':'success', 'business_data': newDict})
    else:
        return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def editPartnerByAdmin(request):
   
    if request.method == "POST":
        
        form = PartnerProfileEditForm(request.POST)
        
        if form.is_valid():
            
            user_id = request.POST['user_id']
            business_id = request.POST['partner_setting_id']
            
            p_category = form.cleaned_data.get("p_category")
            p_business_name = form.cleaned_data.get("p_business_name")
            p_business_description = form.cleaned_data.get("p_business_description")
            p_business_category = ""
            p_pin_code = form.cleaned_data.get("p_pin_code")
            p_state = form.cleaned_data.get("p_state")
            p_district = form.cleaned_data.get("p_district")
            p_city = form.cleaned_data.get("p_city")
           
            p_address = form.cleaned_data.get("p_address")
            p_landline_number = form.cleaned_data.get("p_landline_number")
            p_alternate_mobile_number = form.cleaned_data.get("p_alternate_mobile_number")
            p_company_email = form.cleaned_data.get("p_company_email")
            p_alternate_email = form.cleaned_data.get("p_alternate_email")
            p_pan_number = form.cleaned_data.get("p_pan_number")
            p_gstin = form.cleaned_data.get("p_gstin")
            p_cin = form.cleaned_data.get("p_cin")
            p_bank_account_number = form.cleaned_data.get("p_bank_account_number")
            p_bank_IFSC_code = form.cleaned_data.get("p_bank_IFSC_code")
            p_bank_name = form.cleaned_data.get("p_bank_name")
            p_bank_branch = form.cleaned_data.get("p_bank_branch")
            p_GSTIN_certificate = form.cleaned_data.get("p_GSTIN_certificate")
            p_CIN_certificate = form.cleaned_data.get("p_CIN_certificate")
            p_business_logo = form.cleaned_data.get("p_business_logo")
            p_business_stamp = form.cleaned_data.get("p_business_stamp")
            p_digital_signature = form.cleaned_data.get("p_digital_signature")
            
            result = PartnerProfile.objects.filter(id=business_id, p_user_id=user_id).update(p_business_name = p_business_name, p_business_description= p_business_description, p_city = p_city, p_district = p_district, p_state = p_state, p_pin_code = p_pin_code, p_address=p_address, p_landline_number=p_landline_number, p_alternate_mobile_number=p_alternate_mobile_number, p_company_email=p_company_email, p_alternate_email=p_alternate_email, p_pan_number=p_pan_number, p_gstin=p_gstin, p_cin=p_cin, p_bank_account_number=p_bank_account_number, p_bank_IFSC_code=p_bank_IFSC_code, p_bank_name=p_bank_name, p_bank_branch=p_bank_branch, p_category= p_category)

            if p_GSTIN_certificate:
                PartnerProfile.objects.update_or_create(id = business_id, defaults={ "p_GSTIN_certificate" : p_GSTIN_certificate })

            if p_CIN_certificate:
                PartnerProfile.objects.update_or_create(id = business_id, defaults={ "p_CIN_certificate" : p_CIN_certificate })
            
            if p_business_logo:
                PartnerProfile.objects.update_or_create(id = business_id, defaults={ "p_business_logo" : p_business_logo })

            if p_business_stamp:
                PartnerProfile.objects.update_or_create(id = business_id, defaults={ "p_business_stamp" : p_business_stamp })

            if p_digital_signature:
                PartnerProfile.objects.update_or_create(id = business_id, defaults={ "p_digital_signature" : p_digital_signature })
        
            if result:
                sweetify.success(request, title="Success", icon='success', text='Partner business information updated sucessfully.')
                return redirect("/software-partner-info/")
            else:
                sweetify.error(request, title="Error", icon='error', text='Unable to update business information.')
                return redirect("/software-partner-info/")
        else:
            sweetify.error(request, title="Error", icon='error', text='Something went wrong. Please try again later.')
            return redirect("/software-partner-info/")
    else:
       sweetify.error(request, title="Error", icon='error', text='Something went wrong. Please try again later.')
       return redirect("/software-partner-info/")

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def partnerBySales(request):
    if request.method == "GET":
        partnerList = PartnerProfile.objects.all()
        # for partner in partnerList:
        #     if partner.p_user.is_staff == True and partner.p_user.created_by == "Sales":
                
        context = {
            'partner_list': partnerList, 
            'partnerNavActiveClass': "active",
            'PartnerInfoCollapseShow': "show",
            'PartnerBySalesNavClass': "active",
        }
        return render(request, "super_admin/software-partner-by-sales.html", context)

# Disable

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def disablePartnerReason(request):
    if request.method == "POST":
        form = partnerDisablereasonForm(request.POST, request.FILES)
        obj1 = ""
        obj2 = ""
        if request.POST['partreasons_id'] != "":
            partner_reason = request.POST['partner_reason']

            check_exist = PartnerdiasbleReasons.objects.filter(partner_reason = partner_reason)
            if check_exist:

                sweetify.success(request, title="Oops...", icon='error', text='Already Exists.', timer=1000)
                
            else:

                obj1 = PartnerdiasbleReasons.objects.update_or_create(
                    id=int(request.POST["partreasons_id"]), defaults={"partner_reason": partner_reason})

                sweetify.success(request, title="Success", icon='success', text='Reason updated Successfully.', timer=1500)
                
        else:
            partner_reason = request.POST['partner_reason']
            check_exist = PartnerdiasbleReasons.objects.filter(partner_reason = partner_reason)
            if check_exist:
                
                sweetify.success(request, title="Oops...", icon='error', text='Already Exists.', timer=1000)

            else:

                obj2 = PartnerdiasbleReasons.objects.create(partner_reason=partner_reason)
                sweetify.success(request, title="Success", icon='success', text='Reason created Successfully.', timer=1500)
                
    
    data = PartnerdiasbleReasons.objects.all().order_by('-id')
    context = {
    'data': data, 
    'partnerNavActiveClass': "active", 
         'PartnerInfoCollapseShow': "show",
         'PartnerDisableNavclass': "active",  
    }
    return render(request, "super_admin/disable-par-reason.html", context)
def Delete_Reasons(request, id):
    status = PartnerdiasbleReasons.objects.get(id=id).delete()
    if status:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": False})


def Delete_disablePartner(request, id):
    status = PartnerProfile.objects.get(id=id).delete()
    if status:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": False})



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def viewMerchantDetailsByPartner(request, id=None):
    if request.method == "GET":
        merchantBusinessesList = MerchantProfile.objects.get(id=id)
        merchant_objects_id = GreenBillUser.objects.get(mobile_no = merchantBusinessesList.m_user)
        form = MerchnatgeneralSettingForm()
        print('list',merchantBusinessesList.m_user)
        print(id)
        merchnat_business_category = business_category.objects.all()

    if request.method == "POST":
        print('ID',id)
        form = MerchnatgeneralSettingForm(request.POST, request.FILES)
        merchantBusinessesList = MerchantProfile.objects.get(id=id)
        print(form.errors)

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

            print('aa',merchantBusinessesList.m_user)
            
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

            return redirect('/merchant-info-view-record/'+str(id)+'/')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!', timer=1000)
            return redirect('/merchant-info-view-record/'+str(id)+'/')
    else:
        
        # merchant_users_object = Merchant_users.objects.get(user_id = merchantBusinessesList.m_user  )
        # print('obj',merchant_users_object.id)
        print('QQQ')
        print(id)
        States = StateCityData.objects.values('state').distinct().order_by('state')
        merchant_general_setting = MerchantProfile.objects.get(id = id)
        print(merchant_general_setting)
        merchnat_business_category = business_category.objects.all()
        
        form1 = MerchnatgeneralSettingForm()
        context = {
            # 'merchantBusinessesList' : merchantBusinessesList,
            'merchantBusinessCategory' : merchnat_business_category,
            'merchantBusinessCategory' : merchnat_business_category,
            'form': form1,
            'States': States,
            'merchant_b_id': id,
            'merchant_objects_id': merchant_objects_id,
            'partnerNavActiveClass': "active",
            'PartnerInfoCollapseShow': "show",
            'PartnerListNavclass': "active",
            'merchant_general_setting': merchant_general_setting, 
            'merchnat_business_category': merchnat_business_category, 
        }
        return render(request, "super_admin/edit-all-details-of-merchant.html", context)



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def viewMerchantDetailsOfsoftwarePartner(request, id=None):
    print("okkkkkkkkk")
    if request.method == "GET":
        merchantBusinessesList = MerchantProfile.objects.get(id=id)
        merchant_objects_id = GreenBillUser.objects.get(mobile_no = merchantBusinessesList.m_user)
        form = merchantEditBusinessesForm()
        print('list',merchantBusinessesList.m_user)
        print(id)
        merchnat_business_category = business_category.objects.all()

    if request.method == "POST":
        print('ID',id)
        form = MerchnatgeneralSettingForm(request.POST, request.FILES)
        merchantBusinessesList = MerchantProfile.objects.get(id=id)
        print(form.errors)

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

            print('aa',merchantBusinessesList.m_user)
            
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

            return HttpResponseRedirect('/edit-merchant-of-software-partner/'+str(id)+'/')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!', timer=1000)
            return HttpResponseRedirect('/edit-merchant-of-software-partner/'+str(id)+'/')
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
            'merchant_objects_id': merchant_objects_id,
            'merchant_b_id': id,
            'partnerNavActiveClass': "active",
            'PartnerInfoCollapseShow': "show",
            'PartnerSoftwareNavClass': "active",
            'merchant_general_setting': merchant_general_setting, 
            'merchnat_business_category': merchnat_business_category, 
        }
        return render(request, "super_admin/edit-all-details-of-software-partner.html", context)



    
@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def viewMerchantDetails_partner(request, id=None):
    if request.method == "GET":
        merchantBusinessesList = MerchantProfile.objects.get(id=id)
        merchant_objects_id = GreenBillUser.objects.get(mobile_no = merchantBusinessesList.m_user)
        form = MerchnatgeneralSettingForm()
        print('list',merchantBusinessesList.m_user)
        print(id)
        merchnat_business_category = business_category.objects.all()

    if request.method == "POST":
        print('ID',id)
        form = MerchnatgeneralSettingForm(request.POST, request.FILES)
        merchantBusinessesList = MerchantProfile.objects.get(id=id)
        print(form.errors)

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
            bank_account_entity_m1 = form.cleaned_data.get("bank_account_entity_m1")
            bank_account_entity_adress2 = form.cleaned_data.get("bank_account_entity_adress2")
            m_website_url = form.cleaned_data.get("m_website_url")
            m_business_name_for_billing = form.cleaned_data.get("m_business_name_for_billing")
            m_billing_address = form.cleaned_data.get("m_billing_address")
            m_billing_email = form.cleaned_data.get("m_billing_email")
            m_billing_phone = form.cleaned_data.get("m_billing_phone")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")

            business_category_object = business_category.objects.get(id=business_category_temp)
            result = GreenBillUser.objects.filter(mobile_no = merchantBusinessesList.m_user).update(first_name = first_name, last_name = last_name)

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
                UserProfileImage.objects.update_or_create(user_id = merchantBusinessesList.m_user.id, defaults={ "m_profile_image" : profile_image })
            
            if GSTIN_certificate:
                MerchantProfile.objects.update_or_create(id = merchantBusinessesList.m_user.id, defaults={ "m_GSTIN_certificate" : GSTIN_certificate })

            if CIN_certificate:
                MerchantProfile.objects.update_or_create(id = merchantBusinessesList.m_user.id, defaults={ "m_CIN_certificate" : CIN_certificate })
            
            if business_logo:
                MerchantProfile.objects.update_or_create(id = merchantBusinessesList.m_user.id, defaults={ "m_business_logo" : business_logo })

            if business_stamp:
                MerchantProfile.objects.update_or_create(id = merchantBusinessesList.m_user.id, defaults={ "m_business_stamp" : business_stamp })

            if digital_signature:
                MerchantProfile.objects.update_or_create(id = merchantBusinessesList.m_user.id, defaults={ "m_digital_signature" : digital_signature })

            if cancel_bank_cheque_photo:
                MerchantProfile.objects.update_or_create(id = merchantBusinessesList.m_user.id, defaults={ "m_cancel_bank_cheque_photo" : cancel_bank_cheque_photo })

            if udyog_adhar_certificate_file:
                MerchantProfile.objects.update_or_create(id = merchantBusinessesList.m_user.id, defaults={ "m_other_document_certificate1" : udyog_adhar_certificate_file })
            
            if address_proof:
                MerchantProfile.objects.update_or_create(id = merchantBusinessesList.m_user.id, defaults={ "address_proof" : address_proof })

            if m_bank_account_entry:
                MerchantProfile.objects.update_or_create(id = merchantBusinessesList.m_user.id, defaults={ "m_bank_account_entry" : m_bank_account_entry })

            if m_address_bank_account:
                MerchantProfile.objects.update_or_create(id = merchantBusinessesList.m_user.id, defaults={ "m_address_bank_account" : m_address_bank_account })

            if schedule_pdf_upload:
                MerchantProfile.objects.update_or_create(id = merchantBusinessesList.m_user.id, defaults={ "schedule_pdf_upload" : schedule_pdf_upload })
            
            sweetify.success(request, title="Success", icon='success',
                             text='Merchant records updated Successfully !!!', timer=1000)

            return HttpResponseRedirect('/view-merchant-info-all-records/'+str(id)+'/')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!', timer=1000)
            return HttpResponseRedirect('/view-merchant-info-all-records/'+str(id)+'/')
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
            'merchant_objects_id': merchant_objects_id,
            'States': States,
            'form': form1,
            'merchant_id': id,
            'partnerMerchantNavclass': "active", 
            'partnerMerchantInfoNavcollclass': "show",
            'partnerMerchantInfoNavclass': "active",
            'merchant_general_setting': merchant_general_setting, 
            'merchnat_business_category': merchnat_business_category, 
        }
        return render(request, "partner/edit-records-of-merchant-by-partner.html", context)

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def Merchant_info_list(request):
    # partner = PartnerProfile.objects.get(p_user=request.user).p_category
    
    # # Software Partner
    # if partner == "Software Partner":

    #     par_user_id = Partner_users.objects.get(user_id=request.user)

    #     partner_object = par_user_id.partner_user_id
    #     # data = MerchantDisablereasons.objects.all()
    #     print(partner_object)
    #     if request.method == "GET":
    #         customer_object1 = GreenBillUser.objects.get(mobile_no = partner_object)

    #         merchantBusinessesList = MerchantProfile.objects.filter(merchant_by_partner=customer_object1).order_by('-id')
    #         merchantBusinessesListcount = MerchantProfile.objects.filter(merchant_by_partner=customer_object1).count()
    #         qs = business_category.objects.all().order_by('business_category_name')
        
    #         form = MerchantSignUpForm(request.POST)
    #         form1 = MerchantSignUpOtherDetailsForm(request.POST)
        
    #         # To get only unique values
    #         merchantList = MerchantProfile.objects.all().distinct().order_by('-id')
    #         data = MerchantDisablereasons.objects.all()
    #         # To avoid duplicates entries by m_user
    #         newMerchantList = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_user_id__isnull = False,m_disabled_account=False ).exclude(id__in=Subquery(merchantList.values('m_user_id')[1:]))
    #         total_merchant_count = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_user_id__isnull=False,m_disabled_account=False).exclude(id__in=Subquery(merchantList.values('m_user_id')[1:])).count()
        
    #         for merchant in newMerchantList:
    #             merchant_object = GreenBillUser.objects.get(mobile_no = merchant.m_user)
    #             merchant.date_joined = merchant_object.date_joined

    #     context = {
    #         'merchant_list': merchantBusinessesList,
    #         'merchantBusinessesListcount': merchantBusinessesListcount,
    #         'merchantNavActiveClass': "active", 
    #         'MerchantInfoCollapseShow': "show",
    #         'MerchantListNavclass': "active",
    #         'form': form, 'form1': form1, 
    #         'business_category_list' : qs,
    #         "total_merchant": total_merchant_count,
    #         "data" : data,
    #         'bulkMailSmsMerchantForm':bulkMailSmsMerchantForm
    #     }

    #     return render(request, "partner/merchan-info-list.html", context)
    # else:
    par_user_id = Partner_users.objects.get(user_id=request.user)

    partnercategoryobject = PartnerProfile.objects.get(p_user=request.user).p_category

    partner_object = par_user_id.partner_user_id
    # data = MerchantDisablereasons.objects.all()
    # print(partner_object)
    if request.method == "GET":
        customer_object1 = GreenBillUser.objects.get(mobile_no = partner_object)

        merchantBusinessesList = MerchantProfile.objects.filter(merchant_by_partner=customer_object1).order_by('-id')
        merchantBusinessesListcount = MerchantProfile.objects.filter(merchant_by_partner=customer_object1).count()
        qs = business_category.objects.all().order_by('business_category_name')
    
        form = MerchantSignUpForm(request.POST)
        form1 = MerchantSignUpOtherDetailsForm(request.POST)
        States = StateCityData.objects.values('state').distinct().order_by('state')

        # To get only unique values
        merchantList = MerchantProfile.objects.all().distinct().order_by('-id')
        data = MerchantDisablereasons.objects.all()
        # To avoid duplicates entries by m_user
        newMerchantList = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_user_id__isnull = False,m_disabled_account=False ).exclude(id__in=Subquery(merchantList.values('m_user_id')[1:]))
        total_merchant_count = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_user_id__isnull=False,m_disabled_account=False).exclude(id__in=Subquery(merchantList.values('m_user_id')[1:])).count()
    
        for merchant in newMerchantList:
            merchant_object = GreenBillUser.objects.get(mobile_no = merchant.m_user)
            merchant.date_joined = merchant_object.date_joined



        context = {'merchant_list': merchantBusinessesList,
            'merchantBusinessesListcount': merchantBusinessesListcount,
            'partnerMerchantNavclass': "active", 
            'partnerMerchantInfoNavcollclass': "show",
            'partnerMerchantInfoNavclass': "active",
            'form': form, 'form1': form1, 
            'States': States,
            'business_category_list' : qs,
            "partnercategoryobject": partnercategoryobject,
            "total_merchant": total_merchant_count,
            "data" : data,
            'bulkMailSmsMerchantForm':bulkMailSmsMerchantForm}

        return render(request, "partner/merchan-info-list.html", context)
    else: 

        return JsonResponse({'success': False})

# change merchantby partner 

def merchantChangeByOwner(request):
    partner_type = request.POST['m_partner_type']
    merchant_mobile_no = request.POST['value']
    partner_business_name = request.POST['m_partner']
    # print("In function to change !!!!!!!!!!!!")
    # print(partner_type,merchant_mobile_no,partner_business_name)
    # print("*********************************")

    greebill_user_id_merchant = GreenBillUser.objects.get(mobile_no = merchant_mobile_no)
    # print(greebill_user_id)

    partner_id = PartnerProfile.objects.get(p_business_name = partner_business_name)
    # print(partner_id)
    
    merchant_list = MerchantProfile.objects.filter(m_user=greebill_user_id_merchant)
    # print(merchant)
    # print(merchant_list[0].merchant_by_partner)


    # assiging greenbill instance to object field
    greenbill_user_id_partner =  GreenBillUser.objects.get(mobile_no= partner_id.p_user)
    # print("$$$$$$$$$$$$$$$$$$$")

    # print(greenbill_user_id_partner)
    # print(merchant_list)


    merchant_list[0].merchant_by_partner= greenbill_user_id_partner 

    print("Printing list !!!!!!!!!")
    for merchant in merchant_list :
        merchant.merchant_by_partner = greenbill_user_id_partner
        merchant.save()
        # print(merchant.merchant_by_partner)
        # print(merchant.m_pin_code)
        # print("____________________________")
    return redirect(merchant_info)
    # return JsonResponse({"msg":"Success data loading !!!"})

# get partener by type 

def GetpartnersbyType(request):
    print("In link")
    type_of_partner = request.POST['type']
    list1 = []
    print("Every thing got")
    print(type_of_partner)
    if type_of_partner == 'Software Partner':
        partner = "Marketing Partner"
    else:
        partner ='Software Partner'

        

    filtered_partner_list = []

    user_state = PartnerProfile.objects.filter(p_category = partner)


    for partner in user_state:
        list1.append({
            "partner": partner.p_business_name
        })
        
    for x in list1:
        if x['partner'] not in filtered_partner_list:
            if x['partner'] != '':
                filtered_partner_list.append(x['partner'])

    filtered_partner_list.sort()
    print("Sorted list         !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    return JsonResponse({"data":filtered_partner_list})


def GetCitiesByState(request):

    state = request.POST['state']

    list1 = []

    filtered_city_list = []

    user_state = StateCityData.objects.filter(state = state)

    for city in user_state:
        list1.append({
            "c_city": city.city
        })
        
    for x in list1:
        if x['c_city'] not in filtered_city_list:
            if x['c_city'] != '':
                filtered_city_list.append(x['c_city'])

    filtered_city_list.sort()

    return JsonResponse({"data":filtered_city_list})


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def Edit_Cust_info(request):

    if request.method == "POST":
        id = request.POST['mid']
        cust_form = Edit_Customer_Info_Form(request.POST)
        cust_first_name = request.POST['edit_fname']
        cust_last_lname = request.POST['edit_lname']
        cust_email = request.POST['edit_email']
        customer_area = request.POST['edit_area']
        customer_pin_code = request.POST['edit_pin_code'] 
        if request.POST['cust_record_id'] != "":
            user = Customer_Info_Model.objects.filter(id=id).update(
                cust_first_name=cust_first_name,
                cust_last_lname=cust_last_lname,
                cust_email=cust_email,
                customer_area=customer_area,
                customer_pin_code=customer_pin_code,
            )
            sweetify.success(request, title="Success", icon='success',
                             text='Customer Updated Successfully.', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error',
                           text='Customer Upadte Failed', timer=1500)
    return redirect(Merchant_info_list)
    

def Delete_customer_record(request, id):
    cust = Customer_Info_Model.objects.get(id=id).delete()
    if cust:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": False})


def Check_Contact_number(request, id):
    mobile_no = id
    per_user_id = Partner_users.objects.get(user_id=request.user)

    try:
        mob_num1 = GreenBillUser.objects.get(mobile_no=mobile_no)
    except:
        mob_num1 = ""
        
    if mob_num1:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def customer_info_by_mobile_no(request, mobile_no):
    
    user_id = request.user

    partner_users = Partner_users.objects.get(user_id = user_id)

    partner_business_object = PartnerProfile.objects.get(p_user = partner_users.partner_user_id.id, p_active_account = True)

    partner_business_id = partner_business_object.id

    customer_bill_list = CustomerBill.objects.filter(partner_business_name=partner_business_object)

    data = []

    base_url = "http://157.230.228.250/"

    try:
        customer_object = GreenBillUser.objects.get(mobile_no = mobile_no)

        personal_details = {
                'mobile_no' : customer_object.mobile_no,
                'first_name' : customer_object.first_name,
                'last_name' : customer_object.last_name,
                'email': customer_object.email,
        }

    except:

        try:

            customer_object = Customer_Info_Model.objects.get(cust_mobile_num = mobile_no)

            personal_details = {
                    'mobile_no' : customer_object.cust_mobile_num,
                    'first_name' : customer_object.cust_first_name,
                    'last_name' : customer_object.cust_last_lname,
                    'email': customer_object.cust_email
            }

        except:

            personal_details = {
                'mobile_no' : mobile_no,
                'first_name' : '',
                'last_name' : '',
                'email': ''
            }


    customer_bill_list = CustomerBill.objects.filter(partner_business_name=partner_business_object)

    for bill in customer_bill_list:
        if mobile_no == bill.mobile_no.mobile_no:
            try:
                bill_file = str(base_url) + str(bill.bill.url)
            except:
                bill_file = ""
            data.append({
                'bill_id': bill.id,
                'mobile_no': mobile_no,
                'amount': str(bill.bill_amount),
                'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "CustomerBill",
                'customer_added': bill.customer_added
            })
            

    parking_bill_list = SaveParkingLotBill.objects.filter(p_business_id = partner_business_id)
    for bill in parking_bill_list:
        if mobile_no == bill.mobile_no:
            try:
                bill_file = str(base_url) + str(bill.bill_file.url)
            except:
                bill_file = ""
            data.append({
                'bill_id': bill.id,
                'mobile_no': mobile_no,
                'amount': str(bill.amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SaveParkingLotBill",
                'customer_added': False
            })
            
    petrol_bill_list = SavePetrolPumpBill.objects.filter(p_business_id = partner_business_id)
    for bill in petrol_bill_list:
        if mobile_no == bill.mobile_no:
            try:
                bill_file = str(base_url) + str(bill.bill_file.url)
            except:
                bill_file = ""
            data.append({
                'bill_id': bill.id,
                'mobile_no': mobile_no,
                'amount': str(bill.total_amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SavePetrolPumpBill",
                'customer_added': False
            })
            
    # sorted_data = sorted(data, key=data.bill_date)

    data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

 

    context = {
        "personal_details" : personal_details,
        "bills" : data,
        'CustomerInfoNavClass': 'active',
    }
    return render(request, "partner/customer_info_by_mobile_no.html", context)


'''@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def addMerchantBypartner(request):
   
    print('entry point')
    if request.method == "POST":
        print('hello323')
        par_user_id = Partner_users.objects.get(user_id=request.user)

        partner_object = par_user_id.partner_user_id

        mobile_no = request.POST['mobile_no']

        try:
            print('----------')
            user_object = GreenBillUser.objects.filter(mobile_no = mobile_no)
            print('878641')
            # is_customer = user_object[0].is_customer
            print(')))')

        except:
            is_customer = ''
            user_object = ''

            print('1111')
        if user_object:
            if user_object[0].is_staff:
                msg = 'Mobile number is already registered as Owner or Owner Staff. So please Use Owner Web Panel.'
                print('~~~~~~~~~~~')
                return JsonResponse({'status':'fail', 'msg': msg})
            
            elif user_object[0].is_partner:
                msg = 'Mobile number is already registered as Partner. So please Use Partner Web Panel.'
                print('888888888888888')
                return JsonResponse({'status':'fail', 'msg': msg})

            elif (user_object[0].is_merchant or user_object[0].is_merchant_staff):
                msg = 'Mobile number is already registered as Merchant or Merchant user. So please Use Merchant Web Panel.'
                print('!!!!!!!!!111')
                return JsonResponse({'status':'fail', 'msg': msg})
            elif user_object[0].is_customer:
                # m_email = request.POST['m_email']
                # m_business_name = request.POST['m_business_name']
                # m_business_category = request.POST['m_business_category']
                # m_pin_code = request.POST['m_pin_code']
                # m_city = request.POST['m_city']
                # m_area = request.POST['m_area']
                # m_state = request.POST['m_state']
                # m_district = request.POST['m_district']
                # temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
                msg = 'Mobile number is already Used. Please try with other mobile number.'
                print('----------------------')
                return JsonResponse({'status':'fail', 'msg': msg})

            # else:
            #     msg = 'Mobile number is already Used. Please try with other mobile number.'
              #     return JsonResponse({'status':'fail', 'msg': msg})


        form = MerchantSignUpForm1(request.POST)
        form1 = MerchantSignUpOtherDetailsForm(request.POST)
        print('form valid or not')
        if form.is_valid() and form1.is_valid():
            print('valid')
            mobile_no = form.cleaned_data.get("mobile_no")
            is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no)
            print('form')
            if is_merchant:
                return JsonResponse({'status':'error', 'msg': "Merchant with this number is already exists."})
            else:
                print(']]]]]')

                temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

                user_id = GreenBillUser.objects.create_user(
                    mobile_no = mobile_no,
                    m_email = form.cleaned_data.get('m_email'),
                    password = temp_password,
                )

                try:
                    last_unique_id = MerchantUniqueIds.objects.all().last()
                    print('))))))))')
                except:
                    print('+=====')
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

                letters = string.ascii_letters
                digit = string.digits

                random_string = str(user_id.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
            
                GreenBillUser.objects.filter(mobile_no = user_id).update(is_merchant = 1, is_merchant_staff = 1, merchant_referral_code = random_string)
                
                Merchant_users.objects.create(user_id = user_id, merchant_user_id = user_id)
                merchant_by_partner = "By Partner"
                m_email = form1.cleaned_data.get("m_email")
                m_business_name = form1.cleaned_data.get("m_business_name")
                m_business_category = form1.cleaned_data.get("m_business_category")
                # m_city = form1.cleaned_data.get("m_city")
                # m_district = form1.cleaned_data.get("m_district")
                # m_state = form1.cleaned_data.get("m_state")
                m_pin_code = form1.cleaned_data.get("m_pin_code")
                # m_area = form1.cleaned_data.get("m_area")
                cust_city = form1.cleaned_data.get("m_city")
                m_city = cust_city.capitalize()

                cust_district = form1.cleaned_data.get("m_district")
                m_district = cust_district.capitalize()

                cust_state = form1.cleaned_data.get("m_state")
                m_state = cust_state.capitalize()

                cust_area = form1.cleaned_data.get("m_area")
                m_area = cust_area.capitalize()

                MerchantProfile.objects.create(m_user = user_id, m_business_name = m_business_name, by_partner =  merchant_by_partner, merchant_by_partner = par_user_id.partner_user_id,
                    m_business_category = m_business_category, m_city = m_city, m_district = m_district,
                    m_state = m_state, m_pin_code = m_pin_code, m_area= m_area,  m_disabled_account = False, m_latest_account=True, status=1, m_active_account = 1, m_unique_id=m_unique_id)

                mobile_no = form.cleaned_data.get("mobile_no")
                email = form.cleaned_data.get('m_email')
                raw_password = temp_password
                user = authenticate(mobile_no=mobile_no, password=raw_password)

                subject = 'Thank You For Registration.'
                message = f' Dear Valued Merchant, \n Warm Greetings from Green Bill Team!!! \n We are glad to see you chose Green Bill as {m_business_category} and below are your login credentials for the same \n URL: http://157.230.228.250/merchant-login/ \n Username: {mobile_no} \n Password: {raw_password} \n You are advised to login and complete your profile and business details for better coordination.'
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [user_id.m_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()
                
                # if res.status_code == 200:
                print('###############')
                return JsonResponse({'status':'success', 'msg': 'Merchant Added Successfully !!!.'})
                # else:
                #     return JsonResponse({'status':'error', 'msg': "Failed to add merchant."})
        # else:
            # print("set1")
        #     return JsonResponse({'status':'error', 'msg': "User already Exists."})
        #     # return JsonResponse({'status':'success', 'msg': 'Merchant Added Successfully !!!.'})
    else:
        print("set2")
        print('2222222')
        return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})'''










@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def addMerchantBypartner(request):
    # print(request.POST)
    # sys.exit()
    print('helllo')
    if request.method == "POST":
        par_user_id = Partner_users.objects.get(user_id=request.user)

        partner_object = par_user_id.partner_user_id

        mobile_no = request.POST['mobile_no']

        try:
            user_object = GreenBillUser.objects.filter(mobile_no = mobile_no)
            is_customer = user_object[0].is_customer

        except:
            is_customer = ''
            user_object = ''
        if user_object:
            if user_object[0].is_staff:
                msg = 'Mobile number is already registered as Owner or Owner Staff. So please Use Owner Web Panel.'
                return JsonResponse({'status':'fail', 'msg': msg})
            
            elif user_object[0].is_partner:
                msg = 'Mobile number is already registered as Partner. So please Use Partner Web Panel.'
                return JsonResponse({'status':'fail', 'msg': msg})

            elif (user_object[0].is_merchant or user_object[0].is_merchant_staff):
                msg = 'Mobile number is already registered as Merchant or Merchant user. So please Use Merchant Web Panel.'
                return JsonResponse({'status':'fail', 'msg': msg})
            elif user_object[0].is_customer:
                # m_email = request.POST['m_email']
                # m_business_name = request.POST['m_business_name']
                # m_business_category = request.POST['m_business_category']
                # m_pin_code = request.POST['m_pin_code']
                # m_city = request.POST['m_city']
                # m_area = request.POST['m_area']
                # m_state = request.POST['m_state']
                # m_district = request.POST['m_district']
                # temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
                msg = 'Mobile number is already Used. Please try with other mobile number.'
                return JsonResponse({'status':'fail', 'msg': msg})

            # else:
            #     msg = 'Mobile number is already Used. Please try with other mobile number.'
            #     return JsonResponse({'status':'fail', 'msg': msg})
        form = MerchantSignUpForm1(request.POST)

        form1 = MerchantSignUpOtherDetailsForm(request.POST)
        if form.is_valid() and form1.is_valid():
            mobile_no = form.cleaned_data.get("mobile_no")
            is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no)
            
            if is_merchant:
                return JsonResponse({'status':'error', 'msg': "Merchant with this number is already exists."})
            else:

                temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

                user_id = GreenBillUser.objects.create_user(
                    mobile_no = mobile_no,
                    m_email = form.cleaned_data.get('m_email'),
                    password = temp_password,
                )

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

                letters = string.ascii_letters
                digit = string.digits

                random_string = str(user_id.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
            
                GreenBillUser.objects.filter(mobile_no = user_id).update(is_merchant = 1, is_merchant_staff = 1, merchant_referral_code = random_string)
                
                Merchant_users.objects.create(user_id = user_id, merchant_user_id = user_id)
                merchant_by_partner = "By Partner"
                m_email = form1.cleaned_data.get("m_email")
                m_business_name = form1.cleaned_data.get("m_business_name")
                m_business_category = form1.cleaned_data.get("m_business_category")
                # m_city = form1.cleaned_data.get("m_city")
                # m_district = form1.cleaned_data.get("m_district")
                # m_state = form1.cleaned_data.get("m_state")
                m_pin_code = form1.cleaned_data.get("m_pin_code")
                # m_area = form1.cleaned_data.get("m_area")
                cust_city = form1.cleaned_data.get("m_city")
                m_city = cust_city.capitalize()

                cust_district = form1.cleaned_data.get("m_district")
                m_district = cust_district.capitalize()

                cust_state = form1.cleaned_data.get("m_state")
                m_state = cust_state.capitalize()

                cust_area = form1.cleaned_data.get("m_area")
                m_area = cust_area.capitalize()

                MerchantProfile.objects.create(m_user = user_id, m_business_name = m_business_name, by_partner =  merchant_by_partner, merchant_by_partner = par_user_id.partner_user_id,
                    m_business_category = m_business_category, m_city = m_city, m_district = m_district,
                    m_state = m_state, m_pin_code = m_pin_code, m_area= m_area,  m_disabled_account = False, m_latest_account=True, status=1, m_active_account = 1, m_unique_id=m_unique_id)

                mobile_no = form.cleaned_data.get("mobile_no")
                email = form.cleaned_data.get('m_email')
                raw_password = temp_password
                user = authenticate(mobile_no=mobile_no, password=raw_password)

                subject = 'Thank You For Registration.'
                message = f' Dear Valued Merchant, \n Warm Greetings from Green Bill Team!!! \n We are glad to see you chose Green Bill as {m_business_category} and below are your login credentials for the same \n URL: http://157.230.228.250/merchant-login/ \n Username: {mobile_no} \n Password: {raw_password} \n You are advised to login and complete your profile and business details for better coordination.'
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [user_id.m_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()
                
                # if res.status_code == 200:
                return JsonResponse({'status':'success', 'msg': 'Merchant Added Successfully !!!.'})
                # else:
                #     return JsonResponse({'status':'error', 'msg': "Failed to add merchant."})
        # else:
        #     # print("set1")
        #     return JsonResponse({'status':'error', 'msg': "User already Exists."})
        #     # return JsonResponse({'status':'success', 'msg': 'Merchant Added Successfully !!!.'})
    else:
        print("set2")
        return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})











@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def view_partner_record(request, id):
    if request.method == "GET":

        partnerList = PartnerProfile.objects.get(p_user=id)

        par_mob_no = partnerList.p_user

        commision_per_merchant = partnerList.merchant_commission

        commision_per_merchant_bill = partnerList.p_commission_per_bill

        check_category = partnerList.p_category

        customer_id = partnerList.p_user

        merchnat_business_category = business_category.objects.all()

        total_comission_till_now = 0

        bill_comission_till_now = 0

        comission_counter = 0

        overall_commision = 0

        if check_category == "Software Partner":

            given_date = datetime.today().date()
 
            first_day_of_month = given_date.strftime("%Y-%m-01")
            
            data = MerchantDisablereasons.objects.all()

            customer_object1 = GreenBillUser.objects.get(mobile_no = customer_id)

            merchantBusinessesList = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_disabled_account=False).order_by('-id')

            merchantBusinessesListcount = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_disabled_account=False).count()

            bill_monthly_commision = 0

            partner_month_comission = 0

            for merchant in merchantBusinessesList:

                merchant_profile_id = MerchantProfile.objects.get(id=merchant.id)

                user_id = GreenBillUser.objects.get(mobile_no = merchant.m_user) 

                merchant.m_number = user_id

                start_date=timezone.localtime(merchant.date_joined).strftime("%Y-%m-%d")

                customer_bill1 = CustomerBill.objects.filter(business_name = merchant_profile_id, customer_added = False)

                merchant_bill1 = MerchantBill.objects.filter(business_name = merchant_profile_id)

                parking_bill_list1 = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile_id, is_pass = False)

                petrol_bill_list1 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile_id)

                if customer_bill1:
                    for bill in customer_bill1:
                        bill_start_date1=timezone.localtime(bill.created_at).strftime("%Y-%m-%d")

                        if first_day_of_month <= bill_start_date1:
                            bill_monthly_commision = bill_monthly_commision + 1

                if merchant_bill1:
                    for bill in merchant_bill1:
                        bill_start_date2=timezone.localtime(bill.created_at).strftime("%Y-%m-%d")

                        if first_day_of_month <= bill_start_date2:
                            bill_monthly_commision = bill_monthly_commision + 1

                if parking_bill_list1:
                    for bill in parking_bill_list1:
                        bill_start_date3=timezone.localtime(bill.created_at).strftime("%Y-%m-%d")

                        if first_day_of_month <= bill_start_date3:
                            bill_monthly_commision = bill_monthly_commision + 1

                if petrol_bill_list1:
                    for bill in petrol_bill_list1:
                        bill_start_date4=timezone.localtime(bill.created_at).strftime("%Y-%m-%d")

                        if first_day_of_month <= bill_start_date4:
                            bill_monthly_commision = bill_monthly_commision + 1

                total_bills = 0

                customer_bill = CustomerBill.objects.filter(business_name = merchant_profile_id, customer_added = False).count()

                merchant_bill = MerchantBill.objects.filter(business_name = merchant_profile_id).count()

                parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile_id, is_pass = False).count()

                petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile_id).count()

                total_bills = int(customer_bill) + int(merchant_bill) + int(parking_bill_list) + int(petrol_bill_list)

                par_comission = int(customer_bill) + int(merchant_bill) + int(parking_bill_list) + int(petrol_bill_list)

                commision_per_merchant_bill = partnerList.p_commission_per_bill
                try:
                    bills_comission = float(total_bills) * float(commision_per_merchant_bill)
                except:
                    bills_comission = 0
                merchant.total_comission = bills_comission

                if par_comission != 0:
                    overall_commision = float(par_comission) * float(commision_per_merchant_bill) + float(overall_commision)
            try:
                partner_month_comission = float(bill_monthly_commision) * float(commision_per_merchant_bill)
            except:
                partner_month_comission = 0
            p_monthlyModel = PartnerMonthlyCommision.objects.filter(p_mobile_no = par_mob_no, month = given_date.month, year = given_date.year)

            try:
                if p_monthlyModel:

                    current_month_amount = p_monthlyModel[0].amount

                    if float(partner_month_comission) != float(current_month_amount):

                        p_monthlyModel = PartnerMonthlyCommision.objects.filter(p_mobile_no = par_mob_no, month = given_date.month, year = given_date.year).update(amount = partner_month_comission)

                else:
                    p_monthlyModel = PartnerMonthlyCommision.objects.create(p_mobile_no = par_mob_no, month = given_date.month, amount = partner_month_comission, year = given_date.year)

            except:
                pass

            context = {
                'partner_month_comission': partner_month_comission,
                'overall_commision': overall_commision,
                'data' : data,
                'par_mob_no': id,
                'merchantBusinessesListcount' : merchantBusinessesListcount,
                'merchantBusinessesList' : merchantBusinessesList,
                'merchantBusinessCategory' : merchnat_business_category,
                'customer_id' : id,
                'partnerNavActiveClass': "active",
                'PartnerInfoCollapseShow': "show",
                'PartnerSoftwareNavClass': "active",
            }
            
            return render(request, "super_admin/view-all-partner-records.html", context) 
            # return render(request, "super_admin/view-all-merchant-by-partner.html", context)   
        else:
            merchant_monthly_commision = 0

            bill_monthly_commision = 0

            partner_month_comission = 0

            overall_bills_commision = 0

            monthly_per_sms_bills = 0

            monthly_per_digital_bills = 0

            per_sms_bills = 0

            per_digital_bills = 0

            total_of_total= 0

            given_date = datetime.today().date()
 
            first_day_of_month = given_date.strftime("%Y-%m-01")

            data = MerchantDisablereasons.objects.all()



            customer_object1 = GreenBillUser.objects.get(mobile_no = customer_id)

            merchantBusinessesList = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_disabled_account=False).order_by('-id')

            merchantBusinessesListcount = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_disabled_account=False).count()

            # print('merchantBusinessesListcount',merchantBusinessesListcount)
            partner_month_comission = 0

            vyas_yes = False

            for merchant in merchantBusinessesList:
                print(merchant)



                start_date=timezone.localtime(merchant.date_joined).strftime("%Y-%m-%d")

                merchant_profile_id = MerchantProfile.objects.get(id=merchant.id)

                user_id = GreenBillUser.objects.get(mobile_no = merchant.m_user) 

                print("*******")
                print(type(user_id.mobile_no))
                print(type(merchant.m_user))
            
                if user_id.mobile_no == "7020598727":
                    print("shsbdhdy377488484")

                    vyas_yes = True

                merchant_subscriptions_till_now = merchant_subscriptions.objects.filter(merchant_id= user_id).count()
                merchant_subscriptions_till_now_object =merchant_subscriptions.objects.filter(merchant_id= user_id)
                print("**************imp********************")
                print(merchant_subscriptions_till_now)

               
                
                if first_day_of_month <= start_date:

                    merchant_monthly_commision = merchant_monthly_commision + 1
                   
                merchant_profile_id = MerchantProfile.objects.get(id=merchant.id)

                user_id = GreenBillUser.objects.get(mobile_no = merchant.m_user) 

                merchant.m_number = user_id

                customer_bill = CustomerBill.objects.filter(business_name = merchant_profile_id, customer_added = False).count()

                merchant_bill = MerchantBill.objects.filter(business_name = merchant_profile_id).count()

                parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile_id, is_pass = False).count()

                petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile_id).count()

                customer_bill1 = CustomerBill.objects.filter(business_name = merchant_profile_id, customer_added = False)

                merchant_bill1 = MerchantBill.objects.filter(business_name = merchant_profile_id)

                parking_bill_list1 = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile_id, is_pass = False)

                petrol_bill_list1 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile_id)


                if customer_bill1:
                    for bill in customer_bill1:
                        if bill.greenbill_digital_bill == "True":
                            per_digital_bills = per_digital_bills + 1

                        if bill.greenbill_sms_bill == "True":
                            per_sms_bills = per_sms_bills + 1

                        bill_start_date1=timezone.localtime(bill.created_at).strftime("%Y-%m-%d")

                        if first_day_of_month <= bill_start_date1:
                            if bill.greenbill_digital_bill == "True":
                                monthly_per_digital_bills = monthly_per_digital_bills + 1

                            if bill.greenbill_sms_bill == "True":
                                monthly_per_sms_bills = monthly_per_sms_bills + 1

                if merchant_bill1:
                    for bill in merchant_bill1:
                        if bill.greenbill_digital_bill == "True":
                            per_digital_bills = per_digital_bills + 1

                        if bill.greenbill_sms_bill == "True":
                            per_sms_bills = per_sms_bills + 1

                        bill_start_date2=timezone.localtime(bill.created_at).strftime("%Y-%m-%d")

                        if first_day_of_month <= bill_start_date2:
                            if bill.greenbill_digital_bill == "True":
                                monthly_per_digital_bills = monthly_per_digital_bills + 1

                            if bill.greenbill_sms_bill == "True":
                                monthly_per_sms_bills = monthly_per_sms_bills + 1

                if parking_bill_list1:
                    for bill in parking_bill_list1:
                        if bill.greenbill_digital_bill == "True":
                            per_digital_bills = per_digital_bills + 1

                        if bill.greenbill_sms_bill == "True":
                            per_sms_bills = per_sms_bills + 1

                        bill_start_date3=timezone.localtime(bill.created_at).strftime("%Y-%m-%d")

                        if first_day_of_month <= bill_start_date3:
                            if bill.greenbill_digital_bill == "True":
                                monthly_per_digital_bills = monthly_per_digital_bills + 1

                            if bill.greenbill_sms_bill == "True":
                                monthly_per_sms_bills = monthly_per_sms_bills + 1

                if petrol_bill_list1:
                    for bill in petrol_bill_list1:
                        if bill.greenbill_digital_bill == "True":
                            per_digital_bills = per_digital_bills + 1

                        if bill.greenbill_sms_bill == "True":
                            per_sms_bills = per_sms_bills + 1

                        bill_start_date4=timezone.localtime(bill.created_at).strftime("%Y-%m-%d")

                        if first_day_of_month <= bill_start_date4:
                            if bill.greenbill_digital_bill == "True":
                                monthly_per_digital_bills = monthly_per_digital_bills + 1

                            if bill.greenbill_sms_bill == "True":
                                monthly_per_sms_bills = monthly_per_sms_bills + 1 

                t=0
                d=0


                try:

                    i = merchant_subscriptions_till_now_object[len(merchant_subscriptions_till_now_object)-1]
                    # for i in merchant_subscriptions_till_now_object:

                    r = subscription_plan_details.objects.get(subscription_name = i.subscription_name)
                    print("P:SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                    print()
                    t = float(i.valid_for_month) * float(i.no_of_users)*float(r.cost_for_users)
                    d = d+(t*float(commision_per_merchant))/100
                    print("*@&@8282882229")
                    print(d)
                except:
                    pass


                total_bills = int(customer_bill) + int(merchant_bill) + int(parking_bill_list) + int(petrol_bill_list)

                par_comission = int(customer_bill) + int(merchant_bill) + int(parking_bill_list) + int(petrol_bill_list)

                commision_per_merchant = partnerList.merchant_commission

                commision_per_sms_bill = partnerList.p_commission_per_sms_bill

                commision_per_digital_bill = partnerList.p_commission_per_digital_bill

                if not partnerList.p_commission_per_bill:
                    commision_per_merchant_bill = 0

                bills_comission = float(total_bills) * float(commision_per_merchant)

                print("*#&#&*#*#")
                print(commision_per_merchant)

                # merchant.total_comission = float(bills_comission) + float(commision_per_merchant)
                

                if par_comission != 0:
                   
                    overall_bills_commision = (float(per_sms_bills) * float(commision_per_sms_bill)) + (float(per_digital_bills) * float(commision_per_digital_bill)) + float(overall_commision)

               
                total_amount_to_cal_inpercent = d
                print("Amount to addd....................")
                print(total_amount_to_cal_inpercent)

                total_of_total = total_amount_to_cal_inpercent+total_of_total

                total_merchant_with_commission =  float(merchantBusinessesListcount) * float(commision_per_merchant) +(float(total_amount_to_cal_inpercent)) 
                overall_commision =  float(overall_bills_commision)+(float(total_of_total)) 

                if vyas_yes:
                    merchant.total_comission = float(total_amount_to_cal_inpercent)+float(overall_bills_commision)- 11.08+0.12
                    overall_commision =  float(overall_bills_commision)+(float(total_of_total)) -11.08+0.12

                else:

                    merchant.total_comission = float(total_amount_to_cal_inpercent)+float(overall_bills_commision)
                    overall_commision =  float(overall_bills_commision)+(float(total_of_total)) 

 

            print("bvvvvvvvvvbbbbbbbbbbbbbbbbbbbbbbbbbb")
            if vyas_yes and given_date.month == 4 and given_date.year == 2022:
                print("innid")
                partner_month_comission = partner_month_comission+(float(total_of_total)) + (float(monthly_per_sms_bills) * float(partnerList.p_commission_per_sms_bill)) + (float(monthly_per_digital_bills) * float(partnerList.p_commission_per_digital_bill))- 1.38+0.12
            else:
                partner_month_comission = partner_month_comission+(float(total_of_total)) + (float(monthly_per_sms_bills) * float(partnerList.p_commission_per_sms_bill)) + (float(monthly_per_digital_bills) * float(partnerList.p_commission_per_digital_bill))
            # partner_month_comission = partner_month_comission+(float(total_of_total)) + (float(monthly_per_sms_bills) * float(partnerList.p_commission_per_sms_bill)) + (float(monthly_per_digital_bills) * float(partnerList.p_commission_per_digital_bill))- 11.08

            print(partner_month_comission)
            # partner_month_comission = partner_month_comission+(float(total_of_total)) + (float(monthly_per_sms_bills) * float(partnerList.p_commission_per_sms_bill)) + (float(monthly_per_digital_bills) * float(partnerList.p_commission_per_digital_bill))

            p_monthlyModel = PartnerMonthlyCommision.objects.filter(p_mobile_no = par_mob_no, month = given_date.month, year = given_date.year)

            try:
                if p_monthlyModel:

                    current_month_amount = p_monthlyModel[0].amount

                    if float(partner_month_comission) != float(current_month_amount):

                        p_monthlyModel = PartnerMonthlyCommision.objects.filter(p_mobile_no = par_mob_no, month = given_date.month, year = given_date.year).update(amount = partner_month_comission)

                else:
                    p_monthlyModel = PartnerMonthlyCommision.objects.create(p_mobile_no = par_mob_no, month = given_date.month, amount = partner_month_comission, year = given_date.year)

            except:
                pass



            context = {
                'partner_month_comission' : partner_month_comission,
                'par_mob_no': id,
                'data' : data,
                'merchantBusinessesListcount' : merchantBusinessesListcount,
                'merchantBusinessesList' : merchantBusinessesList,
                'merchantBusinessCategory' : merchnat_business_category,
                'overall_commision': overall_commision,
                'customer_id' : id,
                'partnerNavActiveClass': "active",
                'PartnerInfoCollapseShow': "show",
                'PartnerListNavclass': "active",
            }
            return render(request, "super_admin/view-all-merchant-by-partner.html", context)                  
    else:
        return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})


def Delete_customer_by_owner(request, id):
    customer = Customer_Info_Model.objects.get(id=id).delete()
    if cust:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": False})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def delete_merchant_by_owner(request, id):
    instance = MerchantProfile.objects.get(id=id)
    
    instance.delete()
    return JsonResponse({'success': True})



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def getAllMerchantBusinessDetailsByOwner(request):
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


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def editMerchantBusinessData_byowner(request):
    if request.method == "POST":
        form = merchantEditBusinessesForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            user_id = request.POST['user_id']
            business_id = request.POST['merchant_setting_id']
            par_id = request.POST['partner_no']
            print(par_id)
            
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
                return redirect('/view-partner-info-record/'+par_id+'/')
                # return JsonResponse({'status':'success', 'msg': "Merchant business information updated sucessfully."})
            else:
                sweetify.error(request, title="error", icon='error', text='Unable to update business information.', timer=1000)
                return redirect('/view-partner-info-record/'+par_id+'/')
                # return JsonResponse({'status':'error', 'msg': "Unable to update business information."})
        else:
            sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
            return redirect('/view-partner-info-record/'+par_id+'/')
            # return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})
    else:
        sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
        return redirect('/view-partner-info-record/'+par_id+'/')
        # return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})





@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def viewMerchantInfo(request, id=None):
    if request.method == "GET":
        merchantBusinessesList = MerchantProfile.objects.filter(m_user=id)
        form = merchantEditBusinessesForm()
        merchnat_business_category = business_category.objects.all()
        context = {
            'merchantBusinessesList' : merchantBusinessesList,
            'merchantBusinessCategory' : merchnat_business_category,
            'form': form,
            'merchantNavActiveClass': "active",
        }
        return render(request, "partner/merchant-info-view.html", context)
    else:
        return JsonResponse({'status':'error', 'msg': "Something went wrong. Please try again later."})


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def getAllMerchantBusinessDetails(request):
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

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def editMerchantBusinessData(request):
    
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

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def deleteMerchantBusiness(request, id):
    instance = MerchantProfile.objects.get(id=id)
    
    instance.delete()
    return JsonResponse({'success': True})












# Create your views here.



@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def BulkEmailPartner(request):


    staff = GreenBillUser.objects.filter(is_merchant=True)

    is_subscription_available = False
    if request.method == "POST":
        if is_subscription_available == True:
            customer_state_value = request.POST.get('customer_state_value')
            customer_state_value_new = customer_state_value.split(",")

            customer_city_value = request.POST.get('customer_city_value')
            customer_city_value_new = customer_city_value.split(",")

            customer_area_value = request.POST.get('customer_area_value')
            customer_area_value_new = customer_area_value.split(",")

            title = request.POST.get('title')
            message = request.POST.get('message')
            smsheader = request.POST.get('smsheader')
            template = request.POST.get('template')
            sent_notice = request.POST.getlist('sentnotice')
            customer = request.POST.get('checksc')
            merchant = request.POST.get('checksm')
            custom_number = request.POST.get('custom-no')
            file_upload = request.FILES.get('myfile')
            joined_lines = ''
            csv_fields = ''
            if file_upload:
                if not file_upload.name.endswith('.csv'):
                    sweetify.error(request, title="Error", icon='error',
                                                    text="Choose valid csv file!!!", timer=5500)
                else:
                    file_data = file_upload.read().decode("utf-8")
                    file_lines = file_data.split("\n")
                    csv_fields = [line.replace('\r','') for line in file_lines if line]

                    converted_list = [str(no) for no in csv_fields]
                    joined_lines = ",".join(converted_list)
            custom_number_list = ''
            if custom_number:
                custom_number_list = custom_number.split(',')

            receiver_name = ''
            if custom_number: 
                receiver_name = custom_number
            if file_upload:
                receiver_name = joined_lines
            if customer:
                receiver_name = 'customer'
            if merchant:
                receiver_name = 'merchant'

            individual_user = request.POST.getlist('individual')

            if customer  and merchant and custom_number_list and csv_fields and individual_user:
                # print('OWNER')
                sweetify.error(request,text="Please select either from group or individual list !!!", timer=5500)
            elif custom_number_list or customer or merchant or csv_fields or individual_user:
           
             
                for notice in sent_notice:

                    if notice == "sms":
                            
                            notice_id = bulkMailSmsPartnerModel.objects.update_or_create(customer_state=customer_state_value_new, customer_city=customer_city_value_new, customer_area=customer_area_value_new, owner_id=request.user, title=title, message=message,receiver=receiver_name, defaults= { 'title':title, 'message':message, 'o_sent_sms':True })

                    elif notice == "sent_mail":
                            
                            notice_id = bulkMailSmsPartnerModel.objects.update_or_create(customer_state=customer_state_value_new, customer_city=customer_city_value_new, customer_area=customer_area_value_new, owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template,receiver=receiver_name, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template, 'o_sent_mail':True })
                                 
                if individual_user:
                    for user in individual_user:
                        u = GreenBillUser.objects.get(id=user)
                        print(u)
                        for notice in sent_notice:
                                
                                if notice == "sms":
                                    contact = u.mobile_no
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
                                                            "OA":"GBPARK",
                                                            "MSISDN": contact, # Recipient's Mobile Number
                                                            "CHANNEL":"SMS",
                                                            "CAMPAIGN_NAME":"hind_user",
                                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                            "USER_NAME":"hind_hsi",
                                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                                            "DLT_CT_ID":"1007161814187973948", # Template Id
                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                        }
                                                    ]
                                                }

                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                        response = requests.post(url, json = data_temp)

                                    sms_response = sendSMS(str(contact), message)
                                    
                                    try:
                                        print('success')
                                            # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                            # message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
                                    except:
                                            owner_notice_sent_save = ""
                                elif notice == "sent_mail":
                                    try:
                                        email_id = u.email
                                        email_from = settings.EMAIL_HOST_USER
                                        recipient_list = [email_id, 'mohini.d@zappkode.com' ]
                                        message = message
                                       
                                        plain_message = strip_tags(message)
                                        send_mail( title, plain_message, email_from, recipient_list)

                                    except:
                                        
                                        owner_notice_sent_save = ""
                                # else:
                                #     # try:
                                #         individual_user_object = GreenBillUser.objects.get(mobile_no=individual_user)
                                #         print('owner_notice_sent_saveowner_notice_sent_save',individual_user)
                                #         owner_notice_sent_save = OwnerSentNotice.objects.create(
                                #         notice_id=notice_object, user_id=individual_user_object, notification=True)

                                #         print('owner_notice_sent_save',owner_notice_sent_save)
                                #     # except:
                                #     #     owner_notice_sent_save = ""

                if csv_fields:
                    for notice in sent_notice:
                        for number in csv_fields:
                            print('number',number)
                            try:
                                email_id = number
                                print(email_id)
                                email_from = settings.EMAIL_HOST_USER
                                print('email from',email_from)
                                recipient_list = [email_id ]
                                # recipient_list = ['shreyash.t@zappkode.com']
                                print('email to',recipient_list)
                                message = message
                               
                                plain_message = strip_tags(message)
                                print('sent message:',plain_message)
                                send_mail( title, plain_message, email_from, recipient_list)
                            except:
                                        
                                owner_notice_sent_save = ""

                if custom_number:
                    for notice in sent_notice:
                        for number in custom_number_list:
                            print('number',number)
                            try:
                                email_id = number
                                print(email_id)
                                email_from = settings.EMAIL_HOST_USER
                                print('email from',email_from)
                                recipient_list = [email_id ]
                                # recipient_list = ['shreyash.t@zappkode.com']
                                print('email to',recipient_list)
                                message = message
                               
                                plain_message = strip_tags(message)
                                print('sent message:',plain_message)
                                send_mail( title, plain_message, email_from, recipient_list)
                            except:
                                        
                                owner_notice_sent_save = ""
                
                
                sweetify.success(request, title="Success", icon='success',
                                    text='Notice Send successfully!', timer=5500)
                    # return redirect("/owner_notice_board/")
            else:
                sweetify.error(request, title="Error", icon='error', text="Something Went Wrong!!!", timer=5500)

        else:
            sweetify.error(request, title="Sorry", icon='error', text="You don't have active email subscription plan!!!", timer=5500)              

    par_user_id = Partner_users.objects.get(user_id=request.user)
    partner_object = par_user_id.partner_user_id
    smsmail = bulkMailSmsPartnerModel.objects.filter(owner_id=partner_object,o_sent_mail=True).order_by('-id')
    states = GreenBillUser.objects.values('c_state').distinct()
    context = {
        'cust_data': states,
        'data': smsmail,
        'merchant_list': staff,
        'PromotionsNavclass': 'active',
         'ShowPromotionsNavclass':'show',
          'BulkEmailNavclass':'active',

        'bulkMailSmsPartnerForm':bulkMailSmsPartnerForm,
    }

    return render(request, 'partner/partner-promotion-email.html' , context)
    





@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/parnter-login/")
def BulkSmsPartner(request):

    bulk_sms_header = smsHeaderModel.objects.filter(request_user=request.user, Active_status = True)
    bulk_sms_template = templateContentModel.objects.filter(request_user=request.user, status='Approved')

    merchant_users_count = MerchantProfile.objects.filter(by_partner = "By Partner").count()
    try:
        smsid = bulkMailSmsPartnerModel.objects.filter().last().id
    except:
        smsid = ''

    staff = GreenBillUser.objects.filter(is_merchant=True)
    customer_addresswise_count = "" 

    partnercategory = PartnerProfile.objects.get(p_user = request.user).p_category

    if request.method == "POST":
        custom_number = ''
        receipent_count = ''
        file_upload = ''
        customer_state_value = request.POST.get('customer_state_value')
        customer_state_value_new = customer_state_value.split(",")

        customer_city_value = request.POST.get('customer_city_value')
        customer_city_value_new = customer_city_value.split(",")

        customer_area_value = request.POST.get('customer_area_value')
        customer_area_value_new = customer_area_value.split(",")

        merchant_state_value = request.POST.get('merchant_state_value')
        merchant_state_value_new = merchant_state_value.split(",")

        merchant_city_value = request.POST.get('merchant_city_value')
        merchant_city_value_new = merchant_city_value.split(",")

        merchant_area_value = request.POST.get('merchant_area_value')
        merchant_area_value_new = merchant_area_value.split(",")
        
        title = request.POST.get('title')
        message = request.POST.get('message')
        smsheader = request.POST.get('smsheader')
        template = request.POST.get('template_id')

        unique_template_id = templateContentModel.objects.get(request_user = request.user, status='Approved', template_content=template).template_id
        
        customer = request.POST.get('checksc')
        merchant = request.POST.get('checksm')
        sent_notice = request.POST.getlist('sentnotice')
        transactional = request.POST.get('transactional')
        user_group = request.POST.getlist('group')
        template_header_id =request.POST.get('template_header_id')
        if partnercategory == 'Software Partner':
            custom_number = request.POST.get('custom-no')
            receipent_count =request.POST.get('receipent_count')
            file_upload = request.FILES.get('myfile')
        else:
            custom_number = request.POST.get('custom-no1')
            receipent_count =request.POST.get('receipent_count')
            file_upload = request.FILES.get('myfile1')
        
        
        joined_lines = ''
        csv_fields = ''
        receipent_count = ''
        if file_upload:
            if not file_upload.name.endswith('.csv'):
                sweetify.error(request, title="Error", icon='error',
                                                text="Choose valid csv file!!!", timer=5500)
            else:
                file_data = file_upload.read().decode("utf-8")
                file_lines = file_data.split("\n")
                csv_fields = [line.replace('\r','') for line in file_lines if line]

                converted_list = [str(no) for no in csv_fields]
                receipent_count = len(converted_list)
                joined_lines = ",".join(converted_list)

                
        custom_number_list = ''
        if custom_number:
            custom_number_list = custom_number.split(',')
            
        
        individual_user = request.POST.getlist('individual')
        
        receiver_name = ''
        if customer: 
            receiver_name = 'customer'
        if merchant:
            receiver_name = 'merchant'
        if custom_number: 
            receiver_name = custom_number
        if file_upload:
            receiver_name = joined_lines 
        
        if customer and custom_number_list and merchant and csv_fields:
            
            sweetify.error(request,text="Please select either from group or individual list !!!", timer=5500)
        elif custom_number_list or customer or merchant or csv_fields:
         
            for notice in sent_notice:
                   
                if notice == "sms":
                    notice_id = bulkMailSmsPartnerModel.objects.update_or_create(customer_state=customer_state_value_new, customer_city=customer_city_value_new, customer_area=customer_area_value_new, owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template, receiver=receiver_name, transactional=transactional, defaults= { 'title':title, 'message':message, 'smsheader':smsheader, 'template':template, 'receiver':receiver_name, 'o_sent_sms':True })
                elif notice == "sent_mail":
                    notice_id = bulkMailSmsPartnerModel.objects.update_or_create(customer_state=customer_state_value_new, customer_city=customer_city_value_new, customer_area=customer_area_value_new, owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template, receiver=receiver_name, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template, 'receiver':receiver_name, 'o_sent_mail':True })
                else:
                    notice_id = Merchant_Notice_Model.objects.update_or_create(owner_id=request.user, notice_title=title, message=message, defaults= { 'notice_title':title,  'message':message, 'o_notification':True })

                    notice_object = Merchant_Notice_Model.objects.get(id= notice_id[0].id)
          
            if transactional == 'transactional':
                par_user_id = Partner_users.objects.get(user_id=request.user)
                partner_object = par_user_id.partner_user_id
                partner_business_object = PartnerProfile.objects.get(p_user = partner_object, p_active_account = True)
                per_id=par_user_id.partner_user_id

                subscription_object = getPartnerActiveTransactionalSubscriptionPlan(request, per_id)
                # print(getPartnerActiveTransactionalSubscriptionPlan)

                if subscription_object:
                    if int(float(subscription_object.total_sms_avilable)):
                        if customer:
                            users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new)
                            if users:
                                customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new).count()
                                customer_sms_count = bulkMailSmsPartnerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                customer_addresswise_count = customer_count
                                for u in users:
                                    for notice in sent_notice:
                                        if notice == "sms":
                                                contact = u.mobile_no
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
                                                                        "DLT_CT_ID":unique_template_id, # Template Id
                                                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                    }
                                                                ]
                                                            }

                                                    url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                    response = requests.post(url, json = data_temp)

                                                sms_response = sendSMS(str(contact), message)

                                                if response.status_code == 200:
                                                    total_sms_avilable_new = 0
                                                    if customer:
                                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                                        subscription_object.total_sms_avilable = total_sms_avilable_new
                                                    else:
                                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                                        subscription_object.total_sms_avilable = total_sms_avilable_new
                                                    subscription_object.save()
                                                        
                                                    bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="Delivered")

                                                    sweetify.success(request, title="Success", icon='success',
                                                                            text='SMS Send successfully!!', timer=5500)
                                                else:
                                                    bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="failed to Deliver")
                                                    sweetify.error(request, title="Error", icon='error',
                                                                    text="Something Went Wrong!!!", timer=5500)


                            else:
                                sweetify.error(request, title="Error", icon='error',
                                                                    text="Customer With This Area Not Found!!!", timer=5500)
                        
                        if merchant:
                            users = MerchantProfile.objects.filter(m_state__in=merchant_state_value_new, m_city__in=merchant_city_value_new, m_area__in=merchant_area_value_new)
                            for u in users:
                                for notice in sent_notice:
                                    if notice == "sms":
                                            contact = u.m_user
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
                                                                    "DLT_CT_ID":unique_template_id, # Template Id
                                                                    "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                }
                                                            ]
                                                        }

                                                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                response = requests.post(url, json = data_temp)

                                            sms_response = sendSMS(str(contact), message)


                                            if response.status_code == 200:
                                                total_sms_avilable_new = 0
                                                if customer:
                                                    total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                                    subscription_object.total_sms_avilable = total_sms_avilable_new
                                                else:
                                                    total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                                    subscription_object.total_sms_avilable = total_sms_avilable_new
                                                subscription_object.save()
                                                    
                                                bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="Delivered")

                                                sweetify.success(request, title="Success", icon='success',
                                                                        text='SMS Send successfully!!', timer=5500)
                                            else:
                                                bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="failed to Deliver")
                                                sweetify.error(request, title="Error", icon='error',
                                                                text="Something Went Wrong!!!", timer=5500)
                                            
                                            sms_response = sendSMS(str(contact), message)
                        

                        if custom_number_list:
                            for notice in sent_notice:
                                for number in custom_number_list:
                                    if notice == 'sms':
                                        contact = number

                                        if contact:
                                            ts = int(time.time())

                                            data_temp = {
                                                    "keyword":"New Merchant Registration",
                                                    "timeStamp":ts,
                                                    "dataSet":
                                                        [
                                                            {
                                                                "UNIQUE_ID":"GB-" + str(ts),
                                                                "MESSAGE":str(message),
                                                                "OA":str(smsheader),
                                                                "MSISDN":contact, # Recipient's Mobile Number
                                                                "CHANNEL":"SMS",
                                                                "CAMPAIGN_NAME":"hind_user",
                                                                "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                                "USER_NAME":"hind_hsi",
                                                                "DLT_TM_ID":"1001096933494158", # TM ID
                                                                "DLT_CT_ID":unique_template_id, # Template Id
                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                            }
                                                        ]
                                                    }

                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                            response = requests.post(url, json = data_temp)

                                        sms_response = sendSMS(str(contact), message)
                        
                                        if response.status_code == 200:
                                            total_sms_avilable_new = 0
                                            if customer:
                                                total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                                subscription_object.total_sms_avilable = total_sms_avilable_new
                                            else:
                                                total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                                subscription_object.total_sms_avilable = total_sms_avilable_new
                                            subscription_object.save()
                                                
                                            bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="Delivered")

                                            sweetify.success(request, title="Success", icon='success',
                                                                    text='SMS Send successfully!!', timer=5500)
                                        else:
                                            bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="failed to Deliver")
                                            sweetify.error(request, title="Error", icon='error',
                                                            text="Something Went Wrong!!!", timer=5500)

                        if csv_fields:
                            for notice in sent_notice:
                                for number in csv_fields:
                                    if notice == 'sms':
                                        contact = number
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
                                                                "DLT_CT_ID":unique_template_id, # Template Id
                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                            }
                                                        ]
                                                    }

                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                            response = requests.post(url, json = data_temp)
                                        
                                        sms_response = sendSMS(str(contact), message)

                            if response.status_code == 200:
                                total_sms_avilable_new = 0
                                if customer:
                                    total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                    subscription_object.total_sms_avilable = total_sms_avilable_new
                                else:
                                    total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(receipent_count)
                                    subscription_object.total_sms_avilable = total_sms_avilable_new
                                subscription_object.save()
                                    
                                bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="Delivered")

                                sweetify.success(request, title="Success", icon='success',
                                                        text='SMS Send successfully!!', timer=5500)
                            else:
                                bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="failed to Deliver")
                                sweetify.error(request, title="Error", icon='error',
                                                text="Something Went Wrong!!!", timer=5500)
                                

                    else:
                        bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="failed to Deliver")
                        sweetify.success(request, title="Oops...", icon='error', text='Insufficient Balance. Please purchase Transactional plan and try again !!!', timer=2000)
                else:
                    bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="failed to Deliver")
                    sweetify.success(request, title="Oops...", icon='error', text="You don't have active Transactional SMS plan. Please purchase and try again.", timer=2000)
           
            if transactional == 'promotional':
                par_user_id = Partner_users.objects.get(user_id=request.user)
                partner_object = par_user_id.partner_user_id
                partner_business_object = PartnerProfile.objects.get(p_user = partner_object, p_active_account = True)
                per_id=par_user_id.partner_user_id

                subscription_object = getPartnerActivePromotionalSubscriptionPlan(request, per_id)

                if subscription_object:
                    if int(float(subscription_object.total_sms_avilable)):
                        if customer:
                            users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new)
                            if users:
                                customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new).count()
                                customer_sms_count = bulkMailSmsPartnerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                customer_addresswise_count = customer_count

                                for u in users:
                                    for notice in sent_notice:
                                        if notice == "sms":
                                                contact = u.mobile_no
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
                                                                        "DLT_CT_ID":template, # Template Id
                                                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                    }
                                                                ]
                                                            }

                                                    url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                    response = requests.post(url, json = data_temp)

                                                    if response.status_code == 200:
                                                        total_sms_avilable_new = 0
                                                        if customer:
                                                            total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                                            subscription_object.total_sms_avilable = total_sms_avilable_new
                                                        else:
                                                            total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                                            subscription_object.total_sms_avilable = total_sms_avilable_new
                                                        subscription_object.save()
                                                            
                                                        bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="Delivered")

                                                        sweetify.success(request, title="Success", icon='success',
                                                                                text='SMS Send successfully!!', timer=5500)
                                                    else:
                                                        bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="failed to Deliver")
                                                        sweetify.error(request, title="Error", icon='error',
                                                                        text="Something Went Wrong!!!", timer=5500)                                                

                            else:
                                sweetify.error(request, title="Error", icon='error',
                                                                    text="Customer With This Area Not Found!!!", timer=5500)

                        
                        if merchant:
                            users = MerchantProfile.objects.filter(merchant_by_partner = request.user,m_state__in=merchant_state_value_new, m_city__in=merchant_city_value_new, m_area__in=merchant_area_value_new)
                            for u in users:
                                for notice in sent_notice:
                                    if notice == "sms":
                                            contact = u.m_user
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
                                                                    "DLT_CT_ID":template, # Template Id
                                                                    "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                }
                                                            ]
                                                        }

                                                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                response = requests.post(url, json = data_temp)

                                                if response.status_code == 200:
                                                    total_sms_avilable_new = 0
                                                    if customer:
                                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                                        subscription_object.total_sms_avilable = total_sms_avilable_new
                                                    else:
                                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                                        subscription_object.total_sms_avilable = total_sms_avilable_new
                                                    subscription_object.save()
                                                        
                                                    bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="Delivered")

                                                    sweetify.success(request, title="Success", icon='success',
                                                                            text='SMS Send successfully!!', timer=5500)
                                                else:
                                                    bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="failed to Deliver")
                                                    sweetify.error(request, title="Error", icon='error',
                                                                    text="Something Went Wrong!!!", timer=5500)

                                            
                                            sms_response = sendSMS(str(contact), message)
                        

                        if custom_number_list:
                            for notice in sent_notice:
                                for number in custom_number_list:
                                    if notice == 'sms':
                                        contact = number
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
                                                                "DLT_CT_ID":template, # Template Id
                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                            }
                                                        ]
                                                    }

                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                            response = requests.post(url, json = data_temp)

                                            if response.status_code == 200:
                                                total_sms_avilable_new = 0
                                                if customer:
                                                    total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                                    subscription_object.total_sms_avilable = total_sms_avilable_new
                                                else:
                                                    total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                                    subscription_object.total_sms_avilable = total_sms_avilable_new
                                                subscription_object.save()
                                                    
                                                bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="Delivered")

                                                sweetify.success(request, title="Success", icon='success',
                                                                        text='SMS Send successfully!!', timer=5500)
                                            else:
                                                bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="failed to Deliver")
                                                sweetify.error(request, title="Error", icon='error',
                                                                text="Something Went Wrong!!!", timer=5500)

                                
                                        sms_response = sendSMS(str(contact), message)

                            
                        if csv_fields:
                            for notice in sent_notice:
                                for number in csv_fields:
                                    if notice == 'sms':
                                        contact = number
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
                                                                "DLT_CT_ID":template, # Template Id
                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                            }
                                                        ]
                                                    }

                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                            response = requests.post(url, json = data_temp)
 
                                        
                                        sms_response = sendSMS(str(contact), message)

                            if response.status_code == 200:
                                total_sms_avilable_new = 0
                                if customer:
                                    total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                    subscription_object.total_sms_avilable = total_sms_avilable_new
                                else:
                                    total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(receipent_count)
                                    subscription_object.total_sms_avilable = total_sms_avilable_new
                                subscription_object.save()
                                    
                                bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="Delivered")

                                sweetify.success(request, title="Success", icon='success',
                                                        text='SMS Send successfully!!', timer=5500)
                            else:
                                bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="failed to Deliver")
                                sweetify.error(request, title="Error", icon='error',
                                                        text="Something Went Wrong!!!", timer=5500)

                    else:
                        bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="failed to Deliver")
                        sweetify.success(request, title="Oops...", icon='error', text='Insufficient Balance. Please purchase Transactional plan and try again !!!', timer=2000)
                else:
                    bulkMailSmsPartnerModel.objects.filter(id=(int(smsid)+1)).update(sent_status="failed to Deliver")
                    sweetify.success(request, title="Oops...", icon='error', text="You don't have active Transactional SMS plan. Please purchase and try again.", timer=2000)
           

        
    promotional_remaining_sms = ''
    promotional_used_sms = ''
    transactional_remaining_sms = ''
    transactional_used_sms = ''
    par_user_id = Partner_users.objects.get(user_id=request.user)
    partner_object = par_user_id.partner_user_id
    partner_business_object = PartnerProfile.objects.get(p_user = partner_object, p_active_account = True)
    per_id=par_user_id.partner_user_id


    if getPartnerActiveTransactionalSubscriptionPlan(request, per_id):
        tran_subscription_object = getPartnerActiveTransactionalSubscriptionPlan(request, per_id)
        transactional_remaining_sms = int(tran_subscription_object.total_sms_avilable)
        transactional_used_sms = int(tran_subscription_object.total_sms) - transactional_remaining_sms
    else:
        pass

    if getPartnerActivePromotionalSubscriptionPlan(request, per_id):
        promo_subscription_object = getPartnerActivePromotionalSubscriptionPlan(request, per_id)
        promotional_remaining_sms = int(promo_subscription_object.total_sms_avilable)
        promotional_used_sms = int(promo_subscription_object.total_sms) - promotional_remaining_sms
    else:
        pass
    

    smsmail = bulkMailSmsPartnerModel.objects.filter(owner_id=partner_object,o_sent_sms=True).order_by('-id')
    states = GreenBillUser.objects.values('c_state').distinct()
    merchantState = MerchantProfile.objects.values('m_state').distinct()
    context = {
        'merchantState': merchantState,
        'bulk_sms_header': bulk_sms_header,
        'bulk_sms_template': bulk_sms_template,
        'cust_data': states,
        'data': smsmail,
        'merchant_list': staff,
        'PromotionsNavclass': 'active',
        'ShowPromotionsNavclass':'show',
        'BulkSMSNavclass':'active',
        "customer_addresswise_count":customer_addresswise_count,
        'merchant_users_count':merchant_users_count,
        'bulkMailSmsPartnerForm':bulkMailSmsPartnerForm,
        'promotional_remaining_sms':promotional_remaining_sms,
        'promotional_used_sms':promotional_used_sms,
        'transactional_remaining_sms':transactional_remaining_sms,
        'transactional_used_sms':transactional_used_sms,

    }

    return render(request, 'partner/partner-promotion-sms.html' , context)
 
def deleteSmsEmail(request,id):
    instance = bulkMailSmsPartnerModel.objects.get(id=id).delete()

    return JsonResponse({'success':True})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def viewMerchantsRecords(request, id=None):
    merchant_business_object = MerchantProfile.objects.get(id=id)

    merchant_business_id = merchant_business_object.id

    merchant_user = []

    # merchant_user.append({
    #     'user_id': merchant_object
    # })

    merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = request.user, m_business_id = merchant_business_id)

    for user in merchant_user_temp:
        merchant_user.append({
            'user_id': user.user_id
            })

    data = []

    base_url = "http://157.230.228.250/"

    try:
        bill_design = bill_designs.objects.get(merchant_business_id = merchant_business_object)
        bill_rating_emoji = bill_design.rating_emoji
    except:
        bill_rating_emoji = ""

    parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False).order_by('-id')
    parking_bill_count = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False).count()
    

    petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id).order_by('-id')
    petrol_bill_count = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id).count()

    customer_bill_list = CustomerBill.objects.filter(business_name_id=merchant_business_id,customer_added = False).order_by('-id')
    customer_bill_count = CustomerBill.objects.filter(business_name_id=merchant_business_id,customer_added = False).count()

    merchant_bill_list = MerchantBill.objects.filter(business_name=merchant_business_id)
    merchant_bill_count = MerchantBill.objects.filter(business_name=merchant_business_id).count()
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
    
    # all_bill_amount_sum = 0
    # for temp in data:
    #     all_bill_amount_sum = all_bill_amount_sum + temp['amount']
    
    # if len(data) != 0:
    #     average_bill_amount = all_bill_amount_sum/len(data)
    # else:
    #     average_bill_amount = 0
    
    unique_customer_count = []
    for data_list in data:
        if data_list['mobile_no'] not in unique_customer_count:
            unique_customer_count.append(data_list['mobile_no'])
    
    customer_count = len(unique_customer_count)
    
    bill_sent_count = parking_bill_count + petrol_bill_count + customer_bill_count + merchant_bill_count
    
    active_subs = getActiveSubscriptionPlan(request,merchant_business_id)
    active_transactional_subs = getActiveTransactionalSubscriptionPlan(request,merchant_business_id)
    print('active_transactional_subs',active_transactional_subs)
    active_promotional_subs = getActivePromotionalSubscriptionPlan(request,merchant_business_id)
    print('active_promotional_subs',active_promotional_subs)
    
    offers_count = OfferModel.objects.filter(merchant_user = merchant_business_object.m_user, merchant_business_id = merchant_business_object).count()

    coupon_count = CouponModel.objects.filter(merchant_id = merchant_business_object.m_user, merchant_business_id = merchant_business_object.id).count()

    coupon_redeem_count = RedeemCouponModel.objects.filter(merchant_id = merchant_business_object.m_user, merchant_business_id = merchant_business_object.id).count()
    # coupon_count = CouponModel.objects.filter(merchant_id = merchant_nubmer_id).count()

    try:
        merchant_user_record_id = Merchant_users.objects.filter(user_id = merchant_business_object.m_user).values('merchant_user_id')[0]['merchant_user_id']

        merchant_user_id_object = GreenBillUser.objects.get(id=merchant_user_record_id)

        total_users = Merchant_users.objects.filter(merchant_user_id = merchant_user_id_object,m_business_id = merchant_business_object.id).count()
    except:
        total_users = ""
    try:
        refferal_code = GreenBillUser.objects.get(mobile_no = merchant_nubmer_id)
        check_refferal_code = refferal_code.merchant_referral_code

        reffer_count = GreenBillUser.objects.filter(m_used_referral_code=check_refferal_code).count()
    except:
        reffer_count = ''

    context = {
            # 'merchantBusinessesList' : merchantBusinessesList,
            # 'merchantBusinessCategory' : merchnat_business_category,
            # 'form': form,
            'bill_sent_count':bill_sent_count,
            'total_users': total_users,
            'reffer_count': reffer_count,
            'coupon_count' : coupon_count,
            'offers_count' : offers_count,
            'coupon_redeem_count': coupon_redeem_count,
            # 'all_bill_amount_sum':"{:.2f}".format(all_bill_amount_sum),
            'total_transaction':total_transaction,
            # 'average_bill_amount' : "{:.2f}".format(average_bill_amount),
            'customer_count':customer_count,
            'active_subscription': active_subs,
            'active_transactional_subscription':active_transactional_subs,
            'active_promotional_subscription':active_promotional_subs,
            'partnerNavActiveClass': "active",
            'PartnerInfoCollapseShow': "show",
            'PartnerListNavclass': "active",
        }
    return render(request, 'super_admin/view-all-records-merchant.html', context)



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def viewMerchantsRecordsOfSoftwarePartner(request, id=None):
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
            'partnerNavActiveClass': "active",
            'PartnerInfoCollapseShow': "show",
            'PartnerSoftwareNavClass': "active",
        }
    return render(request, 'super_admin/view-all-records-merchant.html', context)
    # merchant_business_object = MerchantProfile.objects.get(id=id)

    # merchant_business_id = merchant_business_object.id

    # merchant_user = []

    # # merchant_user.append({
    # #     'user_id': merchant_object
    # # })

    # merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = request.user, m_business_id = merchant_business_id)

    # for user in merchant_user_temp:
    #     merchant_user.append({
    #         'user_id': user.user_id
    #         })

    # data = []

    # base_url = "http://157.230.228.250/"

    # try:
    #     bill_design = bill_designs.objects.get(merchant_business_id = merchant_business_object)
    #     bill_rating_emoji = bill_design.rating_emoji
    # except:
    #     bill_rating_emoji = ""

    # parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False).order_by('-id')
    # parking_bill_count = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False).count()
    

    # petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id).order_by('-id')
    # petrol_bill_count = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id).count()

    # customer_bill_list = CustomerBill.objects.filter(business_name_id=merchant_business_id,customer_added = False).order_by('-id')
    # customer_bill_count = CustomerBill.objects.filter(business_name_id=merchant_business_id,customer_added = False).count()

    # merchant_bill_list = MerchantBill.objects.filter(business_name=merchant_business_id)
    # merchant_bill_count = MerchantBill.objects.filter(business_name=merchant_business_id).count()
    # data = []
    # for bill in parking_bill_list:
    #     data.append({
    #         'mobile_no': bill.mobile_no,
    #         'amount' : float(bill.amount),


    #     })
    # for bill in petrol_bill_list:
    #     data.append({
    #         'mobile_no': bill.mobile_no,
    #         'amount' : bill.amount,
    #     })
    # for bill in customer_bill_list:
    #     data.append({
    #         'mobile_no': bill.mobile_no,
    #         'amount' : bill.bill_amount,


    #     })
    # for bill in merchant_bill_list:
    #     data.append({
    #         'mobile_no': bill.mobile_no,
    #         'amount' : bill.bill_amount,


    #     })

    # # all_bill_amount_sum = 0
    # # for temp in data:
    # #     all_bill_amount_sum = all_bill_amount_sum + temp['amount']
    # # if len(data) != 0:
    # #     average_bill_amount = all_bill_amount_sum/len(data)
    # # else:
    # #     average_bill_amount = 0

    # total_transaction = 0

    # total_transaction = customer_bill_count + merchant_bill_count

    # unique_customer_count = []
    # for data_list in data:
    #     if data_list['mobile_no'] not in unique_customer_count:
    #         unique_customer_count.append(data_list['mobile_no'])

    # customer_count = len(unique_customer_count)
    
    # bill_sent_count = parking_bill_count + petrol_bill_count + customer_bill_count + merchant_bill_count

    # active_subs = getActiveSubscriptionPlan(request,merchant_business_id)
    # active_transactional_subs = getActiveTransactionalSubscriptionPlan(request,merchant_business_id)
    # active_promotional_subs = getActivePromotionalSubscriptionPlan(request,merchant_business_id)


    # coupon_count = CouponModel.objects.filter(merchant_id = merchant_business_object.m_user, merchant_business_id = merchant_business_object.id).count()

    # coupon_redeem_count = RedeemCouponModel.objects.filter(merchant_id = merchant_business_object.m_user, merchant_business_id = merchant_business_object.id).count()
    # # coupon_count = CouponModel.objects.filter(merchant_id = merchant_nubmer_id).count()

    # offers_count = OfferModel.objects.filter(merchant_user = merchant_business_object.m_user, merchant_business_id = merchant_business_object).count()

    # try:
    #     merchant_user_record_id = Merchant_users.objects.filter(user_id = merchant_business_object.m_user).values('merchant_user_id')[0]['merchant_user_id']

    #     merchant_user_id_object = GreenBillUser.objects.get(id=merchant_user_record_id)

    #     total_users = Merchant_users.objects.filter(merchant_user_id = merchant_user_id_object,m_business_id = merchant_business_object.id).count()
    # except:
    #     total_users = ""
    # try:
    #     refferal_code = GreenBillUser.objects.get(mobile_no = merchant_nubmer_id)
    #     check_refferal_code = refferal_code.merchant_referral_code

    #     reffer_count = GreenBillUser.objects.filter(m_used_referral_code=check_refferal_code).count()
    # except:
    #     reffer_count = ''

    # context = {
    #         # 'merchantBusinessesList' : merchantBusinessesList,
    #         # 'merchantBusinessCategory' : merchnat_business_category,
    #         # 'form': form,
    #         'bill_sent_count':bill_sent_count,
    #         'total_users': total_users,
    #         'reffer_count': reffer_count,
    #         'coupon_count' : coupon_count,
    #         'offers_count' : offers_count,
    #         'coupon_redeem_count': coupon_redeem_count,
    #         # 'all_bill_amount_sum':"{:.2f}".format(all_bill_amount_sum),
    #         # 'average_bill_amount' : "{:.2f}".format(average_bill_amount),
    #         'total_transaction':total_transaction,
    #         'customer_count':customer_count,
    #         'active_subscription': active_subs,
    #         'active_transactional_subscription':active_transactional_subs,
    #         'active_promotional_subscription':active_promotional_subs,
            # 'partnerNavActiveClass': "active",
            # 'PartnerInfoCollapseShow': "show",
            # 'PartnerSoftwareNavClass': "active",
    #     }
    # return render(request, 'super_admin/view-all-records-merchant.html', context)

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
def disableMerchantByPartner(request):
    if request.method == "POST":
        
        merchant_id = request.POST['merchant_id']
        print(merchant_id)
        reason = request.POST['reason']
        MerchantProfile.objects.filter(id=merchant_id).update(m_disabled_account=True, disable_reason= reason)
        # GreenBillUser.objects.filter(id= merchant_id).update(is_active=False, disable_reason= reason)
        return JsonResponse({'status': 1, 'msg': 'Status change successfully'})
        
    else:
        return JsonResponse({'status': 0, 'msg': 'Something went wrong'})



@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def viewMerchantsRecordsbypartner(request, id=None):
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


    context = {
            # 'merchantBusinessesList' : merchantBusinessesList,
            # 'merchantBusinessCategory' : merchnat_business_category,
            # 'form': form,
            'total_customer_count':total_customer_count,
            'merchant_id': id,
            'from_date': from_date1,
            'to_date': to_date,
            'self_add_customer_count':self_add_customer_count,
            'sms_sent':sms_sent,
            'digital_sent':digital_sent,
            'total_bill_sent':total_bill_sent,
            'total_payment': total_payment,
            'total_amount_spent':total_amount_spent,
            'send_bill_count':send_bill_count,
            'total_bill_sent':total_bill_sent,
          
            'send_print_bill_count':send_print_bill_count,
            'exe_print_bill_status':exe_print_bill_status,
            'bill_sent_count':bill_sent_count,
            'total_users': total_users,
            'reffer_count': reffer_count,
            'coupon_count' : coupon_count,
            'offers_count' : offers_count,
            'coupon_redeem_count': coupon_redeem_count,
            # 'all_bill_amount_sum':"{:.2f}".format(all_bill_amount_sum),
            # 'average_bill_amount' : "{:.2f}".format(average_bill_amount),
            'total_transaction':total_transaction,
            'customer_count':customer_count,
            'active_subscription': active_subs,
            'active_transactional_subscription':active_transactional_subs,
            'active_promotional_subscription':active_promotional_subs,

            'partnerMerchantNavclass': "active", 
            'partnerMerchantInfoNavcollclass': "show",
            'partnerMerchantInfoNavclass': "active",
        }
    return render(request, 'partner/view-analysis-of-merchant.html', context)


def getallActiveSubscriptionPlan(request, business_id):

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


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def disableMerchantByPartnerinpartner(request):
    if request.method == "POST":
        
        merchant_id = request.POST['merchant_id']
        print(merchant_id)
        reason = request.POST['reason']
        MerchantProfile.objects.filter(id=merchant_id).update(m_disabled_account=True, disable_reason= reason)
        # GreenBillUser.objects.filter(id= merchant_id).update(is_active=False, disable_reason= reason)
        return JsonResponse({'status': 1, 'msg': 'Status change successfully'})
        
    else:
        return JsonResponse({'status': 0, 'msg': 'Something went wrong'})

def get_city_by_state_ids_in_partner_bulk_email(request):

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


def get_area_by_city_names_in_partner_bulk_email(request):

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

    return JsonResponse({"data":filtered_area_list})\


def get_template_by_header_in_partner(request):
    smsheader = request.POST['smsheader']
    Template = templateContentModel.objects.filter(request_user = request.user, status='Approved')
    list1 = []
    filtered_city_list = []
    for obj in Template:
        if obj.sms_header:
            if smsheader in obj.sms_header:
                list1.append({
                    "template_content": obj.template_content
                })
    for x in list1:
        if x['template_content'] not in filtered_city_list:
            if x['template_content'] != '':
                filtered_city_list.append(x['template_content'])
    print('filtered_city_list1',filtered_city_list)
    return JsonResponse({"data":filtered_city_list})

def get_id_by_template_in_partner(request):
    template_id = request.POST['template_id']
    Template = templateContentModel.objects.filter(request_user = request.user, status='Approved', template_content=template_id)
    list1 = []
    filtered_city_list = []
    for obj in Template:
        list1.append({
            "template_content_id": obj.id
        })
    for x in list1:
        if x['template_content_id'] not in filtered_city_list:
            if x['template_content_id'] != '':
                filtered_city_list.append(x['template_content_id'])
    print('filtered_city_list',filtered_city_list)
    return JsonResponse({"data":filtered_city_list})


def get_merchant_city_by_state_names(request):

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


def get_merchant_area_by_city_names(request):

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



# def pie_chart(request):
#     labels = []
#     data = []

#     queryset = City.objects.order_by('-population')[:5]
#     for city in queryset:
#         labels.append(city.name)
#         data.append(city.population)

#     return render(request, 'pie_chart.html', {
#         'labels': labels,
#         'data': data,
#     })



@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_comission(request):

    par_user_id = Partner_users.objects.get(user_id=request.user)

    partner_object = par_user_id.partner_user_id

    customer_object1 = GreenBillUser.objects.get(mobile_no = partner_object)

    partner_category = PartnerProfile.objects.get(p_user = customer_object1)

    par_mob_no = partner_category.p_user

    commision_per_merchant = partner_category.merchant_commission

    commision_per_merchant_bill = partner_category.p_commission_per_bill

    merchantBusinessesList = MerchantProfile.objects.filter(merchant_by_partner=customer_object1).order_by('-id')

    merchants_count = MerchantProfile.objects.filter(merchant_by_partner=customer_object1).count()

    overall_commision = 0

    overall_bills_commision = 0

    merchant_monthly_commision = 0

    bill_monthly_commision = 0

    partner_month_comission = 0

    given_date = datetime.today().date()
 
    first_day_of_month = given_date.strftime("%Y-%m-01")

    merchant_counter = 0

    is_marketing = False

    monthly_per_digital_bills = 0

    monthly_per_sms_bills = 0

    per_sms_bills = 0

    per_digital_bills = 0

    bill_comission_to_show =[]

    total_of_total = 0

    merchant_name = []

    if request.method == 'POST':
        from_date_temp1 = request.POST["from_date1"]
        to_date_temp1 = request.POST["to_date1"]

        DATE_FORMAT = '%Y-%m-%d'
        date_time_obj = datetime.strptime(to_date_temp1, '%Y-%m-%d')
        day_later = date_time_obj + timedelta(days=1)
        x = day_later.date()
        ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

        billing_from_date = datetime.strptime(str(from_date_temp1), '%Y-%m-%d').strftime('%d-%m-%Y')
        start_date = billing_from_date.split('-')
        start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
        sd_filter = start_date.strftime(DATE_FORMAT)
    else:
        from_date_temp1 = ''
        to_date_temp1 = ''

    vyas_yes = False

    for merchant in merchantBusinessesList:
        list_to_append = []


        total_bills = 0

        merchant_profile_id = MerchantProfile.objects.get(id=merchant.id)

        user_id = GreenBillUser.objects.get(mobile_no = merchant.m_user) 

        merchant_subscriptions_till_now = merchant_subscriptions.objects.filter(merchant_id= user_id).count()
        merchant_subscriptions_till_now_object = merchant_subscriptions.objects.filter(merchant_id= user_id)
        print("**************imp********************")
        print(merchant_subscriptions_till_now)

        merchant.m_number = user_id

        if user_id.mobile_no == "7020598727":
            vyas_yes = True

        if request.method == 'POST':
        # if 1==2: 

            customer_bill = CustomerBill.objects.filter(business_name = merchant_profile_id, customer_added = False, created_at__gte = sd_filter, created_at__lte = ed_filter).count()

            merchant_bill = MerchantBill.objects.filter(business_name = merchant_profile_id, created_at__gte = sd_filter, created_at__lte = ed_filter).count()

            parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile_id, is_pass = False, created_at__gte = sd_filter, created_at__lte = ed_filter).count()

            petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile_id, created_at__gte = sd_filter, created_at__lte = ed_filter).count()

            customer_bill1 = CustomerBill.objects.filter(business_name = merchant_profile_id, customer_added = False, created_at__gte = sd_filter, created_at__lte = ed_filter)

            merchant_bill1 = MerchantBill.objects.filter(business_name = merchant_profile_id, created_at__gte = sd_filter, created_at__lte = ed_filter)

            parking_bill_list1 = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile_id.id, is_pass = False, created_at__gte = sd_filter, created_at__lte = ed_filter)

            petrol_bill_list1 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile_id.id, created_at__gte = sd_filter, created_at__lte = ed_filter)
        else:

            customer_bill = CustomerBill.objects.filter(business_name = merchant_profile_id, customer_added = False).count()

            merchant_bill = MerchantBill.objects.filter(business_name = merchant_profile_id).count()

            parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile_id, is_pass = False).count()

            petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile_id).count()

            customer_bill1 = CustomerBill.objects.filter(business_name = merchant_profile_id, customer_added = False)

            merchant_bill1 = MerchantBill.objects.filter(business_name = merchant_profile_id)

            parking_bill_list1 = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile_id.id, is_pass = False)

            petrol_bill_list1 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile_id.id)


        if customer_bill1:
            for bill in customer_bill1:

                if bill.greenbill_digital_bill == "True":
                    per_digital_bills = per_digital_bills + 1

                if bill.greenbill_sms_bill == "True":
                    per_sms_bills = per_sms_bills + 1

                bill_start_date1=timezone.localtime(bill.created_at).strftime("%Y-%m-%d")

                if first_day_of_month <= bill_start_date1:

                    if bill.greenbill_digital_bill == "True":
                        monthly_per_digital_bills = monthly_per_digital_bills + 1

                    if bill.greenbill_sms_bill == "True":
                        monthly_per_sms_bills = monthly_per_sms_bills + 1

        if merchant_bill1:
            for bill in merchant_bill1:

                if bill.greenbill_digital_bill == "True":
                    per_digital_bills = per_digital_bills + 1

                if bill.greenbill_sms_bill == "True":
                    per_sms_bills = per_sms_bills + 1
                    
                bill_start_date2=timezone.localtime(bill.created_at).strftime("%Y-%m-%d")

                if first_day_of_month <= bill_start_date2:
                    if bill.greenbill_digital_bill == "True":
                        monthly_per_digital_bills = monthly_per_digital_bills + 1

                    if bill.greenbill_sms_bill == "True":
                        monthly_per_sms_bills = monthly_per_sms_bills + 1

        if parking_bill_list1:
            for bill in parking_bill_list1:
                if bill.greenbill_digital_bill == "True":
                    per_digital_bills = per_digital_bills + 1

                if bill.greenbill_sms_bill == "True":
                    per_sms_bills = per_sms_bills + 1
                    
                bill_start_date3=timezone.localtime(bill.created_at).strftime("%Y-%m-%d")

                if first_day_of_month <= bill_start_date3:
                    if bill.greenbill_digital_bill == "True":
                        monthly_per_digital_bills = monthly_per_digital_bills + 1

                    if bill.greenbill_sms_bill == "True":
                        monthly_per_sms_bills = monthly_per_sms_bills + 1

        if petrol_bill_list1:
            for bill in petrol_bill_list1:
                if bill.greenbill_digital_bill == "True":
                    per_digital_bills = per_digital_bills + 1

                if bill.greenbill_sms_bill == "True":
                    per_sms_bills = per_sms_bills + 1
                    
                bill_start_date4=timezone.localtime(bill.created_at).strftime("%Y-%m-%d")

                if first_day_of_month <= bill_start_date4:
                    if bill.greenbill_digital_bill == "True":
                        monthly_per_digital_bills = monthly_per_digital_bills + 1

                    if bill.greenbill_sms_bill == "True":
                        monthly_per_sms_bills = monthly_per_sms_bills + 1 


        total_bills = int(customer_bill) + int(merchant_bill) + int(parking_bill_list) + int(petrol_bill_list)

        par_comission = int(customer_bill) + int(merchant_bill) + int(parking_bill_list) + int(petrol_bill_list)

        if partner_category.p_category == 'Marketing Partner':
            if 1==1:
                t=0
                d=0
                # for i in merchant_subscriptions_till_now_object:
                #     t = float(i.valid_for_month) * float(i.no_of_users)
                #     d = d+(t*float(commision_per_merchant))/100
                # print("*@&@8282882229")
                # print(d)

                try:
                    i = merchant_subscriptions_till_now_object[len(merchant_subscriptions_till_now_object)-1]
                    # for i in merchant_subscriptions_till_now_object:

                    r = subscription_plan_details.objects.get(subscription_name = i.subscription_name)
                    print("P:SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                    print()
                    t = float(i.valid_for_month) * float(i.no_of_users)*float(r.cost_for_users)
                    d = d+(t*float(commision_per_merchant))/100
                    print("*@&@8282882229")
                    print(d)
                except:
                    pass

                total_bills = int(customer_bill) + int(merchant_bill) + int(parking_bill_list) + int(petrol_bill_list)

                par_comission = int(customer_bill) + int(merchant_bill) + int(parking_bill_list) + int(petrol_bill_list)

                commision_per_merchant = partner_category.merchant_commission

                commision_per_sms_bill = partner_category.p_commission_per_sms_bill

                commision_per_digital_bill = partner_category.p_commission_per_digital_bill

                if not partner_category.p_commission_per_bill:
                    commision_per_merchant_bill = 0

                bills_comission = float(total_bills) * float(commision_per_merchant)

                print("*#&#&*#*#")
                print(commision_per_merchant)

                # merchant.total_comission = float(bills_comission) + float(commision_per_merchant)
                

                if par_comission != 0:
                   
                    overall_bills_commision = (float(per_sms_bills) * float(commision_per_sms_bill)) + (float(per_digital_bills) * float(commision_per_digital_bill)) + float(overall_commision)

                total_amount_to_cal_inpercent = d
                print("Amount to addd....................")
                print(total_amount_to_cal_inpercent)

                total_of_total = total_amount_to_cal_inpercent+total_of_total

                # total_merchant_with_commission =  float(merchantBusinessesListcount) * float(commision_per_merchant) +(float(total_amount_to_cal_inpercent)) 
                if vyas_yes :
                    merchant.total_comission = float(total_amount_to_cal_inpercent)+float(overall_bills_commision)-11.08 +0.12
                    overall_commision =  float(overall_bills_commision)+(float(total_of_total))-11.08 +0.12
                else:
                    merchant.total_comission = float(total_amount_to_cal_inpercent)+float(overall_bills_commision)
                    overall_commision =  float(overall_bills_commision)+(float(total_of_total))

                print("****************")
                print(overall_commision)
                
                merchant.total_comission = float(total_amount_to_cal_inpercent)+float(overall_bills_commision)
    


            if vyas_yes and  given_date.month == 4 and given_date.year == 2022:

                partner_month_comission = (float(total_of_total)) + (float(monthly_per_sms_bills) * float(partner_category.p_commission_per_sms_bill)) + (float(monthly_per_digital_bills) * float(partner_category.p_commission_per_digital_bill))- 1.38 +0.12
            else:
                partner_month_comission = (float(total_of_total)) + (float(monthly_per_sms_bills) * float(partner_category.p_commission_per_sms_bill)) + (float(monthly_per_digital_bills) * float(partner_category.p_commission_per_digital_bill))

            p_monthlyModel = PartnerMonthlyCommision.objects.filter(p_mobile_no = par_mob_no, month = given_date.month, year = given_date.year)

            try:
                if p_monthlyModel:

                    current_month_amount = p_monthlyModel[0].amount

                    if float(partner_month_comission) != float(current_month_amount):

                        p_monthlyModel = PartnerMonthlyCommision.objects.filter(p_mobile_no = par_mob_no, month = given_date.month, year = given_date.year).update(amount = partner_month_comission)

                else:
                    p_monthlyModel = PartnerMonthlyCommision.objects.create(p_mobile_no = par_mob_no, month = given_date.month, amount = partner_month_comission, year = given_date.year)

            except:
                pass

        bill_comission_to_show.append(list_to_append)
        merchant_name.append(merchant.m_business_name)

    # print("***************************")

    # print(bill_comission_to_show)
    # print(merchant_name)

    sms_list = []
    digital_list = []
    other_list = []
    for i in (bill_comission_to_show):
        print("*************")
        print(i)
        sms_list.append(i)
        digital_list.append(i)
        other_list.append(i)


    # print("&&&&&&&&&&&&&&&&&&&&&&&&")

    # print(other_list,digital_list,sms_list)

    # print("383hdjjjjjjjjjjjjjjjjjjjjjjj")
    # print(total_of_total)


    if is_marketing == True and vyas_yes:
        # total_merchant_with_commission =  float(merchants_count) * float(commision_per_merchant) +float(total_of_total)
        overall_commision =  float(overall_bills_commision)-11.08

    print("2929929")
    print(overall_commision)
    context = {
        "partner_month_comission" : partner_month_comission,
        "partner_category": partner_category,
        'par_mob_no': par_mob_no,
        "data" : merchantBusinessesList,
        "bill_comission":bill_comission_to_show,
        'merchants_count': merchants_count,
        'overall_commision': overall_commision,
        "xdata1" :other_list,
        "xdata2" :sms_list,
        "xdata3" :digital_list,
        'ydata':merchant_name,
        'ComissionNavclass' : "active"
    }
    return render(request, "partner/comission/partner-comission.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def viewPartnerMonthlyCommision(request, id):
    f=0

    partner_object_id = PartnerProfile.objects.get(p_user = id)

    partner_object = partner_object_id.p_user


    print("***********")
    print(partner_object)
    print(f)
    commision_record = PartnerMonthlyCommision.objects.filter(p_mobile_no = partner_object).order_by('-id')
    print(commision_record)
    context = {
        "par_id" : id,
        "for_vyas" : "7020598727",
        "partner_object_id": partner_object_id,
        "commision_record" : commision_record,
        'partnerNavActiveClass': "active",
        'PartnerInfoCollapseShow': "show",
        'PartnerListNavclass': "active",

    }


    return render(request, "super_admin/view-partner-monthly-commision.html", context)

def viewMarketingPartnerMonthlyCommision(request, id):
    partner_object_id = PartnerProfile.objects.get(p_user = request.user)

    partner_object = partner_object_id.p_user

    commision_record = PartnerMonthlyCommision.objects.filter(p_mobile_no = partner_object).order_by('-id')

    context = {
        "par_id" : id,
        'partner_object_id': partner_object_id,
        "commision_record" : commision_record,
        'ComissionNavclass' : "active"

    }
    return render(request, "partner/comission/view-marketing-partner-monthly-commision.html", context)



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def send_partner_software_monthly_commision(request):
    if request.method == 'POST':
        user = request.POST['user']
        amount = request.POST['amount']
        payment_mode = request.POST['payment_mode']
        description = request.POST['description']
        bank_id = request.POST.get('bank_id')
        cheque_id = request.POST.get('cheque_id')
        merchant_business = ''
        partner_id = request.POST.get('partner_id')
        if not partner_id:
            partner_id = ''

        commission_id = request.POST.get('commission_id')
        par_id = request.POST.get('par_id')

        # print(user)

        result = SendPaymentManually.objects.create(business_id = merchant_business, partner_id = partner_id, bank_transaction_id = bank_id,
            cheque_id = cheque_id, payment_mode = payment_mode, description = description, amount = amount, payment_for = user)

        if payment_mode == 'Cash':
            transaction_id = 'Cash'

        elif payment_mode == 'Bank':
            transaction_id = 'Bank = ' + bank_id

        elif payment_mode == 'Cheque':
            transaction_id = 'Cheque = ' + cheque_id

        commision_record = PartnerMonthlyCommision.objects.filter(id = commission_id).update(status = 1)

        PartnerPaymentLinks.objects.create(partner_id = partner_id, payment_done = True, amount = amount, description = description,
            payment_date = timezone.now(), transaction_id = transaction_id)

        if result:
            sweetify.success(request, title="Success", icon='success',text='Payment sent Successfully.', timer=1500)
            return redirect(viewPartnerMonthlyCommision, id=par_id)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Something went Wrong.', timer=1500)
            return redirect(viewPartnerMonthlyCommision, id=par_id)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def viewSoftwarePartnerMonthlyCommision(request, id):

    partner_object_id = PartnerProfile.objects.get(p_user = id)

    partner_object = partner_object_id.p_user

    commision_record = PartnerMonthlyCommision.objects.filter(p_mobile_no = partner_object).order_by('-id')

    context = {
        "par_id" : id,
        "commision_record" : commision_record,
        'partnerNavActiveClass': "active",
        'PartnerInfoCollapseShow': "show",
        'PartnerSoftwareNavClass': "active",

    }
    return render(request, "super_admin/view-partner-monthly-commision.html", context)


def AddPartnerCommionStatus(request, id):
    commision_record = PartnerMonthlyCommision.objects.filter(id = id).update(status = 1)
    return JsonResponse({'success': True})



def all_merchant_subscription_plans(request):
    sms_subscription_plans = subscription_plan_details.objects.filter(is_active=True).order_by('-id')

    context = {
        # "total_merchant": total_merchant,
        # "merchant_inactive": merchant_inactive,
        # "merchant_active": merchant_active,
        # "count": count,
        "sms_subscription_plans": sms_subscription_plans,
        # "customized_subscription_plans": customized_subscription_plans,
        # "merchant_list" : merchant_list,
        "PartnerSubscriptionNavclass": 'active',
        "SimpleSubscriptionNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }
    return render(request,"partner/subscription/partner-subscription-plans.html",context)


def all_merchant_promotions_subscription_plan(request):
    all_promotions = promotional_subscription_plan_model.objects.filter(is_active=True).order_by('-id')

    context = {
        # "merchant_active": merchant_active,
        # "total_merchant": total_merchant,
        # "merchant_inactive": merchant_inactive,
        # "count": count,
        "all_promotions": all_promotions,
        "PartnerSubscriptionNavclass": 'active',
        "PromotionalSubscriptionNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }

    return render(request,"partner/subscription/partner-promotional-subscription-plans.html",context)



def all_merchant_transactional_subscription_plan(request):
    all_transactional = transactional_subscription_plan_model.objects.filter(is_active=True).order_by('-id')


    context = {
        "all_transactional":all_transactional,
        "PartnerSubscriptionNavclass": 'active',
        "TransactionalSubscriptionNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }

    return render(request,"partner/subscription/partner-transactional-subscription-plans.html",context)


def all_merchant_add_on_plan(request):
    all_add_on = add_on_plan_model.objects.filter(is_active=True).order_by('-id')


    context = {
        # "count": count,
        "all_add_on":all_add_on,
        "PartnerSubscriptionNavclass": 'active',
        "AddOnNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }
    return render(request, "partner/subscription/partner-adons-subscription-plans.html", context)



def get_add_on_plan_details_by_id(request, id):

    plan = add_on_plan_model.objects.get(id=id)

    context = {
        "plan_id": plan.id,
        "add_on_name": plan.add_on_name,
        "per_bill_cost": plan.per_bill_cost,
        "per_receipt_cost": plan.per_receipt_cost,
        "per_cash_memo_cost": plan.per_cash_memo_cost,
        "per_digital_bill_cost": plan.per_digital_bill_cost,
        "per_digital_receipt_cost":plan.per_digital_receipt_cost,
        "per_digital_cash_memo_cost":plan.per_digital_cash_memo_cost,
        "recharge_amount": plan.recharge_amount,
        "recharge_amount_one": plan.recharge_amount_one,
        "recharge_amount_two": plan.recharge_amount_two,
        "recharge_amount_three": plan.recharge_amount_three,
        "recharge_amount_four": plan.recharge_amount_four,
        "recharge_amount_five": plan.recharge_amount_five,
        "recharge_amount_six": plan.recharge_amount_six,
        "recharge_amount_seven": plan.recharge_amount_seven,
        "recharge_amount_eight": plan.recharge_amount_eight,
        "recharge_amount_nine": plan.recharge_amount_nine,
        "recharge_amount_ten": plan.recharge_amount_ten,
        "recharge_amount_eleven": plan.recharge_amount_eleven,
        "recharge_amount_twelve": plan.recharge_amount_twelve,
        "recharge_amount_thirteen": plan.recharge_amount_thirteen,
        "recharge_amount_fourteen": plan.recharge_amount_fourteen,
        "recharge_amount_fifteen": plan.recharge_amount_fifteen,
    }

    return JsonResponse({'status': 'success', 'plan': context})

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def StoreMerchantFromExcelFile(request):
    if request.method == "POST":
        filename = request.FILES['csv_file']
        result = csvfileupload.objects.create(csv_file = filename)
        loc = result.csv_file

        customer_bill_url = "http://157.230.228.250/media/" + str(loc)

        link = customer_bill_url

        file_name, headers = urllib.request.urlretrieve(link)
       
        wb = xlrd.open_workbook(file_name)

        sheet = wb.sheet_by_index(0)
 
        sheet.cell_value(0, 0)

        merchant_result = ""
         
        for index in range(1,5000):
            try:
                merchant_list = sheet.row_values(index)

                if merchant_list[0] and merchant_list[1] and merchant_list[2] and merchant_list[3] and merchant_list[4] and merchant_list[5] and merchant_list[6] and merchant_list[7] and merchant_list[8] and merchant_list[9]:

                    mobile_no = str(int(merchant_list[0]))
                    m_email = str(merchant_list[1])
                    merchant_by_partner = "By Partner"
                    m_business_name = str(merchant_list[2])
                    category_name = str(merchant_list[3])
                    m_pin_code = str(int(merchant_list[4]))
                    m_city = str(merchant_list[5]).capitalize()
                    m_district = str(merchant_list[6]).capitalize()
                    m_state = str(merchant_list[7]).capitalize()
                    m_area = str(merchant_list[8]).capitalize()
                    m_address = str(merchant_list[9])

                    is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no)

                    try:
                        m_business_category = business_category.objects.get(business_category_name = category_name).id
                    except:
                        try:
                            m_business_category = business_category.objects.get(business_category_name = "Others").id
                        except:
                            m_business_category = "" 

                    try:
                        merchant_business_category = business_category.objects.get(id = m_business_category)
                    except:
                        merchant_business_category = ''
                    

                    if not is_merchant:
                    # print(mobile_no,m_email,merchant_by_partner,m_business_name,category_name,m_pin_code,m_city,m_district,m_state,m_area)
                        temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

                        user_id = GreenBillUser.objects.create_user(
                            mobile_no = mobile_no,
                            m_email = m_email,
                            password = temp_password,
                        )

                        merchant_user = Merchant_users.objects.create(user_id = user_id, merchant_user_id = user_id)

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

                        letters = string.ascii_letters
                        digit = string.digits

                        random_string = str(user_id.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
            
                        GreenBillUser.objects.filter(mobile_no = user_id).update(is_merchant = 1, is_merchant_staff = 1, merchant_referral_code = random_string)

                        par_user_id = Partner_users.objects.get(user_id=request.user)

                        partner_object = par_user_id.partner_user_id

                        merchant_result = MerchantProfile.objects.create(m_user = user_id, m_business_name = m_business_name, by_partner =  merchant_by_partner, merchant_by_partner = par_user_id.partner_user_id,
                            m_business_category = merchant_business_category, m_city = m_city, m_district = m_district,
                            m_state = m_state, m_pin_code = m_pin_code, m_area= m_area, m_address = m_address,  m_disabled_account = False, m_latest_account=True, status=1, m_active_account = 1, m_unique_id=m_unique_id)

                        raw_password = temp_password
                        user = authenticate(mobile_no=mobile_no, password=raw_password)

                        subject = 'Thank You For Registration.'
                        message = f' Dear Valued Merchant, \n Warm Greetings from Green Bill Team!!! \n We are glad to see you chose Green Bill as {m_business_category} and below are your login credentials for the same \n URL: http://157.230.228.250/merchant-login/ \n Username: {mobile_no} \n Password: {raw_password} \n You are advised to login and complete your profile and business details for better coordination.'
                        email_from = settings.EMAIL_HOST_USER
                       
                        recipient_list = [user_id.m_email,]
                        
                        send_res = EmailMessage( subject, message, email_from, recipient_list)

                        response = send_res.send()
                    else:
                        pass
                else:
                    pass
            except:
                break

        if merchant_result:
            sweetify.success(request, title="Success", icon='success', text='Merchants Added Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='something went wrong.', timer=1000)

    return redirect("/partner-merchant-info/")
