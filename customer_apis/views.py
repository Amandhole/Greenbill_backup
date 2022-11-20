import random
import os
import base64
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
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
from users.models import GreenBillUser, UserProfileImage
from .serializers import *
from django.contrib.auth import update_session_auth_hash
from datetime import datetime,date
from django.utils import formats
from authentication.models import otp_validation
from django.conf import settings
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from green_points.models import GreenPointsModel
from merchant_software_apis.models import *
from category_and_tags.models import bill_category, bill_tags
from users.models import MerchantProfile
from .models import *
from parking_lot_apis.models import ParkingLotPass, SaveParkingLotBill
from petrol_pump_apis.models import SavePetrolPumpBill
from django.db.models import Q
from merchant_cashmemo_design.models import Cash_Memo_Design_Model, CustomerCashMemoDetailModels, CustomerReceiptDetailsModels
from customer_bill.models import *

from .models import *
import random
import string

from bill_design.models import *

from coupon.models import *

from share_a_word.models import *

from suggest_a_brand.models import *

from feedback.models import *

import json
from supports_faq.models import *

# SMS
import requests
import time
import pyshorteners

from offers.models import *

from green_points.models import *

from super_admin_settings.models import GreenPointsEarnedHistory, GreenPointsSettings

from super_admin_settings.models import notification_settings

from django.utils.dateparse import parse_date
from rest_framework.decorators import api_view
from django.utils.functional import SimpleLazyObject



# from customer_apis.serializers import CustmomerInfoSerializer

# customer-info view 

@csrf_exempt
def cust_info_api(request):
    try :
        # print("Inside try")
        if request.method == "POST":
            # print("Inside post !!!!!!!!!!!!!!!")
            # received_json_data = json.loads(request.body.decode("utf-8"))
            p = request.POST['user_id']
            # print(p)
            mobile_no = request.POST['cust_mobile_num']
            # print(p)
            try:
                # print("Prrrrrrrrrrrrrrrrrrrrrr!!!!!!!!!!!!")
                user_object = GreenBillUser.objects.get(id = p)
            except:
                return JsonResponse({'status':'ffff !!!'})
            
            
            try:
                # print("Printing !!!!")
                mer_user_id = Merchant_users.objects.get(user_id = user_object)
            except:
                return JsonResponse({'status':'errorrr !!!'})


            # print("Merchat done !!",mer_user_id)
            merchant_object = mer_user_id.merchant_user_id
            
            merchant_business_object = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

            merchant_business_id = merchant_business_object.id

            parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False).order_by('-id')
            petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id).order_by('-id')
            customer_bill_list = CustomerBill.objects.filter(business_name = merchant_business_object, customer_added = False).order_by('-id')
            merchant_bill_list = MerchantBill.objects.filter(business_name = merchant_business_object, customer_added = False).order_by('-id')
            merchant_added_customer_list = Customer_Info_Model.objects.filter(mer_id = merchant_object,merchant_business_id=merchant_business_id).order_by('-id')

            # print("All  done !!")
            
            is_customer = Customer_Info_Model.objects.filter(cust_mobile_num = mobile_no)
            is_customer1 = GreenBillUser.objects.filter(mobile_no = mobile_no)

            # print("Inside eevert done !!")
            # print(len(is_customer))
            if len((is_customer))>0:
                # sweetify.error(request, title="Soory", icon='error', text='Number is already exists', timer=1500)
                return JsonResponse({'status':'Number already exists !! '})

            else:
                try:
                    # user = Customer_Info_Model.objects.update_or_create(
                    #     mer_id=mer_user_id.merchant_user_id,
                    #     merchant_business_id =merchant_business_object,
                    #     cust_first_name= received_json_data['cust_first_name'],
                    #     cust_last_lname=  received_json_data['cust_last_lname'],
                    #     cust_email=received_json_data['cust_email'],
                    #     cust_mobile_num=received_json_data['cust_mobile_num'],
                    #     customer_state=received_json_data['customer_state'],
                    #     customer_city=received_json_data['customer_city'],
                    #     customer_area=received_json_data['customer_area'],
                    #     customer_pin_code=received_json_data['customer_pin_code'],

                    # )
                    user = Customer_Info_Model.objects.update_or_create(
                        mer_id=mer_user_id.merchant_user_id,
                        merchant_business_id =merchant_business_object,
                        cust_first_name= request.POST['cust_first_name'],
                        cust_last_lname=  request.POST['cust_last_lname'],
                        cust_email=request.POST['cust_email'],
                        cust_mobile_num=mobile_no,
                        customer_state=request.POST['customer_state'],
                        customer_city=request.POST['customer_city'],
                        customer_area=request.POST['customer_area'],
                        customer_pin_code=request.POST['customer_pin_code'],

                    )

                    return JsonResponse({'status':'Customer Added Successfully !!!'})
                except:
                    return JsonResponse({'status':'Error saving customer data !!!! '})


        return JsonResponse({'status':'success'})
    except:
        return JsonResponse({'status':'Failed'})
    return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


# class customer_info_api(generics.GenericAPIView):
#     # try :
#     #     serializer = CustmomerInfoSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         print(serializer.data)
#     #         return JsonResponse({'status':'success'})
#     # except:
#     #     return JsonResponse({'status':'Failed'})
#     try:
#         def post(self, request):
#             if request.method == "POST":
#                 v1 = request.POST['mer_id']
#                 v2 = request.POST['per_id']
#                 v3 = request.POST['merchant_business_id']
#                 v4 = request.POST['cust_first_name']
#                 v5 = request.POST['cust_last_lname']
#                 v6 = request.POST['cust_email']
#                 v7 = request.POST['cust_mobile_num']
#                 v8 = request.POST['customer_state']
#                 v9 = request.POST['customer_city']
#                 v10 = request.POST['customer_area']
#                 v11 = request.POST['customer_pin_code']
#                 v12 = request.POST['date_joined']
#                 print(v1,v2,v3,v4,v5,v6,v7,v8,v9)
#                 return JsonResponse({'status':'Successfully Done '})
#     except:
#         print("Not done")
#         return JsonResponse({'status':'Not Done '})

#     return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


@csrf_exempt
def customerLogin(request):
    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        password = request.POST['password']

        try:

            if GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_customer')[0]['is_customer']:

                user = authenticate(mobile_no=mobile_no, password=password)

                if user:
                    is_customer = GreenBillUser.objects.filter(
                        mobile_no=mobile_no).values('is_customer')[0]['is_customer']
                    serializer = customerSerializer(user)

                    try:
                        token = Token.objects.create(user=user)
                    except:
                        token = Token.objects.get(user_id=user.id)

                    if user is not None and is_customer:
                        return JsonResponse({'status': 'success', 'token': token.key, 'data': serializer.data}, status=200)
                    else:
                        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)
                else:
                    return JsonResponse({'status': 'error', 'message': "Invalid credentials !!!"}, status=400)
            else:
                return JsonResponse({'status': 'error', 'message': "User not register !!!"}, status=400)
        except:
            return JsonResponse({'status': 'error', 'message': "User not register !!!"}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


class customerChangePassword(generics.GenericAPIView):
    serializer_class = customerSerializer
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


# def base64_file(data, name=None):
#     _format, _img_str = data.split(';base64,')
#     _name, ext = _format.split('/')
#     if not name:
#         name = _name.split(":")[-1]
#     return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))

class setCustomerProfileData(generics.GenericAPIView):
    serializer_class = customerSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            user_id = request.POST['user_id']
            email = request.POST["email"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            c_gender = request.POST["c_gender"].lower()
            
            c_dob = request.POST["c_dob"]

            if c_dob is not None and c_dob != '' and c_dob != "":
                formatted_c_dob = datetime.strptime(c_dob, '%d-%m-%Y').strftime('%Y-%m-%d')
            else:
                formatted_c_dob = None

            c_address_1 = request.POST["c_address_1"]
            c_address_2 = request.POST["c_address_2"]
            c_area = request.POST["c_area"]
            c_state = request.POST["c_state"]
            c_pincode = request.POST["c_pincode"]
            c_city = request.POST["c_city"]
            # c_profile_image = request.FILES["c_profile_image"]

            profile = GreenBillUser.objects.filter(id=user_id).update(email=email, first_name=first_name, last_name=last_name, c_gender=c_gender,c_dob=formatted_c_dob, c_address_1=c_address_1, c_address_2=c_address_2, c_area=c_area, c_state=c_state, c_pincode=c_pincode, c_city=c_city)

            # if c_profile_image:

            #     #random_no = random.randint(9999999, 999999999)

            #     #c_profile_image = base64_file(data=c_profile_image_temp, name="profile_image"+str(random_no))

            #     image = UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "c_profile_image" : c_profile_image })

            # if profile and image :
            if profile:
                return JsonResponse({'status': 'success', 'message': "Profile edited successfully !!!"}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)

        else:
            return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


class getCustomerProfileImage(generics.GenericAPIView):

    serializer_class = customerSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            user_id = request.POST['user_id']

            if user_id:
                user = GreenBillUser.objects.get(id=user_id)

                userDetails = UserProfileImage.objects.filter(user=user_id)
                base_url = "http://157.230.228.250/"

                if user:
                    if userDetails:
                        try:
                            new_dic = {
                                'mobile_no': user.mobile_no,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'c_unique_id': user.c_unique_id,
                                'profile_image': str(base_url) + str(userDetails[0].c_profile_image.url)
                            }
                        except:
                            new_dic = {
                                'mobile_no': user.mobile_no,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'c_unique_id': user.c_unique_id,
                                'profile_image': str(base_url) + str("/media/user-profile-pic.png")
                            }
                    else:

                        new_dic = {
                            'mobile_no': user.mobile_no,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'c_unique_id': user.c_unique_id,
                            'profile_image': str(base_url) + str("/media/user-profile-pic.png")
                        }
                    return JsonResponse({'status': "success", 'data': new_dic}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "User not found"}, status=400)
            else:
                return JsonResponse({'status': "error", 'message': "User id is mandatory."}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "Something went wrong."}, status=400)

@csrf_exempt   
class GetCustomerLoyeltyPoints(generics.GenericAPIView):

    serializer_class = customerSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            mobile_no = request.POST["mobile_no"]

            if Loyeltypoints.objects.get(mobile_no=mobile_no).loyeltyPoints:
                loyelty_pt = Loyeltypoints.objects.get(mobile_no=mobile_no).loyeltyPoints

                return JsonResponse({'status': "success", 'data': loyelty_pt}, status=200)
            else:
                return JsonResponse({'status': "error", 'message': "No Record found"}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "User not found"}, status=400)

class setCustomerProfileImage(generics.GenericAPIView):

    serializer_class = customerSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            user_id = request.POST['user_id']
            c_profile_image = request.FILES["c_profile_image"]

            if user_id and c_profile_image:

                #random_no = random.randint(9999999, 999999999)
                #m_profile_image = base64_file(data=m_profile_image_temp, name="profile_image"+str(random_no))

                image = UserProfileImage.objects.update_or_create(user_id=user_id, defaults={
                    "c_profile_image": c_profile_image})

                if image:
                    return JsonResponse({'status': "success", 'message': "Profile image uploaded successfully."}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "Failed to upload profile image."}, status=400)
            else:
                return JsonResponse({'status': "error", 'message': "user_id and c_profile_image are mandatory fields."}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "Something went wrong."}, status=400)


