
from rest_framework import generics
import random
import os
import hashlib
from cryptography.fernet import Fernet
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from owner_notice_board.sendsms import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token  # To generate the token
from rest_framework import viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from users.models import GreenBillUser, UserProfileImage, MerchantProfile, Merchant_users, MerchantUniqueIds

from merchant_apis.serializers import *
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, timedelta
from django.utils import formats
from authentication.models import *
from merchant_stamp.models import *
from owner_stamp.models import *
from django.conf import settings
from django.core.mail import send_mail
from category_and_tags.models import business_category
from bill_design.models import authorised_sign
from offers.models import OfferModel
from referral_points.models import *
from coupon.models import *

import base64
from django.core.files.base import ContentFile
import calendar

import json
from django.core import serializers
from django.db.models import Sum

from merchant_enquiry.models import *
from merchant_software_apis.models import *
from parking_lot_apis.models import *
from petrol_pump_apis.models import *
from customer_info.models import *

import random
import string
from bill_design.models import *

from merchant_role.models import *
from users.models import *

from merchant_setting.models import *
from merchant_promotion.models import *

from datetime import date

from suggest.models import *

# SMS
import requests
import time
import pyshorteners

from share_a_word.models import *

from suggest_a_brand.models import *

from feedback.models import *

from merchant_cashmemo_design.models import Cash_Memo_Design_Model, CustomerCashMemoDetailModels, CustomerReceiptDetailsModels,save_template_for_cashmemo,save_template_for_receipt

from supports_faq.models import *


from coupon.models import CouponModel

from offers.models import *

from merchant_payment.models import *

from merchant_setting.models import MerchantPaymentSetting

from my_subscription.models import *

from django.db.models import Q

from subscription_plan.models import *

from super_admin_settings.models import notification_settings

from merchant_software_apis.models import DeviceId, MerchantBill
import socket
from pyfcm import FCMNotification
import inflect
from merchant_software_apis.models import DeviceId
import socket
from pyfcm import FCMNotification

from payments.models import *

from django.utils import timezone

from owner_notice_board.models import *
from merchant_notice.models import *
from merchant_software_apis.models import ExePrintStatus
from referral_points.models import *
from promotions.models import *
from bill_design.models import *


@csrf_exempt
def merchantcarddetails(request):
    try:
        if request.method == "POST":
            id = request.POST["user_id"]
            print(id)


            user_object = GreenBillUser.objects.get(mobile_no = id)
            print(user_object)

            merchant_user = Merchant_users.objects.get(user_id = user_object)
            print(merchant_user)

            merchant_object = merchant_user.merchant_user_id
            print(merchant_object)

            merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
            print(merchant_business_id)

            contact_object  = contact_card.objects.get(merchant_business_id = merchant_business_id)
            print(contact_object)
            
            

            context = {
                "data":contact_object
            }
            print(type(context))
            # print(context["data"])
            serializer = MerchantContactCardSerializer(contact_object)
            print(serializer.data)
            return JsonResponse({'status': 'success', 'message': "Data Recived",'data':serializer.data}, status=200)
    except:
        print("in expect")
        return JsonResponse({'status': 'Error', 'message': "Failed to get Data !!!"}, status=400)


@csrf_exempt
def merchantcard(request):
    if request.method == "POST" :
        contact_check = []
        social_media_check = []

        doc = request.FILES
        email_card = request.POST["email_card"]
        first_name =  request.POST["first_name"]
        city = request.POST["city"]
        country =  request.POST["country"]
        description = request.POST["description"]

        about = request.POST["about_us"]
        alternate_mobile = request.POST["alternate_mobile"]
        bussiness_time = request.POST["buss_time"]
        
        background = request.FILES.get("background_pic",False)
        cover = request.FILES.get("cover_pic",False)
        file_pic = request.FILES.get("profile_pic")
        # gallery1 = request.FILES.get("Gallery1",False)
        # gallery2 = request.FILES.get("Gallery2",False)
        # gallery3 = request.FILES.get("Gallery3",False)
        temp_choice = request.POST.get("template_check",False)
        # video_url = request.POST["youtube_video_url"]
        
        mobile_no = request.POST["mobile_no"]

        facebook = request.POST["facebook"]
        youtube = request.POST["youtube"]
        phone = request.POST["phone"]
        website = request.POST["website"]
        email = request.POST["email_link"]
        msg = request.POST["msg"]
        whatsapp = request.POST["whatsapp"]
        addtocontact = request.POST["addtocontact"]
        map = request.POST["map"]

        print("**")
        
        account_holder_name = request.POST['account_holder_name']
        account_no = request.POST['account_no']
        ifsc_Code = request.POST['ifsc_Code']
        bank_name = request.POST['bank_name']
        pan_card = request.POST['pan_card']
        gstin_number = request.POST['gstin_number']


        if facebook=="true":
            social_media_check.append("facebook")
        if youtube=="true":
            social_media_check.append("youtube")
        if phone=="true":
            contact_check.append("phone")
        if website=="true":
            contact_check.append("website")
        if map=="true":
            contact_check.append("map")

        if email=="true":
            social_media_check.append("email")
        if msg=="true":
            contact_check.append("msg")
        if whatsapp=="true":
            contact_check.append("whatsapp")
        if addtocontact=="true":
            contact_check.append("addtocontact")
        

        

        print("************************************")

        print(social_media_check)
        if "facebook" in social_media_check:
            facebook_status = True
            facebook_url = request.POST["facebook_url"]
        else:
            facebook_status = False
            facebook_url = ""

        if "youtube" in social_media_check:
            youtube_status = True
            youtube_url = request.POST["youtube_url"]
        else:
            youtube_status = False
            youtube_url = ""

        if "email" in social_media_check:
            email_status = True
            email_url = request.POST["email_url"]
        else:
            email_status = False
            email_url = ""

        print(facebook_url,youtube_url)
       

        print("************************************")

        print(contact_check)

        if "phone" in contact_check:
            phone_status = True
            phone_number = request.POST["phone_number"]
        else:
            phone_status = False
            phone_number = ""

        if "website" in contact_check:
            website_status = True
            website_url = request.POST["website_url"]
        else:
            website_status = False
            website_url = ""
        
        if "map" in contact_check:
            map_status = True
            map_link = request.POST["map_link"]
        else:
            map_status = False
            map_link = ""
        if "whatsapp" in contact_check:
            whatsapp_status = True
            whatsapp_number = request.POST["whatsapp_url"]
        else:
            whatsapp_status = False
            whatsapp_number = ""

        if "addtobook" in contact_check:
            addtobook_status = True
            addtobook_url = request.POST["addtobook_url"]
        else:
            addtobook_status = False
            addtobook_url = ""
        
        if "msg" in contact_check:
            msg_status = True
            msg_link = request.POST["msg_link"]
        else:
            msg_status = False
            msg_link = ""

        print(phone_number,website_url,map_link)
      

       
        print("*")
        print(mobile_no)

        user_object = GreenBillUser.objects.get(mobile_no = mobile_no)
        print(user_object) 

        merchant_user = Merchant_users.objects.get(user_id = user_object)
        print(merchant_user)  

        merchant_object = merchant_user.merchant_user_id        
        print(merchant_object)  

        merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
        print(merchant_business_id)

        # merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
        # result = ''

        try:
            obj = contact_card.objects.filter(merchant_business_id = merchant_business_id)[0]
        except:
            obj =False
        
        if obj and background:
            obj.background_photo = background
            obj.save()

        if obj and cover:
            obj.cover_photo = cover
            obj.save()

        if obj and file_pic:
            obj.card_photo = file_pic 
            obj.save()

        if len(social_media_check) == 0 or len(social_media_check) <= 4:
            result = contact_card.objects.update_or_create(merchant_business_id = merchant_business_id, defaults={ 
                "card_desc":description,"card_city":city,"card_country":country,"card_email":email_card,"card_phone_no":mobile_no,"card_name":first_name,
                 "facebook" : facebook_status, "facebook_url" : facebook_url, "youtube" : youtube_status, "youtube_url" : youtube_url,
                  "phone" : phone_status, "phone_number" : phone_number, "website" : website_status, 
                   "website_url" : website_url, "map" : map_status, "map_link" : map_link,"msg":msg_status,
                   "msg_number":msg_link,"whatsapp":whatsapp_status,"whatsapp_number":whatsapp_number,"address_book":addtobook_status,"address_book_number":addtobook_url,"email":email_status,"email_url":email_url,
                   "alternate_mobile":alternate_mobile,
                   "bussiness_time":bussiness_time,"about_us":about,"temp_choice":temp_choice,"card_desc":description,"acco_holder_name":account_holder_name,"acc_no":account_no,"ifsc_code":ifsc_Code,"bank_name":bank_name,"gstin_no":gstin_number,"pan_card":pan_card})
        else:
            result = contact_card.objects.update_or_create(merchant_business_id = merchant_business_id, defaults={  "phone" : phone_status, "phone_number" : phone_number, "website" : website_status, 
               "website_url" : website_url, "map" : map_status, "map_link" : map_link, })


        
        if result:
            return JsonResponse({'status': 'success', 'message': "Card Details Set Successfully !!!"}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to set !!!"}, status=400)


    # elif request.method == "POST":
        
    #     contact_check = []
    #     social_media_check = []



    #     email = request.POST["email"]
    #     first_name =  request.POST["first_name"]
    #     city = request.POST["city"]
    #     country =  request.POST["country"]
    #     description = request.POST["description"]
    #     mobile_no = request.POST["mobile_no"]
    #     # file_pic = request.FILES["profile_pic"]


    #     facebook = request.POST["facebook"]
    #     youtube = request.POST["youtube"]
    #     phone = request.POST["phone"]
    #     website = request.POST["website"]
    #     map = request.POST["map"]
    #     print("**")
    #     print(facebook,youtube,map,phone)
    #     if facebook=="true":
    #         social_media_check.append("facebook")
    #     if youtube=="true":
    #         social_media_check.append("youtube")
    #     if phone=="true":
    #         contact_check.append("phone")
    #     if website=="true":
    #         contact_check.append("website")
    #     if map=="true":
    #         contact_check.append("map")


    #     # social_media_check = request.POST.getlist("social_media_check")

    #     print("************************************")

    #     print(social_media_check)
    #     if "facebook" in social_media_check:
    #         facebook_status = True
    #         facebook_url = request.POST["facebook_url"]
    #     else:
    #         facebook_status = False
    #         facebook_url = ""

    #     if "youtube" in social_media_check:
    #         youtube_status = True
    #         youtube_url = request.POST["youtube_url"]
    #     else:
    #         youtube_status = False
    #         youtube_url = ""

    #     print(facebook_url,youtube_url)
    #     # contact_check =  request.POST.getlist("contact_check")

    #     print("************************************")

    #     print(contact_check)

    #     if "phone" in contact_check:
    #         phone_status = True
    #         phone_number = request.POST["phone_number"]
    #     else:
    #         phone_status = False
    #         phone_number = ""

    #     if "website" in contact_check:
    #         website_status = True
    #         website_url = request.POST["website_url"]
    #     else:
    #         website_status = False
    #         website_url = ""
        
    #     if "map" in contact_check:
    #         map_status = True
    #         map_link = request.POST["map_link"]
    #     else:
    #         map_status = False
    #         map_link = ""

    #     print(phone_number,website_url,map_link)
    #     # merchant_user_object = Merchant_users.objects.get(user_id = mobile_no)

    #     # merchant_object = merchant_user_object.merchant_user_id

    #     # mobile_no =  request.user.mobile_no
    #     print("*")
    #     print(mobile_no)

    #     user_object = GreenBillUser.objects.get(mobile_no = mobile_no)
    #     print(user_object) 
        
    #     merchant_user = Merchant_users.objects.get(user_id = user_object)
    #     print(merchant_user)  

    #     merchant_object = merchant_user.merchant_user_id        
    #     print(merchant_object)  

    #     merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
    #     print(merchant_business_id)

    #     # merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
    #     result = ''

    #     if len(social_media_check) == 0 or len(social_media_check) <= 4:
    #         result = contact_card.objects.update_or_create(merchant_business_id = merchant_business_id, defaults={ 
    #             "card_desc":description,"card_city":city,"card_country":country,"card_email":email,"card_phone_no":mobile_no,"card_name":first_name,
    #              "facebook" : facebook_status, "facebook_url" : facebook_url, "youtube" : youtube_status, "youtube_url" : youtube_url,
    #               "phone" : phone_status, "phone_number" : phone_number, "website" : website_status, 
    #                "website_url" : website_url, "map" : map_status, "map_link" : map_link,})
    #     else:
    #         result = contact_card.objects.update_or_create(merchant_business_id = merchant_business_id, defaults={  "phone" : phone_status, "phone_number" : phone_number, "website" : website_status, 
    #            "website_url" : website_url, "map" : map_status, "map_link" : map_link, })

        

        # if result:
        #     return JsonResponse({'status': 'Success', 'message': "Card Details Set Successfully !!!"}, status=200)
        # else:
        #     return JsonResponse({'status': 'error', 'message': "Failed to set !!!"}, status=400)

    return JsonResponse({'status': 'error', 'message': "Something went wrong !!!"}, status=400)


@csrf_exempt
def merchantLogin(request):

    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        password = request.POST['password']

        try:

            if GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']:

                user = authenticate(mobile_no=mobile_no, password=password)

                if user:
                    is_merchant = GreenBillUser.objects.filter(
                        mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
                    serializer = merchantSerializer(user)

                    try:
                        token = Token.objects.create(user=user)
                    except:
                        token = Token.objects.get(user_id=user.id)

                    if user is not None and is_merchant:
                        return JsonResponse({'status': 'success', 'token': token.key, 'data': serializer.data}, status=200)
                    else:
                        return JsonResponse({'status': 'error', 'message': "Something went wrong !!!"}, status=400)
                else:
                    return JsonResponse({'status': 'error', 'message': "Invalid credentials !!!"}, status=400)

            else:
                return JsonResponse({'status': 'error', 'message': "User not register !!!"}, status=400)
        except:
            return JsonResponse({'status': 'error', 'message': "User not register !!!"}, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': "Something went wrong !!!"}, status=400)


class merchantChangePassword(generics.GenericAPIView):
    serializer_class = merchantSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST['user_id']

        user = GreenBillUser.objects.get(id=user_id)

        old_password = request.POST['old_password']

        success = GreenBillUser.check_password(user, old_password)

        if success == True:
            new_password = request.POST['new_password']

            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)  # Important!

            return JsonResponse({'status': 'success', 'message': "Password changed successfully !!!"}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed, old password not matched !!!"}, status=400)


@csrf_exempt
def getMerchantBusinessCategory(request):
    if request.method == "GET":
        business_categories = business_category.objects.all()
        serializer = BusinessCategorySerializer(business_categories, many=True)
        # return JsonResponse({'status' : 'success', 'data' : serializer.data}, status=200)
        # return Response(serializer.data)
        return JsonResponse(serializer.data, status=200, safe=False)
    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)

@csrf_exempt
def validateMerchantMobileNumber(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']

        try:
            user_object = GreenBillUser.objects.filter(mobile_no = mobile_no)

        except:
            user_object = ''

        if user_object:
            if user_object[0].is_staff:
                return JsonResponse({'status':'error', 'message': "Mobile number already registered."}, status=400)

            elif user_object[0].is_partner:
                return JsonResponse({'status':'error', 'message': "Mobile number already registered."}, status=400)

            elif (user_object[0].is_merchant or user_object[0].is_merchant_staff):
                return JsonResponse({'status':'error', 'message': "Mobile number already registered."}, status=400)

            elif user_object[0].is_customer:
                return JsonResponse({'status':'success', 'message': "Mobile number not registered."}, status=200)
                
            else:
                return JsonResponse({'status':'error', 'message': "Mobile number already registered."}, status=400)
        else:
            return JsonResponse({'status':'success', 'message': "Mobile number not registered."}, status=200)

        # try:
        #     is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
        # except:
        #     is_merchant = ""

        # if is_merchant:
        #     return JsonResponse({'status':'error', 'message': "Mobile number already registered."}, status=400)
        # else:
        #     return JsonResponse({'status':'success', 'message': "Mobile number not registered."}, status=200)
    else:
        return JsonResponse({'status':'error', 'message': "Something went wrong."}, status=400)
        

@csrf_exempt
def generateOtpMerchnat(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        signature = request.POST['signature']
        # email = request.POST['m_email']

        try:
            is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
        except:
            is_merchant = ""

        if is_merchant:
            return JsonResponse({'status':'error', 'message': "Mobile number exists as merchant."}, status=400)
        else:
            if mobile_no:
                otp = random.randint(99999, 999999)
                otp_validation.objects.update_or_create(
                    mobile_no=mobile_no, defaults={'otp': otp})

                # subject = 'welcome to Green Bill'
                # message = f'Please use this OTP: {otp}'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [email,]
                # send_mail( subject, message, email_from, recipient_list)

                ts = int(time.time())

                sms_data_temp = {
                        "keyword":"App New Registration OTP",
                        "timeStamp":ts,
                        "dataSet":
                            [
                                {
                                    "UNIQUE_ID":"GB-" + str(ts),
                                    "MESSAGE":"<"+"#"+"> "+"Dear Green Bill user, use " + str(otp) + " as OTP for your registration." + str(signature),
                                    "OA":"GRBILL",
                                    "MSISDN":str(mobile_no), # Recipient's Mobile Number
                                    "CHANNEL":"SMS",
                                    "CAMPAIGN_NAME":"hind_user",
                                    "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                    "USER_NAME":"hind_hsi",
                                    "DLT_TM_ID":"1001096933494158", # TM ID
                                    "DLT_CT_ID":"1007162106850723917", # Template Id
                                    "DLT_PE_ID":"1001659120000037015" # PE ID 
                                }
                            ]
                        }

                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                response = requests.post(url, json = sms_data_temp)

                if response.status_code == 200:
                    return JsonResponse({'status': 'success'}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': "Failed to send otp !!!"}, status=400)
            else:
                return JsonResponse({'status': 'error'}, status=403)
        # elif mobile_exists[0].is_customer:
        #     return JsonResponse({'status':'error', 'message': "Mobile Number is registered as Customer. So please Use Customer Web Panel OR Customer App!!!"}, status=400)
        # elif mobile_exists[0].is_merchant or mobile_exists[0].is_merchant_staff:
        #     return JsonResponse({'status':'error', 'message': "Mobile Number is registered as Merchant or Merchant user. So please Use Merchant Web Panel OR Merchant App!!!"}, status=400)
        # elif mobile_exists[0].is_partner:
        #     return JsonResponse({'status':'error', 'message': "Mobile Number is registered as Partner. So please Use Partner Web Panel.!!!"}, status=400)
        # elif mobile_exists[0].is_staff:
        #     return JsonResponse({'status':'error', 'message': "Mobile Number is registered as Owner or Owner Staff. So please Use Owner Web Panel.!!!"}, status=400)
        # else:
        #     return JsonResponse({'status':'error', 'message': "Customer Exists, Please use different Mobile Number !!!"}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


@csrf_exempt
def generateOtpMerchantForgotPassword(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        signature = request.POST['signature']

        try:
            if mobile_no:
                mobile_exists = GreenBillUser.objects.get(mobile_no=mobile_no)
                is_merchant = GreenBillUser.objects.filter(
                    mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
                email = GreenBillUser.objects.filter(
                    mobile_no=mobile_no).values('m_email')[0]['m_email']
                if mobile_exists and is_merchant:
                    otp = random.randint(99999, 999999)
                    otp_validation.objects.update_or_create(
                        mobile_no=mobile_no, defaults={'otp': otp})

                    # subject = 'welcome to Green Bill'
                    # message = f'Please use this OTP: {otp}'
                    # email_from = settings.EMAIL_HOST_USER
                    # recipient_list = [email,]
                    # mail_res = send_mail( subject, message, email_from, recipient_list )
                    # print(mail_res)

                    ts = int(time.time())

                    sms_data_temp = {
                            "keyword":"App Forgot Password OTP",
                            "timeStamp":ts,
                            "dataSet":
                                [
                                    {
                                        "UNIQUE_ID":"GB-" + str(ts),
                                        "MESSAGE":"<"+"#"+"> "+"Dear Green Bill user, use " + str(otp) + " as OTP to reset your password. " + str(signature),
                                        "OA":"GRBILL",
                                        "MSISDN":str(mobile_no), # Recipient's Mobile Number
                                        "CHANNEL":"SMS",
                                        "CAMPAIGN_NAME":"hind_user",
                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                        "USER_NAME":"hind_hsi",
                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                        "DLT_CT_ID":"1007162107620813728", # Template Id
                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                    }
                                ]
                            }

                    url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                    response = requests.post(url, json = sms_data_temp)

                    if response.status_code == 200:
                        return JsonResponse({'status': 'success'}, status=200)
                    else:
                        return JsonResponse({'status': 'error', 'message': "Failed to send otp !!!"}, status=400)
                else:
                    return JsonResponse({'status': 'error', 'message': 'User not registered'}, status=400)
            else:
                return JsonResponse({'status': 'error'}, status=403)
        except:
            return JsonResponse({'status': 'error', 'message': 'User not registered'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


@csrf_exempt
def otpValidateMerchant(request):
    if request.method == "POST":
        temp_otp = request.POST['otp']
        mobile_no = request.POST['mobile_no']
        otp = otp_validation.objects.filter(
            mobile_no=mobile_no).values('otp')[0]['otp']

        if otp == temp_otp:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid otp'}, status=406)

    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


@csrf_exempt
def ReferralCodeValidateMerchant(request):
    if request.method == "POST":
        m_used_referral_code = request.POST['m_used_referral_code']

        try:
            result = GreenBillUser.objects.get(merchant_referral_code = m_used_referral_code)
        except:
            result = ""

        if result:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid Referral Code !!!'}, status=406)


@csrf_exempt
def merchantRegister(request):

    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        password = request.POST['password']

        exists = GreenBillUser.objects.filter(mobile_no=mobile_no)

        if exists:
            is_customer = GreenBillUser.objects.filter(
                mobile_no=mobile_no).values('is_customer')[0]['is_customer']
        else:
            is_customer = False

        if is_customer == True:

            user = GreenBillUser.objects.get(mobile_no=mobile_no)

            m_email = request.POST['m_email']
            is_merchant = 1
            is_active = 1
            is_merchant_staff = 1

            letters = string.ascii_letters
            digit = string.digits

            random_string = str(user.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

            try:
                m_used_referral_code = request.POST['m_used_referral_code']
            except:
                m_used_referral_code = ""

            GreenBillUser.objects.filter(id=user.id).update(
                m_email=m_email, is_merchant=is_merchant, is_merchant_staff = is_merchant_staff, is_active=is_active, merchant_referral_code = random_string[0:6], m_used_referral_code = m_used_referral_code)
            
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

            unique_id_status = GreenBillUser.objects.filter(mobile_no = user).update(m_unique_id = m_unique_id)

            if unique_id_status:
                MerchantUniqueIds.objects.create(m_unique_no = no)

            # Unique Id End

            # Email Verification Start

            if m_email:
                random_string = str(user.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(5))
                email_verification_status = GreenBillUser.objects.filter(mobile_no = user).update(email_verification_url = random_string)
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

            merchant_user = Merchant_users.objects.create(user_id=user, merchant_user_id=user)

            m_business_name = request.POST["m_business_name"]
            m_business_category_id = request.POST["m_business_category"]
            m_city = request.POST["m_city"]
            m_district = request.POST["m_district"]
            m_state = request.POST["m_state"]
            m_pin_code = request.POST["m_pin_code"]
            m_area = request.POST['m_area']

            try:
                m_used_referral_code = request.POST['m_used_referral_code']
            except:
                m_used_referral_code = ""

            m_business_category = business_category.objects.get(
                id=m_business_category_id)

            # MerchantProfile.objects.create(m_user=user, m_business_name=m_business_name, m_business_category=m_business_category,
            #                                m_city=m_city, m_area=m_area, m_district=m_district, m_state=m_state, m_pin_code=m_pin_code, m_active_account=1)

            
            merchant_profile_id = MerchantProfile.objects.create(m_user=user, m_business_name=m_business_name, m_business_category=m_business_category, m_city=m_city, m_area=m_area, m_district=m_district, m_state=m_state, m_pin_code=m_pin_code, m_active_account=1)

            role_name1 = 'Admin'

            role_name2 = 'Exe User'

            merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name1)

            merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name2)




            newUser = GreenBillUser.objects.get(id=user.id)

            temp = newUser.set_password(password)
            temp2 = newUser.save()

            update_session_auth_hash(request, user)

            notification_object = notification_settings.objects.get(id = 6)

            if notification_object.send_sms:

                if m_business_category_id == "11":

                    ts = int(time.time())

                    data_temp = {
                            "keyword":"Welcome Message",
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

                elif m_business_category_id == "12":

                    ts = int(time.time())

                    data_temp = {
                            "keyword":"Welcome Message",
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
                            "keyword":"Welcome Message",
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

            if notification_object.send_app_notification:
                device = DeviceId.objects.filter(mobile_no=mobile_no).first()
                push_service = FCMNotification(api_key=settings.API_KEY)

                if device != None:
                    registration_id = device.device_id
                else:
                    registration_id = ""

                message_title = "New Merchant Registration"
                message_body = "HThank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login."
                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)


            return JsonResponse({'status': 'success', 'message': 'User created successfully !!!'}, status=200)

        elif is_customer == False:

            serializer = merchantSerializer_register(data=request.POST)

            # print(serializer)

            if serializer.is_valid():

                user = serializer.save()

                user.set_password(request.POST["password"])
                user.save()

                letters = string.ascii_letters
                digit = string.digits

                random_string = str(user.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                try:
                    m_used_referral_code = request.POST['m_used_referral_code']
                except:
                    m_used_referral_code = ""

                GreenBillUser.objects.filter(id=user.id).update(merchant_referral_code = random_string[0:6], m_used_referral_code = m_used_referral_code, is_merchant_staff = True, is_merchant = True)

                m_email = request.POST['m_email']

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

                unique_id_status = GreenBillUser.objects.filter(mobile_no = user).update(m_unique_id = m_unique_id)

                if unique_id_status:
                    MerchantUniqueIds.objects.create(m_unique_no = no)

                # Unique Id End

                # Email Verification Start

                if m_email:
                    random_string = str(user.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(5))
                    email_verification_status = GreenBillUser.objects.filter(mobile_no = user).update(email_verification_url = random_string)
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

                merchant_user = Merchant_users.objects.create(user_id=user, merchant_user_id=user)

                m_business_name = request.POST["m_business_name"]
                m_business_category_id = request.POST["m_business_category"]
                m_city = request.POST["m_city"]
                m_district = request.POST["m_district"]
                m_state = request.POST["m_state"]
                m_pin_code = request.POST["m_pin_code"]
                m_area = request.POST['m_area']
                

                m_business_category = business_category.objects.get(
                    id=m_business_category_id)

                merchant_profile_id = MerchantProfile.objects.create(m_user=user, m_business_name=m_business_name, m_business_category=m_business_category, m_city=m_city, m_area=m_area, m_district=m_district, m_state=m_state, m_pin_code=m_pin_code, m_active_account=1)

                role_name1 = 'Admin'
                role_name2 = 'Exe User'
                role_name3 = 'Operator'

                if merchant_profile_id.m_business_category.id != 11 and merchant_profile_id.m_business_category.id != 12:
                    merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name1)

                    merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name2)

                if merchant_profile_id.m_business_category.id == 11 or merchant_profile_id.m_business_category.id == 12:
                    merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name1)

                    merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name3)



                notification_object = notification_settings.objects.get(id = 6)

                if notification_object.send_sms:

                    if m_business_category_id == "11":

                        ts = int(time.time())

                        data_temp = {
                                "keyword":"Welcome Message",
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

                    elif m_business_category_id == "12":

                        ts = int(time.time())

                        data_temp = {
                                "keyword":"Welcome Message",
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
                                "keyword":"Welcome Message",
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

                if notification_object.send_app_notification:
                    device = DeviceId.objects.filter(mobile_no=mobile_no).first()
                    push_service = FCMNotification(api_key=settings.API_KEY)

                    if device != None:
                        registration_id = device.device_id
                    else:
                        registration_id = ""

                    message_title = "New Merchant Registration"
                    message_body = "HThank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login."
                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

                return JsonResponse({'status': 'success', 'message': 'User created successfully !!!'},
                                    status=200)

            else:
                return JsonResponse({'status': 'error', 'message': serializer.errors}, status=400)

        else:
            return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


@csrf_exempt
def forgotPasswordMerchant(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        new_password = request.POST['new_password']

        result = GreenBillUser.objects.filter(mobile_no=mobile_no).values('id')[0]['id']
        user = GreenBillUser.objects.get(id=result)
        success = GreenBillUser.check_password(user, new_password)

        if success == True:
            return JsonResponse({'status': 'error', 'message': 'New Password cannot be same as Old Password !!!'}, status=400)
            
        else:
            if result:
                
                user.set_password(new_password)
                user.save()

                update_session_auth_hash(request, user)  # Important!

                return JsonResponse({'status': 'success', 'message': 'Password changed successfully !!!'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'User not found !!!'}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Something went wrong, please try again later !!!'}, status=400)


# def base64_file(data, name=None):
#     _format, _img_str = data.split(';base64,')
#     _name, ext = _format.split('/')
#     if not name:
#         name = _name.split(":")[-1]
#     return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))


class setMerchantProfileData(generics.GenericAPIView):
    serializer_class = merchantSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            user_id = request.POST['user_id']
            m_email = request.POST["m_email"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            
            m_dob = request.POST.get("m_dob",None) 

            if m_dob is not None and m_dob != '' and m_dob != "":
                formatted_m_dob = datetime.strptime(m_dob, '%d-%m-%Y').strftime('%Y-%m-%d')
            else:
                formatted_m_dob = None


            m_designation = request.POST["m_designation"]
            m_adhaar_number = request.POST["m_adhaar_number"]
            m_pan_number = request.POST["m_pan_number"]
            # m_profile_image = request.FILES["m_profile_image"]

            # m_business_name = request.POST["m_business_name"]
            # # m_business_category = request.POST["m_pan_number"]
            # m_area = request.POST["m_area"]
            # m_city = request.POST["m_city"]
            # m_district = request.POST["m_district"]
            # m_state = request.POST["m_state"]
            # m_pin_code = request.POST["m_pin_code"]

            # MerchantProfile.objects.update_or_create(m_user = request.user, defaults={ "m_business_name" : m_business_name, "m_city" : m_city, "m_area" : m_area, "m_district" : m_district, "m_state" : m_state, "m_pin_code" : m_pin_code, "m_active_account" : 1})

            # print(m_profile_image)

            profile = GreenBillUser.objects.filter(id=user_id).update(m_email=m_email, first_name=first_name, last_name=last_name,
                m_dob=formatted_m_dob, m_designation=m_designation, m_adhaar_number=m_adhaar_number, m_pan_number=m_pan_number)

            # if m_profile_image:

            #     #random_no = random.randint(9999999, 999999999)

            #     #m_profile_image = base64_file(data=m_profile_image_temp, name="profile_image"+str(random_no))

            #     image = UserProfileImage.objects.update_or_create(user_id = user_id, defaults={
            #     "m_profile_image" : m_profile_image })

            if profile:
                return JsonResponse({'status': 'success', 'message': "Profile edited successfully !!!"}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)

        else:
            return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


class getMerchantProfileImage(generics.GenericAPIView):

    serializer_class = merchantSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            user_id = request.POST['user_id']
            b_id = request.POST['b_id']

            if user_id:
                user = GreenBillUser.objects.get(id=user_id)

                # userDetails = UserProfileImage.objects.filter(user=user_id)
                try:
                    userDetails = MerchantProfile.objects.get(id=b_id)
                except:
                    userDetails = ""
                base_url = "http://157.230.228.250/"

                if user:
                    if userDetails:
                        try:
                            new_dic = {
                                'mobile_no': user.mobile_no,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'profile_image': str(base_url) + str(userDetails.m_business_logo.url)
                            }
                        except:
                            new_dic = {
                                'mobile_no': user.mobile_no,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'profile_image': str(base_url) + str("/media/user-profile-pic.png")
                            }
                    else:

                        new_dic = {
                            'mobile_no': user.mobile_no,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'profile_image': str(base_url) + str("/media/user-profile-pic.png")
                        }
                    return JsonResponse({'status': "success", 'data': new_dic}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "User not found"}, status=400)
            else:
                return JsonResponse({'status': "error", 'message': "User id is mandatory."}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "Something went wrong."}, status=400)


class setMerchantProfileImage(generics.GenericAPIView):

    serializer_class = merchantSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            user_id = request.POST['user_id']
            m_profile_image = request.FILES["m_profile_image"]

            if user_id and m_profile_image:

                #random_no = random.randint(9999999, 999999999)
                #m_profile_image = base64_file(data=m_profile_image_temp, name="profile_image"+str(random_no))

                image = UserProfileImage.objects.update_or_create(user_id=user_id, defaults={
                    "m_profile_image": m_profile_image})

                if image:
                    return JsonResponse({'status': "success", 'message': "Profile image uploaded successfully."}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "Failed to upload profile image."}, status=400)
            else:
                return JsonResponse({'status': "error", 'message': "user_id and m_profile_image are mandatory fields."}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "Something went wrong."}, status=400)


class getMerchantDetails(generics.GenericAPIView):
    serializer_class = merchantSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":

            mobile_no = request.POST['mobile_no']
            user_temp = GreenBillUser.objects.get(mobile_no=mobile_no)

            is_varified = user_temp.is_verified_email

            try:
                token = Token.objects.get(user_id=user_temp)
            except:
                return JsonResponse({'status': "error", 'message': "Mobile no. not registered"}, status=400)

            if request.META['HTTP_AUTHORIZATION'] == str("Token " + token.key):

                if GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']:
                    user = GreenBillUser.objects.get(mobile_no=mobile_no)
                    serializer = merchantSerializer(user)

                    

                    base_url = "http://157.230.228.250/"

                    try:
                        profile_image = UserProfileImage.objects.get(
                            user_id=user.id)
                        if profile_image.m_profile_image:
                            image_url = str(
                                base_url) + str(profile_image.m_profile_image.url)
                        else:
                            image_url = str(base_url) + \
                                str("/media/user-profile-pic.png")
                    except:
                        image_url = str(base_url) + \
                            str("/media/user-profile-pic.png")

                    return JsonResponse({'status': "success", 'profile_data': serializer.data, 'image_data': image_url, 'is_varified': is_varified}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "User not exists"}, status=400)
            else:
                return JsonResponse({'status': "error", 'message': "token not valid !!!"}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)


@csrf_exempt
def removeMerchantProfileImage(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        result = UserProfileImage.objects.update_or_create(
            user_id=user_id, defaults={"m_profile_image": ""})

        if result:
            return JsonResponse({'status': "success", 'message': "Profile image removed successfully."}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to remove profile image"}, status=400)
    else:
        return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)


class getMerchantGeneralSetting(generics.GenericAPIView):
    serializer_class = merchantSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":

            m_business_id = request.POST['m_business_id']

            data = MerchantProfile.objects.filter(id = m_business_id)

            merchant_user_id = MerchantProfile.objects.get(id = m_business_id)

            merchant_object = GreenBillUser.objects.get(mobile_no = merchant_user_id.m_user)

            if data:
                base_url = "http://157.230.228.250"
                if data[0].m_GSTIN_certificate:
                    m_GSTIN_certificate = str(base_url) + str(data[0].m_GSTIN_certificate.url)
                else:
                    m_GSTIN_certificate = ""

                if data[0].m_CIN_certificate:
                    m_CIN_certificate = str(base_url) + str(data[0].m_CIN_certificate.url)
                else:
                    m_CIN_certificate = ""

                if data[0].m_business_logo:
                    m_business_logo = str(base_url) + str(data[0].m_business_logo.url)
                else:
                    m_business_logo = ""

                if data[0].m_business_stamp:
                    m_business_stamp = str(base_url) + str(data[0].m_business_stamp.url)
                else:
                    m_business_stamp = ""

                if data[0].m_digital_signature:
                    m_digital_signature = str(base_url) + str(data[0].m_digital_signature.url)
                else:
                    m_digital_signature = ""

                if data[0].m_cancel_bank_cheque_photo:
                    m_cancel_bank_cheque_photo = str(base_url) + str(data[0].m_cancel_bank_cheque_photo.url)
                else:
                    m_cancel_bank_cheque_photo = ""

                if data[0].m_other_document_certificate1:
                    udyog_adhaar_certificate = str(base_url) + str(data[0].m_other_document_certificate1.url)
                else:
                    udyog_adhaar_certificate = ""

                if data[0].address_proof:
                    address_proof = str(base_url) + str(data[0].address_proof.url)
                else:
                    address_proof = ""

                if data[0].m_address_bank_account:
                    attested_pan_card_legal_entity = str(base_url) + str(data[0].m_address_bank_account.url)
                else:
                    attested_pan_card_legal_entity = ""

                if data[0].m_bank_account_entry:
                    signature_proof_of_autorize_sign = str(base_url) + str(data[0].m_bank_account_entry.url)
                else:
                    signature_proof_of_autorize_sign = ""

                if data[0].company_registration_certificate:
                    company_registration_certificate = str(base_url) + str(data[0].company_registration_certificate.url)
                else:
                    company_registration_certificate = ""

                if data[0].schedule_pdf_upload:
                    schedule_pdf_upload = str(base_url) + str(data[0].schedule_pdf_upload.url)
                else:
                    schedule_pdf_upload = ""

                data_dict = {
                    'm_business_name': data[0].m_business_name,
                    'm_business_category_id': data[0].m_business_category_id,
                    'm_business_category_name': data[0].m_business_category.business_category_name,
                    'm_pin_code': data[0].m_pin_code,
                    'm_city': data[0].m_city,
                    'm_area': data[0].m_area,
                    'm_district': data[0].m_district,
                    'm_state': data[0].m_state,
                    'm_address': data[0].m_address,
                    'm_landline_number': data[0].m_landline_number,
                    'm_alternate_mobile_number': data[0].m_alternate_mobile_number,
                    'm_company_email': data[0].m_company_email,
                    'm_alternate_email': data[0].m_alternate_email,
                    'm_pan_number': data[0].m_pan_number,
                    'm_gstin': data[0].m_gstin,
                    'm_cin': data[0].m_cin,
                    'm_bank_account_number': data[0].m_bank_account_number,
                    'm_bank_IFSC_code': data[0].m_bank_IFSC_code,
                    'm_bank_name': data[0].m_bank_name,
                    'm_bank_branch': data[0].m_bank_branch,
                    'm_GSTIN_certificate': m_GSTIN_certificate,
                    'm_CIN_certificate': m_CIN_certificate,
                    'm_business_logo': m_business_logo,
                    'm_business_stamp': m_business_stamp,
                    'm_digital_signature': m_digital_signature,
                    'm_website_url': data[0].m_website_url,
                    'm_business_name_for_billing': data[0].m_business_name_for_billing,
                    'm_billing_address': data[0].m_billing_address,
                    'm_billing_email': data[0].m_billing_email,
                    'm_billing_phone': data[0].m_billing_phone,
                    'm_vat_tin_number': data[0].m_vat_tin_number,
                    'm_aadhaar_number': data[0].m_aadhaar_number,
                    'Entity_Account_m': data[0].Entity_Account_m,
                    'Entity_Bank_Account_m': data[0].Entity_Bank_Account_m,
                    'first_name': merchant_object.first_name,
                    'last_name': merchant_object.last_name,
                    'm_cancel_bank_cheque_photo': m_cancel_bank_cheque_photo,
                    'udyog_adhaar_certificate': udyog_adhaar_certificate,
                    'address_proof': address_proof,
                    'attested_pan_card_legal_entity': attested_pan_card_legal_entity,
                    'signature_proof_of_autorize_sign': signature_proof_of_autorize_sign,
                    'company_registration_certificate': company_registration_certificate,
                    'schedule_pdf_upload': schedule_pdf_upload,
                }
                
                return JsonResponse({'status': "success", 'data': data_dict}, status=200)
            else:
                return JsonResponse({'status': "error", 'message': "Data not found."}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)

class RemoveDigitalSignature(generics.GenericAPIView):
    serializer_class = merchantSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":

            m_business_id = request.POST['m_business_id']

            signature = ''

            result = MerchantProfile.objects.filter(id = m_business_id).update(m_digital_signature = signature)

            if result:
                return JsonResponse({'status': "success", 'message': "Digital Signature Removed Successfully."}, status=200)
            else:
                return JsonResponse({'status': "error", 'message': "Something went wrong."}, status=400)

class RemoveBusinessLogo(generics.GenericAPIView):
    serializer_class = merchantSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":

            m_business_id = request.POST['m_business_id']

            logo = ''

            result = MerchantProfile.objects.filter(id = m_business_id).update(m_business_logo = logo)

            if result:
                return JsonResponse({'status': "success", 'message': "Business Logo Removed Successfully."}, status=200)
            else:
                return JsonResponse({'status': "error", 'message': "Something went wrong."}, status=400)

class setMerchantGeneralSetting(generics.GenericAPIView):
    serializer_class = merchantSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":

            # user_id = request.POST['user_id']

            m_business_id = request.POST['m_business_id']

            merchant_user_id = MerchantProfile.objects.filter(id = m_business_id)

            m_business_name = request.POST['m_business_name']
            m_business_category_id= request.POST['m_business_category_id']
            m_pin_code= request.POST['m_pin_code']
            m_city= request.POST['m_city']
            m_area= request.POST['m_area']
            m_district= request.POST['m_district']
            m_state= request.POST['m_state']
            m_address= request.POST['m_address']
            m_landline_number= request.POST['m_landline_number']
            m_alternate_mobile_number= request.POST['m_alternate_mobile_number']
            m_company_email= request.POST['m_company_email']
            m_alternate_email= request.POST['m_alternate_email']
            m_pan_number= request.POST['m_pan_number']
            m_gstin= request.POST['m_gstin']
            m_cin= request.POST['m_cin']
            m_bank_account_number= request.POST['m_bank_account_number']
            m_bank_IFSC_code= request.POST['m_bank_IFSC_code']
            m_bank_name= request.POST['m_bank_name']
            m_bank_branch= request.POST['m_bank_branch']
            m_GSTIN_certificate= request.FILES.get('m_GSTIN_certificate', "")
            m_CIN_certificate= request.FILES.get('m_CIN_certificate', "")
            m_business_logo= request.FILES.get('m_business_logo', "")
            m_business_stamp= request.FILES.get('m_business_stamp', "")
            m_digital_signature= request.FILES.get('m_digital_signature', "")
            # cancel_bank_cheque_photo = request.FILES.get("cancel_bank_cheque_photo", "")

            m_website_url = request.POST['m_website_url']
            m_business_name_for_billing = request.POST['m_business_name_for_billing']
            m_billing_address = request.POST['m_billing_address']
            m_billing_email = request.POST['m_billing_email']
            m_billing_phone = request.POST['m_billing_phone']

            m_vat_tin_number = request.POST['m_vat_tin_number']
            Entity_Bank_Account_m = request.POST['Entity_Bank_Account_m']
            Entity_Account_m = request.POST['Entity_Account_m']
            m_aadhaar_number = request.POST['m_aadhaar_number']

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            GreenBillUser.objects.filter(mobile_no = merchant_user_id[0].m_user).update(first_name = first_name, last_name = last_name)
            
            data = MerchantProfile.objects.filter(id = m_business_id)

            result = MerchantProfile.objects.filter(id=data[0].id).update(m_aadhaar_number = m_aadhaar_number, Entity_Account_m = Entity_Account_m, Entity_Bank_Account_m = Entity_Bank_Account_m, m_vat_tin_number = m_vat_tin_number, m_billing_phone = m_billing_phone, m_billing_email = m_billing_email, m_billing_address= m_billing_address, m_website_url = m_website_url, m_business_name_for_billing = m_business_name_for_billing, m_business_name= m_business_name, m_business_category_id= m_business_category_id, m_pin_code= m_pin_code, m_city= m_city, m_area=m_area, m_district=m_district, m_state=m_state, m_address=m_address, m_landline_number=m_landline_number, m_alternate_mobile_number= m_alternate_mobile_number, m_company_email=m_company_email, m_alternate_email=m_alternate_email, m_pan_number= m_pan_number, m_gstin=m_gstin, m_cin=m_cin, m_bank_account_number=m_bank_account_number, m_bank_IFSC_code=m_bank_IFSC_code, m_bank_name=m_bank_name, m_bank_branch=m_bank_branch)

            if m_GSTIN_certificate:
                MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_GSTIN_certificate" : m_GSTIN_certificate })

            if m_CIN_certificate:
                MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_CIN_certificate" : m_CIN_certificate })
            
            if m_business_logo:
                MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_business_logo" : m_business_logo })

            if m_business_stamp:
                MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_business_stamp" : m_business_stamp })

            if m_digital_signature:
                MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_digital_signature" : m_digital_signature })

            # if cancel_bank_cheque_photo:
            #     MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_cancel_bank_cheque_photo" : cancel_bank_cheque_photo })


            if result:
                return JsonResponse({'status': "success", 'message': "Business settings saved successfully."}, status=200)
            else:
                return JsonResponse({'status': "error", 'message': "Unable to upload the data."}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)


class MerchantUploadCancelCheck(generics.GenericAPIView):
    serializer_class = merchantSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            m_business_id = request.POST.get('m_business_id')
            cancel_bank_cheque_photo = request.FILES.get("cancel_bank_cheque_photo", "")

            m_GSTIN_certificate = request.FILES.get("m_gstin_certificate")

            m_CIN_certificate = request.FILES.get("m_CIN_certificate")

            m_other_document_certificate1 = request.FILES.get("udyog_adhaar_certificate")

            address_proof = request.FILES.get("address_proof")

            m_address_bank_account = request.FILES.get("pan_card_legal_entity")

            m_bank_account_entry = request.FILES.get("proof_of_authourize_signature")

            company_registration_certificate = request.FILES.get("m_company_registration_certificate")

            schedule_pdf_upload = request.FILES.get("m_schedule_pdf_upload")

            m_digital_signature = request.FILES.get("m_digital_signature")

            m_business_logo = request.FILES.get("m_business_logo")

            data = MerchantProfile.objects.filter(id = m_business_id)

            if cancel_bank_cheque_photo:
                result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_cancel_bank_cheque_photo" : cancel_bank_cheque_photo })

            elif m_GSTIN_certificate:
                result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_GSTIN_certificate" : m_GSTIN_certificate })

            elif m_CIN_certificate:
                result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_CIN_certificate" : m_CIN_certificate })

            elif m_other_document_certificate1:
                result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_other_document_certificate1" : m_other_document_certificate1 })

            elif address_proof:
                result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "address_proof" : address_proof })

            elif m_address_bank_account:
                result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_address_bank_account" : m_address_bank_account })

            elif m_bank_account_entry:
                result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_bank_account_entry" : m_bank_account_entry })

            elif company_registration_certificate:
                result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "company_registration_certificate" : company_registration_certificate })

            elif schedule_pdf_upload:
                result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "schedule_pdf_upload" : schedule_pdf_upload })

            elif m_business_logo:
                result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_business_logo" : m_business_logo })

            elif m_digital_signature:
                result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_digital_signature" : m_digital_signature })

            if result:
                return JsonResponse({'status': "success", 'message': "General setting data uploaded successfully."}, status=200)
            else:
                return JsonResponse({'status': "error", 'message': "Unable to upload the data."}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)



class getMerchantBusinesses(generics.GenericAPIView):
    serializer_class = merchantBusinessSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        user_id = request.POST['user_id']

        merchant_user = Merchant_users.objects.get(user_id = user_id)

        if user_id:
            merchantBusiness = MerchantProfile.objects.filter(m_user = merchant_user.merchant_user_id)

            serializers = merchantBusinessSerializer(merchantBusiness, many=True)

            return JsonResponse(serializers.data, status=200, safe=False)
        else:
            return JsonResponse(serializers.errors, status=400)
            
        

# @csrf_exempt
# def getMerchantDetails(request):
#     queryset = GreenBillUser.objects.all()

#     if request.method == "POST":
#         mobile_no = request.POST['mobile_no']
#         if GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']:
#             user = GreenBillUser.objects.get(mobile_no=mobile_no)
#             serializer = merchantSerializer(user)

#             base_url = "http://157.230.228.250"

#             try:
#                 profile_image = UserProfileImage.objects.get(user_id=user.id)
#                 if profile_image.m_profile_image:
#                     image_url = str(base_url) + str(profile_image.m_profile_image.url)
#             except:
#                 image_url = str(base_url) + str("/media/user-profile-pic.png")

#             return JsonResponse({'status': "success", 'profile_data': serializer.data, 'image_data': image_url}, status=200)
#         else:
#             return JsonResponse({'status': "error", 'message': "user not exists"}, status=400)
#     else:
#         return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)

# @csrf_exempt
# def get_token_key(request):
#     if request.method == "POST":
#         user_id = request.POST['user_id']
#         try:
#             token = Token.objects.get(user_id=user_id)
#             return JsonResponse({'status': "success", 'token_key': token.key}, status=200)
#         except:
#             return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)
#     else:
#         return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)

class addDMenquiry(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
          
        user_id = request.POST['user_id']

        user_object = GreenBillUser.objects.get(id = user_id)
        name = request.POST['name']
        bissiness_name = request.POST['bissiness_name']
        contact_no = request.POST['contact_no']
        email_id =  request.POST['email_id']
        intrested_in = request.POST['intrested_in']
        comments = request.POST['comments']

        result = MerchantEnquiryModel.objects.create(
                mer_id = user_object,
                customer_name = name,
                bissiness_name = bissiness_name,
                contact_no = contact_no,
                email_id = email_id,
                intrested_in = intrested_in,
                comments = comments,
                enquary_status = "Active",
            )

        if result:
            return JsonResponse({'status': "success", "message":"Enquiry added Successfully"}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to add Enquiry"}, status=400)

class getCustomerInfo(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST.get('user_id')

        user_profile_object = Merchant_users.objects.get(user_id = user_id)

        merchant_object = GreenBillUser.objects.get(id = user_profile_object.merchant_user_id.id)

        merchant_business_id = request.POST['merchant_business_id']

        merchant_business_object = MerchantProfile.objects.get(id = merchant_business_id)

        customer_bill_list = CustomerBill.objects.filter(business_name=merchant_business_object,customer_added = False).order_by('-id')
        parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False).order_by('-id')
        petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id).order_by('-id')
        merchant_bill_list = MerchantBill.objects.filter(business_name = merchant_business_object, customer_added = False).order_by('-id').distinct()
        merchant_added_customer_list = Customer_Info_Model.objects.filter(mer_id = merchant_object,merchant_business_id=merchant_business_object).order_by('-id')


        customer_info_data = []

        for customer in merchant_added_customer_list:
            customer_info_data.append({
                "mobile_no" : customer.cust_mobile_num,
                "name" : customer.cust_first_name + ' ' + customer.cust_last_lname,
                "email" : customer.cust_email,
                "state" : "",
                "city": customer.customer_area,
                "date": timezone.localtime(customer.date_joined).strftime("%Y-%m-%d"),
            })

        for bill in parking_bill_list:
            try:
                user = GreenBillUser.objects.get(mobile_no = bill.mobile_no, is_customer = True)
                date = timezone.localtime(user.date_joined).strftime("%Y-%m-%d")

                count = count + 1
                name = user.first_name + ' ' + user.last_name
                email = user.email
                state = user.c_state 
                city = user.c_city
                customer_info_data.append({
                'mobile_no':mobile_no,
                'name': name,
                'email':email,
                'state':state,
                'city':city,
                'date': datetime.strptime(str(user.date_joined), '%Y-%m-%d').strftime('%Y-%m-%d'),
                })
            except:
                customer_info_data.append({
                    'mobile_no': bill.mobile_no,
                    'name': '',
                    'email':'',
                    'state':'',
                    'city':'',
                    'date': timezone.localtime(bill.created_at).strftime("%Y-%m-%d"),
                });


        for bill in petrol_bill_list:

            try:
                user = GreenBillUser.objects.get(mobile_no = bill.mobile_no, is_customer = True)
                date = timezone.localtime(user.date_joined).strftime("%Y-%m-%d")
                count = count + 1
                name = user.first_name + ' ' + user.last_name
                email = user.email
                state = user.c_state 
                city = user.c_city
                customer_info_data.append({
                'mobile_no':mobile_no,
                'name': name,
                'email':email,
                'state':state,
                'city':city,
                'date': date,
                })
            except:
                customer_info_data.append({
                    'mobile_no': bill.mobile_no,
                    'name': '',
                    'email':'',
                    'state':'',
                    'city':'',
                    'date': timezone.localtime(bill.created_at).strftime("%Y-%m-%d"),
                });

        for bill in customer_bill_list:

            try:
                user = GreenBillUser.objects.get(mobile_no = bill.mobile_no, is_customer = True)
                date = timezone.localtime(user.date_joined).strftime("%Y-%m-%d")
                count = count + 1
                name = user.first_name + ' ' + user.last_name
                email = user.email
                state = user.c_state 
                city = user.c_city
                customer_info_data.append({
                'mobile_no':mobile_no,
                'name': name,
                'email':email,
                'state':state,
                'city':city,
                'date': date,
                })
            except:
                customer_info_data.append({
                    'mobile_no': bill.mobile_no,
                    'name': '',
                    'email':'',
                    'state':'',
                    'city':'',
                    'date': timezone.localtime(bill.created_at).strftime("%Y-%m-%d"),
                });


        for bill in merchant_bill_list:
            try:
                user = GreenBillUser.objects.get(mobile_no = bill.mobile_no, is_customer = True)
                date = timezone.localtime(user.date_joined).strftime("%Y-%m-%d")
                count = count + 1
                name = user.first_name + ' ' + user.last_name
                email = user.email
                state = user.c_state 
                city = user.c_city
                customer_info_data.append({
                'mobile_no':mobile_no,
                'name': name,
                'email':email,
                'state':state,
                'city':city,
                'date': date,
                })
            except:
                customer_info_data.append({
                    'mobile_no': bill.mobile_no,
                    'name': '',
                    'email':'',
                    'state':'',
                    'city':'',
                    'date': timezone.localtime(bill.created_at).strftime("%Y-%m-%d"),
                });

        customer_info_data1 = []
        customer_info_data2 = []
        new_data = []
        filtered_list = []
        filtered_list2 = []
        customer_receipt = CustomerReceiptDetailsModels.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_object).order_by('-id')

        for user in customer_receipt:
            try:
                customer_info_data2.append({
                    'mobile_no': user.mobile_number,
                    'name': user.cash_received_from,
                    'email':'',
                    'state':'',
                    'city':'',
                    'date': datetime.strptime(str(user.date), '%Y-%m-%d').strftime('%Y-%m-%d'),
                    })
            except:
                customer_info_data2.append({
                    'mobile_no': user.mobile_number,
                    'name': '',
                    'email':'',
                    'state':'',
                    'city':'',
                    'date': '',
                    })

        for x in customer_info_data2:
            if x['mobile_no'] not in filtered_list:
                if x['mobile_no'] != '':
                    filtered_list.append(x['mobile_no'])

                    customer_info_data.append({
                        'mobile_no': x['mobile_no'],
                        'name': x['name'],
                        'email':'',
                        'state':'',
                        'city':'',
                        'date': x['date'],
                        })

        customer_cash_memo = CustomerCashMemoDetailModels.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_object).order_by('-id')

        for user in customer_cash_memo:
            try:
                customer_info_data1.append({
                    'mobile_no': user.mobile_number,
                    'name': user.name,
                    'email':'',
                    'state':'',
                    'city':'',
                    'date': datetime.strptime(str(user.date), '%Y-%m-%d').strftime('%Y-%m-%d'),
                    })
            except:
                customer_info_data1.append({
                    'mobile_no': user.mobile_number,
                    'name': '',
                    'email':'',
                    'state':'',
                    'city':'',
                    'date': '',
                    })

        for x in customer_info_data1:
            if x['mobile_no'] not in filtered_list:
                if x['mobile_no'] != '':
                    filtered_list.append(x['mobile_no'])

                    customer_info_data.append({
                        'mobile_no': x['mobile_no'],
                        'name': x['name'],
                        'email':'',
                        'state':'',
                        'city':'',
                        'date': x['date'],
                        })


        for unique in customer_info_data:
            if unique['mobile_no'] not in filtered_list2:
                filtered_list2.append(unique['mobile_no'])
                new_data.append({
                    "mobile_no" : unique['mobile_no'],
                    "name" : unique['name'],
                    "email" : unique['email'],
                    "state" : unique['state'],
                    "city": unique['city'],
                    "date": unique['date'],
                })

        # for bills in customer_bill_list:
        #     if bills.mobile_no not in mobile_no_list and bills.bill_amount not in mobile_no_list:
        #         mobile_no_list.append({
        #             'mobile_no': bills.mobile_no,
        #             'amount': bills.bill_amount
        #             })
        #     else:
        #         pass

            
        # for bills in customer_bill_list:
        #     if bills.mobile_no in mobile_no_list:
        #         continue
        #     else:
        #         mobile_no_list.append(bills.mobile_no)

        # for bills in parking_bill_list:
        #     if bills.mobile_no in mobile_no_list:
        #         continue
        #     else:
        #         mobile_no_list.append(bills.mobile_no)

        # for bills in petrol_bill_list:
        #     if bills.mobile_no in mobile_no_list:
        #         continue
        #     else:
        #         mobile_no_list.append(bills.mobile_no)

        # for merchant_bill in merchant_bill_list:
        #     if merchant_bill.mobile_no in mobile_no_list:
        #         continue
        #     else:
        #        mobile_no_list.append(merchant_bill.mobile_no)


        # data = []

        # for mobile_no in mobile_no_list:

        #     try:
        #         user = GreenBillUser.objects.get(mobile_no = mobile_no)
        #         name = user.first_name + ' ' + user.last_name
        #         email = user.email
        #         state = user.c_state 
        #         city = user.c_city
        #     except:
        #         name = ""
        #         email = ""
        #         state = ""
        #         city = ""

        #     data.append({
        #         'mobile_no':mobile_no,
        #         'name': name if name else "",
        #         'email':email if email else "",
        #         'state':state if state else "",
        #         'city':city if city else "",
        #     })

        new_data.sort(key = lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse = True)

        if new_data:
            return JsonResponse({'status': "success", "data":new_data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)


class getCashMemoByMobileNo(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST['user_id']

        mobile_no = request.POST['mobile_no']

        user_profile_object = Merchant_users.objects.get(user_id = user_id)

        merchant_object = GreenBillUser.objects.get(id = user_profile_object.merchant_user_id.id)

        merchant_business_id = request.POST['merchant_business_id']

        merchant_business_object = MerchantProfile.objects.get(id = merchant_business_id)

        cash_memo = CustomerCashMemoDetailModels.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_object, mobile_number = mobile_no).order_by('-id')

        cash_memo1 = CustomerCashMemoDetailModels.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_object, mobile_number = mobile_no).last()

        all_bill = []


        if cash_memo1:

            personal_details = {
                'mobile_no' : cash_memo1.mobile_number,
                'name' : cash_memo1.name,
            }

        else: 
            personal_details = {
                'mobile_no' : mobile_no,
                'name' : '',
            }            

        base_url = "http://157.230.228.250/"


        for bill in cash_memo:
            all_bill.append({

                'id': bill.id,
                'date': datetime.strptime(str(bill.date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'memo_no': bill.memo_no,
                'amount': str(bill.total),
                'memo_url' : str(base_url) + 'cash-memo/' + str(bill.memo_url) + "/"
            })

        if cash_memo:
            return JsonResponse({'status': 'success', 'data' : all_bill, 'personal_details' : personal_details}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)



class getReceiptByMobileNo(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST['user_id']

        mobile_no = request.POST['mobile_no']

        user_profile_object = Merchant_users.objects.get(user_id = user_id)

        merchant_object = GreenBillUser.objects.get(id = user_profile_object.merchant_user_id.id)

        merchant_business_id = request.POST['merchant_business_id']

        merchant_business_object = MerchantProfile.objects.get(id = merchant_business_id)

        receipt = CustomerReceiptDetailsModels.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_object, mobile_number = mobile_no).order_by('-id')

        receipt1 = CustomerReceiptDetailsModels.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_object, mobile_number = mobile_no).last()

        all_bill = []
        if receipt1:

            personal_details = {
                'mobile_no' : receipt1.mobile_number,
                'name' : receipt1.cash_received_from,
            }

        else: 
            personal_details = {
                'mobile_no' : mobile_no,
                'name' : '',
            }

        base_url = "http://157.230.228.250/"

        for bill in receipt:
            all_bill.append({
                'id': bill.id,
                'date': datetime.strptime(str(bill.date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'receipt_no': bill.receipt_no,
                'amount': str(bill.total),
                'receipt_url' : str(base_url) + 'receipt/' + str(bill.receipt_url) + "/"
            })

        if receipt:
            return JsonResponse({'status': 'success', 'data' : all_bill, 'personal_details' : personal_details}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)



class getBillsByMobileNo(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST['user_id']

        mobile_no = request.POST['mobile_no']

        # merchant_business_id = request.POST['merchant_business_id']

        # user_profile_object = Merchant_users.objects.get(user_id = user_id)

        # merchant_object = GreenBillUser.objects.get(id = user_profile_object.merchant_user_id.id)

        # merchant_business_object = MerchantProfile.objects.get(id = merchant_business_id)

        # customer_bill_list = CustomerBill.objects.filter(business_name=merchant_business_object)

        data = []

        base_url = "http://157.230.228.250/"

        try:
            customer_object = GreenBillUser.objects.get(mobile_no = mobile_no)

            personal_details = {
                    'mobile_no' : customer_object.mobile_no,
                    'first_name' : customer_object.first_name,
                    'last_name' : customer_object.last_name,
                    'email': customer_object.email,
                    'c_gender': customer_object.c_gender,
                    'c_dob': datetime.strptime(str(customer_object.c_dob), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'c_area': customer_object.c_area,
                    'c_pincode': customer_object.c_pincode
            }

        except:

            try:

                customer_object = Customer_Info_Model.objects.get(cust_mobile_num = mobile_no)

                personal_details = {
                        'mobile_no' : customer_object.cust_mobile_num,
                        'first_name' : customer_object.cust_first_name,
                        'last_name' : customer_object.cust_last_lname,
                        'email': customer_object.cust_email,
                        'c_gender': customer_object.c_gender,
                        'c_dob': datetime.strptime(str(customer_object.date_of_birth), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        'cust_profile': customer_object.cust_profile,
                        'c_area': customer_object.customer_area,
                        'c_pincode': customer_object.customer_pin_code
                }

            except:

                personal_details = {
                    'mobile_no' : mobile_no,
                    'first_name' : '',
                    'last_name' : '',
                    'email': '',
                    'c_gender': '',
                    'c_dob': '',
                    'c_profile': '',
                    'c_area': '',
                    'c_pincode': ''
                }


        # customer_bill_list = CustomerBill.objects.filter(business_name=merchant_business_object)
        customer_bill_list = CustomerBill.objects.filter(mobile_no=mobile_no)

        for bill in customer_bill_list:
            # if mobile_no == bill.mobile_no:
            try:
                bill_file = str(base_url) + str(bill.bill.url)
                if bill.customer_added == True:
                    new_bill_url = str(base_url) + 'self-added-bill/' + str(bill.bill_url) + "/"
                else:
                    new_bill_url = str(base_url) + 'my-bill/' + str(bill.bill_url) + "/"
            except:
                bill_file = ""
            data.append({
                'bill_id': bill.id,
                'mobile_no': mobile_no,
                'amount': str(bill.bill_amount),
                'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "CustomerBill",
                'customer_added': bill.customer_added,
                'new_bill_url' : new_bill_url
            })
                

        # parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id)
        parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no=mobile_no)
        for bill in parking_bill_list:
            # if mobile_no == bill.mobile_no:
            try:
                bill_file = str(base_url) + str(bill.bill_file.url)
                new_bill_url = str(base_url) + 'parking-lot-bill/' + str(bill.bill_url) + "/"
            except:
                bill_file = ""
            data.append({
                'bill_id': bill.id,
                'mobile_no': mobile_no,
                'amount': str(bill.amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SaveParkingLotBill",
                'customer_added': False,
                'new_bill_url': new_bill_url,
            })
               

        # petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id)
        petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no=mobile_no)
        for bill in petrol_bill_list:
            # if mobile_no == bill.mobile_no:
            try:
                bill_file = str(base_url) + str(bill.bill_file.url)
                new_bill_url = str(base_url) + 'petrol-pump-bill/' + str(bill.bill_url) + "/"
            except:
                bill_file = ""
            data.append({
                'bill_id': bill.id,
                'mobile_no': mobile_no,
                'amount': str(bill.total_amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SavePetrolPumpBill",
                'customer_added': False,
                'new_bill_url': new_bill_url
            })

        # sorted_data = sorted(data, key=data.bill_date)

        data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

        if data:
            return JsonResponse({'status': "success", "personal_details": personal_details, "all_bills":data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)


class customerInfoSendSms(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        bill_id = request.POST['bill_id']
        mobile_no = request.POST['mobile_no']
        db_table = request.POST['db_table']

        if mobile_no:
            if db_table == "CustomerBill":
                bill_object = CustomerBill.objects.get(id = bill_id)
                business_id = bill_object.business_name.id
                customer_bill_url = "http://157.230.228.250/my-bill/" + str(bill_object.bill_url) + "/"

            if db_table == "MerchantBill":
                bill_object = MerchantBill.objects.get(id = bill_id)
                business_id = bill_object.business_name.id
                customer_bill_url = "http://157.230.228.250/my-bill-merchant/" + str(bill_object.bill_url) + "/"

            elif db_table == "SaveParkingLotBill":
                bill_object = SaveParkingLotBill.objects.get(id = bill_id)
                business_id = bill_object.m_business_id
                customer_bill_url = "http://157.230.228.250/parking-lot-bill/" + str(bill_object.bill_url) + "/"

            elif db_table == "SavePetrolPumpBill":
                bill_object = SavePetrolPumpBill.objects.get(id = bill_id)
                business_id = bill_object.m_business_id
                customer_bill_url = "http://157.230.228.250/petrol-pump-bill/" + str(bill_object.bill_url) + "/"

            subscription_object = getActiveSubscriptionPlan(request, business_id) 

            if subscription_object:

                if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

                    s = pyshorteners.Shortener()
                    short_url = s.tinyurl.short(customer_bill_url)

                    if db_table == "CustomerBill" or db_table == "MerchantBill":

                        ts = int(time.time())
                        data_temp = {
                                "keyword":"Bill Delivery SMS",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
                                            "OA":"GBBILL",
                                            "MSISDN": mobile_no, # Recipient's Mobile Number
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

                    elif db_table == "SaveParkingLotBill":

                        ts = int(time.time())
                        data_temp = {
                                "keyword":"Bill Delivery SMS",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
                                            "OA":"GBPARK",
                                            "MSISDN": mobile_no, # Recipient's Mobile Number
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

                    elif db_table == "SavePetrolPumpBill":

                        ts = int(time.time())
                        data_temp = {
                                "keyword":"Bill Delivery SMS",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
                                            "OA":"GBPUMP",
                                            "MSISDN": mobile_no, # Recipient's Mobile Number
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

                    if response.status_code == 200:
                        total_amount_avilable_new = 0
                        total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
                        subscription_object.total_amount_avilable = total_amount_avilable_new
                        subscription_object.save()
                        return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                    else:
                        return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                else:
                    return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)
            else:
                return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
        else:
            return JsonResponse({'status':'error', 'message': "You don't have active Green Bill Subscription. Please purchase and try again."}, status=400)



class getBillInfoList(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        merchant_business_id = request.POST['merchant_business_id']

        from_date = request.POST.get('from_date')
        
        to_date = request.POST.get('to_date')

        data = []

        base_url = "http://157.230.228.250/"

        parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id).order_by('-id')
        for bill in parking_bill_list:
            try:
                bill_file = str(base_url) + str(bill.bill_file.url)
            except:
                bill_file = ""

            if bill.is_checkoutpin == True:
                try:
                    mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                except:
                    mobile_no = bill.mobile_no
            else:
                mobile_no = bill.mobile_no

            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': mobile_no,
                'amount': str(bill.amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SaveParkingLotBill",
                'created_at': str(bill.created_at),
                'customer_added': False,
                'url': str(base_url) + "parking-lot-bill/" + str(bill.bill_url) + "/"
            })
               

        petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id).order_by('-id')
        for bill in petrol_bill_list:
            try:
                bill_file = str(base_url) + str(bill.bill_file.url)
            except:
                bill_file = ""

            if bill.is_checkoutpin == True:
                try:
                    mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                except:
                    mobile_no = bill.mobile_no
            else:
                mobile_no = bill.mobile_no

            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': mobile_no,
                'amount': str(bill.total_amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SavePetrolPumpBill",
                'created_at': str(bill.created_at),
                'customer_added': False,
                'url': str(base_url) + "petrol-pump-bill/" + str(bill.bill_url) + "/",
            })

        merchant_object = MerchantProfile.objects.get(id = merchant_business_id)

        customer_bill = CustomerBill.objects.filter(business_name = merchant_object, customer_added = False).order_by('-id')

        for bill in customer_bill:
            try:
                bill_file = str(base_url) + str(bill.bill.url)
            except:
                bill_file = ""

            if bill.is_checkoutpin == True:
                try:
                    mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                except:
                    mobile_no = bill.mobile_no
            else:
                mobile_no = bill.mobile_no

            if bill.customer_added == True:
                url = str(base_url) + 'self-added-bill/' + str(bill.bill_url) + "/"
            else:
                url = str(base_url) + 'my-bill/' + str(bill.bill_url) + "/"

            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': mobile_no,
                'amount': str(bill.bill_amount),
                'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "CustomerBill",
                'created_at': str(bill.created_at),
                'customer_added': False,
                'url':url,
            })

        merchant_bill = MerchantBill.objects.filter(business_name = merchant_object)

        for bill in merchant_bill:
            try:
                bill_file = str(base_url) + str(bill.bill.url)
            except:
                bill_file = ""

            if bill.is_checkoutpin == True:
                try:
                    mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                except:
                    mobile_no = bill.mobile_no
            else:
                mobile_no = bill.mobile_no

            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': mobile_no,
                'amount': str(bill.bill_amount),
                'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "MerchantBill",
                'created_at': str(bill.created_at),
                'customer_added': False,
                'url': str(base_url) + "my-bill-merchant/" + str(bill.bill_url) + "/",
            })

        data.sort(key = lambda x: x['created_at'], reverse = True)

        total_bills_created = 0
        total_amount_collected = 0
        total_flag_bills = 0

        for bill in data:
            total_bills_created = total_bills_created + 1
            total_amount_collected = float(total_amount_collected) + float(bill['amount'])

        new_data = []

        if from_date and to_date:

            if data:
                if from_date:
                    from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

                if to_date:
                    to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

                for bill in data:
                    bill_date = datetime.strptime(str(bill['bill_date']), '%d-%m-%Y').strftime('%Y-%m-%d')
                    if from_date and to_date:
                        
                        if bill_date >= from_date and bill_date <= to_date:
                            new_data.append(bill)

                new_data.sort(key = lambda x: x['created_at'], reverse = True)

                total_bills_created = 0
                total_amount_collected = 0
                total_flag_bills = 0

                for bill in new_data:
                    total_bills_created = total_bills_created + 1
                    total_amount_collected = float(total_amount_collected) + float(bill['amount'])

                if new_data:
                    return JsonResponse({'status': "success", "all_bills":new_data, "total_bills_created": total_bills_created,
                    "total_amount_collected":total_amount_collected, "from_date": from_date, "to_date": to_date}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)
        else:

            if data:
                return JsonResponse({'status': "success", "all_bills":data, "total_bills_created": total_bills_created,
                    "total_amount_collected":total_amount_collected, "from_date": "", "to_date": "" }, status=200)
            else:
                return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)


class BillInfoSendSms(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        bill_id = request.POST['bill_id']
        mobile_no = request.POST['mobile_no']
        db_table = request.POST['db_table']

        # print(db_table)


        if mobile_no:
            if db_table == "CustomerBill":
                bill_object = CustomerBill.objects.get(id = bill_id)
                business_id = bill_object.business_name.id
                customer_bill_url = "http://157.230.228.250/my-bill/" + str(bill_object.bill_url) + "/"

            if db_table == "MerchantBill":
                bill_object = MerchantBill.objects.get(id = bill_id)
                business_id = bill_object.business_name.id
                customer_bill_url = "http://157.230.228.250/my-bill-merchant/" + str(bill_object.bill_url) + "/"

            elif db_table == "SaveParkingLotBill":
                bill_object = SaveParkingLotBill.objects.get(id = bill_id)
                business_id = bill_object.m_business_id
                customer_bill_url = "http://157.230.228.250/parking-lot-bill/" + str(bill_object.bill_url) + "/"

            elif db_table == "SavePetrolPumpBill":
                bill_object = SavePetrolPumpBill.objects.get(id = bill_id)
                business_id = bill_object.m_business_id
                customer_bill_url = "http://157.230.228.250/petrol-pump-bill/" + str(bill_object.bill_url) + "/"

            subscription_object = getActiveSubscriptionPlan(request, business_id) 

            device = DeviceId.objects.filter(mobile_no=mobile_no).first()
            push_service = FCMNotification(api_key=settings.API_KEY)

            if subscription_object and subscription_object.total_amount_avilable:

                if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):
                    s = pyshorteners.Shortener()
                    short_url = s.tinyurl.short(customer_bill_url)

                    if db_table == "CustomerBill" or db_table == "MerchantBill":

                        if device != None:

                            try:
                                registration_id = device.device_id
                            except:
                                registration_id = ''

                            message_title = "New Bill"

                            message_body = "Hey Green Bill user, view and download your bill here. " + str(customer_bill_url)

                            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

                            total_amount_avilable_new = 0
                            total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_digital_bill_cost)
                            subscription_object.total_amount_avilable = total_amount_avilable_new
                            subscription_object.save()

                            return JsonResponse({'status':'success', 'message': 'Notification send successfully'}, status=200)
                        else:

                            ts = int(time.time())
                            data_temp = {
                                    "keyword":"Bill Delivery SMS",
                                    "timeStamp":ts,
                                    "dataSet":
                                        [
                                            {
                                                "UNIQUE_ID":"GB-" + str(ts),
                                                "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
                                                "OA":"GBBILL",
                                                "MSISDN": mobile_no, # Recipient's Mobile Number
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

                            if response.status_code == 200:
                                total_amount_avilable_new = 0
                                total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
                                subscription_object.total_amount_avilable = total_amount_avilable_new
                                subscription_object.save()
                                return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                            else:
                                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)


                    elif db_table == "SaveParkingLotBill":
                        if device != None:

                            try:
                                registration_id = device.device_id
                            except:
                                registration_id = ''

                            message_title = "New Bill"

                            message_body = "Hey Green Bill user, view and download your bill here. " + str(customer_bill_url)

                            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

                            total_amount_avilable_new = 0
                            total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_digital_bill_cost)
                            subscription_object.total_amount_avilable = total_amount_avilable_new
                            subscription_object.save()

                            return JsonResponse({'status':'success', 'message': 'Notification send successfully'}, status=200)
                        else:

                            ts = int(time.time())
                            data_temp = {
                                    "keyword":"Bill Delivery SMS",
                                    "timeStamp":ts,
                                    "dataSet":
                                        [
                                            {
                                                "UNIQUE_ID":"GB-" + str(ts),
                                                "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
                                                "OA":"GBPARK",
                                                "MSISDN": mobile_no, # Recipient's Mobile Number
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

                            if response.status_code == 200:
                                total_amount_avilable_new = 0
                                total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
                                subscription_object.total_amount_avilable = total_amount_avilable_new
                                subscription_object.save()
                                return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                            else:
                                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)


                    elif db_table == "SavePetrolPumpBill":

                        if device != None:

                            try:
                                registration_id = device.device_id
                            except:
                                registration_id = ''

                            message_title = "New Bill"

                            message_body = "Hey Green Bill user, view and download your bill here. " + str(customer_bill_url)

                            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

                            total_amount_avilable_new = 0
                            total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_digital_bill_cost)
                            subscription_object.total_amount_avilable = total_amount_avilable_new
                            subscription_object.save()

                            return JsonResponse({'status':'success', 'message': 'Notification send successfully'}, status=200)

                        else:

                            ts = int(time.time())
                            data_temp = {
                                    "keyword":"Bill Delivery SMS",
                                    "timeStamp":ts,
                                    "dataSet":
                                        [
                                            {
                                                "UNIQUE_ID":"GB-" + str(ts),
                                                "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
                                                "OA":"GBPUMP",
                                                "MSISDN": mobile_no, # Recipient's Mobile Number
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
         
                            if response.status_code == 200:
                                total_amount_avilable_new = 0
                                total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
                                subscription_object.total_amount_avilable = total_amount_avilable_new
                                subscription_object.save()
                                return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                            else:
                                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                else:
                    return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
            else:
                return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
        else:
            return JsonResponse({'status':'error', 'message': "You don't have active Green Bill Subscription. Please purchase and try again."}, status=400)


class getMerchantReferralCode(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST['user_id']

        user_profile_object = Merchant_users.objects.get(user_id = user_id)

        merchant_object = GreenBillUser.objects.get(id = user_profile_object.merchant_user_id.id)

        if merchant_object:
            return JsonResponse({'status':'success', 'message': merchant_object.merchant_referral_code}, status=200)
        else:
            return JsonResponse({'status' : 'error', 'message': "Referral Code Not Available"}, status=400)


class createMerchantUser(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST['user_id']

        user_profile_object = Merchant_users.objects.get(user_id = user_id)

        merchant_object = GreenBillUser.objects.get(id = user_profile_object.merchant_user_id.id)

        m_business_id = request.POST['m_business_id']

        m_business_object = MerchantProfile.objects.get(id = m_business_id)

        if GreenBillUser.objects.filter(mobile_no = request.POST['mobile_no']).exists():
            return JsonResponse({'status':'error', 'message': "Mobile number is already used !!!"}, status=400)

        else:

            startswith = str(m_business_object.id) + ','
            endswith = ','+ str(m_business_object.id)
            contains = ','+ str(m_business_object.id) + ','
            exact = str(m_business_object.id)

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

            role_name_id = request.POST["role_id"]

            role1 = "Exe User"

            merchant_role1 = merchant_userrole.objects.filter(role_id = role_name_id, role__role_name = role1)

            if merchant_role1:

                if number_of_users:
                            
                    all_merchant_users = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = m_business_object.id)
                
                    number_of_exe_role = 0
                    
                    for user in all_merchant_users:
                        
                        temp1 = GreenBillUser.objects.get(mobile_no=user.user_id)
                        
                        role_data = merchant_userrole.objects.filter(user = temp1)

                        for oject1 in role_data:
                            
                            user.user_id.role = oject1.id
                            
                            user.user_id.role_name = oject1.role
                            
                            roles2 = merchant_role.objects.filter(role_name= oject1.role, merchant_business_id = m_business_object)
                            
                            for oject2 in roles2:
                                
                                role_name1 = oject2.role_name
                                
                                if role_name1 == 'Exe User':
                                    
                                    number_of_exe_role = number_of_exe_role + 1

                    if int(number_of_exe_role + 1) < int(number_of_users):
                        temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
        
                        user = GreenBillUser.objects.create_user(
                            mobile_no = request.POST['mobile_no'],
                            m_email = request.POST['email'],
                            first_name = request.POST['first_name'],
                            last_name = request.POST['last_name'],
                            password = temp_password,
                            is_merchant_staff = 1
                        )

                        result1 = Merchant_users.objects.create(user_id = user, merchant_user_id = merchant_object, raw_password= temp_password, m_business_id = m_business_object.id, m_business_name= m_business_object.m_business_name)

                        role_id = request.POST["role_id"]

                        result2 = merchant_userrole.objects.create(user = user, role_id = role_id)

                        name = request.POST['first_name']
                        email = request.POST['email']
                        mobile_no = request.POST['mobile_no']

                        ts = int(time.time())

                        data_temp = {
                                "keyword":"ID and Password of users",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Dear Green Bill user, here is the login credentials for your team. Username: " + mobile_no + " Password: "+ temp_password,
                                            "OA":"GRBILL", 
                                            "MSISDN": mobile_no, # Recipient's Mobile Number
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

                        if user and result1 and result2:
                            return JsonResponse({'status': 'success', 'message': 'User created successfully !!!'}, status=200)
                        else:
                            return JsonResponse({'status': 'success', 'message': 'Failed to create user !!!'}, status=400)
                    else:
                        return JsonResponse({'status': 'success', 'message': 'Exe user can created as per your subscription plan !!!'}, status=400)
                else:
                    return JsonResponse({'status': 'success', 'message': 'Exe user can created as per your subscription plan !!!'}, status=400)
            else:        
                temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
                
                user = GreenBillUser.objects.create_user(
                    mobile_no = request.POST['mobile_no'],
                    m_email = request.POST['email'],
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    password = temp_password,
                    is_merchant_staff = 1
                )

                result1 = Merchant_users.objects.create(user_id = user, merchant_user_id = merchant_object, raw_password= temp_password, m_business_id = m_business_object.id, m_business_name= m_business_object.m_business_name)

                role_id = request.POST["role_id"]

                result2 = merchant_userrole.objects.create(user = user, role_id = role_id)

                name = request.POST['first_name']
                email = request.POST['email']
                mobile_no = request.POST['mobile_no']

                ts = int(time.time())

                data_temp = {
                        "keyword":"ID and Password of users",
                        "timeStamp":ts,
                        "dataSet":
                            [
                                {
                                    "UNIQUE_ID":"GB-" + str(ts),
                                    "MESSAGE":"Dear Green Bill user, here is the login credentials for your team. Username: " + mobile_no + " Password: "+ temp_password,
                                    "OA":"GRBILL", 
                                    "MSISDN": mobile_no, # Recipient's Mobile Number
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

            if user and result1 and result2:
                return JsonResponse({'status': 'success', 'message': 'User created successfully !!!'}, status=200)
            else:
                return JsonResponse({'status': 'success', 'message': 'Failed to create user !!!'}, status=400)


class MerchantUserRole(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_user_id = request.POST['m_user_id']

        merchant_business_id = request.POST['merchant_business_id']

        merchant_business_object = MerchantProfile.objects.get(id = merchant_business_id)

        merchant_object = GreenBillUser.objects.get(id = m_user_id)

        result = merchant_role.objects.filter(merchant_id = merchant_object, merchant_business_id = merchant_business_object)

        # print(result)

        serializer = MerchantUserRoleSerializer(result, many=True)

        if result:
            return JsonResponse(serializer.data, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)

class MerchantUsers(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_user_id = request.POST['m_user_id']

        m_business_id = request.POST['m_business_id']

        merchant_object = GreenBillUser.objects.get(id = m_user_id)

        merchant_business = MerchantProfile.objects.get(id = m_business_id)

        merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = m_business_id).order_by('-id')

        merchant_user = []

        for user in merchant_user_temp:

            role_temp = merchant_userrole.objects.filter(user = user.user_id)
    
            try:
                role_id = str(role_temp[0].role.id)
                role_name = role_temp[0].role.role_name

            except:
                role_id = ""
                role_name = ""


            merchant_user.append({
                'id': user.user_id.id,
                'name': user.user_id.first_name + " " + user.user_id.last_name,
                'mobile_no': user.user_id.mobile_no,
                'email': user.user_id.m_email,
                'role_id': role_id,
                'role_name': role_name
            })

        if merchant_user:
            return JsonResponse({'data':merchant_user}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)

# Dashboard

class ParkingMerchantDashboardHeaderCalulations(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        parking_bills = SaveParkingLotBill.objects.filter(m_business_id = m_business_id, created_at__date = timezone.now(), is_pass = False).all()

        total_bills = 0
        total_collection = float(0)
        total_flagged = 0

        for bill in parking_bills:
            total_bills += 1
            total_collection = total_collection + float(bill.amount)

            if bill.bill_flag == True:
                total_flagged = total_flagged + 1

        parking_pass = ParkingLotPass.objects.filter(m_business_id = m_business_id, created_at__date = timezone.now()).all()

        total_pass_collection = 0
        total_pass = 0

        for pass_temp in parking_pass:
            total_pass_collection = total_pass_collection + float(pass_temp.amount)
            total_pass = total_pass + 1

        todays_payments = {
            'cash': float(total_collection + total_pass_collection),
            'online': ''
        }

        todays_bill = {
            'total': total_bills,
            'flagged': total_flagged
        }

        space_data = MerchantParkingLotSpace.objects.filter(m_business_id = m_business_id)

        actual_space_data = []

        for data_temp in space_data:

            try:
                temp = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True)

                vehicle_parked_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__date = timezone.now()).count()

                vehicle_exit_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = True, manage_space = True, created_at__date = timezone.now()).count()
                
                space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()
                
            except:
                space_avilable_count = 0

            space_avilable_count_temp = int(data_temp.spaces_count) - int(space_avilable_count)

            space_used = int(data_temp.spaces_count) - int(space_avilable_count_temp)

            parking_bills = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__date = timezone.now())

            total_bills_made = float(0)

            for bill in parking_bills:
                total_bills_made = total_bills_made + float(bill.amount)

            actual_space_data.append({
                "id": data_temp.id,
                "vehicle_type": data_temp.vehicle_type,
                "space": data_temp.spaces_count,
                "available_parking_space": str(space_avilable_count_temp),
                "space_used": space_used,
                "space_avilable_count": space_avilable_count,
                "vehicle_exit_count": vehicle_exit_count,
                "vehicle_parked_count": vehicle_parked_count,
                "total_bills_made": total_bills_made
            })

        space_available = []
        foorloop_count = 0

        for space in actual_space_data:
            if foorloop_count < 3:
                space_available.append({
                    'vehicle_type': space['vehicle_type'],
                    'available_parking_space': space['available_parking_space'],
                    'total_space': space['space'],
                })
                foorloop_count+=1

        not_exited = []
        foorloop_count = 0
        for space in actual_space_data:
            if foorloop_count < 3:
                not_exited.append({
                    'vehicle_type': space['vehicle_type'],
                    'space_used': space['space_used']
                })
                foorloop_count+=1

        if m_business_id:
            return JsonResponse({'status':"success", 'todays_payments': todays_payments, 'todays_bill': todays_bill, 'space_available': space_available, 'not_exited': not_exited}, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class ParkingMerchantVehicleTypeWiseCalulationsGraph(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        space_data = MerchantParkingLotSpace.objects.filter(m_business_id = m_business_id)
        if from_date and to_date:
            DATE_FORMAT = '%Y-%m-%d'

            date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
            day_later = date_time_obj + timedelta(days=1)
            x = day_later.date()
            ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

            vehical_start_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = vehical_start_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            actual_space_data = []

            for data_temp in space_data:

                try:
                    temp = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True)

                    vehicle_parked_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__range = (sd_filter, ed_filter)).count()

                    vehicle_exit_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = True, manage_space = True, created_at__range = (sd_filter, ed_filter)).count()
                    
                    space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()
                    
                except:
                    space_avilable_count = 0

                space_avilable_count_temp = int(data_temp.spaces_count) - int(space_avilable_count)

                space_used = int(data_temp.spaces_count) - int(space_avilable_count_temp)

                parking_bills = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__range = (sd_filter, ed_filter))

                total_bills_made = 0

                for bill in parking_bills:
                    total_bills_made = total_bills_made + float(bill.amount)

                actual_space_data.append({
                    "id": data_temp.id,
                    "vehicle_type": data_temp.vehicle_type,
                    "space": data_temp.spaces_count,
                    "available_parking_space": str(space_avilable_count_temp),
                    "space_used": space_used,
                    "space_avilable_count": space_avilable_count,
                    "vehicle_exit_count": vehicle_exit_count,
                    "vehicle_parked_count": vehicle_parked_count,
                    "total_bills_made": float(total_bills_made)
                })

            labels = []
            data = []

            for space in actual_space_data:
                vehicle_type_temp = space["vehicle_type"]
                labels.append(vehicle_type_temp)
                # data.append(round(space['total_bills_made']))
                decimal_value = format(float(space['total_bills_made']), ".2f")
                data.append(decimal_value)

        else: 

            actual_space_data = []

            for data_temp in space_data:

                try:
                    temp = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True)

                    vehicle_parked_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__date = timezone.now()).count()

                    vehicle_exit_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = True, manage_space = True, created_at__date = timezone.now()).count()
                    
                    space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()
                    
                except:
                    space_avilable_count = 0

                space_avilable_count_temp = int(data_temp.spaces_count) - int(space_avilable_count)

                space_used = int(data_temp.spaces_count) - int(space_avilable_count_temp)

                parking_bills = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__date = timezone.now())

                total_bills_made = 0

                for bill in parking_bills:
                    total_bills_made = total_bills_made + float(bill.amount)

                actual_space_data.append({
                    "id": data_temp.id,
                    "vehicle_type": data_temp.vehicle_type,
                    "space": data_temp.spaces_count,
                    "available_parking_space": str(space_avilable_count_temp),
                    "space_used": space_used,
                    "space_avilable_count": space_avilable_count,
                    "vehicle_exit_count": vehicle_exit_count,
                    "vehicle_parked_count": vehicle_parked_count,
                    "total_bills_made": float(total_bills_made)
                })

            labels = []
            data = []

            for space in actual_space_data:
                vehicle_type_temp = space["vehicle_type"]
                labels.append(vehicle_type_temp)
                # data.append(round(space['total_bills_made']))
                decimal_value = format(float(space['total_bills_made']), ".2f")
                data.append(decimal_value)
                # data.append(round(space['total_bills_made'],2))
                # productWiseBillsdoughnutChart_labels_temp.append(vehicle_type_temp)
                # productWiseBillsdoughnutChart_data_temp.append(space['vehicle_parked_count'])

        if labels and data:
            return JsonResponse({'status':"success", 'labels': labels, 'data': data}, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)

class ViewRatingAnalysisGraph(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        merchant_business_id = MerchantProfile.objects.get(id = m_business_id)

        ratings = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id).order_by('-id')

        feedback_count = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id).count()

        star1 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 1).count()
        star2 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 2).count()
        star3 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 3).count()
        star4 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 4).count()
        star5 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 5).count()
        total_rating = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id)

        total_feedback_count = 0

        for obj in total_rating:
            if obj.rating:
                total_feedback_count = total_feedback_count + 1

        average_rating = ((star5 * 5) + (star4 * 4) + (star3 * 3) + (star2 * 2) + (star1 * 1))/(total_feedback_count)


        rating1 = 0
        rating2 = 0
        rating3 = 0
        rating4 = 0
        rating5 = 0

        data = []

        for obj1 in ratings:
            if obj1.rating:
                if obj1.rating == '1':
                    rating1 = rating1 + 1
                if obj1.rating == '2':
                    rating2 = rating2 + 1
                if obj1.rating == '3':
                    rating3 = rating3 + 1
                if obj1.rating == '4':
                    rating4 = rating4 + 1
                if obj1.rating == '5':
                    rating5 = rating5 + 1

        data.append(rating1)
        data.append(rating2)
        data.append(rating3)
        data.append(rating4)
        data.append(rating5)

        rating_percentage = []
        star1percentage = 0
        star2percentage = 0
        star3percentage = 0
        star4percentage = 0
        star5percentage = 0
        if feedback_count:
            star1percentage = (rating1/feedback_count)*100
            rating_percentage.append("%.2f" % round(star1percentage, 2))
        
            star2percentage = (rating2/feedback_count)*100
            rating_percentage.append("%.2f" % round(star2percentage, 2))
        
            star3percentage = (rating3/feedback_count)*100
            rating_percentage.append("%.2f" % round(star3percentage, 2))
        
            star4percentage = (rating4/feedback_count)*100
            rating_percentage.append("%.2f" % round(star4percentage, 2))
        
            star5percentage = (rating5/feedback_count)*100
            rating_percentage.append("%.2f" % round(star5percentage, 2))

        labels = ['1 Star','2 Star','3 Star','4 Star','5 Star']

        if labels and data:
            return JsonResponse({'status':"success", 'labels': labels, 'data': data, 'rating_percentage': rating_percentage, 'average_rating': average_rating, 'total_feedback_count': total_feedback_count}, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)





class ParkingMerchantVehicleTypeWiseBillsGraph(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        space_data = MerchantParkingLotSpace.objects.filter(m_business_id = m_business_id)

        if from_date and to_date:
            DATE_FORMAT = '%Y-%m-%d'

            d_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = d_from_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
            day_later = date_time_obj + timedelta(days=1)
            x = day_later.date()
            ed_filter = datetime.strptime(str(x), '%Y-%m-%d')


            actual_space_data = []

            for data_temp in space_data:

                try:
                    temp = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True)

                    vehicle_parked_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__range = (sd_filter,ed_filter)).count()

                    vehicle_exit_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = True, manage_space = True, created_at__range = (sd_filter, ed_filter)).count()
                    
                    space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()
                    
                except:
                    space_avilable_count = 0

                space_avilable_count_temp = int(data_temp.spaces_count) - int(space_avilable_count)

                space_used = int(data_temp.spaces_count) - int(space_avilable_count_temp)

                parking_bills = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__range = (sd_filter, ed_filter))

                total_bills_made = 0

                for bill in parking_bills:
                    total_bills_made = total_bills_made + float(bill.amount)

                actual_space_data.append({
                    "id": data_temp.id,
                    "vehicle_type": data_temp.vehicle_type,
                    "space": data_temp.spaces_count,
                    "available_parking_space": str(space_avilable_count_temp),
                    "space_used": space_used,
                    "space_avilable_count": space_avilable_count,
                    "vehicle_exit_count": vehicle_exit_count,
                    "vehicle_parked_count": vehicle_parked_count,
                    "total_bills_made": float(total_bills_made)
                })

            labels = []
            data = []

            for space in actual_space_data:
                vehicle_type_temp = space["vehicle_type"]
                labels.append(vehicle_type_temp)
                # data.append(round(space['vehicle_parked_count']))
                decimal_value = format(float(space['vehicle_parked_count']), ".2f")
                data.append(decimal_value)

        else:

            actual_space_data = []

            for data_temp in space_data:

                try:
                    temp = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True)

                    vehicle_parked_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__date = timezone.now()).count()

                    vehicle_exit_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = True, manage_space = True, created_at__date = timezone.now()).count()
                    
                    space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()
                    
                except:
                    space_avilable_count = 0

                space_avilable_count_temp = int(data_temp.spaces_count) - int(space_avilable_count)

                space_used = int(data_temp.spaces_count) - int(space_avilable_count_temp)

                parking_bills = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__date = timezone.now())

                total_bills_made = 0

                for bill in parking_bills:
                    total_bills_made = total_bills_made + float(bill.amount)

                actual_space_data.append({
                    "id": data_temp.id,
                    "vehicle_type": data_temp.vehicle_type,
                    "space": data_temp.spaces_count,
                    "available_parking_space": str(space_avilable_count_temp),
                    "space_used": space_used,
                    "space_avilable_count": space_avilable_count,
                    "vehicle_exit_count": vehicle_exit_count,
                    "vehicle_parked_count": vehicle_parked_count,
                    "total_bills_made": float(total_bills_made)
                })

            labels = []
            data = []

            for space in actual_space_data:
                vehicle_type_temp = space["vehicle_type"]
                labels.append(vehicle_type_temp)
                # data.append(round(space['vehicle_parked_count']))
                decimal_value = format(float(space['vehicle_parked_count']), ".2f")
                data.append(decimal_value)
                # data.append(float(space['vehicle_parked_count']))

        if labels and data:
            return JsonResponse({'status':"success", 'labels': labels, 'data': data}, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class PetrolMerchantDashboardHeaderCalulations(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, created_at__date = timezone.now()).all()

        total_bills = 0
        total_collection = float(0)
        total_flagged = 0

        for bill in petrol_bills:
            total_bills += 1
            total_collection = total_collection + float(bill.total_amount)

            if bill.bill_flag == True:
                total_flagged = total_flagged + 1

        todays_payments = {
            'cash': float(total_collection),
            'online': ''
        }

        todays_bill = {
            'total': total_bills,
            'flagged': total_flagged
        }

        products = MerchantPetrolPump.objects.filter(m_business_id = m_business_id).all()

        for product in products:
            petrol_bills_temp = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, product_id = product.id, created_at__date = timezone.now()).all()
            
            total_liter = float(0)
            total_amount = float(0)

            for bill in petrol_bills_temp:
                total_liter = total_liter + float(bill.volume)
                total_amount = total_amount + float(bill.amount)

            product.total_liter_sold = total_liter
            product.total_amount_colleted = total_amount

            # product_name_temp = "'" + product.product_name + "'"

            # productSaledoughnutChart_labels_temp.append(product_name_temp)

            # productSaledoughnutChart_data_temp.append(total_amount)

        todays_sales = []
        foorloop_count = 0

        for product in products:
            if foorloop_count < 3:
                todays_sales.append({
                    'product_name': product.product_name,
                    'total_amount_colleted': float((round(product.total_amount_colleted,2)))
                })
                foorloop_count+=1


        todays_rate = []
        foorloop_count = 0

        for product in products:
            if foorloop_count < 3:
                todays_rate.append({
                    'product_name': product.product_name,
                    'product_cost': float(product.product_cost)
                })
                foorloop_count+=1

        if m_business_id:
            return JsonResponse({'status':"success", 'todays_payments': todays_payments, 'todays_bill': todays_bill, 'todays_sales': todays_sales, 'todays_rate': todays_rate}, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class PetrolMerchantProductSalesGraph(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        products = MerchantPetrolPump.objects.filter(m_business_id = m_business_id).all()

        labels = []
        data = []

        if from_date and to_date:
            DATE_FORMAT = '%Y-%m-%d'

            d_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = d_from_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
            day_later = date_time_obj + timedelta(days=1)
            x = day_later.date()
            ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

            for product in products:

                petrol_bills_temp = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, product_id = product.id, created_at__range = (sd_filter,ed_filter)).all()
                total_liter = 0
                total_amount = 0

                for bill in petrol_bills_temp:
                    total_liter = total_liter + float(bill.volume)
                    total_amount = total_amount + float(bill.amount)

                product.total_liter_sold = total_liter
                product.total_amount_colleted = total_amount

                product_name_temp = product.product_name

                labels.append(product_name_temp)

                # data.append(round(total_amount))
                decimal_value = format(float(total_amount), ".2f")
                data.append(decimal_value)

        else:

            for product in products:

                petrol_bills_temp = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, product_id = product.id, created_at__date = timezone.now()).all()
                total_liter = 0
                total_amount = 0

                for bill in petrol_bills_temp:
                    total_liter = total_liter + float(bill.volume)
                    total_amount = total_amount + float(bill.amount)

                product.total_liter_sold = total_liter
                product.total_amount_colleted = total_amount

                product_name_temp = product.product_name

                labels.append(product_name_temp)

                # data.append(round(total_amount))
                decimal_value = format(float(total_amount), ".2f")
                data.append(decimal_value)

        if labels and data:
            return JsonResponse({'status':"success", 'labels': labels, 'data': data}, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class PetrolMerchantAddOnSalesGraph(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        addon_products = AddonPetrolPump.objects.filter(m_business_id = m_business_id).all()

        labels = []
        data = []

        if from_date and to_date:
            DATE_FORMAT = '%Y-%m-%d'

            d_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = d_from_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
            day_later = date_time_obj + timedelta(days=1)
            x = day_later.date()
            ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

            for addon_product in addon_products:

                petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, created_at__range = (sd_filter,ed_filter)).all()

                total_sold = 0
                amount_collected = 0

                for bills in petrol_bills:
                    addon_products_temp = bills.addon_product_id
                    addon_product_cost_temp = bills.addon_product_cost
                    addon_quantity_temp = bills.addon_quantity

                    if addon_products_temp:
                        bill_addon_products = list(addon_products_temp.split(","))
                        bill_addon_costs = list(addon_product_cost_temp.split(","))
                        addon_quantity = list(addon_quantity_temp.split(","))

                        for product in bill_addon_products:
                            if addon_product.id == int(product):
                                index = bill_addon_products.index(product)
                                total_sold = total_sold + int(addon_quantity[index])
                                amount_collected = amount_collected + float(bill_addon_costs[index]) * float(addon_quantity[index])
                
                addon_product.total_sold = total_sold
                addon_product.amount_collected = amount_collected

                product_name_temp = addon_product.product_name

                labels.append(product_name_temp)

                # data.append(round(amount_collected))
                decimal_value = format(float(amount_collected), ".2f")
                data.append(decimal_value)

        else:

            for addon_product in addon_products:

                petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, created_at__date = timezone.now()).all()

                total_sold = 0
                amount_collected = 0

                for bills in petrol_bills:
                    addon_products_temp = bills.addon_product_id
                    addon_product_cost_temp = bills.addon_product_cost
                    addon_quantity_temp = bills.addon_quantity

                    if addon_products_temp:
                        bill_addon_products = list(addon_products_temp.split(","))
                        bill_addon_costs = list(addon_product_cost_temp.split(","))
                        addon_quantity = list(addon_quantity_temp.split(","))

                        for product in bill_addon_products:
                            if addon_product.id == int(product):
                                index = bill_addon_products.index(product)
                                total_sold = total_sold + int(addon_quantity[index])
                                amount_collected = amount_collected + float(bill_addon_costs[index]) * float(addon_quantity[index])
                
                addon_product.total_sold = total_sold
                addon_product.amount_collected = amount_collected

                product_name_temp = addon_product.product_name

                labels.append(product_name_temp)

                # data.append(round(amount_collected))
                decimal_value = format(float(amount_collected), ".2f")
                data.append(decimal_value)

        if labels and data:
            return JsonResponse({'status':"success", 'labels': labels, 'data': data}, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class PetrolMerchantUserAnalysis(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        m_user_id = request.POST['m_user_id']
        # from_date = request.POST['from_date']
        # to_date = request.POST['to_date']

        # if from_date:
        #     from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')

        # if to_date:
        #     to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%d-%m-%Y')


        merchant_object = GreenBillUser.objects.get(id = m_user_id)

        merchant_business = MerchantProfile.objects.get(id = m_business_id)

        merchant_user = []

        merchant_user.append({
            'user_id': merchant_object
        })

        merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = m_business_id)

        for user in merchant_user_temp:
            merchant_user.append({
                'user_id': user.user_id
                })

        merchant_user_details = []



        for user in merchant_user:

                total_collection = 0
                total_flagged = 0

                petrol_logs = PetrolLog.objects.filter(user_id = user['user_id'].id, created_at__date = timezone.now())

                if petrol_logs:
                    login_at = petrol_logs[0].login_at
                    logout_at = petrol_logs[0].logout_at
                else:
                    login_at = ""
                    logout_at = ""
                   
                bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, user_id = user['user_id'].id, created_at__date = timezone.now()).all()
                total_bills = bills.count()

                for bill in bills:

                    total_collection = total_collection + float(bill.total_amount)

                    if bill.bill_flag == True and bill.flag_by == str(user['user_id'].id):
                        total_flagged = total_flagged + 1

                name = user['user_id'].first_name + ' ' + user['user_id'].last_name

                import pytz
                  
                IST = pytz.timezone('Asia/Kolkata')

                try:
                    login_at = login_at.astimezone(IST)
                except:
                    pass

                try:
                    logout_at = logout_at.astimezone(IST)
                except:
                    pass

                if login_at:
                    login_temp_time = str(login_at.time()).split('.')[0]
                else:
                    login_temp_time = ""

                try:
                    login_date = datetime.strptime(str(login_at.date()), '%Y-%m-%d').strftime('%d-%m-%Y')
                except:
                    login_date = ""

                try:
                    login_time = datetime.strptime(str(login_temp_time), '%H:%M:%S').strftime('%H:%M')
                except:
                    login_time = ""

                if logout_at:
                    logout_temp_time = str(logout_at.time()).split('.')[0]
                else:
                    logout_temp_time = ""

                try:
                    logout_time = datetime.strptime(str(logout_temp_time), '%H:%M:%S').strftime('%H:%M')
                except:
                    logout_time = ""

                merchant_user_details.append({
                    'name': name,
                    'total_bills': total_bills,
                    'total_collection': total_collection,
                    'login_at': login_at,
                    'logout_at': logout_time,
                    'total_flagged': total_flagged,
                    'login_date' : login_date,
                    'login_time' : login_time,
                })

        if merchant_user:
            return JsonResponse({'status':"success", 'data': merchant_user_details}, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class ParkingMerchantUserAnalysis(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        m_user_id = request.POST['m_user_id']

        # from_date = request.POST['from_date']
        # to_date = request.POST['to_date']

        merchant_object = GreenBillUser.objects.get(id = m_user_id)

        merchant_business = MerchantProfile.objects.get(id = m_business_id)

        merchant_user = []

        merchant_user.append({
            'user_id': merchant_object
        })

        merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = m_business_id)

        for user in merchant_user_temp:
            merchant_user.append({
                'user_id': user.user_id
                })


        merchant_user_details = []

        for user in merchant_user:

            total_collection_bill = 0
            total_flagged = 0
            total_hours = ""

            parking_logs = ParkingLog.objects.filter(user_id = user['user_id'].id, created_at__date = timezone.now())

            if parking_logs:
                login_at = parking_logs[0].login_at
                logout_at = parking_logs[0].logout_at
                
                # total_hours = logout_at - login_at

                # seconds = total_hours.seconds
                # hours = seconds//3600
                # print(hours)

            else:
                login_at = ""
                logout_at = ""
                total_hours = ""
               
            bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, user_id = user['user_id'].id, created_at__date = timezone.now(), is_pass = False).all()
            total_bills = bills.count()

            for bill in bills:

                total_collection_bill = total_collection_bill + float(bill.amount)

                if bill.bill_flag == True and bill.flag_by == str(user['user_id'].id):
                    total_flagged = total_flagged + 1

            name = user['user_id'].first_name + ' ' + user['user_id'].last_name

            parking_pass = ParkingLotPass.objects.filter(m_business_id = merchant_business.id, user_id = user['user_id'].id, created_at__date = timezone.now()).all()

            total_pass_collection = 0
            total_pass = 0

            for pass_temp in parking_pass:

                total_pass_collection = total_pass_collection + float(pass_temp.amount)
                total_pass = total_pass + 1

            import pytz
                  
            IST = pytz.timezone('Asia/Kolkata')

            try:
                login_at = login_at.astimezone(IST)
            except:
                pass

            try:
                logout_at = logout_at.astimezone(IST)
            except:
                pass

            if login_at:
                login_temp_time = str(login_at.time()).split('.')[0]
            else:
                login_temp_time = ""

            try:
                login_date = datetime.strptime(str(login_at.date()), '%Y-%m-%d').strftime('%d-%m-%Y')
            except:
                login_date = ""

            try:
                login_time = datetime.strptime(str(login_temp_time), '%H:%M:%S').strftime('%H:%M')
            except:
                login_time = ""

            if logout_at:
                logout_temp_time = str(logout_at.time()).split('.')[0]
            else:
                logout_temp_time = ""

            try:
                logout_time = datetime.strptime(str(logout_temp_time), '%H:%M:%S').strftime('%H:%M')
            except:
                logout_time = ""

            merchant_user_details.append({
                'name': name,
                'total_bills': total_bills,
                'total_collection_bill': total_collection_bill,
                'login_at': login_at,
                'logout_at': logout_time,
                'total_flagged': total_flagged,
                'total_hours' : total_hours,
                'total_pass_collection': total_pass_collection,
                'total_pass' : total_pass,
                'total_collection': float(total_collection_bill + total_pass_collection),
                'login_date' : login_date,
                'login_time' : login_time,
            })

        if merchant_user:
            return JsonResponse({'status':"success", 'data': merchant_user_details}, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class ParkingMerchantSessionGraph(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        context = {}

        # vehicles = MerchantParkingAddVehicle.objects.filter(m_business_id = m_business_id).all()

        # labels = []

        data = []

        month_labels = []

        today = date.today()

        # for vehicle in vehicles:
        #     labels.append(vehicle.vehicle_type)

        for i in range(4,13):
            datetime_object = datetime.strptime(str(i), "%m")
            full_month_name = datetime_object.strftime("%b")
            # data_temp['month'] = full_month_name
            month_labels.append(full_month_name)

        for j in range(1,4):
            datetime_object = datetime.strptime(str(j), "%m")
            full_month_name = datetime_object.strftime("%b")
            month_labels.append(full_month_name)


        # for vehicle in vehicles:

        data_temp = []
        month3 = []
        year3 = []
        for i in range(4,13):
            y1 = today.year
            year3.append(y1)
            if i < 10:
                m1 = "0" + str(i)
                month3.append(m1) 
            else:
                month3.append(i)
        for j in range(1,4):
            y2 = today.year + 1
            year3.append(y2)
            if j < 10:
                m2 = "0" + str(j)
                month3.append(m2)
        for month,year in zip(month3,year3):
            
            parking_bills = SaveParkingLotBill.objects.filter(m_business_id = m_business_id, created_at__year = year, created_at__month = month).all()
            total_collection = 0

            for bill in parking_bills:
                total_collection = total_collection + float(bill.amount)

            decimal_value = format(float(total_collection), ".2f")
            data_temp.append(decimal_value)
        
        context['status'] = "success"

        # context['labels'] = labels

        context['month_labels'] = month_labels

        context['Amount'] = data_temp

        if context:
            return JsonResponse(context, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class OtherBusinessMerchantSessionGraph(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST['user_id']

        merchant_users_object = Merchant_users.objects.get(user_id = user_id)

        merchant_object = merchant_users_object.merchant_user_id

        merchant_business = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)


        context = {}

        data = []

        month_labels = []

        today = date.today()


        for i in range(4,13):
            datetime_object = datetime.strptime(str(i), "%m")
            full_month_name = datetime_object.strftime("%b")
            # data_temp['month'] = full_month_name
            month_labels.append(full_month_name)

        for j in range(1,4):
            datetime_object = datetime.strptime(str(j), "%m")
            full_month_name = datetime_object.strftime("%b")
            month_labels.append(full_month_name)


        data_temp = []
        month3 = []
        year3 = []
        for i in range(4,13):
            y1 = today.year
            year3.append(y1)
            if i < 10:
                m1 = "0" + str(i)
                month3.append(m1) 
            else:
                month3.append(i)
        for j in range(1,4):
            y2 = today.year + 1
            year3.append(y2)
            if j < 10:
                m2 = "0" + str(j)
                month3.append(m2)
        for month,year in zip(month3,year3):
            
            merchant_bills = MerchantBill.objects.filter(business_name = merchant_business, created_at__year = year, created_at__month = month).all()
            customer_bills2 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False,created_at__year = year,created_at__month = month).all()
            total_collection = 0
            total_collection1= 0
            total_collection2= 0


            for bill in merchant_bills:
                total_collection1= total_collection1+ float(bill.bill_amount)

            for bill in customer_bills2:
                total_collection2= total_collection2+ float(bill.bill_amount)
                
            total_collection = float(total_collection1) + float(total_collection2)

            decimal_value = format(float(total_collection), ".2f")
            data_temp.append(decimal_value)

        
        context['status'] = "success"

        context['month_labels'] = month_labels

        context['Amount'] = data_temp

        if context:
            return JsonResponse(context, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class OtherBusinessBillSessionDatewiseGraph(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST['user_id']

        merchant_users_object = Merchant_users.objects.get(user_id = user_id)

        merchant_object = merchant_users_object.merchant_user_id

        merchant_business = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)


        context = {}

        data_temp = []

        days_labels = []

        today = date.today()
        current_year = today.year
        current_month = today.month
        total_days = calendar.monthrange(current_year, current_month)[1]
        
        for i in range(1,total_days+1):
            month_days = str(i)
            days_labels.append(month_days)

        
        month3 = []
        year3 = []
        days3 = []

        y1 = today.year
        year3.append(y1)
        m1 = today.month
        month3.append(m1)


        for j in range(1,total_days+1):
            days3.append(j) 

        for year in year3:
            for month in month3:
                for day in days3:
                    merchant_bills1 = MerchantBill.objects.filter(business_name = merchant_business,created_at__year = year, created_at__month = month,created_at__day = day).values('created_at__day').annotate(data_sum=Sum('bill_amount'))
                    customer_bills2 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__month = month,created_at__day = day).values('created_at__day').annotate(data_sum=Sum('bill_amount'))
                    
                    if merchant_bills1 or customer_bills2:
                        total_collection = 0
                        total_collection1 = 0
                        total_collection2 = 0
                        if merchant_bills1:
                            for bill in merchant_bills1:
                                total_collection1 = float(bill['data_sum'])

                        if customer_bills2:
                            for bill in customer_bills2:
                                total_collection2 = float(bill['data_sum'])
                        total_collection = float(total_collection1) + float(total_collection2)

                        decimal_value = format(float(total_collection), ".2f")
                        data_temp.append(decimal_value)
                    else:
                        total_collection = float(0)

                        decimal_value = format(float(total_collection), ".2f")
                        data_temp.append(decimal_value)
                    

        context['status'] = "success"

        context['days_labels'] = days_labels

        context['Amount'] = data_temp

        if context:
            return JsonResponse(context, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)

class GetMerchantExeDetails(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        merchant_business = MerchantProfile.objects.get(id = m_business_id)

        exe_send_and_print_bill_status1 = CustomerBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), exe_bill_type = 2).count()

        exe_send_and_print_bill_status2 = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), exe_bill_type = 2).count()

        exe_send_bill_status1 = CustomerBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), exe_bill_type = 1).count()

        exe_send_bill_status2 = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), exe_bill_type = 1).count()

        print_bill_status = ExePrintStatus.objects.filter(business_id = m_business_id, created_at__date = timezone.now()).count()

        send_print_bill_status = int(exe_send_and_print_bill_status1) + int(exe_send_and_print_bill_status2)

        send_bill_status = int(exe_send_bill_status1) + int(exe_send_bill_status2)

        if merchant_business:
            return JsonResponse({'status' : "success", "print_bill_status": print_bill_status, "send_print_bill_status": send_print_bill_status, "send_bill_status": send_bill_status}, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)




class PetrolMerchantSessionGraph(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        context = {}

        # products = MerchantPetrolPump.objects.filter(m_business_id = m_business_id).all()

        # labels = []

        data = []

        month_labels = []

        today = date.today()

        # for product in products:
        #     labels.append(product.product_name)
        
        for i in range(4,13):
            datetime_object = datetime.strptime(str(i), "%m")
            full_month_name = datetime_object.strftime("%b")
            month_labels.append(full_month_name)

        for j in range(1,4):
            datetime_object = datetime.strptime(str(j), "%m")
            full_month_name = datetime_object.strftime("%b")
            month_labels.append(full_month_name)


        # for product in products:

        data_temp = []
        month3 = []
        year3 = []
        for i in range(4,13):
            y1 = today.year
            year3.append(y1)
            if i < 10:
                m1 = "0" + str(i)
                month3.append(m1) 
            else:
                month3.append(i)
        for j in range(1,4):
            y2 = today.year + 1
            year3.append(y2)
            if j < 10:
                m2 = "0" + str(j)
                month3.append(m2)
        for month,year in zip(month3,year3):

            petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, created_at__year = year, created_at__month = month).all()
            
            total_collection = 0

            for bill in petrol_bills:
                if bill.amount:
                # amount1 = float(str(bill.amount))
                # print(type(bill.amount),bill.amount,type(amount1))
                    total_collection = total_collection + float(bill.total_amount)

            decimal_value = format(float(total_collection), ".2f")
            data_temp.append(decimal_value)


        context['status'] = "success"

        # context['labels'] = labels

        context['month_labels'] = month_labels

        context['Amount'] = data_temp

        if context:
            return JsonResponse(context, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class SuggestBusiness_API(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']
        user_id = request.POST['user_id']

        suggested_business_name = request.POST['suggested_business_name']
        contact_no = request.POST['contact_no']
        address = request.POST['address']

        result = SuggestBusiness.objects.create(m_business_id = m_business_id, user_id = user_id, suggested_business_name = suggested_business_name, contact_no = contact_no, address = address)

        if result:
            return JsonResponse({'status': 'success', 'message': 'Business suggested Successfully !!!'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to suggest !!!'}, status=400)


class SuggestBusinessList_API(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']
        user_id = user_id = request.POST['user_id']

        result = SuggestBusiness.objects.filter(m_business_id = m_business_id, user_id = user_id).order_by('-id')

        business_list = []

        for business in result:
           business_list.append({
            'id': business.id,
            'm_business_id': business.m_business_id,
            'user_id': business.user_id,
            'suggested_business_name': business.suggested_business_name,
            'contact_no': business.contact_no,
            'address': business.address,
            'suggested_date': datetime.strptime(str((business.created_at).date()), '%Y-%m-%d').strftime('%d-%m-%Y')
           }) 

        # serializer = SuggestBusinessSerializer(result, many=True)

        if result:
            return JsonResponse({'status' : "success", "data": business_list}, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)

class SuggestBrandAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        mobile_no =  request.POST['mobile_no']

        brand = request.POST['brand']

        location = request.POST['location']

        contact_no = request.POST['contact_no']

        result = SuggestBrand.objects.create(mobile_no = mobile_no, contact_no = contact_no, brand = brand, location = location, is_merchant = True)

        if result:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class FeedbackAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        mobile_no =  request.POST['mobile_no']

        bug = request.POST['bug']

        if bug == "true":
            bug_status = True
        else:
            bug_status = False

        suggestion = request.POST['suggestion']

        if suggestion == "true":
            suggestion_status = True
        else:
            suggestion_status = False

        comments = request.POST['comments']

        result = Feedback.objects.create(mobile_no = mobile_no, bug = bug_status, suggestion = suggestion_status, comments = comments, is_merchant = True)

        if result:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)



class get_stamp_data(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        merchant_business_id = request.POST.get('business_id')

        try:
            merchant_select_stamp = merchantusagestamp.objects.filter(merchant_business_id = merchant_business_id).last()
            stamp_id = merchant_select_stamp.merchant_stamp_id_one
        except:
            stamp_id = ''

        if stamp_id:
            temp_stamp = ""
            temp_stamp = stamp_id.replace("[", "")
            temp_stamp = temp_stamp.replace("]", "")
            temp_stamp = temp_stamp.replace("'", "")
            stamp_id = temp_stamp

        new_stamp_id = stamp_id.split(", ")

        stamp_data = []
        own_stamp = []
        for stamp in new_stamp_id:
            if stamp:
                latest_stamp_record = wstampmodels.objects.filter(id=stamp)
                for stamp1 in latest_stamp_record:
                    stamp_data.append({
                        "id" : stamp1.id,
                        "stamp_name" : stamp1.stamp_name,
                        "type":'default_stamps',
                        })

        try:

            saved_stamp_image = selectstampimage.objects.get(merchant_business_id = merchant_business_id).m_select_image
            selected_stamp_image = merchantstampupload.objects.filter(id = saved_stamp_image)

            for stamp in selected_stamp_image:
                own_stamp.append({
                    "id" : stamp.id,
                    "stamp_name": stamp.stamp_name,
                    "type":'own_stamps',
                    })
        except:
            pass

        if stamp_data:
            return JsonResponse({'status' : "success", "data1": stamp_data, "data2": own_stamp}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)

class CreateCashMemoAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST['user_id']
        m_business_id = request.POST['m_business_id']

        is_stamp_type = request.POST.get('stamp_type')
        stamp_data_id = request.POST.get('stamp_id')

        user_object = GreenBillUser.objects.get(id = user_id)
        merchant_business_object = MerchantProfile.objects.get(id = m_business_id)

        authorise = authorised_sign.objects.all()
        auth = ''
        sign = ''
        for auth in authorise:
            auth = auth.selection

        try:
            sign = authorised_sign.objects.get(id=auth).sign
        except:
            sign = ''

        try:
            memo = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_object).last()
        except:
            memo = ""

        if not memo:
            memo_no =  str("01").zfill(3)
        else:
            last_receipt = memo.memo_no
            no = int(last_receipt) + 1
            memo_no = str(no).zfill(3)

        name = request.POST['name']
        address = request.POST['address']
        mobile_number = request.POST['mobile_number']
        # total = request.POST['total']
        # total_in_words = request.POST['total_in_words']
        date = datetime.strptime(str(request.POST['date']), '%d-%m-%Y').strftime('%Y-%m-%d')
        # template_choice = request.POST['template_choice']

        description = request.POST['description']
        quantity = request.POST['quantity']
        rate = request.POST['rate']
        # amount = request.POST['amount']
        term_and_condition1 = request.POST.get('term_and_condition1')
        term_and_condition2 = request.POST.get('term_and_condition2')
        term_and_condition3 = request.POST.get('term_and_condition3')

        authorised = sign

        temp_desc = []
        if description:
            temp_desc.append(description)
    
        temp_desc = [str(i or '') for i in temp_desc]
        description = ",".join(temp_desc)

        temp_quant = []
        quantity_1 = quantity.split(",")
        quantity_2 = [int(q) for q in quantity_1]
        if quantity:
            temp_quant.append(quantity)
        
        conv = lambda i : i or ''
        temp_quant = [conv(i) for i in temp_quant]
        update_quantity = ",".join(temp_quant)


        temp_rate = []
        rate_1 = rate.split(",")
        rate_2 = [int(r) for r in rate_1]
        if rate:
            temp_rate.append(rate)
         
        conv = lambda i : i or ''
        temp_rate = [conv(i) for i in temp_rate]
        update_rate = ",".join(temp_rate)

        
        temp_amnt1 = []
        for quan, rat in zip(quantity_2, rate_2):
            temp_amnt1.append(quan * rat)
        temp_amnt2 = []
        for j in temp_amnt1:
          temp_amnt2.append(str(j))
        amount = ','.join(temp_amnt2)

        total = 0
        for i in temp_amnt2:
            total = total + int(i)
        p = inflect.engine()
        total_in_words = p.number_to_words(total)


        result = CustomerCashMemoDetailModels.objects.create(merchant_business_id = merchant_business_object, merchant_user = user_object, 
        name = name, address = address, mobile_number = mobile_number, total = total, 
        total_in_words = total_in_words, date=date, description = description, 
        quantity = update_quantity, rate = update_rate, amount = amount, 
        memo_no = memo_no,authorised_sign=authorised,
        term_and_condition1=term_and_condition1,
        term_and_condition2=term_and_condition2,
        term_and_condition3=term_and_condition3,
        stamp_last_record = stamp_data_id,
        is_stamp_type = is_stamp_type,)

        letters = string.ascii_letters
        digit = string.digits
        random_string = str(result.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
        
        result.memo_url = random_string

        result.save()

        if result:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class CashMemoListAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        m_business_id = request.POST['m_business_id']

        from_date = request.POST.get('from_date')

        to_date = request.POST.get('to_date')

        merchant_business_object = MerchantProfile.objects.get(id = m_business_id)

        if from_date and to_date:
            result = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_object, date__range=(from_date,to_date)).order_by("-id")
            object_list_count = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_object, date__range=(from_date,to_date)).count()
            total_cost_cash_memo = 0
            for object1 in result:
                if object1.total:
                    total_cost_cash_memo = float(object1.total) + float(total_cost_cash_memo)
        else:
            result = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_object).order_by("-id")
            object_list_count = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_object).count()
            total_cost_cash_memo = 0
            for object1 in result:
                if object1.total:
                    total_cost_cash_memo = float(object1.total) + float(total_cost_cash_memo)

        coupons_list = []

        for coupon in result:
            coupons_list.append({
                'id': coupon.id,
                'memo_no': coupon.memo_no,
                'name': coupon.name,
                'address': coupon.address,
                'mobile_number': coupon.mobile_number,
                'date': datetime.strptime(str(coupon.date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'total': float(coupon.total),
                'memo_url': "http://157.230.228.250/cash-memo/" + str(coupon.memo_url) + "/"
            })

        if result:
            return JsonResponse({'status' : "success", "data": coupons_list, "from_date": from_date, "to_date": to_date, "object_list_count": object_list_count, "total_cost_cash_memo": total_cost_cash_memo}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class CashMemoDeleteAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        m_business_id = request.POST['m_business_id']
        merchant_business_object = MerchantProfile.objects.get(id = m_business_id)

        cash_memo_id = request.POST['cash_memo_id']

        result = CustomerCashMemoDetailModels.objects.get(id = cash_memo_id, merchant_business_id = merchant_business_object).delete()

        if result:
            return JsonResponse({'status' : "success"}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class CashMemoSendAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        cash_memo_id = request.POST['cash_memo_id']
        mobile_no = request.POST['mobile_no']

        memo_object = CustomerCashMemoDetailModels.objects.get(id = cash_memo_id)

        business_id = memo_object.merchant_business_id.id

        subscription_object = getActiveSubscriptionPlan(request, business_id)

        if subscription_object:
            if subscription_object.total_amount_avilable and subscription_object.per_bill_cost:
                if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

                    letters = string.ascii_letters
                    digit = string.digits
                    random_string = str(id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                    
                    memo_object.memo_url = random_string

                    memo_object.save()

                    memo_url = ""

                    device = DeviceId.objects.filter(mobile_no=mobile_no, user_type='customer').first()

                    push_service = FCMNotification(api_key=settings.API_KEY)

                    if device:

                        registration_id = device.device_id

                        message_title = "Receiving New Cash Memo"

                        message_body = "You have received a Cash Memo from. " + str(memo_object.merchant_business_id.m_business_name)

                        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

                    if mobile_no:

                        memo_url = "http://157.230.228.250/cash-memo/" + str(random_string) + "/"

                        s = pyshorteners.Shortener()
                        short_url = s.tinyurl.short(memo_url)

                        ts = int(time.time())

                        data_temp = {
                                "keyword":"Cash Memo",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Hey Green Bill user to view or download your cash memo click on link " + short_url,
                                            "OA":"GBBILL",
                                            "MSISDN": str(mobile_no), # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098381110505", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                        response = requests.post(url, json = data_temp)

                        if response.status_code:
                            total_amount_avilable_new = 0
                            total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
                            subscription_object.total_amount_avilable = total_amount_avilable_new
                            subscription_object.save()
                            return JsonResponse({'status' : "success"}, status=200)
                        else:
                            return JsonResponse({'status' : "error"}, status=400)
                    else:
                        return JsonResponse({'status' : "error"}, status=400)
                else:
                    return JsonResponse({'status': 'error','message':"Insufficient Balance. Please purchase purchase Add On's and try again !!!"}, status=400)
            else:
                return JsonResponse({'status' : "error", 'message':"Not enough balance to send. Please recharge now !!!"}, status=400)

        else:
            return JsonResponse({'status': 'error','message':"You don't have active Green Bill Subscription. Please purchase and try again."}, status=400)


class CashMemoSaveTemplate(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        selected_template = request.POST['selected_template'] 

        user_object = GreenBillUser.objects.get(id = user_id)

        result=save_template_for_cashmemo.objects.create(merchant_user=user_object, template=selected_template)
        
        if result:
            return JsonResponse({'status' : "success",'message':"Template Added Successfully."}, status=200)
        else:
            return JsonResponse({'status' : "error",'message':"Fail to Add."}, status=400)


class CashMemoTemplateExist(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        # selected_template = request.POST['selected_template'] 

        try:
            user_object = GreenBillUser.objects.filter(id = user_id).last()
        except UniversityDetails.DoesNotExist:
            user = None

        result = []

        # if save_template_for_cashmemo.objects.filter(merchant_user=user_object).exists():
        #     data = save_template_for_cashmemo.objects.get(merchant_user=user_object)
        #     result.append({
        #             'template_id':data.template,
        #             'term1': "",
        #             'term2': "",
        #             'term3': ""
        #             })
        # else:
        #     result.append({
        #             'template_id': "",
        #             })

        

        terms = CustomerCashMemoDetailModels.objects.filter(merchant_user=user_object).last()

        if terms:
            if terms.term_and_condition1:
                condition1 = terms.term_and_condition1
            else:
                condition1 = ""

            if terms.term_and_condition2:
                condition2 = terms.term_and_condition2
            else:
                condition2 = ""

            if terms.term_and_condition3:
                condition3 = terms.term_and_condition3
            else:
                condition3 = ""

            if save_template_for_cashmemo.objects.filter(merchant_user=user_object).exists():
                try:
                    data = save_template_for_cashmemo.objects.filter(merchant_user=user_object).last()
                except:
                    data = '0'

                result.append({
                        'template_id':data.template,
                        'term1': condition1,
                        'term2': condition2,
                        'term3': condition3,
                        })
            else:
                result.append({
                        'template_id': "",
                        'term1': condition1,
                        'term2': condition2,
                        'term3': condition3,
                        }) 
        else:
            if save_template_for_cashmemo.objects.filter(merchant_user=user_object).exists():
                data = save_template_for_cashmemo.objects.get(merchant_user=user_object)
                result.append({
                        'template_id':data.template,
                        'term1': "",
                        'term2': "",
                        'term3': "",
                        })

            else:
                result.append({
                        'template_id': "",
                        'term1': "",
                        'term2': "",
                        'term3': "",
                        })


        if result:
            return JsonResponse({'status' : "success",'data':result}, status=200)
        else:
            return JsonResponse({'status' : "error",'data':result}, status=400)



class CreateReceiptAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST['user_id']
        m_business_id = request.POST['m_business_id']

        is_stamp_type = request.POST.get('stamp_type')
        stamp_data_id = request.POST.get('stamp_id')

        user_object = GreenBillUser.objects.get(id = user_id)
        merchant_business_object = MerchantProfile.objects.get(id = m_business_id)

        try:
            receipt = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_object).last()
        except:
            receipt = ""

        if not receipt:
            receipt_no =  str("01").zfill(3)

        else:
            last_receipt = receipt.receipt_no
            no = int(last_receipt) + 1
            receipt_no =  str(no).zfill(3)

        authorise = authorised_sign.objects.all()
        auth = ''
        sign = ''
        for auth in authorise:
            auth = auth.selection
        try:
            sign = authorised_sign.objects.get(id=auth).sign
        except:
            sign = ''

        mobile_no = request.POST['mobile_no']
        cash_received_from = request.POST['cash_received_from']
        amount_for = request.POST['amount_for']
        date = datetime.strptime(str(request.POST['date']), '%d-%m-%Y').strftime('%Y-%m-%d')
        # template_choice = request.POST['template_choice']
        total = request.POST['total']
        received_in_cash = request.POST.get('cash'),
        received_in_cheque = request.POST.get('cheque'),
        received_in_other = request.POST.get('other'),
       
        term_and_condition1 = request.POST.get('term_and_condition1')
        term_and_condition2 = request.POST.get('term_and_condition2')
        term_and_condition3 = request.POST.get('term_and_condition3')
        authorised = sign
        # grand_total = request.POST['grand_total']

        ### this three lines are written by yaman if needed can be deleted

        greenbilluser = GreenBillUser.objects.get(id=user_id)

        template_selected = save_template_for_receipt.objects.filter(merchant_user=greenbilluser).last()

        template = template_selected.template


        p = inflect.engine()
        rs = p.number_to_words(total)
        
        result = CustomerReceiptDetailsModels.objects.create(merchant_business_id = merchant_business_object, merchant_user = user_object, 
        receipt_no = receipt_no, mobile_number = mobile_no, cash_received_from = cash_received_from, 
        rs = rs, amount_for = amount_for, date = date, 
        total = total,received_in_cash=received_in_cash,
        received_in_cheque=received_in_cheque,
        received_in_other=received_in_other,
        authorised_sign=authorised,
        term_and_condition1 = term_and_condition1,
        term_and_condition2 = term_and_condition2,
        term_and_condition3 = term_and_condition3,
        template_choice=template,
        stamp_last_record = stamp_data_id,
        is_stamp_type = is_stamp_type,)

        letters = string.ascii_letters
        digit = string.digits
        random_string = str(result.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
        
        result.receipt_url = random_string

        result.save()

        if result:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)

class ReceiptListAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        m_business_id = request.POST['m_business_id']

        from_date = request.POST.get('from_date')

        to_date = request.POST.get('to_date')

        merchant_business_object = MerchantProfile.objects.get(id = m_business_id)

        if from_date and to_date:
            result = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_object, date__range=(from_date,to_date)).order_by("-id")
            object_list_count = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_object, date__range=(from_date,to_date)).count()
            total_cost_receipt = 0
            for object1 in result:
                if object1.total:
                    total_cost_receipt = float(object1.total) + float(total_cost_receipt)

        else:
            result = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_object).order_by("-id")
            object_list_count = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_object).count()
            total_cost_receipt = 0
            for object1 in result:
                if object1.total:
                    total_cost_receipt = float(object1.total) + float(total_cost_receipt)

        receipt_list = []

        for receipt in result:
            receipt_list.append({
                'id': receipt.id,
                'receipt_no': receipt.receipt_no,
                'mobile_number': receipt.mobile_number,
                'date': datetime.strptime(str(receipt.date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'total': float(receipt.total) if receipt.total else float(0),
                'receipt_url': "http://157.230.228.250/receipt/" + str(receipt.receipt_url) + "/",
            })

        if result:
            return JsonResponse({'status' : "success", "data": receipt_list,"from_date":from_date,"to_date":to_date, "total_cost_receipt":total_cost_receipt,"object_list_count":object_list_count}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)

class ReceiptDeleteAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        m_business_id = request.POST['m_business_id']
        merchant_business_object = MerchantProfile.objects.get(id = m_business_id)

        receipt_id = request.POST['receipt_id']

        result = CustomerReceiptDetailsModels.objects.get(id = receipt_id, merchant_business_id = merchant_business_object).delete()

        if result:
            return JsonResponse({'status' : "success"}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class ReceiptSendAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        receipt_id = request.POST['receipt_id']
        mobile_no = request.POST['mobile_no']

        receipt_object = CustomerReceiptDetailsModels.objects.get(id = receipt_id)

        business_id = receipt_object.merchant_business_id.id

        subscription_object = getActiveSubscriptionPlan(request, business_id)

        if subscription_object:
            if subscription_object.total_amount_avilable and subscription_object.per_bill_cost:

                if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

                    letters = string.ascii_letters
                    digit = string.digits
                    random_string = str(id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                    
                    receipt_object.receipt_url = random_string

                    receipt_object.save()

                    receipt_url = ""

                    device = DeviceId.objects.filter(mobile_no=mobile_no, user_type='customer').first()

                    push_service = FCMNotification(api_key=settings.API_KEY)

                    if device:

                        registration_id = device.device_id

                        message_title = "Receiving New Receipt"

                        message_body = "You have received a Payment Receipt from . " + str(receipt_object.merchant_business_id.m_business_name)

                        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

                    if mobile_no:

                        receipt_url = "http://157.230.228.250/receipt/" + str(random_string) + "/"

                        s = pyshorteners.Shortener()
                        short_url = s.tinyurl.short(receipt_url)

                        ts = int(time.time())

                        data_temp = {
                            "keyword":"Cash Receipt",
                            "timeStamp":ts,
                            "dataSet":
                                [
                                    {
                                        "UNIQUE_ID":"GB-" + str(ts),
                                        "MESSAGE":"Hey Green Bill user to view or download your receipt click on link " + short_url,
                                        "OA":"GBBILL",
                                        "MSISDN": str(mobile_no), # Recipient's Mobile Number
                                        "CHANNEL":"SMS",
                                        "CAMPAIGN_NAME":"hind_user",
                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                        "USER_NAME":"hind_hsi",
                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                        "DLT_CT_ID":"1007162098384997217", # Template Id
                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                    }
                                ]
                            }

                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                        response = requests.post(url, json = data_temp)

                        if response.status_code:
                            total_amount_avilable_new = 0
                            total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
                            subscription_object.total_amount_avilable = total_amount_avilable_new
                            subscription_object.save()
                            return JsonResponse({'status' : "success"}, status=200)
                        else:
                            return JsonResponse({'status' : "error"}, status=400)
                    else:
                        return JsonResponse({'status' : "error"}, status=400)
                else:
                    return JsonResponse({'status': 'error','message':"Insufficient Balance. Please purchase purchase Add On's and try again !!!"}, status=400)
            else:
                return JsonResponse({'status': 'error','message':"Not enough balance to send. Please recharge now. !!!"}, status=400)

        else:
            return JsonResponse({'status': 'error','message':"You don't have active Green Bill Subscription. Please purchase and try again."}, status=400)



class ReceiptSaveTemplate(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        selected_template = request.POST['template_choice'] 
        user_object = GreenBillUser.objects.get(id=user_id)

        result=save_template_for_receipt.objects.create(merchant_user=user_object, template=selected_template)
        
        if result:
            return JsonResponse({'status' : "success",'message':"Template Added Successfully."}, status=200)
        else:
            return JsonResponse({'status' : "error",'message':"Fail to Add."}, status=400)


class ReceiptTemplateExist(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        # selected_template = request.POST['selected_template'] 

        try:
            user_object = GreenBillUser.objects.get(id = user_id)
        except:
            user = None

        result = []

        # if save_template_for_receipt.objects.filter(merchant_user=user_object).exists():
        #     data = save_template_for_receipt.objects.get(merchant_user=user_object)
        #     result.append({
        #             'template_id':data.template,
        #             })
        # else:
        #     result.append({
        #             'template_id': "",
        #             })

        terms = CustomerReceiptDetailsModels.objects.filter(merchant_user=user_object).last()

        if terms:

            if terms.term_and_condition1:
                condition1 = terms.term_and_condition1
            else:
                condition1 = ""

            if terms.term_and_condition2:
                condition2 = terms.term_and_condition2
            else:
                condition2 = ""

            if terms.term_and_condition3:
                condition3 = terms.term_and_condition3
            else:
                condition3 = ""

            if save_template_for_receipt.objects.filter(merchant_user=user_object).exists():
                data = save_template_for_receipt.objects.filter(merchant_user=user_object).last()
                result.append({
                        'template_id':data.template,
                        'term1': condition1,
                        'term2': condition2,
                        'term3': condition3,
                        })

            else:
                result.append({
                        'template_id': "",
                        'term1': condition1,
                        'term2': condition2,
                        'term3': condition3,
                        })
        else:
            if save_template_for_receipt.objects.filter(merchant_user=user_object).exists():
                data = save_template_for_receipt.objects.filter(merchant_user=user_object).last()
                result.append({
                        'template_id':data.template,
                        'term1': "",
                        'term2': "",
                        'term3': "",
                        })

            else:
                result.append({
                        'template_id': "",
                        'term1': "",
                        'term2': "",
                        'term3': "",
                        })

        if result:
            return JsonResponse({'status' : "success",'data':result}, status=200)
        else:
            return JsonResponse({'status' : "error",'data':result}, status=400)


class GetSupportAndFaqsModulesAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        customer_modules = []
        customer_modules_new = []

        m_business_id = request.POST['m_business_id']

        merchant_object = MerchantProfile.objects.get(id = m_business_id)

        if merchant_object.m_business_category.id == 11:
            user_name = "petrol_pump"
        elif merchant_object.m_business_category.id == 12:
            user_name = "parking_lot"
        else:
            user_name = "other_business"

        # print(user_name)

        faqs = FAQs_Model.objects.filter(user_name = user_name)

        for faq in faqs:
            if faq.module_name in customer_modules:
                continue
            else:
                customer_modules.append(faq.module_name)

        for module in customer_modules:

            try:
                module_name_temp = Add_Module_Name.objects.get(id = module)
                module_name = module_name_temp.module_name
            except:
                module_name = ""

            if module_name:
                customer_modules_new.append({
                    'id': module,
                    'module_name': module_name,
                })

        if customer_modules_new:
            return JsonResponse({'status': 'success', 'data' : customer_modules_new}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GetSupportAndFaqsDataAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        module_id =  request.POST['module_id']
       
        faqs = FAQs_Model.objects.filter(module_name = module_id)
        
        faqs_serializer = MerchantFaqsSerializer(faqs, many=True)

        if module_id:
            return JsonResponse({'status': 'success', 'faqs' : faqs_serializer.data}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)

                
class CreateandUpdateCouponAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        coupon_type = request.POST['coupon_type']
        # coupon_logo = request.FILES['coupon_logo']
        m_user_id = request.POST['m_user_id']
        merchant_object = GreenBillUser.objects.get(id = m_user_id)
        status1 = ""
        status2 = ""
        if coupon_type == "coupon_value":
            amount_in = request.POST['amount_in']

            if amount_in == "percentage":
                coupon_val = request.POST['coupon_value_percent']
                coupon_val_per = coupon_val 

                if request.POST["coupon_id"] != "":

                    status1 = CouponModel.objects.update_or_create(id=int(request.POST["coupon_id"]),defaults={
                        "coupon_name" : request.POST['coupon_name'],
                        "valid_from" : datetime.strptime(str(request.POST['valid_from']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                        "valid_through" : datetime.strptime(str(request.POST['valid_through']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                        "coupon_code" : request.POST['coupon_code'],
                        "coupon_value" : coupon_val_per,
                        "green_point" : request.POST['green_point'],
                        # "coupon_logo" : coupon_logo,
                        "coupon_background_color":"",
                        "coupon_valid_for_user" : request.POST['coupon_valid_for_user'],
                        'merchant_business_id': request.POST['m_business_id'],
                        'amount_in' : amount_in
                        })
                        
                else:
                    status2 = CouponModel.objects.create(
                        merchant_id = merchant_object,
                        coupon_name = request.POST['coupon_name'],
                        valid_from = datetime.strptime(str(request.POST['valid_from']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                        valid_through = datetime.strptime(str(request.POST['valid_through']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                        coupon_code = request.POST['coupon_code'],
                        coupon_value = coupon_val_per + "%",
                        green_point = request.POST['green_point'],
                        # coupon_logo = request.FILES['coupon_logo'],
                        coupon_background_color = "",
                        coupon_valid_for_user = request.POST['coupon_valid_for_user'],
                        merchant_business_id = request.POST['m_business_id'],
                        amount_in = amount_in
                    )

            else:
                coupon_val = request.POST['coupon_value_fixamount']
                if request.POST["coupon_id"] != "":
                    status1 = CouponModel.objects.update_or_create(id=int(request.POST["coupon_id"]),defaults={
                        "coupon_name" : request.POST['coupon_name'],
                        "valid_from" : datetime.strptime(str(request.POST['valid_from']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                        "valid_through" : datetime.strptime(str(request.POST['valid_through']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                        "coupon_code" : request.POST['coupon_code'],
                        "coupon_value":coupon_val,
                        "green_point" : request.POST['green_point'],
                        # "coupon_logo" : request.FILES['coupon_logo'],
                        "coupon_background_color":"",
                        "coupon_valid_for_user" : request.POST['coupon_valid_for_user'],
                        'merchant_business_id': request.POST['m_business_id'],
                        'amount_in':amount_in
                        })
                    
                else:
                    status2 = CouponModel.objects.create(
                        merchant_id = merchant_object,
                        coupon_name = request.POST['coupon_name'],
                        valid_from = datetime.strptime(str(request.POST['valid_from']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                        valid_through = datetime.strptime(str(request.POST['valid_through']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                        coupon_code = request.POST['coupon_code'],
                        coupon_value = coupon_val,
                        green_point = request.POST['green_point'],
                        # coupon_logo = request.FILES['coupon_logo'],
                        coupon_background_color="",
                        coupon_valid_for_user = request.POST['coupon_valid_for_user'],
                        merchant_business_id = request.POST['m_business_id'],
                        amount_in = amount_in
                    )
        else:
            coupon_caption_name = request.POST['coupon_caption_name']
            amount_in = request.POST['amount_in']

            if request.POST["coupon_id"] != "":
                status1 = CouponModel.objects.update_or_create(id=int(request.POST["coupon_id"]),defaults={
                    "coupon_name" : request.POST['coupon_name'],
                    "valid_from" : datetime.strptime(str(request.POST['valid_from']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                    "valid_through" : datetime.strptime(str(request.POST['valid_through']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                    "coupon_code" : request.POST['coupon_code'],
                    "green_point" : request.POST['green_point'],
                    # "coupon_logo" : request.FILES['coupon_logo'],
                    "coupon_caption" : coupon_caption_name,
                    "coupon_background_color" : "",
                    "coupon_valid_for_user" : request.POST['coupon_valid_for_user'],
                    'merchant_business_id': request.POST['m_business_id'],
                    'amount_in' : amount_in
                    })

            else:
                status2 = CouponModel.objects.create(
                    merchant_id = merchant_object,
                    coupon_name = request.POST['coupon_name'],
                    valid_from = datetime.strptime(str(request.POST['valid_from']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                    valid_through = datetime.strptime(str(request.POST['valid_through']), '%d-%m-%Y').strftime('%Y-%m-%d'),
                    coupon_code = request.POST['coupon_code'],
                    green_point = request.POST['green_point'],
                    # coupon_logo = request.FILES['coupon_logo'],
                    coupon_caption = coupon_caption_name,
                    coupon_background_color = "",
                    coupon_valid_for_user = request.POST['coupon_valid_for_user'],
                    merchant_business_id = request.POST['m_business_id'],
                    amount_in = amount_in
                )

        if status1:
            return JsonResponse({'status': 'success', 'message': 'Coupon updated Successfully'}, status=200)
        elif status2:
            return JsonResponse({'status': 'success', 'message': 'Coupon created Successfully'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Fail to Create !!!'}, status=400)
            


class MerchantCouponListAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        m_business_id = request.POST['m_business_id']

        coupon_list = CouponModel.objects.filter(merchant_business_id = m_business_id).order_by('-id')
        coupon_data = []
        today = date.today()
        for coupon in coupon_list:

            if coupon.valid_through < today:
                coupon.expiry_status = True
            else:
                coupon.expiry_status = False

            user_object = GreenBillUser.objects.get(mobile_no = coupon.merchant_id)
            coupon.valid_from = datetime.strptime(str(coupon.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y')
            coupon.valid_through = datetime.strptime(str(coupon.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y')

            count_redeem = RedeemCouponModel.objects.filter(coupon_id = coupon.id ).count()


            if PromotionsAmount.objects.all():
                data = PromotionsAmount.objects.latest('id')
                coupon_amount = data.coupon_amount
            else:
                coupon_amount = 0

            if coupon.total_customers:
                coupon.total_amount = float(coupon_amount) * float(coupon.total_customers)
            else:
                coupon.total_amount = 0

            coupon_data.append({
                'id': int(coupon.id),
                'merchant_business_id': coupon.merchant_business_id,
                'coupon_name': coupon.coupon_name,
                'valid_from': coupon.valid_from,
                'valid_through': coupon.valid_through,
                'coupon_code': coupon.coupon_code,
                'coupon_value': coupon.coupon_value,
                'green_point': coupon.green_point,
                'coupon_logo': coupon.coupon_logo.url,
                'coupon_redeem': str(count_redeem),
                'coupon_caption': coupon.coupon_caption,
                'coupon_valid_for_user': coupon.coupon_valid_for_user,
                'amount_in': coupon.amount_in,
                'cout': coupon.cout,
                'coupon_panel': coupon.coupon_panel,
                'total_customers': coupon.total_customers,
                'total_amount': coupon.total_amount,
                'expired': coupon.expiry_status,
            })

        # serializer = MerchantCouponListSerializer(coupon_list, many=True)

        if coupon_list:
            return JsonResponse({'status': 'success', 'data' : coupon_data}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)

class MerchantDeleteCouponAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        coupon_id = request.POST['coupon_id']
        result = CouponModel.objects.get(id=coupon_id).delete()
        if result:
            return JsonResponse({"status": 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GetMerchantClicksOfCouponsAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        coupon_id = request.POST['coupon_id']

        count = CouponModel.objects.get(id = coupon_id).cout

        count1 = count + 1

        result = CouponModel.objects.filter(id = coupon_id).update(cout = count1)

        if result:            
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class MerchantGetOffersAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST['user_id']
        merchant_users_object = Merchant_users.objects.get(user_id = user_id)
        business_name= MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)
        merchant_name_object = business_name.m_business_name 
        merchant_state_object = business_name.m_state
        merchant_city_object = business_name.m_city
        merchant_area_object = business_name.m_area
        merchant_business_category_id = business_name.m_business_category.id

        offers = OfferModel.objects.filter(status = "1", Offer_type = "Merchant").order_by('-id')

        offers_list = []
        today = date.today()
        today_date = today.strftime("%Y-%m-%d")

        for offer in offers:
            offer_image_url = "http://157.230.228.250" + str(offer.offer_image.url)

            try:
                business_logo = "http://157.230.228.250" + str(offer.merchant_business_id.m_business_logo.url)
            except:
                business_logo = ""

            if offer.offer_panel == "owner":
                business_logo = "http://157.230.228.250" + str(offer.offer_logo.url)

            try:
                merchant_business_id = offer.merchant_business_id.id
            except:
                merchant_business_id = ""

            try:
                m_business_name = offer.merchant_business_id.m_business_name
            except:
                m_business_name = offer.o_business_name

            try:
                merchant_user = offer.merchant_user.id
            except:
                merchant_user = ""

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
                                                    offers_list.append({
                                                        "id": offer.id,
                                                        "offer_name": offer.offer_name,
                                                        "offer_caption": offer.offer_caption,
                                                        "valid_from": datetime.strptime(str(offer.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                                        "valid_through": datetime.strptime(str(offer.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                                        "offer_image": offer_image_url,
                                                        "disapproved_reason": offer.disapproved_reason,
                                                        "status": offer.status,
                                                        "Offer_type": offer.Offer_type,
                                                        "offer_business_category": offer.offer_business_category,
                                                        "created_date": offer.created_date,
                                                        "offer_panel": offer.offer_panel,
                                                        "merchant_user": merchant_user,
                                                        "merchant_business_id": merchant_business_id,
                                                        "m_business_logo": business_logo,
                                                        "m_business_name":  m_business_name,
                                                    })
                                            else:
                                                offers_list.append({
                                                    "id": offer.id,
                                                    "offer_name": offer.offer_name,
                                                    "offer_caption": offer.offer_caption,
                                                    "valid_from": datetime.strptime(str(offer.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                                    "valid_through": datetime.strptime(str(offer.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                                    "offer_image": offer_image_url,
                                                    "disapproved_reason": offer.disapproved_reason,
                                                    "status": offer.status,
                                                    "Offer_type": offer.Offer_type,
                                                    "offer_business_category": offer.offer_business_category,
                                                    "created_date": offer.created_date,
                                                    "offer_panel": offer.offer_panel,
                                                    "merchant_user": merchant_user,
                                                    "merchant_business_id": merchant_business_id,
                                                    "m_business_logo": business_logo,
                                                    "m_business_name":  m_business_name,
                                                })
                                    else:
                                        offers_list.append({
                                            "id": offer.id,
                                            "offer_name": offer.offer_name,
                                            "offer_caption": offer.offer_caption,
                                            "valid_from": datetime.strptime(str(offer.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                            "valid_through": datetime.strptime(str(offer.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                            "offer_image": offer_image_url,
                                            "disapproved_reason": offer.disapproved_reason,
                                            "status": offer.status,
                                            "Offer_type": offer.Offer_type,
                                            "offer_business_category": offer.offer_business_category,
                                            "created_date": offer.created_date,
                                            "offer_panel": offer.offer_panel,
                                            "merchant_user": merchant_user,
                                            "merchant_business_id": merchant_business_id,
                                            "m_business_logo": business_logo,
                                            "m_business_name":  m_business_name,
                                        })

        # serializer = MerchantOffersListSerializer(offers, many=True)

        if offers_list:
            return JsonResponse({'status': 'success', 'data' : offers_list}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class GetMerchantClicksOfOffersAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        offer_id = request.POST['offer_id']

        count = OfferModel.objects.get(id = offer_id).cout

        count1 = count + 1

        result = OfferModel.objects.filter(id = offer_id).update(cout = count1)

        if result:            
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)



class MerchantCreateandUpdateOffersAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        merchant_id = request.POST['merchant_id']
        merchant_object = GreenBillUser.objects.get(id = merchant_id)
        obj1 = ""
        obj2 = ""

        if request.POST['offer_id'] != "":
            offer_name = request.POST['offer_name']
            offer_caption = request.POST['offer_caption']
            valid_from = request.POST['valid_from']
            Offer_type = request.POST.get('user')
            valid_through = request.POST['valid_through']
            obj1 = OfferModel.objects.update_or_create(
                id=int(request.POST["offer_id"]), 
                defaults={"Offer_type": Offer_type, 
                "offer_name": offer_name, 
                "offer_caption": offer_caption, 
                "valid_from": datetime.strptime(str(valid_from), '%d-%m-%Y').strftime('%Y-%m-%d'),
                "valid_through": datetime.strptime(str(valid_through), '%d-%m-%Y').strftime('%Y-%m-%d'), 
                })
        else:
            merchant_business_id = request.POST['merchant_business_id']
            merchant_business_id1 = MerchantProfile.objects.get(id = merchant_business_id, m_active_account = True)
            offer_name = request.POST['offer_name']
            offer_caption = request.POST['offer_caption']
            Offer_type = request.POST['user']
            offer_image = request.FILES['offer_image']
            valid_from = request.POST['valid_from']
            valid_through = request.POST['valid_through']

       
            obj2 = OfferModel.objects.create(
                 merchant_user = merchant_object,
                 merchant_business_id = merchant_business_id1, 
                 offer_caption = offer_caption, 
                 valid_from = datetime.strptime((valid_from), '%d-%m-%Y').strftime('%Y-%m-%d'),
                 valid_through = datetime.strptime((valid_through), '%d-%m-%Y').strftime('%Y-%m-%d'), 
                 offer_image = offer_image, 
                 Offer_type = Offer_type, 
                 offer_name = offer_name
            )
            

        if obj1:
            return JsonResponse({'status': 'success', 'message': 'Offer updated Successfully'}, status=200)
        elif obj2:
            return JsonResponse({'status': 'success', 'message': 'Offer created Successfully'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Fail to Create !!!'}, status=400)


class MerchantOffersListAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        merchant_business_id = request.POST['merchant_business_id']

        offer_list = OfferModel.objects.filter(merchant_business_id = merchant_business_id).order_by('-id')

        offer_active_status = []
        today = date.today()

        if PromotionsAmount.objects.all():
            data = PromotionsAmount.objects.latest('id')
            offer_amount = data.offer_amount
        else:
            offer_amount = 0

        for offer in offer_list:
            if offer.offer_logo:
                logo = offer.offer_logo.url
            else:
                logo = ""
            if offer.valid_through < today:
                offer.expire_status=True
                available_status = False

                if not offer.customer_merchant_count:
                    offer.customer_merchant_count= 0

                total_amount = float(offer_amount) * float(offer.customer_merchant_count)

                offer_active_status.append({
                    'id': offer.id,
                    'offer_name': offer.offer_name,
                    'offer_caption': offer.offer_caption,
                    'valid_from': datetime.strptime(str(offer.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'valid_through': datetime.strptime(str(offer.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'offer_image': offer.offer_image.url,
                    'disapproved_reason': offer.disapproved_reason,
                    'status': offer.status,
                    'Offer_type': offer.Offer_type,
                    'offer_business_category': offer.offer_business_category,
                    'created_date': offer.created_date,
                    'offer_panel': offer.offer_panel,
                    'o_business_name': offer.o_business_name,
                    'offer_logo': logo,
                    'merchant_business_name': offer.merchant_business_name,
                    'check_business_category': offer.check_business_category,
                    'customer_city': offer.customer_city,
                    'customer_state': offer.customer_state,
                    'customer_area': offer.customer_area,
                    'offer_amount': offer.offer_amount,
                    'cout': offer.cout,
                    # 'merchant_user': offer.merchant_user,
                    # 'merchant_business_id': offer.merchant_business_id,
                    'active_status': available_status,
                    'total_users': offer.customer_merchant_count,
                    'total_amount': total_amount,
                    });
            else:
                available_status = True

                if not offer.customer_merchant_count:
                    offer.customer_merchant_count= 0

                total_amount = float(offer_amount) * float(offer.customer_merchant_count)

                offer_active_status.append({
                    'id': offer.id,
                    'offer_name': offer.offer_name,
                    'offer_caption': offer.offer_caption,
                    'valid_from': datetime.strptime(str(offer.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'valid_through': datetime.strptime(str(offer.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'offer_image': offer.offer_image.url,
                    'disapproved_reason': offer.disapproved_reason,
                    'status': offer.status,
                    'Offer_type': offer.Offer_type,
                    'offer_business_category': offer.offer_business_category,
                    'created_date': offer.created_date,
                    'offer_panel': offer.offer_panel,
                    'o_business_name': offer.o_business_name,
                    'offer_logo': logo,
                    'merchant_business_name': offer.merchant_business_name,
                    'check_business_category': offer.check_business_category,
                    'customer_city': offer.customer_city,
                    'customer_state': offer.customer_state,
                    'customer_area': offer.customer_area,
                    'offer_amount': offer.offer_amount,
                    'cout': offer.cout,
                    # 'merchant_user': offer.merchant_user,
                    # 'merchant_business_id': offer.merchant_business_id,
                    'active_status': available_status,
                    'total_users': offer.customer_merchant_count,
                    'total_amount': total_amount,
                    });


        for offer in offer_list:
            offer.valid_from = datetime.strptime(str(offer.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y')
            offer.valid_through = datetime.strptime(str(offer.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y')

        serializer = MerchantOffersListSerializer(offer_list, many=True)

        if offer_list:
            return JsonResponse({'status': 'success', 'data' : offer_active_status}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class MerchantDeleteOffersAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        offer_id = request.POST['offer_id']
        result = OfferModel.objects.get(id=offer_id).delete()
        if result:
            return JsonResponse({"status": 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


    
class CreatePaymentLink(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        mobile_no = request.POST['mobile_no']
        name = request.POST['name']
        email = request.POST['email']
        amount = request.POST['amount']
        description = request.POST['description']
        send_sms = request.POST['send_sms']
        m_business_id = request.POST['m_business_id']

        subscription_object = getActiveTransactionalSubscriptionPlan(request, m_business_id)

        if subscription_object:

            if int(subscription_object.total_sms_avilable) >= int(1):

                try:
                    payment_settings = MerchantPaymentSetting.objects.get(m_business_id = m_business_id)
                except:
                    payment_settings = ""

                if payment_settings:

                    result = PaymentLinks.objects.create(m_business_id = m_business_id, mobile_no = mobile_no, name = name, email = email, amount = amount, description = description)

                    try:
                        business_object = MerchantProfile.objects.get(id = m_business_id)
                    except:
                        business_object = ""
                   
                    if result and send_sms:
                        letters = string.ascii_letters
                        digit = string.digits
                        random_string = str(result.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                        PaymentLinks.objects.filter(id=result.id).update(payment_url = random_string)

                        payment_url_temp = "http://157.230.228.250/payment-link/" + str(random_string) + "/"

                        s = pyshorteners.Shortener()

                        short_url = s.tinyurl.short(payment_url_temp)

                        ts = int(time.time())

                        data_temp = {
                                "keyword":"Payment Link",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Hey Green Bill user, " + business_object.m_business_name + " has shared payment link for " + "Rs. " + result.amount + ". Click link " + short_url + " to pay now.",
                                            "OA":"GRBILL",
                                            "MSISDN": str(result.mobile_no), # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162209490097673", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                        response = requests.post(url, json = data_temp)

                    if result:
                        total_sms_avilable_new = 0
                        total_sms_avilable_new = int(subscription_object.total_sms_avilable) - int(1)
                        subscription_object.total_sms_avilable = total_sms_avilable_new
                        subscription_object.save()
                        return JsonResponse({'status': 'success'}, status=200)
                    else:
                        return JsonResponse({'status': 'error'}, status=400)
                else:
                    return JsonResponse({'status': 'error','message':'To create a Payment link. Payment setting must be done, to change the payment setting please go to Web Panel Settings => Payment Setting from the sidebar.'}, status=400)
            else:
                return JsonResponse({'status': 'error','message':'Insufficient Balance. Please purchase Transactional plan and try again !!!'}, status=400)
        else:
            return JsonResponse({'status': 'error','message':"You don't have active Transactional SMS plan. Please purchase and try again."}, status=400)

class PaymentLinkList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        m_business_id =  request.POST['m_business_id']
        
        payment_link_list = PaymentLinks.objects.filter(m_business_id = m_business_id).order_by('-id')

        payment_link = PaymentLinkListSerializer(payment_link_list, many=True)

        if payment_link_list:
            return JsonResponse({'status': 'success', 'data' : payment_link.data}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class PaymentLinkSend(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        payment_link_id = request.POST['payment_link_id']

        try:
            payment_link = PaymentLinks.objects.get(id = payment_link_id)
        except:
            payment_link = ""

        try:
            business_object = MerchantProfile.objects.get(id = payment_link.m_business_id)
        except:
            business_object = ""


        try:
            payment_settings = MerchantPaymentSetting.objects.get(m_business_id = payment_link.m_business_id)
        except:
            payment_settings = ""

        m_business_id = payment_link.m_business_id

        subscription_object = getActiveTransactionalSubscriptionPlan(request, m_business_id)

        if subscription_object:

            if int(subscription_object.total_sms_avilable) >= int(1):

                if payment_settings:

                    if payment_link and business_object:
                        letters = string.ascii_letters
                        digit = string.digits
                        random_string = str(payment_link.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                        PaymentLinks.objects.filter(id=payment_link.id).update(payment_url = random_string)

                        payment_url_temp = "http://157.230.228.250/payment-link/" + str(random_string) + "/"

                        s = pyshorteners.Shortener()

                        short_url = s.tinyurl.short(payment_url_temp)

                        ts = int(time.time())

                        data_temp = {
                                "keyword":"Payment Link",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Hey Green Bill user, " + business_object.m_business_name + " has shared payment link for " + "Rs. " + payment_link.amount + ". Click link " + short_url + " to pay now.",
                                            "OA":"GRBILL",
                                            "MSISDN": str(payment_link.mobile_no), # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162209490097673", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                        response = requests.post(url, json = data_temp)

                        if response.status_code == 200:
                            total_sms_avilable_new = 0
                            total_sms_avilable_new = int(subscription_object.total_sms_avilable) - int(1)
                            subscription_object.total_sms_avilable = total_sms_avilable_new
                            subscription_object.save()
                            return JsonResponse({'status': 'success'}, status=200)
                        else:
                            return JsonResponse({'status': 'error'}, status=400)
                    else:
                        return JsonResponse({'status': 'error'}, status=400)
                else:
                    return JsonResponse({'status': 'error','message':'To Send a Payment link. Payment setting must be done, to change the payment setting please go to Web Panel Settings => Payment Setting from the sidebar.'}, status=400)
            else:
                return JsonResponse({'status': 'error','message':'Insufficient Balance. Please purchase Transactional plan and try again !!!'}, status=400)
        else:
            return JsonResponse({'status': 'error','message':"You don't have active Transactional SMS plan. Please purchase and try again."}, status=400)

class PaymentLinkDelete(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        payment_link_id = request.POST['payment_link_id']

        try:
            instance = PaymentLinks.objects.get(id=payment_link_id, payment_done = False)
            result = instance.delete()
        except:
            result = ""

        if result:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GetSubscriptionDetails(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        m_business_id = request.POST['m_business_id']

        subscription_data = []

        try:

            business_id = m_business_id

            startswith = str(business_id) + ','
            endswith = ','+ str(business_id)
            contains = ','+ str(business_id) + ','
            exact = str(business_id)
                    
            subscription_object = merchant_subscriptions.objects.get(
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )
            if subscription_object.no_of_users:
                number_of_users = subscription_object.no_of_users
            else:
                number_of_users = "0"


            subscription_data.append({
                'per_bill_cost' : subscription_object.per_bill_cost,
                'per_receipt_cost': subscription_object.per_receipt_cost,
                'per_cash_memo_cost': subscription_object.per_cash_memo_cost,
                'per_digital_bill_cost': subscription_object.per_digital_bill_cost,
                'per_digital_receipt_cost': subscription_object.per_digital_receipt_cost,
                'per_digital_cash_memo_cost': subscription_object.per_digital_cash_memo_cost,
                'subscription_name': subscription_object.subscription_name,
                'purchase_date': datetime.strptime(str((subscription_object.purchase_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'purchase_cost': subscription_object.purchase_cost,
                'total_amount_avilable': subscription_object.total_amount_avilable,
                'expiry_date': subscription_object.expiry_date,
                'valid_for_month': subscription_object.valid_for_month,
                'number_of_users': number_of_users,
            })

            total_amount_avilable = subscription_object.total_amount_avilable

        except:
            subscription_data = []
            total_amount_avilable = 0

        promotional_sms_data = []

        try:

            business_id = m_business_id

            startswith = str(business_id) + ','
            endswith = ','+ str(business_id)
            contains = ','+ str(business_id) + ','
            exact = str(business_id)
                    
            subscription_object = promotional_sms_subscriptions.objects.get(
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )

            promotional_sms_data.append({
                'promotional_sms_subscription_name' : subscription_object.subscription_name,
                'promotional_sms_purchase_date': datetime.strptime(str((subscription_object.purchase_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'promotional_sms_purchase_cost': subscription_object.purchase_cost,
                'promotional_sms_total_sms': subscription_object.total_sms,
                'promotional_sms_per_sms_cost': subscription_object.per_sms_cost,
                'promotional_sms_total_sms_avilable': subscription_object.total_sms_avilable,
            })

            total_promotional_sms_avilable = int(subscription_object.total_sms_avilable)

            if total_promotional_sms_avilable is None:
                total_promotional_sms_avilable = 0

        except:
            bulk_sms_data = []
            total_promotional_sms_avilable = 0

        transactional_sms_data = []

        try:

            business_id = m_business_id

            startswith = str(business_id) + ','
            endswith = ','+ str(business_id)
            contains = ','+ str(business_id) + ','
            exact = str(business_id)
                    
            subscription_object = transactional_sms_subscriptions.objects.get(
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )

            transactional_sms_data.append({
                'transactional_sms_subscription_name' : subscription_object.subscription_name,
                'transactional_sms_purchase_date': datetime.strptime(str((subscription_object.purchase_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'transactional_sms_purchase_cost': subscription_object.purchase_cost,
                'transactional_sms_total_sms': subscription_object.total_sms,
                'transactional_sms_per_sms_cost': subscription_object.per_sms_cost,
                'transactional_sms_total_sms_avilable': subscription_object.total_sms_avilable,
            })

            total_transactional_sms_avilable = int(subscription_object.total_sms_avilable)

            if total_transactional_sms_avilable is None:
                total_transactional_sms_avilable = 0

        except:
            bulk_sms_data = []
            total_transactional_sms_avilable = 0


        add_on_recharge_data = []

        try:

            business_id = m_business_id

            startswith = str(business_id) + ','
            endswith = ','+ str(business_id)
            contains = ','+ str(business_id) + ','
            exact = str(business_id)
                    
            ad_ons_object = recharge_history.objects.get(
                Q(is_add_on_plan = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )

            add_on_recharge_data.append({
                'per_bill_cost' : ad_ons_object.per_bill_cost,
                'per_receipt_cost': ad_ons_object.per_receipt_cost,
                'per_cash_memo_cost': ad_ons_object.per_cash_memo_cost,
                'per_digital_bill_cost': ad_ons_object.per_digital_bill_cost,
                'per_digital_receipt_cost': ad_ons_object.per_digital_receipt_cost,
                'per_digital_cash_memo_cost': ad_ons_object.per_digital_cash_memo_cost,
                'subscription_name': ad_ons_object.subscription_name,
                'purchase_date': datetime.strptime(str((ad_ons_object.purchase_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'cost': ad_ons_object.cost,
                # 'total_amount_avilable': ad_ons_object.total_amount_avilable,
                'expiry_date': ad_ons_object.expiry_date
            })

            # total_amount_avilable = subscription_object.total_amount_avilable

        except:
            add_on_recharge_data = []
            # total_amount_avilable = 0


        if m_business_id:
            return JsonResponse({'status': 'success', 'total_amount_avilable': total_amount_avilable, 'total_promotional_sms_avilable': total_promotional_sms_avilable,
                'total_transactional_sms_avilable': total_transactional_sms_avilable, 'subscription_data' : subscription_data, 
                'promotional_sms_data': promotional_sms_data, 'transactional_sms_data': transactional_sms_data, 'add_on_recharge_data': add_on_recharge_data}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class GetSubscriptionHistory(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        m_business_id = request.POST['m_business_id']

        business_id = m_business_id

        startswith = str(business_id) + ','
        endswith = ','+ str(business_id)
        contains = ','+ str(business_id) + ','
        exact = str(business_id)
                
        recharge_his = recharge_history.objects.filter(
            Q(business_ids__startswith = startswith) | 
            Q(business_ids__endswith = endswith) | 
            Q(business_ids__contains = contains) | 
            Q(business_ids__exact = exact)
        ).order_by('-id')

        recharge_history_new = []

        for recharge in recharge_his:
            recharge.purchase_date = datetime.strptime(str((recharge.purchase_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y')
            recharge.subscription_bill_url = "http://157.230.228.250/my-subscription-bill/"+ str(recharge.id) + str("/")

            recharge_history_new.append({
                "id": recharge.id,
                "subscription_plan_id": recharge.subscription_plan_id,
                "subscription_name": recharge.subscription_name,
                "business_ids": recharge.business_ids,
                "valid_for_month": recharge.valid_for_month,
                "per_bill_cost": recharge.per_bill_cost,
                "per_receipt_cost": recharge.per_receipt_cost,
                "per_cash_memo_cost": recharge.per_cash_memo_cost,
                "per_digital_bill_cost": recharge.per_digital_bill_cost,
                "per_digital_receipt_cost": recharge.per_digital_receipt_cost,
                "per_digital_cash_memo_cost": recharge.per_digital_cash_memo_cost,
                "total_sms": recharge.total_sms,
                "per_sms_cost": recharge.per_sms_cost,
                "is_subscription_plan": recharge.is_subscription_plan,
                "is_promotional_sms_plan": recharge.is_promotional_sms_plan,
                "is_transactional_sms_plan": recharge.is_transactional_sms_plan,
                "is_add_on_plan": recharge.is_add_on_plan,
                "cost": recharge.cost,
                "purchase_date": recharge.purchase_date,
                "expiry_date": recharge.expiry_date,
                "transaction_id": recharge.transaction_id,
                "payu_transaction_id": recharge.payu_transaction_id,
                "invoice_no": recharge.invoice_no,
                "mode": recharge.mode,
                "cheque_no": recharge.cheque_no,
                "bank_transaction_id": recharge.cheque_no,
                "merchant_id": recharge.merchant_id.id,
                "subscription_bill_url": recharge.subscription_bill_url,
            })

        # recharge_history_new = RechargeHistorySerializer(recharge_his, many=True)

        if recharge_history_new:
            return JsonResponse({'status': 'success', 'data' : recharge_history_new}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GetSubscriptionPlans(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        business_category_id = request.POST['business_category_id']
        m_business_id = request.POST['m_business_id']
        result = []
        plans = subscription_plan_details.objects.filter(is_active = True).order_by('-id').distinct()

        merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

        merchant_object = GreenBillUser.objects.get(id=merchant_id)

      
        business_object = MerchantProfile.objects.get(id=m_business_id)
        merchant_state = business_object.m_state

        if merchant_state == "Maharashtra" or merchant_state == "maharashtra":

            sgst = 9
            cgst = 9
            igst = 1

        else:
            igst = 18
            sgst = 1
            cgst = 1
        subscriptions_list = []

        for plan in plans:
            if plan.user_type != "partner":
                total_cost = plan.subscription_plan_cost
                plan.including_gst = float(total_cost) - float(plan.gst_amount)
                # if plan.business_category == business_category_id:
                if plan.customized_plan_for == "merchant":

                    merchant_name_list = list(plan.merchant_name.split(","))

                    if str(m_business_id) in merchant_name_list:

                        if plan not in subscriptions_list:

                            subscriptions_list.append(plan) 

                            result.append({
                                "id":plan.id,
                                "subscription_name":plan.subscription_name,
                                "valid_for_month":plan.valid_for_month,
                                "per_bill_cost":plan.per_bill_cost,
                                "per_receipt_cost":plan.per_receipt_cost,
                                "per_cash_memo_cost":plan.per_cash_memo_cost,
                                "per_digital_bill_cost":plan.per_digital_bill_cost,
                                "per_digital_receipt_cost":plan.per_digital_receipt_cost,
                                "per_digital_cash_memo_cost":plan.per_digital_cash_memo_cost,
                                "software_maintainace_cost":plan.software_maintainace_cost,
                                "recharge_amount":plan.recharge_amount,
                                "discount_in":plan.discount_in,
                                "discount_percentage":plan.discount_percentage,
                                "discount_amount":plan.discount_amount,
                                "user_type":plan.user_type,
                                "total_amount": format(float(plan.subscription_plan_cost), ".2f"),
                                "subscription_plan_cost":plan.including_gst,
                                "business_category":plan.business_category,
                                "merchant_name":plan.merchant_name,
                                "customized_plan_for":plan.customized_plan_for,
                                "customized_plan":plan.customized_plan,
                                "suited_for":plan.suited_for,
                                "created_date":plan.created_date,
                                "is_active":plan.is_active,
                                "is_offer":plan.is_offer,
                                "number_of_users":plan.number_of_users,
                                "cost_for_users":plan.cost_for_users,
                                "gst_amount":plan.gst_amount,
                                "sgst_value" : sgst,
                                "cgst_value" : cgst,
                                "igst_value" : igst,

                            }) 

                elif plan.customized_plan_for ==  "business_category":

                    category_list = list(plan.business_category.split(","))

                    if str(business_category_id) in category_list:

                        if plan not in subscriptions_list:

                            subscriptions_list.append(plan) 

                            result.append({
                                "id":plan.id,
                                "subscription_name":plan.subscription_name,
                                "valid_for_month":plan.valid_for_month,
                                "per_bill_cost":plan.per_bill_cost,
                                "per_receipt_cost":plan.per_receipt_cost,
                                "per_cash_memo_cost":plan.per_cash_memo_cost,
                                "per_digital_bill_cost":plan.per_digital_bill_cost,
                                "per_digital_receipt_cost":plan.per_digital_receipt_cost,
                                "per_digital_cash_memo_cost":plan.per_digital_cash_memo_cost,
                                "software_maintainace_cost":plan.software_maintainace_cost,
                                "recharge_amount":plan.recharge_amount,
                                "discount_in":plan.discount_in,
                                "discount_percentage":plan.discount_percentage,
                                "discount_amount":plan.discount_amount,
                                "user_type":plan.user_type,
                                "total_amount": format(float(plan.subscription_plan_cost), ".2f"),
                                "subscription_plan_cost":plan.including_gst,
                                "business_category":plan.business_category,
                                "merchant_name":plan.merchant_name,
                                "customized_plan_for":plan.customized_plan_for,
                                "customized_plan":plan.customized_plan,
                                "suited_for":plan.suited_for,
                                "created_date":plan.created_date,
                                "is_active":plan.is_active,
                                "is_offer":plan.is_offer,
                                "number_of_users":plan.number_of_users,
                                "cost_for_users":plan.cost_for_users,
                                "gst_amount":plan.gst_amount,
                                "sgst_value" : sgst,
                                "cgst_value" : cgst,
                                "igst_value" : igst,

                            })
                else:
                    if business_category_id != "11" and business_category_id != "12":
                        result.append({
                            "id":plan.id,
                            "subscription_name":plan.subscription_name,
                            "valid_for_month":plan.valid_for_month,
                            "per_bill_cost":plan.per_bill_cost,
                            "per_receipt_cost":plan.per_receipt_cost,
                            "per_cash_memo_cost":plan.per_cash_memo_cost,
                            "per_digital_bill_cost":plan.per_digital_bill_cost,
                            "per_digital_receipt_cost":plan.per_digital_receipt_cost,
                            "per_digital_cash_memo_cost":plan.per_digital_cash_memo_cost,
                            "software_maintainace_cost":plan.software_maintainace_cost,
                            "recharge_amount":plan.recharge_amount,
                            "discount_in":plan.discount_in,
                            "discount_percentage":plan.discount_percentage,
                            "discount_amount":plan.discount_amount,
                            "user_type":plan.user_type,
                            "total_amount": format(float(plan.subscription_plan_cost), ".2f"),
                            "subscription_plan_cost":plan.including_gst,
                            "business_category":plan.business_category,
                            "merchant_name":plan.merchant_name,
                            "customized_plan_for":plan.customized_plan_for,
                            "customized_plan":plan.customized_plan,
                            "suited_for":plan.suited_for,
                            "created_date":plan.created_date,
                            "is_active":plan.is_active,
                            "is_offer":plan.is_offer,
                            "number_of_users":plan.number_of_users,
                            "cost_for_users":plan.cost_for_users,
                            "gst_amount":plan.gst_amount,
                            "sgst_value" : sgst,
                            "cgst_value" : cgst,
                            "igst_value" : igst,

                        }) 

 
        
        # plans_new = SubscriptionPlanSerializer(plans, many=True)

        if result:
            return JsonResponse({'status': 'success', 'data' : result}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GetPromotionalSMSSubscription(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        business_id = request.POST['business_id']
        merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

        # merchant_object = GreenBillUser.objects.get(id=merchant_id)
      
        business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)
        all_business = MerchantProfile.objects.get(id=business_id)

        merchant_state = all_business.m_state

        if merchant_state == "Maharashtra" or merchant_state == "maharashtra":

            sgst = 9
            cgst = 9
            igst = 1

        else:
            igst = 18
            sgst = 1
            cgst = 1

        plans = promotional_subscription_plan_model.objects.filter(is_active = True).order_by('-id')

        plans_new = []

        
        for plan in plans:

            gst_amount = plan.gst_amount
            toal_cost = plan.total_sms_cost
            plan.total_amount_with_gst = float(toal_cost) - float(gst_amount)
            if all_business.m_business_category.id !=11 and all_business.m_business_category.id != 12:
                plans_new.append({
                    "id":plan.id,
                    "subscription_name":plan.subscription_name,
                    "total_sms":plan.total_sms,
                    "per_sms_cost":plan.per_sms_cost,
                    "total_sms_cost":plan.total_amount_with_gst,
                    "total_amount":plan.total_sms_cost,
                    "discount_in":plan.discount_in,
                    "discount_percentage":plan.discount_percentage,
                    "discount_amount":plan.discount_amount,
                    "created_date":plan.created_date,
                    "is_active":plan.is_active,
                    "total_sms_avilable":plan.total_sms_avilable,
                    "gst_amount":plan.gst_amount,
                    "sgst_value" : sgst,
                    "cgst_value" : cgst,
                    "igst_value" : igst,

                    })


        if plans_new:
            return JsonResponse({'status': 'success', 'data' : plans_new}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)



        

class GetTransactionalSMSSubscription(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        business_id = request.POST['business_id'] 
        
        merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

        merchant_object = GreenBillUser.objects.get(id=merchant_id)

      
        business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)
        all_business = MerchantProfile.objects.get(id = business_id)


        # all_business = MerchantProfile.objects.filter(m_user=merchant_id , m_active_account = True)

        merchant_state = business_object.m_state

        if merchant_state == "Maharashtra" or merchant_state == "maharashtra":

            sgst = 9
            cgst = 9
            igst = 1

        else:
            igst = 18
            sgst = 1
            cgst = 1

        plans = transactional_subscription_plan_model.objects.filter(is_active = True).order_by('-id')

        plans_new = []

        for plan in plans:
            gst_amount = plan.gst_amount
            total_cost = plan.total_sms_cost
            plan.total_cost_with_gst = float(total_cost) - float(gst_amount)
            if all_business.m_business_category.id !=11 and all_business.m_business_category.id != 12:
                plans_new.append({
                    "id":plan.id,
                    "subscription_name":plan.subscription_name,
                    "total_sms":plan.total_sms,
                    "per_sms_cost":plan.per_sms_cost,
                    "total_sms_cost":plan.total_cost_with_gst,
                    "total_amount":plan.total_sms_cost,
                    "discount_in":plan.discount_in,
                    "discount_percentage":plan.discount_percentage,
                    "discount_amount":plan.discount_amount,
                    "created_date":plan.created_date,
                    "is_active":plan.is_active,
                    "total_sms_avilable":plan.total_sms_avilable,
                    "gst_amount":plan.gst_amount,
                    "sgst_value" : sgst,
                    "cgst_value" : cgst,
                    "igst_value" : igst,
                    }) 



        # plans_new = TransactionalSMSSubscriptionPlanSerializer(plans, many=True)

        if plans_new:
            return JsonResponse({'status': 'success', 'data' : plans_new}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GetAddOnRecharge(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
    
        business_id = request.POST['business_id'] 

        merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

        merchant_object = GreenBillUser.objects.get(id=merchant_id)

        business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)

        # all_business = MerchantProfile.objects.filter(m_user=merchant_id , m_active_account = True)
        all_business = MerchantProfile.objects.get(id = business_id)

        merchant_state = all_business.m_state

        if merchant_state == "Maharashtra" or merchant_state == "maharashtra":

            sgst = 9
            cgst = 9
            igst = 1

        else:
            igst = 18
            sgst = 1
            cgst = 1


        addons_plans = add_on_plan_model.objects.all().filter(is_active=True).order_by('-id')
        # subscription_object = ""
        # for business in all_business:
        #     business_id = business.id
        #     startswith = str(business_id) + ','
        #     endswith = ','+ str(business_id)
        #     contains = ','+ str(business_id) + ','
        #     exact = str(business_id)

        #     try:  
        #         subscription_object = merchant_subscriptions.objects.get(
        #             Q(merchant_id = merchant_object),
        #             Q(is_active = True),
        #             Q(business_ids__startswith = startswith) | 
        #             Q(business_ids__endswith = endswith) | 
        #             Q(business_ids__contains = contains) | 
        #             Q(business_ids__exact = exact)
        #         )
        #     except:
        #         subscription_object = ""


        plans_new = []
        for plan in addons_plans:
            adon_gst_amount = plan.gst_amount
            total_adon_cost = plan.recharge_amount
            plan.total_adon_cost_with_gst = float(total_adon_cost) - float(adon_gst_amount)
        
            plans_new.append({
                "id":plan.id,
                "add_on_name":plan.add_on_name,
                "per_bill_cost":plan.per_bill_cost,
                "per_receipt_cost":plan.per_receipt_cost,
                "per_cash_memo_cost":plan.per_cash_memo_cost,
                "per_digital_bill_cost":plan.per_digital_bill_cost,
                "per_digital_receipt_cost":plan.per_digital_receipt_cost,
                "per_digital_cash_memo_cost":plan.per_digital_cash_memo_cost,
                "recharge_amount":plan.total_adon_cost_with_gst,
                "total_amount":plan.recharge_amount,
                "created_date":plan.created_date,
                "is_active":plan.is_active,
                "gst_amount":plan.gst_amount,
                "sgst_value" : sgst,
                "cgst_value" : cgst,
                "igst_value" : igst,
                })

        if plans_new:
            return JsonResponse({'status': 'success', 'data' : plans_new}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GetAddOnAmounts(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        plan_id = request.POST['plan_id']

        try:
            addons_plans = add_on_plan_model.objects.get(id=plan_id)
        # print('addons_plans',addons_plans)
            list1 = []

            filtered_amount_list = []

            if addons_plans.recharge_amount_one:
                if addons_plans.recharge_amount_one not in list1:
                    if addons_plans.recharge_amount_one != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_one
                        })

            if addons_plans.recharge_amount_two:
                if addons_plans.recharge_amount_two not in list1:
                    if addons_plans.recharge_amount_two != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_two
                        })

            if addons_plans.recharge_amount_three: 
                if addons_plans.recharge_amount_three not in list1:
                    if addons_plans.recharge_amount_three != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_three
                        })

            if addons_plans.recharge_amount_four:
                if addons_plans.recharge_amount_four not in list1:
                    if addons_plans.recharge_amount_four != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_four
                        })

            if addons_plans.recharge_amount_five:
                if addons_plans.recharge_amount_five not in list1:
                    if addons_plans.recharge_amount_five != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_five
                        })

            if addons_plans.recharge_amount_six:
                if addons_plans.recharge_amount_six not in list1:
                    if addons_plans.recharge_amount_six != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_six
                        })

            if addons_plans.recharge_amount_seven:
                if addons_plans.recharge_amount_seven not in list1:
                    if addons_plans.recharge_amount_seven != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_seven
                        })

            if addons_plans.recharge_amount_eight:
                if addons_plans.recharge_amount_eight not in list1:
                    if addons_plans.recharge_amount_eight != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_eight
                        })

            if addons_plans.recharge_amount_nine:
                if addons_plans.recharge_amount_nine not in list1:
                    if addons_plans.recharge_amount_nine != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_nine
                        })

            if addons_plans.recharge_amount_ten:
                if addons_plans.recharge_amount_ten not in list1:
                    if addons_plans.recharge_amount_ten != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_ten
                        })

            if addons_plans.recharge_amount_eleven:
                if addons_plans.recharge_amount_eleven not in list1:
                    if addons_plans.recharge_amount_eleven != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_eleven
                        })

            if addons_plans.recharge_amount_twelve:
                if addons_plans.recharge_amount_twelve not in list1:
                    if addons_plans.recharge_amount_twelve != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_twelve
                        })

            if addons_plans.recharge_amount_thirteen:
                if addons_plans.recharge_amount_thirteen not in list1:
                    if addons_plans.recharge_amount_thirteen != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_thirteen
                        })

            if addons_plans.recharge_amount_fourteen:
                if addons_plans.recharge_amount_fourteen not in list1:
                    if addons_plans.recharge_amount_fourteen != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_fourteen
                        })

            if addons_plans.recharge_amount_fifteen:
                if addons_plans.recharge_amount_fifteen not in list1:
                    if addons_plans.recharge_amount_fifteen != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_fifteen
                        })

            if addons_plans.recharge_amount_sixteen:
                if addons_plans.recharge_amount_sixteen not in list1:
                    if addons_plans.recharge_amount_sixteen != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_sixteen
                        })

            if addons_plans.recharge_amount_seventeen:
                if addons_plans.recharge_amount_seventeen not in list1:
                    if addons_plans.recharge_amount_seventeen != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_seventeen
                        })

            if addons_plans.recharge_amount_eighteen:
                if addons_plans.recharge_amount_eighteen not in list1:
                    if addons_plans.recharge_amount_eighteen != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_eighteen
                        })

            if addons_plans.recharge_amount_nineteen:
                if addons_plans.recharge_amount_nineteen not in list1:
                    if addons_plans.recharge_amount_nineteen != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_nineteen
                        })

            if addons_plans.recharge_amount_twenty:
                if addons_plans.recharge_amount_twenty not in list1:
                    if addons_plans.recharge_amount_twenty != '':
                        list1.append({
                            "all_recharge_amount": addons_plans.recharge_amount_twenty
                        })

            result = True
        except:
            result = False


        if result:
            return JsonResponse(list1, status=200, safe=False)
            # return JsonResponse(serializer.data, status=200, safe=False)
        else:
            return JsonResponse({'status': "error"}, status=400)


class GetRechargeHistoryDetails(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST['user_id']

        m_business_id = request.POST['m_business_id']

        merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

        merchant_object = GreenBillUser.objects.get(id=merchant_id)

        startswith = str(m_business_id) + ','
        endswith = ','+ str(m_business_id)
        contains = ','+ str(m_business_id) + ','
        exact = str(m_business_id)

        recharge_his = recharge_history.objects.filter(
            Q(merchant_id = merchant_object),
            Q(business_ids__startswith = startswith) | 
            Q(business_ids__endswith = endswith) | 
            Q(business_ids__contains = contains) | 
            Q(business_ids__exact = exact)
        ).order_by('-id')

        result = []

        for recharge in recharge_his:

            if recharge.is_subscription_plan == True:
                try:
                    subscription = subscription_plan_details.objects.get(id=recharge.subscription_plan_id)
                    subscription_type = "Green Bill Subscription"
                        
                    users_cost = float(recharge.no_of_users) * float(recharge.valid_for_month) * float(subscription.cost_for_users)
                    final_amount = float(users_cost) + float(recharge.cost) + float(recharge.gst_amount)
                except:
                    final_amount = 0
                    

            # elif recharge.is_add_on_plan == True: 
            #     final_amount = float(recharge.cost) + float(recharge.gst_amount) 

            # if recharge.is_subscription_plan == True:

            #     subscription_type = "Green Bill Subscription"

            #     subscription_plan = subscription_plan_details.objects.filter(id=recharge.subscription_plan_id)

            #     for subscription in subscription_plan:

            #         try:
            #             users_cost = float(recharge.no_of_users) * float(recharge.valid_for_month) * float(subscription.cost_for_users)
            #             final_amount = float(users_cost) + float(recharge.cost) + float(recharge.gst_amount)
            #         except:
            #             final_amount = 0

            elif recharge.is_promotional_sms_plan == True:

                subscription_type = "Promotional SMS Plan"

                final_amount = recharge.cost

            elif recharge.is_transactional_sms_plan == True:

                subscription_type = "Transactional SMS Plan"

                final_amount = recharge.cost

            elif recharge.is_add_on_plan == True:

                subscription_type = "Add On's Plan"

                final_amount = float(recharge.cost) + float(recharge.gst_amount) 

            if recharge.transaction_id:
                transaction_id = recharge.transaction_id
            else: 
                transaction_id = ""

            if recharge.mode:
                recharge_mode = recharge.mode
                if recharge.mode == 'bank':
                    recharge_mode_id = recharge.bank_transaction_id
                elif recharge.mode == 'cheque':
                    recharge_mode_id = recharge.cheque_no
                else:
                    recharge_mode_id = ""
            else:
                recharge_mode_id = ""
                recharge_mode = "PayU"
                


            purchase_date = timezone.localtime(recharge.purchase_date).strftime("%Y-%m-%d")

            result.append({
                'bill_id': recharge.id,
                'date': datetime.strptime(str(purchase_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'subscription_type': subscription_type,
                'recharge_mode': recharge_mode,
                "recharge_mode_id": recharge_mode_id,
                'transaction_id': transaction_id,
                'amount': str(final_amount),
                'business': 'Green Bill',
                'url': "http://157.230.228.250/my-subscription-bill/" + str(recharge.id) + "/"
                
            })

        if result:
            return JsonResponse({'status': "success", "result":result}, status=200)

        else:
            return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)


class GetReceivedBill(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        m_business_id = request.POST['m_business_id']

        from_date = request.POST.get('from_date')

        to_date = request.POST.get('to_date')

        merchant_objects = MerchantProfile.objects.get(id = m_business_id).m_user

        all_bills = MerchantBill.objects.filter(bill_received_business_name = m_business_id).order_by("-id")

        bills_new = []

        for bill in all_bills:
            try:
                business_id = bill.business_name.id
                business_name = bill.business_name.m_business_name
            except:
                business_name = ""

            bill_url = "http://157.230.228.250/my-bill-merchant/" + str(bill.bill_url) + "/"

            bills_new.append({
                "bill_id":bill.id,
                "invoice_no": bill.invoice_no,
                "bill_amount": str(bill.bill_amount),
                "bill_date": datetime.strptime(str((bill.bill_date)), '%Y-%m-%d').strftime('%d-%m-%Y'),
                "business_name": business_name,
                "bill_url" : bill_url,
                "bill_image" : bill.bill.url,
                'created_at': str(bill.created_at),
            })

        startswith = str(m_business_id) + ','
        endswith = ','+ str(m_business_id)
        contains = ','+ str(m_business_id) + ','
        exact = str(m_business_id)

        recharge_his = recharge_history.objects.filter(
            Q(merchant_id = merchant_objects),
            Q(business_ids__startswith = startswith) | 
            Q(business_ids__endswith = endswith) | 
            Q(business_ids__contains = contains) | 
            Q(business_ids__exact = exact)
        ).order_by('-id')

        for recharge in recharge_his:
            if recharge.is_subscription_plan == True:
                subscription_plan = subscription_plan_details.objects.filter(id=recharge.subscription_plan_id)
                
                for subscription in subscription_plan:

                    try:
                        users_cost = float(recharge.no_of_users) * float(recharge.valid_for_month) * float(subscription.cost_for_users)
                        final_amount = float(users_cost) + float(recharge.cost) + float(recharge.gst_amount)
                    except:
                        final_amount = 0
            else:
                final_amount = recharge.cost


            purchase_date = timezone.localtime(recharge.purchase_date).strftime("%Y-%m-%d")
            try:
                bills_new.append({
                    'bill_id': recharge.id,
                    'invoice_no': recharge.invoice_no,
                    'bill_amount': str(final_amount),
                    'bill_date': datetime.strptime(str(purchase_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'business_name': 'Green Bill',
                    "bill_url" : "http://157.230.228.250/my-subscription-bill/"+ str(recharge.id) + str("/"),
                    "bill_image" : "",
                    'created_at': str(recharge.purchase_date),
                })
            except:
                pass

        # bills_new.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)
        bills_new.sort(key = lambda x: x['created_at'], reverse = True)

        

        new_data = []

        if from_date and to_date:

            if bills_new:
                if from_date:
                    from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')
                    
                if to_date:
                    to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')
                    
                for bill in bills_new:
                    
                    if from_date and to_date:
                        bill_date = datetime.strptime(str(bill['bill_date']), '%d-%m-%Y').strftime('%Y-%m-%d')

                        if bill_date >= from_date and bill_date <= to_date:
                            new_data.append(bill)
  
            # new_data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)
            new_data.sort(key = lambda x: x['created_at'], reverse = True)

            received_amount = 0
            received_bills = 0

            # for z in new_data:
            #     received_amount =  float(received_amount) + float(z['amount'])
            #     received_bills = len(new_data)

            if new_data:
                return JsonResponse({'status': "success", "data":new_data, 
                     "from_date": from_date, "to_date": to_date}, status=200)
            else:
                return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)
        else:

            if bills_new:
                return JsonResponse({'status': 'success', 'data' : bills_new,
                    "from_date":"", "to_date":""}, status=200)
            else:
                return JsonResponse({'status': 'error'}, status=400)


class SendReceivedBill(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        bill_id = request.POST["bill_id"]
        business_id = request.POST["business_id"]
        if business_id == 'customer':
            merchant_bill = MerchantBill.objects.filter(id = bill_id)

            letters = string.ascii_letters
            digit = string.digits
            random_string = str(merchant_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

            customer_bill = CustomerBill.objects.create(user_id = merchant_bill[0].user_id, mobile_no = merchant_bill[0].mobile_no,
                email = merchant_bill[0].email, bill = merchant_bill[0].bill, business_name = merchant_bill[0].business_name,
                invoice_no = merchant_bill[0].invoice_no, green_bill_transaction = merchant_bill[0].green_bill_transaction, green_bill_print_transaction = merchant_bill[0].green_bill_print_transaction,
                print_transaction = merchant_bill[0].print_transaction, bill_amount = merchant_bill[0].bill_amount, customer_bill_category = merchant_bill[0].customer_bill_category,stamp_id=merchant_bill[0].stamp_id, exe_bill_type = merchant_bill[0].exe_bill_type
            )

            history_result1 = sent_bill_history.objects.create(user_id = merchant_bill[0].user_id,
                mobile_no = merchant_bill[0].mobile_no, m_business_id = merchant_bill[0].business_name.id, green_bill_print_transaction = merchant_bill[0].green_bill_print_transaction,
                print_transaction = merchant_bill[0].print_transaction, bill_amount = merchant_bill[0].bill_amount,
                customer_bill = True
            )

            customer_bill_new = CustomerBill.objects.filter(id=customer_bill.id).update(bill_url = random_string) 

            MerchantBill.objects.filter(id =bill_id).delete()

            if customer_bill:
                return JsonResponse({'status': 'success', 'message' : 'Bill Transfer successfully !!!'}, status=200)
            else:
                return JsonResponse({'status': 'error','message' : 'Failed to Transfer!!!'}, status=400)
        else:

            merchant_bill = MerchantBill.objects.filter(id =bill_id)

            letters = string.ascii_letters
            digit = string.digits
            random_string = str(merchant_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

            merchant_bill1 = MerchantBill.objects.create(user_id = merchant_bill[0].user_id, mobile_no = merchant_bill[0].mobile_no, email = merchant_bill[0].email,
                bill = merchant_bill[0].bill, business_name = merchant_bill[0].business_name, bill_received_business_name = business_id,
                invoice_no = merchant_bill[0].invoice_no, green_bill_transaction = merchant_bill[0].green_bill_transaction, green_bill_print_transaction = merchant_bill[0].green_bill_print_transaction,
                print_transaction = merchant_bill[0].print_transaction, bill_amount = merchant_bill[0].bill_amount, customer_bill_category = merchant_bill[0].customer_bill_category,stamp_id=merchant_bill[0].stamp_id, exe_bill_type = merchant_bill[0].exe_bill_type
            )

            merchant_bill_new = MerchantBill.objects.filter(id=merchant_bill1.id).update(bill_url = random_string) 

            merchant_bill = MerchantBill.objects.filter(id =bill_id).delete()

            if merchant_bill1:
                return JsonResponse({'status': 'success', 'message' : 'Bill Transfer successfully !!!'}, status=200)
            else:
                return JsonResponse({'status': 'error','message' : 'Failed to Transfer!!!'}, status=400)
       



class GetRejectedBill(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        merchant_business_id = request.POST['merchant_business_id']

        from_date = request.POST.get('from_date')

        to_date = request.POST.get('to_date')

        base_url = "http://157.230.228.250/"

        data = []

        parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, reject_status = True).order_by('-id')
        
        for bill in parking_bill_list:
            try:
                bill_file = str(base_url) + str(bill.bill_file.url)
            except:
                bill_file = ""

            if bill.is_checkoutpin == True:
                try:
                    mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                except:
                    mobile_no = bill.mobile_no
            else:
                mobile_no = bill.mobile_no

            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': mobile_no,
                'amount': str(bill.amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SaveParkingLotBill",
                'customer_added': False,
                'reject_status':bill.reject_status,
            })
               

        petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, reject_status = True).order_by('-id')
        
        for bill in petrol_bill_list:
            try:
                bill_file = str(base_url) + str(bill.bill_file.url)
            except:
                bill_file = ""

            if bill.is_checkoutpin == True:
                try:
                    mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                except:
                    mobile_no = bill.mobile_no
            else:
                mobile_no = bill.mobile_no
                
            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': mobile_no,
                'amount': str(bill.total_amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SavePetrolPumpBill",
                'customer_added': False,
                'reject_status':bill.reject_status,
            })

        merchant_object = MerchantProfile.objects.get(id = merchant_business_id)

        customer_bill = CustomerBill.objects.filter(business_name = merchant_object, customer_added = False, reject_status = True).order_by('-id')

        for bill in customer_bill:
            try:
                bill_file = str(base_url) + str(bill.bill.url)
            except:
                bill_file = ""

            if bill.is_checkoutpin == True:
                try:
                    mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                except:
                    mobile_no = bill.mobile_no
            else:
                mobile_no = bill.mobile_no

            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': mobile_no,
                'amount': str(bill.bill_amount),
                'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "CustomerBill",
                'customer_added': False,
                'reject_status':bill.reject_status,
            })

        merchant_bill = MerchantBill.objects.filter(business_name = merchant_object, reject_status = True)

        for bill in merchant_bill:
            try:
                bill_file = str(base_url) + str(bill.bill.url)
            except:
                bill_file = ""

            if bill.is_checkoutpin == True:
                try:
                    mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                except:
                    mobile_no = bill.mobile_no
            else:
                mobile_no = bill.mobile_no
                
            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': mobile_no,
                'amount': str(bill.bill_amount),
                'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "MerchantBill",
                'customer_added': False,
                'reject_status':bill.reject_status,
            })

        data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

        new_data = []
        if from_date and to_date:
            if data:
                if from_date:
                    from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

                if to_date:
                    to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

                for bill in data:
                        bill_date = datetime.strptime(str(bill['bill_date']), '%d-%m-%Y').strftime('%Y-%m-%d')
                        if from_date and to_date:
                            
                            if bill_date >= from_date and bill_date <= to_date:
                                new_data.append(bill)

                new_data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

                if new_data:
                    return JsonResponse({'status': "success", "data":new_data, 
                         "from_date": from_date, "to_date": to_date}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)
        else:

            if data:
                return JsonResponse({"status": "success", "data" : data, "to_date":"","from_date":"" }, status=200)
            else:
                return JsonResponse({'status': 'error'}, status=400)


class DeleteRejectedBill(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        db_table = request.POST['db_table']

        bill_id = request.POST['bill_id']

        if db_table == "SaveParkingLotBill":
            result = SaveParkingLotBill.objects.filter(id = bill_id).delete()

        elif db_table == "SavePetrolPumpBill":
            result = SavePetrolPumpBill.objects.filter(id = bill_id).delete()

        elif db_table == "CustomerBill":
            result = CustomerBill.objects.filter(id = bill_id).delete()

        elif db_table == "MerchantBill":
            result = MerchantBill.objects.filter(id = bill_id).delete()

        if result:
            return JsonResponse({'status': "success", "message":"Bill Deleted Successfully"}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to Delete"}, status=400)




class GetPaymentHistory(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        business_id = request.POST['merchant_business_id']

        from_date = request.POST.get('from_date')

        to_date = request.POST.get('to_date')
        # user_id = request.POST['user_id']

        # merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

        # merchant_object = GreenBillUser.objects.get(id=merchant_id)

        # business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)

        # business_id = business_object.id

        startswith = str(business_id) + ','
        endswith = ','+ str(business_id)
        contains = ','+ str(business_id) + ','
        exact = str(business_id)
                
        count1 = 0
        count2 = 0
        count3 = 0
        total_transaction_count = 0
        payment_history = recharge_history.objects.filter(
            # Q(merchant_id = merchant_object),
            Q(business_ids__startswith = startswith) | 
            Q(business_ids__endswith = endswith) | 
            Q(business_ids__contains = contains) | 
            Q(business_ids__exact = exact)
        ).order_by('-id')

        payment_history_new = []
        for history in payment_history:
            count1 = count1 + 1
            history.cost = format(history.cost, ".2f") if history.cost else float(0)
            history.purchase_date = datetime.strptime(str((history.purchase_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y')
            history.subscription_bill_url = "http://157.230.228.250/my-subscription-bill/"+ str(history.id) + str("/")


        # payment_history_new = PaymentHistorySerializer(payment_history, many=True)

            payment_history_new.append({
                    "id": history.id,
                    "business":"Green Bill",
                    "description":history.subscription_name,
                    "transaction_id":history.transaction_id,
                    "mode": 'PayU' if history.transaction_id else history.mode,
                    "purchase_date":history.purchase_date,
                    "cost":float(history.cost),
                    "subscription_bill_url": history.subscription_bill_url,
                })


        merchant_bill = MerchantBill.objects.filter(bill_received_business_name = business_id, payment_done = True).order_by('-id')
        for history in merchant_bill:
            count2 = count2 + 1
            history.cost = format(history.bill_amount, ".2f")
            if history.payment_date:
                history.purchase_date = datetime.strptime(str((history.payment_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y')
            else:
                history.purchase_date = ""

            if history.payment_date:
                payment_history_new.append({
                    "id":history.id,
                    "business":history.business_name.m_business_name,
                    "description":"Bill Payment",
                    "transaction_id":history.transaction_id,
                    "mode": 'PayU' if history.transaction_id else '',
                    "purchase_date":history.purchase_date,
                    "cost":float(history.cost),
                    "bill_url":history.bill_url,
                    })

        my_ads_payment = PromotionsPaymentHistory.objects.filter(merchant_business_id = business_id, payment_done = True).order_by('-id')

        for history in my_ads_payment:
            count3 = count3 + 1
            history.cost = history.payment_amount

            if history.payment_date:
                history.purchase_date = datetime.strptime(str((history.payment_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y')
            else:
                history.purchase_date = ""

            if history.payment_date:
                payment_history_new.append({
                    "id":history.id,
                    "business":history.merchant_business_id.m_business_name,
                    "description":"Third Party Ads",
                    "transaction_id":history.transaction_id,
                    "mode": 'PayU' if history.transaction_id else '',
                    "purchase_date":history.purchase_date,
                    "cost":float(history.cost),
                    "bill_url": "",
                    })

        merchant_business_id = MerchantProfile.objects.get(id = business_id, m_active_account = True)
        data = OfferModel.objects.filter(merchant_business_id = merchant_business_id,offer_panel='merchant', status=1).order_by("-id")

        if PromotionsAmount.objects.all():
            amount = PromotionsAmount.objects.latest('id')
            offer_amount = amount.offer_amount
        else:
            offer_amount = 0

        today = date.today()
        total_amount_spent = 0.0

        for offer in data:
            # if offer.valid_through >= today:
            count3 = count3 + 1

            payment_history_new.append({
                "id":0,
                "business":"Offer",
                "description": offer.offer_name,
                "transaction_id": None,
                "mode": "",
                "purchase_date": datetime.strptime(str((offer.created_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                "cost": float(offer_amount) * float(offer.customer_merchant_count),
                "bill_url": "",
            })
            total_amount_spent = total_amount_spent + (float(offer_amount) * float(offer.customer_merchant_count))

        coupon_merchant_id = MerchantProfile.objects.get(id = business_id, m_active_account = True).id

        coupon_list = CouponModel.objects.filter(merchant_business_id = coupon_merchant_id, coupon_panel = "merchant").order_by('-id')

        if PromotionsAmount.objects.all():
            data = PromotionsAmount.objects.latest('id')
            coupon_amount = data.coupon_amount
        else:
            coupon_amount = 0

        today = date.today()
        for coupon in coupon_list:
            # if coupon.valid_through >= today:
            count3 = count3 + 1

            payment_history_new.append({
                "id":0,
                "business":"Coupon",
                "description": coupon.coupon_name,
                "transaction_id": None,
                "mode": "",
                "purchase_date": datetime.strptime(str((datetime(coupon.valid_from.year, coupon.valid_from.month, coupon.valid_from.day)).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                "cost": float(coupon_amount) * float(coupon.total_customers),
                "bill_url": "",
            })

            total_amount_spent = total_amount_spent + (float(coupon_amount) * float(coupon.total_customers))
        
        total_transaction_count = count1 + count2 + count3

        payment_history_new.sort(key = lambda x: datetime.strptime(x['purchase_date'], '%d-%m-%Y'), reverse = True)

        for payment in payment_history_new:
            if payment['business'] != "Offer" and payment['business'] != "Coupon":
                if payment["cost"] != 0:
                    total_amount_spent = total_amount_spent + payment["cost"]


        # for bill in sorted_payment_history:
        #     bill['purchase_date_new'] = datetime.strptime(str(bill['purchase_date']), '%m-%d-%Y').strftime('%m-%d-%Y') if bill['purchase_date'] else ""
        new_data = []
        count = 0
        if from_date and to_date:
            if payment_history_new:
                if from_date:
                    from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

                if to_date:
                    to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

                for bill in payment_history_new:
                    if from_date and to_date:
                        purchase_date_new = datetime.strptime(str(bill['purchase_date']), '%d-%m-%Y').strftime('%Y-%m-%d')
                        if purchase_date_new >= from_date and purchase_date_new <= to_date:
                            count = count + 1
                            new_data.append(bill)

                new_data.sort(key = lambda x: datetime.strptime(x['purchase_date'], '%d-%m-%Y'), reverse = True)

                total_amount_spent = 0
                total_transaction_count = count
                for payment in new_data:
                    if payment['cost']:
                        total_amount_spent = total_amount_spent + float(payment['cost'])

            if new_data:
                return JsonResponse({'status': "success", "data":new_data, 'total_amount_spent': format(total_amount_spent, ".2f"), 'total_transaction_count': total_transaction_count, "from_date": from_date, "to_date": to_date}, status=200)
            else:
                return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)
        else:

            if payment_history_new:
                return JsonResponse({'status': 'success', 'data' : payment_history_new,"from_date":"","to_date":"",'total_amount_spent': format(total_amount_spent, ".2f"), 'total_transaction_count': total_transaction_count}, status=200)
            else:
                return JsonResponse({'status': 'No data found.'}, status=400)


class GetPaymentReceived(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        business_id = request.POST['merchant_business_id']

        from_date = request.POST.get('from_date')

        to_date = request.POST.get('to_date')

        payment_received_data = []

        received_payments = PaymentLinks.objects.filter(m_business_id = business_id, payment_done = True).order_by('-id')
        for payment in received_payments:
            if payment.description:
                description = payment.description
            else:
                description = ''

            payment_received_data.append({
                'mobile_no': payment.mobile_no,
                'amount' : format(float(payment.amount), ".2f"),
                'payment_date' : payment.payment_date,
                'transaction_id' : payment.transaction_id,
                'created_at' : payment.created_at,
                'payment_date_new':datetime.strptime(str(payment.payment_date.date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'description':  description,
            })

            payment.payment_date = datetime.strptime(str(payment.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d')
    

        customer_bill = CustomerBill.objects.filter(business_name = business_id,payment_done = True)
        for customer in customer_bill:
            payment_received_data.append({
                'mobile_no': customer.mobile_no,
                'amount' : format(float(customer.bill_amount), ".2f"),
                'payment_date' : customer.payment_date,
                'transaction_id' : customer.transaction_id,
                'created_at' : customer.created_at,
                'payment_date_new':datetime.strptime(str(customer.payment_date.date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'description':  '',
            })


        merchant_bill = MerchantBill.objects.filter(business_name = business_id,payment_done = True)        
        for merchant in merchant_bill:
            payment_received_data.append({
                'mobile_no': merchant.mobile_no,
                'amount' : format(float(merchant.bill_amount), ".2f"),
                'payment_date' : merchant.payment_date if merchant.payment_date else "",
                'transaction_id' : merchant.transaction_id,
                'created_at' : merchant.created_at,
                'payment_date_new':datetime.strptime(str(merchant.payment_date.date()), '%Y-%m-%d').strftime('%d-%m-%Y') if merchant.payment_date else "",
                'description':  '',
            })


        parking_bill = SaveParkingLotBill.objects.filter(m_business_id = business_id, payment_done = True) 
        for parking in parking_bill:
            payment_received_data.append({
                'mobile_no': parking.mobile_no,
                'amount' : format(float(parking.amount), ".2f"),
                'payment_date' : parking.payment_date,
                'transaction_id' : parking.transaction_id,
                'created_at' : parking.created_at,
                'payment_date_new':datetime.strptime(str(parking.payment_date.date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'description':  '',
            })

        petrol_bill = SavePetrolPumpBill.objects.filter(m_business_id = business_id, payment_done=True)
        for petrol in petrol_bill:
            payment_received_data.append({
                'mobile_no': petrol.mobile_no,
                'amount' : format(float(petrol.amount), ".2f"),
                'payment_date' : petrol.payment_date,
                'transaction_id' : petrol.transaction_id,
                'created_at' : petrol.created_at,
                'payment_date_new' : datetime.strptime(str(petrol.payment_date.date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'description':  '',
            })

        total_payments_count =  len(payment_received_data)

        total_payment = 0.00

        for payment in payment_received_data:
            total_payment = total_payment + float(payment['amount'])

        new_data = []

        if from_date and to_date:
            if payment_received_data:
                if from_date:
                    from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

                if to_date:
                    to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

                for bill in payment_received_data:
                    payement_bill_date = datetime.strptime(str(bill['payment_date_new']), '%d-%m-%Y').strftime('%Y-%m-%d')
                    if payement_bill_date >= from_date and payement_bill_date <= to_date:
                        new_data.append(bill)

                # new_data.sort(key = lambda x: datetime.strptime(x['payment_date_new'], '%d-%m-%Y'), reverse = True)
                total_payment = 0.00
                total_payments_count = 0

                for payment in new_data:
                    total_payment = total_payment + float(payment['amount'])

                total_payments_count = len(new_data)

            if new_data:
                return JsonResponse({'status': "success", "data":new_data, 
                "from_date": from_date, "to_date": to_date,"total_payment_received": float(total_payment), "total_payments_received_count": total_payments_count}, status=200)
            else:
                return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)
        else:

            if payment_received_data:
                return JsonResponse({"status": "success", "data" : payment_received_data,"from_date": "", "to_date": "", "total_payment_received": float(total_payment), "total_payments_received_count": total_payments_count}, status=200)
            else:
                return JsonResponse({'status': 'error'}, status=400)


class GetBillRating(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        merchant_business_id = request.POST['merchant_business_id']

        merchant_rating = request.POST.get('merchant_rating')

        merchant_business_object = MerchantProfile.objects.get(id = merchant_business_id)

        all_bills = CustomerBill.objects.filter(business_name = merchant_business_object).order_by('-id')

        new_list = []

        if merchant_rating:
            merchant_rating_count = CustomerBill.objects.filter(business_name = merchant_business_object, rating = merchant_rating).count()
        else:
            merchant_rating_count = 0
            for bill in all_bills:
                if bill.rating:
                    merchant_rating_count = merchant_rating_count + 1

        for bill in all_bills:

            if bill:
                try:
                    bill_design_object = bill_designs.objects.get(merchant_business_id = merchant_business_id)
                    bill_rating_emoji = bill_design_object.rating_emoji
                except:
                    testingstring = '\U0001f604'
                    bill_rating_emoji = testingstring.encode('unicode_escape')
                    # bill_rating_emoji = '😊'

                ratings = ""
                rating_id = ""

                if bill.rating:

                    rating_id = bill.rating

                    for x in range(int(bill.rating)):
                        ratings = " ".join((ratings, bill_rating_emoji))


                bill.rating = ratings

                bill.bill_date = datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y')

                bill.bill_amount = "{:.2f}".format(bill.bill_amount)

                if bill.rating:

                    new_list.append({
                        "id": bill.id,
                        "user_id": bill.user_id,
                        "mobile_no": bill.mobile_no,
                        "bill_amount": bill.bill_amount,
                        "bill_date": bill.bill_date,
                        "invoice_no":bill.invoice_no,
                        "rating_id":  rating_id,
                        "rating": bill.rating,
                        "store_feedback":bill.feedback_selected_option,
                        "merchant_reply":bill.feedback_reply,
                    })

        # all_bills_new = BillRatingSerializer(all_bills, many=True)

        if new_list:
            return JsonResponse({'status': 'success', 'data' : new_list, "merchant_rating_count": merchant_rating_count}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)

class GetDashboardDetails(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        merchant_business_id = request.POST['merchant_business_id']

        merchant_business = MerchantProfile.objects.get(id = merchant_business_id)

        # Total Transactions

        total_transaction = 0

        total_transaction1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False,created_at__date = timezone.now()).count()

        total_transaction2 = MerchantBill.objects.filter(business_name = merchant_business,created_at__date = timezone.now()).count()

        total_transaction = total_transaction1 + total_transaction2

        # Average Transactions

        date_joined = merchant_business.date_joined

        today = date.today()

        current_date = today.strftime("%Y-%m-%d")
        current_date_new = datetime.strptime(str(current_date), "%Y-%m-%d")
        date_joined_new = datetime.strptime(str(date_joined.date()), "%Y-%m-%d")
        diff = current_date_new - date_joined_new

        total_days = diff.days

        average_transaction = 0

        received_payments1 = PaymentLinks.objects.filter(m_business_id = merchant_business, payment_done = True,created_at__date = timezone.now())

        payment_amount1 = 0
        for pay in received_payments1:
            if pay.amount:
                payment_amount1 = float(payment_amount1) + float(pay.amount)

        customer_bills1 = CustomerBill.objects.filter(business_name = merchant_business,payment_done = True,created_at__date = timezone.now())

        cust_amount1 = 0
        for bill in customer_bills1:
            if bill.bill_amount:
                cust_amount1 = float(cust_amount1) + float(bill.bill_amount)

        merchant_bills1 = MerchantBill.objects.filter(business_name = merchant_business,payment_done = True,created_at__date = timezone.now())

        mer_amount1 = 0
        for bill in merchant_bills1:
            if bill.bill_amount:
                mer_amount1 = float(mer_amount1) + float(bill.bill_amount)

        parking_bills1 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business, payment_done = True,created_at__date = timezone.now()) 

        park_amount1 = 0
        for bill in parking_bills1:
            if bill.amount:
                park_amount1 = float(park_amount1) + float(bill.amount)

        petrol_bills1 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business, payment_done=True,created_at__date = timezone.now())

        petr_amount1 = 0
        for bill in petrol_bills1:
            if bill:
                petr_amount1 = float(petr_amount1) + float(bill.amount)


        average_transaction = float(petr_amount1) + float(park_amount1) + float(mer_amount1) + float(cust_amount1) + float(payment_amount1)

        # if total_transaction != 0 and total_days != 0:
        #     average_transaction = total_transaction/total_days
        # else:
        #     average_transaction = 0



        # Total Sales

        customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False,created_at__date = timezone.now()).order_by('-id')

        merchant_bill = MerchantBill.objects.filter(business_name = merchant_business,created_at__date = timezone.now()).order_by('-id')

        total_sales = 0

        for bill in customer_bill:
            total_sales = total_sales + float(bill.bill_amount)

        for bill in merchant_bill:
            total_sales = total_sales + float(bill.bill_amount)

        # Average Sales

        average_sales = 0

        if total_transaction != 0 and total_sales != 0:
            average_sales = total_sales/total_transaction
        else:
            average_sales = 0

        data = {
            'todays_transaction': total_transaction,
            'average_transaction': "{:.2f}".format(average_transaction),
            'total_sales': "{:.2f}".format(total_sales),
            'average_sales': "{:.2f}".format(average_sales),
        }

        if data:
            return JsonResponse({'status': 'success', 'data' : data}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


def getActiveSubscriptionPlan(request, business_id):

    subscription_object = ""

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



class MerchantBillingAnalysisGraphAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        merchant_business_id = request.POST['merchant_business_id']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        merchant_business = MerchantProfile.objects.get(id = merchant_business_id)


        if from_date and to_date:
            DATE_FORMAT = '%Y-%m-%d'
            date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
            day_later = date_time_obj + timedelta(days=1)
            x = day_later.date()
            ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

            billing_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = billing_from_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')

            merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')

            merchant_bill1 = MerchantBill.objects.filter(bill_received_business_name = merchant_business_id, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')

            startswith = str(merchant_business.id) + ','
            endswith = ','+ str(merchant_business.id)
            contains = ','+ str(merchant_business.id) + ','
            exact = str(merchant_business.id)

            recharge_his = recharge_history.objects.filter(
                Q(purchase_date__gte = sd_filter),
                Q(purchase_date__lte = ed_filter),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            ).order_by('-id')

            rejected_bill_count = 0
            received_bill_count = 0
            sent_bill_count = 0

            for bill in customer_bill:
                sent_bill_count = sent_bill_count + 1
                if bill.reject_status == True:
                    rejected_bill_count = rejected_bill_count + 1

            for bill in merchant_bill:
                sent_bill_count = sent_bill_count + 1
                if bill.reject_status == True:
                    rejected_bill_count = rejected_bill_count + 1
            for bill in merchant_bill1:
                # if int(bill.bill_received_business_name) == merchant_business.id:
                received_bill_count = received_bill_count + 1

            for recharge in recharge_his:
                received_bill_count = received_bill_count + 1

            billing_analysis_labels_temp = []
            billing_analysis_labels_temp.append("Sent Bills")
            billing_analysis_labels_temp.append("Received Bills")
            billing_analysis_labels_temp.append("Rejected Bills")

            billing_analysis_data_temp = []
            billing_analysis_data_temp.append(str(sent_bill_count))
            billing_analysis_data_temp.append(str(received_bill_count))
            billing_analysis_data_temp.append(str(rejected_bill_count))


        else:

            customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__date = timezone.now()).order_by('-id')

            merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now()).order_by('-id')

            merchant_bill1 = MerchantBill.objects.filter(bill_received_business_name = merchant_business_id, created_at__date = timezone.now()).order_by('-id')

            startswith = str(merchant_business.id) + ','
            endswith = ','+ str(merchant_business.id)
            contains = ','+ str(merchant_business.id) + ','
            exact = str(merchant_business.id)

            recharge_his = recharge_history.objects.filter(
                Q(purchase_date__date = timezone.now()),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            ).order_by('-id')


            rejected_bill_count = 0
            received_bill_count = 0
            sent_bill_count = 0

            for bill in customer_bill:
                sent_bill_count = sent_bill_count + 1
                if bill.reject_status == True:
                    rejected_bill_count = rejected_bill_count + 1

            for bill in merchant_bill:
                sent_bill_count = sent_bill_count + 1
                if bill.reject_status == True:
                    rejected_bill_count = rejected_bill_count + 1

                # if int(bill.bill_received_business_name) == merchant_business.id:
            for bill in merchant_bill1:
                received_bill_count = received_bill_count + 1

            for recharge in recharge_his:
                received_bill_count = received_bill_count + 1

            billing_analysis_labels_temp = []
            billing_analysis_labels_temp.append("Sent Bills")
            billing_analysis_labels_temp.append("Received Bills")
            billing_analysis_labels_temp.append("Rejected Bills")

            billing_analysis_data_temp = []
            billing_analysis_data_temp.append(str(sent_bill_count))
            billing_analysis_data_temp.append(str(received_bill_count))
            billing_analysis_data_temp.append(str(rejected_bill_count))

        if billing_analysis_data_temp and billing_analysis_labels_temp:
            return JsonResponse({'status': 'success', 'labels': billing_analysis_labels_temp, 'data': billing_analysis_data_temp}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)


class MerchantDigitalBillingGraphAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        merchant_business_id = request.POST['merchant_business_id']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        merchant_business = MerchantProfile.objects.get(id = merchant_business_id)

        # notifications = sent_bill_history.objects.filter(
        #     m_business_id = merchant_business.id,
        #     created_at__date = timezone.now(),
        #     digital_bill = True
        # ).count()

        # sms = sent_bill_history.objects.filter(
        #     m_business_id = merchant_business.id,
        #     created_at__date = timezone.now(),
        #     sms_bill = True
        # ).count()

        if from_date and to_date:

            DATE_FORMAT = '%Y-%m-%d'

            d_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = d_from_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
            day_later = date_time_obj + timedelta(days=1)
            x = day_later.date()
            ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

            customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')
            merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')

            parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False,created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')
            petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id,created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')


            digital_sent = 0
            sms_sent = 0

            try:
                for bill in customer_bill:
                    if bill.greenbill_digital_bill == "True":
                        digital_sent = digital_sent + 1
                    elif bill.greenbill_sms_bill == "True":
                        sms_sent = sms_sent + 1

                for bill in merchant_bill:
                    if bill.greenbill_digital_bill == "True":
                        digital_sent = digital_sent + 1
                    elif bill.greenbill_sms_bill == "True":
                        sms_sent = sms_sent + 1

                for bill in parking_bill_list:
                    if bill.greenbill_digital_bill == "True":
                        digital_sent = digital_sent + 1
                    elif bill.greenbill_sms_bill == "True":
                        sms_sent = sms_sent + 1

                for bill in petrol_bill_list:
                    if bill.greenbill_digital_bill == "True":
                        digital_sent = digital_sent + 1
                    elif bill.greenbill_sms_bill == "True":
                        sms_sent = sms_sent + 1
            except:
                pass

            digital_billing_labels_temp = []
            digital_billing_labels_temp.append("SMS Sent")
            digital_billing_labels_temp.append("Notifications Sent")

            digital_billing_data_temp = []
            digital_billing_data_temp.append(str(sms_sent))
            digital_billing_data_temp.append(str(digital_sent))

        else:

            customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__date = timezone.now()).order_by('-id')
            merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now()).order_by('-id')

            parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False,created_at__date = timezone.now()).order_by('-id')
            petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id,created_at__date = timezone.now()).order_by('-id')

            digital_sent = 0
            sms_sent = 0
            
            try:
                for bill in customer_bill:
                    if bill.greenbill_digital_bill == "True":
                        digital_sent = digital_sent + 1
                    elif bill.greenbill_sms_bill == "True":
                        sms_sent = sms_sent + 1

                for bill in merchant_bill:
                    if bill.greenbill_digital_bill == "True":
                        digital_sent = digital_sent + 1
                    elif bill.greenbill_sms_bill == "True":
                        sms_sent = sms_sent + 1

                for bill in parking_bill_list:
                    if bill.greenbill_digital_bill == "True":
                        digital_sent = digital_sent + 1
                    elif bill.greenbill_sms_bill == "True":
                        sms_sent = sms_sent + 1

                for bill in petrol_bill_list:
                    if bill.greenbill_digital_bill == "True":
                        digital_sent = digital_sent + 1
                    elif bill.greenbill_sms_bill == "True":
                        sms_sent = sms_sent + 1
            except:
                pass

            digital_billing_labels_temp = []
            digital_billing_labels_temp.append("SMS Sent")
            digital_billing_labels_temp.append("Notifications Sent")

            digital_billing_data_temp = []
            digital_billing_data_temp.append(str(sms_sent))
            digital_billing_data_temp.append(str(digital_sent))

        if digital_billing_data_temp and digital_billing_labels_temp:
            return JsonResponse({'status': 'success', 'labels': digital_billing_labels_temp, 'data': digital_billing_data_temp}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)


class MerchantCouponsDetailsGraphAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        merchant_business_id = request.POST['merchant_business_id']

        merchant_business = MerchantProfile.objects.get(id = merchant_business_id)

        all_coupons = CouponModel.objects.filter(merchant_business_id = merchant_business.id)

        coupon_active_count = 0
        coupon_expired_count = 0

        today = date.today()
        current_date = today.strftime("%Y-%m-%d")
        current_date_new = datetime.strptime(str(current_date), "%Y-%m-%d")

        for coupon in all_coupons:
            valid_to_date = datetime.strptime(str(coupon.valid_through), "%Y-%m-%d")
            if valid_to_date < current_date_new:
                coupon_expired_count = coupon_expired_count + 1
            else:
                coupon_active_count = coupon_active_count + 1

        coupons_labels_temp = []
        coupons_labels_temp.append("Active")
        coupons_labels_temp.append("Expired")

        coupons_data_temp = []
        coupons_data_temp.append(str(coupon_active_count))
        coupons_data_temp.append(str(coupon_expired_count))

        if coupons_data_temp and coupons_labels_temp:
            return JsonResponse({'status': 'success', 'labels': coupons_labels_temp, 'data': coupons_data_temp}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)


class MerchantOffersDetailsGraphAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        merchant_business_id = request.POST['merchant_business_id']

        merchant_business = MerchantProfile.objects.get(id = merchant_business_id)

        all_offers = OfferModel.objects.filter(merchant_business_id = merchant_business)

        offer_active_count = 0
        offer_expired_count = 0
        offer_not_approved = 0

        today = date.today()
        current_date = today.strftime("%Y-%m-%d")
        current_date_new = datetime.strptime(str(current_date), "%Y-%m-%d")

        for offer in all_offers:
            valid_to_date = datetime.strptime(str(offer.valid_through), "%Y-%m-%d")
            if valid_to_date < current_date_new:
                if offer.status == "1":
                    offer_expired_count = offer_expired_count + 1
            elif offer.status == "1":
                offer_active_count = offer_active_count + 1
            if offer.status == "0":
                offer_not_approved = offer_not_approved + 1

        offer_labels_temp = []
        offer_labels_temp.append("Active")
        offer_labels_temp.append("Expired")
        offer_labels_temp.append("Not Approved")

        offer_data_temp = []
        offer_data_temp.append(str(offer_active_count))
        offer_data_temp.append(str(offer_expired_count))
        offer_data_temp.append(str(offer_not_approved))

        if offer_data_temp and offer_labels_temp:
            return JsonResponse({'status': 'success', 'labels': offer_labels_temp, 'data': offer_data_temp}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)


class MerchantOverallCustomerAnalysisGraphAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        merchant_business_id = request.POST['merchant_business_id']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        merchant_business = MerchantProfile.objects.get(id = merchant_business_id)
        context = {}
        if from_date and to_date:
            DATE_FORMAT = '%Y-%m-%d'
            cust_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = cust_from_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            cust_to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            end_date = cust_to_date.split('-')
            end_date = date(int(end_date[2]), int(end_date[1]), int(end_date[0]))
            ed_filter = end_date.strftime(DATE_FORMAT)

            unique_customer = []

            customers1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__range = (sd_filter, ed_filter))

            customers2 = MerchantBill.objects.filter(business_name = merchant_business,customer_added = False, created_at__range = (sd_filter, ed_filter))
            
            customers3 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id,is_pass=False, created_at__range = (sd_filter, ed_filter))
            customers4 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, created_at__range = (sd_filter, ed_filter))

            for customer in customers1:
                if customer.mobile_no in unique_customer:
                    pass
                else:
                    unique_customer.append(customer.mobile_no)

            for customer in customers2:
                if customer.mobile_no in unique_customer:
                    pass
                else:
                    unique_customer.append(customer.mobile_no)

            for customer in customers3:
                if customer.mobile_no in unique_customer:
                    pass
                else:
                    unique_customer.append(customer.mobile_no)

            for customer in customers4:
                if customer.mobile_no in unique_customer:
                    pass
                else:
                    unique_customer.append(customer.mobile_no)


            new_customer_count = 0
            returning_customers_count = 0

            for mobile_no in unique_customer:
                bill_count1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
                bill_count2 = MerchantBill.objects.filter(business_name = merchant_business, mobile_no = mobile_no).count()
                bill_count3 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, mobile_no = mobile_no).count()
                bill_count4 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, mobile_no = mobile_no).count()
                bill_count = 0
                bill_count = bill_count1 + bill_count2 + bill_count3 + bill_count4
                if bill_count == 1:
                    new_customer_count = new_customer_count + 1
                elif bill_count != 0:
                    returning_customers_count = returning_customers_count + 1

                
            # total_customers = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False).distinct()

            customers1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False)
            customers2 = MerchantBill.objects.filter(business_name = merchant_business)
            customers3 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id,is_pass=False)
            customers4 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id)

            total_unique_customer = []
            for customer in customers1:
                if customer.mobile_no in total_unique_customer:
                    pass
                else:
                    total_unique_customer.append(customer.mobile_no)

            for customer in customers2:
                if customer.mobile_no in total_unique_customer:
                    pass
                else:
                    total_unique_customer.append(customer.mobile_no)

            for customer in customers3:
                if customer.mobile_no in total_unique_customer:
                    pass
                else:
                    total_unique_customer.append(customer.mobile_no)

            for customer in customers4:
                if customer.mobile_no in total_unique_customer:
                    pass
                else:
                    total_unique_customer.append(customer.mobile_no)


            total_customer_count = len(total_unique_customer)
            new_customers_value = 0

            if new_customer_count != 0 and total_customer_count != 0:
                new_customers_value = int((new_customer_count * 100)/total_customer_count)
                new_customers_text = str(new_customer_count)
            else:
                new_customers_value = 0
                new_customers_text = 0

            context['new_customers_text'] = str(new_customers_text)
            context['new_customers_value'] = str(new_customers_value)

            # returning_customers_count = 0
            # for mobile_no in unique_customer:
            #     bill_count1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
            #     bill_count2 = MerchantBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
            #     bill_count = 0
            #     bill_count = bill_count1 + bill_count2
            #     if bill_count >= 2:
            #         returning_customers_count = returning_customers_count + 1

            if returning_customers_count != 0 and total_customer_count != 0:
                returning_customers_value = int((returning_customers_count * 100)/total_customer_count)
                returning_customers_text = str(returning_customers_count)
            else:
                returning_customers_value = 0
                returning_customers_text = 0

            context['returning_customers_text'] = str(returning_customers_text)
            context['returning_customers_value'] = str(returning_customers_value)

        else:
            unique_customer = []
            customers1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__date = timezone.now())

            customers2 = MerchantBill.objects.filter(business_name = merchant_business,customer_added = False, created_at__date = timezone.now())
            customers3 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id,is_pass=False, created_at__date = timezone.now())
            customers4 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, created_at__date = timezone.now())


            for customer in customers1:
                if customer.mobile_no in unique_customer:
                    pass
                else:
                    unique_customer.append(customer.mobile_no)

            for customer in customers2:
                if customer.mobile_no in unique_customer:
                    pass
                else:
                    unique_customer.append(customer.mobile_no)

            for customer in customers3:
                if customer.mobile_no in unique_customer:
                    pass
                else:
                    unique_customer.append(customer.mobile_no)

            for customer in customers4:
                if customer.mobile_no in unique_customer:
                    pass
                else:
                    unique_customer.append(customer.mobile_no)

            new_customer_count = 0
            returning_customers_count = 0

            for mobile_no in unique_customer:
                bill_count1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
                bill_count2 = MerchantBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
                bill_count3 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, mobile_no = mobile_no).count()
                bill_count4 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, mobile_no = mobile_no).count()
                bill_count = 0
                bill_count = bill_count1 + bill_count2 + bill_count3 + bill_count4
                if bill_count == 1:
                    new_customer_count = new_customer_count + 1
                elif bill_count != 0:
                    returning_customers_count = returning_customers_count + 1                

            customers1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False)
            customers2 = MerchantBill.objects.filter(business_name = merchant_business)
            customers3 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id,is_pass=False)
            customers4 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id)


            total_unique_customer = []
            for customer in customers1:
                if customer.mobile_no in total_unique_customer:
                    pass
                else:
                    total_unique_customer.append(customer.mobile_no)

            for customer in customers2:
                if customer.mobile_no in total_unique_customer:
                    pass
                else:
                    total_unique_customer.append(customer.mobile_no)

            for customer in customers3:
                if customer.mobile_no in total_unique_customer:
                    pass
                else:
                    total_unique_customer.append(customer.mobile_no)

            for customer in customers4:
                if customer.mobile_no in total_unique_customer:
                    pass
                else:
                    total_unique_customer.append(customer.mobile_no)

            total_customer_count = len(total_unique_customer)

            new_customers_value = 0

            if new_customer_count != 0 and total_customer_count != 0:
                new_customers_value = int((new_customer_count * 100)/total_customer_count)
                new_customers_text = str(new_customer_count)
            else:
                new_customers_value = 0
                new_customers_text = 0


            context['new_customers_text'] = str(new_customers_text)
            context['new_customers_value'] = str(new_customers_value)
            # returning_customers_count = 0
            # for mobile_no in unique_customer:
            #     bill_count1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
            #     bill_count2 = MerchantBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
            #     bill_count = 0
            #     bill_count = bill_count1 + bill_count2
            #     if bill_count >= 2:
            #         returning_customers_count = returning_customers_count + 1

            # print(total_customer_count)

            if returning_customers_count != 0 and total_customer_count != 0:
                returning_customers_value = int((returning_customers_count * 100)/total_customer_count)
                returning_customers_text = str(returning_customers_count)
            else:
                returning_customers_value = 0
                returning_customers_text = 0

            context['returning_customers_text'] = str(returning_customers_text)
            context['returning_customers_value'] = str(returning_customers_value)

        # data = []

        # data = {
        #     'new_customers_text': str(new_customers_text),
        #     'new_customers_value': new_customers_value,
        #     'returning_customers_text': str(returning_customers_text),
        #     'returning_customers_value': returning_customers_value
        # }

        if context:
            return JsonResponse({'status': 'success', 'data': context}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)


class SendBulkSMS(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        transactional = request.POST['transactional']
        customer = request.POST['customer']
        smsheader = request.POST['smsheader']
        unique_template_id = request.POST['template_id']
        message = request.POST['message']
        customer_state_value = request.POST['customer_state_value']
        customer_state_value_new = customer_state_value.split(",")

        customer_city_value = request.POST['customer_city_value']
        if customer_city_value:
            customer_city_value_new = customer_city_value.split(",")
        else:
            customer_city_value_new = ''

        customer_area_value = request.POST['customer_area_value']
        campaign_name = request.POST.get('campaign_name')
        if customer_area_value:
            customer_area_value_new = customer_area_value.split(",")
        else:
            customer_area_value_new = ''


        receipent_count = GreenBillUser.objects.filter(is_customer=True).count()
        try:
            smsid = bulkMailSmsMerchantCustomerModel.objects.filter().last().id
        except:
            smsid = ""


        if customer_city_value_new != '' and customer_area_value_new != '':
            notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(campaign_name=campaign_name, customer_state=customer_state_value_new, customer_city=customer_city_value_new, customer_area=customer_area_value_new, owner_id=GreenBillUser.objects.get(id=user_id),message=message,smsheader=smsheader,template=template, receiver_name=customer, transactional=transactional, defaults= { 'message':message, 'smsheader':smsheader, 'template':template, 'receiver_name':customer, 'o_sent_sms':True })
        elif customer_city_value_new != '' and customer_area_value_new == '':
            notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(campaign_name=campaign_name, customer_state=customer_state_value_new, customer_city=customer_city_value_new, owner_id=GreenBillUser.objects.get(id=user_id),message=message,smsheader=smsheader,template=template, receiver_name=customer, transactional=transactional, defaults= { 'message':message, 'smsheader':smsheader, 'template':template, 'receiver_name':customer, 'o_sent_sms':True })
        elif customer_city_value_new == '' and customer_area_value_new == '':
            notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(campaign_name=campaign_name, customer_state=customer_state_value_new, owner_id=GreenBillUser.objects.get(id=user_id),message=message,smsheader=smsheader,template=template, receiver_name=customer, transactional=transactional, defaults= { 'message':message, 'smsheader':smsheader, 'template':template, 'receiver_name':customer, 'o_sent_sms':True })

        if transactional == 'transactional':
            # print('transactional')
            merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']
            business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)

            subscription_object = getActiveTransactionalSubscriptionPlan(request, business_object.id)

            if subscription_object:
                # print('subscropin plan')
                if int(float(subscription_object.total_sms_avilable)) >= int(receipent_count):
                    if customer:
                        if customer_city_value_new != '' and customer_area_value_new != '':
                            users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new)
                            if users:
                                customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new).count()
                                customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                customer_addresswise_count = customer_count

                                for u in users:
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
                                    # print(sms_response)
                                    # try:
                                    #     print('success')
                                    #         # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                    #         # message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
                                    # except:
                                    #         owner_notice_sent_save = ""
                                    # sms_response = sendSMS(str(contact), message)
                                    # print(sms_response)
                                if response.status_code == 200:
                                    total_sms_avilable_new = 0
                                    if customer:
                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                        subscription_object.total_sms_avilable = total_sms_avilable_new
                                    else:
                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                        subscription_object.total_sms_avilable = total_sms_avilable_new

                                    subscription_object.save()

                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
                                    return JsonResponse({'status' : 'error', 'message': "SMS sent successfully"}, status=200)
                                else:
                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                    return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                            else:
                                return JsonResponse({'status' : 'error', 'message': "Customers not found"}, status=400)
                        
                        elif customer_city_value_new != '' and customer_area_value_new == '':
                            users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new)
                            if users:
                                customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new).count()
                                customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                customer_addresswise_count = customer_count

                                for u in users:
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
                                    # print(sms_response)
                                    # try:
                                    #     print('success')
                                    #         # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                    #         # message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
                                    # except:
                                    #         owner_notice_sent_save = ""
                                    # sms_response = sendSMS(str(contact), message)
                                    # print(sms_response)
                                if response.status_code == 200:
                                    total_sms_avilable_new = 0
                                    if customer:
                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                        subscription_object.total_sms_avilable = total_sms_avilable_new
                                    else:
                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                        subscription_object.total_sms_avilable = total_sms_avilable_new

                                    subscription_object.save()

                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
                                    return JsonResponse({'status' : 'error', 'message': "SMS sent successfully"}, status=200)
                                else:
                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                    return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                            else:
                                return JsonResponse({'status' : 'error', 'message': "Customers Not Found"}, status=400)
                        
                        elif customer_city_value_new == '' and customer_area_value_new == '':
                            users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new)
                            if users:
                                customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new).count()
                                customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                customer_addresswise_count = customer_count

                                for u in users:
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
                                    # print(sms_response)
                                    # try:
                                    #     print('success')
                                    #         # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                    #         # message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
                                    # except:
                                    #         owner_notice_sent_save = ""
                                    # sms_response = sendSMS(str(contact), message)
                                    # print(sms_response)
                                if response.status_code == 200:
                                    total_sms_avilable_new = 0
                                    if customer:
                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                        subscription_object.total_sms_avilable = total_sms_avilable_new
                                    else:
                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                        subscription_object.total_sms_avilable = total_sms_avilable_new

                                    subscription_object.save()

                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
                                    return JsonResponse({'status' : 'error', 'message': "SMS sent successfully"}, status=200)
                                else:
                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                    return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                            else:
                                return JsonResponse({'status' : 'error', 'message': "Customers Not Found"}, status=400)

                else:
                    return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
            else:
                return JsonResponse({'status' : 'error', 'message': "You don't have active Transactional SMS plan. Please purchase and try again."}, status=400)
                            
        if transactional == 'promotional':
            merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']
            business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)

            subscription_object = getActivePromotionalSubscriptionPlan(request, business_object.id)
            if subscription_object:
                if int(float(subscription_object.total_sms_avilable)) >= int(receipent_count):
                    if customer:
                        if customer_city_value_new != '' and customer_area_value_new != '':
                            users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new)
                            if users:
                                customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new).count()
                                customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                customer_addresswise_count = customer_count

                                for u in users:
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

                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
                                    return JsonResponse({'status' : 'error', 'message': "Sms sent successfully"}, status=200)
                                else:
                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                    return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                                
                            else:
                                return JsonResponse({'status' : 'error', 'message': "Customers Not Found"}, status=400)
                        elif customer_city_value_new != '' and customer_area_value_new == '':
                            users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new)
                            if users:
                                customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new).count()
                                customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                customer_addresswise_count = customer_count

                                for u in users:
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

                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
                                    return JsonResponse({'status' : 'error', 'message': "SMS sent successfully"}, status=200)
                                else:
                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                    return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                                
                            else:
                                return JsonResponse({'status' : 'error', 'message': "Customers Not Found"}, status=400)
                        elif customer_city_value_new == '' and customer_area_value_new == '':
                            users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new)
                            if users:
                                customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new).count()
                                customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                customer_addresswise_count = customer_count

                                for u in users:
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

                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
                                    return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                else:
                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                    return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                                
                            else:
                                return JsonResponse({'status' : 'error', 'message': "Customers Not Found"}, status=400)

                        else:
                            return JsonResponse({'status' : 'error', 'message': "Customers in this area not found."}, status=400)
                else:
                    return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
            else:
                return JsonResponse({'status' : 'error', 'message': "You don't have active Promotional SMS plan. Please purchase and try again."}, status=400)
            
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)
   



class GetSMSHeaderList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST['user_id']
        type_header = request.POST['header_type']

        header_data = []
        header = smsHeaderModel.objects.filter(request_user=user_id,Active_status=True,status='Approved',header_type=type_header)
        for head in header:
            header_data.append({
                'id':head.id,
                'status': head.status,
                'header_content' : head.header_content,
                'created_at' : datetime.strptime(str(head.created_at.date()), '%Y-%m-%d').strftime('%Y-%m-%d'),
            })

        if header_data:
            return JsonResponse({'status': 'success', 'data' : header_data}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GetSMSTemplateList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        smsheader = request.POST['SMSheader']

        Template = templateContentModel.objects.filter(request_user = user_id, status='Approved')
        list1 = []
        filtered_city_list = []

        for obj in Template:
            if obj.sms_header:
                if smsheader in obj.sms_header:
                    list1.append({
                        "id": obj.id,
                        "status": obj.status,
                        "template_content": obj.template_content,
                        "created_at": datetime.strptime(str(obj.created_at.date()), '%Y-%m-%d').strftime('%Y-%m-%d'),
                    })


        # user_id = request.POST['user_id']
        # sms_header = request.POST['SMSheader']

        # template_data = []
        # templates = templateContentModel.objects.filter(request_user=user_id,status='Approved')
        # for temp in templates:
        #     template_data.append({
        #         'id':temp.id,
        #         'status': temp.status,
        #         'template_content' : temp.template_content,
        #         'created_at' : datetime.strptime(str(temp.created_at.date()), '%Y-%m-%d').strftime('%Y-%m-%d'),
        #     })

        if list1:
            return JsonResponse({'status': 'success', 'data' : list1}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)

class GetCustomerCountByStateCityArea(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        customer_state_value = request.POST['customer_state_value']
        customer_city_value = request.POST['customer_city_value']
        customer_area_value = request.POST['customer_area_value']

        list1 = []

        total_count = 0

        if customer_state_value:
            total_count = total_count + (GreenBillUser.objects.filter(c_state = customer_state_value,is_customer=True).count())
        elif customer_city_value:
            total_count = total_count + (GreenBillUser.objects.filter(c_city = customer_city_value,is_customer=True).count())
        elif customer_area_value:
            total_count = total_count + (GreenBillUser.objects.filter(c_area = customer_area_value, is_customer=True).count())


        if total_count:
            return JsonResponse({'status': 'success', 'data' : total_count}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GetCustomerState(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        states_data = []
        states = GreenBillUser.objects.values('c_state').distinct()
        # print(states,'states')
        for i in states:
            if i['c_state'] != '':
                states_data.append(i)

        # for state in states:
        #     states_data.append({
        #         'id':state.id,
        #         'states': state.status,
        #         'template_content' : temp.template_content,
        #         'created_at' : datetime.strptime(str(temp.created_at.date()), '%Y-%m-%d').strftime('%Y-%m-%d'),
        #     })

        if states_data:
            return JsonResponse({'status': 'success', 'data' : states_data}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GetCustomerCityByState(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        state_value = request.POST['state_value']

        customer_state_value_new = state_value.split(",")
        filtered_city_list = []

        for cust_state in customer_state_value_new:
            cus_state_id = GreenBillUser.objects.filter(c_state = cust_state).values('c_city').distinct()
            for city in cus_state_id:
                if city['c_city'] != '':
                    filtered_city_list.append(city)
            

        if filtered_city_list:
            return JsonResponse({'status': 'success', 'data' : filtered_city_list}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GetCustomerAreaByCity(generics.GenericAPIView):
    def post(self, request):

        city_value = request.POST['city_value']

        customer_city_value_new = city_value.split(",")
        filtered_area_list = []

        for area in customer_city_value_new:
            cust_id = GreenBillUser.objects.filter(c_city=area).values('c_area').distinct()
            
            for area in cust_id:
                if area['c_area'] != '' or area['c_area'] != None:
                    filtered_area_list.append(area)
                

        if filtered_area_list:
            return JsonResponse({'status': 'success', 'data' : filtered_area_list}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)



class SubscriptionPurchasedSuccess(generics.GenericAPIView):
    def post(self, request):
        status=request.POST["status"]
        firstname=request.POST["firstname"]
        amount= request.POST["amount"]
        txnid=request.POST["txnid"]
        posted_hash=request.POST["hash"]
        key=request.POST["key"]
        productinfo=request.POST["productinfo"]
        email=request.POST["email"]
        udf1 = request.POST["lastname"] # subscription id
        subscription_id = request.POST["lastname"]
        udf2 = request.POST["address2"] # user id
        user_id = request.POST["address2"] # user id
        udf3 = request.POST["udf3"] # encoded password
        udf4 = request.POST["udf4"] # decode key id
        udf5 = request.POST["udf5"] # Business Ids
        udf6 = request.POST["udf6"]
        business_ids = udf5

        mihpayid = request.POST["mihpayid"]

        success_url = "http://157.230.228.250/payment-success-message/"
        fail_url = "http://157.230.228.250/payment-fail-message/"


        if productinfo == 'Green Bill Subscription':
            # print('Green Bill')

            SALT="7ViVXMy1" # Production Salt

            merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

            merchant_object = GreenBillUser.objects.get(id=merchant_id)

            # user_object =  GreenBillUser.objects.get(id=user_id)

            retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

            hash_string = retHashSeq.encode('utf-8')
            
            hashh = hashlib.sha512(hash_string).hexdigest().lower()
            # print('hashh',hashh)

            if status == "success":
                # print('status')

                if posted_hash:
                    # print('hash')

                    subscription_object = subscription_plan_details.objects.get(id=subscription_id)
                    # print('subscription_object',subscription_object)

                    valid_for_month = subscription_object.valid_for_month
                    per_bill_cost = subscription_object.per_bill_cost
                    per_receipt_cost = subscription_object.per_receipt_cost
                    per_cash_memo_cost = subscription_object.per_cash_memo_cost
                    per_digital_bill_cost = subscription_object.per_digital_bill_cost
                    per_digital_receipt_cost = subscription_object.per_digital_receipt_cost
                    per_digital_cash_memo_cost = subscription_object.per_digital_cash_memo_cost

                    total_amount = float(subscription_object.recharge_amount)
                    subscription_plan_cost = float(subscription_object.subscription_plan_cost)

                    today = date.today()
                    d1 = today.strftime("%d-%m-%Y")
                    start_date = datetime.strptime(d1, "%d-%m-%Y")
                    delta_period = int(subscription_object.valid_for_month)
                    end_date = start_date + relativedelta(months=delta_period)
                    expiry_date = end_date.strftime("%d-%m-%Y")

                    business_ids_list = list(business_ids.split(","))

                    subscription_available_referral_count = 0

                    subscription_available_referral_count = merchant_subscriptions.objects.filter(merchant_id = merchant_object).count()

                    for business_id in business_ids_list:
                        startswith = str(business_id) + ','
                        endswith = ','+ str(business_id)
                        contains = ','+ str(business_id) + ','
                        exact = str(business_id)

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



                        if check_subscription_available:

                            business_ids_list_temp = list((check_subscription_available.business_ids).split(","))
                            
                            business_ids_list_temp.remove(business_id)

                            business_ids_new = ""

                            business_ids_new = ','.join(business_ids_list_temp)
                            
                            update_result = merchant_subscriptions.objects.filter(id = check_subscription_available.id).update(business_ids = business_ids_new)

                            get_updated_suscription = merchant_subscriptions.objects.get(id = check_subscription_available.id)

                            if get_updated_suscription.business_ids == "":
                                merchant_subscriptions.objects.filter(id = get_updated_suscription.id).update(is_active = False)

                    subscription_active_status = True

                    subscription =  merchant_subscriptions.objects.create(
                        subscription_id = subscription_object.id,
                        subscription_name = subscription_object.subscription_name,
                        merchant_id = merchant_object,
                        business_ids = business_ids,
                        valid_for_month = valid_for_month,

                        per_bill_cost = per_bill_cost,
                        per_receipt_cost = per_receipt_cost,
                        per_cash_memo_cost = per_cash_memo_cost,

                        per_digital_bill_cost = per_digital_bill_cost,
                        per_digital_receipt_cost = per_digital_receipt_cost,
                        per_digital_cash_memo_cost = per_digital_cash_memo_cost,

                        recharge_amount = total_amount,
                        total_amount_avilable = total_amount,
                        is_active = subscription_active_status,

                        purchase_cost = subscription_plan_cost,
                        expiry_date = expiry_date,

                        transaction_id = txnid,
                        payu_transaction_id = mihpayid,
                    )
                    try:
                        last_id = recharge_history.objects.filter().last()
                        invoice_no = 'GB' + str(last_id.id+1)
                    except:
                        invoice_no = 'GB' + str(1)
                    
                    recharge_history.objects.create(
                        subscription_plan_id = subscription_object.id,
                        subscription_name = subscription_object.subscription_name,
                        merchant_id = merchant_object,
                        business_ids = business_ids,

                        valid_for_month = valid_for_month,

                        per_bill_cost = per_bill_cost,
                        per_receipt_cost = per_receipt_cost,
                        per_cash_memo_cost = per_cash_memo_cost,

                        per_digital_bill_cost = per_digital_bill_cost,
                        per_digital_receipt_cost = per_digital_receipt_cost,
                        per_digital_cash_memo_cost = per_digital_cash_memo_cost,

                        cost = subscription_plan_cost,

                        is_subscription_plan = True,
                        expiry_date = expiry_date,

                        transaction_id = txnid,
                        payu_transaction_id = mihpayid,
                        invoice_no = invoice_no
                    )

                    if merchant_object.m_used_referral_code and subscription_available_referral_count == 0:

                        referral_object = ReferralModel.objects.get(id = 1)

                        if referral_object.recharge_amount_per_refferal:

                            referral_user_object = GreenBillUser.objects.get(merchant_referral_code = merchant_object.m_used_referral_code)

                            # try:
                            referral_merchant_subscriptions_object = merchant_subscriptions.objects.filter(merchant_id = referral_user_object, is_active = True).order_by('-id')
                            # except:
                            #     referral_merchant_subscriptions_object = ""

                            if referral_merchant_subscriptions_object:
                                referral_merchant_subscriptions_total_amount = 0
                                referral_merchant_subscriptions_total_amount = float(referral_merchant_subscriptions_object[0].total_amount_avilable) + float(referral_object.recharge_amount_per_refferal)
                                
                                merchant_subscriptions.objects.filter(
                                    id = referral_merchant_subscriptions_object[0].id
                                    ).update(total_amount_avilable = referral_merchant_subscriptions_total_amount)

                                ReferralHistory.objects.create(
                                    referent_mobile_no = merchant_object.mobile_no,
                                    referral_mobile_no = referral_user_object.mobile_no,
                                    is_referral = True,
                                    is_referent = False,
                                    earned_recharge_points = referral_object.recharge_amount_per_refferal
                                )

                        if referral_object.recharge_amount_per_referent:
                            subscription.total_amount_avilable = float(total_amount) + float(referral_object.recharge_amount_per_referent)
                            subscription.save()

                            ReferralHistory.objects.create(
                                referent_mobile_no = merchant_object.mobile_no,
                                referral_mobile_no = referral_user_object.mobile_no,
                                is_referral = False,
                                is_referent = True,
                                earned_recharge_points = referral_object.recharge_amount_per_referent
                            )

                    if subscription:
                        return render(request,'merchant/payment_success_message/subscription_payment_success.html')
                        # return JsonResponse({'status':'success', 'message': 'Subscription purchased Successfully.'}, status=200)

                else:
                    return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
                    # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)                       
            else:
                return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
                # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)
        else:
            return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
            # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)  



        if productinfo == 'Promotional Sms Subscription':
            SALT="7ViVXMy1" # Production Salt

            merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

            merchant_object = GreenBillUser.objects.get(id=merchant_id)

            user_object =  GreenBillUser.objects.get(id=user_id)

            retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

            hash_string = retHashSeq.encode('utf-8')
            
            hashh = hashlib.sha512(hash_string).hexdigest().lower()

            if status == "success":

                if posted_hash:

                    subscription_object = promotional_subscription_plan_model.objects.get(id=subscription_id)

                    total_sms = subscription_object.total_sms
                    per_sms_cost = subscription_object.per_sms_cost
                    total_sms_cost = float(subscription_object.total_sms_cost)
                    subscription_plan_cost = float(subscription_object.total_sms_cost)
                    total_sms_avilable = total_sms

                    business_ids_list = list(business_ids.split(","))

                    for business_id in business_ids_list:
                        startswith = str(business_id) + ','
                        endswith = ','+ str(business_id)
                        contains = ','+ str(business_id) + ','
                        exact = str(business_id)

                        try:
                            check_subscription_available = promotional_sms_subscriptions.objects.get(
                                Q(merchant_id = merchant_object),
                                Q(is_active = True),
                                Q(business_ids__startswith = startswith) | 
                                Q(business_ids__endswith = endswith) | 
                                Q(business_ids__contains = contains) | 
                                Q(business_ids__exact = exact)
                            )
                        except:
                            check_subscription_available = ""

                        if check_subscription_available:

                            business_ids_list_temp = list((check_subscription_available.business_ids).split(","))
                            
                            business_ids_list_temp.remove(business_id)

                            business_ids_new = ""

                            business_ids_new = ','.join(business_ids_list_temp)
                            
                            update_result = promotional_sms_subscriptions.objects.filter(id = check_subscription_available.id).update(business_ids = business_ids_new)

                            get_updated_suscription = promotional_sms_subscriptions.objects.get(id = check_subscription_available.id)

                            if get_updated_suscription.business_ids == "":
                                promotional_sms_subscriptions.objects.filter(id = get_updated_suscription.id).update(is_active = False)

                    subscription_active_status = True

                    subscription =  promotional_sms_subscriptions.objects.create(
                        subscription_id = subscription_object.id,
                        subscription_name = subscription_object.subscription_name,
                        merchant_id = merchant_object,
                        business_ids = business_ids,

                        total_sms = total_sms,
                        per_sms_cost = per_sms_cost,

                        total_sms_avilable = total_sms_avilable,

                        is_active = subscription_active_status,
                        purchase_cost = subscription_plan_cost,

                        transaction_id = txnid,
                        payu_transaction_id = mihpayid,
                    )

                    try:
                        last_id = recharge_history.objects.filter().last()
                        invoice_no = 'GB' + str(last_id.id+1)
                    except:
                        invoice_no = 'GB' + str(1)

                    recharge_history.objects.create(
                        subscription_plan_id = subscription_object.id,
                        subscription_name = subscription_object.subscription_name,
                        merchant_id = merchant_object,
                        business_ids = business_ids,

                        total_sms = total_sms,
                        per_sms_cost = per_sms_cost,

                        cost = subscription_plan_cost,

                        is_promotional_sms_plan = True,

                        transaction_id = txnid,
                        payu_transaction_id = mihpayid,
                        invoice_no = invoice_no
                    )

                    if subscription:
                        return render(request,'merchant/payment_success_message/subscription_payment_success.html')
                        # return JsonResponse({'status':'success', 'message': 'Subscription purchased Successfully.'}, status=200)
                else:
                    return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
                    # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)                       
            else:
                return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
                # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)
        else:
            return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
            # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)


        if productinfo == 'Transactional Sms Subscription':
            SALT="7ViVXMy1" # Production Salt

            merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

            merchant_object = GreenBillUser.objects.get(id=merchant_id)

            user_object =  GreenBillUser.objects.get(id=user_id)

            retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

            hash_string = retHashSeq.encode('utf-8')
            
            hashh = hashlib.sha512(hash_string).hexdigest().lower()

            if status == "success":

                if posted_hash:

                    subscription_object = transactional_subscription_plan_model.objects.get(id=subscription_id)

                    total_sms = subscription_object.total_sms
                    per_sms_cost = subscription_object.per_sms_cost
                    total_sms_cost = float(subscription_object.total_sms_cost)
                    subscription_plan_cost = float(subscription_object.total_sms_cost)
                    total_sms_avilable = total_sms

                    business_ids_list = list(business_ids.split(","))

                    for business_id in business_ids_list:
                        startswith = str(business_id) + ','
                        endswith = ','+ str(business_id)
                        contains = ','+ str(business_id) + ','
                        exact = str(business_id)

                        try:
                            check_subscription_available = transactional_sms_subscriptions.objects.get(
                                Q(merchant_id = merchant_object),
                                Q(is_active = True),
                                Q(business_ids__startswith = startswith) | 
                                Q(business_ids__endswith = endswith) | 
                                Q(business_ids__contains = contains) | 
                                Q(business_ids__exact = exact)
                            )
                        except:
                            check_subscription_available = ""

                        if check_subscription_available:

                            business_ids_list_temp = list((check_subscription_available.business_ids).split(","))
                            
                            business_ids_list_temp.remove(business_id)

                            business_ids_new = ""

                            business_ids_new = ','.join(business_ids_list_temp)
                            
                            update_result = transactional_sms_subscriptions.objects.filter(id = check_subscription_available.id).update(business_ids = business_ids_new)

                            get_updated_suscription = transactional_sms_subscriptions.objects.get(id = check_subscription_available.id)

                            if get_updated_suscription.business_ids == "":
                                transactional_sms_subscriptions.objects.filter(id = get_updated_suscription.id).update(is_active = False)

                    subscription_active_status = True

                    subscription =  transactional_sms_subscriptions.objects.create(
                        subscription_id = subscription_object.id,
                        subscription_name = subscription_object.subscription_name,
                        merchant_id = merchant_object,
                        business_ids = business_ids,

                        total_sms = total_sms,
                        per_sms_cost = per_sms_cost,

                        total_sms_avilable = total_sms_avilable,

                        is_active = subscription_active_status,
                        purchase_cost = subscription_plan_cost,

                        transaction_id = txnid,
                        payu_transaction_id = mihpayid,
                    )
                    try:
                        last_id = recharge_history.objects.filter().last()
                        invoice_no = 'GB' + str(last_id.id+1)
                    except:
                        invoice_no = 'GB' + str(1)
                    recharge_history.objects.create(
                        subscription_plan_id = subscription_object.id,
                        subscription_name = subscription_object.subscription_name,
                        merchant_id = merchant_object,
                        business_ids = business_ids,

                        total_sms = total_sms,
                        per_sms_cost = per_sms_cost,

                        cost = subscription_plan_cost,

                        is_transactional_sms_plan = True,

                        transaction_id = txnid,
                        payu_transaction_id = mihpayid,
                        invoice_no = invoice_no
                    )

                    if subscription:
                        return render(request,'merchant/payment_success_message/subscription_payment_success.html')
                        # return JsonResponse({'status':'success', 'message': 'Subscription purchased Successfully.'}, status=200)
                
                else:
                    return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
                    # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)                       

            else:
                return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
                # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)
        else:
            return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
            # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)


        if productinfo == "Add's On Subscription":
            SALT="7ViVXMy1" # Production Salt

            merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

            merchant_object = GreenBillUser.objects.get(id=merchant_id)

            user_object =  GreenBillUser.objects.get(id=user_id)

            retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

            hash_string = retHashSeq.encode('utf-8')
            
            hashh = hashlib.sha512(hash_string).hexdigest().lower()

            if status == "success":

                if posted_hash:

                    subscription_object = add_on_plan_model.objects.get(id=subscription_id)

                    per_bill_cost = subscription_object.per_bill_cost
                    per_receipt_cost = subscription_object.per_receipt_cost
                    per_cash_memo_cost = subscription_object.per_cash_memo_cost
                    per_digital_bill_cost = subscription_object.per_digital_bill_cost
                    per_digital_receipt_cost = subscription_object.per_digital_receipt_cost
                    per_digital_cash_memo_cost = subscription_object.per_digital_cash_memo_cost

                    business_id = udf5

                    startswith = str(business_id) + ','
                    endswith = ','+ str(business_id)
                    contains = ','+ str(business_id) + ','
                    exact = str(business_id)

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

                    if check_subscription_available:

                        total_amount = float(check_subscription_available.total_amount_avilable) + float(subscription_object.recharge_amount)

                        subscription =  merchant_subscriptions.objects.filter(id = check_subscription_available.id).update(

                            per_bill_cost = per_bill_cost,
                            per_receipt_cost = per_receipt_cost,
                            per_cash_memo_cost = per_cash_memo_cost,

                            per_digital_bill_cost = per_digital_bill_cost,
                            per_digital_receipt_cost = per_digital_receipt_cost,
                            per_digital_cash_memo_cost = per_digital_cash_memo_cost,

                            total_amount_avilable = total_amount,

                        )
                        try:
                            last_id = recharge_history.objects.filter().last()
                            invoice_no = 'GB' + str(last_id.id+1)
                        except:
                            invoice_no = 'GB' + str(1)
                        recharge_history.objects.create(
                            
                            subscription_plan_id = subscription_object.id,
                            subscription_name = subscription_object.add_on_name,
                            merchant_id = merchant_object,
                            business_ids = business_id,

                            per_bill_cost = per_bill_cost,
                            per_receipt_cost = per_receipt_cost,
                            per_cash_memo_cost = per_cash_memo_cost,

                            per_digital_bill_cost = per_digital_bill_cost,
                            per_digital_receipt_cost = per_digital_receipt_cost,
                            per_digital_cash_memo_cost = per_digital_cash_memo_cost,

                            cost = subscription_object.recharge_amount,

                            is_add_on_plan = True,

                            transaction_id = txnid,
                            payu_transaction_id = mihpayid,
                            invoice_no = invoice_no

                        )

                        if subscription:
                            return render(request,'merchant/payment_success_message/subscription_payment_success.html')
                            # return JsonResponse({'status':'success', 'message': 'Add On purchased Successfully'}, status=200)

                else:
                    return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
                    # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)                       

            else:
                return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
                # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)
        else:
            return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
            # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)


class SubscriptionPurchasedFailed(generics.GenericAPIView):
    def post(self, request):
        status=request.POST["status"]
        udf2 = request.POST["address2"]
        if status == "success":
            return render(request,'merchant/payment_success_message/subscription_payment_success.html')

        if status == "error":
            return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
        return render(request,'merchant/payment_success_message/subscription_payment_failed.html')


class SubscriptionBuyButtonInfo(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST['user_id']
        business_ids = request.POST['business_ids']
        plan_id = request.POST['plan_id']
    
        data=[]
        subscription = subscription_plan_details.objects.get(id=plan_id)
        user_object = GreenBillUser.objects.get(id=user_id)
        key="IUZdcF"
        SALT="7ViVXMy1"
        PAYU_BASE_URL = "https://secure.payu.in/_payment"

        action = PAYU_BASE_URL

        enc_key = Fernet.generate_key()
        fernet = Fernet(enc_key)
        password = user_object.password
        encPassword = fernet.encrypt(password.encode())

        merchant_subscriptions_key = merchant_subscriptions_keys.objects.create(key = enc_key.decode("utf-8"))

        firstname = str(user_object.first_name)

        if user_object.email != "":
            email = str(user_object.email)
        else:
            email = "support@greenbill.in"
        
        phone = str(user_object.mobile_no)

        surl = "http://157.230.228.250/subscription-purchased-success/"

        furl = "http://157.230.228.250/subscription-purchased-fail/"


        udf1 = ""
        udf2 = ""
        udf3 = ""
        udf4 = ""
        udf5 = ""
        udf6 = ""

        posted={}

        for i in request.POST:
            posted[i]=request.POST[i]

        random_str =  random.randint(9999999, 99999999)

        hash_object = hashlib.sha256(b'randint(0,20)' + bytes(subscription.id) + bytes(user_object.id) + bytes(random_str))

        txnid=hash_object.hexdigest()[0:20]

        hashh = ''
        posted['txnid']=txnid
        posted['key']=key
        productinfo = str("subscription_name-"+ subscription.subscription_name)
        amount = str(subscription.subscription_plan_cost)

        udf1 = str(subscription.id) # subscription id
        
        udf2 = str(user_object.id) # user object

        udf3 = str(encPassword.decode("utf-8")) # encoded Password

        udf4 = str(merchant_subscriptions_key.id) # decode key id

        udf5 = str(business_ids) # Business Ids

        udf6 = ""

        hashSequence = key + "|" + txnid + "|" + amount + "|" + productinfo + "|" + firstname + "|" + email + "|" + udf1 + "|" + udf2 + "|" + udf3 + "|" + udf4 + "|" + udf5 + "|" + udf6 + "|||||" + SALT

        hash_string = hashSequence.encode('utf-8')

        hashh = hashlib.sha512(hash_string).hexdigest().lower()

        data.append({
            "MERCHANT_KEY": key,
            "firstname" : firstname,
            "email" : email,
            "phone": phone,
            "surl": surl,
            "furl" : furl,
            "hashh":hashh,
            "posted":posted,
            "txnid":txnid,
            "hash_string":str(hash_string),
            "amount":amount,
            "productinfo":productinfo,
            "udf1":udf1,
            "udf2":udf2,
            "udf3":udf3,
            "udf4":udf4,
            "udf5":udf5,
            "udf6":udf6,
            "subscription_id": subscription.id,
            "action":action,
            })

        if data:
            return JsonResponse({'status':'success', 'data': data}, status=200)
        else:
            return JsonResponse({'status' : 'error', 'message': "Fail to Retrieve Data."}, status=400)


class GetBusinessNameByCategory(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        merchant_business_category = request.POST['merchant_business_category']

        merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']
        all_business = MerchantProfile.objects.filter(m_user=merchant_id)

        business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)
     
        merchant_state = business_object.m_state

        result = []
        for active_category in all_business:
            business_name = active_category.m_business_name + "("+ active_category.m_area +")"
            if int(merchant_business_category) == 11:
                if int(active_category.m_business_category.id) == int(merchant_business_category):
                    result.append({
                        'id':active_category.id,
                        'business_name':business_name
                    })
            elif int(merchant_business_category) == 12:
                if int(active_category.m_business_category.id) == int(merchant_business_category):
                    result.append({
                        'id':active_category.id,
                        'business_name':business_name
                    })
            elif int(active_category.m_business_category.id) != 11 and int(active_category.m_business_category.id) != 12:
                result.append({
                    'id':active_category.id,
                    'business_name':business_name
                })


        if result:
            return JsonResponse({'status':'success', 'data': result}, status=200)
        else:
            return JsonResponse({'status' : 'error', 'message': "No Data Found."}, status=400)

            

        
class MerchantParkingPassList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        m_business_id = request.POST['m_business_id']

        result = ParkingLotPass.objects.filter(m_business_id = m_business_id).order_by('-id')

        data = []

        # today = date.today()
        for parkingPass in result:

            try:
                business_name = MerchantProfile.objects.filter(id = parkingPass.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            base_url = "http://157.230.228.250/"

            try:
                m_business = MerchantProfile.objects.filter(id = parkingPass.m_business_id)
                
                if m_business[0].m_business_logo:
                    business_logo = str(base_url) + str(m_business[0].m_business_logo.url)
                else:
                    business_logo = ""
            except:
                business_logo = ""

            # if parkingPass.valid_to >= today:
            data.append({
                        "id": parkingPass.id,
                        "business_name": business_name,
                        "business_logo": business_logo,
                        "mobile_no": parkingPass.mobile_no,
                        "amount": parkingPass.amount,
                        "vehical_no": parkingPass.vehical_no,
                        "valid_from": datetime.strptime(str(parkingPass.valid_from,), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        "valid_to": datetime.strptime(str(parkingPass.valid_to), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        "comments": parkingPass.comments,
                        "vehical_no" : parkingPass.vehical_no,
                        "created_at" : parkingPass.created_at,
                        "pass_type": parkingPass.pass_type,
                        "company_id": parkingPass.company_id,
                        "company_name": parkingPass.company_name,
                        "vehicle_type": parkingPass.vehicle_type
                    })

        if result:
            return JsonResponse({'status': "success", 'data': data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Data not available !!!"}, status=400)


class CreateMerchantPaymentSetting(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        payu_key = request.POST['payu_key']

        payu_salt = request.POST['payu_salt']

        Result = MerchantPaymentSetting.objects.update_or_create(m_business_id = m_business_id, defaults={'payu_key': payu_key, 'payu_salt': payu_salt })

        if Result:
            return JsonResponse({'status': 'success', 'message': 'Payment Setting Stored Successfully !!!'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Fail to Create !!!'}, status=400)


class ShowMerchantPaymentSetting(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        m_business_id = request.POST['m_business_id']

        try:
            data = MerchantPaymentSetting.objects.get(m_business_id = m_business_id)
        except:
            data = ""
        if data: 
            payu_key = data.payu_key
            payu_salt = data.payu_salt
        else: 
            payu_key = ""
            payu_salt = ""


        if data:
            return JsonResponse({'status': "success", "payu_key":payu_key, "payu_salt":payu_salt}, status=200)

        else:
            return JsonResponse({'status': "success", "payu_key":payu_key, "payu_salt":payu_salt}, status=200)



class MerchantNoticeBoardList(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST['user_id']

        notice_details = []

        notice_data = OwnerSentNotice.objects.filter(user_id=GreenBillUser.objects.get(id = user_id)).order_by('-id')

        for notice in notice_data:

            notification_list = OnwerNoticeBoard.objects.filter(id=notice.notice_id_id).order_by('-id')
            
            for notification in notification_list:
                owner_user_object = GreenBillUser.objects.filter(mobile_no = notification.owner_id)

                if notification.notice_file:
                    notice_file = notification.notice_file.url
                else:
                    notice_file = ""

                notice_details.append({
                    'id': notification.id,
                    'name' : owner_user_object[0].first_name + " " + owner_user_object[0].last_name,
                    'notice_title': notification.notice_title,
                    'message':notification.message,
                    'notice_file': notice_file,
                    'created_at' : timezone.localtime(notification.created_at).strftime("%d-%m-%Y"),
                     })

        notice_data = merchant_notice_sent.objects.filter(user_id=GreenBillUser.objects.get(id = user_id)).order_by('-id')
    
        for notice in notice_data:
            
            notification_list = Merchant_Notice_Model.objects.filter(id=notice.notice_id_id).order_by('-id')

            for notification in notification_list:

                if notification.notice_file:
                    notice_file = notification.notice_file.url
                else:
                    notice_file = ""
                    
                owner_user_object = GreenBillUser.objects.filter(mobile_no = notification.owner_id)
                notice_details.append({
                    'id': notification.id,
                    'name' : owner_user_object[0].first_name + " " + owner_user_object[0].last_name,
                    'notice_title': notification.notice_title,
                    'message':notification.message,
                    'notice_file': notice_file,
                    'created_at' :  timezone.localtime(notification.created_at).strftime("%d-%m-%Y"),
                    })

        if notice_details:
            return JsonResponse({'status': 'success', 'data' : notice_details}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)

@csrf_exempt
def GetUserCitiesByStates(request):

    if request.method == "POST":

        selected_state = request.POST.get('state')

        states = StateCityData.objects.values('state').distinct().order_by('state')

        states_list = []

        cities_list = []

        for obj in states:
            states_list.append(obj)

        if selected_state:

            list1 = []

            user_state = StateCityData.objects.filter(state = selected_state)

            for city in user_state:
                list1.append({
                    "c_city": city.city
                })
                
            for x in list1:
                if x['c_city'] not in cities_list:
                    if x['c_city'] != '':
                        cities_list.append({"city": x['c_city']})


            cities_list.sort(key = lambda x: x['city'])


        if states:
            return JsonResponse({'status': 'success', 'states' : states_list, 'cities': cities_list}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)





class HitNumberOfViewsAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(request):
        merchant_mobile = request.POST.get("merchant_mobile")
        result = contact_card.objects.get(card_phone_no=merchant_mobile)
        print(result)
        result.share = result.share + 1
        result.save()
        if result:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)




 








@csrf_exempt
def MerchantAnalysisApi(request):
    
    if request.method == "POST":

            # data =  Card_feedback.objects.filter(merchant_business_id=merchant_business_id).reverse()
            # var = contact_card.objects.filter(merchant_business_id=merchant_business_id)
    
            data =  Card_feedback.objects.all()
    
            print(data)
        
            # context = {'data':data}

            # serializer = MerchantAnalysisCardSerializer(context)
    

            return JsonResponse({'status': 'success', 'message': "Data Recived",'data':data}, status=200)
        
    else:
            print('in except')   
            return JsonResponse({'status': 'Error', 'message': "Failed to get Data !!!"}, status=400)



# import random
# import os
# import hashlib
# from cryptography.fernet import Fernet
# from dateutil.relativedelta import relativedelta
# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse, JsonResponse
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.parsers import JSONParser
# from owner_notice_board.sendsms import *
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework import generics
# from rest_framework import mixins
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token  # To generate the token
# from rest_framework import viewsets
# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework.authtoken.views import ObtainAuthToken
# from django.contrib.auth import authenticate, login
# from rest_framework.authtoken.models import Token
# from users.models import GreenBillUser, UserProfileImage, MerchantProfile, Merchant_users, MerchantUniqueIds
# from .serializers import *
# from django.contrib.auth import update_session_auth_hash
# from datetime import datetime, timedelta
# from django.utils import formats
# from authentication.models import *
# from merchant_stamp.models import *
# from owner_stamp.models import *
# from django.conf import settings
# from django.core.mail import send_mail
# from category_and_tags.models import business_category
# from bill_design.models import authorised_sign
# from offers.models import OfferModel
# from referral_points.models import *
# from coupon.models import *

# import base64
# from django.core.files.base import ContentFile
# import calendar

# import json
# from django.core import serializers
# from django.db.models import Sum

# from merchant_enquiry.models import *
# from merchant_software_apis.models import *
# from parking_lot_apis.models import *
# from petrol_pump_apis.models import *
# from customer_info.models import *

# import random
# import string
# from bill_design.models import *

# from merchant_role.models import *
# from users.models import *

# from merchant_setting.models import *
# from merchant_promotion.models import *

# from datetime import date

# from suggest.models import *

# # SMS
# import requests
# import time
# import pyshorteners

# from share_a_word.models import *

# from suggest_a_brand.models import *

# from feedback.models import *

# from merchant_cashmemo_design.models import Cash_Memo_Design_Model, CustomerCashMemoDetailModels, CustomerReceiptDetailsModels,save_template_for_cashmemo,save_template_for_receipt

# from supports_faq.models import *


# from coupon.models import CouponModel

# from offers.models import *

# from merchant_payment.models import *

# from merchant_setting.models import MerchantPaymentSetting

# from my_subscription.models import *

# from django.db.models import Q

# from subscription_plan.models import *

# from super_admin_settings.models import notification_settings

# from merchant_software_apis.models import DeviceId, MerchantBill
# import socket
# from pyfcm import FCMNotification
# import inflect
# from merchant_software_apis.models import DeviceId
# import socket
# from pyfcm import FCMNotification

# from payments.models import *

# from django.utils import timezone

# from owner_notice_board.models import *
# from merchant_notice.models import *
# from merchant_software_apis.models import ExePrintStatus
# from referral_points.models import *
# from promotions.models import *

# @csrf_exempt
# def merchantLogin(request):

#     if request.method == "POST":

#         mobile_no = request.POST['mobile_no']
#         password = request.POST['password']

#         try:

#             if GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']:

#                 user = authenticate(mobile_no=mobile_no, password=password)

#                 if user:
#                     is_merchant = GreenBillUser.objects.filter(
#                         mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
#                     serializer = merchantSerializer(user)

#                     try:
#                         token = Token.objects.create(user=user)
#                     except:
#                         token = Token.objects.get(user_id=user.id)

#                     if user is not None and is_merchant:
#                         return JsonResponse({'status': 'success', 'token': token.key, 'data': serializer.data}, status=200)
#                     else:
#                         return JsonResponse({'status': 'error', 'message': "Something went wrong !!!"}, status=400)
#                 else:
#                     return JsonResponse({'status': 'error', 'message': "Invalid credentials !!!"}, status=400)

#             else:
#                 return JsonResponse({'status': 'error', 'message': "User not register !!!"}, status=400)
#         except:
#             return JsonResponse({'status': 'error', 'message': "User not register !!!"}, status=400)

#     else:
#         return JsonResponse({'status': 'error', 'message': "Something went wrong !!!"}, status=400)


# class merchantChangePassword(generics.GenericAPIView):
#     serializer_class = merchantSerializer
#     queryset = GreenBillUser.objects.all()

#     lookup_field = 'id'

#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         user_id = request.POST['user_id']

#         user = GreenBillUser.objects.get(id=user_id)

#         old_password = request.POST['old_password']

#         success = GreenBillUser.check_password(user, old_password)

#         if success == True:
#             new_password = request.POST['new_password']

#             user.set_password(new_password)
#             user.save()

#             update_session_auth_hash(request, user)  # Important!

#             return JsonResponse({'status': 'success', 'message': "Password changed successfully !!!"}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': "Failed, old password not matched !!!"}, status=400)


# @csrf_exempt
# def getMerchantBusinessCategory(request):
#     if request.method == "GET":
#         business_categories = business_category.objects.all()
#         serializer = BusinessCategorySerializer(business_categories, many=True)
#         # return JsonResponse({'status' : 'success', 'data' : serializer.data}, status=200)
#         # return Response(serializer.data)
#         return JsonResponse(serializer.data, status=200, safe=False)
#     else:
#         return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)

# @csrf_exempt
# def validateMerchantMobileNumber(request):
#     if request.method == "POST":
#         mobile_no = request.POST['mobile_no']

#         try:
#             user_object = GreenBillUser.objects.filter(mobile_no = mobile_no)

#         except:
#             user_object = ''

#         if user_object:
#             if user_object[0].is_staff:
#                 return JsonResponse({'status':'error', 'message': "Mobile number already registered."}, status=400)

#             elif user_object[0].is_partner:
#                 return JsonResponse({'status':'error', 'message': "Mobile number already registered."}, status=400)

#             elif (user_object[0].is_merchant or user_object[0].is_merchant_staff):
#                 return JsonResponse({'status':'error', 'message': "Mobile number already registered."}, status=400)

#             elif user_object[0].is_customer:
#                 return JsonResponse({'status':'success', 'message': "Mobile number not registered."}, status=200)
                
#             else:
#                 return JsonResponse({'status':'error', 'message': "Mobile number already registered."}, status=400)
#         else:
#             return JsonResponse({'status':'success', 'message': "Mobile number not registered."}, status=200)

#         # try:
#         #     is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
#         # except:
#         #     is_merchant = ""

#         # if is_merchant:
#         #     return JsonResponse({'status':'error', 'message': "Mobile number already registered."}, status=400)
#         # else:
#         #     return JsonResponse({'status':'success', 'message': "Mobile number not registered."}, status=200)
#     else:
#         return JsonResponse({'status':'error', 'message': "Something went wrong."}, status=400)
        

# @csrf_exempt
# def generateOtpMerchnat(request):
#     if request.method == "POST":
#         mobile_no = request.POST['mobile_no']
#         signature = request.POST['signature']
#         # email = request.POST['m_email']

#         try:
#             is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
#         except:
#             is_merchant = ""

#         if is_merchant:
#             return JsonResponse({'status':'error', 'message': "Mobile number exists as merchant."}, status=400)
#         else:
#             if mobile_no:
#                 otp = random.randint(99999, 999999)
#                 otp_validation.objects.update_or_create(
#                     mobile_no=mobile_no, defaults={'otp': otp})

#                 # subject = 'welcome to Green Bill'
#                 # message = f'Please use this OTP: {otp}'
#                 # email_from = settings.EMAIL_HOST_USER
#                 # recipient_list = [email,]
#                 # send_mail( subject, message, email_from, recipient_list)

#                 ts = int(time.time())

#                 sms_data_temp = {
#                         "keyword":"App New Registration OTP",
#                         "timeStamp":ts,
#                         "dataSet":
#                             [
#                                 {
#                                     "UNIQUE_ID":"GB-" + str(ts),
#                                     "MESSAGE":"<"+"#"+"> "+"Dear Green Bill user, use " + str(otp) + " as OTP for your registration." + str(signature),
#                                     "OA":"GRBILL",
#                                     "MSISDN":str(mobile_no), # Recipient's Mobile Number
#                                     "CHANNEL":"SMS",
#                                     "CAMPAIGN_NAME":"hind_user",
#                                     "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                     "USER_NAME":"hind_hsi",
#                                     "DLT_TM_ID":"1001096933494158", # TM ID
#                                     "DLT_CT_ID":"1007162106850723917", # Template Id
#                                     "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                 }
#                             ]
#                         }

#                 url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                 response = requests.post(url, json = sms_data_temp)

#                 if response.status_code == 200:
#                     return JsonResponse({'status': 'success'}, status=200)
#                 else:
#                     return JsonResponse({'status': 'error', 'message': "Failed to send otp !!!"}, status=400)
#             else:
#                 return JsonResponse({'status': 'error'}, status=403)
#         # elif mobile_exists[0].is_customer:
#         #     return JsonResponse({'status':'error', 'message': "Mobile Number is registered as Customer. So please Use Customer Web Panel OR Customer App!!!"}, status=400)
#         # elif mobile_exists[0].is_merchant or mobile_exists[0].is_merchant_staff:
#         #     return JsonResponse({'status':'error', 'message': "Mobile Number is registered as Merchant or Merchant user. So please Use Merchant Web Panel OR Merchant App!!!"}, status=400)
#         # elif mobile_exists[0].is_partner:
#         #     return JsonResponse({'status':'error', 'message': "Mobile Number is registered as Partner. So please Use Partner Web Panel.!!!"}, status=400)
#         # elif mobile_exists[0].is_staff:
#         #     return JsonResponse({'status':'error', 'message': "Mobile Number is registered as Owner or Owner Staff. So please Use Owner Web Panel.!!!"}, status=400)
#         # else:
#         #     return JsonResponse({'status':'error', 'message': "Customer Exists, Please use different Mobile Number !!!"}, status=400)
#     else:
#         return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


# @csrf_exempt
# def generateOtpMerchantForgotPassword(request):
#     if request.method == "POST":
#         mobile_no = request.POST['mobile_no']
#         signature = request.POST['signature']

#         try:
#             if mobile_no:
#                 mobile_exists = GreenBillUser.objects.get(mobile_no=mobile_no)
#                 is_merchant = GreenBillUser.objects.filter(
#                     mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
#                 email = GreenBillUser.objects.filter(
#                     mobile_no=mobile_no).values('m_email')[0]['m_email']
#                 if mobile_exists and is_merchant:
#                     otp = random.randint(99999, 999999)
#                     otp_validation.objects.update_or_create(
#                         mobile_no=mobile_no, defaults={'otp': otp})

#                     # subject = 'welcome to Green Bill'
#                     # message = f'Please use this OTP: {otp}'
#                     # email_from = settings.EMAIL_HOST_USER
#                     # recipient_list = [email,]
#                     # mail_res = send_mail( subject, message, email_from, recipient_list )
#                     # print(mail_res)

#                     ts = int(time.time())

#                     sms_data_temp = {
#                             "keyword":"App Forgot Password OTP",
#                             "timeStamp":ts,
#                             "dataSet":
#                                 [
#                                     {
#                                         "UNIQUE_ID":"GB-" + str(ts),
#                                         "MESSAGE":"<"+"#"+"> "+"Dear Green Bill user, use " + str(otp) + " as OTP to reset your password. " + str(signature),
#                                         "OA":"GRBILL",
#                                         "MSISDN":str(mobile_no), # Recipient's Mobile Number
#                                         "CHANNEL":"SMS",
#                                         "CAMPAIGN_NAME":"hind_user",
#                                         "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                         "USER_NAME":"hind_hsi",
#                                         "DLT_TM_ID":"1001096933494158", # TM ID
#                                         "DLT_CT_ID":"1007162107620813728", # Template Id
#                                         "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                     }
#                                 ]
#                             }

#                     url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                     response = requests.post(url, json = sms_data_temp)

#                     if response.status_code == 200:
#                         return JsonResponse({'status': 'success'}, status=200)
#                     else:
#                         return JsonResponse({'status': 'error', 'message': "Failed to send otp !!!"}, status=400)
#                 else:
#                     return JsonResponse({'status': 'error', 'message': 'User not registered'}, status=400)
#             else:
#                 return JsonResponse({'status': 'error'}, status=403)
#         except:
#             return JsonResponse({'status': 'error', 'message': 'User not registered'}, status=400)
#     else:
#         return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


# @csrf_exempt
# def otpValidateMerchant(request):
#     if request.method == "POST":
#         temp_otp = request.POST['otp']
#         mobile_no = request.POST['mobile_no']
#         otp = otp_validation.objects.filter(
#             mobile_no=mobile_no).values('otp')[0]['otp']

#         if otp == temp_otp:
#             return JsonResponse({'status': 'success'}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid otp'}, status=406)

#     else:
#         return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


# @csrf_exempt
# def ReferralCodeValidateMerchant(request):
#     if request.method == "POST":
#         m_used_referral_code = request.POST['m_used_referral_code']

#         try:
#             result = GreenBillUser.objects.get(merchant_referral_code = m_used_referral_code)
#         except:
#             result = ""

#         if result:
#             return JsonResponse({'status': 'success'}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid Referral Code !!!'}, status=406)


# @csrf_exempt
# def merchantRegister(request):

#     if request.method == "POST":

#         mobile_no = request.POST['mobile_no']
#         password = request.POST['password']

#         exists = GreenBillUser.objects.filter(mobile_no=mobile_no)

#         if exists:
#             is_customer = GreenBillUser.objects.filter(
#                 mobile_no=mobile_no).values('is_customer')[0]['is_customer']
#         else:
#             is_customer = False

#         if is_customer == True:

#             user = GreenBillUser.objects.get(mobile_no=mobile_no)

#             m_email = request.POST['m_email']
#             is_merchant = 1
#             is_active = 1
#             is_merchant_staff = 1

#             letters = string.ascii_letters
#             digit = string.digits

#             random_string = str(user.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

#             try:
#                 m_used_referral_code = request.POST['m_used_referral_code']
#             except:
#                 m_used_referral_code = ""

#             GreenBillUser.objects.filter(id=user.id).update(
#                 m_email=m_email, is_merchant=is_merchant, is_merchant_staff = is_merchant_staff, is_active=is_active, merchant_referral_code = random_string[0:6], m_used_referral_code = m_used_referral_code)
            
#             # Unique Id Start

#             try:
#                 last_unique_id = MerchantUniqueIds.objects.all().last()
#             except:
#                 last_unique_id = ""

#             if not last_unique_id:
#                 m_unique_id = str("GBM") + str("01").zfill(6)
#                 no = 1
#             else:
#                 last_no = last_unique_id.m_unique_no
#                 no = int(last_no) + 1
#                 m_unique_id = str("GBM") + str(no).zfill(6)

#             unique_id_status = GreenBillUser.objects.filter(mobile_no = user).update(m_unique_id = m_unique_id)

#             if unique_id_status:
#                 MerchantUniqueIds.objects.create(m_unique_no = no)

#             # Unique Id End

#             # Email Verification Start

#             if m_email:
#                 random_string = str(user.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(5))
#                 email_verification_status = GreenBillUser.objects.filter(mobile_no = user).update(email_verification_url = random_string)
#                 s = pyshorteners.Shortener()
#                 email_verification_url = "http://157.230.228.250/email-verification/"+str(random_string)+"/"
#                 short_url = s.tinyurl.short(email_verification_url)
#                 if email_verification_status and short_url:
#                     subject = 'Account Verification'
#                     message = f'Thank you for choosing GreenBill. Please click on below link to verify Email Id,\n' + str(short_url) + '\n\nTeam GreenBill'
#                     email_from = settings.EMAIL_HOST_USER
#                     recipient_list = [m_email,]
#                     send_mail( subject, message, email_from, recipient_list)

#             # Email Verification End

#             merchant_user = Merchant_users.objects.create(user_id=user, merchant_user_id=user)

#             m_business_name = request.POST["m_business_name"]
#             m_business_category_id = request.POST["m_business_category"]
#             m_city = request.POST["m_city"]
#             m_district = request.POST["m_district"]
#             m_state = request.POST["m_state"]
#             m_pin_code = request.POST["m_pin_code"]
#             m_area = request.POST['m_area']

#             try:
#                 m_used_referral_code = request.POST['m_used_referral_code']
#             except:
#                 m_used_referral_code = ""

#             m_business_category = business_category.objects.get(
#                 id=m_business_category_id)

#             # MerchantProfile.objects.create(m_user=user, m_business_name=m_business_name, m_business_category=m_business_category,
#             #                                m_city=m_city, m_area=m_area, m_district=m_district, m_state=m_state, m_pin_code=m_pin_code, m_active_account=1)

            
#             merchant_profile_id = MerchantProfile.objects.create(m_user=user, m_business_name=m_business_name, m_business_category=m_business_category, m_city=m_city, m_area=m_area, m_district=m_district, m_state=m_state, m_pin_code=m_pin_code, m_active_account=1)

#             role_name1 = 'Admin'

#             role_name2 = 'Exe User'

#             merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name1)

#             merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name2)




#             newUser = GreenBillUser.objects.get(id=user.id)

#             temp = newUser.set_password(password)
#             temp2 = newUser.save()

#             update_session_auth_hash(request, user)

#             notification_object = notification_settings.objects.get(id = 6)

#             if notification_object.send_sms:

#                 if m_business_category_id == "11":

#                     ts = int(time.time())

#                     data_temp = {
#                             "keyword":"Welcome Message",
#                             "timeStamp":ts,
#                             "dataSet":
#                                 [
#                                     {
#                                         "UNIQUE_ID":"GB-" + str(ts),
#                                         "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
#                                         "OA":"GBPUMP",
#                                         "MSISDN":mobile_no, # Recipient's Mobile Number
#                                         "CHANNEL":"SMS",
#                                         "CAMPAIGN_NAME":"hind_user",
#                                         "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                         "USER_NAME":"hind_hsi",
#                                         "DLT_TM_ID":"1001096933494158", # TM ID
#                                         "DLT_CT_ID":"1007162098316946419", # Template Id
#                                         "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                     }
#                                 ]
#                             }

#                     url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                     response = requests.post(url, json = data_temp)

#                 elif m_business_category_id == "12":

#                     ts = int(time.time())

#                     data_temp = {
#                             "keyword":"Welcome Message",
#                             "timeStamp":ts,
#                             "dataSet":
#                                 [
#                                     {
#                                         "UNIQUE_ID":"GB-" + str(ts),
#                                         "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
#                                         "OA":"GBPARK",
#                                         "MSISDN":mobile_no, # Recipient's Mobile Number
#                                         "CHANNEL":"SMS",
#                                         "CAMPAIGN_NAME":"hind_user",
#                                         "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                         "USER_NAME":"hind_hsi",
#                                         "DLT_TM_ID":"1001096933494158", # TM ID
#                                         "DLT_CT_ID":"1007162098316946419", # Template Id
#                                         "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                     }
#                                 ]
#                             }

#                     url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                     response = requests.post(url, json = data_temp)

#                 else:

#                     ts = int(time.time())

#                     data_temp = {
#                             "keyword":"Welcome Message",
#                             "timeStamp":ts,
#                             "dataSet":
#                                 [
#                                     {
#                                         "UNIQUE_ID":"GB-" + str(ts),
#                                         "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
#                                         "OA":"GBBILL",
#                                         "MSISDN":mobile_no, # Recipient's Mobile Number
#                                         "CHANNEL":"SMS",
#                                         "CAMPAIGN_NAME":"hind_user",
#                                         "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                         "USER_NAME":"hind_hsi",
#                                         "DLT_TM_ID":"1001096933494158", # TM ID
#                                         "DLT_CT_ID":"1007162098316946419", # Template Id
#                                         "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                     }
#                                 ]
#                             }

#                     url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                     response = requests.post(url, json = data_temp)

#             if notification_object.send_email:
#                 subject = 'New Merchant Registration'
#                 message = f'Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.'
#                 email_from = settings.EMAIL_HOST_USER
#                 recipient_list = [m_email,]
#                 send_mail( subject, message, email_from, recipient_list)

#             if notification_object.send_app_notification:
#                 device = DeviceId.objects.filter(mobile_no=mobile_no).first()
#                 push_service = FCMNotification(api_key=settings.API_KEY)

#                 if device != None:
#                     registration_id = device.device_id
#                 else:
#                     registration_id = ""

#                 message_title = "New Merchant Registration"
#                 message_body = "HThank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login."
#                 result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)


#             return JsonResponse({'status': 'success', 'message': 'User created successfully !!!'}, status=200)

#         elif is_customer == False:

#             serializer = merchantSerializer_register(data=request.POST)

#             # print(serializer)

#             if serializer.is_valid():

#                 user = serializer.save()

#                 user.set_password(request.POST["password"])
#                 user.save()

#                 letters = string.ascii_letters
#                 digit = string.digits

#                 random_string = str(user.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

#                 try:
#                     m_used_referral_code = request.POST['m_used_referral_code']
#                 except:
#                     m_used_referral_code = ""

#                 GreenBillUser.objects.filter(id=user.id).update(merchant_referral_code = random_string[0:6], m_used_referral_code = m_used_referral_code, is_merchant_staff = True, is_merchant = True)

#                 m_email = request.POST['m_email']

#                 # Unique Id Start

#                 try:
#                     last_unique_id = MerchantUniqueIds.objects.all().last()
#                 except:
#                     last_unique_id = ""

#                 if not last_unique_id:
#                     m_unique_id = str("GBM") + str("01").zfill(6)
#                     no = 1
#                 else:
#                     last_no = last_unique_id.m_unique_no
#                     no = int(last_no) + 1
#                     m_unique_id = str("GBM") + str(no).zfill(6)

#                 unique_id_status = GreenBillUser.objects.filter(mobile_no = user).update(m_unique_id = m_unique_id)

#                 if unique_id_status:
#                     MerchantUniqueIds.objects.create(m_unique_no = no)

#                 # Unique Id End

#                 # Email Verification Start

#                 if m_email:
#                     random_string = str(user.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(5))
#                     email_verification_status = GreenBillUser.objects.filter(mobile_no = user).update(email_verification_url = random_string)
#                     s = pyshorteners.Shortener()
#                     email_verification_url = "http://157.230.228.250/email-verification/"+str(random_string)+"/"
#                     short_url = s.tinyurl.short(email_verification_url)
#                     if email_verification_status and short_url:
#                         subject = 'Account Verification'
#                         message = f'Thank you for choosing GreenBill. Please click on below link to verify Email Id,\n' + str(short_url) + '\n\nTeam GreenBill'
#                         email_from = settings.EMAIL_HOST_USER
#                         recipient_list = [m_email,]
#                         send_mail( subject, message, email_from, recipient_list)

#                 # Email Verification End

#                 merchant_user = Merchant_users.objects.create(user_id=user, merchant_user_id=user)

#                 m_business_name = request.POST["m_business_name"]
#                 m_business_category_id = request.POST["m_business_category"]
#                 m_city = request.POST["m_city"]
#                 m_district = request.POST["m_district"]
#                 m_state = request.POST["m_state"]
#                 m_pin_code = request.POST["m_pin_code"]
#                 m_area = request.POST['m_area']
                

#                 m_business_category = business_category.objects.get(
#                     id=m_business_category_id)

#                 merchant_profile_id = MerchantProfile.objects.create(m_user=user, m_business_name=m_business_name, m_business_category=m_business_category, m_city=m_city, m_area=m_area, m_district=m_district, m_state=m_state, m_pin_code=m_pin_code, m_active_account=1)

#                 role_name1 = 'Admin'
#                 role_name2 = 'Exe User'
#                 role_name3 = 'Operator'

#                 if merchant_profile_id.m_business_category.id != 11 and merchant_profile_id.m_business_category.id != 12:
#                     merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name1)

#                     merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name2)

#                 if merchant_profile_id.m_business_category.id == 11 or merchant_profile_id.m_business_category.id == 12:
#                     merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name1)

#                     merchant_role.objects.create(merchant_business_id = merchant_profile_id, merchant_id = merchant_user.user_id, role_name = role_name3)



#                 notification_object = notification_settings.objects.get(id = 6)

#                 if notification_object.send_sms:

#                     if m_business_category_id == "11":

#                         ts = int(time.time())

#                         data_temp = {
#                                 "keyword":"Welcome Message",
#                                 "timeStamp":ts,
#                                 "dataSet":
#                                     [
#                                         {
#                                             "UNIQUE_ID":"GB-" + str(ts),
#                                             "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
#                                             "OA":"GBPUMP",
#                                             "MSISDN":mobile_no, # Recipient's Mobile Number
#                                             "CHANNEL":"SMS",
#                                             "CAMPAIGN_NAME":"hind_user",
#                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                             "USER_NAME":"hind_hsi",
#                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                             "DLT_CT_ID":"1007162098316946419", # Template Id
#                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                         }
#                                     ]
#                                 }

#                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                         response = requests.post(url, json = data_temp)

#                     elif m_business_category_id == "12":

#                         ts = int(time.time())

#                         data_temp = {
#                                 "keyword":"Welcome Message",
#                                 "timeStamp":ts,
#                                 "dataSet":
#                                     [
#                                         {
#                                             "UNIQUE_ID":"GB-" + str(ts),
#                                             "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
#                                             "OA":"GBPARK",
#                                             "MSISDN":mobile_no, # Recipient's Mobile Number
#                                             "CHANNEL":"SMS",
#                                             "CAMPAIGN_NAME":"hind_user",
#                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                             "USER_NAME":"hind_hsi",
#                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                             "DLT_CT_ID":"1007162098316946419", # Template Id
#                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                         }
#                                     ]
#                                 }

#                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                         response = requests.post(url, json = data_temp)

#                     else:

#                         ts = int(time.time())

#                         data_temp = {
#                                 "keyword":"Welcome Message",
#                                 "timeStamp":ts,
#                                 "dataSet":
#                                     [
#                                         {
#                                             "UNIQUE_ID":"GB-" + str(ts),
#                                             "MESSAGE":"Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.",
#                                             "OA":"GBBILL",
#                                             "MSISDN":mobile_no, # Recipient's Mobile Number
#                                             "CHANNEL":"SMS",
#                                             "CAMPAIGN_NAME":"hind_user",
#                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                             "USER_NAME":"hind_hsi",
#                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                             "DLT_CT_ID":"1007162098316946419", # Template Id
#                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                         }
#                                     ]
#                                 }

#                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                         response = requests.post(url, json = data_temp)

#                 if notification_object.send_email:
#                     subject = 'New Merchant Registration'
#                     message = f'Thank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login.'
#                     email_from = settings.EMAIL_HOST_USER
#                     recipient_list = [m_email,]
#                     send_mail( subject, message, email_from, recipient_list)

#                 if notification_object.send_app_notification:
#                     device = DeviceId.objects.filter(mobile_no=mobile_no).first()
#                     push_service = FCMNotification(api_key=settings.API_KEY)

#                     if device != None:
#                         registration_id = device.device_id
#                     else:
#                         registration_id = ""

#                     message_title = "New Merchant Registration"
#                     message_body = "HThank you for choosing GreenBill as your Digital Billing Buddy. Please visit our website or download GreenBill Merchant App to login."
#                     result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

#                 return JsonResponse({'status': 'success', 'message': 'User created successfully !!!'},
#                                     status=200)

#             else:
#                 return JsonResponse({'status': 'error', 'message': serializer.errors}, status=400)

#         else:
#             return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)
#     else:
#         return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


# @csrf_exempt
# def forgotPasswordMerchant(request):
#     if request.method == "POST":
#         mobile_no = request.POST['mobile_no']
#         new_password = request.POST['new_password']

#         result = GreenBillUser.objects.filter(mobile_no=mobile_no).values('id')[0]['id']
#         user = GreenBillUser.objects.get(id=result)
#         success = GreenBillUser.check_password(user, new_password)

#         if success == True:
#             return JsonResponse({'status': 'error', 'message': 'New Password cannot be same as Old Password !!!'}, status=400)
            
#         else:
#             if result:
                
#                 user.set_password(new_password)
#                 user.save()

#                 update_session_auth_hash(request, user)  # Important!

#                 return JsonResponse({'status': 'success', 'message': 'Password changed successfully !!!'}, status=200)
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'User not found !!!'}, status=200)
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Something went wrong, please try again later !!!'}, status=400)


# # def base64_file(data, name=None):
# #     _format, _img_str = data.split(';base64,')
# #     _name, ext = _format.split('/')
# #     if not name:
# #         name = _name.split(":")[-1]
# #     return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))


# class setMerchantProfileData(generics.GenericAPIView):
#     serializer_class = merchantSerializer
#     queryset = GreenBillUser.objects.all()

#     lookup_field = 'id'

#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         if request.method == "POST":
#             user_id = request.POST['user_id']
#             m_email = request.POST["m_email"]
#             first_name = request.POST["first_name"]
#             last_name = request.POST["last_name"]
            
#             m_dob = request.POST.get("m_dob",None) 

#             if m_dob is not None and m_dob != '' and m_dob != "":
#                 formatted_m_dob = datetime.strptime(m_dob, '%d-%m-%Y').strftime('%Y-%m-%d')
#             else:
#                 formatted_m_dob = None


#             m_designation = request.POST["m_designation"]
#             m_adhaar_number = request.POST["m_adhaar_number"]
#             m_pan_number = request.POST["m_pan_number"]
#             # m_profile_image = request.FILES["m_profile_image"]

#             # m_business_name = request.POST["m_business_name"]
#             # # m_business_category = request.POST["m_pan_number"]
#             # m_area = request.POST["m_area"]
#             # m_city = request.POST["m_city"]
#             # m_district = request.POST["m_district"]
#             # m_state = request.POST["m_state"]
#             # m_pin_code = request.POST["m_pin_code"]

#             # MerchantProfile.objects.update_or_create(m_user = request.user, defaults={ "m_business_name" : m_business_name, "m_city" : m_city, "m_area" : m_area, "m_district" : m_district, "m_state" : m_state, "m_pin_code" : m_pin_code, "m_active_account" : 1})

#             # print(m_profile_image)

#             profile = GreenBillUser.objects.filter(id=user_id).update(m_email=m_email, first_name=first_name, last_name=last_name,
#                 m_dob=formatted_m_dob, m_designation=m_designation, m_adhaar_number=m_adhaar_number, m_pan_number=m_pan_number)

#             # if m_profile_image:

#             #     #random_no = random.randint(9999999, 999999999)

#             #     #m_profile_image = base64_file(data=m_profile_image_temp, name="profile_image"+str(random_no))

#             #     image = UserProfileImage.objects.update_or_create(user_id = user_id, defaults={
#             #     "m_profile_image" : m_profile_image })

#             if profile:
#                 return JsonResponse({'status': 'success', 'message': "Profile edited successfully !!!"}, status=200)
#             else:
#                 return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)

#         else:
#             return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


# class getMerchantProfileImage(generics.GenericAPIView):

#     serializer_class = merchantSerializer
#     queryset = GreenBillUser.objects.all()

#     lookup_field = 'id'

#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         if request.method == "POST":
#             user_id = request.POST['user_id']
#             b_id = request.POST['b_id']

#             if user_id:
#                 user = GreenBillUser.objects.get(id=user_id)

#                 # userDetails = UserProfileImage.objects.filter(user=user_id)
#                 try:
#                     userDetails = MerchantProfile.objects.get(id=b_id)
#                 except:
#                     userDetails = ""
#                 base_url = "http://157.230.228.250/"

#                 if user:
#                     if userDetails:
#                         try:
#                             new_dic = {
#                                 'mobile_no': user.mobile_no,
#                                 'first_name': user.first_name,
#                                 'last_name': user.last_name,
#                                 'profile_image': str(base_url) + str(userDetails.m_business_logo.url)
#                             }
#                         except:
#                             new_dic = {
#                                 'mobile_no': user.mobile_no,
#                                 'first_name': user.first_name,
#                                 'last_name': user.last_name,
#                                 'profile_image': str(base_url) + str("/media/user-profile-pic.png")
#                             }
#                     else:

#                         new_dic = {
#                             'mobile_no': user.mobile_no,
#                             'first_name': user.first_name,
#                             'last_name': user.last_name,
#                             'profile_image': str(base_url) + str("/media/user-profile-pic.png")
#                         }
#                     return JsonResponse({'status': "success", 'data': new_dic}, status=200)
#                 else:
#                     return JsonResponse({'status': "error", 'message': "User not found"}, status=400)
#             else:
#                 return JsonResponse({'status': "error", 'message': "User id is mandatory."}, status=400)
#         else:
#             return JsonResponse({'status': "error", 'message': "Something went wrong."}, status=400)


# class setMerchantProfileImage(generics.GenericAPIView):

#     serializer_class = merchantSerializer
#     queryset = GreenBillUser.objects.all()

#     lookup_field = 'id'

#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         if request.method == "POST":
#             user_id = request.POST['user_id']
#             m_profile_image = request.FILES["m_profile_image"]

#             if user_id and m_profile_image:

#                 #random_no = random.randint(9999999, 999999999)
#                 #m_profile_image = base64_file(data=m_profile_image_temp, name="profile_image"+str(random_no))

#                 image = UserProfileImage.objects.update_or_create(user_id=user_id, defaults={
#                     "m_profile_image": m_profile_image})

#                 if image:
#                     return JsonResponse({'status': "success", 'message': "Profile image uploaded successfully."}, status=200)
#                 else:
#                     return JsonResponse({'status': "error", 'message': "Failed to upload profile image."}, status=400)
#             else:
#                 return JsonResponse({'status': "error", 'message': "user_id and m_profile_image are mandatory fields."}, status=400)
#         else:
#             return JsonResponse({'status': "error", 'message': "Something went wrong."}, status=400)


# class getMerchantDetails(generics.GenericAPIView):
#     serializer_class = merchantSerializer
#     queryset = GreenBillUser.objects.all()

#     lookup_field = 'id'

#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         if request.method == "POST":

#             mobile_no = request.POST['mobile_no']
#             user_temp = GreenBillUser.objects.get(mobile_no=mobile_no)

#             is_varified = user_temp.is_verified_email

#             try:
#                 token = Token.objects.get(user_id=user_temp)
#             except:
#                 return JsonResponse({'status': "error", 'message': "Mobile no. not registered"}, status=400)

#             if request.META['HTTP_AUTHORIZATION'] == str("Token " + token.key):

#                 if GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']:
#                     user = GreenBillUser.objects.get(mobile_no=mobile_no)
#                     serializer = merchantSerializer(user)

                    

#                     base_url = "http://157.230.228.250/"

#                     try:
#                         profile_image = UserProfileImage.objects.get(
#                             user_id=user.id)
#                         if profile_image.m_profile_image:
#                             image_url = str(
#                                 base_url) + str(profile_image.m_profile_image.url)
#                         else:
#                             image_url = str(base_url) + \
#                                 str("/media/user-profile-pic.png")
#                     except:
#                         image_url = str(base_url) + \
#                             str("/media/user-profile-pic.png")

#                     return JsonResponse({'status': "success", 'profile_data': serializer.data, 'image_data': image_url, 'is_varified': is_varified}, status=200)
#                 else:
#                     return JsonResponse({'status': "error", 'message': "User not exists"}, status=400)
#             else:
#                 return JsonResponse({'status': "error", 'message': "token not valid !!!"}, status=400)
#         else:
#             return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)


# @csrf_exempt
# def removeMerchantProfileImage(request):
#     if request.method == "POST":
#         user_id = request.POST['user_id']
#         result = UserProfileImage.objects.update_or_create(
#             user_id=user_id, defaults={"m_profile_image": ""})

#         if result:
#             return JsonResponse({'status': "success", 'message': "Profile image removed successfully."}, status=200)
#         else:
#             return JsonResponse({'status': "error", 'message': "Failed to remove profile image"}, status=400)
#     else:
#         return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)


# class getMerchantGeneralSetting(generics.GenericAPIView):
#     serializer_class = merchantSerializer
#     queryset = GreenBillUser.objects.all()

#     lookup_field = 'id'

#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         if request.method == "POST":

#             m_business_id = request.POST['m_business_id']

#             data = MerchantProfile.objects.filter(id = m_business_id)

#             merchant_user_id = MerchantProfile.objects.get(id = m_business_id)

#             merchant_object = GreenBillUser.objects.get(mobile_no = merchant_user_id.m_user)

#             if data:
#                 base_url = "http://157.230.228.250"
#                 if data[0].m_GSTIN_certificate:
#                     m_GSTIN_certificate = str(base_url) + str(data[0].m_GSTIN_certificate.url)
#                 else:
#                     m_GSTIN_certificate = ""

#                 if data[0].m_CIN_certificate:
#                     m_CIN_certificate = str(base_url) + str(data[0].m_CIN_certificate.url)
#                 else:
#                     m_CIN_certificate = ""

#                 if data[0].m_business_logo:
#                     m_business_logo = str(base_url) + str(data[0].m_business_logo.url)
#                 else:
#                     m_business_logo = ""

#                 if data[0].m_business_stamp:
#                     m_business_stamp = str(base_url) + str(data[0].m_business_stamp.url)
#                 else:
#                     m_business_stamp = ""

#                 if data[0].m_digital_signature:
#                     m_digital_signature = str(base_url) + str(data[0].m_digital_signature.url)
#                 else:
#                     m_digital_signature = ""

#                 if data[0].m_cancel_bank_cheque_photo:
#                     m_cancel_bank_cheque_photo = str(base_url) + str(data[0].m_cancel_bank_cheque_photo.url)
#                 else:
#                     m_cancel_bank_cheque_photo = ""

#                 if data[0].m_other_document_certificate1:
#                     udyog_adhaar_certificate = str(base_url) + str(data[0].m_other_document_certificate1.url)
#                 else:
#                     udyog_adhaar_certificate = ""

#                 if data[0].address_proof:
#                     address_proof = str(base_url) + str(data[0].address_proof.url)
#                 else:
#                     address_proof = ""

#                 if data[0].m_address_bank_account:
#                     attested_pan_card_legal_entity = str(base_url) + str(data[0].m_address_bank_account.url)
#                 else:
#                     attested_pan_card_legal_entity = ""

#                 if data[0].m_bank_account_entry:
#                     signature_proof_of_autorize_sign = str(base_url) + str(data[0].m_bank_account_entry.url)
#                 else:
#                     signature_proof_of_autorize_sign = ""

#                 if data[0].company_registration_certificate:
#                     company_registration_certificate = str(base_url) + str(data[0].company_registration_certificate.url)
#                 else:
#                     company_registration_certificate = ""

#                 if data[0].schedule_pdf_upload:
#                     schedule_pdf_upload = str(base_url) + str(data[0].schedule_pdf_upload.url)
#                 else:
#                     schedule_pdf_upload = ""

#                 data_dict = {
#                     'm_business_name': data[0].m_business_name,
#                     'm_business_category_id': data[0].m_business_category_id,
#                     'm_business_category_name': data[0].m_business_category.business_category_name,
#                     'm_pin_code': data[0].m_pin_code,
#                     'm_city': data[0].m_city,
#                     'm_area': data[0].m_area,
#                     'm_district': data[0].m_district,
#                     'm_state': data[0].m_state,
#                     'm_address': data[0].m_address,
#                     'm_landline_number': data[0].m_landline_number,
#                     'm_alternate_mobile_number': data[0].m_alternate_mobile_number,
#                     'm_company_email': data[0].m_company_email,
#                     'm_alternate_email': data[0].m_alternate_email,
#                     'm_pan_number': data[0].m_pan_number,
#                     'm_gstin': data[0].m_gstin,
#                     'm_cin': data[0].m_cin,
#                     'm_bank_account_number': data[0].m_bank_account_number,
#                     'm_bank_IFSC_code': data[0].m_bank_IFSC_code,
#                     'm_bank_name': data[0].m_bank_name,
#                     'm_bank_branch': data[0].m_bank_branch,
#                     'm_GSTIN_certificate': m_GSTIN_certificate,
#                     'm_CIN_certificate': m_CIN_certificate,
#                     'm_business_logo': m_business_logo,
#                     'm_business_stamp': m_business_stamp,
#                     'm_digital_signature': m_digital_signature,
#                     'm_website_url': data[0].m_website_url,
#                     'm_business_name_for_billing': data[0].m_business_name_for_billing,
#                     'm_billing_address': data[0].m_billing_address,
#                     'm_billing_email': data[0].m_billing_email,
#                     'm_billing_phone': data[0].m_billing_phone,
#                     'm_vat_tin_number': data[0].m_vat_tin_number,
#                     'm_aadhaar_number': data[0].m_aadhaar_number,
#                     'Entity_Account_m': data[0].Entity_Account_m,
#                     'Entity_Bank_Account_m': data[0].Entity_Bank_Account_m,
#                     'first_name': merchant_object.first_name,
#                     'last_name': merchant_object.last_name,
#                     'm_cancel_bank_cheque_photo': m_cancel_bank_cheque_photo,
#                     'udyog_adhaar_certificate': udyog_adhaar_certificate,
#                     'address_proof': address_proof,
#                     'attested_pan_card_legal_entity': attested_pan_card_legal_entity,
#                     'signature_proof_of_autorize_sign': signature_proof_of_autorize_sign,
#                     'company_registration_certificate': company_registration_certificate,
#                     'schedule_pdf_upload': schedule_pdf_upload,
#                 }
                
#                 return JsonResponse({'status': "success", 'data': data_dict}, status=200)
#             else:
#                 return JsonResponse({'status': "error", 'message': "Data not found."}, status=400)
#         else:
#             return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)

# class RemoveDigitalSignature(generics.GenericAPIView):
#     serializer_class = merchantSerializer
#     queryset = GreenBillUser.objects.all()

#     lookup_field = 'id'

#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         if request.method == "POST":

#             m_business_id = request.POST['m_business_id']

#             signature = ''

#             result = MerchantProfile.objects.filter(id = m_business_id).update(m_digital_signature = signature)

#             if result:
#                 return JsonResponse({'status': "success", 'message': "Digital Signature Removed Successfully."}, status=200)
#             else:
#                 return JsonResponse({'status': "error", 'message': "Something went wrong."}, status=400)

# class RemoveBusinessLogo(generics.GenericAPIView):
#     serializer_class = merchantSerializer
#     queryset = GreenBillUser.objects.all()

#     lookup_field = 'id'

#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         if request.method == "POST":

#             m_business_id = request.POST['m_business_id']

#             logo = ''

#             result = MerchantProfile.objects.filter(id = m_business_id).update(m_business_logo = logo)

#             if result:
#                 return JsonResponse({'status': "success", 'message': "Business Logo Removed Successfully."}, status=200)
#             else:
#                 return JsonResponse({'status': "error", 'message': "Something went wrong."}, status=400)

# class setMerchantGeneralSetting(generics.GenericAPIView):
#     serializer_class = merchantSerializer
#     queryset = GreenBillUser.objects.all()

#     lookup_field = 'id'

#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         if request.method == "POST":

#             # user_id = request.POST['user_id']

#             m_business_id = request.POST['m_business_id']

#             merchant_user_id = MerchantProfile.objects.filter(id = m_business_id)

#             m_business_name = request.POST['m_business_name']
#             m_business_category_id= request.POST['m_business_category_id']
#             m_pin_code= request.POST['m_pin_code']
#             m_city= request.POST['m_city']
#             m_area= request.POST['m_area']
#             m_district= request.POST['m_district']
#             m_state= request.POST['m_state']
#             m_address= request.POST['m_address']
#             m_landline_number= request.POST['m_landline_number']
#             m_alternate_mobile_number= request.POST['m_alternate_mobile_number']
#             m_company_email= request.POST['m_company_email']
#             m_alternate_email= request.POST['m_alternate_email']
#             m_pan_number= request.POST['m_pan_number']
#             m_gstin= request.POST['m_gstin']
#             m_cin= request.POST['m_cin']
#             m_bank_account_number= request.POST['m_bank_account_number']
#             m_bank_IFSC_code= request.POST['m_bank_IFSC_code']
#             m_bank_name= request.POST['m_bank_name']
#             m_bank_branch= request.POST['m_bank_branch']
#             m_GSTIN_certificate= request.FILES.get('m_GSTIN_certificate', "")
#             m_CIN_certificate= request.FILES.get('m_CIN_certificate', "")
#             m_business_logo= request.FILES.get('m_business_logo', "")
#             m_business_stamp= request.FILES.get('m_business_stamp', "")
#             m_digital_signature= request.FILES.get('m_digital_signature', "")
#             # cancel_bank_cheque_photo = request.FILES.get("cancel_bank_cheque_photo", "")

#             m_website_url = request.POST['m_website_url']
#             m_business_name_for_billing = request.POST['m_business_name_for_billing']
#             m_billing_address = request.POST['m_billing_address']
#             m_billing_email = request.POST['m_billing_email']
#             m_billing_phone = request.POST['m_billing_phone']

#             m_vat_tin_number = request.POST['m_vat_tin_number']
#             Entity_Bank_Account_m = request.POST['Entity_Bank_Account_m']
#             Entity_Account_m = request.POST['Entity_Account_m']
#             m_aadhaar_number = request.POST['m_aadhaar_number']

#             first_name = request.POST['first_name']
#             last_name = request.POST['last_name']

#             GreenBillUser.objects.filter(mobile_no = merchant_user_id[0].m_user).update(first_name = first_name, last_name = last_name)
            
#             data = MerchantProfile.objects.filter(id = m_business_id)

#             result = MerchantProfile.objects.filter(id=data[0].id).update(m_aadhaar_number = m_aadhaar_number, Entity_Account_m = Entity_Account_m, Entity_Bank_Account_m = Entity_Bank_Account_m, m_vat_tin_number = m_vat_tin_number, m_billing_phone = m_billing_phone, m_billing_email = m_billing_email, m_billing_address= m_billing_address, m_website_url = m_website_url, m_business_name_for_billing = m_business_name_for_billing, m_business_name= m_business_name, m_business_category_id= m_business_category_id, m_pin_code= m_pin_code, m_city= m_city, m_area=m_area, m_district=m_district, m_state=m_state, m_address=m_address, m_landline_number=m_landline_number, m_alternate_mobile_number= m_alternate_mobile_number, m_company_email=m_company_email, m_alternate_email=m_alternate_email, m_pan_number= m_pan_number, m_gstin=m_gstin, m_cin=m_cin, m_bank_account_number=m_bank_account_number, m_bank_IFSC_code=m_bank_IFSC_code, m_bank_name=m_bank_name, m_bank_branch=m_bank_branch)

#             if m_GSTIN_certificate:
#                 MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_GSTIN_certificate" : m_GSTIN_certificate })

#             if m_CIN_certificate:
#                 MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_CIN_certificate" : m_CIN_certificate })
            
#             if m_business_logo:
#                 MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_business_logo" : m_business_logo })

#             if m_business_stamp:
#                 MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_business_stamp" : m_business_stamp })

#             if m_digital_signature:
#                 MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_digital_signature" : m_digital_signature })

#             # if cancel_bank_cheque_photo:
#             #     MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_cancel_bank_cheque_photo" : cancel_bank_cheque_photo })


#             if result:
#                 return JsonResponse({'status': "success", 'message': "Business settings saved successfully."}, status=200)
#             else:
#                 return JsonResponse({'status': "error", 'message': "Unable to upload the data."}, status=400)
#         else:
#             return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)


# class MerchantUploadCancelCheck(generics.GenericAPIView):
#     serializer_class = merchantSerializer
#     queryset = GreenBillUser.objects.all()

#     lookup_field = 'id'

#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         if request.method == "POST":
#             m_business_id = request.POST.get('m_business_id')
#             cancel_bank_cheque_photo = request.FILES.get("cancel_bank_cheque_photo", "")

#             m_GSTIN_certificate = request.FILES.get("m_gstin_certificate")

#             m_CIN_certificate = request.FILES.get("m_CIN_certificate")

#             m_other_document_certificate1 = request.FILES.get("udyog_adhaar_certificate")

#             address_proof = request.FILES.get("address_proof")

#             m_address_bank_account = request.FILES.get("pan_card_legal_entity")

#             m_bank_account_entry = request.FILES.get("proof_of_authourize_signature")

#             company_registration_certificate = request.FILES.get("m_company_registration_certificate")

#             schedule_pdf_upload = request.FILES.get("m_schedule_pdf_upload")

#             m_digital_signature = request.FILES.get("m_digital_signature")

#             m_business_logo = request.FILES.get("m_business_logo")

#             data = MerchantProfile.objects.filter(id = m_business_id)

#             if cancel_bank_cheque_photo:
#                 result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_cancel_bank_cheque_photo" : cancel_bank_cheque_photo })

#             elif m_GSTIN_certificate:
#                 result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_GSTIN_certificate" : m_GSTIN_certificate })

#             elif m_CIN_certificate:
#                 result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_CIN_certificate" : m_CIN_certificate })

#             elif m_other_document_certificate1:
#                 result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_other_document_certificate1" : m_other_document_certificate1 })

#             elif address_proof:
#                 result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "address_proof" : address_proof })

#             elif m_address_bank_account:
#                 result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_address_bank_account" : m_address_bank_account })

#             elif m_bank_account_entry:
#                 result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_bank_account_entry" : m_bank_account_entry })

#             elif company_registration_certificate:
#                 result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "company_registration_certificate" : company_registration_certificate })

#             elif schedule_pdf_upload:
#                 result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "schedule_pdf_upload" : schedule_pdf_upload })

#             elif m_business_logo:
#                 result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_business_logo" : m_business_logo })

#             elif m_digital_signature:
#                 result = MerchantProfile.objects.update_or_create(id = data[0].id, defaults={ "m_digital_signature" : m_digital_signature })

#             if result:
#                 return JsonResponse({'status': "success", 'message': "General setting data uploaded successfully."}, status=200)
#             else:
#                 return JsonResponse({'status': "error", 'message': "Unable to upload the data."}, status=400)
#         else:
#             return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)



# class getMerchantBusinesses(generics.GenericAPIView):
#     serializer_class = merchantBusinessSerializer
#     queryset = GreenBillUser.objects.all()

#     lookup_field = 'id'

#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
        
#         user_id = request.POST['user_id']

#         merchant_user = Merchant_users.objects.get(user_id = user_id)

#         if user_id:
#             merchantBusiness = MerchantProfile.objects.filter(m_user = merchant_user.merchant_user_id)

#             serializers = merchantBusinessSerializer(merchantBusiness, many=True)

#             return JsonResponse(serializers.data, status=200, safe=False)
#         else:
#             return JsonResponse(serializers.errors, status=400)
            
        

# # @csrf_exempt
# # def getMerchantDetails(request):
# #     queryset = GreenBillUser.objects.all()

# #     if request.method == "POST":
# #         mobile_no = request.POST['mobile_no']
# #         if GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']:
# #             user = GreenBillUser.objects.get(mobile_no=mobile_no)
# #             serializer = merchantSerializer(user)

# #             base_url = "http://157.230.228.250"

# #             try:
# #                 profile_image = UserProfileImage.objects.get(user_id=user.id)
# #                 if profile_image.m_profile_image:
# #                     image_url = str(base_url) + str(profile_image.m_profile_image.url)
# #             except:
# #                 image_url = str(base_url) + str("/media/user-profile-pic.png")

# #             return JsonResponse({'status': "success", 'profile_data': serializer.data, 'image_data': image_url}, status=200)
# #         else:
# #             return JsonResponse({'status': "error", 'message': "user not exists"}, status=400)
# #     else:
# #         return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)

# # @csrf_exempt
# # def get_token_key(request):
# #     if request.method == "POST":
# #         user_id = request.POST['user_id']
# #         try:
# #             token = Token.objects.get(user_id=user_id)
# #             return JsonResponse({'status': "success", 'token_key': token.key}, status=200)
# #         except:
# #             return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)
# #     else:
# #         return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)

# class addDMenquiry(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
          
#         user_id = request.POST['user_id']

#         user_object = GreenBillUser.objects.get(id = user_id)
#         name = request.POST['name']
#         bissiness_name = request.POST['bissiness_name']
#         contact_no = request.POST['contact_no']
#         email_id =  request.POST['email_id']
#         intrested_in = request.POST['intrested_in']
#         comments = request.POST['comments']

#         result = MerchantEnquiryModel.objects.create(
#                 mer_id = user_object,
#                 customer_name = name,
#                 bissiness_name = bissiness_name,
#                 contact_no = contact_no,
#                 email_id = email_id,
#                 intrested_in = intrested_in,
#                 comments = comments,
#                 enquary_status = "Active",
#             )

#         if result:
#             return JsonResponse({'status': "success", "message":"Enquiry added Successfully"}, status=200)
#         else:
#             return JsonResponse({'status': "error", 'message': "Failed to add Enquiry"}, status=400)

# class getCustomerInfo(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         user_id = request.POST.get('user_id')

#         user_profile_object = Merchant_users.objects.get(user_id = user_id)

#         merchant_object = GreenBillUser.objects.get(id = user_profile_object.merchant_user_id.id)

#         merchant_business_id = request.POST['merchant_business_id']

#         merchant_business_object = MerchantProfile.objects.get(id = merchant_business_id)

#         customer_bill_list = CustomerBill.objects.filter(business_name=merchant_business_object,customer_added = False).order_by('-id')
#         parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False).order_by('-id')
#         petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id).order_by('-id')
#         merchant_bill_list = MerchantBill.objects.filter(business_name = merchant_business_object, customer_added = False).order_by('-id').distinct()
#         merchant_added_customer_list = Customer_Info_Model.objects.filter(mer_id = merchant_object,merchant_business_id=merchant_business_object).order_by('-id')


#         customer_info_data = []

#         for customer in merchant_added_customer_list:
#             customer_info_data.append({
#                 "mobile_no" : customer.cust_mobile_num,
#                 "name" : customer.cust_first_name + ' ' + customer.cust_last_lname,
#                 "email" : customer.cust_email,
#                 "state" : "",
#                 "city": customer.customer_area,
#                 "date": timezone.localtime(customer.date_joined).strftime("%Y-%m-%d"),
#             })

#         for bill in parking_bill_list:
#             try:
#                 user = GreenBillUser.objects.get(mobile_no = bill.mobile_no, is_customer = True)
#                 date = timezone.localtime(user.date_joined).strftime("%Y-%m-%d")

#                 count = count + 1
#                 name = user.first_name + ' ' + user.last_name
#                 email = user.email
#                 state = user.c_state 
#                 city = user.c_city
#                 customer_info_data.append({
#                 'mobile_no':mobile_no,
#                 'name': name,
#                 'email':email,
#                 'state':state,
#                 'city':city,
#                 'date': datetime.strptime(str(user.date_joined), '%Y-%m-%d').strftime('%Y-%m-%d'),
#                 })
#             except:
#                 customer_info_data.append({
#                     'mobile_no': bill.mobile_no,
#                     'name': '',
#                     'email':'',
#                     'state':'',
#                     'city':'',
#                     'date': timezone.localtime(bill.created_at).strftime("%Y-%m-%d"),
#                 });


#         for bill in petrol_bill_list:

#             try:
#                 user = GreenBillUser.objects.get(mobile_no = bill.mobile_no, is_customer = True)
#                 date = timezone.localtime(user.date_joined).strftime("%Y-%m-%d")
#                 count = count + 1
#                 name = user.first_name + ' ' + user.last_name
#                 email = user.email
#                 state = user.c_state 
#                 city = user.c_city
#                 customer_info_data.append({
#                 'mobile_no':mobile_no,
#                 'name': name,
#                 'email':email,
#                 'state':state,
#                 'city':city,
#                 'date': date,
#                 })
#             except:
#                 customer_info_data.append({
#                     'mobile_no': bill.mobile_no,
#                     'name': '',
#                     'email':'',
#                     'state':'',
#                     'city':'',
#                     'date': timezone.localtime(bill.created_at).strftime("%Y-%m-%d"),
#                 });

#         for bill in customer_bill_list:

#             try:
#                 user = GreenBillUser.objects.get(mobile_no = bill.mobile_no, is_customer = True)
#                 date = timezone.localtime(user.date_joined).strftime("%Y-%m-%d")
#                 count = count + 1
#                 name = user.first_name + ' ' + user.last_name
#                 email = user.email
#                 state = user.c_state 
#                 city = user.c_city
#                 customer_info_data.append({
#                 'mobile_no':mobile_no,
#                 'name': name,
#                 'email':email,
#                 'state':state,
#                 'city':city,
#                 'date': date,
#                 })
#             except:
#                 customer_info_data.append({
#                     'mobile_no': bill.mobile_no,
#                     'name': '',
#                     'email':'',
#                     'state':'',
#                     'city':'',
#                     'date': timezone.localtime(bill.created_at).strftime("%Y-%m-%d"),
#                 });


#         for bill in merchant_bill_list:
#             try:
#                 user = GreenBillUser.objects.get(mobile_no = bill.mobile_no, is_customer = True)
#                 date = timezone.localtime(user.date_joined).strftime("%Y-%m-%d")
#                 count = count + 1
#                 name = user.first_name + ' ' + user.last_name
#                 email = user.email
#                 state = user.c_state 
#                 city = user.c_city
#                 customer_info_data.append({
#                 'mobile_no':mobile_no,
#                 'name': name,
#                 'email':email,
#                 'state':state,
#                 'city':city,
#                 'date': date,
#                 })
#             except:
#                 customer_info_data.append({
#                     'mobile_no': bill.mobile_no,
#                     'name': '',
#                     'email':'',
#                     'state':'',
#                     'city':'',
#                     'date': timezone.localtime(bill.created_at).strftime("%Y-%m-%d"),
#                 });

#         customer_info_data1 = []
#         customer_info_data2 = []
#         new_data = []
#         filtered_list = []
#         filtered_list2 = []
#         customer_receipt = CustomerReceiptDetailsModels.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_object).order_by('-id')

#         for user in customer_receipt:
#             try:
#                 customer_info_data2.append({
#                     'mobile_no': user.mobile_number,
#                     'name': user.cash_received_from,
#                     'email':'',
#                     'state':'',
#                     'city':'',
#                     'date': datetime.strptime(str(user.date), '%Y-%m-%d').strftime('%Y-%m-%d'),
#                     })
#             except:
#                 customer_info_data2.append({
#                     'mobile_no': user.mobile_number,
#                     'name': '',
#                     'email':'',
#                     'state':'',
#                     'city':'',
#                     'date': '',
#                     })

#         for x in customer_info_data2:
#             if x['mobile_no'] not in filtered_list:
#                 if x['mobile_no'] != '':
#                     filtered_list.append(x['mobile_no'])

#                     customer_info_data.append({
#                         'mobile_no': x['mobile_no'],
#                         'name': x['name'],
#                         'email':'',
#                         'state':'',
#                         'city':'',
#                         'date': x['date'],
#                         })

#         customer_cash_memo = CustomerCashMemoDetailModels.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_object).order_by('-id')

#         for user in customer_cash_memo:
#             try:
#                 customer_info_data1.append({
#                     'mobile_no': user.mobile_number,
#                     'name': user.name,
#                     'email':'',
#                     'state':'',
#                     'city':'',
#                     'date': datetime.strptime(str(user.date), '%Y-%m-%d').strftime('%Y-%m-%d'),
#                     })
#             except:
#                 customer_info_data1.append({
#                     'mobile_no': user.mobile_number,
#                     'name': '',
#                     'email':'',
#                     'state':'',
#                     'city':'',
#                     'date': '',
#                     })

#         for x in customer_info_data1:
#             if x['mobile_no'] not in filtered_list:
#                 if x['mobile_no'] != '':
#                     filtered_list.append(x['mobile_no'])

#                     customer_info_data.append({
#                         'mobile_no': x['mobile_no'],
#                         'name': x['name'],
#                         'email':'',
#                         'state':'',
#                         'city':'',
#                         'date': x['date'],
#                         })


#         for unique in customer_info_data:
#             if unique['mobile_no'] not in filtered_list2:
#                 filtered_list2.append(unique['mobile_no'])
#                 new_data.append({
#                     "mobile_no" : unique['mobile_no'],
#                     "name" : unique['name'],
#                     "email" : unique['email'],
#                     "state" : unique['state'],
#                     "city": unique['city'],
#                     "date": unique['date'],
#                 })

#         # for bills in customer_bill_list:
#         #     if bills.mobile_no not in mobile_no_list and bills.bill_amount not in mobile_no_list:
#         #         mobile_no_list.append({
#         #             'mobile_no': bills.mobile_no,
#         #             'amount': bills.bill_amount
#         #             })
#         #     else:
#         #         pass

            
#         # for bills in customer_bill_list:
#         #     if bills.mobile_no in mobile_no_list:
#         #         continue
#         #     else:
#         #         mobile_no_list.append(bills.mobile_no)

#         # for bills in parking_bill_list:
#         #     if bills.mobile_no in mobile_no_list:
#         #         continue
#         #     else:
#         #         mobile_no_list.append(bills.mobile_no)

#         # for bills in petrol_bill_list:
#         #     if bills.mobile_no in mobile_no_list:
#         #         continue
#         #     else:
#         #         mobile_no_list.append(bills.mobile_no)

#         # for merchant_bill in merchant_bill_list:
#         #     if merchant_bill.mobile_no in mobile_no_list:
#         #         continue
#         #     else:
#         #        mobile_no_list.append(merchant_bill.mobile_no)


#         # data = []

#         # for mobile_no in mobile_no_list:

#         #     try:
#         #         user = GreenBillUser.objects.get(mobile_no = mobile_no)
#         #         name = user.first_name + ' ' + user.last_name
#         #         email = user.email
#         #         state = user.c_state 
#         #         city = user.c_city
#         #     except:
#         #         name = ""
#         #         email = ""
#         #         state = ""
#         #         city = ""

#         #     data.append({
#         #         'mobile_no':mobile_no,
#         #         'name': name if name else "",
#         #         'email':email if email else "",
#         #         'state':state if state else "",
#         #         'city':city if city else "",
#         #     })

#         new_data.sort(key = lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse = True)

#         if new_data:
#             return JsonResponse({'status': "success", "data":new_data}, status=200)
#         else:
#             return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)


# class getCashMemoByMobileNo(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         user_id = request.POST['user_id']

#         mobile_no = request.POST['mobile_no']

#         user_profile_object = Merchant_users.objects.get(user_id = user_id)

#         merchant_object = GreenBillUser.objects.get(id = user_profile_object.merchant_user_id.id)

#         merchant_business_id = request.POST['merchant_business_id']

#         merchant_business_object = MerchantProfile.objects.get(id = merchant_business_id)

#         cash_memo = CustomerCashMemoDetailModels.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_object, mobile_number = mobile_no).order_by('-id')

#         cash_memo1 = CustomerCashMemoDetailModels.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_object, mobile_number = mobile_no).last()

#         all_bill = []


#         if cash_memo1:

#             personal_details = {
#                 'mobile_no' : cash_memo1.mobile_number,
#                 'name' : cash_memo1.name,
#             }

#         else: 
#             personal_details = {
#                 'mobile_no' : mobile_no,
#                 'name' : '',
#             }            

#         base_url = "http://157.230.228.250/"


#         for bill in cash_memo:
#             all_bill.append({

#                 'id': bill.id,
#                 'date': datetime.strptime(str(bill.date), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'memo_no': bill.memo_no,
#                 'amount': str(bill.total),
#                 'memo_url' : str(base_url) + 'cash-memo/' + str(bill.memo_url) + "/"
#             })

#         if cash_memo:
#             return JsonResponse({'status': 'success', 'data' : all_bill, 'personal_details' : personal_details}, status=200)
#         else:
#             return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)



# class getReceiptByMobileNo(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         user_id = request.POST['user_id']

#         mobile_no = request.POST['mobile_no']

#         user_profile_object = Merchant_users.objects.get(user_id = user_id)

#         merchant_object = GreenBillUser.objects.get(id = user_profile_object.merchant_user_id.id)

#         merchant_business_id = request.POST['merchant_business_id']

#         merchant_business_object = MerchantProfile.objects.get(id = merchant_business_id)

#         receipt = CustomerReceiptDetailsModels.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_object, mobile_number = mobile_no).order_by('-id')

#         receipt1 = CustomerReceiptDetailsModels.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_object, mobile_number = mobile_no).last()

#         all_bill = []
#         if receipt1:

#             personal_details = {
#                 'mobile_no' : receipt1.mobile_number,
#                 'name' : receipt1.cash_received_from,
#             }

#         else: 
#             personal_details = {
#                 'mobile_no' : mobile_no,
#                 'name' : '',
#             }

#         base_url = "http://157.230.228.250/"

#         for bill in receipt:
#             all_bill.append({
#                 'id': bill.id,
#                 'date': datetime.strptime(str(bill.date), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'receipt_no': bill.receipt_no,
#                 'amount': str(bill.total),
#                 'receipt_url' : str(base_url) + 'receipt/' + str(bill.receipt_url) + "/"
#             })

#         if receipt:
#             return JsonResponse({'status': 'success', 'data' : all_bill, 'personal_details' : personal_details}, status=200)
#         else:
#             return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)



# class getBillsByMobileNo(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         user_id = request.POST['user_id']

#         mobile_no = request.POST['mobile_no']

#         # merchant_business_id = request.POST['merchant_business_id']

#         # user_profile_object = Merchant_users.objects.get(user_id = user_id)

#         # merchant_object = GreenBillUser.objects.get(id = user_profile_object.merchant_user_id.id)

#         # merchant_business_object = MerchantProfile.objects.get(id = merchant_business_id)

#         # customer_bill_list = CustomerBill.objects.filter(business_name=merchant_business_object)

#         data = []

#         base_url = "http://157.230.228.250/"

#         try:
#             customer_object = GreenBillUser.objects.get(mobile_no = mobile_no)

#             personal_details = {
#                     'mobile_no' : customer_object.mobile_no,
#                     'first_name' : customer_object.first_name,
#                     'last_name' : customer_object.last_name,
#                     'email': customer_object.email,
#                     'c_gender': customer_object.c_gender,
#                     'c_dob': datetime.strptime(str(customer_object.c_dob), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                     'c_area': customer_object.c_area,
#                     'c_pincode': customer_object.c_pincode
#             }

#         except:

#             try:

#                 customer_object = Customer_Info_Model.objects.get(cust_mobile_num = mobile_no)

#                 personal_details = {
#                         'mobile_no' : customer_object.cust_mobile_num,
#                         'first_name' : customer_object.cust_first_name,
#                         'last_name' : customer_object.cust_last_lname,
#                         'email': customer_object.cust_email,
#                         'c_gender': customer_object.c_gender,
#                         'c_dob': datetime.strptime(str(customer_object.date_of_birth), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                         'cust_profile': customer_object.cust_profile,
#                         'c_area': customer_object.customer_area,
#                         'c_pincode': customer_object.customer_pin_code
#                 }

#             except:

#                 personal_details = {
#                     'mobile_no' : mobile_no,
#                     'first_name' : '',
#                     'last_name' : '',
#                     'email': '',
#                     'c_gender': '',
#                     'c_dob': '',
#                     'c_profile': '',
#                     'c_area': '',
#                     'c_pincode': ''
#                 }


#         # customer_bill_list = CustomerBill.objects.filter(business_name=merchant_business_object)
#         customer_bill_list = CustomerBill.objects.filter(mobile_no=mobile_no)

#         for bill in customer_bill_list:
#             # if mobile_no == bill.mobile_no:
#             try:
#                 bill_file = str(base_url) + str(bill.bill.url)
#                 if bill.customer_added == True:
#                     new_bill_url = str(base_url) + 'self-added-bill/' + str(bill.bill_url) + "/"
#                 else:
#                     new_bill_url = str(base_url) + 'my-bill/' + str(bill.bill_url) + "/"
#             except:
#                 bill_file = ""
#             data.append({
#                 'bill_id': bill.id,
#                 'mobile_no': mobile_no,
#                 'amount': str(bill.bill_amount),
#                 'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'bill_file': bill_file,
#                 'db_table': "CustomerBill",
#                 'customer_added': bill.customer_added,
#                 'new_bill_url' : new_bill_url
#             })
                

#         # parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id)
#         parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no=mobile_no)
#         for bill in parking_bill_list:
#             # if mobile_no == bill.mobile_no:
#             try:
#                 bill_file = str(base_url) + str(bill.bill_file.url)
#                 new_bill_url = str(base_url) + 'parking-lot-bill/' + str(bill.bill_url) + "/"
#             except:
#                 bill_file = ""
#             data.append({
#                 'bill_id': bill.id,
#                 'mobile_no': mobile_no,
#                 'amount': str(bill.amount),
#                 'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
#                 'bill_file': bill_file,
#                 'db_table': "SaveParkingLotBill",
#                 'customer_added': False,
#                 'new_bill_url': new_bill_url,
#             })
               

#         # petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id)
#         petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no=mobile_no)
#         for bill in petrol_bill_list:
#             # if mobile_no == bill.mobile_no:
#             try:
#                 bill_file = str(base_url) + str(bill.bill_file.url)
#                 new_bill_url = str(base_url) + 'petrol-pump-bill/' + str(bill.bill_url) + "/"
#             except:
#                 bill_file = ""
#             data.append({
#                 'bill_id': bill.id,
#                 'mobile_no': mobile_no,
#                 'amount': str(bill.total_amount),
#                 'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
#                 'bill_file': bill_file,
#                 'db_table': "SavePetrolPumpBill",
#                 'customer_added': False,
#                 'new_bill_url': new_bill_url
#             })

#         # sorted_data = sorted(data, key=data.bill_date)

#         data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

#         if data:
#             return JsonResponse({'status': "success", "personal_details": personal_details, "all_bills":data}, status=200)
#         else:
#             return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)


# class customerInfoSendSms(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         bill_id = request.POST['bill_id']
#         mobile_no = request.POST['mobile_no']
#         db_table = request.POST['db_table']

#         if mobile_no:
#             if db_table == "CustomerBill":
#                 bill_object = CustomerBill.objects.get(id = bill_id)
#                 business_id = bill_object.business_name.id
#                 customer_bill_url = "http://157.230.228.250/my-bill/" + str(bill_object.bill_url) + "/"

#             if db_table == "MerchantBill":
#                 bill_object = MerchantBill.objects.get(id = bill_id)
#                 business_id = bill_object.business_name.id
#                 customer_bill_url = "http://157.230.228.250/my-bill-merchant/" + str(bill_object.bill_url) + "/"

#             elif db_table == "SaveParkingLotBill":
#                 bill_object = SaveParkingLotBill.objects.get(id = bill_id)
#                 business_id = bill_object.m_business_id
#                 customer_bill_url = "http://157.230.228.250/parking-lot-bill/" + str(bill_object.bill_url) + "/"

#             elif db_table == "SavePetrolPumpBill":
#                 bill_object = SavePetrolPumpBill.objects.get(id = bill_id)
#                 business_id = bill_object.m_business_id
#                 customer_bill_url = "http://157.230.228.250/petrol-pump-bill/" + str(bill_object.bill_url) + "/"

#             subscription_object = getActiveSubscriptionPlan(request, business_id) 

#             if subscription_object:

#                 if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

#                     s = pyshorteners.Shortener()
#                     short_url = s.tinyurl.short(customer_bill_url)

#                     if db_table == "CustomerBill" or db_table == "MerchantBill":

#                         ts = int(time.time())
#                         data_temp = {
#                                 "keyword":"Bill Delivery SMS",
#                                 "timeStamp":ts,
#                                 "dataSet":
#                                     [
#                                         {
#                                             "UNIQUE_ID":"GB-" + str(ts),
#                                             "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
#                                             "OA":"GBBILL",
#                                             "MSISDN": mobile_no, # Recipient's Mobile Number
#                                             "CHANNEL":"SMS",
#                                             "CAMPAIGN_NAME":"hind_user",
#                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                             "USER_NAME":"hind_hsi",
#                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                             "DLT_CT_ID":"1007161814187973948", # Template Id
#                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                         }
#                                     ]
#                                 }

#                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                         response = requests.post(url, json = data_temp)

#                     elif db_table == "SaveParkingLotBill":

#                         ts = int(time.time())
#                         data_temp = {
#                                 "keyword":"Bill Delivery SMS",
#                                 "timeStamp":ts,
#                                 "dataSet":
#                                     [
#                                         {
#                                             "UNIQUE_ID":"GB-" + str(ts),
#                                             "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
#                                             "OA":"GBPARK",
#                                             "MSISDN": mobile_no, # Recipient's Mobile Number
#                                             "CHANNEL":"SMS",
#                                             "CAMPAIGN_NAME":"hind_user",
#                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                             "USER_NAME":"hind_hsi",
#                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                             "DLT_CT_ID":"1007161814187973948", # Template Id
#                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                         }
#                                     ]
#                                 }

#                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                         response = requests.post(url, json = data_temp)

#                     elif db_table == "SavePetrolPumpBill":

#                         ts = int(time.time())
#                         data_temp = {
#                                 "keyword":"Bill Delivery SMS",
#                                 "timeStamp":ts,
#                                 "dataSet":
#                                     [
#                                         {
#                                             "UNIQUE_ID":"GB-" + str(ts),
#                                             "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
#                                             "OA":"GBPUMP",
#                                             "MSISDN": mobile_no, # Recipient's Mobile Number
#                                             "CHANNEL":"SMS",
#                                             "CAMPAIGN_NAME":"hind_user",
#                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                             "USER_NAME":"hind_hsi",
#                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                             "DLT_CT_ID":"1007161814187973948", # Template Id
#                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                         }
#                                     ]
#                                 }

#                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                         response = requests.post(url, json = data_temp)

#                     if response.status_code == 200:
#                         total_amount_avilable_new = 0
#                         total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
#                         subscription_object.total_amount_avilable = total_amount_avilable_new
#                         subscription_object.save()
#                         return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
#                     else:
#                         return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
#                 else:
#                     return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)
#             else:
#                 return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
#         else:
#             return JsonResponse({'status':'error', 'message': "You don't have active Green Bill Subscription. Please purchase and try again."}, status=400)



# class getBillInfoList(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         merchant_business_id = request.POST['merchant_business_id']

#         from_date = request.POST.get('from_date')
        
#         to_date = request.POST.get('to_date')

#         data = []

#         base_url = "http://157.230.228.250/"

#         parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id).order_by('-id')
#         for bill in parking_bill_list:
#             try:
#                 bill_file = str(base_url) + str(bill.bill_file.url)
#             except:
#                 bill_file = ""

#             if bill.is_checkoutpin == True:
#                 try:
#                     mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
#                 except:
#                     mobile_no = bill.mobile_no
#             else:
#                 mobile_no = bill.mobile_no

#             data.append({
#                 'bill_id': bill.id,
#                 'invoice_no': bill.invoice_no,
#                 'mobile_no': mobile_no,
#                 'amount': str(bill.amount),
#                 'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
#                 'bill_file': bill_file,
#                 'db_table': "SaveParkingLotBill",
#                 'created_at': str(bill.created_at),
#                 'customer_added': False,
#                 'url': str(base_url) + "parking-lot-bill/" + str(bill.bill_url) + "/"
#             })
               

#         petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id).order_by('-id')
#         for bill in petrol_bill_list:
#             try:
#                 bill_file = str(base_url) + str(bill.bill_file.url)
#             except:
#                 bill_file = ""

#             if bill.is_checkoutpin == True:
#                 try:
#                     mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
#                 except:
#                     mobile_no = bill.mobile_no
#             else:
#                 mobile_no = bill.mobile_no

#             data.append({
#                 'bill_id': bill.id,
#                 'invoice_no': bill.invoice_no,
#                 'mobile_no': mobile_no,
#                 'amount': str(bill.total_amount),
#                 'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
#                 'bill_file': bill_file,
#                 'db_table': "SavePetrolPumpBill",
#                 'created_at': str(bill.created_at),
#                 'customer_added': False,
#                 'url': str(base_url) + "petrol-pump-bill/" + str(bill.bill_url) + "/",
#             })

#         merchant_object = MerchantProfile.objects.get(id = merchant_business_id)

#         customer_bill = CustomerBill.objects.filter(business_name = merchant_object, customer_added = False).order_by('-id')

#         for bill in customer_bill:
#             try:
#                 bill_file = str(base_url) + str(bill.bill.url)
#             except:
#                 bill_file = ""

#             if bill.is_checkoutpin == True:
#                 try:
#                     mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
#                 except:
#                     mobile_no = bill.mobile_no
#             else:
#                 mobile_no = bill.mobile_no

#             if bill.customer_added == True:
#                 url = str(base_url) + 'self-added-bill/' + str(bill.bill_url) + "/"
#             else:
#                 url = str(base_url) + 'my-bill/' + str(bill.bill_url) + "/"

#             data.append({
#                 'bill_id': bill.id,
#                 'invoice_no': bill.invoice_no,
#                 'mobile_no': mobile_no,
#                 'amount': str(bill.bill_amount),
#                 'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'bill_file': bill_file,
#                 'db_table': "CustomerBill",
#                 'created_at': str(bill.created_at),
#                 'customer_added': False,
#                 'url':url,
#             })

#         merchant_bill = MerchantBill.objects.filter(business_name = merchant_object)

#         for bill in merchant_bill:
#             try:
#                 bill_file = str(base_url) + str(bill.bill.url)
#             except:
#                 bill_file = ""

#             if bill.is_checkoutpin == True:
#                 try:
#                     mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
#                 except:
#                     mobile_no = bill.mobile_no
#             else:
#                 mobile_no = bill.mobile_no

#             data.append({
#                 'bill_id': bill.id,
#                 'invoice_no': bill.invoice_no,
#                 'mobile_no': mobile_no,
#                 'amount': str(bill.bill_amount),
#                 'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'bill_file': bill_file,
#                 'db_table': "MerchantBill",
#                 'created_at': str(bill.created_at),
#                 'customer_added': False,
#                 'url': str(base_url) + "my-bill-merchant/" + str(bill.bill_url) + "/",
#             })

#         data.sort(key = lambda x: x['created_at'], reverse = True)

#         total_bills_created = 0
#         total_amount_collected = 0
#         total_flag_bills = 0

#         for bill in data:
#             total_bills_created = total_bills_created + 1
#             total_amount_collected = float(total_amount_collected) + float(bill['amount'])

#         new_data = []

#         if from_date and to_date:

#             if data:
#                 if from_date:
#                     from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

#                 if to_date:
#                     to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

#                 for bill in data:
#                     bill_date = datetime.strptime(str(bill['bill_date']), '%d-%m-%Y').strftime('%Y-%m-%d')
#                     if from_date and to_date:
                        
#                         if bill_date >= from_date and bill_date <= to_date:
#                             new_data.append(bill)

#                 new_data.sort(key = lambda x: x['created_at'], reverse = True)

#                 total_bills_created = 0
#                 total_amount_collected = 0
#                 total_flag_bills = 0

#                 for bill in new_data:
#                     total_bills_created = total_bills_created + 1
#                     total_amount_collected = float(total_amount_collected) + float(bill['amount'])

#                 if new_data:
#                     return JsonResponse({'status': "success", "all_bills":new_data, "total_bills_created": total_bills_created,
#                     "total_amount_collected":total_amount_collected, "from_date": from_date, "to_date": to_date}, status=200)
#                 else:
#                     return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)
#         else:

#             if data:
#                 return JsonResponse({'status': "success", "all_bills":data, "total_bills_created": total_bills_created,
#                     "total_amount_collected":total_amount_collected, "from_date": "", "to_date": "" }, status=200)
#             else:
#                 return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)


# class BillInfoSendSms(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         bill_id = request.POST['bill_id']
#         mobile_no = request.POST['mobile_no']
#         db_table = request.POST['db_table']

#         # print(db_table)


#         if mobile_no:
#             if db_table == "CustomerBill":
#                 bill_object = CustomerBill.objects.get(id = bill_id)
#                 business_id = bill_object.business_name.id
#                 customer_bill_url = "http://157.230.228.250/my-bill/" + str(bill_object.bill_url) + "/"

#             if db_table == "MerchantBill":
#                 bill_object = MerchantBill.objects.get(id = bill_id)
#                 business_id = bill_object.business_name.id
#                 customer_bill_url = "http://157.230.228.250/my-bill-merchant/" + str(bill_object.bill_url) + "/"

#             elif db_table == "SaveParkingLotBill":
#                 bill_object = SaveParkingLotBill.objects.get(id = bill_id)
#                 business_id = bill_object.m_business_id
#                 customer_bill_url = "http://157.230.228.250/parking-lot-bill/" + str(bill_object.bill_url) + "/"

#             elif db_table == "SavePetrolPumpBill":
#                 bill_object = SavePetrolPumpBill.objects.get(id = bill_id)
#                 business_id = bill_object.m_business_id
#                 customer_bill_url = "http://157.230.228.250/petrol-pump-bill/" + str(bill_object.bill_url) + "/"

#             subscription_object = getActiveSubscriptionPlan(request, business_id) 

#             device = DeviceId.objects.filter(mobile_no=mobile_no).first()
#             push_service = FCMNotification(api_key=settings.API_KEY)

#             if subscription_object and subscription_object.total_amount_avilable:

#                 if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):
#                     s = pyshorteners.Shortener()
#                     short_url = s.tinyurl.short(customer_bill_url)

#                     if db_table == "CustomerBill" or db_table == "MerchantBill":

#                         if device != None:

#                             try:
#                                 registration_id = device.device_id
#                             except:
#                                 registration_id = ''

#                             message_title = "New Bill"

#                             message_body = "Hey Green Bill user, view and download your bill here. " + str(customer_bill_url)

#                             result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

#                             total_amount_avilable_new = 0
#                             total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_digital_bill_cost)
#                             subscription_object.total_amount_avilable = total_amount_avilable_new
#                             subscription_object.save()

#                             return JsonResponse({'status':'success', 'message': 'Notification send successfully'}, status=200)
#                         else:

#                             ts = int(time.time())
#                             data_temp = {
#                                     "keyword":"Bill Delivery SMS",
#                                     "timeStamp":ts,
#                                     "dataSet":
#                                         [
#                                             {
#                                                 "UNIQUE_ID":"GB-" + str(ts),
#                                                 "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
#                                                 "OA":"GBBILL",
#                                                 "MSISDN": mobile_no, # Recipient's Mobile Number
#                                                 "CHANNEL":"SMS",
#                                                 "CAMPAIGN_NAME":"hind_user",
#                                                 "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                                 "USER_NAME":"hind_hsi",
#                                                 "DLT_TM_ID":"1001096933494158", # TM ID
#                                                 "DLT_CT_ID":"1007161814187973948", # Template Id
#                                                 "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                             }
#                                         ]
#                                     }

#                             url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                             response = requests.post(url, json = data_temp)

#                             if response.status_code == 200:
#                                 total_amount_avilable_new = 0
#                                 total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
#                                 subscription_object.total_amount_avilable = total_amount_avilable_new
#                                 subscription_object.save()
#                                 return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
#                             else:
#                                 return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)


#                     elif db_table == "SaveParkingLotBill":
#                         if device != None:

#                             try:
#                                 registration_id = device.device_id
#                             except:
#                                 registration_id = ''

#                             message_title = "New Bill"

#                             message_body = "Hey Green Bill user, view and download your bill here. " + str(customer_bill_url)

#                             result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

#                             total_amount_avilable_new = 0
#                             total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_digital_bill_cost)
#                             subscription_object.total_amount_avilable = total_amount_avilable_new
#                             subscription_object.save()

#                             return JsonResponse({'status':'success', 'message': 'Notification send successfully'}, status=200)
#                         else:

#                             ts = int(time.time())
#                             data_temp = {
#                                     "keyword":"Bill Delivery SMS",
#                                     "timeStamp":ts,
#                                     "dataSet":
#                                         [
#                                             {
#                                                 "UNIQUE_ID":"GB-" + str(ts),
#                                                 "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
#                                                 "OA":"GBPARK",
#                                                 "MSISDN": mobile_no, # Recipient's Mobile Number
#                                                 "CHANNEL":"SMS",
#                                                 "CAMPAIGN_NAME":"hind_user",
#                                                 "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                                 "USER_NAME":"hind_hsi",
#                                                 "DLT_TM_ID":"1001096933494158", # TM ID
#                                                 "DLT_CT_ID":"1007161814187973948", # Template Id
#                                                 "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                             }
#                                         ]
#                                     }

#                             url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                             response = requests.post(url, json = data_temp)

#                             if response.status_code == 200:
#                                 total_amount_avilable_new = 0
#                                 total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
#                                 subscription_object.total_amount_avilable = total_amount_avilable_new
#                                 subscription_object.save()
#                                 return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
#                             else:
#                                 return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)


#                     elif db_table == "SavePetrolPumpBill":

#                         if device != None:

#                             try:
#                                 registration_id = device.device_id
#                             except:
#                                 registration_id = ''

#                             message_title = "New Bill"

#                             message_body = "Hey Green Bill user, view and download your bill here. " + str(customer_bill_url)

#                             result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

#                             total_amount_avilable_new = 0
#                             total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_digital_bill_cost)
#                             subscription_object.total_amount_avilable = total_amount_avilable_new
#                             subscription_object.save()

#                             return JsonResponse({'status':'success', 'message': 'Notification send successfully'}, status=200)

#                         else:

#                             ts = int(time.time())
#                             data_temp = {
#                                     "keyword":"Bill Delivery SMS",
#                                     "timeStamp":ts,
#                                     "dataSet":
#                                         [
#                                             {
#                                                 "UNIQUE_ID":"GB-" + str(ts),
#                                                 "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
#                                                 "OA":"GBPUMP",
#                                                 "MSISDN": mobile_no, # Recipient's Mobile Number
#                                                 "CHANNEL":"SMS",
#                                                 "CAMPAIGN_NAME":"hind_user",
#                                                 "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                                 "USER_NAME":"hind_hsi",
#                                                 "DLT_TM_ID":"1001096933494158", # TM ID
#                                                 "DLT_CT_ID":"1007161814187973948", # Template Id
#                                                 "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                             }
#                                         ]
#                                     }

#                             url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                             response = requests.post(url, json = data_temp)
         
#                             if response.status_code == 200:
#                                 total_amount_avilable_new = 0
#                                 total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
#                                 subscription_object.total_amount_avilable = total_amount_avilable_new
#                                 subscription_object.save()
#                                 return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
#                             else:
#                                 return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
#                 else:
#                     return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
#             else:
#                 return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
#         else:
#             return JsonResponse({'status':'error', 'message': "You don't have active Green Bill Subscription. Please purchase and try again."}, status=400)


# class getMerchantReferralCode(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         user_id = request.POST['user_id']

#         user_profile_object = Merchant_users.objects.get(user_id = user_id)

#         merchant_object = GreenBillUser.objects.get(id = user_profile_object.merchant_user_id.id)

#         if merchant_object:
#             return JsonResponse({'status':'success', 'message': merchant_object.merchant_referral_code}, status=200)
#         else:
#             return JsonResponse({'status' : 'error', 'message': "Referral Code Not Available"}, status=400)


# class createMerchantUser(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         user_id = request.POST['user_id']

#         user_profile_object = Merchant_users.objects.get(user_id = user_id)

#         merchant_object = GreenBillUser.objects.get(id = user_profile_object.merchant_user_id.id)

#         m_business_id = request.POST['m_business_id']

#         m_business_object = MerchantProfile.objects.get(id = m_business_id)

#         if GreenBillUser.objects.filter(mobile_no = request.POST['mobile_no']).exists():
#             return JsonResponse({'status':'error', 'message': "Mobile number is already used !!!"}, status=400)

#         else:

#             startswith = str(m_business_object.id) + ','
#             endswith = ','+ str(m_business_object.id)
#             contains = ','+ str(m_business_object.id) + ','
#             exact = str(m_business_object.id)

#             try:
#                 check_subscription_available = merchant_subscriptions.objects.get(
#                     Q(merchant_id = merchant_object),
#                     Q(is_active = True),
#                     Q(business_ids__startswith = startswith) | 
#                     Q(business_ids__endswith = endswith) | 
#                     Q(business_ids__contains = contains) | 
#                     Q(business_ids__exact = exact)
#                 )
#             except:
#                 check_subscription_available = ""

#             number_of_users = ''

#             if check_subscription_available:
#                 if check_subscription_available.no_of_users:
#                     number_of_users = check_subscription_available.no_of_users

#             role_name_id = request.POST["role_id"]

#             role1 = "Exe User"

#             merchant_role1 = merchant_userrole.objects.filter(role_id = role_name_id, role__role_name = role1)

#             if merchant_role1:

#                 if number_of_users:
                            
#                     all_merchant_users = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = m_business_object.id)
                
#                     number_of_exe_role = 0
                    
#                     for user in all_merchant_users:
                        
#                         temp1 = GreenBillUser.objects.get(mobile_no=user.user_id)
                        
#                         role_data = merchant_userrole.objects.filter(user = temp1)

#                         for oject1 in role_data:
                            
#                             user.user_id.role = oject1.id
                            
#                             user.user_id.role_name = oject1.role
                            
#                             roles2 = merchant_role.objects.filter(role_name= oject1.role, merchant_business_id = m_business_object)
                            
#                             for oject2 in roles2:
                                
#                                 role_name1 = oject2.role_name
                                
#                                 if role_name1 == 'Exe User':
                                    
#                                     number_of_exe_role = number_of_exe_role + 1

#                     if int(number_of_exe_role + 1) < int(number_of_users):
#                         temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
        
#                         user = GreenBillUser.objects.create_user(
#                             mobile_no = request.POST['mobile_no'],
#                             m_email = request.POST['email'],
#                             first_name = request.POST['first_name'],
#                             last_name = request.POST['last_name'],
#                             password = temp_password,
#                             is_merchant_staff = 1
#                         )

#                         result1 = Merchant_users.objects.create(user_id = user, merchant_user_id = merchant_object, raw_password= temp_password, m_business_id = m_business_object.id, m_business_name= m_business_object.m_business_name)

#                         role_id = request.POST["role_id"]

#                         result2 = merchant_userrole.objects.create(user = user, role_id = role_id)

#                         name = request.POST['first_name']
#                         email = request.POST['email']
#                         mobile_no = request.POST['mobile_no']

#                         ts = int(time.time())

#                         data_temp = {
#                                 "keyword":"ID and Password of users",
#                                 "timeStamp":ts,
#                                 "dataSet":
#                                     [
#                                         {
#                                             "UNIQUE_ID":"GB-" + str(ts),
#                                             "MESSAGE":"Dear Green Bill user, here is the login credentials for your team. Username: " + mobile_no + " Password: "+ temp_password,
#                                             "OA":"GRBILL", 
#                                             "MSISDN": mobile_no, # Recipient's Mobile Number
#                                             "CHANNEL":"SMS",
#                                             "CAMPAIGN_NAME":"hind_user",
#                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                             "USER_NAME":"hind_hsi",
#                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                             "DLT_CT_ID":"1007162098336084141", # Template Id
#                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                         }
#                                     ]
#                                 }

#                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                         response = requests.post(url, json = data_temp)

#                         if user and result1 and result2:
#                             return JsonResponse({'status': 'success', 'message': 'User created successfully !!!'}, status=200)
#                         else:
#                             return JsonResponse({'status': 'success', 'message': 'Failed to create user !!!'}, status=400)
#                     else:
#                         return JsonResponse({'status': 'success', 'message': 'Exe user can created as per your subscription plan !!!'}, status=400)
#                 else:
#                     return JsonResponse({'status': 'success', 'message': 'Exe user can created as per your subscription plan !!!'}, status=400)
#             else:        
#                 temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
                
#                 user = GreenBillUser.objects.create_user(
#                     mobile_no = request.POST['mobile_no'],
#                     m_email = request.POST['email'],
#                     first_name = request.POST['first_name'],
#                     last_name = request.POST['last_name'],
#                     password = temp_password,
#                     is_merchant_staff = 1
#                 )

#                 result1 = Merchant_users.objects.create(user_id = user, merchant_user_id = merchant_object, raw_password= temp_password, m_business_id = m_business_object.id, m_business_name= m_business_object.m_business_name)

#                 role_id = request.POST["role_id"]

#                 result2 = merchant_userrole.objects.create(user = user, role_id = role_id)

#                 name = request.POST['first_name']
#                 email = request.POST['email']
#                 mobile_no = request.POST['mobile_no']

#                 ts = int(time.time())

#                 data_temp = {
#                         "keyword":"ID and Password of users",
#                         "timeStamp":ts,
#                         "dataSet":
#                             [
#                                 {
#                                     "UNIQUE_ID":"GB-" + str(ts),
#                                     "MESSAGE":"Dear Green Bill user, here is the login credentials for your team. Username: " + mobile_no + " Password: "+ temp_password,
#                                     "OA":"GRBILL", 
#                                     "MSISDN": mobile_no, # Recipient's Mobile Number
#                                     "CHANNEL":"SMS",
#                                     "CAMPAIGN_NAME":"hind_user",
#                                     "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                     "USER_NAME":"hind_hsi",
#                                     "DLT_TM_ID":"1001096933494158", # TM ID
#                                     "DLT_CT_ID":"1007162098336084141", # Template Id
#                                     "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                 }
#                             ]
#                         }

#                 url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                 response = requests.post(url, json = data_temp)

#             if user and result1 and result2:
#                 return JsonResponse({'status': 'success', 'message': 'User created successfully !!!'}, status=200)
#             else:
#                 return JsonResponse({'status': 'success', 'message': 'Failed to create user !!!'}, status=400)


# class MerchantUserRole(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_user_id = request.POST['m_user_id']

#         merchant_business_id = request.POST['merchant_business_id']

#         merchant_business_object = MerchantProfile.objects.get(id = merchant_business_id)

#         merchant_object = GreenBillUser.objects.get(id = m_user_id)

#         result = merchant_role.objects.filter(merchant_id = merchant_object, merchant_business_id = merchant_business_object)

#         # print(result)

#         serializer = MerchantUserRoleSerializer(result, many=True)

#         if result:
#             return JsonResponse(serializer.data, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)

# class MerchantUsers(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_user_id = request.POST['m_user_id']

#         m_business_id = request.POST['m_business_id']

#         merchant_object = GreenBillUser.objects.get(id = m_user_id)

#         merchant_business = MerchantProfile.objects.get(id = m_business_id)

#         merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = m_business_id).order_by('-id')

#         merchant_user = []

#         for user in merchant_user_temp:

#             role_temp = merchant_userrole.objects.filter(user = user.user_id)
    
#             try:
#                 role_id = str(role_temp[0].role.id)
#                 role_name = role_temp[0].role.role_name

#             except:
#                 role_id = ""
#                 role_name = ""


#             merchant_user.append({
#                 'id': user.user_id.id,
#                 'name': user.user_id.first_name + " " + user.user_id.last_name,
#                 'mobile_no': user.user_id.mobile_no,
#                 'email': user.user_id.m_email,
#                 'role_id': role_id,
#                 'role_name': role_name
#             })

#         if merchant_user:
#             return JsonResponse({'data':merchant_user}, status=200)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)

# # Dashboard

# class ParkingMerchantDashboardHeaderCalulations(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         parking_bills = SaveParkingLotBill.objects.filter(m_business_id = m_business_id, created_at__date = timezone.now(), is_pass = False).all()

#         total_bills = 0
#         total_collection = float(0)
#         total_flagged = 0

#         for bill in parking_bills:
#             total_bills += 1
#             total_collection = total_collection + float(bill.amount)

#             if bill.bill_flag == True:
#                 total_flagged = total_flagged + 1

#         parking_pass = ParkingLotPass.objects.filter(m_business_id = m_business_id, created_at__date = timezone.now()).all()

#         total_pass_collection = 0
#         total_pass = 0

#         for pass_temp in parking_pass:
#             total_pass_collection = total_pass_collection + float(pass_temp.amount)
#             total_pass = total_pass + 1

#         todays_payments = {
#             'cash': float(total_collection + total_pass_collection),
#             'online': ''
#         }

#         todays_bill = {
#             'total': total_bills,
#             'flagged': total_flagged
#         }

#         space_data = MerchantParkingLotSpace.objects.filter(m_business_id = m_business_id)

#         actual_space_data = []

#         for data_temp in space_data:

#             try:
#                 temp = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True)

#                 vehicle_parked_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__date = timezone.now()).count()

#                 vehicle_exit_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = True, manage_space = True, created_at__date = timezone.now()).count()
                
#                 space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()
                
#             except:
#                 space_avilable_count = 0

#             space_avilable_count_temp = int(data_temp.spaces_count) - int(space_avilable_count)

#             space_used = int(data_temp.spaces_count) - int(space_avilable_count_temp)

#             parking_bills = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__date = timezone.now())

#             total_bills_made = float(0)

#             for bill in parking_bills:
#                 total_bills_made = total_bills_made + float(bill.amount)

#             actual_space_data.append({
#                 "id": data_temp.id,
#                 "vehicle_type": data_temp.vehicle_type,
#                 "space": data_temp.spaces_count,
#                 "available_parking_space": str(space_avilable_count_temp),
#                 "space_used": space_used,
#                 "space_avilable_count": space_avilable_count,
#                 "vehicle_exit_count": vehicle_exit_count,
#                 "vehicle_parked_count": vehicle_parked_count,
#                 "total_bills_made": total_bills_made
#             })

#         space_available = []
#         foorloop_count = 0

#         for space in actual_space_data:
#             if foorloop_count < 3:
#                 space_available.append({
#                     'vehicle_type': space['vehicle_type'],
#                     'available_parking_space': space['available_parking_space'],
#                     'total_space': space['space'],
#                 })
#                 foorloop_count+=1

#         not_exited = []
#         foorloop_count = 0
#         for space in actual_space_data:
#             if foorloop_count < 3:
#                 not_exited.append({
#                     'vehicle_type': space['vehicle_type'],
#                     'space_used': space['space_used']
#                 })
#                 foorloop_count+=1

#         if m_business_id:
#             return JsonResponse({'status':"success", 'todays_payments': todays_payments, 'todays_bill': todays_bill, 'space_available': space_available, 'not_exited': not_exited}, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class ParkingMerchantVehicleTypeWiseCalulationsGraph(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']
#         from_date = request.POST['from_date']
#         to_date = request.POST['to_date']

#         space_data = MerchantParkingLotSpace.objects.filter(m_business_id = m_business_id)
#         if from_date and to_date:
#             DATE_FORMAT = '%Y-%m-%d'

#             date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
#             day_later = date_time_obj + timedelta(days=1)
#             x = day_later.date()
#             ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

#             vehical_start_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
#             start_date = vehical_start_date.split('-')
#             start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
#             sd_filter = start_date.strftime(DATE_FORMAT)

#             actual_space_data = []

#             for data_temp in space_data:

#                 try:
#                     temp = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True)

#                     vehicle_parked_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__range = (sd_filter, ed_filter)).count()

#                     vehicle_exit_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = True, manage_space = True, created_at__range = (sd_filter, ed_filter)).count()
                    
#                     space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()
                    
#                 except:
#                     space_avilable_count = 0

#                 space_avilable_count_temp = int(data_temp.spaces_count) - int(space_avilable_count)

#                 space_used = int(data_temp.spaces_count) - int(space_avilable_count_temp)

#                 parking_bills = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__range = (sd_filter, ed_filter))

#                 total_bills_made = 0

#                 for bill in parking_bills:
#                     total_bills_made = total_bills_made + float(bill.amount)

#                 actual_space_data.append({
#                     "id": data_temp.id,
#                     "vehicle_type": data_temp.vehicle_type,
#                     "space": data_temp.spaces_count,
#                     "available_parking_space": str(space_avilable_count_temp),
#                     "space_used": space_used,
#                     "space_avilable_count": space_avilable_count,
#                     "vehicle_exit_count": vehicle_exit_count,
#                     "vehicle_parked_count": vehicle_parked_count,
#                     "total_bills_made": float(total_bills_made)
#                 })

#             labels = []
#             data = []

#             for space in actual_space_data:
#                 vehicle_type_temp = space["vehicle_type"]
#                 labels.append(vehicle_type_temp)
#                 # data.append(round(space['total_bills_made']))
#                 decimal_value = format(float(space['total_bills_made']), ".2f")
#                 data.append(decimal_value)

#         else: 

#             actual_space_data = []

#             for data_temp in space_data:

#                 try:
#                     temp = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True)

#                     vehicle_parked_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__date = timezone.now()).count()

#                     vehicle_exit_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = True, manage_space = True, created_at__date = timezone.now()).count()
                    
#                     space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()
                    
#                 except:
#                     space_avilable_count = 0

#                 space_avilable_count_temp = int(data_temp.spaces_count) - int(space_avilable_count)

#                 space_used = int(data_temp.spaces_count) - int(space_avilable_count_temp)

#                 parking_bills = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__date = timezone.now())

#                 total_bills_made = 0

#                 for bill in parking_bills:
#                     total_bills_made = total_bills_made + float(bill.amount)

#                 actual_space_data.append({
#                     "id": data_temp.id,
#                     "vehicle_type": data_temp.vehicle_type,
#                     "space": data_temp.spaces_count,
#                     "available_parking_space": str(space_avilable_count_temp),
#                     "space_used": space_used,
#                     "space_avilable_count": space_avilable_count,
#                     "vehicle_exit_count": vehicle_exit_count,
#                     "vehicle_parked_count": vehicle_parked_count,
#                     "total_bills_made": float(total_bills_made)
#                 })

#             labels = []
#             data = []

#             for space in actual_space_data:
#                 vehicle_type_temp = space["vehicle_type"]
#                 labels.append(vehicle_type_temp)
#                 # data.append(round(space['total_bills_made']))
#                 decimal_value = format(float(space['total_bills_made']), ".2f")
#                 data.append(decimal_value)
#                 # data.append(round(space['total_bills_made'],2))
#                 # productWiseBillsdoughnutChart_labels_temp.append(vehicle_type_temp)
#                 # productWiseBillsdoughnutChart_data_temp.append(space['vehicle_parked_count'])

#         if labels and data:
#             return JsonResponse({'status':"success", 'labels': labels, 'data': data}, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)

# class ViewRatingAnalysisGraph(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         merchant_business_id = MerchantProfile.objects.get(id = m_business_id)

#         ratings = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id).order_by('-id')

#         feedback_count = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id).count()

#         star1 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 1).count()
#         star2 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 2).count()
#         star3 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 3).count()
#         star4 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 4).count()
#         star5 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 5).count()
#         total_rating = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id)

#         total_feedback_count = 0

#         for obj in total_rating:
#             if obj.rating:
#                 total_feedback_count = total_feedback_count + 1

#         average_rating = ((star5 * 5) + (star4 * 4) + (star3 * 3) + (star2 * 2) + (star1 * 1))/(total_feedback_count)


#         rating1 = 0
#         rating2 = 0
#         rating3 = 0
#         rating4 = 0
#         rating5 = 0

#         data = []

#         for obj1 in ratings:
#             if obj1.rating:
#                 if obj1.rating == '1':
#                     rating1 = rating1 + 1
#                 if obj1.rating == '2':
#                     rating2 = rating2 + 1
#                 if obj1.rating == '3':
#                     rating3 = rating3 + 1
#                 if obj1.rating == '4':
#                     rating4 = rating4 + 1
#                 if obj1.rating == '5':
#                     rating5 = rating5 + 1

#         data.append(rating1)
#         data.append(rating2)
#         data.append(rating3)
#         data.append(rating4)
#         data.append(rating5)

#         rating_percentage = []
#         star1percentage = 0
#         star2percentage = 0
#         star3percentage = 0
#         star4percentage = 0
#         star5percentage = 0
#         if feedback_count:
#             star1percentage = (rating1/feedback_count)*100
#             rating_percentage.append("%.2f" % round(star1percentage, 2))
        
#             star2percentage = (rating2/feedback_count)*100
#             rating_percentage.append("%.2f" % round(star2percentage, 2))
        
#             star3percentage = (rating3/feedback_count)*100
#             rating_percentage.append("%.2f" % round(star3percentage, 2))
        
#             star4percentage = (rating4/feedback_count)*100
#             rating_percentage.append("%.2f" % round(star4percentage, 2))
        
#             star5percentage = (rating5/feedback_count)*100
#             rating_percentage.append("%.2f" % round(star5percentage, 2))

#         labels = ['1 Star','2 Star','3 Star','4 Star','5 Star']

#         if labels and data:
#             return JsonResponse({'status':"success", 'labels': labels, 'data': data, 'rating_percentage': rating_percentage, 'average_rating': average_rating, 'total_feedback_count': total_feedback_count}, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)





# class ParkingMerchantVehicleTypeWiseBillsGraph(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']
#         from_date = request.POST['from_date']
#         to_date = request.POST['to_date']

#         space_data = MerchantParkingLotSpace.objects.filter(m_business_id = m_business_id)

#         if from_date and to_date:
#             DATE_FORMAT = '%Y-%m-%d'

#             d_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
#             start_date = d_from_date.split('-')
#             start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
#             sd_filter = start_date.strftime(DATE_FORMAT)

#             date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
#             day_later = date_time_obj + timedelta(days=1)
#             x = day_later.date()
#             ed_filter = datetime.strptime(str(x), '%Y-%m-%d')


#             actual_space_data = []

#             for data_temp in space_data:

#                 try:
#                     temp = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True)

#                     vehicle_parked_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__range = (sd_filter,ed_filter)).count()

#                     vehicle_exit_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = True, manage_space = True, created_at__range = (sd_filter, ed_filter)).count()
                    
#                     space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()
                    
#                 except:
#                     space_avilable_count = 0

#                 space_avilable_count_temp = int(data_temp.spaces_count) - int(space_avilable_count)

#                 space_used = int(data_temp.spaces_count) - int(space_avilable_count_temp)

#                 parking_bills = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__range = (sd_filter, ed_filter))

#                 total_bills_made = 0

#                 for bill in parking_bills:
#                     total_bills_made = total_bills_made + float(bill.amount)

#                 actual_space_data.append({
#                     "id": data_temp.id,
#                     "vehicle_type": data_temp.vehicle_type,
#                     "space": data_temp.spaces_count,
#                     "available_parking_space": str(space_avilable_count_temp),
#                     "space_used": space_used,
#                     "space_avilable_count": space_avilable_count,
#                     "vehicle_exit_count": vehicle_exit_count,
#                     "vehicle_parked_count": vehicle_parked_count,
#                     "total_bills_made": float(total_bills_made)
#                 })

#             labels = []
#             data = []

#             for space in actual_space_data:
#                 vehicle_type_temp = space["vehicle_type"]
#                 labels.append(vehicle_type_temp)
#                 # data.append(round(space['vehicle_parked_count']))
#                 decimal_value = format(float(space['vehicle_parked_count']), ".2f")
#                 data.append(decimal_value)

#         else:

#             actual_space_data = []

#             for data_temp in space_data:

#                 try:
#                     temp = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True)

#                     vehicle_parked_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__date = timezone.now()).count()

#                     vehicle_exit_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = True, manage_space = True, created_at__date = timezone.now()).count()
                    
#                     space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()
                    
#                 except:
#                     space_avilable_count = 0

#                 space_avilable_count_temp = int(data_temp.spaces_count) - int(space_avilable_count)

#                 space_used = int(data_temp.spaces_count) - int(space_avilable_count_temp)

#                 parking_bills = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, created_at__date = timezone.now())

#                 total_bills_made = 0

#                 for bill in parking_bills:
#                     total_bills_made = total_bills_made + float(bill.amount)

#                 actual_space_data.append({
#                     "id": data_temp.id,
#                     "vehicle_type": data_temp.vehicle_type,
#                     "space": data_temp.spaces_count,
#                     "available_parking_space": str(space_avilable_count_temp),
#                     "space_used": space_used,
#                     "space_avilable_count": space_avilable_count,
#                     "vehicle_exit_count": vehicle_exit_count,
#                     "vehicle_parked_count": vehicle_parked_count,
#                     "total_bills_made": float(total_bills_made)
#                 })

#             labels = []
#             data = []

#             for space in actual_space_data:
#                 vehicle_type_temp = space["vehicle_type"]
#                 labels.append(vehicle_type_temp)
#                 # data.append(round(space['vehicle_parked_count']))
#                 decimal_value = format(float(space['vehicle_parked_count']), ".2f")
#                 data.append(decimal_value)
#                 # data.append(float(space['vehicle_parked_count']))

#         if labels and data:
#             return JsonResponse({'status':"success", 'labels': labels, 'data': data}, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class PetrolMerchantDashboardHeaderCalulations(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, created_at__date = timezone.now()).all()

#         total_bills = 0
#         total_collection = float(0)
#         total_flagged = 0

#         for bill in petrol_bills:
#             total_bills += 1
#             total_collection = total_collection + float(bill.total_amount)

#             if bill.bill_flag == True:
#                 total_flagged = total_flagged + 1

#         todays_payments = {
#             'cash': float(total_collection),
#             'online': ''
#         }

#         todays_bill = {
#             'total': total_bills,
#             'flagged': total_flagged
#         }

#         products = MerchantPetrolPump.objects.filter(m_business_id = m_business_id).all()

#         for product in products:
#             petrol_bills_temp = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, product_id = product.id, created_at__date = timezone.now()).all()
            
#             total_liter = float(0)
#             total_amount = float(0)

#             for bill in petrol_bills_temp:
#                 total_liter = total_liter + float(bill.volume)
#                 total_amount = total_amount + float(bill.amount)

#             product.total_liter_sold = total_liter
#             product.total_amount_colleted = total_amount

#             # product_name_temp = "'" + product.product_name + "'"

#             # productSaledoughnutChart_labels_temp.append(product_name_temp)

#             # productSaledoughnutChart_data_temp.append(total_amount)

#         todays_sales = []
#         foorloop_count = 0

#         for product in products:
#             if foorloop_count < 3:
#                 todays_sales.append({
#                     'product_name': product.product_name,
#                     'total_amount_colleted': float((round(product.total_amount_colleted,2)))
#                 })
#                 foorloop_count+=1


#         todays_rate = []
#         foorloop_count = 0

#         for product in products:
#             if foorloop_count < 3:
#                 todays_rate.append({
#                     'product_name': product.product_name,
#                     'product_cost': float(product.product_cost)
#                 })
#                 foorloop_count+=1

#         if m_business_id:
#             return JsonResponse({'status':"success", 'todays_payments': todays_payments, 'todays_bill': todays_bill, 'todays_sales': todays_sales, 'todays_rate': todays_rate}, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class PetrolMerchantProductSalesGraph(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']
#         from_date = request.POST['from_date']
#         to_date = request.POST['to_date']

#         products = MerchantPetrolPump.objects.filter(m_business_id = m_business_id).all()

#         labels = []
#         data = []

#         if from_date and to_date:
#             DATE_FORMAT = '%Y-%m-%d'

#             d_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
#             start_date = d_from_date.split('-')
#             start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
#             sd_filter = start_date.strftime(DATE_FORMAT)

#             date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
#             day_later = date_time_obj + timedelta(days=1)
#             x = day_later.date()
#             ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

#             for product in products:

#                 petrol_bills_temp = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, product_id = product.id, created_at__range = (sd_filter,ed_filter)).all()
#                 total_liter = 0
#                 total_amount = 0

#                 for bill in petrol_bills_temp:
#                     total_liter = total_liter + float(bill.volume)
#                     total_amount = total_amount + float(bill.amount)

#                 product.total_liter_sold = total_liter
#                 product.total_amount_colleted = total_amount

#                 product_name_temp = product.product_name

#                 labels.append(product_name_temp)

#                 # data.append(round(total_amount))
#                 decimal_value = format(float(total_amount), ".2f")
#                 data.append(decimal_value)

#         else:

#             for product in products:

#                 petrol_bills_temp = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, product_id = product.id, created_at__date = timezone.now()).all()
#                 total_liter = 0
#                 total_amount = 0

#                 for bill in petrol_bills_temp:
#                     total_liter = total_liter + float(bill.volume)
#                     total_amount = total_amount + float(bill.amount)

#                 product.total_liter_sold = total_liter
#                 product.total_amount_colleted = total_amount

#                 product_name_temp = product.product_name

#                 labels.append(product_name_temp)

#                 # data.append(round(total_amount))
#                 decimal_value = format(float(total_amount), ".2f")
#                 data.append(decimal_value)

#         if labels and data:
#             return JsonResponse({'status':"success", 'labels': labels, 'data': data}, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class PetrolMerchantAddOnSalesGraph(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']
#         from_date = request.POST.get('from_date')
#         to_date = request.POST.get('to_date')

#         addon_products = AddonPetrolPump.objects.filter(m_business_id = m_business_id).all()

#         labels = []
#         data = []

#         if from_date and to_date:
#             DATE_FORMAT = '%Y-%m-%d'

#             d_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
#             start_date = d_from_date.split('-')
#             start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
#             sd_filter = start_date.strftime(DATE_FORMAT)

#             date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
#             day_later = date_time_obj + timedelta(days=1)
#             x = day_later.date()
#             ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

#             for addon_product in addon_products:

#                 petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, created_at__range = (sd_filter,ed_filter)).all()

#                 total_sold = 0
#                 amount_collected = 0

#                 for bills in petrol_bills:
#                     addon_products_temp = bills.addon_product_id
#                     addon_product_cost_temp = bills.addon_product_cost
#                     addon_quantity_temp = bills.addon_quantity

#                     if addon_products_temp:
#                         bill_addon_products = list(addon_products_temp.split(","))
#                         bill_addon_costs = list(addon_product_cost_temp.split(","))
#                         addon_quantity = list(addon_quantity_temp.split(","))

#                         for product in bill_addon_products:
#                             if addon_product.id == int(product):
#                                 index = bill_addon_products.index(product)
#                                 total_sold = total_sold + int(addon_quantity[index])
#                                 amount_collected = amount_collected + float(bill_addon_costs[index]) * float(addon_quantity[index])
                
#                 addon_product.total_sold = total_sold
#                 addon_product.amount_collected = amount_collected

#                 product_name_temp = addon_product.product_name

#                 labels.append(product_name_temp)

#                 # data.append(round(amount_collected))
#                 decimal_value = format(float(amount_collected), ".2f")
#                 data.append(decimal_value)

#         else:

#             for addon_product in addon_products:

#                 petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, created_at__date = timezone.now()).all()

#                 total_sold = 0
#                 amount_collected = 0

#                 for bills in petrol_bills:
#                     addon_products_temp = bills.addon_product_id
#                     addon_product_cost_temp = bills.addon_product_cost
#                     addon_quantity_temp = bills.addon_quantity

#                     if addon_products_temp:
#                         bill_addon_products = list(addon_products_temp.split(","))
#                         bill_addon_costs = list(addon_product_cost_temp.split(","))
#                         addon_quantity = list(addon_quantity_temp.split(","))

#                         for product in bill_addon_products:
#                             if addon_product.id == int(product):
#                                 index = bill_addon_products.index(product)
#                                 total_sold = total_sold + int(addon_quantity[index])
#                                 amount_collected = amount_collected + float(bill_addon_costs[index]) * float(addon_quantity[index])
                
#                 addon_product.total_sold = total_sold
#                 addon_product.amount_collected = amount_collected

#                 product_name_temp = addon_product.product_name

#                 labels.append(product_name_temp)

#                 # data.append(round(amount_collected))
#                 decimal_value = format(float(amount_collected), ".2f")
#                 data.append(decimal_value)

#         if labels and data:
#             return JsonResponse({'status':"success", 'labels': labels, 'data': data}, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class PetrolMerchantUserAnalysis(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         m_user_id = request.POST['m_user_id']
#         # from_date = request.POST['from_date']
#         # to_date = request.POST['to_date']

#         # if from_date:
#         #     from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')

#         # if to_date:
#         #     to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%d-%m-%Y')


#         merchant_object = GreenBillUser.objects.get(id = m_user_id)

#         merchant_business = MerchantProfile.objects.get(id = m_business_id)

#         merchant_user = []

#         merchant_user.append({
#             'user_id': merchant_object
#         })

#         merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = m_business_id)

#         for user in merchant_user_temp:
#             merchant_user.append({
#                 'user_id': user.user_id
#                 })

#         merchant_user_details = []



#         for user in merchant_user:

#                 total_collection = 0
#                 total_flagged = 0

#                 petrol_logs = PetrolLog.objects.filter(user_id = user['user_id'].id, created_at__date = timezone.now())

#                 if petrol_logs:
#                     login_at = petrol_logs[0].login_at
#                     logout_at = petrol_logs[0].logout_at
#                 else:
#                     login_at = ""
#                     logout_at = ""
                   
#                 bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, user_id = user['user_id'].id, created_at__date = timezone.now()).all()
#                 total_bills = bills.count()

#                 for bill in bills:

#                     total_collection = total_collection + float(bill.total_amount)

#                     if bill.bill_flag == True and bill.flag_by == str(user['user_id'].id):
#                         total_flagged = total_flagged + 1

#                 name = user['user_id'].first_name + ' ' + user['user_id'].last_name

#                 import pytz
                  
#                 IST = pytz.timezone('Asia/Kolkata')

#                 try:
#                     login_at = login_at.astimezone(IST)
#                 except:
#                     pass

#                 try:
#                     logout_at = logout_at.astimezone(IST)
#                 except:
#                     pass

#                 if login_at:
#                     login_temp_time = str(login_at.time()).split('.')[0]
#                 else:
#                     login_temp_time = ""

#                 try:
#                     login_date = datetime.strptime(str(login_at.date()), '%Y-%m-%d').strftime('%d-%m-%Y')
#                 except:
#                     login_date = ""

#                 try:
#                     login_time = datetime.strptime(str(login_temp_time), '%H:%M:%S').strftime('%H:%M')
#                 except:
#                     login_time = ""

#                 if logout_at:
#                     logout_temp_time = str(logout_at.time()).split('.')[0]
#                 else:
#                     logout_temp_time = ""

#                 try:
#                     logout_time = datetime.strptime(str(logout_temp_time), '%H:%M:%S').strftime('%H:%M')
#                 except:
#                     logout_time = ""

#                 merchant_user_details.append({
#                     'name': name,
#                     'total_bills': total_bills,
#                     'total_collection': total_collection,
#                     'login_at': login_at,
#                     'logout_at': logout_time,
#                     'total_flagged': total_flagged,
#                     'login_date' : login_date,
#                     'login_time' : login_time,
#                 })

#         if merchant_user:
#             return JsonResponse({'status':"success", 'data': merchant_user_details}, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class ParkingMerchantUserAnalysis(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         m_user_id = request.POST['m_user_id']

#         # from_date = request.POST['from_date']
#         # to_date = request.POST['to_date']

#         merchant_object = GreenBillUser.objects.get(id = m_user_id)

#         merchant_business = MerchantProfile.objects.get(id = m_business_id)

#         merchant_user = []

#         merchant_user.append({
#             'user_id': merchant_object
#         })

#         merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = m_business_id)

#         for user in merchant_user_temp:
#             merchant_user.append({
#                 'user_id': user.user_id
#                 })


#         merchant_user_details = []

#         for user in merchant_user:

#             total_collection_bill = 0
#             total_flagged = 0
#             total_hours = ""

#             parking_logs = ParkingLog.objects.filter(user_id = user['user_id'].id, created_at__date = timezone.now())

#             if parking_logs:
#                 login_at = parking_logs[0].login_at
#                 logout_at = parking_logs[0].logout_at
                
#                 # total_hours = logout_at - login_at

#                 # seconds = total_hours.seconds
#                 # hours = seconds//3600
#                 # print(hours)

#             else:
#                 login_at = ""
#                 logout_at = ""
#                 total_hours = ""
               
#             bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, user_id = user['user_id'].id, created_at__date = timezone.now(), is_pass = False).all()
#             total_bills = bills.count()

#             for bill in bills:

#                 total_collection_bill = total_collection_bill + float(bill.amount)

#                 if bill.bill_flag == True and bill.flag_by == str(user['user_id'].id):
#                     total_flagged = total_flagged + 1

#             name = user['user_id'].first_name + ' ' + user['user_id'].last_name

#             parking_pass = ParkingLotPass.objects.filter(m_business_id = merchant_business.id, user_id = user['user_id'].id, created_at__date = timezone.now()).all()

#             total_pass_collection = 0
#             total_pass = 0

#             for pass_temp in parking_pass:

#                 total_pass_collection = total_pass_collection + float(pass_temp.amount)
#                 total_pass = total_pass + 1

#             import pytz
                  
#             IST = pytz.timezone('Asia/Kolkata')

#             try:
#                 login_at = login_at.astimezone(IST)
#             except:
#                 pass

#             try:
#                 logout_at = logout_at.astimezone(IST)
#             except:
#                 pass

#             if login_at:
#                 login_temp_time = str(login_at.time()).split('.')[0]
#             else:
#                 login_temp_time = ""

#             try:
#                 login_date = datetime.strptime(str(login_at.date()), '%Y-%m-%d').strftime('%d-%m-%Y')
#             except:
#                 login_date = ""

#             try:
#                 login_time = datetime.strptime(str(login_temp_time), '%H:%M:%S').strftime('%H:%M')
#             except:
#                 login_time = ""

#             if logout_at:
#                 logout_temp_time = str(logout_at.time()).split('.')[0]
#             else:
#                 logout_temp_time = ""

#             try:
#                 logout_time = datetime.strptime(str(logout_temp_time), '%H:%M:%S').strftime('%H:%M')
#             except:
#                 logout_time = ""

#             merchant_user_details.append({
#                 'name': name,
#                 'total_bills': total_bills,
#                 'total_collection_bill': total_collection_bill,
#                 'login_at': login_at,
#                 'logout_at': logout_time,
#                 'total_flagged': total_flagged,
#                 'total_hours' : total_hours,
#                 'total_pass_collection': total_pass_collection,
#                 'total_pass' : total_pass,
#                 'total_collection': float(total_collection_bill + total_pass_collection),
#                 'login_date' : login_date,
#                 'login_time' : login_time,
#             })

#         if merchant_user:
#             return JsonResponse({'status':"success", 'data': merchant_user_details}, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class ParkingMerchantSessionGraph(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         context = {}

#         # vehicles = MerchantParkingAddVehicle.objects.filter(m_business_id = m_business_id).all()

#         # labels = []

#         data = []

#         month_labels = []

#         today = date.today()

#         # for vehicle in vehicles:
#         #     labels.append(vehicle.vehicle_type)

#         for i in range(4,13):
#             datetime_object = datetime.strptime(str(i), "%m")
#             full_month_name = datetime_object.strftime("%b")
#             # data_temp['month'] = full_month_name
#             month_labels.append(full_month_name)

#         for j in range(1,4):
#             datetime_object = datetime.strptime(str(j), "%m")
#             full_month_name = datetime_object.strftime("%b")
#             month_labels.append(full_month_name)


#         # for vehicle in vehicles:

#         data_temp = []
#         month3 = []
#         year3 = []
#         for i in range(4,13):
#             y1 = today.year
#             year3.append(y1)
#             if i < 10:
#                 m1 = "0" + str(i)
#                 month3.append(m1) 
#             else:
#                 month3.append(i)
#         for j in range(1,4):
#             y2 = today.year + 1
#             year3.append(y2)
#             if j < 10:
#                 m2 = "0" + str(j)
#                 month3.append(m2)
#         for month,year in zip(month3,year3):
            
#             parking_bills = SaveParkingLotBill.objects.filter(m_business_id = m_business_id, created_at__year = year, created_at__month = month).all()
#             total_collection = 0

#             for bill in parking_bills:
#                 total_collection = total_collection + float(bill.amount)

#             decimal_value = format(float(total_collection), ".2f")
#             data_temp.append(decimal_value)
        
#         context['status'] = "success"

#         # context['labels'] = labels

#         context['month_labels'] = month_labels

#         context['Amount'] = data_temp

#         if context:
#             return JsonResponse(context, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class OtherBusinessMerchantSessionGraph(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         user_id = request.POST['user_id']

#         merchant_users_object = Merchant_users.objects.get(user_id = user_id)

#         merchant_object = merchant_users_object.merchant_user_id

#         merchant_business = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)


#         context = {}

#         data = []

#         month_labels = []

#         today = date.today()


#         for i in range(4,13):
#             datetime_object = datetime.strptime(str(i), "%m")
#             full_month_name = datetime_object.strftime("%b")
#             # data_temp['month'] = full_month_name
#             month_labels.append(full_month_name)

#         for j in range(1,4):
#             datetime_object = datetime.strptime(str(j), "%m")
#             full_month_name = datetime_object.strftime("%b")
#             month_labels.append(full_month_name)


#         data_temp = []
#         month3 = []
#         year3 = []
#         for i in range(4,13):
#             y1 = today.year
#             year3.append(y1)
#             if i < 10:
#                 m1 = "0" + str(i)
#                 month3.append(m1) 
#             else:
#                 month3.append(i)
#         for j in range(1,4):
#             y2 = today.year + 1
#             year3.append(y2)
#             if j < 10:
#                 m2 = "0" + str(j)
#                 month3.append(m2)
#         for month,year in zip(month3,year3):
            
#             merchant_bills = MerchantBill.objects.filter(business_name = merchant_business, created_at__year = year, created_at__month = month).all()
#             customer_bills2 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False,created_at__year = year,created_at__month = month).all()
#             total_collection = 0
#             total_collection1= 0
#             total_collection2= 0


#             for bill in merchant_bills:
#                 total_collection1= total_collection1+ float(bill.bill_amount)

#             for bill in customer_bills2:
#                 total_collection2= total_collection2+ float(bill.bill_amount)
                
#             total_collection = float(total_collection1) + float(total_collection2)

#             decimal_value = format(float(total_collection), ".2f")
#             data_temp.append(decimal_value)

        
#         context['status'] = "success"

#         context['month_labels'] = month_labels

#         context['Amount'] = data_temp

#         if context:
#             return JsonResponse(context, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class OtherBusinessBillSessionDatewiseGraph(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         user_id = request.POST['user_id']

#         merchant_users_object = Merchant_users.objects.get(user_id = user_id)

#         merchant_object = merchant_users_object.merchant_user_id

#         merchant_business = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)


#         context = {}

#         data_temp = []

#         days_labels = []

#         today = date.today()
#         current_year = today.year
#         current_month = today.month
#         total_days = calendar.monthrange(current_year, current_month)[1]
        
#         for i in range(1,total_days+1):
#             month_days = str(i)
#             days_labels.append(month_days)

        
#         month3 = []
#         year3 = []
#         days3 = []

#         y1 = today.year
#         year3.append(y1)
#         m1 = today.month
#         month3.append(m1)


#         for j in range(1,total_days+1):
#             days3.append(j) 

#         for year in year3:
#             for month in month3:
#                 for day in days3:
#                     merchant_bills1 = MerchantBill.objects.filter(business_name = merchant_business,created_at__year = year, created_at__month = month,created_at__day = day).values('created_at__day').annotate(data_sum=Sum('bill_amount'))
#                     customer_bills2 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__month = month,created_at__day = day).values('created_at__day').annotate(data_sum=Sum('bill_amount'))
                    
#                     if merchant_bills1 or customer_bills2:
#                         total_collection = 0
#                         total_collection1 = 0
#                         total_collection2 = 0
#                         if merchant_bills1:
#                             for bill in merchant_bills1:
#                                 total_collection1 = float(bill['data_sum'])

#                         if customer_bills2:
#                             for bill in customer_bills2:
#                                 total_collection2 = float(bill['data_sum'])
#                         total_collection = float(total_collection1) + float(total_collection2)

#                         decimal_value = format(float(total_collection), ".2f")
#                         data_temp.append(decimal_value)
#                     else:
#                         total_collection = float(0)

#                         decimal_value = format(float(total_collection), ".2f")
#                         data_temp.append(decimal_value)
                    

#         context['status'] = "success"

#         context['days_labels'] = days_labels

#         context['Amount'] = data_temp

#         if context:
#             return JsonResponse(context, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)

# class GetMerchantExeDetails(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         merchant_business = MerchantProfile.objects.get(id = m_business_id)

#         exe_send_and_print_bill_status1 = CustomerBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), exe_bill_type = 2).count()

#         exe_send_and_print_bill_status2 = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), exe_bill_type = 2).count()

#         exe_send_bill_status1 = CustomerBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), exe_bill_type = 1).count()

#         exe_send_bill_status2 = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), exe_bill_type = 1).count()

#         print_bill_status = ExePrintStatus.objects.filter(business_id = m_business_id, created_at__date = timezone.now()).count()

#         send_print_bill_status = int(exe_send_and_print_bill_status1) + int(exe_send_and_print_bill_status2)

#         send_bill_status = int(exe_send_bill_status1) + int(exe_send_bill_status2)

#         if merchant_business:
#             return JsonResponse({'status' : "success", "print_bill_status": print_bill_status, "send_print_bill_status": send_print_bill_status, "send_bill_status": send_bill_status}, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)




# class PetrolMerchantSessionGraph(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         context = {}

#         # products = MerchantPetrolPump.objects.filter(m_business_id = m_business_id).all()

#         # labels = []

#         data = []

#         month_labels = []

#         today = date.today()

#         # for product in products:
#         #     labels.append(product.product_name)
        
#         for i in range(4,13):
#             datetime_object = datetime.strptime(str(i), "%m")
#             full_month_name = datetime_object.strftime("%b")
#             month_labels.append(full_month_name)

#         for j in range(1,4):
#             datetime_object = datetime.strptime(str(j), "%m")
#             full_month_name = datetime_object.strftime("%b")
#             month_labels.append(full_month_name)


#         # for product in products:

#         data_temp = []
#         month3 = []
#         year3 = []
#         for i in range(4,13):
#             y1 = today.year
#             year3.append(y1)
#             if i < 10:
#                 m1 = "0" + str(i)
#                 month3.append(m1) 
#             else:
#                 month3.append(i)
#         for j in range(1,4):
#             y2 = today.year + 1
#             year3.append(y2)
#             if j < 10:
#                 m2 = "0" + str(j)
#                 month3.append(m2)
#         for month,year in zip(month3,year3):

#             petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, created_at__year = year, created_at__month = month).all()
            
#             total_collection = 0

#             for bill in petrol_bills:
#                 if bill.amount:
#                 # amount1 = float(str(bill.amount))
#                 # print(type(bill.amount),bill.amount,type(amount1))
#                     total_collection = total_collection + float(bill.total_amount)

#             decimal_value = format(float(total_collection), ".2f")
#             data_temp.append(decimal_value)


#         context['status'] = "success"

#         # context['labels'] = labels

#         context['month_labels'] = month_labels

#         context['Amount'] = data_temp

#         if context:
#             return JsonResponse(context, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class SuggestBusiness_API(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']
#         user_id = request.POST['user_id']

#         suggested_business_name = request.POST['suggested_business_name']
#         contact_no = request.POST['contact_no']
#         address = request.POST['address']

#         result = SuggestBusiness.objects.create(m_business_id = m_business_id, user_id = user_id, suggested_business_name = suggested_business_name, contact_no = contact_no, address = address)

#         if result:
#             return JsonResponse({'status': 'success', 'message': 'Business suggested Successfully !!!'}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Failed to suggest !!!'}, status=400)


# class SuggestBusinessList_API(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']
#         user_id = user_id = request.POST['user_id']

#         result = SuggestBusiness.objects.filter(m_business_id = m_business_id, user_id = user_id).order_by('-id')

#         business_list = []

#         for business in result:
#            business_list.append({
#             'id': business.id,
#             'm_business_id': business.m_business_id,
#             'user_id': business.user_id,
#             'suggested_business_name': business.suggested_business_name,
#             'contact_no': business.contact_no,
#             'address': business.address,
#             'suggested_date': datetime.strptime(str((business.created_at).date()), '%Y-%m-%d').strftime('%d-%m-%Y')
#            }) 

#         # serializer = SuggestBusinessSerializer(result, many=True)

#         if result:
#             return JsonResponse({'status' : "success", "data": business_list}, status=200, safe = False)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)

# class SuggestBrandAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         mobile_no =  request.POST['mobile_no']

#         brand = request.POST['brand']

#         location = request.POST['location']

#         contact_no = request.POST['contact_no']

#         result = SuggestBrand.objects.create(mobile_no = mobile_no, contact_no = contact_no, brand = brand, location = location, is_merchant = True)

#         if result:
#             return JsonResponse({'status': 'success'}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class FeedbackAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         mobile_no =  request.POST['mobile_no']

#         bug = request.POST['bug']

#         if bug == "true":
#             bug_status = True
#         else:
#             bug_status = False

#         suggestion = request.POST['suggestion']

#         if suggestion == "true":
#             suggestion_status = True
#         else:
#             suggestion_status = False

#         comments = request.POST['comments']

#         result = Feedback.objects.create(mobile_no = mobile_no, bug = bug_status, suggestion = suggestion_status, comments = comments, is_merchant = True)

#         if result:
#             return JsonResponse({'status': 'success'}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)



# class get_stamp_data(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         merchant_business_id = request.POST.get('business_id')

#         try:
#             merchant_select_stamp = merchantusagestamp.objects.filter(merchant_business_id = merchant_business_id).last()
#             stamp_id = merchant_select_stamp.merchant_stamp_id_one
#         except:
#             stamp_id = ''

#         if stamp_id:
#             temp_stamp = ""
#             temp_stamp = stamp_id.replace("[", "")
#             temp_stamp = temp_stamp.replace("]", "")
#             temp_stamp = temp_stamp.replace("'", "")
#             stamp_id = temp_stamp

#         new_stamp_id = stamp_id.split(", ")

#         stamp_data = []
#         own_stamp = []
#         for stamp in new_stamp_id:
#             if stamp:
#                 latest_stamp_record = wstampmodels.objects.filter(id=stamp)
#                 for stamp1 in latest_stamp_record:
#                     stamp_data.append({
#                         "id" : stamp1.id,
#                         "stamp_name" : stamp1.stamp_name,
#                         "type":'default_stamps',
#                         })

#         try:

#             saved_stamp_image = selectstampimage.objects.get(merchant_business_id = merchant_business_id).m_select_image
#             selected_stamp_image = merchantstampupload.objects.filter(id = saved_stamp_image)

#             for stamp in selected_stamp_image:
#                 own_stamp.append({
#                     "id" : stamp.id,
#                     "stamp_name": stamp.stamp_name,
#                     "type":'own_stamps',
#                     })
#         except:
#             pass

#         if stamp_data:
#             return JsonResponse({'status' : "success", "data1": stamp_data, "data2": own_stamp}, status=200)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)

# class CreateCashMemoAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         user_id = request.POST['user_id']
#         m_business_id = request.POST['m_business_id']

#         is_stamp_type = request.POST.get('stamp_type')
#         stamp_data_id = request.POST.get('stamp_id')

#         user_object = GreenBillUser.objects.get(id = user_id)
#         merchant_business_object = MerchantProfile.objects.get(id = m_business_id)

#         authorise = authorised_sign.objects.all()
#         auth = ''
#         sign = ''
#         for auth in authorise:
#             auth = auth.selection

#         try:
#             sign = authorised_sign.objects.get(id=auth).sign
#         except:
#             sign = ''

#         try:
#             memo = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_object).last()
#         except:
#             memo = ""

#         if not memo:
#             memo_no =  str("01").zfill(3)
#         else:
#             last_receipt = memo.memo_no
#             no = int(last_receipt) + 1
#             memo_no = str(no).zfill(3)

#         name = request.POST['name']
#         address = request.POST['address']
#         mobile_number = request.POST['mobile_number']
#         # total = request.POST['total']
#         # total_in_words = request.POST['total_in_words']
#         date = datetime.strptime(str(request.POST['date']), '%d-%m-%Y').strftime('%Y-%m-%d')
#         # template_choice = request.POST['template_choice']

#         description = request.POST['description']
#         quantity = request.POST['quantity']
#         rate = request.POST['rate']
#         # amount = request.POST['amount']
#         term_and_condition1 = request.POST.get('term_and_condition1')
#         term_and_condition2 = request.POST.get('term_and_condition2')
#         term_and_condition3 = request.POST.get('term_and_condition3')

#         authorised = sign

#         temp_desc = []
#         if description:
#             temp_desc.append(description)
    
#         temp_desc = [str(i or '') for i in temp_desc]
#         description = ",".join(temp_desc)

#         temp_quant = []
#         quantity_1 = quantity.split(",")
#         quantity_2 = [int(q) for q in quantity_1]
#         if quantity:
#             temp_quant.append(quantity)
        
#         conv = lambda i : i or ''
#         temp_quant = [conv(i) for i in temp_quant]
#         update_quantity = ",".join(temp_quant)


#         temp_rate = []
#         rate_1 = rate.split(",")
#         rate_2 = [int(r) for r in rate_1]
#         if rate:
#             temp_rate.append(rate)
         
#         conv = lambda i : i or ''
#         temp_rate = [conv(i) for i in temp_rate]
#         update_rate = ",".join(temp_rate)

        
#         temp_amnt1 = []
#         for quan, rat in zip(quantity_2, rate_2):
#             temp_amnt1.append(quan * rat)
#         temp_amnt2 = []
#         for j in temp_amnt1:
#           temp_amnt2.append(str(j))
#         amount = ','.join(temp_amnt2)

#         total = 0
#         for i in temp_amnt2:
#             total = total + int(i)
#         p = inflect.engine()
#         total_in_words = p.number_to_words(total)


#         result = CustomerCashMemoDetailModels.objects.create(merchant_business_id = merchant_business_object, merchant_user = user_object, 
#         name = name, address = address, mobile_number = mobile_number, total = total, 
#         total_in_words = total_in_words, date=date, description = description, 
#         quantity = update_quantity, rate = update_rate, amount = amount, 
#         memo_no = memo_no,authorised_sign=authorised,
#         term_and_condition1=term_and_condition1,
#         term_and_condition2=term_and_condition2,
#         term_and_condition3=term_and_condition3,
#         stamp_last_record = stamp_data_id,
#         is_stamp_type = is_stamp_type,)

#         letters = string.ascii_letters
#         digit = string.digits
#         random_string = str(result.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
        
#         result.memo_url = random_string

#         result.save()

#         if result:
#             return JsonResponse({'status': 'success'}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class CashMemoListAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         from_date = request.POST.get('from_date')

#         to_date = request.POST.get('to_date')

#         merchant_business_object = MerchantProfile.objects.get(id = m_business_id)

#         if from_date and to_date:
#             result = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_object, date__range=(from_date,to_date)).order_by("-id")
#             object_list_count = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_object, date__range=(from_date,to_date)).count()
#             total_cost_cash_memo = 0
#             for object1 in result:
#                 if object1.total:
#                     total_cost_cash_memo = float(object1.total) + float(total_cost_cash_memo)
#         else:
#             result = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_object).order_by("-id")
#             object_list_count = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_object).count()
#             total_cost_cash_memo = 0
#             for object1 in result:
#                 if object1.total:
#                     total_cost_cash_memo = float(object1.total) + float(total_cost_cash_memo)

#         coupons_list = []

#         for coupon in result:
#             coupons_list.append({
#                 'id': coupon.id,
#                 'memo_no': coupon.memo_no,
#                 'name': coupon.name,
#                 'address': coupon.address,
#                 'mobile_number': coupon.mobile_number,
#                 'date': datetime.strptime(str(coupon.date), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'total': float(coupon.total),
#                 'memo_url': "http://157.230.228.250/cash-memo/" + str(coupon.memo_url) + "/"
#             })

#         if result:
#             return JsonResponse({'status' : "success", "data": coupons_list, "from_date": from_date, "to_date": to_date, "object_list_count": object_list_count, "total_cost_cash_memo": total_cost_cash_memo}, status=200)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class CashMemoDeleteAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         m_business_id = request.POST['m_business_id']
#         merchant_business_object = MerchantProfile.objects.get(id = m_business_id)

#         cash_memo_id = request.POST['cash_memo_id']

#         result = CustomerCashMemoDetailModels.objects.get(id = cash_memo_id, merchant_business_id = merchant_business_object).delete()

#         if result:
#             return JsonResponse({'status' : "success"}, status=200)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class CashMemoSendAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         cash_memo_id = request.POST['cash_memo_id']
#         mobile_no = request.POST['mobile_no']

#         memo_object = CustomerCashMemoDetailModels.objects.get(id = cash_memo_id)

#         business_id = memo_object.merchant_business_id.id

#         subscription_object = getActiveSubscriptionPlan(request, business_id)

#         if subscription_object:
#             if subscription_object.total_amount_avilable and subscription_object.per_bill_cost:
#                 if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

#                     letters = string.ascii_letters
#                     digit = string.digits
#                     random_string = str(id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                    
#                     memo_object.memo_url = random_string

#                     memo_object.save()

#                     memo_url = ""

#                     device = DeviceId.objects.filter(mobile_no=mobile_no, user_type='customer').first()

#                     push_service = FCMNotification(api_key=settings.API_KEY)

#                     if device:

#                         registration_id = device.device_id

#                         message_title = "Receiving New Cash Memo"

#                         message_body = "You have received a Cash Memo from. " + str(memo_object.merchant_business_id.m_business_name)

#                         result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

#                     if mobile_no:

#                         memo_url = "http://157.230.228.250/cash-memo/" + str(random_string) + "/"

#                         s = pyshorteners.Shortener()
#                         short_url = s.tinyurl.short(memo_url)

#                         ts = int(time.time())

#                         data_temp = {
#                                 "keyword":"Cash Memo",
#                                 "timeStamp":ts,
#                                 "dataSet":
#                                     [
#                                         {
#                                             "UNIQUE_ID":"GB-" + str(ts),
#                                             "MESSAGE":"Hey Green Bill user to view or download your cash memo click on link " + short_url,
#                                             "OA":"GBBILL",
#                                             "MSISDN": str(mobile_no), # Recipient's Mobile Number
#                                             "CHANNEL":"SMS",
#                                             "CAMPAIGN_NAME":"hind_user",
#                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                             "USER_NAME":"hind_hsi",
#                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                             "DLT_CT_ID":"1007162098381110505", # Template Id
#                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                         }
#                                     ]
#                                 }

#                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                         response = requests.post(url, json = data_temp)

#                         if response.status_code:
#                             total_amount_avilable_new = 0
#                             total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
#                             subscription_object.total_amount_avilable = total_amount_avilable_new
#                             subscription_object.save()
#                             return JsonResponse({'status' : "success"}, status=200)
#                         else:
#                             return JsonResponse({'status' : "error"}, status=400)
#                     else:
#                         return JsonResponse({'status' : "error"}, status=400)
#                 else:
#                     return JsonResponse({'status': 'error','message':"Insufficient Balance. Please purchase purchase Add On's and try again !!!"}, status=400)
#             else:
#                 return JsonResponse({'status' : "error", 'message':"Not enough balance to send. Please recharge now !!!"}, status=400)

#         else:
#             return JsonResponse({'status': 'error','message':"You don't have active Green Bill Subscription. Please purchase and try again."}, status=400)


# class CashMemoSaveTemplate(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user_id = request.POST['user_id']
#         selected_template = request.POST['selected_template'] 

#         user_object = GreenBillUser.objects.get(id = user_id)

#         result=save_template_for_cashmemo.objects.create(merchant_user=user_object, template=selected_template)
        
#         if result:
#             return JsonResponse({'status' : "success",'message':"Template Added Successfully."}, status=200)
#         else:
#             return JsonResponse({'status' : "error",'message':"Fail to Add."}, status=400)


# class CashMemoTemplateExist(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user_id = request.POST['user_id']
#         # selected_template = request.POST['selected_template'] 

#         try:
#             user_object = GreenBillUser.objects.filter(id = user_id).last()
#         except UniversityDetails.DoesNotExist:
#             user = None

#         result = []

#         # if save_template_for_cashmemo.objects.filter(merchant_user=user_object).exists():
#         #     data = save_template_for_cashmemo.objects.get(merchant_user=user_object)
#         #     result.append({
#         #             'template_id':data.template,
#         #             'term1': "",
#         #             'term2': "",
#         #             'term3': ""
#         #             })
#         # else:
#         #     result.append({
#         #             'template_id': "",
#         #             })

        

#         terms = CustomerCashMemoDetailModels.objects.filter(merchant_user=user_object).last()

#         if terms:
#             if terms.term_and_condition1:
#                 condition1 = terms.term_and_condition1
#             else:
#                 condition1 = ""

#             if terms.term_and_condition2:
#                 condition2 = terms.term_and_condition2
#             else:
#                 condition2 = ""

#             if terms.term_and_condition3:
#                 condition3 = terms.term_and_condition3
#             else:
#                 condition3 = ""

#             if save_template_for_cashmemo.objects.filter(merchant_user=user_object).exists():
#                 try:
#                     data = save_template_for_cashmemo.objects.filter(merchant_user=user_object).last()
#                 except:
#                     data = '0'

#                 result.append({
#                         'template_id':data.template,
#                         'term1': condition1,
#                         'term2': condition2,
#                         'term3': condition3,
#                         })
#             else:
#                 result.append({
#                         'template_id': "",
#                         'term1': condition1,
#                         'term2': condition2,
#                         'term3': condition3,
#                         }) 
#         else:
#             if save_template_for_cashmemo.objects.filter(merchant_user=user_object).exists():
#                 data = save_template_for_cashmemo.objects.get(merchant_user=user_object)
#                 result.append({
#                         'template_id':data.template,
#                         'term1': "",
#                         'term2': "",
#                         'term3': "",
#                         })

#             else:
#                 result.append({
#                         'template_id': "",
#                         'term1': "",
#                         'term2': "",
#                         'term3': "",
#                         })


#         if result:
#             return JsonResponse({'status' : "success",'data':result}, status=200)
#         else:
#             return JsonResponse({'status' : "error",'data':result}, status=400)



# class CreateReceiptAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         user_id = request.POST['user_id']
#         m_business_id = request.POST['m_business_id']

#         is_stamp_type = request.POST.get('stamp_type')
#         stamp_data_id = request.POST.get('stamp_id')

#         user_object = GreenBillUser.objects.get(id = user_id)
#         merchant_business_object = MerchantProfile.objects.get(id = m_business_id)

#         try:
#             receipt = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_object).last()
#         except:
#             receipt = ""

#         if not receipt:
#             receipt_no =  str("01").zfill(3)

#         else:
#             last_receipt = receipt.receipt_no
#             no = int(last_receipt) + 1
#             receipt_no =  str(no).zfill(3)

#         authorise = authorised_sign.objects.all()
#         auth = ''
#         sign = ''
#         for auth in authorise:
#             auth = auth.selection
#         try:
#             sign = authorised_sign.objects.get(id=auth).sign
#         except:
#             sign = ''

#         mobile_no = request.POST['mobile_no']
#         cash_received_from = request.POST['cash_received_from']
#         amount_for = request.POST['amount_for']
#         date = datetime.strptime(str(request.POST['date']), '%d-%m-%Y').strftime('%Y-%m-%d')
#         # template_choice = request.POST['template_choice']
#         total = request.POST['total']
#         received_in_cash = request.POST.get('cash'),
#         received_in_cheque = request.POST.get('cheque'),
#         received_in_other = request.POST.get('other'),
       
#         term_and_condition1 = request.POST.get('term_and_condition1')
#         term_and_condition2 = request.POST.get('term_and_condition2')
#         term_and_condition3 = request.POST.get('term_and_condition3')
#         authorised = sign
#         # grand_total = request.POST['grand_total']

#         ### this three lines are written by yaman if needed can be deleted

#         greenbilluser = GreenBillUser.objects.get(id=user_id)

#         template_selected = save_template_for_receipt.objects.filter(merchant_user=greenbilluser).last()

#         template = template_selected.template


#         p = inflect.engine()
#         rs = p.number_to_words(total)
        
#         result = CustomerReceiptDetailsModels.objects.create(merchant_business_id = merchant_business_object, merchant_user = user_object, 
#         receipt_no = receipt_no, mobile_number = mobile_no, cash_received_from = cash_received_from, 
#         rs = rs, amount_for = amount_for, date = date, 
#         total = total,received_in_cash=received_in_cash,
#         received_in_cheque=received_in_cheque,
#         received_in_other=received_in_other,
#         authorised_sign=authorised,
#         term_and_condition1 = term_and_condition1,
#         term_and_condition2 = term_and_condition2,
#         term_and_condition3 = term_and_condition3,
#         template_choice=template,
#         stamp_last_record = stamp_data_id,
#         is_stamp_type = is_stamp_type,)

#         letters = string.ascii_letters
#         digit = string.digits
#         random_string = str(result.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
        
#         result.receipt_url = random_string

#         result.save()

#         if result:
#             return JsonResponse({'status': 'success'}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)

# class ReceiptListAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         from_date = request.POST.get('from_date')

#         to_date = request.POST.get('to_date')

#         merchant_business_object = MerchantProfile.objects.get(id = m_business_id)

#         if from_date and to_date:
#             result = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_object, date__range=(from_date,to_date)).order_by("-id")
#             object_list_count = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_object, date__range=(from_date,to_date)).count()
#             total_cost_receipt = 0
#             for object1 in result:
#                 if object1.total:
#                     total_cost_receipt = float(object1.total) + float(total_cost_receipt)

#         else:
#             result = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_object).order_by("-id")
#             object_list_count = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_object).count()
#             total_cost_receipt = 0
#             for object1 in result:
#                 if object1.total:
#                     total_cost_receipt = float(object1.total) + float(total_cost_receipt)

#         receipt_list = []

#         for receipt in result:
#             receipt_list.append({
#                 'id': receipt.id,
#                 'receipt_no': receipt.receipt_no,
#                 'mobile_number': receipt.mobile_number,
#                 'date': datetime.strptime(str(receipt.date), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'total': float(receipt.total) if receipt.total else float(0),
#                 'receipt_url': "http://157.230.228.250/receipt/" + str(receipt.receipt_url) + "/",
#             })

#         if result:
#             return JsonResponse({'status' : "success", "data": receipt_list,"from_date":from_date,"to_date":to_date, "total_cost_receipt":total_cost_receipt,"object_list_count":object_list_count}, status=200)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)

# class ReceiptDeleteAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         m_business_id = request.POST['m_business_id']
#         merchant_business_object = MerchantProfile.objects.get(id = m_business_id)

#         receipt_id = request.POST['receipt_id']

#         result = CustomerReceiptDetailsModels.objects.get(id = receipt_id, merchant_business_id = merchant_business_object).delete()

#         if result:
#             return JsonResponse({'status' : "success"}, status=200)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class ReceiptSendAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         receipt_id = request.POST['receipt_id']
#         mobile_no = request.POST['mobile_no']

#         receipt_object = CustomerReceiptDetailsModels.objects.get(id = receipt_id)

#         business_id = receipt_object.merchant_business_id.id

#         subscription_object = getActiveSubscriptionPlan(request, business_id)

#         if subscription_object:
#             if subscription_object.total_amount_avilable and subscription_object.per_bill_cost:

#                 if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

#                     letters = string.ascii_letters
#                     digit = string.digits
#                     random_string = str(id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                    
#                     receipt_object.receipt_url = random_string

#                     receipt_object.save()

#                     receipt_url = ""

#                     device = DeviceId.objects.filter(mobile_no=mobile_no, user_type='customer').first()

#                     push_service = FCMNotification(api_key=settings.API_KEY)

#                     if device:

#                         registration_id = device.device_id

#                         message_title = "Receiving New Receipt"

#                         message_body = "You have received a Payment Receipt from . " + str(receipt_object.merchant_business_id.m_business_name)

#                         result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

#                     if mobile_no:

#                         receipt_url = "http://157.230.228.250/receipt/" + str(random_string) + "/"

#                         s = pyshorteners.Shortener()
#                         short_url = s.tinyurl.short(receipt_url)

#                         ts = int(time.time())

#                         data_temp = {
#                             "keyword":"Cash Receipt",
#                             "timeStamp":ts,
#                             "dataSet":
#                                 [
#                                     {
#                                         "UNIQUE_ID":"GB-" + str(ts),
#                                         "MESSAGE":"Hey Green Bill user to view or download your receipt click on link " + short_url,
#                                         "OA":"GBBILL",
#                                         "MSISDN": str(mobile_no), # Recipient's Mobile Number
#                                         "CHANNEL":"SMS",
#                                         "CAMPAIGN_NAME":"hind_user",
#                                         "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                         "USER_NAME":"hind_hsi",
#                                         "DLT_TM_ID":"1001096933494158", # TM ID
#                                         "DLT_CT_ID":"1007162098384997217", # Template Id
#                                         "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                     }
#                                 ]
#                             }

#                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                         response = requests.post(url, json = data_temp)

#                         if response.status_code:
#                             total_amount_avilable_new = 0
#                             total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
#                             subscription_object.total_amount_avilable = total_amount_avilable_new
#                             subscription_object.save()
#                             return JsonResponse({'status' : "success"}, status=200)
#                         else:
#                             return JsonResponse({'status' : "error"}, status=400)
#                     else:
#                         return JsonResponse({'status' : "error"}, status=400)
#                 else:
#                     return JsonResponse({'status': 'error','message':"Insufficient Balance. Please purchase purchase Add On's and try again !!!"}, status=400)
#             else:
#                 return JsonResponse({'status': 'error','message':"Not enough balance to send. Please recharge now. !!!"}, status=400)

#         else:
#             return JsonResponse({'status': 'error','message':"You don't have active Green Bill Subscription. Please purchase and try again."}, status=400)



# class ReceiptSaveTemplate(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user_id = request.POST['user_id']
#         selected_template = request.POST['template_choice'] 
#         user_object = GreenBillUser.objects.get(id=user_id)

#         result=save_template_for_receipt.objects.create(merchant_user=user_object, template=selected_template)
        
#         if result:
#             return JsonResponse({'status' : "success",'message':"Template Added Successfully."}, status=200)
#         else:
#             return JsonResponse({'status' : "error",'message':"Fail to Add."}, status=400)


# class ReceiptTemplateExist(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user_id = request.POST['user_id']
#         # selected_template = request.POST['selected_template'] 

#         try:
#             user_object = GreenBillUser.objects.get(id = user_id)
#         except:
#             user = None

#         result = []

#         # if save_template_for_receipt.objects.filter(merchant_user=user_object).exists():
#         #     data = save_template_for_receipt.objects.get(merchant_user=user_object)
#         #     result.append({
#         #             'template_id':data.template,
#         #             })
#         # else:
#         #     result.append({
#         #             'template_id': "",
#         #             })

#         terms = CustomerReceiptDetailsModels.objects.filter(merchant_user=user_object).last()

#         if terms:

#             if terms.term_and_condition1:
#                 condition1 = terms.term_and_condition1
#             else:
#                 condition1 = ""

#             if terms.term_and_condition2:
#                 condition2 = terms.term_and_condition2
#             else:
#                 condition2 = ""

#             if terms.term_and_condition3:
#                 condition3 = terms.term_and_condition3
#             else:
#                 condition3 = ""

#             if save_template_for_receipt.objects.filter(merchant_user=user_object).exists():
#                 data = save_template_for_receipt.objects.filter(merchant_user=user_object).last()
#                 result.append({
#                         'template_id':data.template,
#                         'term1': condition1,
#                         'term2': condition2,
#                         'term3': condition3,
#                         })

#             else:
#                 result.append({
#                         'template_id': "",
#                         'term1': condition1,
#                         'term2': condition2,
#                         'term3': condition3,
#                         })
#         else:
#             if save_template_for_receipt.objects.filter(merchant_user=user_object).exists():
#                 data = save_template_for_receipt.objects.filter(merchant_user=user_object).last()
#                 result.append({
#                         'template_id':data.template,
#                         'term1': "",
#                         'term2': "",
#                         'term3': "",
#                         })

#             else:
#                 result.append({
#                         'template_id': "",
#                         'term1': "",
#                         'term2': "",
#                         'term3': "",
#                         })

#         if result:
#             return JsonResponse({'status' : "success",'data':result}, status=200)
#         else:
#             return JsonResponse({'status' : "error",'data':result}, status=400)


# class GetSupportAndFaqsModulesAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         customer_modules = []
#         customer_modules_new = []

#         m_business_id = request.POST['m_business_id']

#         merchant_object = MerchantProfile.objects.get(id = m_business_id)

#         if merchant_object.m_business_category.id == 11:
#             user_name = "petrol_pump"
#         elif merchant_object.m_business_category.id == 12:
#             user_name = "parking_lot"
#         else:
#             user_name = "other_business"

#         # print(user_name)

#         faqs = FAQs_Model.objects.filter(user_name = user_name)

#         for faq in faqs:
#             if faq.module_name in customer_modules:
#                 continue
#             else:
#                 customer_modules.append(faq.module_name)

#         for module in customer_modules:

#             try:
#                 module_name_temp = Add_Module_Name.objects.get(id = module)
#                 module_name = module_name_temp.module_name
#             except:
#                 module_name = ""

#             if module_name:
#                 customer_modules_new.append({
#                     'id': module,
#                     'module_name': module_name,
#                 })

#         if customer_modules_new:
#             return JsonResponse({'status': 'success', 'data' : customer_modules_new}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class GetSupportAndFaqsDataAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         module_id =  request.POST['module_id']
       
#         faqs = FAQs_Model.objects.filter(module_name = module_id)
        
#         faqs_serializer = MerchantFaqsSerializer(faqs, many=True)

#         if module_id:
#             return JsonResponse({'status': 'success', 'faqs' : faqs_serializer.data}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)

                
# class CreateandUpdateCouponAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
        
#         coupon_type = request.POST['coupon_type']
#         # coupon_logo = request.FILES['coupon_logo']
#         m_user_id = request.POST['m_user_id']
#         merchant_object = GreenBillUser.objects.get(id = m_user_id)
#         status1 = ""
#         status2 = ""
#         if coupon_type == "coupon_value":
#             amount_in = request.POST['amount_in']

#             if amount_in == "percentage":
#                 coupon_val = request.POST['coupon_value_percent']
#                 coupon_val_per = coupon_val 

#                 if request.POST["coupon_id"] != "":

#                     status1 = CouponModel.objects.update_or_create(id=int(request.POST["coupon_id"]),defaults={
#                         "coupon_name" : request.POST['coupon_name'],
#                         "valid_from" : datetime.strptime(str(request.POST['valid_from']), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                         "valid_through" : datetime.strptime(str(request.POST['valid_through']), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                         "coupon_code" : request.POST['coupon_code'],
#                         "coupon_value" : coupon_val_per,
#                         "green_point" : request.POST['green_point'],
#                         # "coupon_logo" : coupon_logo,
#                         "coupon_background_color":"",
#                         "coupon_valid_for_user" : request.POST['coupon_valid_for_user'],
#                         'merchant_business_id': request.POST['m_business_id'],
#                         'amount_in' : amount_in
#                         })
                        
#                 else:
#                     status2 = CouponModel.objects.create(
#                         merchant_id = merchant_object,
#                         coupon_name = request.POST['coupon_name'],
#                         valid_from = datetime.strptime(str(request.POST['valid_from']), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                         valid_through = datetime.strptime(str(request.POST['valid_through']), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                         coupon_code = request.POST['coupon_code'],
#                         coupon_value = coupon_val_per + "%",
#                         green_point = request.POST['green_point'],
#                         # coupon_logo = request.FILES['coupon_logo'],
#                         coupon_background_color = "",
#                         coupon_valid_for_user = request.POST['coupon_valid_for_user'],
#                         merchant_business_id = request.POST['m_business_id'],
#                         amount_in = amount_in
#                     )

#             else:
#                 coupon_val = request.POST['coupon_value_fixamount']
#                 if request.POST["coupon_id"] != "":
#                     status1 = CouponModel.objects.update_or_create(id=int(request.POST["coupon_id"]),defaults={
#                         "coupon_name" : request.POST['coupon_name'],
#                         "valid_from" : datetime.strptime(str(request.POST['valid_from']), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                         "valid_through" : datetime.strptime(str(request.POST['valid_through']), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                         "coupon_code" : request.POST['coupon_code'],
#                         "coupon_value":coupon_val,
#                         "green_point" : request.POST['green_point'],
#                         # "coupon_logo" : request.FILES['coupon_logo'],
#                         "coupon_background_color":"",
#                         "coupon_valid_for_user" : request.POST['coupon_valid_for_user'],
#                         'merchant_business_id': request.POST['m_business_id'],
#                         'amount_in':amount_in
#                         })
                    
#                 else:
#                     status2 = CouponModel.objects.create(
#                         merchant_id = merchant_object,
#                         coupon_name = request.POST['coupon_name'],
#                         valid_from = datetime.strptime(str(request.POST['valid_from']), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                         valid_through = datetime.strptime(str(request.POST['valid_through']), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                         coupon_code = request.POST['coupon_code'],
#                         coupon_value = coupon_val,
#                         green_point = request.POST['green_point'],
#                         # coupon_logo = request.FILES['coupon_logo'],
#                         coupon_background_color="",
#                         coupon_valid_for_user = request.POST['coupon_valid_for_user'],
#                         merchant_business_id = request.POST['m_business_id'],
#                         amount_in = amount_in
#                     )
#         else:
#             coupon_caption_name = request.POST['coupon_caption_name']
#             amount_in = request.POST['amount_in']

#             if request.POST["coupon_id"] != "":
#                 status1 = CouponModel.objects.update_or_create(id=int(request.POST["coupon_id"]),defaults={
#                     "coupon_name" : request.POST['coupon_name'],
#                     "valid_from" : datetime.strptime(str(request.POST['valid_from']), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                     "valid_through" : datetime.strptime(str(request.POST['valid_through']), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                     "coupon_code" : request.POST['coupon_code'],
#                     "green_point" : request.POST['green_point'],
#                     # "coupon_logo" : request.FILES['coupon_logo'],
#                     "coupon_caption" : coupon_caption_name,
#                     "coupon_background_color" : "",
#                     "coupon_valid_for_user" : request.POST['coupon_valid_for_user'],
#                     'merchant_business_id': request.POST['m_business_id'],
#                     'amount_in' : amount_in
#                     })

#             else:
#                 status2 = CouponModel.objects.create(
#                     merchant_id = merchant_object,
#                     coupon_name = request.POST['coupon_name'],
#                     valid_from = datetime.strptime(str(request.POST['valid_from']), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                     valid_through = datetime.strptime(str(request.POST['valid_through']), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                     coupon_code = request.POST['coupon_code'],
#                     green_point = request.POST['green_point'],
#                     # coupon_logo = request.FILES['coupon_logo'],
#                     coupon_caption = coupon_caption_name,
#                     coupon_background_color = "",
#                     coupon_valid_for_user = request.POST['coupon_valid_for_user'],
#                     merchant_business_id = request.POST['m_business_id'],
#                     amount_in = amount_in
#                 )

#         if status1:
#             return JsonResponse({'status': 'success', 'message': 'Coupon updated Successfully'}, status=200)
#         elif status2:
#             return JsonResponse({'status': 'success', 'message': 'Coupon created Successfully'}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Fail to Create !!!'}, status=400)
            


# class MerchantCouponListAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
        
#         m_business_id = request.POST['m_business_id']

#         coupon_list = CouponModel.objects.filter(merchant_business_id = m_business_id).order_by('-id')
#         coupon_data = []
#         today = date.today()
#         for coupon in coupon_list:

#             if coupon.valid_through < today:
#                 coupon.expiry_status = True
#             else:
#                 coupon.expiry_status = False

#             user_object = GreenBillUser.objects.get(mobile_no = coupon.merchant_id)
#             coupon.valid_from = datetime.strptime(str(coupon.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y')
#             coupon.valid_through = datetime.strptime(str(coupon.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y')

#             count_redeem = RedeemCouponModel.objects.filter(coupon_id = coupon.id ).count()


#             if PromotionsAmount.objects.all():
#                 data = PromotionsAmount.objects.latest('id')
#                 coupon_amount = data.coupon_amount
#             else:
#                 coupon_amount = 0

#             if coupon.total_customers:
#                 coupon.total_amount = float(coupon_amount) * float(coupon.total_customers)
#             else:
#                 coupon.total_amount = 0

#             coupon_data.append({
#                 'id': int(coupon.id),
#                 'merchant_business_id': coupon.merchant_business_id,
#                 'coupon_name': coupon.coupon_name,
#                 'valid_from': coupon.valid_from,
#                 'valid_through': coupon.valid_through,
#                 'coupon_code': coupon.coupon_code,
#                 'coupon_value': coupon.coupon_value,
#                 'green_point': coupon.green_point,
#                 'coupon_logo': coupon.coupon_logo.url,
#                 'coupon_redeem': str(count_redeem),
#                 'coupon_caption': coupon.coupon_caption,
#                 'coupon_valid_for_user': coupon.coupon_valid_for_user,
#                 'amount_in': coupon.amount_in,
#                 'cout': coupon.cout,
#                 'coupon_panel': coupon.coupon_panel,
#                 'total_customers': coupon.total_customers,
#                 'total_amount': coupon.total_amount,
#                 'expired': coupon.expiry_status,
#             })

#         # serializer = MerchantCouponListSerializer(coupon_list, many=True)

#         if coupon_list:
#             return JsonResponse({'status': 'success', 'data' : coupon_data}, status=200)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)

# class MerchantDeleteCouponAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         coupon_id = request.POST['coupon_id']
#         result = CouponModel.objects.get(id=coupon_id).delete()
#         if result:
#             return JsonResponse({"status": 'success'}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class GetMerchantClicksOfCouponsAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         coupon_id = request.POST['coupon_id']

#         count = CouponModel.objects.get(id = coupon_id).cout

#         count1 = count + 1

#         result = CouponModel.objects.filter(id = coupon_id).update(cout = count1)

#         if result:            
#             return JsonResponse({'status': 'success'}, status=200)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class MerchantGetOffersAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         user_id = request.POST['user_id']
#         merchant_users_object = Merchant_users.objects.get(user_id = user_id)
#         business_name= MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)
#         merchant_name_object = business_name.m_business_name 
#         merchant_state_object = business_name.m_state
#         merchant_city_object = business_name.m_city
#         merchant_area_object = business_name.m_area
#         merchant_business_category_id = business_name.m_business_category.id

#         offers = OfferModel.objects.filter(status = "1", Offer_type = "Merchant").order_by('-id')

#         offers_list = []
#         today = date.today()
#         today_date = today.strftime("%Y-%m-%d")

#         for offer in offers:
#             offer_image_url = "http://157.230.228.250" + str(offer.offer_image.url)

#             try:
#                 business_logo = "http://157.230.228.250" + str(offer.merchant_business_id.m_business_logo.url)
#             except:
#                 business_logo = ""

#             if offer.offer_panel == "owner":
#                 business_logo = "http://157.230.228.250" + str(offer.offer_logo.url)

#             try:
#                 merchant_business_id = offer.merchant_business_id.id
#             except:
#                 merchant_business_id = ""

#             try:
#                 m_business_name = offer.merchant_business_id.m_business_name
#             except:
#                 m_business_name = offer.o_business_name

#             try:
#                 merchant_user = offer.merchant_user.id
#             except:
#                 merchant_user = ""

#             if datetime.strptime(str(offer.valid_through), "%Y-%m-%d").date() >= datetime.strptime(str(today_date), "%Y-%m-%d").date():
#                 if merchant_name_object != offer.merchant_business_name:
#                     if offer.offer_business_category:
#                         if str(merchant_business_category_id) in offer.offer_business_category:
#                             if offer.merchant_state:
#                                 if merchant_state_object in offer.merchant_state:
#                                     if offer.merchant_city:
#                                         if merchant_city_object in offer.merchant_city:
#                                             if offer.merchant_area:
#                                                 if merchant_area_object in offer.merchant_area:
#                                                     offers_list.append({
#                                                         "id": offer.id,
#                                                         "offer_name": offer.offer_name,
#                                                         "offer_caption": offer.offer_caption,
#                                                         "valid_from": datetime.strptime(str(offer.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                                                         "valid_through": datetime.strptime(str(offer.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                                                         "offer_image": offer_image_url,
#                                                         "disapproved_reason": offer.disapproved_reason,
#                                                         "status": offer.status,
#                                                         "Offer_type": offer.Offer_type,
#                                                         "offer_business_category": offer.offer_business_category,
#                                                         "created_date": offer.created_date,
#                                                         "offer_panel": offer.offer_panel,
#                                                         "merchant_user": merchant_user,
#                                                         "merchant_business_id": merchant_business_id,
#                                                         "m_business_logo": business_logo,
#                                                         "m_business_name":  m_business_name,
#                                                     })
#                                             else:
#                                                 offers_list.append({
#                                                     "id": offer.id,
#                                                     "offer_name": offer.offer_name,
#                                                     "offer_caption": offer.offer_caption,
#                                                     "valid_from": datetime.strptime(str(offer.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                                                     "valid_through": datetime.strptime(str(offer.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                                                     "offer_image": offer_image_url,
#                                                     "disapproved_reason": offer.disapproved_reason,
#                                                     "status": offer.status,
#                                                     "Offer_type": offer.Offer_type,
#                                                     "offer_business_category": offer.offer_business_category,
#                                                     "created_date": offer.created_date,
#                                                     "offer_panel": offer.offer_panel,
#                                                     "merchant_user": merchant_user,
#                                                     "merchant_business_id": merchant_business_id,
#                                                     "m_business_logo": business_logo,
#                                                     "m_business_name":  m_business_name,
#                                                 })
#                                     else:
#                                         offers_list.append({
#                                             "id": offer.id,
#                                             "offer_name": offer.offer_name,
#                                             "offer_caption": offer.offer_caption,
#                                             "valid_from": datetime.strptime(str(offer.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                                             "valid_through": datetime.strptime(str(offer.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                                             "offer_image": offer_image_url,
#                                             "disapproved_reason": offer.disapproved_reason,
#                                             "status": offer.status,
#                                             "Offer_type": offer.Offer_type,
#                                             "offer_business_category": offer.offer_business_category,
#                                             "created_date": offer.created_date,
#                                             "offer_panel": offer.offer_panel,
#                                             "merchant_user": merchant_user,
#                                             "merchant_business_id": merchant_business_id,
#                                             "m_business_logo": business_logo,
#                                             "m_business_name":  m_business_name,
#                                         })

#         # serializer = MerchantOffersListSerializer(offers, many=True)

#         if offers_list:
#             return JsonResponse({'status': 'success', 'data' : offers_list}, status=200)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class GetMerchantClicksOfOffersAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         offer_id = request.POST['offer_id']

#         count = OfferModel.objects.get(id = offer_id).cout

#         count1 = count + 1

#         result = OfferModel.objects.filter(id = offer_id).update(cout = count1)

#         if result:            
#             return JsonResponse({'status': 'success'}, status=200)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)



# class MerchantCreateandUpdateOffersAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         merchant_id = request.POST['merchant_id']
#         merchant_object = GreenBillUser.objects.get(id = merchant_id)
#         obj1 = ""
#         obj2 = ""

#         if request.POST['offer_id'] != "":
#             offer_name = request.POST['offer_name']
#             offer_caption = request.POST['offer_caption']
#             valid_from = request.POST['valid_from']
#             Offer_type = request.POST.get('user')
#             valid_through = request.POST['valid_through']
#             obj1 = OfferModel.objects.update_or_create(
#                 id=int(request.POST["offer_id"]), 
#                 defaults={"Offer_type": Offer_type, 
#                 "offer_name": offer_name, 
#                 "offer_caption": offer_caption, 
#                 "valid_from": datetime.strptime(str(valid_from), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                 "valid_through": datetime.strptime(str(valid_through), '%d-%m-%Y').strftime('%Y-%m-%d'), 
#                 })
#         else:
#             merchant_business_id = request.POST['merchant_business_id']
#             merchant_business_id1 = MerchantProfile.objects.get(id = merchant_business_id, m_active_account = True)
#             offer_name = request.POST['offer_name']
#             offer_caption = request.POST['offer_caption']
#             Offer_type = request.POST['user']
#             offer_image = request.FILES['offer_image']
#             valid_from = request.POST['valid_from']
#             valid_through = request.POST['valid_through']

       
#             obj2 = OfferModel.objects.create(
#                  merchant_user = merchant_object,
#                  merchant_business_id = merchant_business_id1, 
#                  offer_caption = offer_caption, 
#                  valid_from = datetime.strptime((valid_from), '%d-%m-%Y').strftime('%Y-%m-%d'),
#                  valid_through = datetime.strptime((valid_through), '%d-%m-%Y').strftime('%Y-%m-%d'), 
#                  offer_image = offer_image, 
#                  Offer_type = Offer_type, 
#                  offer_name = offer_name
#             )
            

#         if obj1:
#             return JsonResponse({'status': 'success', 'message': 'Offer updated Successfully'}, status=200)
#         elif obj2:
#             return JsonResponse({'status': 'success', 'message': 'Offer created Successfully'}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Fail to Create !!!'}, status=400)


# class MerchantOffersListAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
        
#         merchant_business_id = request.POST['merchant_business_id']

#         offer_list = OfferModel.objects.filter(merchant_business_id = merchant_business_id).order_by('-id')

#         offer_active_status = []
#         today = date.today()

#         if PromotionsAmount.objects.all():
#             data = PromotionsAmount.objects.latest('id')
#             offer_amount = data.offer_amount
#         else:
#             offer_amount = 0

#         for offer in offer_list:
#             if offer.offer_logo:
#                 logo = offer.offer_logo.url
#             else:
#                 logo = ""
#             if offer.valid_through < today:
#                 offer.expire_status=True
#                 available_status = False

#                 if not offer.customer_merchant_count:
#                     offer.customer_merchant_count= 0

#                 total_amount = float(offer_amount) * float(offer.customer_merchant_count)

#                 offer_active_status.append({
#                     'id': offer.id,
#                     'offer_name': offer.offer_name,
#                     'offer_caption': offer.offer_caption,
#                     'valid_from': datetime.strptime(str(offer.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                     'valid_through': datetime.strptime(str(offer.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                     'offer_image': offer.offer_image.url,
#                     'disapproved_reason': offer.disapproved_reason,
#                     'status': offer.status,
#                     'Offer_type': offer.Offer_type,
#                     'offer_business_category': offer.offer_business_category,
#                     'created_date': offer.created_date,
#                     'offer_panel': offer.offer_panel,
#                     'o_business_name': offer.o_business_name,
#                     'offer_logo': logo,
#                     'merchant_business_name': offer.merchant_business_name,
#                     'check_business_category': offer.check_business_category,
#                     'customer_city': offer.customer_city,
#                     'customer_state': offer.customer_state,
#                     'customer_area': offer.customer_area,
#                     'offer_amount': offer.offer_amount,
#                     'cout': offer.cout,
#                     # 'merchant_user': offer.merchant_user,
#                     # 'merchant_business_id': offer.merchant_business_id,
#                     'active_status': available_status,
#                     'total_users': offer.customer_merchant_count,
#                     'total_amount': total_amount,
#                     });
#             else:
#                 available_status = True

#                 if not offer.customer_merchant_count:
#                     offer.customer_merchant_count= 0

#                 total_amount = float(offer_amount) * float(offer.customer_merchant_count)

#                 offer_active_status.append({
#                     'id': offer.id,
#                     'offer_name': offer.offer_name,
#                     'offer_caption': offer.offer_caption,
#                     'valid_from': datetime.strptime(str(offer.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                     'valid_through': datetime.strptime(str(offer.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                     'offer_image': offer.offer_image.url,
#                     'disapproved_reason': offer.disapproved_reason,
#                     'status': offer.status,
#                     'Offer_type': offer.Offer_type,
#                     'offer_business_category': offer.offer_business_category,
#                     'created_date': offer.created_date,
#                     'offer_panel': offer.offer_panel,
#                     'o_business_name': offer.o_business_name,
#                     'offer_logo': logo,
#                     'merchant_business_name': offer.merchant_business_name,
#                     'check_business_category': offer.check_business_category,
#                     'customer_city': offer.customer_city,
#                     'customer_state': offer.customer_state,
#                     'customer_area': offer.customer_area,
#                     'offer_amount': offer.offer_amount,
#                     'cout': offer.cout,
#                     # 'merchant_user': offer.merchant_user,
#                     # 'merchant_business_id': offer.merchant_business_id,
#                     'active_status': available_status,
#                     'total_users': offer.customer_merchant_count,
#                     'total_amount': total_amount,
#                     });


#         for offer in offer_list:
#             offer.valid_from = datetime.strptime(str(offer.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y')
#             offer.valid_through = datetime.strptime(str(offer.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y')

#         serializer = MerchantOffersListSerializer(offer_list, many=True)

#         if offer_list:
#             return JsonResponse({'status': 'success', 'data' : offer_active_status}, status=200)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class MerchantDeleteOffersAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         offer_id = request.POST['offer_id']
#         result = OfferModel.objects.get(id=offer_id).delete()
#         if result:
#             return JsonResponse({"status": 'success'}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


    
# class CreatePaymentLink(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         mobile_no = request.POST['mobile_no']
#         name = request.POST['name']
#         email = request.POST['email']
#         amount = request.POST['amount']
#         description = request.POST['description']
#         send_sms = request.POST['send_sms']
#         m_business_id = request.POST['m_business_id']

#         subscription_object = getActiveTransactionalSubscriptionPlan(request, m_business_id)

#         if subscription_object:

#             if int(subscription_object.total_sms_avilable) >= int(1):

#                 try:
#                     payment_settings = MerchantPaymentSetting.objects.get(m_business_id = m_business_id)
#                 except:
#                     payment_settings = ""

#                 if payment_settings:

#                     result = PaymentLinks.objects.create(m_business_id = m_business_id, mobile_no = mobile_no, name = name, email = email, amount = amount, description = description)

#                     try:
#                         business_object = MerchantProfile.objects.get(id = m_business_id)
#                     except:
#                         business_object = ""
                   
#                     if result and send_sms:
#                         letters = string.ascii_letters
#                         digit = string.digits
#                         random_string = str(result.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

#                         PaymentLinks.objects.filter(id=result.id).update(payment_url = random_string)

#                         payment_url_temp = "http://157.230.228.250/payment-link/" + str(random_string) + "/"

#                         s = pyshorteners.Shortener()

#                         short_url = s.tinyurl.short(payment_url_temp)

#                         ts = int(time.time())

#                         data_temp = {
#                                 "keyword":"Payment Link",
#                                 "timeStamp":ts,
#                                 "dataSet":
#                                     [
#                                         {
#                                             "UNIQUE_ID":"GB-" + str(ts),
#                                             "MESSAGE":"Hey Green Bill user, " + business_object.m_business_name + " has shared payment link for " + "Rs. " + result.amount + ". Click link " + short_url + " to pay now.",
#                                             "OA":"GRBILL",
#                                             "MSISDN": str(result.mobile_no), # Recipient's Mobile Number
#                                             "CHANNEL":"SMS",
#                                             "CAMPAIGN_NAME":"hind_user",
#                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                             "USER_NAME":"hind_hsi",
#                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                             "DLT_CT_ID":"1007162209490097673", # Template Id
#                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                         }
#                                     ]
#                                 }

#                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                         response = requests.post(url, json = data_temp)

#                     if result:
#                         total_sms_avilable_new = 0
#                         total_sms_avilable_new = int(subscription_object.total_sms_avilable) - int(1)
#                         subscription_object.total_sms_avilable = total_sms_avilable_new
#                         subscription_object.save()
#                         return JsonResponse({'status': 'success'}, status=200)
#                     else:
#                         return JsonResponse({'status': 'error'}, status=400)
#                 else:
#                     return JsonResponse({'status': 'error','message':'To create a Payment link. Payment setting must be done, to change the payment setting please go to Web Panel Settings => Payment Setting from the sidebar.'}, status=400)
#             else:
#                 return JsonResponse({'status': 'error','message':'Insufficient Balance. Please purchase Transactional plan and try again !!!'}, status=400)
#         else:
#             return JsonResponse({'status': 'error','message':"You don't have active Transactional SMS plan. Please purchase and try again."}, status=400)

# class PaymentLinkList(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         m_business_id =  request.POST['m_business_id']
        
#         payment_link_list = PaymentLinks.objects.filter(m_business_id = m_business_id).order_by('-id')

#         payment_link = PaymentLinkListSerializer(payment_link_list, many=True)

#         if payment_link_list:
#             return JsonResponse({'status': 'success', 'data' : payment_link.data}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class PaymentLinkSend(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         payment_link_id = request.POST['payment_link_id']

#         try:
#             payment_link = PaymentLinks.objects.get(id = payment_link_id)
#         except:
#             payment_link = ""

#         try:
#             business_object = MerchantProfile.objects.get(id = payment_link.m_business_id)
#         except:
#             business_object = ""


#         try:
#             payment_settings = MerchantPaymentSetting.objects.get(m_business_id = payment_link.m_business_id)
#         except:
#             payment_settings = ""

#         m_business_id = payment_link.m_business_id

#         subscription_object = getActiveTransactionalSubscriptionPlan(request, m_business_id)

#         if subscription_object:

#             if int(subscription_object.total_sms_avilable) >= int(1):

#                 if payment_settings:

#                     if payment_link and business_object:
#                         letters = string.ascii_letters
#                         digit = string.digits
#                         random_string = str(payment_link.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

#                         PaymentLinks.objects.filter(id=payment_link.id).update(payment_url = random_string)

#                         payment_url_temp = "http://157.230.228.250/payment-link/" + str(random_string) + "/"

#                         s = pyshorteners.Shortener()

#                         short_url = s.tinyurl.short(payment_url_temp)

#                         ts = int(time.time())

#                         data_temp = {
#                                 "keyword":"Payment Link",
#                                 "timeStamp":ts,
#                                 "dataSet":
#                                     [
#                                         {
#                                             "UNIQUE_ID":"GB-" + str(ts),
#                                             "MESSAGE":"Hey Green Bill user, " + business_object.m_business_name + " has shared payment link for " + "Rs. " + payment_link.amount + ". Click link " + short_url + " to pay now.",
#                                             "OA":"GRBILL",
#                                             "MSISDN": str(payment_link.mobile_no), # Recipient's Mobile Number
#                                             "CHANNEL":"SMS",
#                                             "CAMPAIGN_NAME":"hind_user",
#                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                             "USER_NAME":"hind_hsi",
#                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                             "DLT_CT_ID":"1007162209490097673", # Template Id
#                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                         }
#                                     ]
#                                 }

#                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                         response = requests.post(url, json = data_temp)

#                         if response.status_code == 200:
#                             total_sms_avilable_new = 0
#                             total_sms_avilable_new = int(subscription_object.total_sms_avilable) - int(1)
#                             subscription_object.total_sms_avilable = total_sms_avilable_new
#                             subscription_object.save()
#                             return JsonResponse({'status': 'success'}, status=200)
#                         else:
#                             return JsonResponse({'status': 'error'}, status=400)
#                     else:
#                         return JsonResponse({'status': 'error'}, status=400)
#                 else:
#                     return JsonResponse({'status': 'error','message':'To Send a Payment link. Payment setting must be done, to change the payment setting please go to Web Panel Settings => Payment Setting from the sidebar.'}, status=400)
#             else:
#                 return JsonResponse({'status': 'error','message':'Insufficient Balance. Please purchase Transactional plan and try again !!!'}, status=400)
#         else:
#             return JsonResponse({'status': 'error','message':"You don't have active Transactional SMS plan. Please purchase and try again."}, status=400)

# class PaymentLinkDelete(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         payment_link_id = request.POST['payment_link_id']

#         try:
#             instance = PaymentLinks.objects.get(id=payment_link_id, payment_done = False)
#             result = instance.delete()
#         except:
#             result = ""

#         if result:
#             return JsonResponse({'status': 'success'}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class GetSubscriptionDetails(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         subscription_data = []

#         try:

#             business_id = m_business_id

#             startswith = str(business_id) + ','
#             endswith = ','+ str(business_id)
#             contains = ','+ str(business_id) + ','
#             exact = str(business_id)
                    
#             subscription_object = merchant_subscriptions.objects.get(
#                 Q(is_active = True),
#                 Q(business_ids__startswith = startswith) | 
#                 Q(business_ids__endswith = endswith) | 
#                 Q(business_ids__contains = contains) | 
#                 Q(business_ids__exact = exact)
#             )
#             if subscription_object.no_of_users:
#                 number_of_users = subscription_object.no_of_users
#             else:
#                 number_of_users = "0"


#             subscription_data.append({
#                 'per_bill_cost' : subscription_object.per_bill_cost,
#                 'per_receipt_cost': subscription_object.per_receipt_cost,
#                 'per_cash_memo_cost': subscription_object.per_cash_memo_cost,
#                 'per_digital_bill_cost': subscription_object.per_digital_bill_cost,
#                 'per_digital_receipt_cost': subscription_object.per_digital_receipt_cost,
#                 'per_digital_cash_memo_cost': subscription_object.per_digital_cash_memo_cost,
#                 'subscription_name': subscription_object.subscription_name,
#                 'purchase_date': datetime.strptime(str((subscription_object.purchase_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'purchase_cost': subscription_object.purchase_cost,
#                 'total_amount_avilable': subscription_object.total_amount_avilable,
#                 'expiry_date': subscription_object.expiry_date,
#                 'valid_for_month': subscription_object.valid_for_month,
#                 'number_of_users': number_of_users,
#             })

#             total_amount_avilable = subscription_object.total_amount_avilable

#         except:
#             subscription_data = []
#             total_amount_avilable = 0

#         promotional_sms_data = []

#         try:

#             business_id = m_business_id

#             startswith = str(business_id) + ','
#             endswith = ','+ str(business_id)
#             contains = ','+ str(business_id) + ','
#             exact = str(business_id)
                    
#             subscription_object = promotional_sms_subscriptions.objects.get(
#                 Q(is_active = True),
#                 Q(business_ids__startswith = startswith) | 
#                 Q(business_ids__endswith = endswith) | 
#                 Q(business_ids__contains = contains) | 
#                 Q(business_ids__exact = exact)
#             )

#             promotional_sms_data.append({
#                 'promotional_sms_subscription_name' : subscription_object.subscription_name,
#                 'promotional_sms_purchase_date': datetime.strptime(str((subscription_object.purchase_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'promotional_sms_purchase_cost': subscription_object.purchase_cost,
#                 'promotional_sms_total_sms': subscription_object.total_sms,
#                 'promotional_sms_per_sms_cost': subscription_object.per_sms_cost,
#                 'promotional_sms_total_sms_avilable': subscription_object.total_sms_avilable,
#             })

#             total_promotional_sms_avilable = int(subscription_object.total_sms_avilable)

#             if total_promotional_sms_avilable is None:
#                 total_promotional_sms_avilable = 0

#         except:
#             bulk_sms_data = []
#             total_promotional_sms_avilable = 0

#         transactional_sms_data = []

#         try:

#             business_id = m_business_id

#             startswith = str(business_id) + ','
#             endswith = ','+ str(business_id)
#             contains = ','+ str(business_id) + ','
#             exact = str(business_id)
                    
#             subscription_object = transactional_sms_subscriptions.objects.get(
#                 Q(is_active = True),
#                 Q(business_ids__startswith = startswith) | 
#                 Q(business_ids__endswith = endswith) | 
#                 Q(business_ids__contains = contains) | 
#                 Q(business_ids__exact = exact)
#             )

#             transactional_sms_data.append({
#                 'transactional_sms_subscription_name' : subscription_object.subscription_name,
#                 'transactional_sms_purchase_date': datetime.strptime(str((subscription_object.purchase_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'transactional_sms_purchase_cost': subscription_object.purchase_cost,
#                 'transactional_sms_total_sms': subscription_object.total_sms,
#                 'transactional_sms_per_sms_cost': subscription_object.per_sms_cost,
#                 'transactional_sms_total_sms_avilable': subscription_object.total_sms_avilable,
#             })

#             total_transactional_sms_avilable = int(subscription_object.total_sms_avilable)

#             if total_transactional_sms_avilable is None:
#                 total_transactional_sms_avilable = 0

#         except:
#             bulk_sms_data = []
#             total_transactional_sms_avilable = 0


#         add_on_recharge_data = []

#         try:

#             business_id = m_business_id

#             startswith = str(business_id) + ','
#             endswith = ','+ str(business_id)
#             contains = ','+ str(business_id) + ','
#             exact = str(business_id)
                    
#             ad_ons_object = recharge_history.objects.get(
#                 Q(is_add_on_plan = True),
#                 Q(business_ids__startswith = startswith) | 
#                 Q(business_ids__endswith = endswith) | 
#                 Q(business_ids__contains = contains) | 
#                 Q(business_ids__exact = exact)
#             )

#             add_on_recharge_data.append({
#                 'per_bill_cost' : ad_ons_object.per_bill_cost,
#                 'per_receipt_cost': ad_ons_object.per_receipt_cost,
#                 'per_cash_memo_cost': ad_ons_object.per_cash_memo_cost,
#                 'per_digital_bill_cost': ad_ons_object.per_digital_bill_cost,
#                 'per_digital_receipt_cost': ad_ons_object.per_digital_receipt_cost,
#                 'per_digital_cash_memo_cost': ad_ons_object.per_digital_cash_memo_cost,
#                 'subscription_name': ad_ons_object.subscription_name,
#                 'purchase_date': datetime.strptime(str((ad_ons_object.purchase_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'cost': ad_ons_object.cost,
#                 # 'total_amount_avilable': ad_ons_object.total_amount_avilable,
#                 'expiry_date': ad_ons_object.expiry_date
#             })

#             # total_amount_avilable = subscription_object.total_amount_avilable

#         except:
#             add_on_recharge_data = []
#             # total_amount_avilable = 0


#         if m_business_id:
#             return JsonResponse({'status': 'success', 'total_amount_avilable': total_amount_avilable, 'total_promotional_sms_avilable': total_promotional_sms_avilable,
#                 'total_transactional_sms_avilable': total_transactional_sms_avilable, 'subscription_data' : subscription_data, 
#                 'promotional_sms_data': promotional_sms_data, 'transactional_sms_data': transactional_sms_data, 'add_on_recharge_data': add_on_recharge_data}, status=200)
#         else:
#             return JsonResponse({'status' : "error"}, status=400)


# class GetSubscriptionHistory(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         business_id = m_business_id

#         startswith = str(business_id) + ','
#         endswith = ','+ str(business_id)
#         contains = ','+ str(business_id) + ','
#         exact = str(business_id)
                
#         recharge_his = recharge_history.objects.filter(
#             Q(business_ids__startswith = startswith) | 
#             Q(business_ids__endswith = endswith) | 
#             Q(business_ids__contains = contains) | 
#             Q(business_ids__exact = exact)
#         ).order_by('-id')

#         recharge_history_new = []

#         for recharge in recharge_his:
#             recharge.purchase_date = datetime.strptime(str((recharge.purchase_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y')
#             recharge.subscription_bill_url = "http://157.230.228.250/my-subscription-bill/"+ str(recharge.id) + str("/")

#             recharge_history_new.append({
#                 "id": recharge.id,
#                 "subscription_plan_id": recharge.subscription_plan_id,
#                 "subscription_name": recharge.subscription_name,
#                 "business_ids": recharge.business_ids,
#                 "valid_for_month": recharge.valid_for_month,
#                 "per_bill_cost": recharge.per_bill_cost,
#                 "per_receipt_cost": recharge.per_receipt_cost,
#                 "per_cash_memo_cost": recharge.per_cash_memo_cost,
#                 "per_digital_bill_cost": recharge.per_digital_bill_cost,
#                 "per_digital_receipt_cost": recharge.per_digital_receipt_cost,
#                 "per_digital_cash_memo_cost": recharge.per_digital_cash_memo_cost,
#                 "total_sms": recharge.total_sms,
#                 "per_sms_cost": recharge.per_sms_cost,
#                 "is_subscription_plan": recharge.is_subscription_plan,
#                 "is_promotional_sms_plan": recharge.is_promotional_sms_plan,
#                 "is_transactional_sms_plan": recharge.is_transactional_sms_plan,
#                 "is_add_on_plan": recharge.is_add_on_plan,
#                 "cost": recharge.cost,
#                 "purchase_date": recharge.purchase_date,
#                 "expiry_date": recharge.expiry_date,
#                 "transaction_id": recharge.transaction_id,
#                 "payu_transaction_id": recharge.payu_transaction_id,
#                 "invoice_no": recharge.invoice_no,
#                 "mode": recharge.mode,
#                 "cheque_no": recharge.cheque_no,
#                 "bank_transaction_id": recharge.cheque_no,
#                 "merchant_id": recharge.merchant_id.id,
#                 "subscription_bill_url": recharge.subscription_bill_url,
#             })

#         # recharge_history_new = RechargeHistorySerializer(recharge_his, many=True)

#         if recharge_history_new:
#             return JsonResponse({'status': 'success', 'data' : recharge_history_new}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class GetSubscriptionPlans(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user_id = request.POST['user_id']
#         business_category_id = request.POST['business_category_id']
#         m_business_id = request.POST['m_business_id']
#         result = []
#         plans = subscription_plan_details.objects.filter(is_active = True).order_by('-id').distinct()

#         merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

#         merchant_object = GreenBillUser.objects.get(id=merchant_id)

      
#         business_object = MerchantProfile.objects.get(id=m_business_id)
#         merchant_state = business_object.m_state

#         if merchant_state == "Maharashtra" or merchant_state == "maharashtra":

#             sgst = 9
#             cgst = 9
#             igst = 1

#         else:
#             igst = 18
#             sgst = 1
#             cgst = 1
#         subscriptions_list = []

#         for plan in plans:
#             if plan.user_type != "partner":
#                 total_cost = plan.subscription_plan_cost
#                 plan.including_gst = float(total_cost) - float(plan.gst_amount)
#                 # if plan.business_category == business_category_id:
#                 if plan.customized_plan_for == "merchant":

#                     merchant_name_list = list(plan.merchant_name.split(","))

#                     if str(m_business_id) in merchant_name_list:

#                         if plan not in subscriptions_list:

#                             subscriptions_list.append(plan) 

#                             result.append({
#                                 "id":plan.id,
#                                 "subscription_name":plan.subscription_name,
#                                 "valid_for_month":plan.valid_for_month,
#                                 "per_bill_cost":plan.per_bill_cost,
#                                 "per_receipt_cost":plan.per_receipt_cost,
#                                 "per_cash_memo_cost":plan.per_cash_memo_cost,
#                                 "per_digital_bill_cost":plan.per_digital_bill_cost,
#                                 "per_digital_receipt_cost":plan.per_digital_receipt_cost,
#                                 "per_digital_cash_memo_cost":plan.per_digital_cash_memo_cost,
#                                 "software_maintainace_cost":plan.software_maintainace_cost,
#                                 "recharge_amount":plan.recharge_amount,
#                                 "discount_in":plan.discount_in,
#                                 "discount_percentage":plan.discount_percentage,
#                                 "discount_amount":plan.discount_amount,
#                                 "user_type":plan.user_type,
#                                 "total_amount": format(float(plan.subscription_plan_cost), ".2f"),
#                                 "subscription_plan_cost":plan.including_gst,
#                                 "business_category":plan.business_category,
#                                 "merchant_name":plan.merchant_name,
#                                 "customized_plan_for":plan.customized_plan_for,
#                                 "customized_plan":plan.customized_plan,
#                                 "suited_for":plan.suited_for,
#                                 "created_date":plan.created_date,
#                                 "is_active":plan.is_active,
#                                 "is_offer":plan.is_offer,
#                                 "number_of_users":plan.number_of_users,
#                                 "cost_for_users":plan.cost_for_users,
#                                 "gst_amount":plan.gst_amount,
#                                 "sgst_value" : sgst,
#                                 "cgst_value" : cgst,
#                                 "igst_value" : igst,

#                             }) 

#                 elif plan.customized_plan_for ==  "business_category":

#                     category_list = list(plan.business_category.split(","))

#                     if str(business_category_id) in category_list:

#                         if plan not in subscriptions_list:

#                             subscriptions_list.append(plan) 

#                             result.append({
#                                 "id":plan.id,
#                                 "subscription_name":plan.subscription_name,
#                                 "valid_for_month":plan.valid_for_month,
#                                 "per_bill_cost":plan.per_bill_cost,
#                                 "per_receipt_cost":plan.per_receipt_cost,
#                                 "per_cash_memo_cost":plan.per_cash_memo_cost,
#                                 "per_digital_bill_cost":plan.per_digital_bill_cost,
#                                 "per_digital_receipt_cost":plan.per_digital_receipt_cost,
#                                 "per_digital_cash_memo_cost":plan.per_digital_cash_memo_cost,
#                                 "software_maintainace_cost":plan.software_maintainace_cost,
#                                 "recharge_amount":plan.recharge_amount,
#                                 "discount_in":plan.discount_in,
#                                 "discount_percentage":plan.discount_percentage,
#                                 "discount_amount":plan.discount_amount,
#                                 "user_type":plan.user_type,
#                                 "total_amount": format(float(plan.subscription_plan_cost), ".2f"),
#                                 "subscription_plan_cost":plan.including_gst,
#                                 "business_category":plan.business_category,
#                                 "merchant_name":plan.merchant_name,
#                                 "customized_plan_for":plan.customized_plan_for,
#                                 "customized_plan":plan.customized_plan,
#                                 "suited_for":plan.suited_for,
#                                 "created_date":plan.created_date,
#                                 "is_active":plan.is_active,
#                                 "is_offer":plan.is_offer,
#                                 "number_of_users":plan.number_of_users,
#                                 "cost_for_users":plan.cost_for_users,
#                                 "gst_amount":plan.gst_amount,
#                                 "sgst_value" : sgst,
#                                 "cgst_value" : cgst,
#                                 "igst_value" : igst,

#                             })
#                 else:
#                     if business_category_id != "11" and business_category_id != "12":
#                         result.append({
#                             "id":plan.id,
#                             "subscription_name":plan.subscription_name,
#                             "valid_for_month":plan.valid_for_month,
#                             "per_bill_cost":plan.per_bill_cost,
#                             "per_receipt_cost":plan.per_receipt_cost,
#                             "per_cash_memo_cost":plan.per_cash_memo_cost,
#                             "per_digital_bill_cost":plan.per_digital_bill_cost,
#                             "per_digital_receipt_cost":plan.per_digital_receipt_cost,
#                             "per_digital_cash_memo_cost":plan.per_digital_cash_memo_cost,
#                             "software_maintainace_cost":plan.software_maintainace_cost,
#                             "recharge_amount":plan.recharge_amount,
#                             "discount_in":plan.discount_in,
#                             "discount_percentage":plan.discount_percentage,
#                             "discount_amount":plan.discount_amount,
#                             "user_type":plan.user_type,
#                             "total_amount": format(float(plan.subscription_plan_cost), ".2f"),
#                             "subscription_plan_cost":plan.including_gst,
#                             "business_category":plan.business_category,
#                             "merchant_name":plan.merchant_name,
#                             "customized_plan_for":plan.customized_plan_for,
#                             "customized_plan":plan.customized_plan,
#                             "suited_for":plan.suited_for,
#                             "created_date":plan.created_date,
#                             "is_active":plan.is_active,
#                             "is_offer":plan.is_offer,
#                             "number_of_users":plan.number_of_users,
#                             "cost_for_users":plan.cost_for_users,
#                             "gst_amount":plan.gst_amount,
#                             "sgst_value" : sgst,
#                             "cgst_value" : cgst,
#                             "igst_value" : igst,

#                         }) 

 
        
#         # plans_new = SubscriptionPlanSerializer(plans, many=True)

#         if result:
#             return JsonResponse({'status': 'success', 'data' : result}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class GetPromotionalSMSSubscription(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user_id = request.POST['user_id']
#         business_id = request.POST['business_id']
#         merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

#         # merchant_object = GreenBillUser.objects.get(id=merchant_id)
      
#         business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)
#         all_business = MerchantProfile.objects.get(id=business_id)

#         merchant_state = all_business.m_state

#         if merchant_state == "Maharashtra" or merchant_state == "maharashtra":

#             sgst = 9
#             cgst = 9
#             igst = 1

#         else:
#             igst = 18
#             sgst = 1
#             cgst = 1

#         plans = promotional_subscription_plan_model.objects.filter(is_active = True).order_by('-id')

#         plans_new = []

        
#         for plan in plans:

#             gst_amount = plan.gst_amount
#             toal_cost = plan.total_sms_cost
#             plan.total_amount_with_gst = float(toal_cost) - float(gst_amount)
#             if all_business.m_business_category.id !=11 and all_business.m_business_category.id != 12:
#                 plans_new.append({
#                     "id":plan.id,
#                     "subscription_name":plan.subscription_name,
#                     "total_sms":plan.total_sms,
#                     "per_sms_cost":plan.per_sms_cost,
#                     "total_sms_cost":plan.total_amount_with_gst,
#                     "total_amount":plan.total_sms_cost,
#                     "discount_in":plan.discount_in,
#                     "discount_percentage":plan.discount_percentage,
#                     "discount_amount":plan.discount_amount,
#                     "created_date":plan.created_date,
#                     "is_active":plan.is_active,
#                     "total_sms_avilable":plan.total_sms_avilable,
#                     "gst_amount":plan.gst_amount,
#                     "sgst_value" : sgst,
#                     "cgst_value" : cgst,
#                     "igst_value" : igst,

#                     })


#         if plans_new:
#             return JsonResponse({'status': 'success', 'data' : plans_new}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)



        

# class GetTransactionalSMSSubscription(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user_id = request.POST['user_id']
#         business_id = request.POST['business_id'] 
        
#         merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

#         merchant_object = GreenBillUser.objects.get(id=merchant_id)

      
#         business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)
#         all_business = MerchantProfile.objects.get(id = business_id)


#         # all_business = MerchantProfile.objects.filter(m_user=merchant_id , m_active_account = True)

#         merchant_state = business_object.m_state

#         if merchant_state == "Maharashtra" or merchant_state == "maharashtra":

#             sgst = 9
#             cgst = 9
#             igst = 1

#         else:
#             igst = 18
#             sgst = 1
#             cgst = 1

#         plans = transactional_subscription_plan_model.objects.filter(is_active = True).order_by('-id')

#         plans_new = []

#         for plan in plans:
#             gst_amount = plan.gst_amount
#             total_cost = plan.total_sms_cost
#             plan.total_cost_with_gst = float(total_cost) - float(gst_amount)
#             if all_business.m_business_category.id !=11 and all_business.m_business_category.id != 12:
#                 plans_new.append({
#                     "id":plan.id,
#                     "subscription_name":plan.subscription_name,
#                     "total_sms":plan.total_sms,
#                     "per_sms_cost":plan.per_sms_cost,
#                     "total_sms_cost":plan.total_cost_with_gst,
#                     "total_amount":plan.total_sms_cost,
#                     "discount_in":plan.discount_in,
#                     "discount_percentage":plan.discount_percentage,
#                     "discount_amount":plan.discount_amount,
#                     "created_date":plan.created_date,
#                     "is_active":plan.is_active,
#                     "total_sms_avilable":plan.total_sms_avilable,
#                     "gst_amount":plan.gst_amount,
#                     "sgst_value" : sgst,
#                     "cgst_value" : cgst,
#                     "igst_value" : igst,
#                     }) 



#         # plans_new = TransactionalSMSSubscriptionPlanSerializer(plans, many=True)

#         if plans_new:
#             return JsonResponse({'status': 'success', 'data' : plans_new}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class GetAddOnRecharge(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user_id = request.POST['user_id']
    
#         business_id = request.POST['business_id'] 

#         merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

#         merchant_object = GreenBillUser.objects.get(id=merchant_id)

#         business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)

#         # all_business = MerchantProfile.objects.filter(m_user=merchant_id , m_active_account = True)
#         all_business = MerchantProfile.objects.get(id = business_id)

#         merchant_state = all_business.m_state

#         if merchant_state == "Maharashtra" or merchant_state == "maharashtra":

#             sgst = 9
#             cgst = 9
#             igst = 1

#         else:
#             igst = 18
#             sgst = 1
#             cgst = 1


#         addons_plans = add_on_plan_model.objects.all().filter(is_active=True).order_by('-id')
#         # subscription_object = ""
#         # for business in all_business:
#         #     business_id = business.id
#         #     startswith = str(business_id) + ','
#         #     endswith = ','+ str(business_id)
#         #     contains = ','+ str(business_id) + ','
#         #     exact = str(business_id)

#         #     try:  
#         #         subscription_object = merchant_subscriptions.objects.get(
#         #             Q(merchant_id = merchant_object),
#         #             Q(is_active = True),
#         #             Q(business_ids__startswith = startswith) | 
#         #             Q(business_ids__endswith = endswith) | 
#         #             Q(business_ids__contains = contains) | 
#         #             Q(business_ids__exact = exact)
#         #         )
#         #     except:
#         #         subscription_object = ""


#         plans_new = []
#         for plan in addons_plans:
#             adon_gst_amount = plan.gst_amount
#             total_adon_cost = plan.recharge_amount
#             plan.total_adon_cost_with_gst = float(total_adon_cost) - float(adon_gst_amount)
        
#             plans_new.append({
#                 "id":plan.id,
#                 "add_on_name":plan.add_on_name,
#                 "per_bill_cost":plan.per_bill_cost,
#                 "per_receipt_cost":plan.per_receipt_cost,
#                 "per_cash_memo_cost":plan.per_cash_memo_cost,
#                 "per_digital_bill_cost":plan.per_digital_bill_cost,
#                 "per_digital_receipt_cost":plan.per_digital_receipt_cost,
#                 "per_digital_cash_memo_cost":plan.per_digital_cash_memo_cost,
#                 "recharge_amount":plan.total_adon_cost_with_gst,
#                 "total_amount":plan.recharge_amount,
#                 "created_date":plan.created_date,
#                 "is_active":plan.is_active,
#                 "gst_amount":plan.gst_amount,
#                 "sgst_value" : sgst,
#                 "cgst_value" : cgst,
#                 "igst_value" : igst,
#                 })

#         if plans_new:
#             return JsonResponse({'status': 'success', 'data' : plans_new}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class GetAddOnAmounts(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         plan_id = request.POST['plan_id']

#         try:
#             addons_plans = add_on_plan_model.objects.get(id=plan_id)
#         # print('addons_plans',addons_plans)
#             list1 = []

#             filtered_amount_list = []

#             if addons_plans.recharge_amount_one:
#                 if addons_plans.recharge_amount_one not in list1:
#                     if addons_plans.recharge_amount_one != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_one
#                         })

#             if addons_plans.recharge_amount_two:
#                 if addons_plans.recharge_amount_two not in list1:
#                     if addons_plans.recharge_amount_two != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_two
#                         })

#             if addons_plans.recharge_amount_three: 
#                 if addons_plans.recharge_amount_three not in list1:
#                     if addons_plans.recharge_amount_three != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_three
#                         })

#             if addons_plans.recharge_amount_four:
#                 if addons_plans.recharge_amount_four not in list1:
#                     if addons_plans.recharge_amount_four != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_four
#                         })

#             if addons_plans.recharge_amount_five:
#                 if addons_plans.recharge_amount_five not in list1:
#                     if addons_plans.recharge_amount_five != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_five
#                         })

#             if addons_plans.recharge_amount_six:
#                 if addons_plans.recharge_amount_six not in list1:
#                     if addons_plans.recharge_amount_six != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_six
#                         })

#             if addons_plans.recharge_amount_seven:
#                 if addons_plans.recharge_amount_seven not in list1:
#                     if addons_plans.recharge_amount_seven != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_seven
#                         })

#             if addons_plans.recharge_amount_eight:
#                 if addons_plans.recharge_amount_eight not in list1:
#                     if addons_plans.recharge_amount_eight != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_eight
#                         })

#             if addons_plans.recharge_amount_nine:
#                 if addons_plans.recharge_amount_nine not in list1:
#                     if addons_plans.recharge_amount_nine != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_nine
#                         })

#             if addons_plans.recharge_amount_ten:
#                 if addons_plans.recharge_amount_ten not in list1:
#                     if addons_plans.recharge_amount_ten != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_ten
#                         })

#             if addons_plans.recharge_amount_eleven:
#                 if addons_plans.recharge_amount_eleven not in list1:
#                     if addons_plans.recharge_amount_eleven != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_eleven
#                         })

#             if addons_plans.recharge_amount_twelve:
#                 if addons_plans.recharge_amount_twelve not in list1:
#                     if addons_plans.recharge_amount_twelve != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_twelve
#                         })

#             if addons_plans.recharge_amount_thirteen:
#                 if addons_plans.recharge_amount_thirteen not in list1:
#                     if addons_plans.recharge_amount_thirteen != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_thirteen
#                         })

#             if addons_plans.recharge_amount_fourteen:
#                 if addons_plans.recharge_amount_fourteen not in list1:
#                     if addons_plans.recharge_amount_fourteen != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_fourteen
#                         })

#             if addons_plans.recharge_amount_fifteen:
#                 if addons_plans.recharge_amount_fifteen not in list1:
#                     if addons_plans.recharge_amount_fifteen != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_fifteen
#                         })

#             if addons_plans.recharge_amount_sixteen:
#                 if addons_plans.recharge_amount_sixteen not in list1:
#                     if addons_plans.recharge_amount_sixteen != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_sixteen
#                         })

#             if addons_plans.recharge_amount_seventeen:
#                 if addons_plans.recharge_amount_seventeen not in list1:
#                     if addons_plans.recharge_amount_seventeen != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_seventeen
#                         })

#             if addons_plans.recharge_amount_eighteen:
#                 if addons_plans.recharge_amount_eighteen not in list1:
#                     if addons_plans.recharge_amount_eighteen != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_eighteen
#                         })

#             if addons_plans.recharge_amount_nineteen:
#                 if addons_plans.recharge_amount_nineteen not in list1:
#                     if addons_plans.recharge_amount_nineteen != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_nineteen
#                         })

#             if addons_plans.recharge_amount_twenty:
#                 if addons_plans.recharge_amount_twenty not in list1:
#                     if addons_plans.recharge_amount_twenty != '':
#                         list1.append({
#                             "all_recharge_amount": addons_plans.recharge_amount_twenty
#                         })

#             result = True
#         except:
#             result = False


#         if result:
#             return JsonResponse(list1, status=200, safe=False)
#             # return JsonResponse(serializer.data, status=200, safe=False)
#         else:
#             return JsonResponse({'status': "error"}, status=400)


# class GetRechargeHistoryDetails(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         user_id = request.POST['user_id']

#         m_business_id = request.POST['m_business_id']

#         merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

#         merchant_object = GreenBillUser.objects.get(id=merchant_id)

#         startswith = str(m_business_id) + ','
#         endswith = ','+ str(m_business_id)
#         contains = ','+ str(m_business_id) + ','
#         exact = str(m_business_id)

#         recharge_his = recharge_history.objects.filter(
#             Q(merchant_id = merchant_object),
#             Q(business_ids__startswith = startswith) | 
#             Q(business_ids__endswith = endswith) | 
#             Q(business_ids__contains = contains) | 
#             Q(business_ids__exact = exact)
#         ).order_by('-id')

#         result = []

#         for recharge in recharge_his:

#             if recharge.is_subscription_plan == True:
#                 try:
#                     subscription = subscription_plan_details.objects.get(id=recharge.subscription_plan_id)
#                     subscription_type = "Green Bill Subscription"
                        
#                     users_cost = float(recharge.no_of_users) * float(recharge.valid_for_month) * float(subscription.cost_for_users)
#                     final_amount = float(users_cost) + float(recharge.cost) + float(recharge.gst_amount)
#                 except:
#                     final_amount = 0
                    

#             # elif recharge.is_add_on_plan == True: 
#             #     final_amount = float(recharge.cost) + float(recharge.gst_amount) 

#             # if recharge.is_subscription_plan == True:

#             #     subscription_type = "Green Bill Subscription"

#             #     subscription_plan = subscription_plan_details.objects.filter(id=recharge.subscription_plan_id)

#             #     for subscription in subscription_plan:

#             #         try:
#             #             users_cost = float(recharge.no_of_users) * float(recharge.valid_for_month) * float(subscription.cost_for_users)
#             #             final_amount = float(users_cost) + float(recharge.cost) + float(recharge.gst_amount)
#             #         except:
#             #             final_amount = 0

#             elif recharge.is_promotional_sms_plan == True:

#                 subscription_type = "Promotional SMS Plan"

#                 final_amount = recharge.cost

#             elif recharge.is_transactional_sms_plan == True:

#                 subscription_type = "Transactional SMS Plan"

#                 final_amount = recharge.cost

#             elif recharge.is_add_on_plan == True:

#                 subscription_type = "Add On's Plan"

#                 final_amount = float(recharge.cost) + float(recharge.gst_amount) 

#             if recharge.transaction_id:
#                 transaction_id = recharge.transaction_id
#             else: 
#                 transaction_id = ""

#             if recharge.mode:
#                 recharge_mode = recharge.mode
#                 if recharge.mode == 'bank':
#                     recharge_mode_id = recharge.bank_transaction_id
#                 elif recharge.mode == 'cheque':
#                     recharge_mode_id = recharge.cheque_no
#                 else:
#                     recharge_mode_id = ""
#             else:
#                 recharge_mode_id = ""
#                 recharge_mode = "PayU"
                


#             purchase_date = timezone.localtime(recharge.purchase_date).strftime("%Y-%m-%d")

#             result.append({
#                 'bill_id': recharge.id,
#                 'date': datetime.strptime(str(purchase_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'subscription_type': subscription_type,
#                 'recharge_mode': recharge_mode,
#                 "recharge_mode_id": recharge_mode_id,
#                 'transaction_id': transaction_id,
#                 'amount': str(final_amount),
#                 'business': 'Green Bill',
#                 'url': "http://157.230.228.250/my-subscription-bill/" + str(recharge.id) + "/"
                
#             })

#         if result:
#             return JsonResponse({'status': "success", "result":result}, status=200)

#         else:
#             return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)


# class GetReceivedBill(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         m_business_id = request.POST['m_business_id']

#         from_date = request.POST.get('from_date')

#         to_date = request.POST.get('to_date')

#         merchant_objects = MerchantProfile.objects.get(id = m_business_id).m_user

#         all_bills = MerchantBill.objects.filter(bill_received_business_name = m_business_id).order_by("-id")

#         bills_new = []

#         for bill in all_bills:
#             try:
#                 business_id = bill.business_name.id
#                 business_name = bill.business_name.m_business_name
#             except:
#                 business_name = ""

#             bill_url = "http://157.230.228.250/my-bill-merchant/" + str(bill.bill_url) + "/"

#             bills_new.append({
#                 "bill_id":bill.id,
#                 "invoice_no": bill.invoice_no,
#                 "bill_amount": str(bill.bill_amount),
#                 "bill_date": datetime.strptime(str((bill.bill_date)), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 "business_name": business_name,
#                 "bill_url" : bill_url,
#                 "bill_image" : bill.bill.url,
#                 'created_at': str(bill.created_at),
#             })

#         startswith = str(m_business_id) + ','
#         endswith = ','+ str(m_business_id)
#         contains = ','+ str(m_business_id) + ','
#         exact = str(m_business_id)

#         recharge_his = recharge_history.objects.filter(
#             Q(merchant_id = merchant_objects),
#             Q(business_ids__startswith = startswith) | 
#             Q(business_ids__endswith = endswith) | 
#             Q(business_ids__contains = contains) | 
#             Q(business_ids__exact = exact)
#         ).order_by('-id')

#         for recharge in recharge_his:
#             if recharge.is_subscription_plan == True:
#                 subscription_plan = subscription_plan_details.objects.filter(id=recharge.subscription_plan_id)
                
#                 for subscription in subscription_plan:

#                     try:
#                         users_cost = float(recharge.no_of_users) * float(recharge.valid_for_month) * float(subscription.cost_for_users)
#                         final_amount = float(users_cost) + float(recharge.cost) + float(recharge.gst_amount)
#                     except:
#                         final_amount = 0
#             else:
#                 final_amount = recharge.cost


#             purchase_date = timezone.localtime(recharge.purchase_date).strftime("%Y-%m-%d")
#             try:
#                 bills_new.append({
#                     'bill_id': recharge.id,
#                     'invoice_no': recharge.invoice_no,
#                     'bill_amount': str(final_amount),
#                     'bill_date': datetime.strptime(str(purchase_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                     'business_name': 'Green Bill',
#                     "bill_url" : "http://157.230.228.250/my-subscription-bill/"+ str(recharge.id) + str("/"),
#                     "bill_image" : "",
#                     'created_at': str(recharge.purchase_date),
#                 })
#             except:
#                 pass

#         # bills_new.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)
#         bills_new.sort(key = lambda x: x['created_at'], reverse = True)

        

#         new_data = []

#         if from_date and to_date:

#             if bills_new:
#                 if from_date:
#                     from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')
                    
#                 if to_date:
#                     to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')
                    
#                 for bill in bills_new:
                    
#                     if from_date and to_date:
#                         bill_date = datetime.strptime(str(bill['bill_date']), '%d-%m-%Y').strftime('%Y-%m-%d')

#                         if bill_date >= from_date and bill_date <= to_date:
#                             new_data.append(bill)
  
#             # new_data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)
#             new_data.sort(key = lambda x: x['created_at'], reverse = True)

#             received_amount = 0
#             received_bills = 0

#             # for z in new_data:
#             #     received_amount =  float(received_amount) + float(z['amount'])
#             #     received_bills = len(new_data)

#             if new_data:
#                 return JsonResponse({'status': "success", "data":new_data, 
#                      "from_date": from_date, "to_date": to_date}, status=200)
#             else:
#                 return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)
#         else:

#             if bills_new:
#                 return JsonResponse({'status': 'success', 'data' : bills_new,
#                     "from_date":"", "to_date":""}, status=200)
#             else:
#                 return JsonResponse({'status': 'error'}, status=400)


# class SendReceivedBill(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         bill_id = request.POST["bill_id"]
#         business_id = request.POST["business_id"]
#         if business_id == 'customer':
#             merchant_bill = MerchantBill.objects.filter(id = bill_id)

#             letters = string.ascii_letters
#             digit = string.digits
#             random_string = str(merchant_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

#             customer_bill = CustomerBill.objects.create(user_id = merchant_bill[0].user_id, mobile_no = merchant_bill[0].mobile_no,
#                 email = merchant_bill[0].email, bill = merchant_bill[0].bill, business_name = merchant_bill[0].business_name,
#                 invoice_no = merchant_bill[0].invoice_no, green_bill_transaction = merchant_bill[0].green_bill_transaction, green_bill_print_transaction = merchant_bill[0].green_bill_print_transaction,
#                 print_transaction = merchant_bill[0].print_transaction, bill_amount = merchant_bill[0].bill_amount, customer_bill_category = merchant_bill[0].customer_bill_category,stamp_id=merchant_bill[0].stamp_id, exe_bill_type = merchant_bill[0].exe_bill_type
#             )

#             history_result1 = sent_bill_history.objects.create(user_id = merchant_bill[0].user_id,
#                 mobile_no = merchant_bill[0].mobile_no, m_business_id = merchant_bill[0].business_name.id, green_bill_print_transaction = merchant_bill[0].green_bill_print_transaction,
#                 print_transaction = merchant_bill[0].print_transaction, bill_amount = merchant_bill[0].bill_amount,
#                 customer_bill = True
#             )

#             customer_bill_new = CustomerBill.objects.filter(id=customer_bill.id).update(bill_url = random_string) 

#             MerchantBill.objects.filter(id =bill_id).delete()

#             if customer_bill:
#                 return JsonResponse({'status': 'success', 'message' : 'Bill Transfer successfully !!!'}, status=200)
#             else:
#                 return JsonResponse({'status': 'error','message' : 'Failed to Transfer!!!'}, status=400)
#         else:

#             merchant_bill = MerchantBill.objects.filter(id =bill_id)

#             letters = string.ascii_letters
#             digit = string.digits
#             random_string = str(merchant_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

#             merchant_bill1 = MerchantBill.objects.create(user_id = merchant_bill[0].user_id, mobile_no = merchant_bill[0].mobile_no, email = merchant_bill[0].email,
#                 bill = merchant_bill[0].bill, business_name = merchant_bill[0].business_name, bill_received_business_name = business_id,
#                 invoice_no = merchant_bill[0].invoice_no, green_bill_transaction = merchant_bill[0].green_bill_transaction, green_bill_print_transaction = merchant_bill[0].green_bill_print_transaction,
#                 print_transaction = merchant_bill[0].print_transaction, bill_amount = merchant_bill[0].bill_amount, customer_bill_category = merchant_bill[0].customer_bill_category,stamp_id=merchant_bill[0].stamp_id, exe_bill_type = merchant_bill[0].exe_bill_type
#             )

#             merchant_bill_new = MerchantBill.objects.filter(id=merchant_bill1.id).update(bill_url = random_string) 

#             merchant_bill = MerchantBill.objects.filter(id =bill_id).delete()

#             if merchant_bill1:
#                 return JsonResponse({'status': 'success', 'message' : 'Bill Transfer successfully !!!'}, status=200)
#             else:
#                 return JsonResponse({'status': 'error','message' : 'Failed to Transfer!!!'}, status=400)
       



# class GetRejectedBill(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         merchant_business_id = request.POST['merchant_business_id']

#         from_date = request.POST.get('from_date')

#         to_date = request.POST.get('to_date')

#         base_url = "http://157.230.228.250/"

#         data = []

#         parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, reject_status = True).order_by('-id')
        
#         for bill in parking_bill_list:
#             try:
#                 bill_file = str(base_url) + str(bill.bill_file.url)
#             except:
#                 bill_file = ""

#             if bill.is_checkoutpin == True:
#                 try:
#                     mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
#                 except:
#                     mobile_no = bill.mobile_no
#             else:
#                 mobile_no = bill.mobile_no

#             data.append({
#                 'bill_id': bill.id,
#                 'invoice_no': bill.invoice_no,
#                 'mobile_no': mobile_no,
#                 'amount': str(bill.amount),
#                 'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
#                 'bill_file': bill_file,
#                 'db_table': "SaveParkingLotBill",
#                 'customer_added': False,
#                 'reject_status':bill.reject_status,
#             })
               

#         petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, reject_status = True).order_by('-id')
        
#         for bill in petrol_bill_list:
#             try:
#                 bill_file = str(base_url) + str(bill.bill_file.url)
#             except:
#                 bill_file = ""

#             if bill.is_checkoutpin == True:
#                 try:
#                     mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
#                 except:
#                     mobile_no = bill.mobile_no
#             else:
#                 mobile_no = bill.mobile_no
                
#             data.append({
#                 'bill_id': bill.id,
#                 'invoice_no': bill.invoice_no,
#                 'mobile_no': mobile_no,
#                 'amount': str(bill.total_amount),
#                 'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
#                 'bill_file': bill_file,
#                 'db_table': "SavePetrolPumpBill",
#                 'customer_added': False,
#                 'reject_status':bill.reject_status,
#             })

#         merchant_object = MerchantProfile.objects.get(id = merchant_business_id)

#         customer_bill = CustomerBill.objects.filter(business_name = merchant_object, customer_added = False, reject_status = True).order_by('-id')

#         for bill in customer_bill:
#             try:
#                 bill_file = str(base_url) + str(bill.bill.url)
#             except:
#                 bill_file = ""

#             if bill.is_checkoutpin == True:
#                 try:
#                     mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
#                 except:
#                     mobile_no = bill.mobile_no
#             else:
#                 mobile_no = bill.mobile_no

#             data.append({
#                 'bill_id': bill.id,
#                 'invoice_no': bill.invoice_no,
#                 'mobile_no': mobile_no,
#                 'amount': str(bill.bill_amount),
#                 'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'bill_file': bill_file,
#                 'db_table': "CustomerBill",
#                 'customer_added': False,
#                 'reject_status':bill.reject_status,
#             })

#         merchant_bill = MerchantBill.objects.filter(business_name = merchant_object, reject_status = True)

#         for bill in merchant_bill:
#             try:
#                 bill_file = str(base_url) + str(bill.bill.url)
#             except:
#                 bill_file = ""

#             if bill.is_checkoutpin == True:
#                 try:
#                     mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
#                 except:
#                     mobile_no = bill.mobile_no
#             else:
#                 mobile_no = bill.mobile_no
                
#             data.append({
#                 'bill_id': bill.id,
#                 'invoice_no': bill.invoice_no,
#                 'mobile_no': mobile_no,
#                 'amount': str(bill.bill_amount),
#                 'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'bill_file': bill_file,
#                 'db_table': "MerchantBill",
#                 'customer_added': False,
#                 'reject_status':bill.reject_status,
#             })

#         data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

#         new_data = []
#         if from_date and to_date:
#             if data:
#                 if from_date:
#                     from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

#                 if to_date:
#                     to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

#                 for bill in data:
#                         bill_date = datetime.strptime(str(bill['bill_date']), '%d-%m-%Y').strftime('%Y-%m-%d')
#                         if from_date and to_date:
                            
#                             if bill_date >= from_date and bill_date <= to_date:
#                                 new_data.append(bill)

#                 new_data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

#                 if new_data:
#                     return JsonResponse({'status': "success", "data":new_data, 
#                          "from_date": from_date, "to_date": to_date}, status=200)
#                 else:
#                     return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)
#         else:

#             if data:
#                 return JsonResponse({"status": "success", "data" : data, "to_date":"","from_date":"" }, status=200)
#             else:
#                 return JsonResponse({'status': 'error'}, status=400)


# class DeleteRejectedBill(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         db_table = request.POST['db_table']

#         bill_id = request.POST['bill_id']

#         if db_table == "SaveParkingLotBill":
#             result = SaveParkingLotBill.objects.filter(id = bill_id).delete()

#         elif db_table == "SavePetrolPumpBill":
#             result = SavePetrolPumpBill.objects.filter(id = bill_id).delete()

#         elif db_table == "CustomerBill":
#             result = CustomerBill.objects.filter(id = bill_id).delete()

#         elif db_table == "MerchantBill":
#             result = MerchantBill.objects.filter(id = bill_id).delete()

#         if result:
#             return JsonResponse({'status': "success", "message":"Bill Deleted Successfully"}, status=200)
#         else:
#             return JsonResponse({'status': "error", 'message': "Failed to Delete"}, status=400)




# class GetPaymentHistory(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         business_id = request.POST['merchant_business_id']

#         from_date = request.POST.get('from_date')

#         to_date = request.POST.get('to_date')
#         # user_id = request.POST['user_id']

#         # merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

#         # merchant_object = GreenBillUser.objects.get(id=merchant_id)

#         # business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)

#         # business_id = business_object.id

#         startswith = str(business_id) + ','
#         endswith = ','+ str(business_id)
#         contains = ','+ str(business_id) + ','
#         exact = str(business_id)
                
#         count1 = 0
#         count2 = 0
#         count3 = 0
#         total_transaction_count = 0
#         payment_history = recharge_history.objects.filter(
#             # Q(merchant_id = merchant_object),
#             Q(business_ids__startswith = startswith) | 
#             Q(business_ids__endswith = endswith) | 
#             Q(business_ids__contains = contains) | 
#             Q(business_ids__exact = exact)
#         ).order_by('-id')

#         payment_history_new = []
#         for history in payment_history:
#             count1 = count1 + 1
#             history.cost = format(history.cost, ".2f") if history.cost else float(0)
#             history.purchase_date = datetime.strptime(str((history.purchase_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y')
#             history.subscription_bill_url = "http://157.230.228.250/my-subscription-bill/"+ str(history.id) + str("/")


#         # payment_history_new = PaymentHistorySerializer(payment_history, many=True)

#             payment_history_new.append({
#                     "id": history.id,
#                     "business":"Green Bill",
#                     "description":history.subscription_name,
#                     "transaction_id":history.transaction_id,
#                     "mode": 'PayU' if history.transaction_id else history.mode,
#                     "purchase_date":history.purchase_date,
#                     "cost":float(history.cost),
#                     "subscription_bill_url": history.subscription_bill_url,
#                 })


#         merchant_bill = MerchantBill.objects.filter(bill_received_business_name = business_id, payment_done = True).order_by('-id')
#         for history in merchant_bill:
#             count2 = count2 + 1
#             history.cost = format(history.bill_amount, ".2f")
#             if history.payment_date:
#                 history.purchase_date = datetime.strptime(str((history.payment_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y')
#             else:
#                 history.purchase_date = ""

#             if history.payment_date:
#                 payment_history_new.append({
#                     "id":history.id,
#                     "business":history.business_name.m_business_name,
#                     "description":"Bill Payment",
#                     "transaction_id":history.transaction_id,
#                     "mode": 'PayU' if history.transaction_id else '',
#                     "purchase_date":history.purchase_date,
#                     "cost":float(history.cost),
#                     "bill_url":history.bill_url,
#                     })

#         my_ads_payment = PromotionsPaymentHistory.objects.filter(merchant_business_id = business_id, payment_done = True).order_by('-id')

#         for history in my_ads_payment:
#             count3 = count3 + 1
#             history.cost = history.payment_amount

#             if history.payment_date:
#                 history.purchase_date = datetime.strptime(str((history.payment_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y')
#             else:
#                 history.purchase_date = ""

#             if history.payment_date:
#                 payment_history_new.append({
#                     "id":history.id,
#                     "business":history.merchant_business_id.m_business_name,
#                     "description":"Third Party Ads",
#                     "transaction_id":history.transaction_id,
#                     "mode": 'PayU' if history.transaction_id else '',
#                     "purchase_date":history.purchase_date,
#                     "cost":float(history.cost),
#                     "bill_url": "",
#                     })

#         merchant_business_id = MerchantProfile.objects.get(id = business_id, m_active_account = True)
#         data = OfferModel.objects.filter(merchant_business_id = merchant_business_id,offer_panel='merchant', status=1).order_by("-id")

#         if PromotionsAmount.objects.all():
#             amount = PromotionsAmount.objects.latest('id')
#             offer_amount = amount.offer_amount
#         else:
#             offer_amount = 0

#         today = date.today()
#         total_amount_spent = 0.0

#         for offer in data:
#             # if offer.valid_through >= today:
#             count3 = count3 + 1

#             payment_history_new.append({
#                 "id":0,
#                 "business":"Offer",
#                 "description": offer.offer_name,
#                 "transaction_id": None,
#                 "mode": "",
#                 "purchase_date": datetime.strptime(str((offer.created_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 "cost": float(offer_amount) * float(offer.customer_merchant_count),
#                 "bill_url": "",
#             })
#             total_amount_spent = total_amount_spent + (float(offer_amount) * float(offer.customer_merchant_count))

#         coupon_merchant_id = MerchantProfile.objects.get(id = business_id, m_active_account = True).id

#         coupon_list = CouponModel.objects.filter(merchant_business_id = coupon_merchant_id, coupon_panel = "merchant").order_by('-id')

#         if PromotionsAmount.objects.all():
#             data = PromotionsAmount.objects.latest('id')
#             coupon_amount = data.coupon_amount
#         else:
#             coupon_amount = 0

#         today = date.today()
#         for coupon in coupon_list:
#             # if coupon.valid_through >= today:
#             count3 = count3 + 1

#             payment_history_new.append({
#                 "id":0,
#                 "business":"Coupon",
#                 "description": coupon.coupon_name,
#                 "transaction_id": None,
#                 "mode": "",
#                 "purchase_date": datetime.strptime(str((datetime(coupon.valid_from.year, coupon.valid_from.month, coupon.valid_from.day)).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 "cost": float(coupon_amount) * float(coupon.total_customers),
#                 "bill_url": "",
#             })

#             total_amount_spent = total_amount_spent + (float(coupon_amount) * float(coupon.total_customers))
        
#         total_transaction_count = count1 + count2 + count3

#         payment_history_new.sort(key = lambda x: datetime.strptime(x['purchase_date'], '%d-%m-%Y'), reverse = True)

#         for payment in payment_history_new:
#             if payment['business'] != "Offer" and payment['business'] != "Coupon":
#                 if payment["cost"] != 0:
#                     total_amount_spent = total_amount_spent + payment["cost"]


#         # for bill in sorted_payment_history:
#         #     bill['purchase_date_new'] = datetime.strptime(str(bill['purchase_date']), '%m-%d-%Y').strftime('%m-%d-%Y') if bill['purchase_date'] else ""
#         new_data = []
#         count = 0
#         if from_date and to_date:
#             if payment_history_new:
#                 if from_date:
#                     from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

#                 if to_date:
#                     to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

#                 for bill in payment_history_new:
#                     if from_date and to_date:
#                         purchase_date_new = datetime.strptime(str(bill['purchase_date']), '%d-%m-%Y').strftime('%Y-%m-%d')
#                         if purchase_date_new >= from_date and purchase_date_new <= to_date:
#                             count = count + 1
#                             new_data.append(bill)

#                 new_data.sort(key = lambda x: datetime.strptime(x['purchase_date'], '%d-%m-%Y'), reverse = True)

#                 total_amount_spent = 0
#                 total_transaction_count = count
#                 for payment in new_data:
#                     if payment['cost']:
#                         total_amount_spent = total_amount_spent + float(payment['cost'])

#             if new_data:
#                 return JsonResponse({'status': "success", "data":new_data, 'total_amount_spent': format(total_amount_spent, ".2f"), 'total_transaction_count': total_transaction_count, "from_date": from_date, "to_date": to_date}, status=200)
#             else:
#                 return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)
#         else:

#             if payment_history_new:
#                 return JsonResponse({'status': 'success', 'data' : payment_history_new,"from_date":"","to_date":"",'total_amount_spent': format(total_amount_spent, ".2f"), 'total_transaction_count': total_transaction_count}, status=200)
#             else:
#                 return JsonResponse({'status': 'No data found.'}, status=400)


# class GetPaymentReceived(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         business_id = request.POST['merchant_business_id']

#         from_date = request.POST.get('from_date')

#         to_date = request.POST.get('to_date')

#         payment_received_data = []

#         received_payments = PaymentLinks.objects.filter(m_business_id = business_id, payment_done = True).order_by('-id')
#         for payment in received_payments:
#             if payment.description:
#                 description = payment.description
#             else:
#                 description = ''

#             payment_received_data.append({
#                 'mobile_no': payment.mobile_no,
#                 'amount' : format(float(payment.amount), ".2f"),
#                 'payment_date' : payment.payment_date,
#                 'transaction_id' : payment.transaction_id,
#                 'created_at' : payment.created_at,
#                 'payment_date_new':datetime.strptime(str(payment.payment_date.date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'description':  description,
#             })

#             payment.payment_date = datetime.strptime(str(payment.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d')
    

#         customer_bill = CustomerBill.objects.filter(business_name = business_id,payment_done = True)
#         for customer in customer_bill:
#             payment_received_data.append({
#                 'mobile_no': customer.mobile_no,
#                 'amount' : format(float(customer.bill_amount), ".2f"),
#                 'payment_date' : customer.payment_date,
#                 'transaction_id' : customer.transaction_id,
#                 'created_at' : customer.created_at,
#                 'payment_date_new':datetime.strptime(str(customer.payment_date.date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'description':  '',
#             })


#         merchant_bill = MerchantBill.objects.filter(business_name = business_id,payment_done = True)        
#         for merchant in merchant_bill:
#             payment_received_data.append({
#                 'mobile_no': merchant.mobile_no,
#                 'amount' : format(float(merchant.bill_amount), ".2f"),
#                 'payment_date' : merchant.payment_date if merchant.payment_date else "",
#                 'transaction_id' : merchant.transaction_id,
#                 'created_at' : merchant.created_at,
#                 'payment_date_new':datetime.strptime(str(merchant.payment_date.date()), '%Y-%m-%d').strftime('%d-%m-%Y') if merchant.payment_date else "",
#                 'description':  '',
#             })


#         parking_bill = SaveParkingLotBill.objects.filter(m_business_id = business_id, payment_done = True) 
#         for parking in parking_bill:
#             payment_received_data.append({
#                 'mobile_no': parking.mobile_no,
#                 'amount' : format(float(parking.amount), ".2f"),
#                 'payment_date' : parking.payment_date,
#                 'transaction_id' : parking.transaction_id,
#                 'created_at' : parking.created_at,
#                 'payment_date_new':datetime.strptime(str(parking.payment_date.date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'description':  '',
#             })

#         petrol_bill = SavePetrolPumpBill.objects.filter(m_business_id = business_id, payment_done=True)
#         for petrol in petrol_bill:
#             payment_received_data.append({
#                 'mobile_no': petrol.mobile_no,
#                 'amount' : format(float(petrol.amount), ".2f"),
#                 'payment_date' : petrol.payment_date,
#                 'transaction_id' : petrol.transaction_id,
#                 'created_at' : petrol.created_at,
#                 'payment_date_new' : datetime.strptime(str(petrol.payment_date.date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                 'description':  '',
#             })

#         total_payments_count =  len(payment_received_data)

#         total_payment = 0.00

#         for payment in payment_received_data:
#             total_payment = total_payment + float(payment['amount'])

#         new_data = []

#         if from_date and to_date:
#             if payment_received_data:
#                 if from_date:
#                     from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

#                 if to_date:
#                     to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

#                 for bill in payment_received_data:
#                     payement_bill_date = datetime.strptime(str(bill['payment_date_new']), '%d-%m-%Y').strftime('%Y-%m-%d')
#                     if payement_bill_date >= from_date and payement_bill_date <= to_date:
#                         new_data.append(bill)

#                 # new_data.sort(key = lambda x: datetime.strptime(x['payment_date_new'], '%d-%m-%Y'), reverse = True)
#                 total_payment = 0.00
#                 total_payments_count = 0

#                 for payment in new_data:
#                     total_payment = total_payment + float(payment['amount'])

#                 total_payments_count = len(new_data)

#             if new_data:
#                 return JsonResponse({'status': "success", "data":new_data, 
#                 "from_date": from_date, "to_date": to_date,"total_payment_received": float(total_payment), "total_payments_received_count": total_payments_count}, status=200)
#             else:
#                 return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)
#         else:

#             if payment_received_data:
#                 return JsonResponse({"status": "success", "data" : payment_received_data,"from_date": "", "to_date": "", "total_payment_received": float(total_payment), "total_payments_received_count": total_payments_count}, status=200)
#             else:
#                 return JsonResponse({'status': 'error'}, status=400)


# class GetBillRating(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         merchant_business_id = request.POST['merchant_business_id']

#         merchant_rating = request.POST.get('merchant_rating')

#         merchant_business_object = MerchantProfile.objects.get(id = merchant_business_id)

#         all_bills = CustomerBill.objects.filter(business_name = merchant_business_object).order_by('-id')

#         new_list = []

#         if merchant_rating:
#             merchant_rating_count = CustomerBill.objects.filter(business_name = merchant_business_object, rating = merchant_rating).count()
#         else:
#             merchant_rating_count = 0
#             for bill in all_bills:
#                 if bill.rating:
#                     merchant_rating_count = merchant_rating_count + 1

#         for bill in all_bills:

#             if bill:
#                 try:
#                     bill_design_object = bill_designs.objects.get(merchant_business_id = merchant_business_id)
#                     bill_rating_emoji = bill_design_object.rating_emoji
#                 except:
#                     testingstring = '\U0001f604'
#                     bill_rating_emoji = testingstring.encode('unicode_escape')
#                     # bill_rating_emoji = '😊'

#                 ratings = ""
#                 rating_id = ""

#                 if bill.rating:

#                     rating_id = bill.rating

#                     for x in range(int(bill.rating)):
#                         ratings = " ".join((ratings, bill_rating_emoji))


#                 bill.rating = ratings

#                 bill.bill_date = datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y')

#                 bill.bill_amount = "{:.2f}".format(bill.bill_amount)

#                 if bill.rating:

#                     new_list.append({
#                         "id": bill.id,
#                         "user_id": bill.user_id,
#                         "mobile_no": bill.mobile_no,
#                         "bill_amount": bill.bill_amount,
#                         "bill_date": bill.bill_date,
#                         "invoice_no":bill.invoice_no,
#                         "rating_id":  rating_id,
#                         "rating": bill.rating,
#                         "store_feedback":bill.feedback_selected_option,
#                         "merchant_reply":bill.feedback_reply,
#                     })

#         # all_bills_new = BillRatingSerializer(all_bills, many=True)

#         if new_list:
#             return JsonResponse({'status': 'success', 'data' : new_list, "merchant_rating_count": merchant_rating_count}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)

# class GetDashboardDetails(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         merchant_business_id = request.POST['merchant_business_id']

#         merchant_business = MerchantProfile.objects.get(id = merchant_business_id)

#         # Total Transactions

#         total_transaction = 0

#         total_transaction1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False,created_at__date = timezone.now()).count()

#         total_transaction2 = MerchantBill.objects.filter(business_name = merchant_business,created_at__date = timezone.now()).count()

#         total_transaction = total_transaction1 + total_transaction2

#         # Average Transactions

#         date_joined = merchant_business.date_joined

#         today = date.today()

#         current_date = today.strftime("%Y-%m-%d")
#         current_date_new = datetime.strptime(str(current_date), "%Y-%m-%d")
#         date_joined_new = datetime.strptime(str(date_joined.date()), "%Y-%m-%d")
#         diff = current_date_new - date_joined_new

#         total_days = diff.days

#         average_transaction = 0

#         received_payments1 = PaymentLinks.objects.filter(m_business_id = merchant_business, payment_done = True,created_at__date = timezone.now())

#         payment_amount1 = 0
#         for pay in received_payments1:
#             if pay.amount:
#                 payment_amount1 = float(payment_amount1) + float(pay.amount)

#         customer_bills1 = CustomerBill.objects.filter(business_name = merchant_business,payment_done = True,created_at__date = timezone.now())

#         cust_amount1 = 0
#         for bill in customer_bills1:
#             if bill.bill_amount:
#                 cust_amount1 = float(cust_amount1) + float(bill.bill_amount)

#         merchant_bills1 = MerchantBill.objects.filter(business_name = merchant_business,payment_done = True,created_at__date = timezone.now())

#         mer_amount1 = 0
#         for bill in merchant_bills1:
#             if bill.bill_amount:
#                 mer_amount1 = float(mer_amount1) + float(bill.bill_amount)

#         parking_bills1 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business, payment_done = True,created_at__date = timezone.now()) 

#         park_amount1 = 0
#         for bill in parking_bills1:
#             if bill.amount:
#                 park_amount1 = float(park_amount1) + float(bill.amount)

#         petrol_bills1 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business, payment_done=True,created_at__date = timezone.now())

#         petr_amount1 = 0
#         for bill in petrol_bills1:
#             if bill:
#                 petr_amount1 = float(petr_amount1) + float(bill.amount)


#         average_transaction = float(petr_amount1) + float(park_amount1) + float(mer_amount1) + float(cust_amount1) + float(payment_amount1)

#         # if total_transaction != 0 and total_days != 0:
#         #     average_transaction = total_transaction/total_days
#         # else:
#         #     average_transaction = 0



#         # Total Sales

#         customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False,created_at__date = timezone.now()).order_by('-id')

#         merchant_bill = MerchantBill.objects.filter(business_name = merchant_business,created_at__date = timezone.now()).order_by('-id')

#         total_sales = 0

#         for bill in customer_bill:
#             total_sales = total_sales + float(bill.bill_amount)

#         for bill in merchant_bill:
#             total_sales = total_sales + float(bill.bill_amount)

#         # Average Sales

#         average_sales = 0

#         if total_transaction != 0 and total_sales != 0:
#             average_sales = total_sales/total_transaction
#         else:
#             average_sales = 0

#         data = {
#             'todays_transaction': total_transaction,
#             'average_transaction': "{:.2f}".format(average_transaction),
#             'total_sales': "{:.2f}".format(total_sales),
#             'average_sales': "{:.2f}".format(average_sales),
#         }

#         if data:
#             return JsonResponse({'status': 'success', 'data' : data}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# def getActiveSubscriptionPlan(request, business_id):

#     subscription_object = ""

#     if business_id:
#         startswith = str(business_id) + ','
#         endswith = ','+ str(business_id)
#         contains = ','+ str(business_id) + ','
#         exact = str(business_id)
        
#         try:
#             subscription_object = merchant_subscriptions.objects.get(
#                 Q(is_active = True),
#                 Q(business_ids__startswith = startswith) | 
#                 Q(business_ids__endswith = endswith) | 
#                 Q(business_ids__contains = contains) | 
#                 Q(business_ids__exact = exact)
#             )

#             return subscription_object

#         except:
#             return subscription_object
#     else:
#         return subscription_object


# def getActiveTransactionalSubscriptionPlan(request, business_id):

#     subscription_object = ""

#     if business_id:
#         startswith = str(business_id) + ','
#         endswith = ','+ str(business_id)
#         contains = ','+ str(business_id) + ','
#         exact = str(business_id)
        
#         try:
#             subscription_object = transactional_sms_subscriptions.objects.get(
#                 Q(is_active = True),
#                 Q(business_ids__startswith = startswith) | 
#                 Q(business_ids__endswith = endswith) | 
#                 Q(business_ids__contains = contains) | 
#                 Q(business_ids__exact = exact)
#             )

#             return subscription_object

#         except:
#             return subscription_object
#     else:
#         return subscription_object


# def getActivePromotionalSubscriptionPlan(request, business_id):

#     subscription_object = ""

#     if business_id:
#         startswith = str(business_id) + ','
#         endswith = ','+ str(business_id)
#         contains = ','+ str(business_id) + ','
#         exact = str(business_id)
        
#         try:
#             subscription_object = promotional_sms_subscriptions.objects.get(
#                 Q(is_active = True),
#                 Q(business_ids__startswith = startswith) | 
#                 Q(business_ids__endswith = endswith) | 
#                 Q(business_ids__contains = contains) | 
#                 Q(business_ids__exact = exact)
#             )

#             return subscription_object

#         except:
#             return subscription_object
#     else:
#         return subscription_object



# class MerchantBillingAnalysisGraphAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         merchant_business_id = request.POST['merchant_business_id']
#         from_date = request.POST['from_date']
#         to_date = request.POST['to_date']

#         merchant_business = MerchantProfile.objects.get(id = merchant_business_id)


#         if from_date and to_date:
#             DATE_FORMAT = '%Y-%m-%d'
#             date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
#             day_later = date_time_obj + timedelta(days=1)
#             x = day_later.date()
#             ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

#             billing_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
#             start_date = billing_from_date.split('-')
#             start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
#             sd_filter = start_date.strftime(DATE_FORMAT)

#             customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')

#             merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')

#             merchant_bill1 = MerchantBill.objects.filter(bill_received_business_name = merchant_business_id, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')

#             startswith = str(merchant_business.id) + ','
#             endswith = ','+ str(merchant_business.id)
#             contains = ','+ str(merchant_business.id) + ','
#             exact = str(merchant_business.id)

#             recharge_his = recharge_history.objects.filter(
#                 Q(purchase_date__gte = sd_filter),
#                 Q(purchase_date__lte = ed_filter),
#                 Q(business_ids__startswith = startswith) | 
#                 Q(business_ids__endswith = endswith) | 
#                 Q(business_ids__contains = contains) | 
#                 Q(business_ids__exact = exact)
#             ).order_by('-id')

#             rejected_bill_count = 0
#             received_bill_count = 0
#             sent_bill_count = 0

#             for bill in customer_bill:
#                 sent_bill_count = sent_bill_count + 1
#                 if bill.reject_status == True:
#                     rejected_bill_count = rejected_bill_count + 1

#             for bill in merchant_bill:
#                 sent_bill_count = sent_bill_count + 1
#                 if bill.reject_status == True:
#                     rejected_bill_count = rejected_bill_count + 1
#             for bill in merchant_bill1:
#                 # if int(bill.bill_received_business_name) == merchant_business.id:
#                 received_bill_count = received_bill_count + 1

#             for recharge in recharge_his:
#                 received_bill_count = received_bill_count + 1

#             billing_analysis_labels_temp = []
#             billing_analysis_labels_temp.append("Sent Bills")
#             billing_analysis_labels_temp.append("Received Bills")
#             billing_analysis_labels_temp.append("Rejected Bills")

#             billing_analysis_data_temp = []
#             billing_analysis_data_temp.append(str(sent_bill_count))
#             billing_analysis_data_temp.append(str(received_bill_count))
#             billing_analysis_data_temp.append(str(rejected_bill_count))


#         else:

#             customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__date = timezone.now()).order_by('-id')

#             merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now()).order_by('-id')

#             merchant_bill1 = MerchantBill.objects.filter(bill_received_business_name = merchant_business_id, created_at__date = timezone.now()).order_by('-id')

#             startswith = str(merchant_business.id) + ','
#             endswith = ','+ str(merchant_business.id)
#             contains = ','+ str(merchant_business.id) + ','
#             exact = str(merchant_business.id)

#             recharge_his = recharge_history.objects.filter(
#                 Q(purchase_date__date = timezone.now()),
#                 Q(business_ids__startswith = startswith) | 
#                 Q(business_ids__endswith = endswith) | 
#                 Q(business_ids__contains = contains) | 
#                 Q(business_ids__exact = exact)
#             ).order_by('-id')


#             rejected_bill_count = 0
#             received_bill_count = 0
#             sent_bill_count = 0

#             for bill in customer_bill:
#                 sent_bill_count = sent_bill_count + 1
#                 if bill.reject_status == True:
#                     rejected_bill_count = rejected_bill_count + 1

#             for bill in merchant_bill:
#                 sent_bill_count = sent_bill_count + 1
#                 if bill.reject_status == True:
#                     rejected_bill_count = rejected_bill_count + 1

#                 # if int(bill.bill_received_business_name) == merchant_business.id:
#             for bill in merchant_bill1:
#                 received_bill_count = received_bill_count + 1

#             for recharge in recharge_his:
#                 received_bill_count = received_bill_count + 1

#             billing_analysis_labels_temp = []
#             billing_analysis_labels_temp.append("Sent Bills")
#             billing_analysis_labels_temp.append("Received Bills")
#             billing_analysis_labels_temp.append("Rejected Bills")

#             billing_analysis_data_temp = []
#             billing_analysis_data_temp.append(str(sent_bill_count))
#             billing_analysis_data_temp.append(str(received_bill_count))
#             billing_analysis_data_temp.append(str(rejected_bill_count))

#         if billing_analysis_data_temp and billing_analysis_labels_temp:
#             return JsonResponse({'status': 'success', 'labels': billing_analysis_labels_temp, 'data': billing_analysis_data_temp}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)


# class MerchantDigitalBillingGraphAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         merchant_business_id = request.POST['merchant_business_id']
#         from_date = request.POST['from_date']
#         to_date = request.POST['to_date']

#         merchant_business = MerchantProfile.objects.get(id = merchant_business_id)

#         # notifications = sent_bill_history.objects.filter(
#         #     m_business_id = merchant_business.id,
#         #     created_at__date = timezone.now(),
#         #     digital_bill = True
#         # ).count()

#         # sms = sent_bill_history.objects.filter(
#         #     m_business_id = merchant_business.id,
#         #     created_at__date = timezone.now(),
#         #     sms_bill = True
#         # ).count()

#         if from_date and to_date:

#             DATE_FORMAT = '%Y-%m-%d'

#             d_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
#             start_date = d_from_date.split('-')
#             start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
#             sd_filter = start_date.strftime(DATE_FORMAT)

#             date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
#             day_later = date_time_obj + timedelta(days=1)
#             x = day_later.date()
#             ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

#             customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')
#             merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')

#             parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False,created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')
#             petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id,created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')


#             digital_sent = 0
#             sms_sent = 0

#             try:
#                 for bill in customer_bill:
#                     if bill.greenbill_digital_bill == "True":
#                         digital_sent = digital_sent + 1
#                     elif bill.greenbill_sms_bill == "True":
#                         sms_sent = sms_sent + 1

#                 for bill in merchant_bill:
#                     if bill.greenbill_digital_bill == "True":
#                         digital_sent = digital_sent + 1
#                     elif bill.greenbill_sms_bill == "True":
#                         sms_sent = sms_sent + 1

#                 for bill in parking_bill_list:
#                     if bill.greenbill_digital_bill == "True":
#                         digital_sent = digital_sent + 1
#                     elif bill.greenbill_sms_bill == "True":
#                         sms_sent = sms_sent + 1

#                 for bill in petrol_bill_list:
#                     if bill.greenbill_digital_bill == "True":
#                         digital_sent = digital_sent + 1
#                     elif bill.greenbill_sms_bill == "True":
#                         sms_sent = sms_sent + 1
#             except:
#                 pass

#             digital_billing_labels_temp = []
#             digital_billing_labels_temp.append("SMS Sent")
#             digital_billing_labels_temp.append("Notifications Sent")

#             digital_billing_data_temp = []
#             digital_billing_data_temp.append(str(sms_sent))
#             digital_billing_data_temp.append(str(digital_sent))

#         else:

#             customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__date = timezone.now()).order_by('-id')
#             merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now()).order_by('-id')

#             parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False,created_at__date = timezone.now()).order_by('-id')
#             petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id,created_at__date = timezone.now()).order_by('-id')

#             digital_sent = 0
#             sms_sent = 0
            
#             try:
#                 for bill in customer_bill:
#                     if bill.greenbill_digital_bill == "True":
#                         digital_sent = digital_sent + 1
#                     elif bill.greenbill_sms_bill == "True":
#                         sms_sent = sms_sent + 1

#                 for bill in merchant_bill:
#                     if bill.greenbill_digital_bill == "True":
#                         digital_sent = digital_sent + 1
#                     elif bill.greenbill_sms_bill == "True":
#                         sms_sent = sms_sent + 1

#                 for bill in parking_bill_list:
#                     if bill.greenbill_digital_bill == "True":
#                         digital_sent = digital_sent + 1
#                     elif bill.greenbill_sms_bill == "True":
#                         sms_sent = sms_sent + 1

#                 for bill in petrol_bill_list:
#                     if bill.greenbill_digital_bill == "True":
#                         digital_sent = digital_sent + 1
#                     elif bill.greenbill_sms_bill == "True":
#                         sms_sent = sms_sent + 1
#             except:
#                 pass

#             digital_billing_labels_temp = []
#             digital_billing_labels_temp.append("SMS Sent")
#             digital_billing_labels_temp.append("Notifications Sent")

#             digital_billing_data_temp = []
#             digital_billing_data_temp.append(str(sms_sent))
#             digital_billing_data_temp.append(str(digital_sent))

#         if digital_billing_data_temp and digital_billing_labels_temp:
#             return JsonResponse({'status': 'success', 'labels': digital_billing_labels_temp, 'data': digital_billing_data_temp}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)


# class MerchantCouponsDetailsGraphAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         merchant_business_id = request.POST['merchant_business_id']

#         merchant_business = MerchantProfile.objects.get(id = merchant_business_id)

#         all_coupons = CouponModel.objects.filter(merchant_business_id = merchant_business.id)

#         coupon_active_count = 0
#         coupon_expired_count = 0

#         today = date.today()
#         current_date = today.strftime("%Y-%m-%d")
#         current_date_new = datetime.strptime(str(current_date), "%Y-%m-%d")

#         for coupon in all_coupons:
#             valid_to_date = datetime.strptime(str(coupon.valid_through), "%Y-%m-%d")
#             if valid_to_date < current_date_new:
#                 coupon_expired_count = coupon_expired_count + 1
#             else:
#                 coupon_active_count = coupon_active_count + 1

#         coupons_labels_temp = []
#         coupons_labels_temp.append("Active")
#         coupons_labels_temp.append("Expired")

#         coupons_data_temp = []
#         coupons_data_temp.append(str(coupon_active_count))
#         coupons_data_temp.append(str(coupon_expired_count))

#         if coupons_data_temp and coupons_labels_temp:
#             return JsonResponse({'status': 'success', 'labels': coupons_labels_temp, 'data': coupons_data_temp}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)


# class MerchantOffersDetailsGraphAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         merchant_business_id = request.POST['merchant_business_id']

#         merchant_business = MerchantProfile.objects.get(id = merchant_business_id)

#         all_offers = OfferModel.objects.filter(merchant_business_id = merchant_business)

#         offer_active_count = 0
#         offer_expired_count = 0
#         offer_not_approved = 0

#         today = date.today()
#         current_date = today.strftime("%Y-%m-%d")
#         current_date_new = datetime.strptime(str(current_date), "%Y-%m-%d")

#         for offer in all_offers:
#             valid_to_date = datetime.strptime(str(offer.valid_through), "%Y-%m-%d")
#             if valid_to_date < current_date_new:
#                 if offer.status == "1":
#                     offer_expired_count = offer_expired_count + 1
#             elif offer.status == "1":
#                 offer_active_count = offer_active_count + 1
#             if offer.status == "0":
#                 offer_not_approved = offer_not_approved + 1

#         offer_labels_temp = []
#         offer_labels_temp.append("Active")
#         offer_labels_temp.append("Expired")
#         offer_labels_temp.append("Not Approved")

#         offer_data_temp = []
#         offer_data_temp.append(str(offer_active_count))
#         offer_data_temp.append(str(offer_expired_count))
#         offer_data_temp.append(str(offer_not_approved))

#         if offer_data_temp and offer_labels_temp:
#             return JsonResponse({'status': 'success', 'labels': offer_labels_temp, 'data': offer_data_temp}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)


# class MerchantOverallCustomerAnalysisGraphAPI(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         merchant_business_id = request.POST['merchant_business_id']
#         from_date = request.POST['from_date']
#         to_date = request.POST['to_date']

#         merchant_business = MerchantProfile.objects.get(id = merchant_business_id)
#         context = {}
#         if from_date and to_date:
#             DATE_FORMAT = '%Y-%m-%d'
#             cust_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
#             start_date = cust_from_date.split('-')
#             start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
#             sd_filter = start_date.strftime(DATE_FORMAT)

#             cust_to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%d-%m-%Y')
#             end_date = cust_to_date.split('-')
#             end_date = date(int(end_date[2]), int(end_date[1]), int(end_date[0]))
#             ed_filter = end_date.strftime(DATE_FORMAT)

#             unique_customer = []

#             customers1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__range = (sd_filter, ed_filter))

#             customers2 = MerchantBill.objects.filter(business_name = merchant_business,customer_added = False, created_at__range = (sd_filter, ed_filter))
            
#             customers3 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id,is_pass=False, created_at__range = (sd_filter, ed_filter))
#             customers4 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, created_at__range = (sd_filter, ed_filter))

#             for customer in customers1:
#                 if customer.mobile_no in unique_customer:
#                     pass
#                 else:
#                     unique_customer.append(customer.mobile_no)

#             for customer in customers2:
#                 if customer.mobile_no in unique_customer:
#                     pass
#                 else:
#                     unique_customer.append(customer.mobile_no)

#             for customer in customers3:
#                 if customer.mobile_no in unique_customer:
#                     pass
#                 else:
#                     unique_customer.append(customer.mobile_no)

#             for customer in customers4:
#                 if customer.mobile_no in unique_customer:
#                     pass
#                 else:
#                     unique_customer.append(customer.mobile_no)


#             new_customer_count = 0
#             returning_customers_count = 0

#             for mobile_no in unique_customer:
#                 bill_count1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
#                 bill_count2 = MerchantBill.objects.filter(business_name = merchant_business, mobile_no = mobile_no).count()
#                 bill_count3 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, mobile_no = mobile_no).count()
#                 bill_count4 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, mobile_no = mobile_no).count()
#                 bill_count = 0
#                 bill_count = bill_count1 + bill_count2 + bill_count3 + bill_count4
#                 if bill_count == 1:
#                     new_customer_count = new_customer_count + 1
#                 elif bill_count != 0:
#                     returning_customers_count = returning_customers_count + 1

                
#             # total_customers = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False).distinct()

#             customers1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False)
#             customers2 = MerchantBill.objects.filter(business_name = merchant_business)
#             customers3 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id,is_pass=False)
#             customers4 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id)

#             total_unique_customer = []
#             for customer in customers1:
#                 if customer.mobile_no in total_unique_customer:
#                     pass
#                 else:
#                     total_unique_customer.append(customer.mobile_no)

#             for customer in customers2:
#                 if customer.mobile_no in total_unique_customer:
#                     pass
#                 else:
#                     total_unique_customer.append(customer.mobile_no)

#             for customer in customers3:
#                 if customer.mobile_no in total_unique_customer:
#                     pass
#                 else:
#                     total_unique_customer.append(customer.mobile_no)

#             for customer in customers4:
#                 if customer.mobile_no in total_unique_customer:
#                     pass
#                 else:
#                     total_unique_customer.append(customer.mobile_no)


#             total_customer_count = len(total_unique_customer)
#             new_customers_value = 0

#             if new_customer_count != 0 and total_customer_count != 0:
#                 new_customers_value = int((new_customer_count * 100)/total_customer_count)
#                 new_customers_text = str(new_customer_count)
#             else:
#                 new_customers_value = 0
#                 new_customers_text = 0

#             context['new_customers_text'] = str(new_customers_text)
#             context['new_customers_value'] = str(new_customers_value)

#             # returning_customers_count = 0
#             # for mobile_no in unique_customer:
#             #     bill_count1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
#             #     bill_count2 = MerchantBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
#             #     bill_count = 0
#             #     bill_count = bill_count1 + bill_count2
#             #     if bill_count >= 2:
#             #         returning_customers_count = returning_customers_count + 1

#             if returning_customers_count != 0 and total_customer_count != 0:
#                 returning_customers_value = int((returning_customers_count * 100)/total_customer_count)
#                 returning_customers_text = str(returning_customers_count)
#             else:
#                 returning_customers_value = 0
#                 returning_customers_text = 0

#             context['returning_customers_text'] = str(returning_customers_text)
#             context['returning_customers_value'] = str(returning_customers_value)

#         else:
#             unique_customer = []
#             customers1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__date = timezone.now())

#             customers2 = MerchantBill.objects.filter(business_name = merchant_business,customer_added = False, created_at__date = timezone.now())
#             customers3 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id,is_pass=False, created_at__date = timezone.now())
#             customers4 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, created_at__date = timezone.now())


#             for customer in customers1:
#                 if customer.mobile_no in unique_customer:
#                     pass
#                 else:
#                     unique_customer.append(customer.mobile_no)

#             for customer in customers2:
#                 if customer.mobile_no in unique_customer:
#                     pass
#                 else:
#                     unique_customer.append(customer.mobile_no)

#             for customer in customers3:
#                 if customer.mobile_no in unique_customer:
#                     pass
#                 else:
#                     unique_customer.append(customer.mobile_no)

#             for customer in customers4:
#                 if customer.mobile_no in unique_customer:
#                     pass
#                 else:
#                     unique_customer.append(customer.mobile_no)

#             new_customer_count = 0
#             returning_customers_count = 0

#             for mobile_no in unique_customer:
#                 bill_count1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
#                 bill_count2 = MerchantBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
#                 bill_count3 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, mobile_no = mobile_no).count()
#                 bill_count4 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id, mobile_no = mobile_no).count()
#                 bill_count = 0
#                 bill_count = bill_count1 + bill_count2 + bill_count3 + bill_count4
#                 if bill_count == 1:
#                     new_customer_count = new_customer_count + 1
#                 elif bill_count != 0:
#                     returning_customers_count = returning_customers_count + 1                

#             customers1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False)
#             customers2 = MerchantBill.objects.filter(business_name = merchant_business)
#             customers3 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id,is_pass=False)
#             customers4 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id)


#             total_unique_customer = []
#             for customer in customers1:
#                 if customer.mobile_no in total_unique_customer:
#                     pass
#                 else:
#                     total_unique_customer.append(customer.mobile_no)

#             for customer in customers2:
#                 if customer.mobile_no in total_unique_customer:
#                     pass
#                 else:
#                     total_unique_customer.append(customer.mobile_no)

#             for customer in customers3:
#                 if customer.mobile_no in total_unique_customer:
#                     pass
#                 else:
#                     total_unique_customer.append(customer.mobile_no)

#             for customer in customers4:
#                 if customer.mobile_no in total_unique_customer:
#                     pass
#                 else:
#                     total_unique_customer.append(customer.mobile_no)

#             total_customer_count = len(total_unique_customer)

#             new_customers_value = 0

#             if new_customer_count != 0 and total_customer_count != 0:
#                 new_customers_value = int((new_customer_count * 100)/total_customer_count)
#                 new_customers_text = str(new_customer_count)
#             else:
#                 new_customers_value = 0
#                 new_customers_text = 0


#             context['new_customers_text'] = str(new_customers_text)
#             context['new_customers_value'] = str(new_customers_value)
#             # returning_customers_count = 0
#             # for mobile_no in unique_customer:
#             #     bill_count1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
#             #     bill_count2 = MerchantBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = mobile_no).count()
#             #     bill_count = 0
#             #     bill_count = bill_count1 + bill_count2
#             #     if bill_count >= 2:
#             #         returning_customers_count = returning_customers_count + 1

#             # print(total_customer_count)

#             if returning_customers_count != 0 and total_customer_count != 0:
#                 returning_customers_value = int((returning_customers_count * 100)/total_customer_count)
#                 returning_customers_text = str(returning_customers_count)
#             else:
#                 returning_customers_value = 0
#                 returning_customers_text = 0

#             context['returning_customers_text'] = str(returning_customers_text)
#             context['returning_customers_value'] = str(returning_customers_value)

#         # data = []

#         # data = {
#         #     'new_customers_text': str(new_customers_text),
#         #     'new_customers_value': new_customers_value,
#         #     'returning_customers_text': str(returning_customers_text),
#         #     'returning_customers_value': returning_customers_value
#         # }

#         if context:
#             return JsonResponse({'status': 'success', 'data': context}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)


# class SendBulkSMS(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user_id = request.POST['user_id']
#         transactional = request.POST['transactional']
#         customer = request.POST['customer']
#         smsheader = request.POST['smsheader']
#         unique_template_id = request.POST['template_id']
#         message = request.POST['message']
#         customer_state_value = request.POST['customer_state_value']
#         customer_state_value_new = customer_state_value.split(",")

#         customer_city_value = request.POST['customer_city_value']
#         if customer_city_value:
#             customer_city_value_new = customer_city_value.split(",")
#         else:
#             customer_city_value_new = ''

#         customer_area_value = request.POST['customer_area_value']
#         campaign_name = request.POST.get('campaign_name')
#         if customer_area_value:
#             customer_area_value_new = customer_area_value.split(",")
#         else:
#             customer_area_value_new = ''


#         receipent_count = GreenBillUser.objects.filter(is_customer=True).count()
#         try:
#             smsid = bulkMailSmsMerchantCustomerModel.objects.filter().last().id
#         except:
#             smsid = ""


#         if customer_city_value_new != '' and customer_area_value_new != '':
#             notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(campaign_name=campaign_name, customer_state=customer_state_value_new, customer_city=customer_city_value_new, customer_area=customer_area_value_new, owner_id=GreenBillUser.objects.get(id=user_id),message=message,smsheader=smsheader,template=template, receiver_name=customer, transactional=transactional, defaults= { 'message':message, 'smsheader':smsheader, 'template':template, 'receiver_name':customer, 'o_sent_sms':True })
#         elif customer_city_value_new != '' and customer_area_value_new == '':
#             notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(campaign_name=campaign_name, customer_state=customer_state_value_new, customer_city=customer_city_value_new, owner_id=GreenBillUser.objects.get(id=user_id),message=message,smsheader=smsheader,template=template, receiver_name=customer, transactional=transactional, defaults= { 'message':message, 'smsheader':smsheader, 'template':template, 'receiver_name':customer, 'o_sent_sms':True })
#         elif customer_city_value_new == '' and customer_area_value_new == '':
#             notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(campaign_name=campaign_name, customer_state=customer_state_value_new, owner_id=GreenBillUser.objects.get(id=user_id),message=message,smsheader=smsheader,template=template, receiver_name=customer, transactional=transactional, defaults= { 'message':message, 'smsheader':smsheader, 'template':template, 'receiver_name':customer, 'o_sent_sms':True })

#         if transactional == 'transactional':
#             # print('transactional')
#             merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']
#             business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)

#             subscription_object = getActiveTransactionalSubscriptionPlan(request, business_object.id)

#             if subscription_object:
#                 # print('subscropin plan')
#                 if int(float(subscription_object.total_sms_avilable)) >= int(receipent_count):
#                     if customer:
#                         if customer_city_value_new != '' and customer_area_value_new != '':
#                             users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new)
#                             if users:
#                                 customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new).count()
#                                 customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
#                                 customer_addresswise_count = customer_count

#                                 for u in users:
#                                     contact = u.mobile_no
#                                     if contact:
        
#                                         ts = int(time.time())

#                                         data_temp = {
#                                                 "keyword":"Bill Delivery SMS",
#                                                 "timeStamp":ts,
#                                                 "dataSet":
#                                                     [
#                                                         {
#                                                             "UNIQUE_ID":"GB-" + str(ts),
#                                                             "MESSAGE": message,
#                                                             "OA":smsheader,
#                                                             "MSISDN": contact, # Recipient's Mobile Number
#                                                             "CHANNEL":"SMS",
#                                                             "CAMPAIGN_NAME":"hind_user",
#                                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                                             "USER_NAME":"hind_hsi",
#                                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                                             "DLT_CT_ID":unique_template_id, # Template Id
#                                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                                         }
#                                                     ]
#                                                 }

#                                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                                         response = requests.post(url, json = data_temp)

                                    
#                                     sms_response = sendSMS(str(contact), message)
#                                     # print(sms_response)
#                                     # try:
#                                     #     print('success')
#                                     #         # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
#                                     #         # message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
#                                     # except:
#                                     #         owner_notice_sent_save = ""
#                                     # sms_response = sendSMS(str(contact), message)
#                                     # print(sms_response)
#                                 if response.status_code == 200:
#                                     total_sms_avilable_new = 0
#                                     if customer:
#                                         total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
#                                         subscription_object.total_sms_avilable = total_sms_avilable_new
#                                     else:
#                                         total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
#                                         subscription_object.total_sms_avilable = total_sms_avilable_new

#                                     subscription_object.save()

#                                     bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
#                                     return JsonResponse({'status' : 'error', 'message': "SMS sent successfully"}, status=200)
#                                 else:
#                                     bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
#                                     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

#                             else:
#                                 return JsonResponse({'status' : 'error', 'message': "Customers not found"}, status=400)
                        
#                         elif customer_city_value_new != '' and customer_area_value_new == '':
#                             users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new)
#                             if users:
#                                 customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new).count()
#                                 customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
#                                 customer_addresswise_count = customer_count

#                                 for u in users:
#                                     contact = u.mobile_no
#                                     if contact:
        
#                                         ts = int(time.time())

#                                         data_temp = {
#                                                 "keyword":"Bill Delivery SMS",
#                                                 "timeStamp":ts,
#                                                 "dataSet":
#                                                     [
#                                                         {
#                                                             "UNIQUE_ID":"GB-" + str(ts),
#                                                             "MESSAGE": message,
#                                                             "OA":smsheader,
#                                                             "MSISDN": contact, # Recipient's Mobile Number
#                                                             "CHANNEL":"SMS",
#                                                             "CAMPAIGN_NAME":"hind_user",
#                                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                                             "USER_NAME":"hind_hsi",
#                                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                                             "DLT_CT_ID":unique_template_id, # Template Id
#                                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                                         }
#                                                     ]
#                                                 }

#                                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                                         response = requests.post(url, json = data_temp)

                                    
#                                     sms_response = sendSMS(str(contact), message)
#                                     # print(sms_response)
#                                     # try:
#                                     #     print('success')
#                                     #         # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
#                                     #         # message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
#                                     # except:
#                                     #         owner_notice_sent_save = ""
#                                     # sms_response = sendSMS(str(contact), message)
#                                     # print(sms_response)
#                                 if response.status_code == 200:
#                                     total_sms_avilable_new = 0
#                                     if customer:
#                                         total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
#                                         subscription_object.total_sms_avilable = total_sms_avilable_new
#                                     else:
#                                         total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
#                                         subscription_object.total_sms_avilable = total_sms_avilable_new

#                                     subscription_object.save()

#                                     bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
#                                     return JsonResponse({'status' : 'error', 'message': "SMS sent successfully"}, status=200)
#                                 else:
#                                     bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
#                                     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

#                             else:
#                                 return JsonResponse({'status' : 'error', 'message': "Customers Not Found"}, status=400)
                        
#                         elif customer_city_value_new == '' and customer_area_value_new == '':
#                             users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new)
#                             if users:
#                                 customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new).count()
#                                 customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
#                                 customer_addresswise_count = customer_count

#                                 for u in users:
#                                     contact = u.mobile_no
#                                     if contact:
        
#                                         ts = int(time.time())

#                                         data_temp = {
#                                                 "keyword":"Bill Delivery SMS",
#                                                 "timeStamp":ts,
#                                                 "dataSet":
#                                                     [
#                                                         {
#                                                             "UNIQUE_ID":"GB-" + str(ts),
#                                                             "MESSAGE": message,
#                                                             "OA":smsheader,
#                                                             "MSISDN": contact, # Recipient's Mobile Number
#                                                             "CHANNEL":"SMS",
#                                                             "CAMPAIGN_NAME":"hind_user",
#                                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                                             "USER_NAME":"hind_hsi",
#                                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                                             "DLT_CT_ID":unique_template_id, # Template Id
#                                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                                         }
#                                                     ]
#                                                 }

#                                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                                         response = requests.post(url, json = data_temp)

                                    
#                                     sms_response = sendSMS(str(contact), message)
#                                     # print(sms_response)
#                                     # try:
#                                     #     print('success')
#                                     #         # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
#                                     #         # message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
#                                     # except:
#                                     #         owner_notice_sent_save = ""
#                                     # sms_response = sendSMS(str(contact), message)
#                                     # print(sms_response)
#                                 if response.status_code == 200:
#                                     total_sms_avilable_new = 0
#                                     if customer:
#                                         total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
#                                         subscription_object.total_sms_avilable = total_sms_avilable_new
#                                     else:
#                                         total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
#                                         subscription_object.total_sms_avilable = total_sms_avilable_new

#                                     subscription_object.save()

#                                     bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
#                                     return JsonResponse({'status' : 'error', 'message': "SMS sent successfully"}, status=200)
#                                 else:
#                                     bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
#                                     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

#                             else:
#                                 return JsonResponse({'status' : 'error', 'message': "Customers Not Found"}, status=400)

#                 else:
#                     return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
#             else:
#                 return JsonResponse({'status' : 'error', 'message': "You don't have active Transactional SMS plan. Please purchase and try again."}, status=400)
                            
#         if transactional == 'promotional':
#             merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']
#             business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)

#             subscription_object = getActivePromotionalSubscriptionPlan(request, business_object.id)
#             if subscription_object:
#                 if int(float(subscription_object.total_sms_avilable)) >= int(receipent_count):
#                     if customer:
#                         if customer_city_value_new != '' and customer_area_value_new != '':
#                             users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new)
#                             if users:
#                                 customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new).count()
#                                 customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
#                                 customer_addresswise_count = customer_count

#                                 for u in users:
#                                     contact = u.mobile_no
#                                     if contact:
        
#                                         ts = int(time.time())

#                                         data_temp = {
#                                                 "keyword":"Bill Delivery SMS",
#                                                 "timeStamp":ts,
#                                                 "dataSet":
#                                                     [
#                                                         {
#                                                             "UNIQUE_ID":"GB-" + str(ts),
#                                                             "MESSAGE": message,
#                                                             "OA":smsheader,
#                                                             "MSISDN": contact, # Recipient's Mobile Number
#                                                             "CHANNEL":"SMS",
#                                                             "CAMPAIGN_NAME":"hind_user",
#                                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                                             "USER_NAME":"hind_hsi",
#                                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                                             "DLT_CT_ID":unique_template_id, # Template Id
#                                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                                         }
#                                                     ]
#                                                 }

#                                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                                         response = requests.post(url, json = data_temp)

#                                     sms_response = sendSMS(str(contact), message)
#                                 if response.status_code == 200:
#                                     total_sms_avilable_new = 0
#                                     if customer:
#                                         total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
#                                         subscription_object.total_sms_avilable = total_sms_avilable_new
#                                     else:
#                                         total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
#                                         subscription_object.total_sms_avilable = total_sms_avilable_new

#                                     subscription_object.save()

#                                     bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
#                                     return JsonResponse({'status' : 'error', 'message': "Sms sent successfully"}, status=200)
#                                 else:
#                                     bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
#                                     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                                
#                             else:
#                                 return JsonResponse({'status' : 'error', 'message': "Customers Not Found"}, status=400)
#                         elif customer_city_value_new != '' and customer_area_value_new == '':
#                             users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new)
#                             if users:
#                                 customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new).count()
#                                 customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
#                                 customer_addresswise_count = customer_count

#                                 for u in users:
#                                     contact = u.mobile_no
#                                     if contact:
        
#                                         ts = int(time.time())

#                                         data_temp = {
#                                                 "keyword":"Bill Delivery SMS",
#                                                 "timeStamp":ts,
#                                                 "dataSet":
#                                                     [
#                                                         {
#                                                             "UNIQUE_ID":"GB-" + str(ts),
#                                                             "MESSAGE": message,
#                                                             "OA":smsheader,
#                                                             "MSISDN": contact, # Recipient's Mobile Number
#                                                             "CHANNEL":"SMS",
#                                                             "CAMPAIGN_NAME":"hind_user",
#                                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                                             "USER_NAME":"hind_hsi",
#                                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                                             "DLT_CT_ID":unique_template_id, # Template Id
#                                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                                         }
#                                                     ]
#                                                 }

#                                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                                         response = requests.post(url, json = data_temp)

                                        
                                    
#                                     sms_response = sendSMS(str(contact), message)
#                                 if response.status_code == 200:
#                                     total_sms_avilable_new = 0
#                                     if customer:
#                                         total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
#                                         subscription_object.total_sms_avilable = total_sms_avilable_new
#                                     else:
#                                         total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
#                                         subscription_object.total_sms_avilable = total_sms_avilable_new

#                                     subscription_object.save()

#                                     bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
#                                     return JsonResponse({'status' : 'error', 'message': "SMS sent successfully"}, status=200)
#                                 else:
#                                     bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
#                                     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                                
#                             else:
#                                 return JsonResponse({'status' : 'error', 'message': "Customers Not Found"}, status=400)
#                         elif customer_city_value_new == '' and customer_area_value_new == '':
#                             users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new)
#                             if users:
#                                 customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new).count()
#                                 customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
#                                 customer_addresswise_count = customer_count

#                                 for u in users:
#                                     contact = u.mobile_no
#                                     if contact:
        
#                                         ts = int(time.time())

#                                         data_temp = {
#                                                 "keyword":"Bill Delivery SMS",
#                                                 "timeStamp":ts,
#                                                 "dataSet":
#                                                     [
#                                                         {
#                                                             "UNIQUE_ID":"GB-" + str(ts),
#                                                             "MESSAGE": message,
#                                                             "OA":smsheader,
#                                                             "MSISDN": contact, # Recipient's Mobile Number
#                                                             "CHANNEL":"SMS",
#                                                             "CAMPAIGN_NAME":"hind_user",
#                                                             "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
#                                                             "USER_NAME":"hind_hsi",
#                                                             "DLT_TM_ID":"1001096933494158", # TM ID
#                                                             "DLT_CT_ID":unique_template_id, # Template Id
#                                                             "DLT_PE_ID":"1001659120000037015" # PE ID 
#                                                         }
#                                                     ]
#                                                 }

#                                         url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

#                                         response = requests.post(url, json = data_temp)
                                    
#                                     sms_response = sendSMS(str(contact), message)
#                                 if response.status_code == 200:
#                                     total_sms_avilable_new = 0
#                                     if customer:
#                                         total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
#                                         subscription_object.total_sms_avilable = total_sms_avilable_new
#                                     else:
#                                         total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
#                                         subscription_object.total_sms_avilable = total_sms_avilable_new

#                                     subscription_object.save()

#                                     bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
#                                     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
#                                 else:
#                                     bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
#                                     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                                
#                             else:
#                                 return JsonResponse({'status' : 'error', 'message': "Customers Not Found"}, status=400)

#                         else:
#                             return JsonResponse({'status' : 'error', 'message': "Customers in this area not found."}, status=400)
#                 else:
#                     return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
#             else:
#                 return JsonResponse({'status' : 'error', 'message': "You don't have active Promotional SMS plan. Please purchase and try again."}, status=400)
            
#         return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)
   



# class GetSMSHeaderList(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         user_id = request.POST['user_id']
#         type_header = request.POST['header_type']

#         header_data = []
#         header = smsHeaderModel.objects.filter(request_user=user_id,Active_status=True,status='Approved',header_type=type_header)
#         for head in header:
#             header_data.append({
#                 'id':head.id,
#                 'status': head.status,
#                 'header_content' : head.header_content,
#                 'created_at' : datetime.strptime(str(head.created_at.date()), '%Y-%m-%d').strftime('%Y-%m-%d'),
#             })

#         if header_data:
#             return JsonResponse({'status': 'success', 'data' : header_data}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class GetSMSTemplateList(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user_id = request.POST['user_id']
#         smsheader = request.POST['SMSheader']

#         Template = templateContentModel.objects.filter(request_user = user_id, status='Approved')
#         list1 = []
#         filtered_city_list = []

#         for obj in Template:
#             if obj.sms_header:
#                 if smsheader in obj.sms_header:
#                     list1.append({
#                         "id": obj.id,
#                         "status": obj.status,
#                         "template_content": obj.template_content,
#                         "created_at": datetime.strptime(str(obj.created_at.date()), '%Y-%m-%d').strftime('%Y-%m-%d'),
#                     })


#         # user_id = request.POST['user_id']
#         # sms_header = request.POST['SMSheader']

#         # template_data = []
#         # templates = templateContentModel.objects.filter(request_user=user_id,status='Approved')
#         # for temp in templates:
#         #     template_data.append({
#         #         'id':temp.id,
#         #         'status': temp.status,
#         #         'template_content' : temp.template_content,
#         #         'created_at' : datetime.strptime(str(temp.created_at.date()), '%Y-%m-%d').strftime('%Y-%m-%d'),
#         #     })

#         if list1:
#             return JsonResponse({'status': 'success', 'data' : list1}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)

# class GetCustomerCountByStateCityArea(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         customer_state_value = request.POST['customer_state_value']
#         customer_city_value = request.POST['customer_city_value']
#         customer_area_value = request.POST['customer_area_value']

#         list1 = []

#         total_count = 0

#         if customer_state_value:
#             total_count = total_count + (GreenBillUser.objects.filter(c_state = customer_state_value,is_customer=True).count())
#         elif customer_city_value:
#             total_count = total_count + (GreenBillUser.objects.filter(c_city = customer_city_value,is_customer=True).count())
#         elif customer_area_value:
#             total_count = total_count + (GreenBillUser.objects.filter(c_area = customer_area_value, is_customer=True).count())


#         if total_count:
#             return JsonResponse({'status': 'success', 'data' : total_count}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class GetCustomerState(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         states_data = []
#         states = GreenBillUser.objects.values('c_state').distinct()
#         # print(states,'states')
#         for i in states:
#             if i['c_state'] != '':
#                 states_data.append(i)

#         # for state in states:
#         #     states_data.append({
#         #         'id':state.id,
#         #         'states': state.status,
#         #         'template_content' : temp.template_content,
#         #         'created_at' : datetime.strptime(str(temp.created_at.date()), '%Y-%m-%d').strftime('%Y-%m-%d'),
#         #     })

#         if states_data:
#             return JsonResponse({'status': 'success', 'data' : states_data}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class GetCustomerCityByState(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         state_value = request.POST['state_value']

#         customer_state_value_new = state_value.split(",")
#         filtered_city_list = []

#         for cust_state in customer_state_value_new:
#             cus_state_id = GreenBillUser.objects.filter(c_state = cust_state).values('c_city').distinct()
#             for city in cus_state_id:
#                 if city['c_city'] != '':
#                     filtered_city_list.append(city)
            

#         if filtered_city_list:
#             return JsonResponse({'status': 'success', 'data' : filtered_city_list}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)


# class GetCustomerAreaByCity(generics.GenericAPIView):
#     def post(self, request):

#         city_value = request.POST['city_value']

#         customer_city_value_new = city_value.split(",")
#         filtered_area_list = []

#         for area in customer_city_value_new:
#             cust_id = GreenBillUser.objects.filter(c_city=area).values('c_area').distinct()
            
#             for area in cust_id:
#                 if area['c_area'] != '' or area['c_area'] != None:
#                     filtered_area_list.append(area)
                

#         if filtered_area_list:
#             return JsonResponse({'status': 'success', 'data' : filtered_area_list}, status=200)
#         else:
#             return JsonResponse({'status': 'error'}, status=400)



# class SubscriptionPurchasedSuccess(generics.GenericAPIView):
#     def post(self, request):
#         status=request.POST["status"]
#         firstname=request.POST["firstname"]
#         amount= request.POST["amount"]
#         txnid=request.POST["txnid"]
#         posted_hash=request.POST["hash"]
#         key=request.POST["key"]
#         productinfo=request.POST["productinfo"]
#         email=request.POST["email"]
#         udf1 = request.POST["lastname"] # subscription id
#         subscription_id = request.POST["lastname"]
#         udf2 = request.POST["address2"] # user id
#         user_id = request.POST["address2"] # user id
#         udf3 = request.POST["udf3"] # encoded password
#         udf4 = request.POST["udf4"] # decode key id
#         udf5 = request.POST["udf5"] # Business Ids
#         udf6 = request.POST["udf6"]
#         business_ids = udf5

#         mihpayid = request.POST["mihpayid"]

#         success_url = "http://157.230.228.250/payment-success-message/"
#         fail_url = "http://157.230.228.250/payment-fail-message/"


#         if productinfo == 'Green Bill Subscription':
#             # print('Green Bill')

#             SALT="7ViVXMy1" # Production Salt

#             merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

#             merchant_object = GreenBillUser.objects.get(id=merchant_id)

#             # user_object =  GreenBillUser.objects.get(id=user_id)

#             retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

#             hash_string = retHashSeq.encode('utf-8')
            
#             hashh = hashlib.sha512(hash_string).hexdigest().lower()
#             # print('hashh',hashh)

#             if status == "success":
#                 # print('status')

#                 if posted_hash:
#                     # print('hash')

#                     subscription_object = subscription_plan_details.objects.get(id=subscription_id)
#                     # print('subscription_object',subscription_object)

#                     valid_for_month = subscription_object.valid_for_month
#                     per_bill_cost = subscription_object.per_bill_cost
#                     per_receipt_cost = subscription_object.per_receipt_cost
#                     per_cash_memo_cost = subscription_object.per_cash_memo_cost
#                     per_digital_bill_cost = subscription_object.per_digital_bill_cost
#                     per_digital_receipt_cost = subscription_object.per_digital_receipt_cost
#                     per_digital_cash_memo_cost = subscription_object.per_digital_cash_memo_cost

#                     total_amount = float(subscription_object.recharge_amount)
#                     subscription_plan_cost = float(subscription_object.subscription_plan_cost)

#                     today = date.today()
#                     d1 = today.strftime("%d-%m-%Y")
#                     start_date = datetime.strptime(d1, "%d-%m-%Y")
#                     delta_period = int(subscription_object.valid_for_month)
#                     end_date = start_date + relativedelta(months=delta_period)
#                     expiry_date = end_date.strftime("%d-%m-%Y")

#                     business_ids_list = list(business_ids.split(","))

#                     subscription_available_referral_count = 0

#                     subscription_available_referral_count = merchant_subscriptions.objects.filter(merchant_id = merchant_object).count()

#                     for business_id in business_ids_list:
#                         startswith = str(business_id) + ','
#                         endswith = ','+ str(business_id)
#                         contains = ','+ str(business_id) + ','
#                         exact = str(business_id)

#                         try:
#                             check_subscription_available = merchant_subscriptions.objects.get(
#                                 Q(merchant_id = merchant_object),
#                                 Q(is_active = True),
#                                 Q(business_ids__startswith = startswith) | 
#                                 Q(business_ids__endswith = endswith) | 
#                                 Q(business_ids__contains = contains) | 
#                                 Q(business_ids__exact = exact)
#                             )
#                         except:
#                             check_subscription_available = ""



#                         if check_subscription_available:

#                             business_ids_list_temp = list((check_subscription_available.business_ids).split(","))
                            
#                             business_ids_list_temp.remove(business_id)

#                             business_ids_new = ""

#                             business_ids_new = ','.join(business_ids_list_temp)
                            
#                             update_result = merchant_subscriptions.objects.filter(id = check_subscription_available.id).update(business_ids = business_ids_new)

#                             get_updated_suscription = merchant_subscriptions.objects.get(id = check_subscription_available.id)

#                             if get_updated_suscription.business_ids == "":
#                                 merchant_subscriptions.objects.filter(id = get_updated_suscription.id).update(is_active = False)

#                     subscription_active_status = True

#                     subscription =  merchant_subscriptions.objects.create(
#                         subscription_id = subscription_object.id,
#                         subscription_name = subscription_object.subscription_name,
#                         merchant_id = merchant_object,
#                         business_ids = business_ids,

#                         valid_for_month = valid_for_month,

#                         per_bill_cost = per_bill_cost,
#                         per_receipt_cost = per_receipt_cost,
#                         per_cash_memo_cost = per_cash_memo_cost,

#                         per_digital_bill_cost = per_digital_bill_cost,
#                         per_digital_receipt_cost = per_digital_receipt_cost,
#                         per_digital_cash_memo_cost = per_digital_cash_memo_cost,

#                         recharge_amount = total_amount,
#                         total_amount_avilable = total_amount,
#                         is_active = subscription_active_status,

#                         purchase_cost = subscription_plan_cost,
#                         expiry_date = expiry_date,

#                         transaction_id = txnid,
#                         payu_transaction_id = mihpayid,
#                     )
#                     try:
#                         last_id = recharge_history.objects.filter().last()
#                         invoice_no = 'GB' + str(last_id.id+1)
#                     except:
#                         invoice_no = 'GB' + str(1)
                    
#                     recharge_history.objects.create(
#                         subscription_plan_id = subscription_object.id,
#                         subscription_name = subscription_object.subscription_name,
#                         merchant_id = merchant_object,
#                         business_ids = business_ids,

#                         valid_for_month = valid_for_month,

#                         per_bill_cost = per_bill_cost,
#                         per_receipt_cost = per_receipt_cost,
#                         per_cash_memo_cost = per_cash_memo_cost,

#                         per_digital_bill_cost = per_digital_bill_cost,
#                         per_digital_receipt_cost = per_digital_receipt_cost,
#                         per_digital_cash_memo_cost = per_digital_cash_memo_cost,

#                         cost = subscription_plan_cost,

#                         is_subscription_plan = True,
#                         expiry_date = expiry_date,

#                         transaction_id = txnid,
#                         payu_transaction_id = mihpayid,
#                         invoice_no = invoice_no
#                     )

#                     if merchant_object.m_used_referral_code and subscription_available_referral_count == 0:

#                         referral_object = ReferralModel.objects.get(id = 1)

#                         if referral_object.recharge_amount_per_refferal:

#                             referral_user_object = GreenBillUser.objects.get(merchant_referral_code = merchant_object.m_used_referral_code)

#                             # try:
#                             referral_merchant_subscriptions_object = merchant_subscriptions.objects.filter(merchant_id = referral_user_object, is_active = True).order_by('-id')
#                             # except:
#                             #     referral_merchant_subscriptions_object = ""

#                             if referral_merchant_subscriptions_object:
#                                 referral_merchant_subscriptions_total_amount = 0
#                                 referral_merchant_subscriptions_total_amount = float(referral_merchant_subscriptions_object[0].total_amount_avilable) + float(referral_object.recharge_amount_per_refferal)
                                
#                                 merchant_subscriptions.objects.filter(
#                                     id = referral_merchant_subscriptions_object[0].id
#                                     ).update(total_amount_avilable = referral_merchant_subscriptions_total_amount)

#                                 ReferralHistory.objects.create(
#                                     referent_mobile_no = merchant_object.mobile_no,
#                                     referral_mobile_no = referral_user_object.mobile_no,
#                                     is_referral = True,
#                                     is_referent = False,
#                                     earned_recharge_points = referral_object.recharge_amount_per_refferal
#                                 )

#                         if referral_object.recharge_amount_per_referent:
#                             subscription.total_amount_avilable = float(total_amount) + float(referral_object.recharge_amount_per_referent)
#                             subscription.save()

#                             ReferralHistory.objects.create(
#                                 referent_mobile_no = merchant_object.mobile_no,
#                                 referral_mobile_no = referral_user_object.mobile_no,
#                                 is_referral = False,
#                                 is_referent = True,
#                                 earned_recharge_points = referral_object.recharge_amount_per_referent
#                             )

#                     if subscription:
#                         return render(request,'merchant/payment_success_message/subscription_payment_success.html')
#                         # return JsonResponse({'status':'success', 'message': 'Subscription purchased Successfully.'}, status=200)

#                 else:
#                     return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#                     # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)                       
#             else:
#                 return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#                 # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)
#         else:
#             return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#             # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)  



#         if productinfo == 'Promotional Sms Subscription':
#             SALT="7ViVXMy1" # Production Salt

#             merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

#             merchant_object = GreenBillUser.objects.get(id=merchant_id)

#             user_object =  GreenBillUser.objects.get(id=user_id)

#             retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

#             hash_string = retHashSeq.encode('utf-8')
            
#             hashh = hashlib.sha512(hash_string).hexdigest().lower()

#             if status == "success":

#                 if posted_hash:

#                     subscription_object = promotional_subscription_plan_model.objects.get(id=subscription_id)

#                     total_sms = subscription_object.total_sms
#                     per_sms_cost = subscription_object.per_sms_cost
#                     total_sms_cost = float(subscription_object.total_sms_cost)
#                     subscription_plan_cost = float(subscription_object.total_sms_cost)
#                     total_sms_avilable = total_sms

#                     business_ids_list = list(business_ids.split(","))

#                     for business_id in business_ids_list:
#                         startswith = str(business_id) + ','
#                         endswith = ','+ str(business_id)
#                         contains = ','+ str(business_id) + ','
#                         exact = str(business_id)

#                         try:
#                             check_subscription_available = promotional_sms_subscriptions.objects.get(
#                                 Q(merchant_id = merchant_object),
#                                 Q(is_active = True),
#                                 Q(business_ids__startswith = startswith) | 
#                                 Q(business_ids__endswith = endswith) | 
#                                 Q(business_ids__contains = contains) | 
#                                 Q(business_ids__exact = exact)
#                             )
#                         except:
#                             check_subscription_available = ""

#                         if check_subscription_available:

#                             business_ids_list_temp = list((check_subscription_available.business_ids).split(","))
                            
#                             business_ids_list_temp.remove(business_id)

#                             business_ids_new = ""

#                             business_ids_new = ','.join(business_ids_list_temp)
                            
#                             update_result = promotional_sms_subscriptions.objects.filter(id = check_subscription_available.id).update(business_ids = business_ids_new)

#                             get_updated_suscription = promotional_sms_subscriptions.objects.get(id = check_subscription_available.id)

#                             if get_updated_suscription.business_ids == "":
#                                 promotional_sms_subscriptions.objects.filter(id = get_updated_suscription.id).update(is_active = False)

#                     subscription_active_status = True

#                     subscription =  promotional_sms_subscriptions.objects.create(
#                         subscription_id = subscription_object.id,
#                         subscription_name = subscription_object.subscription_name,
#                         merchant_id = merchant_object,
#                         business_ids = business_ids,

#                         total_sms = total_sms,
#                         per_sms_cost = per_sms_cost,

#                         total_sms_avilable = total_sms_avilable,

#                         is_active = subscription_active_status,
#                         purchase_cost = subscription_plan_cost,

#                         transaction_id = txnid,
#                         payu_transaction_id = mihpayid,
#                     )

#                     try:
#                         last_id = recharge_history.objects.filter().last()
#                         invoice_no = 'GB' + str(last_id.id+1)
#                     except:
#                         invoice_no = 'GB' + str(1)

#                     recharge_history.objects.create(
#                         subscription_plan_id = subscription_object.id,
#                         subscription_name = subscription_object.subscription_name,
#                         merchant_id = merchant_object,
#                         business_ids = business_ids,

#                         total_sms = total_sms,
#                         per_sms_cost = per_sms_cost,

#                         cost = subscription_plan_cost,

#                         is_promotional_sms_plan = True,

#                         transaction_id = txnid,
#                         payu_transaction_id = mihpayid,
#                         invoice_no = invoice_no
#                     )

#                     if subscription:
#                         return render(request,'merchant/payment_success_message/subscription_payment_success.html')
#                         # return JsonResponse({'status':'success', 'message': 'Subscription purchased Successfully.'}, status=200)
#                 else:
#                     return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#                     # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)                       
#             else:
#                 return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#                 # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)
#         else:
#             return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#             # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)


#         if productinfo == 'Transactional Sms Subscription':
#             SALT="7ViVXMy1" # Production Salt

#             merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

#             merchant_object = GreenBillUser.objects.get(id=merchant_id)

#             user_object =  GreenBillUser.objects.get(id=user_id)

#             retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

#             hash_string = retHashSeq.encode('utf-8')
            
#             hashh = hashlib.sha512(hash_string).hexdigest().lower()

#             if status == "success":

#                 if posted_hash:

#                     subscription_object = transactional_subscription_plan_model.objects.get(id=subscription_id)

#                     total_sms = subscription_object.total_sms
#                     per_sms_cost = subscription_object.per_sms_cost
#                     total_sms_cost = float(subscription_object.total_sms_cost)
#                     subscription_plan_cost = float(subscription_object.total_sms_cost)
#                     total_sms_avilable = total_sms

#                     business_ids_list = list(business_ids.split(","))

#                     for business_id in business_ids_list:
#                         startswith = str(business_id) + ','
#                         endswith = ','+ str(business_id)
#                         contains = ','+ str(business_id) + ','
#                         exact = str(business_id)

#                         try:
#                             check_subscription_available = transactional_sms_subscriptions.objects.get(
#                                 Q(merchant_id = merchant_object),
#                                 Q(is_active = True),
#                                 Q(business_ids__startswith = startswith) | 
#                                 Q(business_ids__endswith = endswith) | 
#                                 Q(business_ids__contains = contains) | 
#                                 Q(business_ids__exact = exact)
#                             )
#                         except:
#                             check_subscription_available = ""

#                         if check_subscription_available:

#                             business_ids_list_temp = list((check_subscription_available.business_ids).split(","))
                            
#                             business_ids_list_temp.remove(business_id)

#                             business_ids_new = ""

#                             business_ids_new = ','.join(business_ids_list_temp)
                            
#                             update_result = transactional_sms_subscriptions.objects.filter(id = check_subscription_available.id).update(business_ids = business_ids_new)

#                             get_updated_suscription = transactional_sms_subscriptions.objects.get(id = check_subscription_available.id)

#                             if get_updated_suscription.business_ids == "":
#                                 transactional_sms_subscriptions.objects.filter(id = get_updated_suscription.id).update(is_active = False)

#                     subscription_active_status = True

#                     subscription =  transactional_sms_subscriptions.objects.create(
#                         subscription_id = subscription_object.id,
#                         subscription_name = subscription_object.subscription_name,
#                         merchant_id = merchant_object,
#                         business_ids = business_ids,

#                         total_sms = total_sms,
#                         per_sms_cost = per_sms_cost,

#                         total_sms_avilable = total_sms_avilable,

#                         is_active = subscription_active_status,
#                         purchase_cost = subscription_plan_cost,

#                         transaction_id = txnid,
#                         payu_transaction_id = mihpayid,
#                     )
#                     try:
#                         last_id = recharge_history.objects.filter().last()
#                         invoice_no = 'GB' + str(last_id.id+1)
#                     except:
#                         invoice_no = 'GB' + str(1)
#                     recharge_history.objects.create(
#                         subscription_plan_id = subscription_object.id,
#                         subscription_name = subscription_object.subscription_name,
#                         merchant_id = merchant_object,
#                         business_ids = business_ids,

#                         total_sms = total_sms,
#                         per_sms_cost = per_sms_cost,

#                         cost = subscription_plan_cost,

#                         is_transactional_sms_plan = True,

#                         transaction_id = txnid,
#                         payu_transaction_id = mihpayid,
#                         invoice_no = invoice_no
#                     )

#                     if subscription:
#                         return render(request,'merchant/payment_success_message/subscription_payment_success.html')
#                         # return JsonResponse({'status':'success', 'message': 'Subscription purchased Successfully.'}, status=200)
                
#                 else:
#                     return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#                     # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)                       

#             else:
#                 return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#                 # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)
#         else:
#             return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#             # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)


#         if productinfo == "Add's On Subscription":
#             SALT="7ViVXMy1" # Production Salt

#             merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

#             merchant_object = GreenBillUser.objects.get(id=merchant_id)

#             user_object =  GreenBillUser.objects.get(id=user_id)

#             retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

#             hash_string = retHashSeq.encode('utf-8')
            
#             hashh = hashlib.sha512(hash_string).hexdigest().lower()

#             if status == "success":

#                 if posted_hash:

#                     subscription_object = add_on_plan_model.objects.get(id=subscription_id)

#                     per_bill_cost = subscription_object.per_bill_cost
#                     per_receipt_cost = subscription_object.per_receipt_cost
#                     per_cash_memo_cost = subscription_object.per_cash_memo_cost
#                     per_digital_bill_cost = subscription_object.per_digital_bill_cost
#                     per_digital_receipt_cost = subscription_object.per_digital_receipt_cost
#                     per_digital_cash_memo_cost = subscription_object.per_digital_cash_memo_cost

#                     business_id = udf5

#                     startswith = str(business_id) + ','
#                     endswith = ','+ str(business_id)
#                     contains = ','+ str(business_id) + ','
#                     exact = str(business_id)

#                     try:
#                         check_subscription_available = merchant_subscriptions.objects.get(
#                             Q(merchant_id = merchant_object),
#                             Q(is_active = True),
#                             Q(business_ids__startswith = startswith) | 
#                             Q(business_ids__endswith = endswith) | 
#                             Q(business_ids__contains = contains) | 
#                             Q(business_ids__exact = exact)
#                         )
#                     except:
#                         check_subscription_available = ""

#                     if check_subscription_available:

#                         total_amount = float(check_subscription_available.total_amount_avilable) + float(subscription_object.recharge_amount)

#                         subscription =  merchant_subscriptions.objects.filter(id = check_subscription_available.id).update(

#                             per_bill_cost = per_bill_cost,
#                             per_receipt_cost = per_receipt_cost,
#                             per_cash_memo_cost = per_cash_memo_cost,

#                             per_digital_bill_cost = per_digital_bill_cost,
#                             per_digital_receipt_cost = per_digital_receipt_cost,
#                             per_digital_cash_memo_cost = per_digital_cash_memo_cost,

#                             total_amount_avilable = total_amount,

#                         )
#                         try:
#                             last_id = recharge_history.objects.filter().last()
#                             invoice_no = 'GB' + str(last_id.id+1)
#                         except:
#                             invoice_no = 'GB' + str(1)
#                         recharge_history.objects.create(
                            
#                             subscription_plan_id = subscription_object.id,
#                             subscription_name = subscription_object.add_on_name,
#                             merchant_id = merchant_object,
#                             business_ids = business_id,

#                             per_bill_cost = per_bill_cost,
#                             per_receipt_cost = per_receipt_cost,
#                             per_cash_memo_cost = per_cash_memo_cost,

#                             per_digital_bill_cost = per_digital_bill_cost,
#                             per_digital_receipt_cost = per_digital_receipt_cost,
#                             per_digital_cash_memo_cost = per_digital_cash_memo_cost,

#                             cost = subscription_object.recharge_amount,

#                             is_add_on_plan = True,

#                             transaction_id = txnid,
#                             payu_transaction_id = mihpayid,
#                             invoice_no = invoice_no

#                         )

#                         if subscription:
#                             return render(request,'merchant/payment_success_message/subscription_payment_success.html')
#                             # return JsonResponse({'status':'success', 'message': 'Add On purchased Successfully'}, status=200)

#                 else:
#                     return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#                     # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)                       

#             else:
#                 return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#                 # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)
#         else:
#             return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#             # return JsonResponse({'status' : 'error', 'message': "Fail to Purchase."}, status=400)


# class SubscriptionPurchasedFailed(generics.GenericAPIView):
#     def post(self, request):
#         status=request.POST["status"]
#         udf2 = request.POST["address2"]
#         if status == "success":
#             return render(request,'merchant/payment_success_message/subscription_payment_success.html')

#         if status == "error":
#             return render(request,'merchant/payment_success_message/subscription_payment_failed.html')
#         return render(request,'merchant/payment_success_message/subscription_payment_failed.html')


# class SubscriptionBuyButtonInfo(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):

#         user_id = request.POST['user_id']
#         business_ids = request.POST['business_ids']
#         plan_id = request.POST['plan_id']
    
#         data=[]
#         subscription = subscription_plan_details.objects.get(id=plan_id)
#         user_object = GreenBillUser.objects.get(id=user_id)
#         key="IUZdcF"
#         SALT="7ViVXMy1"
#         PAYU_BASE_URL = "https://secure.payu.in/_payment"

#         action = PAYU_BASE_URL

#         enc_key = Fernet.generate_key()
#         fernet = Fernet(enc_key)
#         password = user_object.password
#         encPassword = fernet.encrypt(password.encode())

#         merchant_subscriptions_key = merchant_subscriptions_keys.objects.create(key = enc_key.decode("utf-8"))

#         firstname = str(user_object.first_name)

#         if user_object.email != "":
#             email = str(user_object.email)
#         else:
#             email = "support@greenbill.in"
        
#         phone = str(user_object.mobile_no)

#         surl = "http://157.230.228.250/subscription-purchased-success/"

#         furl = "http://157.230.228.250/subscription-purchased-fail/"


#         udf1 = ""
#         udf2 = ""
#         udf3 = ""
#         udf4 = ""
#         udf5 = ""
#         udf6 = ""

#         posted={}

#         for i in request.POST:
#             posted[i]=request.POST[i]

#         random_str =  random.randint(9999999, 99999999)

#         hash_object = hashlib.sha256(b'randint(0,20)' + bytes(subscription.id) + bytes(user_object.id) + bytes(random_str))

#         txnid=hash_object.hexdigest()[0:20]

#         hashh = ''
#         posted['txnid']=txnid
#         posted['key']=key
#         productinfo = str("subscription_name-"+ subscription.subscription_name)
#         amount = str(subscription.subscription_plan_cost)

#         udf1 = str(subscription.id) # subscription id
        
#         udf2 = str(user_object.id) # user object

#         udf3 = str(encPassword.decode("utf-8")) # encoded Password

#         udf4 = str(merchant_subscriptions_key.id) # decode key id

#         udf5 = str(business_ids) # Business Ids

#         udf6 = ""

#         hashSequence = key + "|" + txnid + "|" + amount + "|" + productinfo + "|" + firstname + "|" + email + "|" + udf1 + "|" + udf2 + "|" + udf3 + "|" + udf4 + "|" + udf5 + "|" + udf6 + "|||||" + SALT

#         hash_string = hashSequence.encode('utf-8')

#         hashh = hashlib.sha512(hash_string).hexdigest().lower()

#         data.append({
#             "MERCHANT_KEY": key,
#             "firstname" : firstname,
#             "email" : email,
#             "phone": phone,
#             "surl": surl,
#             "furl" : furl,
#             "hashh":hashh,
#             "posted":posted,
#             "txnid":txnid,
#             "hash_string":str(hash_string),
#             "amount":amount,
#             "productinfo":productinfo,
#             "udf1":udf1,
#             "udf2":udf2,
#             "udf3":udf3,
#             "udf4":udf4,
#             "udf5":udf5,
#             "udf6":udf6,
#             "subscription_id": subscription.id,
#             "action":action,
#             })

#         if data:
#             return JsonResponse({'status':'success', 'data': data}, status=200)
#         else:
#             return JsonResponse({'status' : 'error', 'message': "Fail to Retrieve Data."}, status=400)


# class GetBusinessNameByCategory(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user_id = request.POST['user_id']
#         merchant_business_category = request.POST['merchant_business_category']

#         merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']
#         all_business = MerchantProfile.objects.filter(m_user=merchant_id)

#         business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)
     
#         merchant_state = business_object.m_state

#         result = []
#         for active_category in all_business:
#             business_name = active_category.m_business_name + "("+ active_category.m_area +")"
#             if int(merchant_business_category) == 11:
#                 if int(active_category.m_business_category.id) == int(merchant_business_category):
#                     result.append({
#                         'id':active_category.id,
#                         'business_name':business_name
#                     })
#             elif int(merchant_business_category) == 12:
#                 if int(active_category.m_business_category.id) == int(merchant_business_category):
#                     result.append({
#                         'id':active_category.id,
#                         'business_name':business_name
#                     })
#             elif int(active_category.m_business_category.id) != 11 and int(active_category.m_business_category.id) != 12:
#                 result.append({
#                     'id':active_category.id,
#                     'business_name':business_name
#                 })


#         if result:
#             return JsonResponse({'status':'success', 'data': result}, status=200)
#         else:
#             return JsonResponse({'status' : 'error', 'message': "No Data Found."}, status=400)

            

        
# class MerchantParkingPassList(generics.GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         m_business_id = request.POST['m_business_id']

#         result = ParkingLotPass.objects.filter(m_business_id = m_business_id).order_by('-id')

#         data = []

#         # today = date.today()
#         for parkingPass in result:

#             try:
#                 business_name = MerchantProfile.objects.filter(id = parkingPass.m_business_id).values('m_business_name')[0]['m_business_name']
#             except:
#                 business_name = ""

#             base_url = "http://157.230.228.250/"

#             try:
#                 m_business = MerchantProfile.objects.filter(id = parkingPass.m_business_id)
                
#                 if m_business[0].m_business_logo:
#                     business_logo = str(base_url) + str(m_business[0].m_business_logo.url)
#                 else:
#                     business_logo = ""
#             except:
#                 business_logo = ""

#             # if parkingPass.valid_to >= today:
#             data.append({
#                         "id": parkingPass.id,
#                         "business_name": business_name,
#                         "business_logo": business_logo,
#                         "mobile_no": parkingPass.mobile_no,
#                         "amount": parkingPass.amount,
#                         "vehical_no": parkingPass.vehical_no,
#                         "valid_from": datetime.strptime(str(parkingPass.valid_from,), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                         "valid_to": datetime.strptime(str(parkingPass.valid_to), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                         "comments": parkingPass.comments,
#                         "vehical_no" : parkingPass.vehical_no,
#                         "created_at" : parkingPass.created_at,
#                         "pass_type": parkingPass.pass_type,
#                         "company_id": parkingPass.company_id,
#                         "company_name": parkingPass.company_name,
#                         "vehicle_type": parkingPass.vehicle_type
#                     })

#         if result:
#             return JsonResponse({'status': "success", 'data': data}, status=200)
#         else:
#             return JsonResponse({'status': "error", 'message': "Data not available !!!"}, status=400)


# class CreateMerchantPaymentSetting(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         m_business_id = request.POST['m_business_id']

#         payu_key = request.POST['payu_key']

#         payu_salt = request.POST['payu_salt']

#         Result = MerchantPaymentSetting.objects.update_or_create(m_business_id = m_business_id, defaults={'payu_key': payu_key, 'payu_salt': payu_salt })

#         if Result:
#             return JsonResponse({'status': 'success', 'message': 'Payment Setting Stored Successfully !!!'}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Fail to Create !!!'}, status=400)


# class ShowMerchantPaymentSetting(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         m_business_id = request.POST['m_business_id']

#         try:
#             data = MerchantPaymentSetting.objects.get(m_business_id = m_business_id)
#         except:
#             data = ""
#         if data: 
#             payu_key = data.payu_key
#             payu_salt = data.payu_salt
#         else: 
#             payu_key = ""
#             payu_salt = ""


#         if data:
#             return JsonResponse({'status': "success", "payu_key":payu_key, "payu_salt":payu_salt}, status=200)

#         else:
#             return JsonResponse({'status': "success", "payu_key":payu_key, "payu_salt":payu_salt}, status=200)



# class MerchantNoticeBoardList(generics.GenericAPIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         user_id = request.POST['user_id']

#         notice_details = []

#         notice_data = OwnerSentNotice.objects.filter(user_id=GreenBillUser.objects.get(id = user_id)).order_by('-id')

#         for notice in notice_data:

#             notification_list = OnwerNoticeBoard.objects.filter(id=notice.notice_id_id).order_by('-id')
            
#             for notification in notification_list:
#                 owner_user_object = GreenBillUser.objects.filter(mobile_no = notification.owner_id)

#                 if notification.notice_file:
#                     notice_file = notification.notice_file.url
#                 else:
#                     notice_file = ""

#                 notice_details.append({
#                     'id': notification.id,
#                     'name' : owner_user_object[0].first_name + " " + owner_user_object[0].last_name,
#                     'notice_title': notification.notice_title,
#                     'message':notification.message,
#                     'notice_file': notice_file,
#                     'created_at' : timezone.localtime(notification.created_at).strftime("%d-%m-%Y"),
#                      })

#         notice_data = merchant_notice_sent.objects.filter(user_id=GreenBillUser.objects.get(id = user_id)).order_by('-id')
    
#         for notice in notice_data:
            
#             notification_list = Merchant_Notice_Model.objects.filter(id=notice.notice_id_id).order_by('-id')

#             for notification in notification_list:

#                 if notification.notice_file:
#                     notice_file = notification.notice_file.url
#                 else:
#                     notice_file = ""
                    
#                 owner_user_object = GreenBillUser.objects.filter(mobile_no = notification.owner_id)
#                 notice_details.append({
#                     'id': notification.id,
#                     'name' : owner_user_object[0].first_name + " " + owner_user_object[0].last_name,
#                     'notice_title': notification.notice_title,
#                     'message':notification.message,
#                     'notice_file': notice_file,
#                     'created_at' :  timezone.localtime(notification.created_at).strftime("%d-%m-%Y"),
#                     })

#         if notice_details:
#             return JsonResponse({'status': 'success', 'data' : notice_details}, status=200)
#         else:
#             return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)

# @csrf_exempt
# def GetUserCitiesByStates(request):

#     if request.method == "POST":

#         selected_state = request.POST.get('state')

#         states = StateCityData.objects.values('state').distinct().order_by('state')

#         states_list = []

#         cities_list = []

#         for obj in states:
#             states_list.append(obj)

#         if selected_state:

#             list1 = []

#             user_state = StateCityData.objects.filter(state = selected_state)

#             for city in user_state:
#                 list1.append({
#                     "c_city": city.city
#                 })
                
#             for x in list1:
#                 if x['c_city'] not in cities_list:
#                     if x['c_city'] != '':
#                         cities_list.append({"city": x['c_city']})


#             cities_list.sort(key = lambda x: x['city'])


#         if states:
#             return JsonResponse({'status': 'success', 'states' : states_list, 'cities': cities_list}, status=200)
#         else:
#             return JsonResponse({'status': "error", 'message': "Failed to get Data"}, status=400)