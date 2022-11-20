# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import *
from .models import *

import random
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import get_connection, send_mail, BadHeaderError
from users.models import GreenBillUser, Merchant_users, MerchantUniqueIds, PartnerUniqueIds
from django.contrib import auth

from category_and_tags.models import business_category
import sweetify

import urllib
import uuid 

from super_admin_settings.models import notification_settings, GreenPointsEarnedHistory, GreenPointsSettings

from datetime import datetime
from django.utils import formats

import random
import string

from users.models import UserProfileImage

# SMS

import requests
import time
import pyshorteners


from green_points.models import *

from merchant_role.models import *

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.session.has_key('mobile_no') and request.session.has_key('password'):
        mobile_no = request.session['mobile_no']
        password = request.session['password']

        user = authenticate(mobile_no=mobile_no, password=password)

        is_superuser = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_superuser')[0]['is_superuser']

        is_staff = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_staff')[0]['is_staff']

        if user is not None and (is_superuser or is_staff):
            request.session['mobile_no'] = mobile_no
            request.session['password'] = password
            login(request, user)
            return redirect("/") 
        else:
            msg = ''

    if request.method == "POST":

        if form.is_valid():
            mobile_no = form.cleaned_data.get("mobile_no") 
            password = form.cleaned_data.get("password")
            user = authenticate(mobile_no=mobile_no, password=password)

            is_superuser = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_superuser')[0]['is_superuser']

            is_staff = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_staff')[0]['is_staff']

            if user is not None and (is_superuser or is_staff):
                if not form.cleaned_data.get('remember_me'):
                    request.session['mobile_no'] = mobile_no
                    request.session['password'] = password
                    login(request, user)
                    request.session.set_expiry(0)
                else:
                    request.session['mobile_no'] = mobile_no
                    request.session['password'] = password
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg" : msg, "DashboardNavclass": "active"})

def customer_login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    # customer_notification = notification_settings.objects.get(id = 3)

    # email = "ganesh.t@zappkode.com"

    # mobile_no = "7709977798"

    # if customer_notification.send_sms:
    #     import urllib
    #     username = "sanjog1"
    #     Password = "123456"
    #     sender = "HINDAG"

    #     import html2text
    #     text_maker = html2text.HTML2Text()
    #     text_maker.ignore_links = True
    #     text_maker.bypass_tables = False
    #     html = customer_notification.message
    #     text = text_maker.handle(html)

    #     temp_message = str(customer_notification.message)
    #     temp_dict = {"text": temp_message}
    #     message= urllib.parse.urlencode(temp_dict)
    #     priority='ndnd'
    #     stype='normal'
    

    #     var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""


    #     import requests

    #     url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

    # if customer_notification.send_email:
    #     subject = 'Thank You.'
    #     message = f'{customer_notification.message}'
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list = [email,]
    #     send_mail( subject, message, email_from, recipient_list, html_message = message)

    if request.session.has_key('mobile_no') and request.session.has_key('password'):
        mobile_no = request.session['mobile_no']
        password = request.session['password']

        user = authenticate(mobile_no=mobile_no, password=password)

        if user:
            is_customer = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_customer')[0]['is_customer']

        if user is not None and is_customer:
            request.session['mobile_no'] = mobile_no
            request.session['password'] = password
            login(request, user)
            return redirect("/customer-index/")
        else:
            msg = '' 

    if request.method == "POST":

        if form.is_valid():
            mobile_no = form.cleaned_data.get("mobile_no") 
            password = form.cleaned_data.get("password")
            user = authenticate(mobile_no=mobile_no, password=password)

            if user:
                is_customer = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_customer')[0]['is_customer']

            if user is not None and is_customer:
                if not form.cleaned_data.get('remember_me'):
                    request.session['mobile_no'] = mobile_no
                    request.session['password'] = password
                    login(request, user)
                    request.session.set_expiry(0)
                else:
                    request.session['mobile_no'] = mobile_no
                    request.session['password'] = password
                login(request, user)
                return redirect("/customer-index/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/customer-login.html", {"form": form, "msg" : msg, "DashboardNavclass": "active"})