@csrf_exempt
def validateCustomerMobileNumber(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']

        try:
            is_customer = GreenBillUser.objects.filter(
                mobile_no=mobile_no).values('is_customer')[0]['is_customer']
        except:
            is_customer = ""

        if is_customer:
            return JsonResponse({'status': 'error', 'message': "Mobile number already registered."}, status=400)
        else:
            return JsonResponse({'status': 'success', 'message': "Mobile number not registered."}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': "Something went wrong."}, status=400)


@csrf_exempt
def generateOtpCustomer(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        signature = request.POST['signature']
        # email = request.POST['email']

        try:
            is_customer = GreenBillUser.objects.filter(
                mobile_no=mobile_no).values('is_customer')[0]['is_customer']
        except:
            is_customer = ""

        # if not mobile_exists:
        if is_customer:
            return JsonResponse({'status': 'error', 'message': "Mobile number exists as customer"}, status=400)
        else:
            if mobile_no:
                otp = random.randint(99999, 999999)
                otp_validation.objects.update_or_create(
                    mobile_no=mobile_no, defaults={'otp': otp})

                # subject = 'welcome to Green Bill'
                # message = f'Please use this OTP: {otp}'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [email,]
                # mail_res = send_mail( subject, message, email_from, recipient_list)

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
                    return JsonResponse({'status': 'error'}, status=403)
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
def ReferralCodeValidateCustomer(request):
    if request.method == "POST":
        c_used_referral_code = request.POST['c_used_referral_code']

        try:
            result = GreenBillUser.objects.get(customer_referral_code = c_used_referral_code)
        except:
            result = ""

        if result:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid Referral Code !!!'}, status=406)

@csrf_exempt
def generateOtpCustomerForgotPassword(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        signature = request.POST['signature']

        try:
            if mobile_no:
                mobile_exists = GreenBillUser.objects.get(mobile_no=mobile_no)
                is_customer = GreenBillUser.objects.filter(
                    mobile_no=mobile_no).values('is_customer')[0]['is_customer']
                email = GreenBillUser.objects.filter(
                    mobile_no=mobile_no).values('email')[0]['email']
                if mobile_exists and is_customer:
                    otp = random.randint(99999, 999999)
                    otp_validation.objects.update_or_create(mobile_no=mobile_no, defaults={'otp': otp})

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
def otpValidateCustomer(request):
    if request.method == "POST":
        temo_otp = request.POST['otp']
        mobile_no = request.POST['mobile_no']
        otp = otp_validation.objects.filter(
            mobile_no=mobile_no).values('otp')[0]['otp']

        if otp == temo_otp:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=406)

    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


@csrf_exempt
def customerRegister(request):
    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        password = request.POST['password']

        exists = GreenBillUser.objects.filter(mobile_no=mobile_no)

        if exists:
            is_merchant = GreenBillUser.objects.filter(
                mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']

            is_merchant_staff = GreenBillUser.objects.filter(
                mobile_no=mobile_no).values('is_merchant_staff')[0]['is_merchant_staff']

            is_partner = GreenBillUser.objects.filter(
                mobile_no=mobile_no).values('is_partner')[0]['is_partner']

            is_staff = GreenBillUser.objects.filter(
                mobile_no=mobile_no).values('is_staff')[0]['is_staff']
        else:
            is_merchant = False
            is_merchant_staff = False
            is_partner = False
            is_staff = False

        if is_merchant == True or is_merchant_staff == True or is_partner == True or is_staff == True:

            user = GreenBillUser.objects.get(mobile_no=mobile_no)

            email = request.POST['email']
            c_area = request.POST['c_area']
            
            c_dob = request.POST.get('c_dob',None);
            
            if c_dob:
                formatted_c_dob = datetime.strptime(c_dob, '%d-%m-%Y').strftime('%Y-%m-%d')
            else:
                formatted_c_dob = None

            c_state = request.POST["c_state"]
            c_pincode = request.POST["c_pincode"]
            c_city = request.POST['c_city']
            is_customer = 1
            is_active = 1
            unique_id = uuid.uuid4().hex[:6].upper()

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

            GreenBillUser.objects.filter(id=user.id).update(email=email, c_dob=formatted_c_dob, c_area=c_area, c_state=c_state,
                                                            c_pincode=c_pincode, c_city=c_city, is_customer=is_customer, is_active=is_active, c_unique_id=checkout_pin.upper())


            letters = string.ascii_letters
            digit = string.digits

            random_string = str(user.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
            
            customer_referral_code = random_string[0:6]

            c_used_referral_code = request.POST['c_used_referral_code']

            GreenBillUser.objects.filter(id = user.id).update(customer_referral_code = customer_referral_code, c_used_referral_code = c_used_referral_code)

            try:
                customer_referral_object = GreenBillUser.objects.get(customer_referral_code = c_used_referral_code)
            except:
                customer_referral_object = ""

            green_points_settings_object = GreenPointsSettings.objects.get(id = 1)

            if customer_referral_object:

                GreenPointsEarnedHistory.objects.create(
                    mobile_no = customer_referral_object.mobile_no,
                    referent_mobile_no = mobile_no,
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
                    mobile_no = mobile_no,
                    referent_mobile_no = mobile_no,
                    referral_mobile_no = customer_referral_object.mobile_no,
                    is_referral = False,
                    is_referent = True,
                    earned_green_points = green_points_settings_object.referral_points
                )

                try:
                    referent_green_points_object =  GreenPointsModel.objects.get(mobile_no = mobile_no)
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
                    GreenPointsModel.objects.create(mobile_no = mobile_no, green_points_count = total_green_points)

            newUser = GreenBillUser.objects.get(id=user.id)

            temp = newUser.set_password(password)
            temp2 = newUser.save()

            update_session_auth_hash(request, user)

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

            return JsonResponse({'status': 'success', 'message': 'User created successfully !!!'}, status=200)

        elif is_merchant == False or is_merchant_staff == False or is_partner == False or is_staff == False:
            serializer = customerSerializer(data=request.POST)
            if serializer.is_valid():
                result = serializer.save()

                unique_id = uuid.uuid4().hex[:6].upper()

                user = authenticate(mobile_no=mobile_no, password=password)

                result.set_password(password)
                result.save()

                update_session_auth_hash(request, user)

                email = request.POST['email']

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

                GreenBillUser.objects.filter(
                    id=result.id).update(c_unique_id=checkout_pin.upper())

                letters = string.ascii_letters
                digit = string.digits

                random_string = str(result.id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                
                customer_referral_code = random_string[0:6]

                c_used_referral_code = request.POST['c_used_referral_code']

                GreenBillUser.objects.filter(id = result.id).update(customer_referral_code = customer_referral_code, c_used_referral_code = c_used_referral_code)

                try:
                    customer_referral_object = GreenBillUser.objects.get(customer_referral_code = c_used_referral_code)
                except:
                    customer_referral_object = ""

                green_points_settings_object = GreenPointsSettings.objects.get(id = 1)

                if customer_referral_object:

                    GreenPointsEarnedHistory.objects.create(
                        mobile_no = customer_referral_object.mobile_no,
                        referent_mobile_no = mobile_no,
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
                        mobile_no = mobile_no,
                        referent_mobile_no = mobile_no,
                        referral_mobile_no = customer_referral_object.mobile_no,
                        is_referral = False,
                        is_referent = True,
                        earned_green_points = green_points_settings_object.referral_points
                    )

                    try:
                        referent_green_points_object =  GreenPointsModel.objects.get(mobile_no = mobile_no)
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
                        GreenPointsModel.objects.create(mobile_no = mobile_no, green_points_count = total_green_points)

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

                return JsonResponse({'status': 'success', 'message': 'User created successfully !!!'}, status=200)

            else:
                return JsonResponse({'status': 'error', 'message': serializer.errors}, status=200)

        else:
            return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


@csrf_exempt
def forgotPasswordCustomer(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        new_password = request.POST['new_password']

        result = GreenBillUser.objects.filter(
            mobile_no=mobile_no).values('id')[0]['id']
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
                return JsonResponse({'status': 'error', 'message': 'User not found !!!'}, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': 'Something went wrong, Please try again later !!!'}, status=400)


class getCustomerDetails(generics.GenericAPIView):
    serializer_class = customerSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":

            mobile_no = request.POST['mobile_no']
            user_temp = GreenBillUser.objects.get(mobile_no=mobile_no)

            try:
                token = Token.objects.get(user_id=user_temp)
            except:
                token = ""

            if request.META['HTTP_AUTHORIZATION'] == str("Token " + token.key):

                if GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_customer')[0]['is_customer']:
                    user = GreenBillUser.objects.get(mobile_no=mobile_no)
                    serializer = customerSerializer(user)

                    base_url = "http://157.230.228.250"

                    try:
                        profile_image = UserProfileImage.objects.get(
                            user_id=user.id)
                        if profile_image.c_profile_image:
                            image_url = str(
                                base_url) + str(profile_image.c_profile_image.url)
                        else:
                            image_url = str(base_url) + \
                                str("/media/user-profile-pic.png")
                    except:
                        image_url = str(base_url) + \
                            str("/media/user-profile-pic.png")

                    return JsonResponse({'status': "success", 'profile_data': serializer.data, 'image_data': image_url}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "User not exists"}, status=400)
            else:
                return JsonResponse({'status': "error", 'message': "Token not valid !!!"}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)


@csrf_exempt
def removeCustomerProfileImage(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        result = UserProfileImage.objects.update_or_create(
            user_id=user_id, defaults={"c_profile_image": ""})

        if result:
            return JsonResponse({'status': "success", 'message': "Profile image removed successfully."}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to remove profile image"}, status=400)
    else:
        return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)


class getCustomerGreenPoints(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']

        user_object = GreenBillUser.objects.get(id = user_id)

        try:
            GreenPoints = GreenPointsModel.objects.filter(mobile_no=user_object.mobile_no).values(
                'green_points_count')[0]['green_points_count']

        except:
            GreenPoints = 0

        total_earned_green_points =  GetEarnedGreenPoints(user_object.mobile_no)

        total_green_points_used = GetUsedGreenPoints(user_id)
        total_available_points = int(total_earned_green_points - total_green_points_used)

        data = {
            'total_green_points_available': str(total_available_points),
            'total_earned_green_points': str(total_earned_green_points),
            'total_green_points_used': str(total_green_points_used),
        }

        if data:
            return JsonResponse({'status' : "success", 'data': data}, status=200)
        else:
            return JsonResponse({'status': "success", 'message': str(GreenPoints)}, status=200)

class getShoppingAnalysisByCategory(generics.GenericAPIView):

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]

        customer_object = GreenBillUser.objects.get(id = user_id)

        if from_date and to_date:
            customer_bill_list = CustomerBill.objects.filter(mobile_no = customer_object.mobile_no, delete_bill = False).order_by('-id')
        else:
            customer_bill_list = CustomerBill.objects.filter(mobile_no = customer_object.mobile_no, created_at__date = timezone.now(), delete_bill = False).order_by('-id')

        bills = []

        for bill in customer_bill_list:

            try:
                business_name = bill.business_name.m_business_name
            except:
                business_name = bill.custom_business_name

            try:
                bill_category_temp = bill.customer_bill_category.bill_category_name
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
            except:
                business_logo = ""


            bills.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": float(bill.bill_amount),
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%Y-%m-%d'),
                        "business_logo": business_logo,
                        "customer_added": bill.customer_added,
                        'db_table': "CustomerBill",
                        'seen_status' : bill.seen_status,
                    })

        if from_date and to_date:
            parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no, is_pass = False, delete_bill = False).order_by('-id')
        else:
            parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no, is_pass = False, created_at__date = timezone.now(), delete_bill = False).order_by('-id')

        for bill in parking_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""


            bills.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": float(bill.amount),
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%Y-%m-%d'),
                        "business_logo": business_logo,
                        "customer_added": False,
                        'db_table': "SaveParkingLotBill",
                        'seen_status' : bill.seen_status,
                    })

        if from_date and to_date:
            petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no, delete_bill = False).order_by('-id')
        else:
            petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no, created_at__date = timezone.now(), delete_bill = False).order_by('-id')

        for bill in petrol_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""


            bills.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": float(bill.total_amount),
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%Y-%m-%d'),
                        "business_logo": business_logo,
                        "customer_added": False,
                        'db_table': "SavePetrolPumpBill",
                        'seen_status' : bill.seen_status,
                    })
        

        if from_date and to_date:
            labels = []
            data = []
            data1 = []
            newdata1 = []
            newlabels = []
            from_date= datetime.strptime(request.POST["from_date"], '%Y-%m-%d').date()
            to_date= datetime.strptime(request.POST["to_date"], '%Y-%m-%d').date()

            for bill in bills:
                converted_date = parse_date(bill['bill_date'])
                if converted_date >= from_date and converted_date <= to_date:
                    if bill['bill_category_name']:
                        if bill['bill_category_name'] in labels:
                            pass
                        else:
                            labels.append(bill['bill_category_name'])

            spend_by_bill_category = {new_list: 0 for new_list in labels}

            for bill in bills:
                for x in labels:
                    if bill['bill_category_name']:
                        if bill['bill_category_name'] == x:
                            converted_date = parse_date(bill['bill_date'])
                            if converted_date >= from_date and converted_date <= to_date:
                                if bill['bill_amount']:
                                    spend_by_bill_category[x] =  spend_by_bill_category[x] + float(bill['bill_amount'])

            

            for object in spend_by_bill_category:
                data1.append(spend_by_bill_category[object])
                newdata1.append(spend_by_bill_category[object])

            newdata1.sort(reverse=True)

            for amount1 in newdata1:
                for i, amount2 in enumerate(data1):
                    if amount1 == amount2:
                        for j, category1 in  enumerate(labels):
                            if i == j:
                                newlabels.append(category1)

            for i in newdata1:
                decimal_value = format(float(i), ".2f")
                data.append(decimal_value)

            
        else:

            labels = []
            data = []
            data1 = []
            newdata1 = []
            newlabels = []

            for bill in bills:
                if bill['bill_category_name']:
                    if bill['bill_category_name'] in labels:
                        pass
                    else:
                        labels.append(bill['bill_category_name'])

            spend_by_bill_category = {new_list: 0 for new_list in labels} 

            for bill in bills:
                for x in labels:
                    if bill['bill_category_name']:
                        if bill['bill_category_name'] == x:
                            if bill['bill_amount']:
                                spend_by_bill_category[x] =  spend_by_bill_category[x] + float(bill['bill_amount'])

            # for object in spend_by_bill_category:
            #     data.append(float(spend_by_bill_category[object]))

            for object in spend_by_bill_category:
                data1.append(spend_by_bill_category[object])
                newdata1.append(spend_by_bill_category[object])

            newdata1.sort(reverse=True)

            for amount1 in newdata1:
                for i, amount2 in enumerate(data1):
                    if amount1 == amount2:
                        for j, category1 in  enumerate(labels):
                            if i == j:
                                newlabels.append(category1)

            for i in newdata1:
                decimal_value = format(float(i), ".2f")
                data.append(decimal_value)


        if data and newlabels:
            return JsonResponse({'status': 'success', 'data': data, 'labels': newlabels}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)