def customer_register_view(request):
    

    msg     = None
    success = False

    if request.method == "POST":
        

        form = SignUpForm(request.POST)
        
        if form.is_valid():
            
            
            user_id = form.save()

            try:
                UserProfileImage.objects.filter(user_id = user_id.id)
            except:
                UserProfileImage.objects.create(user_id = user_id.id)
            
            GreenBillUser.objects.filter(mobile_no = user_id).update(is_customer = 1)

            unique_id = uuid.uuid4().hex[:6].upper()

            email = request.POST["email"]
            email_start_chars = email[0:3]

            mobile_no = request.POST["mobile_no"]
            mobile_no_end_chars = mobile_no[7:10]

            cust_state = request.POST["c_state"]

            c_state = cust_state.capitalize()

            cust_city = request.POST["c_city"]

            c_city = cust_city.capitalize()

            cust_area = request.POST["c_area"]

            c_area = cust_area.capitalize()

            checkout_pin = email_start_chars + mobile_no_end_chars

            is_exists = GreenBillUser.objects.filter(c_unique_id = checkout_pin.upper())

            if is_exists:
                mobile_no_end_chars = mobile_no[0:3]
                checkout_pin = email_start_chars + mobile_no_end_chars

            is_exists = GreenBillUser.objects.filter(c_unique_id = checkout_pin.upper())

            if is_exists:
                mobile_no_end_chars = mobile_no[4:7]
                checkout_pin = email_start_chars + mobile_no_end_chars

            letters = string.ascii_letters
            digit = string.digits

            random_string = str(user_id.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
            
            customer_referral_code = random_string[0:6]

            c_used_referral_code = request.POST['c_used_referral_code']
            
            GreenBillUser.objects.filter(mobile_no = user_id).update(c_state = c_state, c_city = c_city, c_area = c_area, c_unique_id = checkout_pin.upper(), customer_referral_code = customer_referral_code, c_used_referral_code = c_used_referral_code)

            try:
                customer_referral_object = GreenBillUser.objects.get(customer_referral_code = c_used_referral_code)
            except:
                customer_referral_object = ""

            green_points_settings_object = GreenPointsSettings.objects.get(id = 1)

            if customer_referral_object:

                GreenPointsEarnedHistory.objects.create(
                    mobile_no = customer_referral_object.mobile_no,
                    referent_mobile_no = user_id.mobile_no,
                    referral_mobile_no = customer_referral_object.mobile_no,
                    is_referral = True,
                    is_referent = False,
                    earned_green_points = green_points_settings_object.referral_points
                )

                try:
                    referral_green_points_object =  GreenPointsModel.objects.get(mobile_no = customer_referral_object.mobile_no)
                    green_points_count = referral_green_points_object.green_points_count
                    referral_green_points_id = referral_green_points_object.id
                except:
                    referral_green_points_object = ""
                    green_points_count = 0
                    referral_green_points_id = ""

                total_green_points = 0

                total_green_points = int(green_points_count) + int(green_points_settings_object.referral_points)

                GreenPointsModel.objects.update_or_create(id = referral_green_points_id, defaults={'green_points_count':total_green_points})

            if c_used_referral_code:

                GreenPointsEarnedHistory.objects.create(
                    mobile_no = user_id.mobile_no,
                    referent_mobile_no = user_id.mobile_no,
                    referral_mobile_no = customer_referral_object.mobile_no,
                    is_referral = False,
                    is_referent = True,
                    earned_green_points = green_points_settings_object.referral_points
                )

                try:
                    referent_green_points_object =  GreenPointsModel.objects.get(mobile_no = user_id.mobile_no)
                    referent_green_points_id = referent_green_points_object.id
                    green_points_count =  referent_green_points_object.green_points_count
                except:
                    referent_green_points_object = ""
                    referent_green_points_id = ""
                    green_points_count = 0

                total_green_points = 0

                total_green_points = int(green_points_count) + int(green_points_settings_object.referral_points)

                if referent_green_points_id != "":
                    GreenPointsModel.objects.filter(id = referent_green_points_id).update(green_points_count = total_green_points)
                else:
                    GreenPointsModel.objects.create(mobile_no = user_id.mobile_no, green_points_count = total_green_points)

            mobile_no = form.cleaned_data.get("mobile_no")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(mobile_no=mobile_no, password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True

            

            email = request.POST["email"]

            import requests
            import time

            notification_object = notification_settings.objects.get(id = 7)

            if notification_object.send_sms:

                ts = int(time.time())

                data_temp = {
                        "keyword":"New Customer Registration",
                        "timeStamp":ts,
                        "dataSet":
                            [
                                {
                                    "UNIQUE_ID":"GB-" + str(ts),
                                    "MESSAGE":"Thank you for registering on Green Bill. Welcome to the Green Bill Community. Feel free to get in touch with us at www.greenbill.in",
                                    "OA":"GBBILL",
                                    "MSISDN":str(mobile_no), # Recipient's Mobile Number
                                    "CHANNEL":"SMS",
                                    "CAMPAIGN_NAME":"hind_user",
                                    "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                    "USER_NAME":"hind_hsi",
                                    "DLT_TM_ID":"1001096933494158", # TM ID
                                    "DLT_CT_ID":"1007161821757152482", # Template Id
                                    "DLT_PE_ID":"1001659120000037015" # PE ID 
                                }
                            ]
                        }

                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                response = requests.post(url, json = data_temp)

            if notification_object.send_email:
                subject = 'New Customer Registration'
                message = f'Thank you for registering on Green Bill. Welcome to the Green Bill Community. Feel free to get in touch with us at www.greenbill.in'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email,]
                send_mail( subject, message, email_from, recipient_list)

            return JsonResponse({'status':'success'})
   
        else:
            if request.method == "POST":
                mobile_no = request.POST["mobile_no"]
                # print(mobile_no)
                email = request.POST["email"]
                c_pincode = request.POST["c_pin_code"]
                # c_dob = request.POST["c_dob"]
                # formatted_c_dob = datetime.strptime(c_dob, '%d-%m-%Y').strftime('%Y-%m-%d')
                cust_state = request.POST["c_state"]
                c_state = cust_state.capitalize()

                cust_city = request.POST["c_city"]
                c_city = cust_city.capitalize()

                cust_area = request.POST["c_area"]
                c_area = cust_area.capitalize()

                email_start_chars = email[0:3]

                mobile_no_end_chars = mobile_no[7:10]

                checkout_pin = email_start_chars + mobile_no_end_chars

                is_exists = GreenBillUser.objects.filter(c_unique_id = checkout_pin.upper())

                if is_exists:
                    mobile_no_end_chars = mobile_no[0:3]
                    checkout_pin = email_start_chars + mobile_no_end_chars

                is_exists = GreenBillUser.objects.filter(c_unique_id = checkout_pin.upper())

                if is_exists:
                    mobile_no_end_chars = mobile_no[4:7]
                    checkout_pin = email_start_chars + mobile_no_end_chars
                        
                GreenBillUser.objects.filter(mobile_no = mobile_no).update(email = email, c_pincode = c_pincode, c_state = c_state, c_city = c_city, c_area = c_area, is_customer = 1, c_unique_id=checkout_pin.upper())
            # print(form.errors, 'fail')

                return JsonResponse({'status':'success'})

    else:

        form = SignUpForm()
        States = StateCityData.objects.values('state').distinct().order_by('state')

    return render(request, "accounts/customer-register.html", {"form": form, "States": States, "msg" : msg, "success" : success })

def customer_logout_view(request):
    auth.logout(request)
    return redirect("/customer-login/")


def merchant_login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    print('new')
    print(request.session)

    # asd

    if request.session.has_key('mobile_no') and request.session.has_key('password'):
        mobile_no = request.session['mobile_no']
        password = request.session['password']

        user = authenticate(mobile_no=mobile_no, password=password)

        if user:
            is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
            
            is_merchant_staff = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant_staff')[0]['is_merchant_staff']

        if user is not None and (is_merchant or is_merchant_staff):
            request.session['mobile_no'] = mobile_no
            request.session['password'] = password
            login(request, user)
            return redirect("/merchant-index/")
        else:
            msg = '' 

    if request.method == "POST":
        
        if form.is_valid():
            mobile_no = form.cleaned_data.get("mobile_no") 
            password = form.cleaned_data.get("password")
            user = authenticate(mobile_no=mobile_no, password=password)

            if user:
                is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']

                is_merchant_staff = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant_staff')[0]['is_merchant_staff']

            if user is not None and (is_merchant or is_merchant_staff):
                if not form.cleaned_data.get('remember_me'):
                    request.session['mobile_no'] = mobile_no
                    request.session['password'] = password
                    login(request, user)
                    request.session.set_expiry(0)
                else:
                    request.session['mobile_no'] = mobile_no
                    request.session['password'] = password
                login(request, user)
                return redirect("/merchant-index/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/merchant-login.html", {"form": form, "msg" : msg, "DashboardNavclass": "active"})


def merchant_customer_switch_view(request):
    if request.session.has_key('mobile_no') and request.session.has_key('password'):
        password = request.session['password']
        if request.method == "POST": 
            password1 = request.POST.get("password")
            if password == password1 :
                sweetify.success(request, title="Success", icon='success', text='Switch Successfully.', timer=1000)
                return redirect("/customer-index/")
            else: 
                sweetify.success(request, title="Oops...", icon='error', text='Incorrect Password.', timer=1000)
                return redirect("/merchant-index/")   
    else:
        sweetify.success(request, title="Oops....", icon='error', text='Session error !!.', timer=1000)
        return redirect("/merchant-index/") 
    
def customer_merchant_switch_view(request):
    if request.session.has_key('mobile_no') and request.session.has_key('password'):
        password = request.session['password']
        if request.method == "POST": 
            password1 = request.POST.get("password")
            if password == password1 :
                sweetify.success(request, title="Success", icon='success', text='Switch Successfully.', timer=1000)
                return redirect("/merchant-index/")
            else: 
                sweetify.success(request, title="Oops...", icon='error', text='Incorrect Password.', timer=1000)
                return redirect("/customer-index/") 
    else:
        sweetify.success(request, title="Oops....", icon='error', text='Session error.', timer=1000)
        return redirect("/customer-index/") 


def merchant_register_view(request):

    msg     = None
    success = False

    qs = business_category.objects.all()

    context = {
        'business_category_list' : qs
    }

    if request.method == "POST":

        form = MerchantSignUpForm(request.POST)

        form1 = MerchantSignUpOtherDetailsForm(request.POST)
        
        if form.is_valid() and form1.is_valid():
            
            user_id = form.save()

            UserProfileImage.objects.create(user_id = user_id.id)

            letters = string.ascii_letters
            digit = string.digits

            m_used_referral_code = request.POST['m_used_referral_code']

            

            random_string = str(user_id.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
            
            GreenBillUser.objects.filter(mobile_no = user_id).update(is_merchant = 1, merchant_referral_code = random_string[0:6], m_used_referral_code = m_used_referral_code)

            # try:
            #     referral_merchant_id = GreenBillUser.objects.get(merchant_referral_code=m_used_referral_code)
            #     merchant_profile_obj = merchant_profile.objects.get('')
            # except:
            #     pass

            GreenBillUser.objects.filter(mobile_no = user_id).update(is_merchant_staff = 1)

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
            
            merchant_user = Merchant_users.objects.create(user_id = user_id, merchant_user_id = user_id)

            m_email = form.cleaned_data.get("m_email")



            if m_email:
            	random_string = str(user_id.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(5))
            	email_verification_status = GreenBillUser.objects.filter(mobile_no = user_id).update(email_verification_url = random_string)
            	s = pyshorteners.Shortener()
            	email_verification_url = "http://157.230.228.250/email-verification/"+str(random_string)+"/"
            	short_url = s.tinyurl.short(email_verification_url)
            	if email_verification_status and short_url:
            		subject = 'Account Verification'
            		message = f'Thank you for choosing GreenBill. Please click on below link to verify Email Id,\n' + str(short_url) + '\n\nTeam GreenBill'
            		email_from = settings.EMAIL_HOST_USER
            		recipient_list = [m_email,]
            		send_mail( subject, message, email_from, recipient_list)

            m_business_name = form1.cleaned_data.get("m_business_name")
            m_business_category = form1.cleaned_data.get("m_business_category")
            # print('m_business_category',m_business_category)
            merchant_city = form1.cleaned_data.get("m_city")
            merchant_area = form1.cleaned_data.get("m_area")
            merchant_district = form1.cleaned_data.get("m_district")
            merchant_state = form1.cleaned_data.get("m_state")
            m_pin_code = form1.cleaned_data.get("m_pin_code")

            m_state = merchant_state.capitalize()

            m_city = merchant_city.capitalize()

            m_area = merchant_area.capitalize()

            m_district = merchant_district.capitalize()

            merchant_profile_id = MerchantProfile.objects.create(m_user = user_id, m_business_name = m_business_name, m_business_category = m_business_category, m_city = m_city, m_area= m_area, m_district = m_district, m_state = m_state, m_pin_code = m_pin_code, m_active_account = 1, m_unique_id = m_unique_id)

            role_name1 = 'Admin'

            role_name2 = 'Exe User'

            role_name3 = 'Operator'

            

            if merchant_profile_id.m_business_category.id != 11 and merchant_profile_id.m_business_category.id != 12:
                merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name1)

                merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name2)

            if merchant_profile_id.m_business_category.id == 11 or merchant_profile_id.m_business_category.id == 12:
                merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name1)

                merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name3)

            mobile_no = form.cleaned_data.get("mobile_no")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(mobile_no=mobile_no, password=raw_password)

            msg     = 'Congratulations on becoming Green Bill Merchant!!! - please <a href="/login">login</a>.'
            success = True

            notification_object = notification_settings.objects.get(id = 6)

            if notification_object.send_sms:

                if m_business_category.id == 11:

                    ts = int(time.time())

                    data_temp = {
                            "keyword":"New Merchant Registration",
                            "timeStamp":ts,
                            "dataSet":
                                [
                                    {
                                        "UNIQUE_ID":"GB-" + str(ts),
                                        "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
                                        "OA":"GBPUMP",
                                        "MSISDN":mobile_no, # Recipient's Mobile Number
                                        "CHANNEL":"SMS",
                                        "CAMPAIGN_NAME":"hind_user",
                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                        "USER_NAME":"hind_hsi",
                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                        "DLT_CT_ID":"1007162098316946419", # Template Id
                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                    }
                                ]
                            }

                    url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                    response = requests.post(url, json = data_temp)

                elif m_business_category.id == 12:

                    ts = int(time.time())

                    data_temp = {
                            "keyword":"New Merchant Registration",
                            "timeStamp":ts,
                            "dataSet":
                                [
                                    {
                                        "UNIQUE_ID":"GB-" + str(ts),
                                        "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
                                        "OA":"GBPARK",
                                        "MSISDN":mobile_no, # Recipient's Mobile Number
                                        "CHANNEL":"SMS",
                                        "CAMPAIGN_NAME":"hind_user",
                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                        "USER_NAME":"hind_hsi",
                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                        "DLT_CT_ID":"1007162098316946419", # Template Id
                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                    }
                                ]
                            }

                    url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                    response = requests.post(url, json = data_temp)

                else:



                    ts = int(time.time())

                    data_temp = {
                            "keyword":"New Merchant Registration",
                            "timeStamp":ts,
                            "dataSet":
                                [
                                    {
                                        "UNIQUE_ID":"GB-" + str(ts),
                                        "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
                                        "OA":"GBBILL",
                                        "MSISDN":mobile_no, # Recipient's Mobile Number
                                        "CHANNEL":"SMS",
                                        "CAMPAIGN_NAME":"hind_user",
                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                        "USER_NAME":"hind_hsi",
                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                        "DLT_CT_ID":"1007162098316946419", # Template Id
                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                    }
                                ]
                            }

                    url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                    response = requests.post(url, json = data_temp)

            if notification_object.send_email:
                subject = 'New Merchant Registration'
                message = f'Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [m_email,]
                send_mail( subject, message, email_from, recipient_list)

            return JsonResponse({'status':'success'})

        else:
            mobile_no = request.POST['mobile_no']

            # is_customer = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_customer')[0]['is_customer']
            is_customer = GreenBillUser.objects.filter(mobile_no=mobile_no)
            print("**********************************************************")
            # print(is_customer)
            # print(list(is_customer))

            # if list(is_customer) :
            if len(list(is_customer))>0:
                m_email = request.POST['m_email']
                m_business_name = request.POST['m_business_name']
                m_business_category = request.POST['m_business_category']
                m_pin_code = request.POST['m_pin_code']
                # m_city = request.POST['m_city']
                # m_area = request.POST['m_area']
                # m_state = request.POST['m_state']
                # m_district = request.POST['m_district']
                m_pin_code = request.POST['m_pin_code']


                merchant_state = request.POST['m_state']
                m_state = merchant_state.capitalize()

                merchant_city = request.POST['m_city']
                m_city = merchant_city.capitalize()

                merchant_area = request.POST['m_area']
                m_area = merchant_area.capitalize()

                merchant_district = request.POST['m_district']
                m_district = merchant_district.capitalize()

                letters = string.ascii_letters
                digit = string.digits

                try:
                    merchant_business_category = business_category.objects.get(id = m_business_category)
                except:
                    merchant_business_category = ''

                # print('merchant_business_category',merchant_business_category)

                try:
                    m_used_referral_code = request.POST['m_used_referral_code']
                except:
                    m_used_referral_code = ''

                user_id = GreenBillUser.objects.get(mobile_no = mobile_no)

                # print('user_id',user_id)

                GreenBillUser.objects.filter(mobile_no = mobile_no).update(is_merchant_staff = 1)
                
                random_string = str(user_id.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                GreenBillUser.objects.filter(mobile_no = mobile_no).update(is_merchant = 1, merchant_referral_code = random_string[0:6], m_used_referral_code = m_used_referral_code)

                

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

                unique_id_status = GreenBillUser.objects.filter(mobile_no = mobile_no).update(m_unique_id = m_unique_id)

                if unique_id_status:
                    MerchantUniqueIds.objects.create(m_unique_no = no)

                try:

                    merchant_user = Merchant_users.objects.create(user_id = user_id, merchant_user_id = user_id)
                except:
                    ''

                if m_email:
                    random_string = ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(5))
                    email_verification_status = GreenBillUser.objects.filter(mobile_no = mobile_no).update(email_verification_url = random_string)
                    s = pyshorteners.Shortener()
                    email_verification_url = "http://157.230.228.250/email-verification/"+str(random_string)+"/"
                    short_url = s.tinyurl.short(email_verification_url)
                    if email_verification_status and short_url:
                        subject = 'Account Verification'
                        message = f'Thank you for choosing GreenBill. Please click on below link to verify Email Id,\n' + str(short_url) + '\n\nTeam GreenBill'
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [m_email,]
                        send_mail( subject, message, email_from, recipient_list)

                merchant_profile_id = MerchantProfile.objects.create(m_user = user_id, m_business_name = m_business_name, m_business_category = merchant_business_category, m_city = m_city, m_area= m_area, m_district = m_district, m_state = m_state, m_pin_code = m_pin_code, m_active_account = 1, m_unique_id = m_unique_id)

                role_name1 = 'Admin'

                role_name2 = 'Exe User'

                merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name1)

                merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name2)

                raw_password = request.POST['password1']

                user = authenticate(mobile_no=mobile_no, password=raw_password)

                msg = 'Congratulations on becoming Green Bill Merchant!!! - please <a href="/login">login</a>.'
                success = True

                notification_object = notification_settings.objects.get(id = 6)

                if notification_object.send_sms:

                    if merchant_business_category == 11:

                        ts = int(time.time())

                        data_temp = {
                                "keyword":"New Merchant Registration",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
                                            "OA":"GBPUMP",
                                            "MSISDN":mobile_no, # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098316946419", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                        response = requests.post(url, json = data_temp)

                    elif merchant_business_category == 12:

                        ts = int(time.time())

                        data_temp = {
                                "keyword":"New Merchant Registration",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
                                            "OA":"GBPARK",
                                            "MSISDN":mobile_no, # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098316946419", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                        response = requests.post(url, json = data_temp)

                    else:



                        ts = int(time.time())

                        data_temp = {
                                "keyword":"New Merchant Registration",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
                                            "OA":"GBBILL",
                                            "MSISDN":mobile_no, # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098316946419", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                        response = requests.post(url, json = data_temp)

                if notification_object.send_email:
                    subject = 'New Merchant Registration'
                    message = f'Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [m_email,]
                    send_mail( subject, message, email_from, recipient_list)

                return JsonResponse({'status':'success'})
            else:
                print("User not registered !!!!!!")
                m_email = request.POST['m_email']
                m_business_name = request.POST['m_business_name']
                m_business_category = request.POST['m_business_category']
                m_pin_code = request.POST['m_pin_code']
                # m_city = request.POST['m_city']
                # m_area = request.POST['m_area']
                # m_state = request.POST['m_state']
                # m_district = request.POST['m_district']
                m_pin_code = request.POST['m_pin_code']

                
                merchant_state = request.POST['m_state']
                m_state = merchant_state.capitalize()

                merchant_city = request.POST['m_city']
                m_city = merchant_city.capitalize()

                merchant_area = request.POST['m_area']
                m_area = merchant_area.capitalize()

                merchant_district = request.POST['m_district']
                m_district = merchant_district.capitalize()

                # mobile_no = request.POST['mobile_no']

                raw_password = request.POST['password1']
                raw_password2 = request.POST['password2']
                print("Printing variables ")
                print(m_email,m_business_category,m_business_name)

                # try: 
                # if raw_password==raw_password2:
                #     print("****************************************************")
                #     print("Password Successfully Validated")
                # else:
                #     print("Different Password !!!!!")
                
                

                letters = string.ascii_letters
                digit = string.digits


                # try:
                user_id = GreenBillUser.objects.create_user(
                        mobile_no = mobile_no,
                        m_email = m_email,
                        password = raw_password,
                    )
                # print("^^^^^^^^^^^^^^^^^^^^^Printing user id of created user !!!!!!")
                # print(user_id)
                # except:
                #     print("****************************************************")
                #     print("Error creating user !!!")
                #     return JsonResponse({'error':'user not created !!!'})

                try:
                    merchant_business_category = business_category.objects.get(id = m_business_category)
                except:
                    merchant_business_category = ''

                # print('merchant_business_category',merchant_business_category)

                try:
                    m_used_referral_code = request.POST['m_used_referral_code']
                except:
                    m_used_referral_code = ''

                user_id = GreenBillUser.objects.get(mobile_no = mobile_no)

                # print('user_id',user_id)

                GreenBillUser.objects.filter(mobile_no = mobile_no).update(is_merchant_staff = 1)
                
                random_string = str(user_id.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                GreenBillUser.objects.filter(mobile_no = mobile_no).update(is_merchant = 1, merchant_referral_code = random_string[0:6], m_used_referral_code = m_used_referral_code)

                

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

                unique_id_status = GreenBillUser.objects.filter(mobile_no = mobile_no).update(m_unique_id = m_unique_id)

                if unique_id_status:
                    MerchantUniqueIds.objects.create(m_unique_no = no)

                try:

                    merchant_user = Merchant_users.objects.create(user_id = user_id, merchant_user_id = user_id)
                except:
                    ''

                if m_email:
                    random_string = ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(5))
                    email_verification_status = GreenBillUser.objects.filter(mobile_no = mobile_no).update(email_verification_url = random_string)
                    s = pyshorteners.Shortener()
                    email_verification_url = "http://157.230.228.250/email-verification/"+str(random_string)+"/"
                    short_url = s.tinyurl.short(email_verification_url)
                    if email_verification_status and short_url:
                        subject = 'Account Verification'
                        message = f'Thank you for choosing GreenBill. Please click on below link to verify Email Id,\n' + str(short_url) + '\n\nTeam GreenBill'
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [m_email,]
                        send_mail( subject, message, email_from, recipient_list)

                merchant_profile_id = MerchantProfile.objects.create(m_user = user_id, m_business_name = m_business_name, m_business_category = merchant_business_category, m_city = m_city, m_area= m_area, m_district = m_district, m_state = m_state, m_pin_code = m_pin_code, m_active_account = 1, m_unique_id = m_unique_id)

                role_name1 = 'Admin'

                role_name2 = 'Exe User'

                merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name1)

                merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name2)

                # raw_password = request.POST['password1']

                user = authenticate(mobile_no=mobile_no, password=raw_password)

                msg = 'Congratulations on becoming Green Bill Merchant!!! - please <a href="/login">login</a>.'
                success = True

                notification_object = notification_settings.objects.get(id = 6)

                if notification_object.send_sms:

                    if merchant_business_category == 11:

                        ts = int(time.time())

                        data_temp = {
                                "keyword":"New Merchant Registration",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
                                            "OA":"GBPUMP",
                                            "MSISDN":mobile_no, # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098316946419", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                        response = requests.post(url, json = data_temp)

                    elif merchant_business_category == 12:

                        ts = int(time.time())

                        data_temp = {
                                "keyword":"New Merchant Registration",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
                                            "OA":"GBPARK",
                                            "MSISDN":mobile_no, # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098316946419", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                        response = requests.post(url, json = data_temp)

                    else:



                        ts = int(time.time())

                        data_temp = {
                                "keyword":"New Merchant Registration",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
                                            "OA":"GBBILL",
                                            "MSISDN":mobile_no, # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098316946419", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                        response = requests.post(url, json = data_temp)

                if notification_object.send_email:
                    subject = 'New Merchant Registration'
                    message = f'Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [m_email,]
                    send_mail( subject, message, email_from, recipient_list)

                return JsonResponse({'status':'success'})
                # return JsonResponse({'status':'error'})
            
    else:
        
        form = MerchantSignUpForm()

        form1 = MerchantSignUpOtherDetailsForm()

        States = StateCityData.objects.values('state').distinct().order_by('state')

    return render(request, "accounts/merchant-register.html", { "form": form, "States": States, "form1": form1, "msg" : msg, "success" : success, "context" : context })

def merchant_logout_view(request):
    auth.logout(request)
    return JsonResponse({'status':'success'})
    # return redirect(merchant_login_view)

def software_partner_login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.session.has_key('mobile_no') and request.session.has_key('password'):
        mobile_no = request.session['mobile_no']
        password = request.session['password']

        user = authenticate(mobile_no=mobile_no, password=password)

        if user:
            is_software_partner = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_partner')[0]['is_partner']

        if user is not None and is_software_partner:
            request.session['mobile_no'] = mobile_no
            request.session['password'] = password
            login(request, user)
            return redirect("/partner-index/")
        else:
            msg = '' 

    if request.method == "POST":

        if form.is_valid():
            mobile_no = form.cleaned_data.get("mobile_no") 
            password = form.cleaned_data.get("password")
            user = authenticate(mobile_no=mobile_no, password=password)

            if user:
                is_software_partner = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_partner')[0]['is_partner']

            if user is not None and is_software_partner:
                if not form.cleaned_data.get('remember_me'):
                    request.session['mobile_no'] = mobile_no
                    request.session['password'] = password
                    login(request, user)
                    request.session.set_expiry(0)
                else:
                    request.session['mobile_no'] = mobile_no
                    request.session['password'] = password
                login(request, user)
                return redirect("/partner-index/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/software_partner-login.html", {"form": form, "msg" : msg, "DashboardNavclass": "active"})

def software_partner_register_view(request):

    msg     = None
    success = False

    if request.method == "POST":

        form = SoftwarePartnerSignUpForm(request.POST)

        form1 = SoftwarePartnerOtherDetailsForm(request.POST)

        
        
        if form.is_valid() and form1.is_valid():
            
            user_id = form.save()

            UserProfileImage.objects.create(user_id = user_id.id)
            
            GreenBillUser.objects.filter(mobile_no = user_id).update(is_partner = 1)

            p_email = form1.cleaned_data.get("p_email")
            p_business_name = form1.cleaned_data.get("p_business_name")
            p_business_category = form1.cleaned_data.get("p_business_category")
            p_city = form1.cleaned_data.get("p_city")
            p_district = form1.cleaned_data.get("p_district")
            p_state = form1.cleaned_data.get("p_state")
            p_pin_code = form1.cleaned_data.get("p_pin_code")

            PartnerProfile.objects.create(p_user = user_id, p_business_name = p_business_name, p_business_category = p_business_category, p_city = p_city, p_district = p_district, p_state = p_state, p_pin_code = p_pin_code)

            mobile_no = form.cleaned_data.get("mobile_no")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(mobile_no=mobile_no, password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True

            partner_notification = notification_settings.objects.get(id = 4)

            if partner_notification.send_sms:
                import urllib
                username = "sanjog1"
                Password = "123456"
                sender = "HINDAG"

                import html2text
                text_maker = html2text.HTML2Text()
                text_maker.ignore_links = True
                text_maker.bypass_tables = False
                html = customer_notification.message
                text = text_maker.handle(html)
               
                
                temp_message = str(customer_notification.message)
                temp_dict = {"text": temp_message}
                message= urllib.parse.urlencode(temp_dict)
                priority='ndnd'
                stype='normal'
                
                

                var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                

                import requests

                url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                

            if partner_notification.send_email:
                subject = 'Thank You.'
                message = f'{customer_notification.message}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [p_email,]
                send_mail( subject, message, email_from, recipient_list, html_message = message)
            
            #return redirect("/login/")

            return JsonResponse({'status':'success'})

        else:
            
            return JsonResponse({'status':'error'})
            
    else:
        form = SoftwarePartnerSignUpForm()

        form1 = SoftwarePartnerOtherDetailsForm()

    return render(request, "accounts/software_partner-register.html", {"form": form, "form1": form1, "msg" : msg, "success" : success })

def partner_logout_view(request):
    auth.logout(request)
    return JsonResponse({'status':'success'})

def generate_otp(request):
    mobile_no = request.POST['mobile_no']
    email = request.POST['email']
    if mobile_no:
        otp = random.randint(99999, 999999)
        otp_validation.objects.update_or_create(mobile_no = mobile_no, defaults={'otp': otp})

        ts = int(time.time())

        sms_data_temp = {
                "keyword":"Web New Registration OTP",
                "timeStamp":ts,
                "dataSet":
                    [
                        {
                            "UNIQUE_ID":"GB-" + str(ts),
                            "MESSAGE":"Dear Green Bill user, Use " + str(otp) + " as OTP for your registration.",
                            "OA":"GRBILL",
                            "MSISDN":str(mobile_no), # Recipient's Mobile Number
                            "CHANNEL":"SMS",
                            "CAMPAIGN_NAME":"hind_user",
                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                            "USER_NAME":"hind_hsi",
                            "DLT_TM_ID":"1001096933494158", # TM ID
                            "DLT_CT_ID":"1007162098351638761", # Template Id
                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                        }
                    ]
                }

        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

        response = requests.post(url, json = sms_data_temp)

        if response.status_code == 200:
            return JsonResponse({'status':'success', 'mobile_no' : mobile_no, 'email' : email})
        else:
            return JsonResponse({'status' : 'error', 'msg': "Failed to send otp"})

        
    else:
        return JsonResponse({'status':'error'})

def generate_otp_merchant(request):
    mobile_no = request.POST['mobile_no']
    email = request.POST['m_email']

    if mobile_no:
        otp = random.randint(99999, 999999)
        otp_validation.objects.update_or_create(mobile_no = mobile_no, defaults={'otp': otp})

        # subject = 'welcome to Green Bill'
        # message = f'Please use this OTP: {otp}'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [email,] 
        # send_mail( subject, message, email_from, recipient_list)

        ts = int(time.time())

        sms_data_temp = {
                "keyword":"Web New Registration OTP",
                "timeStamp":ts,
                "dataSet":
                    [
                        {
                            "UNIQUE_ID":"GB-" + str(ts),
                            "MESSAGE":"Dear Green Bill user, Use " + str(otp) + " as OTP for your registration.",
                            "OA":"GRBILL",
                            "MSISDN":str(mobile_no), # Recipient's Mobile Number
                            "CHANNEL":"SMS",
                            "CAMPAIGN_NAME":"hind_user",
                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                            "USER_NAME":"hind_hsi",
                            "DLT_TM_ID":"1001096933494158", # TM ID
                            "DLT_CT_ID":"1007162098351638761", # Template Id
                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                        }
                    ]
                }

        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

        response = requests.post(url, json = sms_data_temp)

        if response.status_code == 200:
            return JsonResponse({'status':'success', 'mobile_no' : mobile_no, 'm_email' : email})
        else:
            return JsonResponse({'status' : 'error', 'msg': "Failed to send otp"})

    else:
        return JsonResponse({'status':'error'})

def generate_otp_partner(request):
    mobile_no = request.POST['mobile_no']
    email = request.POST['p_email']

    if mobile_no:
        otp = random.randint(99999, 999999)
        otp_validation.objects.update_or_create(mobile_no = mobile_no, defaults={'otp': otp})

        # subject = 'welcome to Green Bill'
        # message = f'Please use this OTP: {otp}'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [email,] 
        # send_mail( subject, message, email_from, recipient_list)

        ts = int(time.time())

        sms_data_temp = {
                "keyword":"Web New Registration OTP",
                "timeStamp":ts,
                "dataSet":
                    [
                        {
                            "UNIQUE_ID":"GB-" + str(ts),
                            "MESSAGE":"Dear Green Bill user, Use " + str(otp) + " as OTP for your registration.",
                            "OA":"GRBILL",
                            "MSISDN":str(mobile_no), # Recipient's Mobile Number
                            "CHANNEL":"SMS",
                            "CAMPAIGN_NAME":"hind_user",
                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                            "USER_NAME":"hind_hsi",
                            "DLT_TM_ID":"1001096933494158", # TM ID
                            "DLT_CT_ID":"1007162098351638761", # Template Id
                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                        }
                    ]
                }

        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

        response = requests.post(url, json = sms_data_temp)

        if response.status_code == 200:
            return JsonResponse({'status':'success', 'mobile_no' : mobile_no, 'p_email' : email})
        else:
            return JsonResponse({'status' : 'error', 'msg': "Failed to send otp"})

    else:
        return JsonResponse({'status':'error'})


# def validate_mobile_no_view(request):

#     mobile_no = request.POST['mobile_no']

#     try:
#         user_object = GreenBillUser.objects.filter(mobile_no = mobile_no)

#     except:
#         user_object = ''
#     print('owner',user_object[0].is_staff)
#     print()

#     if user_object:
#         if user_object[0].is_staff and request.POST["validating_for"] != "owner":
#             msg = 'Mobile number is already registered as Owner or Owner Staff. So please Use Owner Web Panel.'
#             return JsonResponse({'status':'fail', 'msg': msg})
#         elif (user_object[0].is_merchant or user_object[0].is_merchant_staff) and request.POST["validating_for"] != "merchant":
#             msg = 'Mobile number is already registered as Merchant or Merchant user. So please Use Merchant Web Panel.'
#             return JsonResponse({'status':'fail', 'msg': msg})
#         elif user_object[0].is_partner and request.POST["validating_for"] != "partner":
#             msg = 'Mobile number is already registered as Partner. So please Use Partner Web Panel.'
#             return JsonResponse({'status':'fail', 'msg': msg})
#         elif user_object[0].is_customer and request.POST["validating_for"] != "customer":

#             # msg = 'Mobile Number is already registered as Customer. So please Use Customer Web Panel.'
#             # return JsonResponse({'status':'fail', 'msg': msg})
#             return JsonResponse({'status':'success'})
        
        
#         else:
#             msg = 'Mobile number is already Used. Please try with other mobile number.'
#             return JsonResponse({'status':'fail', 'msg': msg})
#     else:
#         return JsonResponse({'status':'success'})
def validate_mobile_no_view(request):

    mobile_no = request.POST['mobile_no']

    try:
        user_object = GreenBillUser.objects.filter(mobile_no = mobile_no)

    except:
        user_object = ''

    if user_object:
        if user_object[0].is_staff and request.POST["validating_for"] != "owner":
            msg = 'Mobile number is already registered as Owner or Owner Staff. So please Use Owner Web Panel.'
            return JsonResponse({'status':'fail', 'msg': msg})
        elif user_object[0].is_partner and request.POST["validating_for"] != "partner":
            msg = 'Mobile number is already registered as Partner. So please Use Partner Web Panel.'
            return JsonResponse({'status':'fail', 'msg': msg})
        elif (user_object[0].is_merchant or user_object[0].is_merchant_staff) and request.POST["validating_for"] != "merchant":
            msg = 'Mobile number is already registered as Merchant or Merchant user. So please Use Merchant Web Panel.'
            return JsonResponse({'status':'fail', 'msg': msg})
        elif (user_object[0].is_merchant and user_object[0].is_merchant_staff):
            msg = 'Mobile number is already registered as Merchant or Merchant user. So please Use Merchant Web Panel.'
            return JsonResponse({'status':'fail', 'msg': msg})
        elif user_object[0].is_customer and request.POST["validating_for"] != "customer":
            return JsonResponse({'status':'success'})
            
        else:
            msg = 'Mobile number is already Used. Please try with other mobile number.'
            return JsonResponse({'status':'fail', 'msg': msg})
    else:
        return JsonResponse({'status':'success'})

def customer_validate_mobile_no(request):
    mobile_no = request.POST['mobile_no']
    try:
        user_object = GreenBillUser.objects.filter(mobile_no = mobile_no)
        is_customer = user_object[0].is_customer

    except:
        is_customer = ''
        user_object = ''
    if user_object:
        if user_object[0].is_staff and request.POST["validating_for"] != "owner":
            if is_customer:
                msg = 'Mobile number is already registered as Owner or Owner Staff. So please Use Owner Web Panel.'
                return JsonResponse({'status':'fail', 'msg': msg})
            else:
                return JsonResponse({'status':'success'})
        elif user_object[0].is_customer and request.POST["validating_for"] != "customer":
            msg = 'Mobile Number is already registered as Customer. So please Use Customer Web Panel.'
            return JsonResponse({'status':'fail', 'msg': msg})
        elif user_object[0].is_partner and request.POST["validating_for"] != "partner":
            if is_customer:
                msg = 'Mobile number is already registered as Partner. So please Use Partner Web Panel.'
                return JsonResponse({'status':'fail', 'msg': msg})
            else:
                return JsonResponse({'status':'success'})

        elif (user_object[0].is_merchant or user_object[0].is_merchant_staff) and request.POST["validating_for"] != "merchant":
            if is_customer:
                msg = 'Mobile number is already registered as Merchant or Merchant user. So please Use Merchant Web Panel.'
                return JsonResponse({'status':'fail', 'msg': msg})
            else:
                return JsonResponse({'status':'success'})
        else:
            if is_customer:
                msg = 'Mobile number is already Used. Please try with other mobile number.'
                return JsonResponse({'status':'fail', 'msg': msg})
            else:
                return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'success'})


def register_otp_validation_view(request):
    
    if request.method == "POST":
        otp_temp = request.POST['otp']
        mobile_no = request.POST['mobile_no']

        otp = otp_validation.objects.filter(mobile_no=mobile_no).values('otp')[0]['otp']
        
        if otp == otp_temp:
            return JsonResponse({ 'status' : 'success', 'mobile_no' : mobile_no })
        else:
            return JsonResponse({ 'status' : 'error'})


def become_customer(request):
    if request.method == "POST":
        email = request.POST["email"]
        c_pincode = request.POST["c_pin_code"]
        c_dob = request.POST["c_dob"]
        formatted_c_dob = datetime.strptime(c_dob, '%d-%m-%Y').strftime('%Y-%m-%d')
        c_state = request.POST["c_state"]
        c_city = request.POST["c_city"]
        c_area = request.POST["c_area"]

        mobile_no = request.user.mobile_no

        email_start_chars = email[0:3]

        mobile_no_end_chars = mobile_no[7:10]

        checkout_pin = email_start_chars + mobile_no_end_chars

        is_exists = GreenBillUser.objects.filter(c_unique_id = checkout_pin.upper())

        if is_exists:
            mobile_no_end_chars = mobile_no[0:3]
            checkout_pin = email_start_chars + mobile_no_end_chars

        is_exists = GreenBillUser.objects.filter(c_unique_id = checkout_pin.upper())

        if is_exists:
            mobile_no_end_chars = mobile_no[4:7]
            checkout_pin = email_start_chars + mobile_no_end_chars
                
        GreenBillUser.objects.filter(mobile_no = request.user.mobile_no).update(email = email, c_pincode = c_pincode, c_dob = formatted_c_dob, c_state = c_state, c_city = c_city, c_area = c_area, is_customer = 1, c_unique_id=checkout_pin.upper())

        return JsonResponse({'status':'success'})
    
    else:
        return JsonResponse({'status':'error'})

def become_merchant(request):
    if request.method == "POST":

        m_email = request.POST["m_email"]

        letters = string.ascii_letters
        digit = string.digits

        random_string = str(request.user.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
        
        GreenBillUser.objects.filter(mobile_no = request.user).update(is_merchant = 1, merchant_referral_code = random_string[0:6], m_email = m_email)

        GreenBillUser.objects.filter(mobile_no = request.user).update(is_merchant_staff = 1)

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

       	unique_id_status = GreenBillUser.objects.filter(mobile_no = request.user.mobile_no).update(m_unique_id = m_unique_id)

       	if unique_id_status:
       		MerchantUniqueIds.objects.create(m_unique_no = no)

       	# Unique Id End

       	# Email Verification Start

       	if m_email:
       		random_string = str(request.user.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(5))
       		email_verification_status = GreenBillUser.objects.filter(mobile_no = request.user).update(email_verification_url = random_string)
       		s = pyshorteners.Shortener()
       		email_verification_url = "http://157.230.228.250/email-verification/"+str(random_string)+"/"
       		short_url = s.tinyurl.short(email_verification_url)
       		if email_verification_status and short_url:
       			subject = 'Account Verification'
       			message = f'Thank you for choosing GreenBill. Please click on below link to verify Email Id,\n' + str(short_url) + '\n\nTeam GreenBill'
       			email_from = settings.EMAIL_HOST_USER
       			recipient_list = [m_email,]
       			send_mail( subject, message, email_from, recipient_list)

		# Email Verification End
        
        Merchant_users.objects.create(user_id = request.user, merchant_user_id = request.user)

        m_business_name = request.POST["m_business_name"]
        m_business_category_temp = request.POST["m_business_category"]
        m_city = request.POST["m_city"]
        m_area = request.POST["m_area"]
        m_district = request.POST["m_district"]
        m_state = request.POST["m_state"]
        m_pin_code = request.POST["m_pin_code"]

        m_business_category = business_category.objects.get(id = m_business_category_temp)

        MerchantProfile.objects.create(m_user = request.user, m_business_name = m_business_name, m_business_category = m_business_category, m_city = m_city, m_area= m_area, m_district = m_district, m_state = m_state, m_pin_code = m_pin_code, m_active_account = 1)

        return JsonResponse({'status':'success'})
    
    else:
        return JsonResponse({'status':'error'})


def merchant_validate_referral_code_view(request):

    m_referral_code = request.POST['m_used_referral_code']
    
    if m_referral_code:

        try:
            user_object = GreenBillUser.objects.filter(merchant_referral_code = m_referral_code)
        except:
            user_object = ''

        if user_object:
            return JsonResponse({'status':'success'})
            
        else:
            msg = 'Invalid Referral Code !!!'
            return JsonResponse({'status':'fail', 'msg': msg})

    else:
        return JsonResponse({'status':'success'})


def customer_validate_referral_code_view(request):

    c_referral_code = request.POST['c_used_referral_code']
    
    if c_referral_code:

        try:
            user_object = GreenBillUser.objects.filter(customer_referral_code = c_referral_code)
        except:
            user_object = ''

        if user_object:
            return JsonResponse({'status':'success'})
            
        else:
            msg = 'Invalid Referral Code !!!'
            return JsonResponse({'status':'fail', 'msg': msg})

    else:
        return JsonResponse({'status':'success'})


def email_verification_view(request, id):
	try:
		user_object = GreenBillUser.objects.get(email_verification_url = id, is_verified_email = False)
		if user_object:
			GreenBillUser.objects.filter(mobile_no = user_object.mobile_no).update(is_verified_email = True)
			return render(request, "accounts/email-verification.html")
		else:
			return render(request, 'page-404.html')
	except:
		return render(request, 'page-404.html')