class getShoppingAnalysisByMerchant(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]

        # print(from_date)

        customer_object = GreenBillUser.objects.get(id = user_id)

        if from_date and to_date:
            customer_bill_list = CustomerBill.objects.filter(mobile_no=customer_object.mobile_no, delete_bill = False).order_by('-id')
        else:
            customer_bill_list = CustomerBill.objects.filter(mobile_no=customer_object.mobile_no, created_at__date = timezone.now(), delete_bill = False).order_by('-id')

        bills = []

        for bill in customer_bill_list:

            try:
                business_name = bill.business_name.m_business_name
            except:
                business_name = bill.custom_business_name

            try:
                bill_category_temp = bill.customer_bill_category.bill_category_name
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
            except:
                business_logo = ""


            bills.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": float(bill.bill_amount),
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%Y-%m-%d'),
                        "business_logo": business_logo,
                        "customer_added": bill.customer_added,
                        'db_table': "CustomerBill",
                        'seen_status' : bill.seen_status,
                    })

        if from_date and to_date:
            parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no, is_pass = False, delete_bill = False).order_by('-id')
        else:
            parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no, is_pass = False, created_at__date = timezone.now(), delete_bill = False).order_by('-id')

        for bill in parking_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""


            bills.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": float(bill.amount),
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%Y-%m-%d'),
                        "business_logo": business_logo,
                        "customer_added": False,
                        'db_table': "SaveParkingLotBill",
                        'seen_status' : bill.seen_status,
                    })

        if from_date and to_date:
            petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no, delete_bill = False).order_by('-id')
        else:
            petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no, created_at__date = timezone.now(), delete_bill = False).order_by('-id')

        for bill in petrol_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""


            bills.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": float(bill.total_amount),
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%Y-%m-%d'),
                        "business_logo": business_logo,
                        "customer_added": False,
                        'db_table': "SavePetrolPumpBill",
                        'seen_status' : bill.seen_status,
                    })

        if from_date and to_date:
            labels = []
            data = []
            data1 = []
            newdata1 = []
            newlabels = []

            # from_date = datetime.strptime(request.POST["from_date"], '%d-%m-%Y').strftime('%Y-%m-%d')
            # to_date = datetime.strptime(request.POST["to_date"], '%d-%m-%Y').strftime('%Y-%m-%d')

            # from_date_new = datetime.strptime(from_date, '%Y-%m-%d').date()
            # to_date_new = datetime.strptime(to_date, '%Y-%m-%d').date()

            # from_date = datetime.strptime(request.POST["from_date"], '%Y-%m-%d').strftime('%Y-%m-%d')
            # to_date = datetime.strptime(request.POST["to_date"], '%Y-%m-%d').strftime('%Y-%m-%d')
            from_date = datetime.strptime(request.POST["from_date"], '%Y-%m-%d').date()
            to_date = datetime.strptime(request.POST["to_date"], '%Y-%m-%d').date()
            
            for bill in bills:
                converted_date = parse_date(bill['bill_date'])
                if converted_date >= from_date and converted_date <= to_date:
                    if bill['business_name']:
                        if bill['business_name'] in labels:
                            pass
                        else:
                            labels.append(bill['business_name'])

            spend_by_bill_business = {new_list: 0 for new_list in labels} 

            for bill in bills:
                for x in labels:
                    if bill['business_name']:
                        if bill['business_name'] == x:
                            converted_date = parse_date(bill['bill_date'])
                            if converted_date >= from_date and converted_date <= to_date:
                                if bill['bill_amount']:
                                    spend_by_bill_business[x] =  spend_by_bill_business[x] + float(bill['bill_amount'])

            for object in spend_by_bill_business:
                data1.append(spend_by_bill_business[object])
                newdata1.append(float(spend_by_bill_business[object]))

            newdata1.sort(reverse=True)

            for amount1 in newdata1:
                for i, amount2 in enumerate(data1):
                    if amount1 == amount2:
                        for j, business_name1 in  enumerate(labels):
                            if i == j:
                                newlabels.append(business_name1)

            for i in newdata1:
                decimal_value = format(float(i), ".2f")
                data.append(decimal_value)
                
        else:
            labels = []
            data = []
            data1 = []
            newdata1 = []
            newlabels = []

            for bill in bills:
                if bill['business_name']:
                    if bill['business_name'] in labels:
                        pass
                    else:
                        labels.append(bill['business_name'])

            spend_by_bill_business = {new_list: 0 for new_list in labels} 

            for bill in bills:
                for x in labels:
                    if bill['business_name']:
                        if bill['business_name'] == x:
                            if bill['bill_amount']:
                                spend_by_bill_business[x] =  spend_by_bill_business[x] + float(bill['bill_amount'])

            for object in spend_by_bill_business:
                data1.append(float(spend_by_bill_business[object]))
                newdata1.append(float(spend_by_bill_business[object]))

            newdata1.sort(reverse=True)

            for amount1 in newdata1:
                for i, amount2 in enumerate(data1):
                    if amount1 == amount2:
                        for j, business_name1 in  enumerate(labels):
                            if i == j:
                                newlabels.append(business_name1)

            for i in newdata1:
                decimal_value = format(float(i), ".2f")
                data.append(decimal_value)


        if data and newlabels:
            return JsonResponse({'status': 'success', 'data': data, 'labels': newlabels}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)

class getBillCategoriesList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        bill_categories = bill_category.objects.all().order_by("bill_category_name")

        data = []

        for category in bill_categories:

            try:
                icon = category.icon.url
                icon_url = "http://157.230.228.250/" + str(icon)
            except:
                icon_url = ""

            data.append({
                'id': category.id,
                'bill_category_name': category.bill_category_name,
                'bill_category_description': category.bill_category_description,
                'icon': str(category.icon),
                'icon_url': icon_url,
            })
        
        # sorted_categories = sorted(bill_categories, key=lambda item: item.get("bill_category_name"))

        if bill_categories:
            # serializer = billCategorySerializer(bill_categories, many=True)
            # return JsonResponse({'status': "success", 'data': serializer.data}, status=200)
            return JsonResponse({'status': "success", 'data': data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)

class getBillTagsList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        mobile_no = request.POST.get('mobile')
        try:
            customer_object = GreenBillUser.objects.get(mobile_no=mobile_no, is_customer=True)
        except:
            customer_object = ''

        if customer_object:
            bill_tags_list = bill_tags.objects.filter(user_id = customer_object).order_by("bill_tags_name")
        else:
            bill_tags_list = ''
        
        if bill_tags_list:
            serializer = billTagSerializer(bill_tags_list, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)

class getMerchantBusinessList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        business_list = MerchantProfile.objects.all().order_by("m_business_name")

        if business_list:
            serializer = merchantBusinessSerializer(business_list, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)

class getCustomerBillList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST['user_id']

        data = []

        customer_object = GreenBillUser.objects.get(id = user_id)

        customer_bill_list = CustomerBill.objects.filter(mobile_no=customer_object.mobile_no).order_by('-id')

        for bill in customer_bill_list:

            try:
                business_name = bill.business_name.m_business_name
            except:
                business_name = bill.custom_business_name

            try:
                bill_category_temp = bill.customer_bill_category.bill_category_name
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
            except:
                business_logo = ""

            if bill.seen_status == False:
                data.append({
                            "id": bill.id,
                            "business_name": business_name,
                            "bill_category_name": bill_category_temp,
                            "bill_amount": bill.bill_amount,
                            "comments": bill.remarks,
                            "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                            "business_logo": business_logo,
                            "customer_added": bill.customer_added,
                            "invoice_no": bill.invoice_no,
                            'db_table': "CustomerBill",
                            'seen_status' : bill.seen_status,
                        })


        parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no, is_pass = False).order_by('-id')

        for bill in parking_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""

            if bill.seen_status == False:
                data.append({
                            "id": bill.id,
                            "business_name": business_name,
                            "bill_category_name": bill_category_temp,
                            "bill_amount": bill.amount,
                            "comments": bill.remarks,
                            "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                            "business_logo": business_logo,
                            "customer_added": False,
                            "invoice_no": bill.invoice_no,
                            'db_table': "SaveParkingLotBill",
                            'seen_status' : bill.seen_status,
                        })


        petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no).order_by('-id')

        for bill in petrol_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""

            if bill.seen_status == False:
                data.append({
                            "id": bill.id,
                            "business_name": business_name,
                            "bill_category_name": bill_category_temp,
                            "bill_amount": bill.total_amount,
                            "comments": bill.remarks,
                            "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                            "business_logo": business_logo,
                            "customer_added": False,
                            "invoice_no": bill.invoice_no,
                            'db_table': "SavePetrolPumpBill",
                            'seen_status' : bill.seen_status,
                        })

        data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

        if data:
            # serializer = customerBillListSerializer(customer_bill_list, many=True)
            return JsonResponse({"status":"success","data":data}, status=200, safe=False)
            # return JsonResponse({"status":"success","data":serializer.data}, status=200)

        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data !!!"}, status=400)

class addCustomerBill(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        bill_file = request.FILES['cust_bill']
        business_id = request.POST['business_id']
        customer_bill_category = request.POST['customer_bill_category_id']
        bill_amount = request.POST['bill_amount']
        bill_date = datetime.strptime(request.POST["bill_date"], '%d-%m-%Y').strftime('%Y-%m-%d')
        bill_tags_values = request.POST['bill_tags_values']
        remarks = request.POST['remarks']
        custom_business = request.POST['custom_business']
        invoice_no = request.POST['invoice_no']
        user_object = GreenBillUser.objects.get(id = user_id)

        # print('bill_tags_values',bill_tags_values)

        # print(custom_business)
        tags_list = []
        updated_bill_tags = ''

        if bill_tags_values:
            tags_list = bill_tags_values.split(",")
            
            updated_tags_list = []
            for tag in tags_list:
                if tag.isdigit():
                    updated_tags_list.append(tag)
                else:
                    result = bill_tags.objects.create(bill_tags_name=tag,user_id=GreenBillUser.objects.get(id=user_id),is_customer_bill_tag=1)
                    tag = result.id
                    updated_tags_list.append(tag)

            updated_bill_tags = ','.join(map(str, updated_tags_list)) 
        
        try:
            business_object = MerchantProfile.objects.get(id = business_id)
        except:
            business_object = ""

        try:
            bill_category_object = bill_category.objects.get(id = customer_bill_category)
        except:
            bill_category_object = ""

        if business_id and bill_category_object:
            result = CustomerBill.objects.create(mobile_no= user_object.mobile_no, bill= bill_file, business_name= business_object, customer_bill_category= bill_category_object, bill_amount= bill_amount, bill_date= bill_date, customer_added = True, bill_tags = updated_bill_tags, remarks = remarks, custom_business_name = custom_business,invoice_no=invoice_no)

        elif business_id:
            result = CustomerBill.objects.create(mobile_no= user_object.mobile_no, bill= bill_file, business_name= business_object, bill_amount= bill_amount, bill_date= bill_date, customer_added = True, bill_tags = updated_bill_tags, remarks = remarks, custom_business_name = custom_business,invoice_no=invoice_no)

        elif bill_category_object:
            result = CustomerBill.objects.create(mobile_no= user_object.mobile_no, bill= bill_file, customer_bill_category= bill_category_object, bill_amount= bill_amount, bill_date= bill_date, customer_added = True, bill_tags = updated_bill_tags, remarks = remarks, custom_business_name = custom_business,invoice_no=invoice_no)

        else:
            result = CustomerBill.objects.create(mobile_no= user_object.mobile_no, bill=bill_file, bill_amount= bill_amount, bill_date= bill_date, customer_added = True, bill_tags = updated_bill_tags, remarks = remarks, custom_business_name = custom_business,invoice_no=invoice_no)

        letters = string.ascii_letters
        digit = string.digits
        random_string = str(result.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
        
        CustomerBill.objects.filter(id = result.id).update(bill_url = random_string)

        if result:
            return JsonResponse({'status' : 'success', 'message' : 'Bill added successfully !'}, status=200)
        else:
            return JsonResponse({'status' : 'error', 'message' : 'Failed to add bill !!!'}, status=400)

class editCustomerBill(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        bill_id = request.POST['id']
        business_id = request.POST['business_id']
        bill_file = request.FILES['cust_bill']
        customer_bill_category = request.POST['customer_bill_category_id']
        bill_amount = request.POST['bill_amount']
        bill_date = request.POST["bill_date"]
        bill_tags_values = request.POST['bill_tags_values']
        remarks = request.POST['remarks']
        custom_business = request.POST['custom_business']
        invoice_no = request.POST['invoice_no']

        db_table = request.POST['db_table']
        tags_list = []
        
        business_object = ''
        bill_category_object=''
        updated_bill_tags = ''
        updated_tags_list = []
        if bill_tags_values:
            tags_list = bill_tags_values.split(",")
            for tag in tags_list:
                if tag.isdigit():
                    updated_tags_list.append(tag)
                else:
                    result = bill_tags.objects.create(bill_tags_name=tag,user_id=GreenBillUser.objects.get(id=user_id),is_customer_bill_tag=1)
                    tag = result.id
                    updated_tags_list.append(tag)

            updated_bill_tags = ','.join(map(str, updated_tags_list))

        try:
            business_object = MerchantProfile.objects.get(id= business_id)
        except:
            pass

        try:
            bill_category_object = bill_category.objects.get(id= customer_bill_category)
        except:
            pass


        if db_table == "CustomerBill":
            try:
                if bill_file:
                    result = CustomerBill.objects.filter(id=bill_id).update(business_name= business_object, bill= bill_file, customer_bill_category= bill_category_object, bill_amount= bill_amount, bill_tags= updated_bill_tags, remarks = remarks, custom_business_name = custom_business,invoice_no=invoice_no)
                    bill_id_object = CustomerBill.objects.get(id=bill_id)
                    bill_id_object.bill = bill_file
                    bill_id_object.save()
                else:
                    result = CustomerBill.objects.filter(id=bill_id).update(business_name=business_object, customer_bill_category=bill_category_object, bill_amount=bill_amount, bill_tags = updated_bill_tags, remarks = remarks, custom_business_name = custom_business,invoice_no=invoice_no)
            except:
                result = CustomerBill.objects.filter(id=bill_id).update(business_name=business_object, customer_bill_category=bill_category_object, bill_amount=bill_amount, bill_tags = updated_bill_tags, remarks = remarks, custom_business_name = custom_business,invoice_no=invoice_no)

        elif db_table == "SaveParkingLotBill":
            result = SaveParkingLotBill.objects.filter(id=bill_id).update(bill_category_id=customer_bill_category, bill_tags = updated_bill_tags, remarks = remarks)

        elif db_table == "SavePetrolPumpBill":
           result = SavePetrolPumpBill.objects.filter(id=bill_id).update(bill_category_id=customer_bill_category, bill_tags = updated_bill_tags, remarks = remarks)


        # if db_table == "CustomerBill":

        #     if business_id and customer_bill_category:
        #         result = CustomerBill.objects.filter(id=bill_id).update(business_name= business_object, bill= bill_file, customer_bill_category= bill_category_object, bill_amount= bill_amount, bill_date= bill_date, bill_tags= updated_bill_tags, remarks = remarks, custom_business_name = custom_business)
        #         bill_id_object = CustomerBill.objects.get(id=bill_id)
        #         bill_id_object.bill = bill_file
        #         bill_id_object.save()
                
        #     elif business_id:
        #         result = CustomerBill.objects.filter(id=bill_id).update(business_name= business_object, bill= bill_file, bill_amount= bill_amount, bill_date= bill_date, bill_tags= updated_bill_tags, remarks = remarks, custom_business_name = custom_business)
        #         bill_id_object = CustomerBill.objects.get(id=bill_id)
        #         bill_id_object.bill = bill_file
        #         bill_id_object.save()

        #     elif customer_bill_category:
        #         result = CustomerBill.objects.filter(id=bill_id).update(customer_bill_category= bill_category_object, bill= bill_file, bill_amount= bill_amount, bill_date= bill_date, bill_tags= updated_bill_tags, remarks = remarks, custom_business_name = custom_business)
        #         bill_id_object = CustomerBill.objects.get(id=bill_id)
        #         bill_id_object.bill = bill_file
        #         bill_id_object.save()
                
        #     else:
        #         result = CustomerBill.objects.filter(id=bill_id).update(bill_amount= bill_amount, bill_date= bill_date, bill_tags= updated_bill_tags, remarks= remarks, custom_business_name= custom_business)
        #         bill_id_object = CustomerBill.objects.get(id=bill_id)
        #         bill_id_object.bill = bill_file
        #         bill_id_object.save()

        # elif db_table == "SaveParkingLotBill":
        #     result = SaveParkingLotBill.objects.filter(id=bill_id).update(bill_category_id=customer_bill_category, bill_tags = updated_bill_tags, remarks = remarks)

        # elif db_table == "SavePetrolPumpBill":
        #     result = SavePetrolPumpBill.objects.filter(id=bill_id).update(bill_category_id=customer_bill_category, bill_tags = updated_bill_tags, remarks = remarks)

        if result:
            return JsonResponse({'status' : 'success', 'message' : 'Bill edited successfully !'}, status=200)
        else:
            return JsonResponse({'status' : 'error', 'message' : 'Failed to edit bill !!!'}, status=400)

class deleteCustomerBill(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        bill_id = request.POST['id']

        db_table = request.POST['db_table']

        if db_table == "CustomerBill":
            result = CustomerBill.objects.filter(id = bill_id).update(delete_bill = True)

        elif db_table == "SaveParkingLotBill":
            result = SaveParkingLotBill.objects.filter(id = bill_id).update(delete_bill = True)

        elif db_table == "SavePetrolPumpBill":
            result = SavePetrolPumpBill.objects.filter(id = bill_id).update(delete_bill = True)

        if result:
            return JsonResponse({'status' : 'success', 'message' : 'Bill deleted successfully !'}, status=200)
        else:
            return JsonResponse({'status' : 'error', 'message' : 'Failed to delete bill !!!'}, status=400)

class downloadCustomerBill(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        bill_id = request.POST['id']

        result = CustomerBill.objects.filter(id = bill_id)

        if result:
            base_url = "http://157.230.228.250"
            
            if result[0].bill:
                file = str(base_url) + str(result[0].bill.url)

            return JsonResponse({'status': 'success', 'message': file }, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)

class getBillByMerchantStore(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        business_id = request.POST['business_id']

        user_id = request.POST['user_id']

        from_date = request.POST["from_date"]

        to_date = request.POST["to_date"]

        customer_object = GreenBillUser.objects.get(id=user_id)

        data = []
        if business_id:
        
            customer_bill_list = CustomerBill.objects.filter(business_name = business_id, mobile_no=customer_object, delete_bill = False).order_by('-id')

            for bill in customer_bill_list:

                try:
                    business_name = bill.business_name.m_business_name
                except:
                    business_name = ""

                try:
                    bill_category_temp = bill.customer_bill_category.bill_category_name
                except:
                    bill_category_temp = ""

                base_url = "http://157.230.228.250/"

                try:
                    business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
                except:
                    business_logo = ""

                date_temp = datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y')

                data.append({
                            "id": bill.id,
                            "business_name": business_name,
                            "bill_category_name": bill_category_temp,
                            "bill_amount": bill.bill_amount,
                            "comments": bill.remarks,
                            "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                            "bill_date_temp": datetime.strptime(date_temp, '%d-%m-%Y'),
                            "business_logo": business_logo,
                            "customer_added": bill.customer_added,
                            "invoice_no": bill.invoice_no,
                            'db_table': "CustomerBill",
                            'seen_status' : bill.seen_status,
                            "bill_flag": False,
                            "reason": "",
                            "is_favourite": bill.is_favourite,
                        })

            parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no, m_business_id = business_id, is_pass = False, delete_bill = False).order_by('-id')

            for bill in parking_bill_list:

                try:
                    business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
                except:
                    business_name = ""

                try:
                    bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
                except:
                    bill_category_temp = ""

                base_url = "http://157.230.228.250/"

                try:
                    business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                    business_logo = str(base_url) + str(business_logo_temp.url)

                except:
                    business_logo = ""


                data.append({
                            "id": bill.id,
                            "business_name": business_name,
                            "bill_category_name": bill_category_temp,
                            "bill_amount": bill.amount,
                            "comments": bill.remarks,
                            "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                            "bill_date_temp": datetime.strptime(str(bill.date), '%d-%m-%Y'),
                            "business_logo": business_logo,
                            "customer_added": False,
                            "invoice_no": bill.invoice_no,
                            'db_table': "SaveParkingLotBill",
                            'seen_status' : bill.seen_status,
                            "bill_flag": bill.bill_flag,
                            "reason": bill.reason,
                            "is_favourite": bill.is_favourite,
                        })


            petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no, m_business_id = business_id, delete_bill = False).order_by('-id')

            for bill in petrol_bill_list:

                try:
                    business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
                except:
                    business_name = ""

                try:
                    bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
                except:
                    bill_category_temp = ""

                base_url = "http://157.230.228.250/"

                try:
                    business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                    business_logo = str(base_url) + str(business_logo_temp.url)

                except:
                    business_logo = ""


                data.append({
                            "id": bill.id,
                            "business_name": business_name,
                            "bill_category_name": bill_category_temp,
                            "bill_amount": bill.total_amount,
                            "comments": bill.remarks,
                            "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                            "bill_date_temp": datetime.strptime(str(bill.date), '%d-%m-%Y'),
                            "business_logo": business_logo,
                            "customer_added": False,
                            "invoice_no": bill.invoice_no,
                            'db_table': "SavePetrolPumpBill",
                            'seen_status' : bill.seen_status,
                            "bill_flag": bill.bill_flag,
                            "reason": bill.reason,
                            "is_favourite": bill.is_favourite,
                        })

        else:
            customer_bill_list = CustomerBill.objects.filter(business_name__isnull=True, mobile_no=customer_object, delete_bill = False).order_by('-id')
            for bill in customer_bill_list:

                if bill.custom_business_name:
                    business_name = bill.custom_business_name
                else:
                    business_name = "Others"

                try:
                    bill_category_temp = bill.customer_bill_category.bill_category_name
                except:
                    bill_category_temp = ""

                base_url = "http://157.230.228.250/"

                # try:
                #     business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
                # except:
                #     business_logo = ""

                date_temp = datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y')

                data.append({
                            "id": bill.id,
                            "business_name": business_name,
                            "bill_category_name": bill_category_temp,
                            "bill_amount": bill.bill_amount,
                            "comments": bill.remarks,
                            "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                            "bill_date_temp": datetime.strptime(date_temp, '%d-%m-%Y'),
                            "business_logo": "",
                            "customer_added": bill.customer_added,
                            "invoice_no": bill.invoice_no,
                            'db_table': "CustomerBill",
                            'seen_status' : bill.seen_status,
                            "bill_flag": False,
                            "reason": "",
                            "is_favourite": bill.is_favourite,
                        })


        sorted_data = []

        if from_date and to_date and data:
            from_date = datetime.strptime(from_date, '%d-%m-%Y')
            to_date = datetime.strptime(to_date, '%d-%m-%Y')
            # print(from_date)
            # print(to_date)
            
            # from_date_new = datetime.strptime(from_date, '%Y-%m-%d').date()
            # to_date_new = datetime.strptime(to_date, '%Y-%m-%d').date()

            for bills in data:
                if bills['bill_date_temp'] >= from_date and bills['bill_date_temp'] <= to_date:
                    sorted_data.append(bills)
        else:
            sorted_data = data

        # print(sorted_data)

        if sorted_data:
            # serializer = customerBillListSerializer(customer_bill_list, many=True)
            return JsonResponse({'status': 'success', 'data': sorted_data }, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)


class SendBillByMerchantStore(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        send_bill_id = request.POST['send_bill_id']
        send_bill_to_merchant = request.POST['business_id']
        db_table = request.POST['db_table']

        if send_bill_to_merchant:
            merchant_business_id = MerchantProfile.objects.get(id = send_bill_to_merchant)
            user_id = GreenBillUser.objects.get(mobile_no = merchant_business_id.m_user)
        
        if db_table == "CustomerBill":
            customer_bill = CustomerBill.objects.filter(id =send_bill_id)

            letters = string.ascii_letters
            digit = string.digits
            random_string = str(customer_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

            customer_bill1 = MerchantBill.objects.create(user_id = customer_bill[0].user_id, mobile_no = customer_bill[0].mobile_no, email = customer_bill[0].email,
                bill = customer_bill[0].bill, business_name = customer_bill[0].business_name, bill_received_business_name = merchant_business_id.id,
                invoice_no = customer_bill[0].invoice_no, green_bill_transaction = customer_bill[0].green_bill_transaction, green_bill_print_transaction = customer_bill[0].green_bill_print_transaction,
                print_transaction = customer_bill[0].print_transaction, bill_amount = customer_bill[0].bill_amount, customer_bill_category = customer_bill[0].customer_bill_category,stamp_id=customer_bill[0].stamp_id, exe_bill_type = customer_bill[0].exe_bill_type
            )
            customer_bill_new = MerchantBill.objects.filter(id=customer_bill1.id).update(bill_url = random_string) 

            CustomerBill.objects.filter(id =customer_bill[0].id).update(delete_bill = True)

            return JsonResponse({'status': 'success', 'message': 'Bill Transfer successfully !!!' }, status=200)

        elif db_table == "SaveParkingLotBill":
            parking_bill = SaveParkingLotBill.objects.filter(id=send_bill_id)

            try:
                business_name1 = MerchantProfile.objects.get(id = parking_bill[0].m_business_id)
            except:
                business_name1 = ""

            try:
                bill_category_temp = bill_category.objects.get(id = parking_bill[0].bill_category_id)
            except:
                bill_category_temp = ""

            customer_bill1 = MerchantBill.objects.create(user_id = parking_bill[0].user_id, mobile_no = parking_bill[0].mobile_no,
                    bill = parking_bill[0].bill_file, business_name = business_name1, bill_received_business_name = merchant_business_id.id,
                    invoice_no = parking_bill[0].invoice_no, 
                    bill_amount = parking_bill[0].amount, customer_bill_category = bill_category_temp
                )

            letters = string.ascii_letters
            digit = string.digits
            random_string = str(parking_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

            customer_bill_new = MerchantBill.objects.filter(id=customer_bill1.id).update(bill_url = random_string) 

            SaveParkingLotBill.objects.filter(id=parking_bill[0].id).update(delete_bill = True)

            return JsonResponse({'status': 'success', 'message': 'Bill Transfer successfully !!!' }, status=200)

        elif db_table == "SavePetrolPumpBill":
            
            petrol_pump = SavePetrolPumpBill.objects.filter(id=send_bill_id)

            business_name1 = MerchantProfile.objects.get(id = petrol_pump[0].m_business_id)
            

            try:
                bill_category_temp = bill_category.objects.get(id = petrol_pump[0].bill_category_id)
            except:
                bill_category_temp = ""

            customer_bill1 = MerchantBill.objects.create(user_id = petrol_pump[0].user_id, mobile_no = petrol_pump[0].mobile_no,
                bill = petrol_pump[0].bill_file, business_name = business_name1, bill_received_business_name = merchant_business_id.id,
                invoice_no = petrol_pump[0].invoice_no, 
                bill_amount = petrol_pump[0].total_amount, customer_bill_category = bill_category_temp
            )

            letters = string.ascii_letters
            digit = string.digits
            random_string = str(petrol_pump[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

            customer_bill_new = MerchantBill.objects.filter(id=customer_bill1.id).update(bill_url = random_string)

            SavePetrolPumpBill.objects.filter(id=petrol_pump[0].id).update(delete_bill = True)
            return JsonResponse({'status': 'success', 'message': 'Bill Transfer successfully !!!' }, status=200)

        else:
            return JsonResponse({'status': 'error', 'message': "Failed to Transfer!!!"}, status=400)

class SaveFavouriteBill(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        send_bill_id = request.POST['send_bill_id']
        favourite_bill = request.POST['favourite_bill']
        db_table = request.POST['db_table']

        if favourite_bill == "0":
            is_check = False
        else:
            is_check = True
        if db_table == "CustomerBill":
            customer_bill_count = CustomerBill.objects.filter(id =send_bill_id).update(is_favourite=is_check)
            return JsonResponse({'status': 'success', 'message': 'Bill saved successfully !!!' }, status=200)

        elif db_table == "SaveParkingLotBill":
            parking_bill_count = SaveParkingLotBill.objects.filter(id=send_bill_id).update(is_favourite = is_check)
            return JsonResponse({'status': 'success', 'message': 'Bill saved successfully !!!' }, status=200)

        elif db_table == "SavePetrolPumpBill":
            petrol_pump_count = SavePetrolPumpBill.objects.filter(id=send_bill_id).update(is_favourite = is_check)
            return JsonResponse({'status': 'success', 'message': 'Bill saved successfully !!!' }, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to save!!!"}, status=400)


class ShareBillTOCustomer(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        mobile_no = request.POST['mobile_no']
        bill_id = request.POST['bill_id']
        db_table = request.POST['db_table']

        if mobile_no != user_id:

            is_exist = GreenBillUser.objects.filter(mobile_no = mobile_no)

            if is_exist:

                result = Sharebillmodel.objects.create(user_id = user_id, mobile_no = mobile_no, bill_id = bill_id, db_table = db_table)

                if result:
                    return JsonResponse({'status': "success", 'message': "Bill Shared successfully !"}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': "Failed to shared bill !!!"}, status=400)
            else:
                return JsonResponse({'status': 'error', 'message': "Customer is not found !!!"}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': "Unable to share on own Number !!!"}, status=400)



class GetSharedCustomersBill(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        mobile_no = request.POST['mobile_no']

        share_model = Sharebillmodel.objects.filter(mobile_no = mobile_no).order_by('-id')

        data = []

        for mobile_no in share_model:

            if mobile_no.db_table == "CustomerBill":

                customer_bill_list = CustomerBill.objects.filter(id = mobile_no.bill_id)

                for bill in customer_bill_list:

                    try:
                        business_name = bill.business_name.m_business_name
                    except:
                        business_name = ""

                    try:
                        bill_category_temp = bill.customer_bill_category.bill_category_name
                    except:
                        bill_category_temp = ""

                    base_url = "http://157.230.228.250/"

                    if bill.customer_added == True:
                        new_bill_url = str(base_url) + 'self-added-bill/' + str(bill.bill_url) + "/"
                    else:
                        new_bill_url = str(base_url) + 'my-bill/' + str(bill.bill_url) + "/"

                    try:
                        business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
                    except:
                        business_logo = ""

                    date_temp = datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y')



                    data.append({
                                "id": bill.id,
                                "sended_by": mobile_no.user_id,
                                "business_name": business_name,
                                "bill_category_name": bill_category_temp,
                                "bill_amount": bill.bill_amount,
                                "comments": bill.remarks,
                                "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                "bill_date_temp": datetime.strptime(date_temp, '%d-%m-%Y'),
                                "business_logo": business_logo,
                                "customer_added": bill.customer_added,
                                "invoice_no": bill.invoice_no,
                                'db_table': "CustomerBill",
                                'seen_status' : bill.seen_status,
                                'bill_file_url': new_bill_url,
                                "bill_flag": False,
                                "reason": "",
                                "is_favourite": bill.is_favourite,
                            })

            elif mobile_no.db_table == "SaveParkingLotBill":

                parking_bill_list = SaveParkingLotBill.objects.filter(id = mobile_no.bill_id)

                for bill in parking_bill_list:

                    try:
                        business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
                    except:
                        business_name = ""

                    try:
                        bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
                    except:
                        bill_category_temp = ""

                    base_url = "http://157.230.228.250/"

                    try:
                        business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                        business_logo = str(base_url) + str(business_logo_temp.url)

                    except:
                        business_logo = ""


                    data.append({
                                "id": bill.id,
                                "sended_by": mobile_no.user_id,
                                "business_name": business_name,
                                "bill_category_name": bill_category_temp,
                                "bill_amount": bill.amount,
                                "comments": bill.remarks,
                                "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                                "bill_date_temp": datetime.strptime(str(bill.date), '%d-%m-%Y'),
                                "business_logo": business_logo,
                                "customer_added": False,
                                "invoice_no": bill.invoice_no,
                                'db_table': "SaveParkingLotBill",
                                'seen_status': bill.seen_status,
                                'bill_file_url': str(base_url) + 'parking-lot-bill/' + str(bill.bill_url) + "/",
                                "bill_flag": bill.bill_flag,
                                "reason": bill.reason,
                                "is_favourite": bill.is_favourite,
                            })

            elif mobile_no.db_table == "SavePetrolPumpBill":

                petrol_bill_list = SavePetrolPumpBill.objects.filter(id = mobile_no.bill_id)

                for bill in petrol_bill_list:

                    try:
                        business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
                    except:
                        business_name = ""

                    try:
                        bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
                    except:
                        bill_category_temp = ""

                    base_url = "http://157.230.228.250/"

                    try:
                        business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                        business_logo = str(base_url) + str(business_logo_temp.url)

                    except:
                        business_logo = ""


                    data.append({
                                "id": bill.id,
                                "sended_by": mobile_no.user_id,
                                "business_name": business_name,
                                "bill_category_name": bill_category_temp,
                                "bill_amount": bill.total_amount,
                                "comments": bill.remarks,
                                "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                                "bill_date_temp": datetime.strptime(str(bill.date), '%d-%m-%Y'),
                                "business_logo": business_logo,
                                "customer_added": False,
                                "invoice_no": bill.invoice_no,
                                'db_table': "SavePetrolPumpBill",
                                'seen_status' : bill.seen_status,
                                'bill_file_url': str(base_url) + 'petrol-pump-bill/' + str(bill.bill_url) + "/",
                                "bill_flag": bill.bill_flag,
                                "reason": bill.reason,
                                "is_favourite": bill.is_favourite,
                            })
        if data:
            return JsonResponse({'status': 'success', 'data': data }, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)





class getBillByBillCategory(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        bill_category_id = request.POST['bill_category_id']

        user_id = request.POST['user_id']

        from_date = request.POST["from_date"]

        to_date = request.POST["to_date"]

        customer_object = GreenBillUser.objects.get(id=user_id)
        
        customer_bill_list = CustomerBill.objects.filter(customer_bill_category = bill_category_id, mobile_no=customer_object.mobile_no, delete_bill = False).order_by('-id')

        data = []

        for bill in customer_bill_list:

            try:
                business_name = bill.business_name.m_business_name
            except:
                business_name = ""

            try:
                bill_category_temp = bill.customer_bill_category.bill_category_name
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
            except:
                business_logo = ""

            date_temp = datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y')

            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": bill.bill_amount,
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        "bill_date_temp": datetime.strptime(date_temp, '%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": bill.customer_added,
                        "invoice_no": bill.invoice_no,
                        'db_table': "CustomerBill",
                        'seen_status' : bill.seen_status,
                        "bill_flag": False,
                        "reason": "",
                        "is_favourite": bill.is_favourite,
                    })

        parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no, bill_category_id = bill_category_id, is_pass = False, delete_bill = False).order_by('-id')

        for bill in parking_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""


            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": bill.amount,
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                        "bill_date_temp": datetime.strptime(str(bill.date), '%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": False,
                        "invoice_no": bill.invoice_no,
                        'db_table': "SaveParkingLotBill",
                        'seen_status' : bill.seen_status,
                        "bill_flag": bill.bill_flag,
                        "reason": bill.reason,
                        "is_favourite": bill.is_favourite,
                    })


        petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no, bill_category_id = bill_category_id, delete_bill = False).order_by('-id')

        for bill in petrol_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""


            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": bill.total_amount,
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                        "bill_date_temp": datetime.strptime(str(bill.date), '%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": False,
                        "invoice_no": bill.invoice_no,
                        'db_table': "SavePetrolPumpBill",
                        'seen_status' : bill.seen_status,
                        "bill_flag": bill.bill_flag,
                        "reason": bill.reason,
                        "is_favourite": bill.is_favourite,
                    })

        sorted_data = []

        if from_date and to_date and data:
            from_date = datetime.strptime(from_date, '%d-%m-%Y')
            to_date = datetime.strptime(to_date, '%d-%m-%Y')
            for bills in data:
                if bills['bill_date_temp'] >= from_date and bills['bill_date_temp'] <= to_date:
                    print('hii')
                    sorted_data.append(bills)
        else:
            sorted_data = data

        if sorted_data:
            # serializer = customerBillListSerializer(customer_bill_list, many=True)
            return JsonResponse({'status': 'success', 'data': sorted_data }, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)


# QR CODE GENERATION 
class generateQRCustomer(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        mobile_no = request.POST['mobile_no']
        vehicle_no = request.POST['vehicle_no']
        vehicle_type = request.POST['vehicle_type']
        description = request.POST['description']
        
        result = customerQR.objects.create(user_id= user_id, mobile_no= mobile_no, vehicle_no= vehicle_no, vehicle_type= vehicle_type, description= description)

        if result:
            return JsonResponse({'status': "success", 'message': "Data added successfully !"}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to store data !!!"}, status=400)

class listQRCustomer(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']

        result = customerQR.objects.filter(user_id= user_id)
        
        if result:
            serializer = customerQRSerializer(result, many=True)
            return JsonResponse({'status': "success", 'data': serializer.data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "No Data Found !!!"}, status=400)

class editQRCustomer(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        id = request.POST['id']

        mobile_no = request.POST['mobile_no']
        vehicle_no = request.POST['vehicle_no']
        vehicle_type = request.POST['vehicle_type']
        description = request.POST['description']


        result = customerQR.objects.filter(id= id).update(mobile_no= mobile_no, vehicle_no= vehicle_no, vehicle_type= vehicle_type, description= description)

        if result:
            return JsonResponse({'status': "success", 'message': "Data updated successfully !"}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to update data !!!"}, status=400)

# QR CODE GENERATION END

class parkingPassList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        mobile_no = request.POST['mobile_no']

        result = ParkingLotPass.objects.filter(mobile_no = mobile_no).order_by('-id')

        data = []

        today = date.today()
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

            if parkingPass.valid_to >= today:
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


class getBillByBillId(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        bill_id = request.POST['bill_id']

        db_table = request.POST['db_table']

        if db_table == "CustomerBill":
            result = CustomerBill.objects.filter(id=bill_id)

        elif db_table == "SaveParkingLotBill":
            result = SaveParkingLotBill.objects.filter(id=bill_id)

        elif db_table == "SavePetrolPumpBill":
            result = SavePetrolPumpBill.objects.filter(id=bill_id)

        base_url = "http://157.230.228.250/"

        bill_tags_name1 = []

        try:

            if result[0].bill_tags:
                bill_tags_list = list(result[0].bill_tags.split(","))
                for bill_tags1 in bill_tags_list:
                    bill_tags_name_temp = bill_tags.objects.filter(id = int(bill_tags1)).values('bill_tags_name')[0]['bill_tags_name']
                    bill_tags_name1.append(bill_tags_name_temp)

            bill_tags_name2 = ', '.join(map(str, bill_tags_name1))

            bill_tags_id = result[0].bill_tags

        except:
            bill_tags_name2 = ""

        try:
            if db_table == "CustomerBill":
                business = MerchantProfile.objects.filter(id = result[0].business_name.id)
            else:
                business = MerchantProfile.objects.filter(id = result[0].m_business_id)

            business_id = business[0].id
            business_name = business[0].m_business_name
        except:
            business_id = ""
            business_name = ""

        try:
            if db_table == "CustomerBill":
                bill_category_temp = bill_category.objects.filter(id = result[0].customer_bill_category.id)
            else:
                bill_category_temp = bill_category.objects.filter(id = result[0].bill_category_id)

            customer_bill_category_id = bill_category_temp[0].id
            bill_category_name = bill_category_temp[0].bill_category_name

        except:
            customer_bill_category_id = ""
            bill_category_name = ""

        try:
            merchant_partner = business[0].merchant_by_partner
            print("(((((((((") 
            print(merchant_partner)
        except:
            merchant_partner = ""
        if db_table == "CustomerBill":
            amount = result[0].bill_amount

            # bill_file_temp = str(base_url) + str(result[0].bill.url)

            try:
                bill_file_temp = str(base_url) + str(result[0].bill.url)
            except:
                bill_file_temp = ""

            bill_date = datetime.strptime(str(result[0].bill_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            customer_added_temp = result[0].customer_added
            custom_business_name_temp = result[0].custom_business_name

        elif db_table == "SaveParkingLotBill":
            amount = result[0].amount

            try:
                bill_file_temp = str(base_url) + str(result[0].bill_file.url)
            except:
                bill_file_temp = ""

            bill_date = datetime.strptime(str(result[0].date), '%d-%m-%Y').strftime('%d-%m-%Y')
            customer_added_temp = False
            custom_business_name_temp = ""

        elif db_table == "SavePetrolPumpBill":
            amount = result[0].total_amount

            try:
                bill_file_temp = str(base_url) + str(result[0].bill_file.url)
            except:
                bill_file_temp = ""

            bill_date = datetime.strptime(str(result[0].date), '%d-%m-%Y').strftime('%d-%m-%Y')
            customer_added_temp = False
            custom_business_name_temp = ""

        # try:
        #     business_id = result[0].business_name.id
        #     business_name =  result[0].business_name.m_business_name

        # except:
        #     business_id = ""
        #     business_name = ""

        # try:
        #     customer_bill_category_id = result[0].customer_bill_category.id
        #     bill_category_name =  result[0].customer_bill_category.bill_category_name

        # except:
        #     customer_bill_category_id = ""
        #     bill_category_name = ""

        bill_url = ""
        invoice_no = ""
        print(business[0])
        if db_table == "CustomerBill":
            bill = CustomerBill.objects.get(id = bill_id)
            if bill.customer_added == False:
                if merchant_partner:
                    bill_url = "http://157.230.228.250/my-green-bill/" + str(bill.bill_url) + "/"
                    invoice_no = ""
                else:
                    bill_url = "http://157.230.228.250/my-bill/" + str(bill.bill_url) + "/"
                    invoice_no = ""

            elif bill.customer_added == True:
                bill_url = "http://157.230.228.250/self-added-bill/" + str(bill.bill_url) + "/"
                invoice_no = result[0].invoice_no

        elif db_table == "SaveParkingLotBill":
            bill = SaveParkingLotBill.objects.get(id = bill_id)
            bill_url = "http://157.230.228.250/parking-lot-bill/" + str(bill.bill_url) + "/"
            invoice_no = result[0].invoice_no

        elif db_table == "SavePetrolPumpBill":
            bill = SavePetrolPumpBill.objects.get(id = bill_id)
            bill_url = "http://157.230.228.250/petrol-pump-bill/" + str(bill.bill_url) + "/"
            invoice_no = result[0].invoice_no
        
        context = {
            "bill_id":result[0].id,
            "bill": bill_file_temp,
            "bill_amount": str(amount),
            "invoice_no": invoice_no,
            "bill_date": bill_date,
            "customer_added": customer_added_temp,
            "bill_tags_id": bill_tags_id if bill_tags_id else "",
            "bill_tags_name": bill_tags_name2,
            "remarks": result[0].remarks,
            "custom_business_name": custom_business_name_temp,
            "business_name": business_name,
            "business_id": str(business_id),
            "customer_bill_category_id" : customer_bill_category_id,
            "customer_bill_category_name": bill_category_name,
            "bill_url" : bill_url,
        }

        if result:
            # serializer = customerBillListSerializer(result, many=True)
            return JsonResponse({'status': "success","data":context}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)

class getBillCategoriesListByCustomerId(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST["user_id"]

        user_object = GreenBillUser.objects.get(id = user_id)
        bill_categories = bill_category.objects.all()

        allocated_bill_categories = []

        bill_categories_temp = []

        for category in bill_categories:
            customer_bill_count = CustomerBill.objects.filter(mobile_no = user_object.mobile_no, customer_bill_category = category, delete_bill = False).count()
            parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = user_object.mobile_no, is_pass = False, delete_bill = False).count()
            petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = user_object.mobile_no, delete_bill = False).count()
            bill_count = 0
            bill_count = customer_bill_count + parking_bill_count + petrol_bill_count

            if customer_bill_count > 0:
                if category in bill_categories_temp:
                    continue
                else:
                    bill_categories_temp.append(category)

            if parking_bill_count > 0:
                if category.id == 27:
                    if category in bill_categories_temp:
                        continue
                    else:
                        bill_categories_temp.append(category)


            if petrol_bill_count > 0:
                if category.id == 26:
                    if category in bill_categories_temp:
                        continue
                    else:
                        bill_categories_temp.append(category)

        for category in bill_categories_temp:
            customer_bill_count = CustomerBill.objects.filter(mobile_no = user_object.mobile_no, customer_bill_category = category, delete_bill = False).count()

            if category.id == 27:
                parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = user_object.mobile_no,bill_category_id=category.id, is_pass = False, delete_bill = False).count()
            else:
                parking_bill_count = 0

            if category.id == 26:
                petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = user_object.mobile_no,bill_category_id = category.id, delete_bill = False).count()
            else:
                petrol_bill_count = 0

            bill_count = 0
            bill_count = customer_bill_count + parking_bill_count + petrol_bill_count

            if bill_count > 0:
                if category in allocated_bill_categories:
                    continue
                else:
                    try:
                        icon = category.icon.url
                        icon_url = "http://157.230.228.250/" + str(icon)
                    except:
                        icon_url = ""

                    allocated_bill_categories.append({
                        "id": category.id,
                        "bill_category_name": category.bill_category_name,
                        "bill_category_description": category.bill_category_description,
                        "bill_count": bill_count,
                        "icon_url": icon_url,
                    })

        if allocated_bill_categories:
            sorted_categories = sorted(allocated_bill_categories, key=lambda item: item.get("bill_category_name"))
        else:
            sorted_categories = ""
        
        if bill_categories:
            # serializer = billCategorySerializer(sorted_categories, many=True)
            return JsonResponse({'status': "success", 'data': sorted_categories}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)

class getMerchantBusinessByCustomerID(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST["user_id"]
        
        business_new_list = MerchantProfile.objects.filter(m_user=user_id)

        new_allocated_business = []

        base_url = "http://157.230.228.250/"

        b_logo = ""

        if business_new_list:
            for b in business_new_list:
                if b.m_business_logo:
                    b_logo = str(base_url) + str(b.m_business_logo.url)
                else:
                    b_logo = ""
                new_allocated_business.append({
                        "id": b.id,
                        "m_business_name": b.m_business_name,
                        "m_business_logo": b_logo,
                    })
        else:
            new_allocated_business = []

        if new_allocated_business:
            return JsonResponse(new_allocated_business, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)

class getMerchantBusinessListByCustomerId(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST["user_id"]

        user_object = GreenBillUser.objects.get(id = user_id)
        
        business_list = MerchantProfile.objects.all()

        allocated_business_list = []

        base_url = "http://157.230.228.250/"

        business_list_temp = []

        for business in business_list:
            
            customer_bill_count = CustomerBill.objects.filter(mobile_no = user_object.mobile_no, business_name = business, delete_bill = False).count()
            if customer_bill_count > 0:
                if business in business_list_temp:
                    continue
                else:
                    business_list_temp.append(business)

            parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = user_object.mobile_no, m_business_id = business.id, is_pass = False, delete_bill = False).count()
            if parking_bill_count > 0:
                if business in business_list_temp:
                    continue
                else:
                    business_list_temp.append(business)

            petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = user_object.mobile_no, m_business_id = business.id, delete_bill = False).count()
            if petrol_bill_count > 0:
                if business in business_list_temp:
                    continue
                else:
                    business_list_temp.append(business)

            customer_bill_count1 = CustomerBill.objects.filter(mobile_no = user_object.mobile_no, business_name__isnull=True, delete_bill = False).count()
            if customer_bill_count1 > 0:
                buisness_name = 'Others'
                if buisness_name in business_list_temp:
                    continue
                else:
                    business_list_temp.append(buisness_name)
        print(len(business_list_temp))

        for business in business_list_temp:
            if type(business) == str:
                customer_bill_count = CustomerBill.objects.filter(mobile_no = user_object.mobile_no, business_name__isnull=True, delete_bill = False).count()
                bill_count = 0
                bill_count = customer_bill_count
                customer_bill_list = CustomerBill.objects.filter(mobile_no = user_object.mobile_no, business_name__isnull=True, delete_bill = False).order_by('-id')

                buisness_name = 'Others'

                allocated_business_list.append({
                    "id": "",
                    "m_business_name": buisness_name,
                    "m_business_logo": "",
                    "bill_count": bill_count
                })


            if type(business) != str and business != None:
                customer_bill_count = CustomerBill.objects.filter(mobile_no = user_object.mobile_no, business_name = business, delete_bill = False).count()
                parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = user_object.mobile_no, m_business_id = business.id, is_pass = False, delete_bill = False).count()
                petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = user_object.mobile_no, m_business_id = business.id, delete_bill = False).count()

                bill_count = 0
                bill_count = customer_bill_count + parking_bill_count + petrol_bill_count
                
                if bill_count > 0:
                    if business in allocated_business_list:
                        continue
                    else:
                        if business.m_business_logo:
                            m_business_logo = str(base_url) + str(business.m_business_logo.url)
                        else:
                            m_business_logo = ""

                        allocated_business_list.append({
                            "id": str(business.id),
                            "m_business_name": business.m_business_name,
                            "m_business_logo": m_business_logo,
                            "bill_count": bill_count
                        })
        # print('allocated_business_list',allocated_business_list)

        if allocated_business_list:
            sorted_business_list = sorted(allocated_business_list, key=lambda item: item.get("m_business_name"))
        else:
            sorted_business_list = ""

        if business_list:
            # serializer = merchantBusinessSerializer(sorted_business_list, many=True)
            return JsonResponse(sorted_business_list, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)


class getTagsListByCustomerId(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST["user_id"]

        user_object = GreenBillUser.objects.get(id = user_id)
        
        bill_tags_list = bill_tags.objects.all()

        allocated_tag_list = []

        base_url = "http://157.230.228.250/"

        bill_tags_temp = []

        for tag in bill_tags_list:
            startswith = str(tag.id) + ','
            endswith = ','+ str(tag.id)
            contains = ','+ str(tag.id) + ','
            exact = str(tag.id)

            customer_bill_count = CustomerBill.objects.filter(Q(mobile_no = user_object.mobile_no), Q(delete_bill = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()
            parking_bill_count = SaveParkingLotBill.objects.filter(Q(mobile_no = user_object.mobile_no), Q(delete_bill = False), Q(is_pass = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()
            petrol_bill_count = SavePetrolPumpBill.objects.filter(Q(mobile_no = user_object.mobile_no), Q(delete_bill = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()

            bill_count = 0
            bill_count = customer_bill_count + parking_bill_count + petrol_bill_count

            if bill_count > 0:
                if tag in bill_tags_temp:
                    continue
                else:
                    bill_tags_temp.append(tag)

        for tag in bill_tags_temp:
            startswith = str(tag.id) + ','
            endswith = ','+ str(tag.id)
            contains = ','+ str(tag.id) + ','
            exact = str(tag.id)

            customer_bill_count = CustomerBill.objects.filter(Q(mobile_no = user_object.mobile_no), Q(delete_bill = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()
            parking_bill_count = SaveParkingLotBill.objects.filter(Q(mobile_no = user_object.mobile_no), Q(delete_bill = False), Q(is_pass = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()
            petrol_bill_count = SavePetrolPumpBill.objects.filter(Q(mobile_no = user_object.mobile_no), Q(delete_bill = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()

            bill_count = 0
            bill_count = customer_bill_count + parking_bill_count + petrol_bill_count

            if bill_count > 0:
                if tag in allocated_tag_list:
                    continue
                else:
                    allocated_tag_list.append({
                        "id": tag.id,
                        "tag_name": tag.bill_tags_name,
                        "bill_count": bill_count
                    })

        if allocated_tag_list:
            sorted_tag_list = sorted(allocated_tag_list, key=lambda item: item.get("tag_name"))
        else:
            sorted_tag_list = ""

        if bill_tags_list:
            return JsonResponse(sorted_tag_list, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)


class getBillByBillTags(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        bill_tag_id = request.POST['bill_tag_id']

        user_id = request.POST['user_id']

        from_date = request.POST["from_date"]

        to_date = request.POST["to_date"]

        customer_object = GreenBillUser.objects.get(id=user_id)

        startswith = str(bill_tag_id) + ','
        endswith = ','+ str(bill_tag_id)
        contains = ','+ str(bill_tag_id) + ','
        exact = str(bill_tag_id)
        
        customer_bill_list = CustomerBill.objects.filter(Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact), Q(mobile_no=customer_object.mobile_no), Q(delete_bill = False)).order_by('-id')

        data = []

        for bill in customer_bill_list:

            try:
                business_name = bill.business_name.m_business_name
            except:
                business_name = ""

            try:
                bill_category_temp = bill.customer_bill_category.bill_category_name
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
            except:
                business_logo = ""

            date_temp = datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y')

            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": bill.bill_amount,
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        "bill_date_temp": datetime.strptime(date_temp, '%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": bill.customer_added,
                        "invoice_no": bill.invoice_no,
                        'db_table': "CustomerBill",
                        'seen_status' : bill.seen_status,
                        "bill_flag": False,
                        "reason": "",
                        "is_favourite": bill.is_favourite,
                    })

        parking_bill_list = SaveParkingLotBill.objects.filter(Q(mobile_no = customer_object.mobile_no), Q(delete_bill = False), Q(is_pass = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).order_by('-id')

        for bill in parking_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""


            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": bill.amount,
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                        "bill_date_temp": datetime.strptime(str(bill.date), '%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": False,
                        "invoice_no": bill.invoice_no,
                        'db_table': "SaveParkingLotBill",
                        'seen_status' : bill.seen_status,
                        "bill_flag": bill.bill_flag,
                        "reason": bill.reason,
                        "is_favourite": bill.is_favourite,
                    })


        petrol_bill_list = SavePetrolPumpBill.objects.filter(Q(mobile_no = customer_object.mobile_no), Q(delete_bill = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).order_by('-id')

        for bill in petrol_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""


            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": bill.total_amount,
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                        "bill_date_temp": datetime.strptime(str(bill.date), '%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": False,
                        "invoice_no": bill.invoice_no,
                        'db_table': "SavePetrolPumpBill",
                        'seen_status' : bill.seen_status,
                        "bill_flag": bill.bill_flag,
                        "reason": bill.reason,
                        "is_favourite": bill.is_favourite,
                    })

        sorted_data = []

        if from_date and to_date and data:
            from_date = datetime.strptime(from_date, '%d-%m-%Y')
            to_date = datetime.strptime(to_date, '%d-%m-%Y')
            for bills in data:
                if bills['bill_date_temp'] >= from_date and bills['bill_date_temp'] <= to_date:
                    sorted_data.append(bills)
        else:
            sorted_data = data

        if sorted_data:
            # serializer = customerBillListSerializer(customer_bill_list, many=True)
            return JsonResponse({'status': 'success', 'data': sorted_data }, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)


class BillViewAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        bill_id = request.POST['bill_id']
        db_table = request.POST['db_table']
        bill_url = ""

        if db_table == "CustomerBill":
            bill = CustomerBill.objects.get(id = bill_id)
            if bill.customer_added == False:
                bill_url = "http://157.230.228.250/my-bill/" + str(bill.bill_url) + "/"

            elif bill.customer_added == True:
                bill_url = "http://157.230.228.250/self-added-bill/" + str(bill.bill_url) + "/"

        elif db_table == "SaveParkingLotBill":
            bill = SaveParkingLotBill.objects.get(id = bill_id)
            bill_url = "http://157.230.228.250/parking-lot-bill/" + str(bill.bill_url) + "/"

        elif db_table == "SavePetrolPumpBill":
            bill = SavePetrolPumpBill.objects.get(id = bill_id)
            bill_url = "http://157.230.228.250/petrol-pump-bill/" + str(bill.bill_url) + "/"

        if bill_url:
            return JsonResponse({'status': 'success', 'data': bill_url}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve bill !!!"}, status=400)


class GetCouponsAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        user_id = request.POST['user_id']
        customer_data_object = GreenBillUser.objects.get(id=user_id)
        customer_state = customer_data_object.c_state
        customer_city = customer_data_object.c_city
        customer_area = customer_data_object.c_area

        all_coupons_new = []
        today_date = date.today()
        all_coupons = CouponModel.objects.all().order_by('-id')
        
        for coupon1 in all_coupons:
            redeem_status = RedeemCouponModel.objects.filter(user_id = user_id, coupon_id = coupon1.id)
            try:
                merchant_object = MerchantProfile.objects.get(id = coupon1.merchant_business_id)
                coupon1.merchant_business_name = merchant_object.m_business_name
                coupon1.merchant_business_id = merchant_object.id
            except:
                coupon1.merchant_business_name = coupon1.owner_name
                coupon1.merchant_business_id = ""

            if redeem_status:
                coupon1.redeem_status = True
            else:
                coupon1.redeem_status = False

            base_url = "http://157.230.228.250/"

            if coupon1.coupon_logo:
                coupon_logo_url = base_url + str(coupon1.coupon_logo.url)
            else:
                coupon_logo_url = ""

            redeem_coupon = RedeemCouponModel.objects.filter(coupon_id=coupon1.id).count()

            if coupon1.valid_through >= today_date:
                if redeem_coupon < int(coupon1.coupon_valid_for_user):
                    if coupon1.customer_state:
                        if customer_state in coupon1.customer_state:
                            if coupon1.customer_city:
                                if customer_city in coupon1.customer_city:
                                    if coupon1.customer_area:
                                        if customer_area in coupon1.customer_area:
                                            all_coupons_new.append({
                                                'id': coupon1.id,
                                                'merchant_id': coupon1.merchant_id.id,
                                                'coupon_name': coupon1.coupon_name,
                                                'valid_from': datetime.strptime(str(coupon1.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                                'valid_through': datetime.strptime(str(coupon1.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                                'coupon_code': coupon1.coupon_code,
                                                'coupon_value': coupon1.coupon_value,
                                                'green_point': coupon1.green_point,
                                                'coupon_valid_for_user': coupon1.coupon_valid_for_user,
                                                'amount_in': coupon1.amount_in,
                                                'coupon_logo': coupon_logo_url,
                                                'coupon_redeem': coupon1.coupon_redeem,
                                                'coupon_caption': coupon1.coupon_caption,
                                                'merchant_business_id':  str(coupon1.merchant_business_id) if coupon1.merchant_business_id else "",
                                                'merchant_business_name': coupon1.merchant_business_name,
                                                'redeem_status': coupon1.redeem_status,
                                                'owner_name': coupon1.owner_name,
                                            })
                                    else:
                                        all_coupons_new.append({
                                            'id': coupon1.id,
                                            'merchant_id': coupon1.merchant_id.id,
                                            'coupon_name': coupon1.coupon_name,
                                            'valid_from': datetime.strptime(str(coupon1.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                            'valid_through': datetime.strptime(str(coupon1.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                            'coupon_code': coupon1.coupon_code,
                                            'coupon_value': coupon1.coupon_value,
                                            'green_point': coupon1.green_point,
                                            'coupon_valid_for_user': coupon1.coupon_valid_for_user,
                                            'amount_in': coupon1.amount_in,
                                            'coupon_logo': coupon_logo_url,
                                            'coupon_redeem': coupon1.coupon_redeem,
                                            'coupon_caption': coupon1.coupon_caption,
                                            'merchant_business_id':  str(coupon1.merchant_business_id) if coupon1.merchant_business_id else "",
                                            'merchant_business_name': coupon1.merchant_business_name,
                                            'redeem_status': coupon1.redeem_status,
                                            'owner_name': coupon1.owner_name,
                                        })
                            else:
                                all_coupons_new.append({
                                    'id': coupon1.id,
                                    'merchant_id': coupon1.merchant_id.id,
                                    'coupon_name': coupon1.coupon_name,
                                    'valid_from': datetime.strptime(str(coupon1.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                    'valid_through': datetime.strptime(str(coupon1.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y'),
                                    'coupon_code': coupon1.coupon_code,
                                    'coupon_value': coupon1.coupon_value,
                                    'green_point': coupon1.green_point,
                                    'coupon_valid_for_user': coupon1.coupon_valid_for_user,
                                    'amount_in': coupon1.amount_in,
                                    'coupon_logo': coupon_logo_url,
                                    'coupon_redeem': coupon1.coupon_redeem,
                                    'coupon_caption': coupon1.coupon_caption,
                                    'merchant_business_id':  str(coupon1.merchant_business_id) if coupon1.merchant_business_id else "",
                                    'merchant_business_name': coupon1.merchant_business_name,
                                    'redeem_status': coupon1.redeem_status,
                                    'owner_name': coupon1.owner_name,
                                })

        if all_coupons_new:
            return JsonResponse({'status': 'success', 'data': all_coupons_new}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)


class GetCouponsRedeemHistoryAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST['user_id']

        coupon_history = RedeemCouponModel.objects.filter(user_id=user_id).order_by('-id')

        coupon_history_new = []

        for coupon in coupon_history:

            try:
                merchant_object = MerchantProfile.objects.get(id = coupon.merchant_business_id)
                coupon.merchant_business_name = merchant_object.m_business_name
                merchant_business_logo = "http://157.230.228.250/" + str(merchant_object.m_business_logo.url)
                coupon.merchant_business_logo = merchant_business_logo
            except:
                coupon.merchant_business_name = ""
                coupon.merchant_business_logo = ""

            try:
                coupon_temp = CouponModel.objects.get(id = int(coupon.coupon_id))
                expiry_date =  datetime.strptime(str(coupon_temp.valid_through), '%Y-%m-%d').strftime('%d-%m-%Y')
            except:
                expiry_date = ""

            coupon_history_new.append({
                    'id': coupon.id,
                    'merchant_id': coupon.merchant_id.id,
                    'merchant_business_id': coupon.merchant_business_id,
                    'user_id': coupon.user_id,
                    'coupon_id': coupon.coupon_id,
                    'coupon_name': coupon.coupon_name,
                    'coupon_code': coupon.coupon_code,
                    'green_point': coupon.green_point,
                    'coupon_redeem_date': datetime.strptime(str((coupon.coupon_redeem_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'merchant_business_name': coupon.merchant_business_name,
                    'merchant_business_logo': coupon.merchant_business_logo,
                    'expiry_date': expiry_date
                })

        if coupon_history_new:
            return JsonResponse({'status': 'success', 'data': coupon_history_new}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)


class RedeemCouponAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        mobile_no =  request.POST['mobile_no']
        coupon_id = request.POST['coupon_id']
        green_point = int(request.POST['green_point'])
        coupon_code = request.POST['coupon_code']
        coupon_name = request.POST['coupon_name']
        merchant_id = request.POST['merchant_id']
        merchant_business_id = request.POST['merchant_business_id']

        merchant_object = GreenBillUser.objects.get(id = merchant_id)
        coupon_user_count = CouponModel.objects.get(id = coupon_id)

        try:
            green_points_obj = GreenPointsModel.objects.get(mobile_no = mobile_no)
            total_green_points = int(green_points_obj.green_points_count)

        except:
            total_green_points = 0

        if total_green_points >= green_point:
            new_green_points = total_green_points - green_point
            GreenPointsModel.objects.filter(mobile_no = mobile_no).update(green_points_count = new_green_points)
            CouponModel.objects.filter(id=coupon_id).update(coupon_redeem="1")
            result = RedeemCouponModel.objects.create(merchant_id = merchant_object, merchant_business_id = merchant_business_id, user_id = user_id, coupon_id = coupon_id, coupon_name=coupon_name, coupon_code=coupon_code, green_point=green_point)

            return JsonResponse({'status': 'success', 'message': "Coupon Redeemed Successfully !!!"}, status=200)

        else:
            return JsonResponse({'status': 'error', 'message': "You don't have sufficient Green points to purchase !!!"}, status=400)



class CouponNumberOfViewsAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        coupon_id_clicks = request.POST.get("coupon_id_clicks")
        result = CouponModel.objects.get(id=coupon_id_clicks)
        result.cout = result.cout + 1
        result.save()

        if result:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GreenPointsEarnedHistoryAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        mobile_no =  request.POST['mobile_no']

        data = []

        customer_object = GreenBillUser.objects.get(mobile_no=mobile_no)
        
        customer_bill_list = CustomerBill.objects.filter(mobile_no=customer_object.mobile_no, green_points_earned__isnull=False).order_by('-id')

        for bill in customer_bill_list:

            try:
                business_name = bill.business_name.m_business_name
            except:
                business_name = ""

            try:
                bill_category_temp = bill.customer_bill_category.bill_category_name
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
            except:
                business_logo = ""


            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": str(bill.bill_amount),
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": str(bill.customer_added),
                        'db_table': "CustomerBill",
                        'green_points_earned': bill.green_points_earned,
                        'seen_status' : str(bill.seen_status),
                    })

        parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = mobile_no, green_points_earned__isnull=False, is_pass = False).order_by('-id')

        for bill in parking_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""


            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": str(bill.amount),
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": str(False),
                        'db_table': "SaveParkingLotBill",
                        'green_points_earned': bill.green_points_earned,
                        'seen_status' : str(bill.seen_status),
                    })


        petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = mobile_no, green_points_earned__isnull=False).order_by('-id')

        for bill in petrol_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""


            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": str(bill.total_amount),
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": str(False),
                        'db_table': "SavePetrolPumpBill",
                        'green_points_earned': bill.green_points_earned,
                        'seen_status' : str(bill.seen_status),
                    })


        
        referral_history = GreenPointsEarnedHistory.objects.filter(mobile_no = mobile_no).order_by('-id')

        for referral in referral_history:
            data.append({
                "id": referral.id,
                "business_name":"",
                "bill_category_name":"",
                "bill_amount":"",
                "comments":"",
                "bill_date": datetime.strptime(str((referral.created_at).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                "business_logo":"",
                "customer_added":"",
                "db_table":'GreenPointsEarnedHistory',
                "green_points_earned":referral.earned_green_points ,
                'seen_status' :"",
                
            })

        data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

        if data:
            return JsonResponse({'status': 'success', 'data': data}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)


def GetEarnedGreenPoints(mobile_no):

    data = []

    customer_object = GreenBillUser.objects.get(mobile_no=mobile_no)
    
    customer_bill_list = CustomerBill.objects.filter(mobile_no=customer_object.mobile_no, green_points_earned__isnull=False).order_by('-id')

    for bill in customer_bill_list:

        try:
            business_name = bill.business_name.m_business_name
        except:
            business_name = ""

        try:
            bill_category_temp = bill.customer_bill_category.bill_category_name
        except:
            bill_category_temp = ""

        base_url = "http://157.230.228.250/"

        try:
            business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
        except:
            business_logo = ""

        data.append({
                    "id": bill.id,
                    "business_name": business_name,
                    "bill_category_name": bill_category_temp,
                    "bill_amount": bill.bill_amount,
                    "comments": bill.remarks,
                    "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    "business_logo": business_logo,
                    "customer_added": bill.customer_added,
                    'db_table': "CustomerBill",
                    'green_points_earned': bill.green_points_earned,
                    'seen_status' : bill.seen_status,
                })

    parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = mobile_no, green_points_earned__isnull=False, is_pass = False).order_by('-id')

    for bill in parking_bill_list:

        try:
            business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
        except:
            business_name = ""

        try:
            bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
        except:
            bill_category_temp = ""

        base_url = "http://157.230.228.250/"

        try:
            business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
            business_logo = str(base_url) + str(business_logo_temp.url)

        except:
            business_logo = ""


        data.append({
                    "id": bill.id,
                    "business_name": business_name,
                    "bill_category_name": bill_category_temp,
                    "bill_amount": bill.amount,
                    "comments": bill.remarks,
                    "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                    "business_logo": business_logo,
                    "customer_added": False,
                    'db_table': "SaveParkingLotBill",
                    'green_points_earned': bill.green_points_earned,
                    'seen_status' : bill.seen_status,
                })


    petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = mobile_no, green_points_earned__isnull=False).order_by('-id')

    for bill in petrol_bill_list:

        try:
            business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
        except:
            business_name = ""

        try:
            bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
        except:
            bill_category_temp = ""

        base_url = "http://157.230.228.250/"

        try:
            business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
            business_logo = str(base_url) + str(business_logo_temp.url)

        except:
            business_logo = ""


        data.append({
                    "id": bill.id,
                    "business_name": business_name,
                    "bill_category_name": bill_category_temp,
                    "bill_amount": bill.total_amount,
                    "comments": bill.remarks,
                    "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                    "business_logo": business_logo,
                    "customer_added": False,
                    'db_table': "SavePetrolPumpBill",
                    'green_points_earned': bill.green_points_earned,
                    'seen_status' : bill.seen_status,
                })

    
    total_earned_ponits = 0

    referral_history = GreenPointsEarnedHistory.objects.filter(mobile_no = mobile_no)

    for referral in referral_history:
        data.append({
            "id": referral.id,
            "green_points_earned":referral.earned_green_points 
        })


    for bill in data:
        if bill['green_points_earned']:
            total_earned_ponits = total_earned_ponits + int(bill['green_points_earned'])

    return total_earned_ponits


def GetUsedGreenPoints(user_id):

    coupon_history = RedeemCouponModel.objects.filter(user_id=user_id).order_by('-id')

    total_green_points_used = 0

    for coupon in coupon_history:
        if coupon.green_point:
            total_green_points_used = total_green_points_used + int(coupon.green_point)


    return total_green_points_used


class ShareWordAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        mobile_no =  request.POST['mobile_no']

        words = request.POST['words']

        result = ShareWord.objects.create(mobile_no = mobile_no, words = words)

        if result:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class SuggestBrandAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        mobile_no =  request.POST['mobile_no']

        brand = request.POST['brand']

        location = request.POST['location']

        contact_no = request.POST['contact_no']

        result = SuggestBrand.objects.create(mobile_no = mobile_no, contact_no = contact_no, brand = brand, location = location, is_customer = True)

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

        result = Feedback.objects.create(mobile_no = mobile_no, bug = bug_status, suggestion = suggestion_status, comments = comments, is_customer = True)

        if result:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class GetSupportAndFaqsModulesAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        customer_modules = []
        customer_modules_new = []

        # videos = Video_Model.objects.filter(user_name = "customer")

        # for video in videos:
        #     if video.module_name in customer_modules:
        #         continue
        #     else:
        #         customer_modules.append(video.module_name)


        # blogs = Blogs_Model.objects.filter(user_name = "customer")

        # for blog in blogs:
        #     if blog.module_name in customer_modules:
        #         continue
        #     else:
        #         customer_modules.append(blog.module_name)


        faqs = FAQs_Model.objects.filter(user_name = "customer")

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

        # videos = Video_Model.objects.filter(user_name = "customer", module_name = module_id)
       
        faqs = FAQs_Model.objects.filter(user_name = "customer", module_name = module_id)
        
        # blogs = Blogs_Model.objects.filter(user_name = "customer", module_name = module_id)

        # videos_serializer = CustomerVideoSerializer(videos, many=True)
        faqs_serializer = CustomerFaqsSerializer(faqs, many=True)
        # blogs_serializer = CustomerBlogsSerializer(blogs, many=True)

        if module_id:
            return JsonResponse({'status': 'success', 'faqs' : faqs_serializer.data}, status=200)
            # return JsonResponse({'status': 'success', 'videos' : videos_serializer.data, 'faqs' : faqs_serializer.data, 'blogs' : blogs_serializer.data}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


class getCustomerReferralCode(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST['user_id']

        customer_object = GreenBillUser.objects.get(id = user_id)

        if not customer_object.customer_referral_code:

            letters = string.ascii_letters

            digit = string.digits

            random_string = str(user_id) + ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

            referral_code = random_string[0:6].upper()

            GreenBillUser.objects.filter(id = user_id).update(customer_referral_code = referral_code)

            customer_object = GreenBillUser.objects.get(id = user_id)

        if customer_object:
            return JsonResponse({'status':'success', 'message': customer_object.customer_referral_code}, status=200)
        else:
            return JsonResponse({'status' : 'error', 'message': "Referral Code Not Available"}, status=400)


class UpdateSeenStatusAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        bill_id = request.POST['bill_id']
        db_table = request.POST['db_table']
        result = ""
        
        if db_table == "CustomerBill":
            result = CustomerBill.objects.filter(id = bill_id).update(seen_status = True)

        elif db_table == "SaveParkingLotBill":
            result = SaveParkingLotBill.objects.filter(id = bill_id).update(seen_status = True)      

        elif db_table == "SavePetrolPumpBill":
            result = SavePetrolPumpBill.objects.filter(id = bill_id).update(seen_status = True)

        if result:
            return JsonResponse({'status': 'success', 'message': "Seen status updated Successfully"}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to update !!!"}, status=400)

class CustomerGetOffersAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        customer_data_object = GreenBillUser.objects.get(id=user_id)
        customer_state = customer_data_object.c_state
        customer_city = customer_data_object.c_city
        customer_area = customer_data_object.c_area
        offers = OfferModel.objects.filter(status = "1", Offer_type = "Customer").order_by('-id')

        offers_list = []
        today_date = date.today()
        for offer in offers:
            offer_image_url = "http://157.230.228.250" + str(offer.offer_image.url)

            business_logo = "http://157.230.228.250" + str(offer.offer_logo.url) if offer.offer_logo else ""

            try:
                merchant_business_id = offer.merchant_business_id.id
            except:
                merchant_business_id = ""

            
            if offer.offer_panel == "merchant" and offer.merchant_business_id:
                m_business_name = offer.merchant_business_id.m_business_name
            if offer.offer_panel == "owner":
                m_business_name = offer.o_business_name
            # else:
            #     m_business_name = ""

            try:
                merchant_user = offer.merchant_user.id
            except:
                merchant_user = ""


            if offer.valid_through >= today_date:
                if offer.customer_state:
                    if customer_state in offer.customer_state:
                        if offer.customer_city:
                            if customer_city in offer.customer_city:
                                if offer.customer_area:
                                    if customer_area in offer.customer_area:
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
                                            "offer_business_category": offer.offer_business_category if offer.offer_business_category else "",
                                            "created_date": offer.created_date,
                                            "offer_panel": offer.offer_panel,
                                            "merchant_user": str(offer.merchant_user.id) if offer.merchant_user else "0",
                                            "merchant_business_id": str(merchant_business_id) if merchant_business_id else "",
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
                                        "offer_business_category": offer.offer_business_category if offer.offer_business_category else "",
                                        "created_date": offer.created_date,
                                        "offer_panel": offer.offer_panel,
                                        "merchant_user": str(offer.merchant_user.id) if offer.merchant_user else "0",
                                        "merchant_business_id": str(merchant_business_id) if merchant_business_id else "",
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
                                "offer_business_category": offer.offer_business_category if offer.offer_business_category else "",
                                "created_date": offer.created_date,
                                "offer_panel": offer.offer_panel,
                                "merchant_user": str(offer.merchant_user.id) if offer.merchant_user else "0",
                                "merchant_business_id": str(merchant_business_id) if merchant_business_id else "",
                                "m_business_logo": business_logo,
                                "m_business_name":  m_business_name,
                            })

        # serializer = CustomerOffersListSerializer(offers, many=True)

        if offers:
            return JsonResponse({'status': 'success', 'data' : offers_list}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class CustomerGetOffersAPI_test(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        offers = OfferModel.objects.filter(status = "1", Offer_type = "Customer").order_by('-id')

        test = []

        for offer in offers:
            test.append({
                'id': offer.id,
            })

        if offers:
            return JsonResponse({'status': 'success', 'data' : test}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class CustomerPaymentHistoryAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        mobile_no = request.POST.get('mobile_no')

        payment_history = []
        customer_bill = CustomerBill.objects.filter(mobile_no = mobile_no, payment_done=True, customer_added=False)

        for bill in customer_bill:
            payment_history.append({
                'invoice_no' : bill.invoice_no,
                'amount' : float(bill.bill_amount),
                # 'created_at' : bill.created_at,
                'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'transaction_id' : bill.transaction_id,
                'mode': 'PayU' if bill.transaction_id else '',
                # 'business_name' : bill.business_name,
                })

        parking_bill = SaveParkingLotBill.objects.filter(mobile_no = mobile_no, payment_done=True)

        for bill in parking_bill:
            payment_history.append({
                'invoice_no' : bill.invoice_no,
                'amount' : float(bill.amount),
                # 'created_at' : bill.created_at,
                'bill_date': bill.date,
                'transaction_id' : bill.transaction_id,
                'mode': 'PayU' if bill.transaction_id else '',
                # 'business_name' : bill.business_name,
                })

        petrol_bill = SavePetrolPumpBill.objects.filter(mobile_no = mobile_no, payment_done=True)

        for bill in petrol_bill:
            payment_history.append({
                'invoice_no' : bill.invoice_no,
                'amount' : float(bill.amount),
                # 'created_at' : bill.created_at,
                'bill_date': bill.date,
                'transaction_id' : bill.transaction_id,
                'mode': 'PayU' if bill.transaction_id else '',
                # 'business_name' : bill.business_name,
                })

        total_amount_spent = 0
        for total in payment_history:
            total_amount_spent = total_amount_spent + float(total['amount'])
            
        total_bill_count = len(payment_history)

        payment_history.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)
        
        if payment_history and total_amount_spent and total_bill_count:
            return JsonResponse({'status': 'success', 'data': payment_history,'total_amount_spent':total_amount_spent,'total_bill_count':total_bill_count}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)



class GetMerchantBusinessByCategoryIdAPI(generics.GenericAPIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	def post(self, request):
		bill_category_id = request.POST["bill_category_id"]
		bill_category_object = bill_category.objects.get(id = bill_category_id)
		merchant_business = MerchantProfile.objects.filter(m_business_category__business_category_name__contains = bill_category_object.bill_category_name)
		data = []
		for business in merchant_business:
			data.append({
		        "id": business.id,
		        "business_name": business.m_business_name
		    })

		if data:
			return JsonResponse({'status': 'success', 'data': data}, status=200)
		else:
			return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)


class CustomerCashMemoListAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        mobile_no = request.POST['mobile_no']

        result = CustomerCashMemoDetailModels.objects.filter(mobile_number = mobile_no, rejected_cash_memo=False).order_by("-id")

        cashmemo_list = []

        for coupon in result:
            cashmemo_list.append({
                'id': coupon.id,
                'memo_no': coupon.memo_no,
                'name': coupon.merchant_business_id.m_business_name if coupon.merchant_business_id else '',
                'address': coupon.address,
                'mobile_number': coupon.mobile_number,
                'date': datetime.strptime(str(coupon.date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'total': float(coupon.total) if coupon.total else 0,
                'memo_url': "http://157.230.228.250/cash-memo/" + str(coupon.memo_url) + "/"
            })

        if result:
            return JsonResponse({'status' : "success", "data": cashmemo_list}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class CustomerReceiptListAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        mobile_no = request.POST['mobile_no']

        result = CustomerReceiptDetailsModels.objects.filter(mobile_number=mobile_no, rejected_receipt=False).order_by("-id")

        receipt_list = []

        for receipt in result:
            receipt_list.append({
                'id': receipt.id,
                'receipt_no': receipt.receipt_no,
                'name':receipt.merchant_business_id.m_business_name if receipt.merchant_business_id else '',
                'mobile_number': receipt.mobile_number,
                'date': datetime.strptime(str(receipt.date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'total': float(receipt.total) if receipt.total else float(0),
                'receipt_url': "http://157.230.228.250/receipt/" + str(receipt.receipt_url) + "/",
            })

        if result:
            return JsonResponse({'status' : "success", "data": receipt_list}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class RatingAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        mobile_no = request.POST['mobile_no']
        customer_object1 = GreenBillUser.objects.get(mobile_no = mobile_no)

        rating_list = []
        data_reply = CustomerBill.objects.filter(Q(mobile_no = customer_object1) & Q(customer_added=False) & (Q(rating=1) | Q(rating=2) | Q(rating=3) | Q(rating=4) | Q(rating=5))).order_by('-id')
        
        for rate in data_reply:
            if rate.business_name:
                try:
                    symbol = bill_designs.objects.get(merchant_business_id = rate.business_name.id).rating_emoji
                except:
                    symbol = '😊'
            else:
                symbol = ''
                # symbol = '😊'

            if rate.rating:
                rating_id = rate.rating
            else:
                rating_id = ""

            if rate.rating == "1":
                symbol = symbol
            if rate.rating == "2":
                symbol = symbol + symbol
            if rate.rating == "3":
                symbol = symbol + symbol + symbol
            if rate.rating == "4":
                symbol = symbol + symbol + symbol + symbol
            if rate.rating == "5":
                symbol = symbol + symbol + symbol + symbol + symbol

            # if rate.feedback_reply:
            if rate.rating != "0" or rate.rating is not None:
                rating_list.append({
                    'id': rate.id,
                    'mobile_no': rate.mobile_no,
                    'invoice_no': rate.invoice_no,
                    'date':datetime.strptime(str(rate.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'rating_id': rating_id,
                    'store_feedback':symbol,
                    'store_reply':rate.feedback_reply,
                })

        if rating_list:
            return JsonResponse({'status' : "success", "data": rating_list}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)

class ViewCustomerRatingAnalysisGraph(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        mobile_no = request.POST['mobile_no']

        customer_object = GreenBillUser.objects.get(mobile_no = mobile_no)

        data_reply = CustomerBill.objects.filter(mobile_no = customer_object,customer_added=False,feedback_submit=True).order_by('-id')

        feedback_count = CustomerBill.objects.filter(mobile_no = customer_object,customer_added=False,feedback_submit=True).count()

        data = []
        rating1 = 0
        rating2 = 0
        rating3 = 0
        rating4 = 0
        rating5 = 0

        for reply in data_reply:
            if reply.feedback_reply:
                if reply.rating == '1':
                    rating1 = rating1 + 1
                if reply.rating == '2':
                    rating2 = rating2 + 1
                if reply.rating == '3':
                    rating3 = rating3 + 1
                if reply.rating == '4':
                    rating4 = rating4 + 1
                if reply.rating == '5':
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

        if data:
            return JsonResponse({'status': "success", 'data': data, 'labels': labels, 'rating_percentage': rating_percentage}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)