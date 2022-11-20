import random
import os
import base64
import uuid
import django.utils.timezone as timezone
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
from users.models import GreenBillUser, UserProfileImage, Merchant_users
from .serializers import *
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from django.utils import formats
from authentication.models import otp_validation
from django.conf import settings
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from merchant_setting.models import *
from .models import *

from merchant_setting.models import parking_app_setting_model, petrol_pump_app_setting_model

# App Notification

from merchant_software_apis.models import DeviceId
import socket
from pyfcm import FCMNotification
import random
import string

from promotions.models import *
from bill_design.models import *

from green_points.models import GreenPointsModel

from datetime import date

# SMS
import requests
import time
import pyshorteners

import sweetify

from super_admin_settings.models import GreenPointsSettings

from my_subscription.views import getActiveSubscriptionPlan

from my_subscription.models import *

from django.db.models import Q
from merchant_role.models import merchant_userrole

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from merchant_setting.models import MerchantPaymentSetting
import random
import hashlib

@csrf_exempt
def petrolPumpMerchantLogin(request):
    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        password = request.POST['password']

        try:
            is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
            is_merchant_staff = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant_staff')[0]['is_merchant_staff']

            print(is_merchant_staff)

            if is_merchant:
                user = authenticate(mobile_no=mobile_no, password=password)

                if user:

                    is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
                    
                    is_business_petrol_pump = MerchantProfile.objects.filter(m_user_id=user.id, m_business_category_id=11)

                else:
                    is_merchant = ""
                    is_business_petrol_pump = ""

                if user and is_merchant and is_business_petrol_pump:

                    serializer = merchantSerializer(user)

                    base_url = "http://157.230.228.250"
                    
                    if is_business_petrol_pump[0].m_business_logo:
                        m_business_logo = str(base_url) + str(is_business_petrol_pump[0].m_business_logo.url)
                    else:
                        m_business_logo = None

                    merchant_user_id = Merchant_users.objects.filter(user_id = user.id).values('merchant_user_id')[0]['merchant_user_id']

                    try:
                        merchant_bussiness = MerchantProfile.objects.get(id = is_business_petrol_pump[0].id, m_user = merchant_user_id)
                        # print(merchant_bussiness)
                    except:
                        merchant_bussiness = ""

                    try:
                        setting = petrol_pump_app_setting_model.objects.filter(merchant_id = merchant_user_id, merchant_bussiness = merchant_bussiness)
                        footer_text1 = setting[0].footer_text1
                        footer_text2 = setting[0].footer_text2
                        footer_text3 = setting[0].footer_text3
                        header_text1 = setting[0].header_text1
                        header_text2 = setting[0].header_text2
                        header_text3 = setting[0].header_text3

                        digital_bill = setting[0].digital_bill
                        sms = setting[0].sms

                    except:
                        footer_text1 = ""
                        footer_text2 = ""
                        footer_text3 = ""
                        header_text1 = ""
                        header_text2 = ""
                        header_text3 = ""
                        digital_bill = True
                        sms = False

                    try:
                        addon_status_temp = AddonPetrolPump.objects.filter(m_business_id = m_business_id)

                        if addon_status_temp.count() >= 1:
                            addon_status = True
                        else:
                            addon_status = False
                    except:
                        addon_status = False

                    business_data = {
                        'm_user_id': merchant_user_id,
                        'm_business_id': is_business_petrol_pump[0].id,
                        'm_business_name': is_business_petrol_pump[0].m_business_name,
                        'm_business_logo': m_business_logo,
                        'm_address': is_business_petrol_pump[0].m_address, 
                        'm_area': is_business_petrol_pump[0].m_area, 
                        'm_city': is_business_petrol_pump[0].m_city,
                        'm_district' : is_business_petrol_pump[0].m_district,
                        'm_state' : is_business_petrol_pump[0].m_state,
                        'm_gstin': is_business_petrol_pump[0].m_gstin,
                        'digital_bill': digital_bill,
                        'sms': sms,
                        'footer_text1': footer_text1,
                        'footer_text2' : footer_text2,
                        'footer_text3' : footer_text3,
                        'header_text1': header_text1,
                        'header_text2': header_text2,
                        'header_text3': header_text3,
                        'addon_status': addon_status,
                        'm_vat_tin_number' : is_business_petrol_pump[0].m_vat_tin_number,
                    }


                    
                    try:
                        token = Token.objects.create(user=user)
                    except:
                        token = Token.objects.get(user_id=user.id)

                    # try: 
                    #     profile_image_temp = UserProfileImage.objects.filter(user=user.id)
                    # except: 
                    #     profile_image_temp = ""

                    # if profile_image_temp and profile_image_temp[0].m_profile_image:
                    #     profile_image = str(base_url) + str(profile_image_temp[0].m_profile_image.url)
                    # else:
                    #     profile_image = ""

                    login_status = PetrolLog.objects.filter(user_id = merchant_user_id, created_at__date = timezone.now())
                    
                    if login_status:
                        pass
                    else:
                        PetrolLog.objects.create(user_id = merchant_user_id, login_at = timezone.now())

                    if user is not None and is_merchant:
                        return JsonResponse({'status': 'success', 'token': token.key, 'data': serializer.data, 'business_details': business_data}, status=200)
                    else:
                        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)
                else:
                    return JsonResponse({'status': 'error', 'message': "Invalid credentials !!!"}, status=400)

            elif is_merchant_staff:
                assign_roles = merchant_userrole.objects.filter(Q(role__role_name ="Operator")|Q(role__role_name ="Admin"),user__mobile_no = mobile_no)
                if assign_roles:
                    user = authenticate(mobile_no=mobile_no, password=password)
                   
                    is_merchant_staff = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant_staff')[0]['is_merchant_staff']
                    
                    if user:
                        merchant_user_id = Merchant_users.objects.filter(user_id = user.id).values('merchant_user_id')[0]['merchant_user_id']
                        m_business_id = Merchant_users.objects.filter(user_id = user.id).values('m_business_id')[0]['m_business_id']
                        
                        is_business_petrol_pump = MerchantProfile.objects.filter(id= m_business_id, m_user_id=merchant_user_id, m_business_category_id=11)
                    
                    else:
                        is_business_petrol_pump = ""
                    
                    if user and is_merchant_staff and is_business_petrol_pump:
                        
                        serializer = merchantSerializer(user)
                        base_url = "http://157.230.228.250"
                        
                        if is_business_petrol_pump[0].m_business_logo:
                            m_business_logo = str(base_url) + str(is_business_petrol_pump[0].m_business_logo.url)
                        else:
                            m_business_logo = None

                        merchant_user_id = Merchant_users.objects.filter(user_id = user.id).values('merchant_user_id')[0]['merchant_user_id']

                        try:
                            merchant_bussiness = MerchantProfile.objects.get(id = m_business_id, m_user = merchant_user_id)
                            print(merchant_bussiness)
                        except:
                            merchant_bussiness = ""

                        try:
                            setting = petrol_pump_app_setting_model.objects.filter(merchant_id = merchant_user_id, merchant_bussiness = merchant_bussiness)
                            footer_text1 = setting[0].footer_text1
                            footer_text2 = setting[0].footer_text2
                            footer_text3 = setting[0].footer_text3
                            header_text1 = setting[0].header_text1
                            header_text2 = setting[0].header_text2
                            header_text3 = setting[0].header_text3
                            digital_bill = setting[0].digital_bill
                            sms = setting[0].sms

                        except:
                            footer_text1 = ""
                            footer_text2 = ""
                            footer_text3 = ""
                            header_text1 = ""
                            header_text2 = ""
                            header_text3 = ""
                            digital_bill = True
                            sms = False

                        try:
                            addon_status_temp = AddonPetrolPump.objects.filter(m_business_id = m_business_id)

                            if addon_status_temp.count() >= 1:
                                addon_status = True
                            else:
                                addon_status = False
                        except:
                            addon_status = False

                        business_data = {
                            'm_user_id': merchant_user_id,
                            'm_business_id': is_business_petrol_pump[0].id,
                            'm_business_name': is_business_petrol_pump[0].m_business_name,
                            'm_business_logo': m_business_logo,
                            'm_address': is_business_petrol_pump[0].m_address, 
                            'm_area': is_business_petrol_pump[0].m_area, 
                            'm_city': is_business_petrol_pump[0].m_city,
                            'm_district' : is_business_petrol_pump[0].m_district,
                            'm_state' : is_business_petrol_pump[0].m_state,
                            'm_gstin': is_business_petrol_pump[0].m_gstin,
                            'digital_bill': digital_bill,
                            'sms': sms,
                            'footer_text1': footer_text1,
                            'footer_text2' : footer_text2,
                            'footer_text3' : footer_text3,
                            'header_text1': header_text1,
                            'header_text2': header_text2,
                            'header_text3':header_text3,
                            'addon_status': addon_status,
                            'm_vat_tin_number' : is_business_petrol_pump[0].m_vat_tin_number,
                        }

                        try:
                            token = Token.objects.create(user=user)
                        except:
                            token = Token.objects.get(user_id=user.id)
                        
                        # try: 
                        #     profile_image_temp = UserProfileImage.objects.filter(user=user.id)
                        # except: 
                        #     profile_image_temp = ""

                        
                        # if profile_image_temp and profile_image_temp[0].m_profile_image:
                        #     profile_image = str(base_url) + str(profile_image_temp[0].m_profile_image.url)
                        # else:
                        #     profile_image = ""

                        login_status = PetrolLog.objects.filter(user_id = user.id, created_at__date = timezone.now())
                        
                        if login_status:
                            pass
                        else:
                            PetrolLog.objects.create(user_id = user.id, login_at = timezone.now())

                        if user is not None and is_merchant_staff:
                            return JsonResponse({'status': 'success', 'token': token.key, 'data': serializer.data, 'business_details': business_data}, status=200)
                        else:
                            return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)
                    else:
                        return JsonResponse({'status': 'error', 'message': "Invalid credentials !!!"}, status=400)
                else:
                    return JsonResponse({'status': 'error', 'message': "Invalid credentials !!!"}, status=400)

            else:
                return JsonResponse({'status': 'error', 'message': "User not register !!!"}, status=400)
        except:
            return JsonResponse({'status': 'error', 'message': "User not register !!!"}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


class getPetrolPumpBusinessList(generics.GenericAPIView):
    serializer_class = merchantSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']
        try:
            merchant_users_object = Merchant_users.objects.get(user_id = user_id)
           
            merchant_general_setting = MerchantProfile.objects.filter(m_user_id=user_id, m_business_category_id=11)
            
        except:
            merchant_general_setting = ""

        if merchant_general_setting: 
            serializers = merchantBusinessSerializer(merchant_general_setting, many=True)
            return JsonResponse({'status': "success", 'data': serializers.data}, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Data Not Found !!!"}, status=400)
            

class getPetrolPumpProductList(generics.GenericAPIView):
    serializer_class = merchantSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['m_user_id']
        m_business_id = request.POST['id']
        
        try:
           
            data= MerchantPetrolPump.objects.filter(user_id= user_id, m_business_id= m_business_id)
            print('data',data)
        except:
            data = ""

        if data: 
            serializers = merchantPetrolPumpProductsSerializer(data, many=True)
            return JsonResponse({'status': "success", 'data': serializers.data}, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Data Not Found !!!"}, status=400)


class generatePetrolPumpInvoiceNumber(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']
        m_user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']

        merchantDetails = MerchantProfile.objects.filter(id=m_business_id, m_user_id=m_user_id, m_business_category_id=11)

        year = timezone.now().year

        try:
            invoice = InvoiceNumberPetrolPump.objects.filter(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id).last()
        except:
            invoice = ""

        if not invoice:
            # invoice_no = str("GB") + str(merchantDetails[0].m_user_id) + str(year) + str("/") + str("01").zfill(5)
            invoice_no = str(year) + str("/") + str("01").zfill(5)

        else:
            last_invoice = invoice.invoice_no
            
            split_list = last_invoice.split("/")
            
            last_no = split_list[1]
            
            no = int(last_no) + 1
            
            # invoice_no = str("GB") + str(merchantDetails[0].m_user_id) + str(year) + str("/") + str(no).zfill(5)
            invoice_no = str(year) + str("/") + str(no).zfill(5)

        
        if invoice_no:
            return JsonResponse({'status': "success", 'message': invoice_no}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to generate invoice !!!"}, status=400)

class savePetrolPumpBill(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']
        m_user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']
        mobile_no = request.POST['mobile_no']
        vehicle_type = request.POST['vehicle_type']
        vehicle_number = request.POST['vehicle_number']
        product_id = request.POST['product_id']
        product_name = request.POST['product_name']
        product_cost = request.POST['product_cost']
        volume = request.POST['volume']
        amount = request.POST['amount']
        date = request.POST['date']
        time = request.POST['time']
        # invoice_no = request.POST['invoice_no']
        worker_name = request.POST['worker_name']
        addon_product_id = request.POST['addon_product_id']
        addon_product_name = request.POST['addon_product_name']
        addon_product_cost = request.POST['addon_product_cost']
        total_amount = request.POST['total_amount']
        c_unique_id_temp = request.POST['c_unique_id']

        business_id = m_business_id

        subscription_object = getActiveSubscriptionPlan(request, business_id)

        if subscription_object:

            try:
                merchant_bussiness = MerchantProfile.objects.get(id = business_id)
            except:
                merchant_bussiness = ""

            try:
                setting = petrol_pump_app_setting_model.objects.get(merchant_bussiness = merchant_bussiness)
                digital_bill = setting.digital_bill
                sms = setting.sms
            except:
                digital_bill = True
                sms = False

            if digital_bill == True and float(subscription_object.total_amount_avilable) < float(subscription_object.per_digital_bill_cost):
                return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
            elif sms == True and float(subscription_object.total_amount_avilable) < float(subscription_object.per_bill_cost):
                return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
            else:
                try:
                    is_checkoutpin_temp = request.POST['is_checkoutpin']
                    if is_checkoutpin_temp == "true":
                        is_checkoutpin = True
                    else:
                        is_checkoutpin = False
                except:
                    is_checkoutpin = False

                try:
                    addon_quantity = request.POST['addon_quantity']
                except:
                    addon_quantity = ""

                try:
                    nozzle_name = request.POST['nozzle_name']
                except:
                    nozzle_name = ""

                if mobile_no and c_unique_id_temp == "":
                    try:
                        c_unique_id = GreenBillUser.objects.filter(mobile_no=mobile_no).values('c_unique_id')[0]['c_unique_id']
                    except:
                        c_unique_id = ""

                elif c_unique_id_temp:
                    c_unique_id = c_unique_id_temp
                    try:
                        mobile_no = GreenBillUser.objects.filter(c_unique_id=c_unique_id).values('mobile_no')[0]['mobile_no']
                    except:
                        return JsonResponse({'status': "error", 'message': "Checkout pin is invalid."}, status=400)
                else:
                    c_unique_id = ""
                    mobile_no = ""

                # try:
                #     c_unique_id = GreenBillUser.objects.filter(mobile_no=mobile_no).values('c_unique_id')[0]['c_unique_id']
                # except:
                #     c_unique_id = ""

                merchantDetails = MerchantProfile.objects.filter(id=m_business_id, m_user_id=m_user_id, m_business_category_id=11)

                year = timezone.now().year

                try:
                    # invoice = InvoiceNumberPetrolPump.objects.filter(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id).last()

                    invoice = InvoiceNumberPetrolPump.objects.filter(m_business_id= m_business_id).last()
                except:
                    invoice = ""

                if not invoice:
                    # invoice_no = str("GB") + str(merchantDetails[0].m_user_id) + str(year) + str("/") + str("01").zfill(5)
                    invoice_no = str(year) + str("/") + str("01").zfill(5)

                else:
                    last_invoice = invoice.invoice_no
                    
                    split_list = last_invoice.split("/")
                    
                    last_no = split_list[1]
                    
                    no = int(last_no) + 1
                    
                    # invoice_no = str("GB") + str(merchantDetails[0].m_user_id) + str(year) + str("/") + str(no).zfill(5)
                    invoice_no = str(year) + str("/") + str(no).zfill(5)
                
                result = SavePetrolPumpBill.objects.create(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id, mobile_no= mobile_no, vehicle_type= vehicle_type, vehicle_number= vehicle_number, product_id= product_id, product_name= product_name, product_cost= product_cost, volume= volume, amount= amount, date= date, time= time,  invoice_no= invoice_no, worker_name = worker_name, addon_product_id = addon_product_id, addon_product_name = addon_product_name, addon_product_cost = addon_product_cost, total_amount = total_amount, c_unique_id = c_unique_id, addon_quantity = addon_quantity, nozzle_name = nozzle_name, is_checkoutpin = is_checkoutpin, green_points_earned = '1')

                if c_unique_id_temp:
                    SavePetrolPumpBill.objects.filter(id = result.id).update(is_checkoutpin = True)

                try:
                    green_points_old = GreenPointsModel.objects.filter(mobile_no=mobile_no).values('green_points_count')[0]['green_points_count']
                    
                except:
                    green_points_old = 0

                green_points_settings_object = GreenPointsSettings.objects.get(id = 1)
                green_points = green_points_settings_object.bill_points

                SavePetrolPumpBill.objects.filter(id = result.id).update(green_points_earned = str(green_points))

                green_points_new = int(green_points_old) + int(green_points)

                try:
                    GreenPointsModel.objects.update_or_create(mobile_no=mobile_no, defaults={
                        'green_points_count': green_points_new})
                except:
                    pass

                if result:
                    invoice_result = InvoiceNumberPetrolPump.objects.create(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id, invoice_no= invoice_no)
                    return JsonResponse({'status': "success", 'bill_id' : str(result.id), 'mobile_no': str(mobile_no), 'invoice_no' : str(invoice_no), 'message': 'Bill Added Successfully !!!'}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "Failed to add Bill !!!"}, status=400)
        else:
            return JsonResponse({'status':'error', 'message': "You don't have active Green Bill Subscription. Please purchase and try again."}, status=400)

class billList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']
        m_user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']

        result = SavePetrolPumpBill.objects.filter(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id, created_at__date = timezone.now(), bill_flag = False)
        serializer = merchantPetrolPumpBillSerializer(result, many=True)
        if result:
            return JsonResponse({'status': "success", 'data': serializer.data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "No Data Found !!!"}, status=400)

class singleBillDetails(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        id = request.POST['id']
        try:
            result = SavePetrolPumpBill.objects.get(id= id)
            serializer = merchantPetrolPumpBillSerializer(result)
        except:
            result = ""

        if result:
            return JsonResponse({'status': "success", 'data': serializer.data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve data !!!"}, status=400)

class dashboardBillCalculations(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']
        m_user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']
        result = SavePetrolPumpBill.objects.filter(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id, created_at__date = timezone.now(),bill_flag=False)
        total_amount = 0
        result_count = 0
        for res in result:
            # if res.amount != "":
                # addon_list = res.addon_product_cost.split(",")
                # total_amount = total_amount + float(res.amount) + float(res.addon_product_cost)
            total_amount = total_amount + float(res.total_amount)

        result_count = result.count()
        
        if m_business_id:
            return JsonResponse({'status': "success", 'total_amount': float(total_amount), 'total_bills': result_count}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve data !!!"}, status=400)

@csrf_exempt
def petrolPumpSendBill(request):
    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        bill_id = request.POST['bill_id']

        bill_object = SavePetrolPumpBill.objects.get(id = bill_id)

        user_object = GreenBillUser.objects.get(id = bill_object.m_user_id)

        business_id = bill_object.m_business_id

        subscription_object = getActiveSubscriptionPlan(request, business_id) 

        if subscription_object:

            try:
                merchant_bussiness = MerchantProfile.objects.get(id = business_id)
            except:
                merchant_bussiness = ""

            try:
                setting = petrol_pump_app_setting_model.objects.get(merchant_id = user_object, merchant_bussiness = merchant_bussiness)
                digital_bill = setting.digital_bill
                sms = setting.sms

            except:
                digital_bill = True
                sms = False

            customer_bill_url = "http://157.230.228.250/petrol-pump-bill/" + str(bill_object.bill_url) + "/"

            s = pyshorteners.Shortener()

            short_url = s.tinyurl.short(customer_bill_url)

            if digital_bill == True:

                if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_digital_bill_cost):

                    SavePetrolPumpBill.objects.filter(id = bill_id).update(greenbill_digital_bill = True)

                    device = DeviceId.objects.filter(mobile_no=mobile_no).first()
                    push_service = FCMNotification(api_key=settings.API_KEY)

                    if device != None:
                        registration_id = device.device_id
                    else:
                        registration_id = ""

                    message_title = "New Bill"

                    message_body = "Hey Green Bill user, view and download your bill here. " + str(customer_bill_url)

                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

                    total_amount_avilable_new = 0
                    total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_digital_bill_cost)
                    subscription_object.total_amount_avilable = total_amount_avilable_new
                    subscription_object.save()

                    return JsonResponse({'status':'success', 'message': 'Notification send successfully'}, status=200)
                else:
                    return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)

            elif sms == True:

                if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

                    device = DeviceId.objects.filter(mobile_no=mobile_no).first()

                    push_service = FCMNotification(api_key=settings.API_KEY)

                    if device != None:
                        SavePetrolPumpBill.objects.filter(id = bill_id).update(greenbill_digital_bill = True)

                        registration_id = device.device_id

                        message_title = "New Bill"

                        message_body = "Hey Green Bill user, view and download your bill here. " + str(customer_bill_url)

                        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

                        total_amount_avilable_new = 0
                        total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_digital_bill_cost)
                        subscription_object.total_amount_avilable = total_amount_avilable_new
                        subscription_object.save()

                        return JsonResponse({'status':'success', 'message': 'Notification send successfully'}, status=200)
                
                    else:
                        registration_id = ""

                        if mobile_no:

                            SavePetrolPumpBill.objects.filter(id = bill_id).update(greenbill_sms_bill = True)

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

                            return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)

                        else:
                            return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                else:
                    return JsonResponse({'status' : 'error', 'message': "Insufficient Balance. Please purchase Add On's and try again !!!"}, status=400)
            else:
                return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)
        else:
            return JsonResponse({'status':'error', 'message': "You don't have active Green Bill Subscription. Please purchase and try again."}, status=400)
    else:
        return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)


class savePetrolPumpBillFile(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        bill_id = request.POST['bill_id']

        bill_file_temp = request.FILES['bill_file']

        bill_object = SavePetrolPumpBill.objects.get(id = bill_id)

        bill_object.bill_file = bill_file_temp

        letters = string.ascii_letters
        digit = string.digits
        random_string = str(bill_id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
        
        bill_object.bill_url = random_string

        bill_object.save()

        if bill_object:
            return JsonResponse({'status': "success"}, status=200)
        else:
            return JsonResponse({'status': "error"}, status=400)

class PetrolPumpBusinessDetails(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']
        m_user_id = request.POST['m_user_id']

        business_details = MerchantProfile.objects.filter(id = m_business_id, m_user_id = m_user_id, m_business_category_id=11)

        base_url = "http://157.230.228.250"
                    
        if business_details[0].m_business_logo:
            m_business_logo = str(base_url) + str(business_details[0].m_business_logo.url)
        else:
            m_business_logo = None

        try:
            merchant_bussiness = MerchantProfile.objects.get(id = m_business_id)
            print(merchant_bussiness)
        except:
            merchant_bussiness = ""
        
        try:
            setting = petrol_pump_app_setting_model.objects.filter(merchant_id = m_user_id,merchant_bussiness = merchant_bussiness).order_by('-id')
            print(setting)
            footer_text1 = setting[0].footer_text1
            footer_text2 = setting[0].footer_text2
            footer_text3 = setting[0].footer_text3
            header_text1 = setting[0].header_text1
            header_text2 = setting[0].header_text2
            header_text3 = setting[0].header_text3

            digital_bill = setting[0].digital_bill
            sms = setting[0].sms

        except:
            footer_text1 = ""
            footer_text2 = ""
            footer_text3 = ""
            header_text1 = ""
            header_text2 = ""
            header_text3 = ""

            digital_bill = True
            sms = False

        try:
            addon_status_temp = AddonPetrolPump.objects.filter(m_business_id = m_business_id)

            if addon_status_temp.count() >= 1:
                addon_status = True
            else:
                addon_status = False
        except:
            addon_status = False

        business_data = {
            'm_user_id': m_user_id,
            'm_business_id': business_details[0].id,
            'm_business_name': business_details[0].m_business_name,
            'm_business_logo': m_business_logo,
            'm_address': business_details[0].m_address, 
            'm_area': business_details[0].m_area, 
            'm_city': business_details[0].m_city,
            'm_district' : business_details[0].m_district,
            'm_state' : business_details[0].m_state,
            'm_gstin': business_details[0].m_gstin,
            'digital_bill': digital_bill,
            'sms': sms,
            'footer_text1': footer_text1,
            'footer_text2' : footer_text2,
            'footer_text3' : footer_text3,
            'header_text1': header_text1,
            'header_text2': header_text2,
            'header_text3': header_text3,
            'addon_status': addon_status,
            'm_vat_tin_number' : business_details[0].m_vat_tin_number,

        }

        if business_data:
            return JsonResponse({'status': 'success', 'business_details': business_data}, status=200)
        else:
            return JsonResponse({'status': "error"}, status=400)


class AddonsProductList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        try:
            result = AddonPetrolPump.objects.filter(m_business_id = m_business_id)

        except:
            result = ""

        serializer = AddonsProductListSerializer(result, many=True)
        
        if result:
            return JsonResponse({'status': "success", "data": serializer.data}, status=200)
        else:
            return JsonResponse({'status': "error"}, status=400)


class PetrolNozzleList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        # try:
        #     result = MerchantPetrolNozzle.objects.filter(m_business_id = m_business_id)

        # except:
        #     result = ""

        # serializer = MerchantPetrolNozzleListSerializer(result, many=True)

        

        try:
            nozzle_count_temp = NozzleCount.objects.get(business_id = m_business_id)

            nozzle_list = []

            for x in range(1, int(nozzle_count_temp.nozzle_count) + 1):
                nozzle_list.append({
                    'id': x,
                    'nozzle':str(x)
                    })
            result = True

        except:
            result = False
        
        if result:
            return JsonResponse(nozzle_list, status=200, safe=False)
            # return JsonResponse(serializer.data, status=200, safe=False)
        else:
            return JsonResponse({'status': "error"}, status=400)

class PetrolBillAddFlag(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        bill_id = request.POST['bill_id']

        flag_by = request.POST['flag_by']

        bill_flag_status_temp = SavePetrolPumpBill.objects.filter(id = bill_id)

        bill_flag_status = bill_flag_status_temp[0].bill_flag

        if bill_flag_status == True:
            bill_flag = False
        else:
            bill_flag = True

        try:
            reason_id = request.POST['reason_id']
            reason = request.POST['reason']
        except:
            reason_id = ""
            reason = ""

        result =  SavePetrolPumpBill.objects.filter(id = bill_id).update(bill_flag = bill_flag, flag_update_at = timezone.now(), flag_by = flag_by, reason_id = reason_id, reason = reason)
        
        if result:
            return JsonResponse({'status' : 'success'}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)



class petrolLogout(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        merchant_user_id = request.POST['merchant_user_id']

        result = PetrolLog.objects.filter(user_id = merchant_user_id, created_at__date = timezone.now()).update(logout_at = timezone.now())

        if result:
            return JsonResponse({'status' : 'success'}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class getflagReason(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        try:
            result = flagbillreason.objects.filter(m_business_id = m_business_id)

        except:
            result = ""

        serializer = FlagBillReasontSerializer(result, many=True)
        
        if result:
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            return JsonResponse({'status': "error"}, status=400)



# Other Modules

class ManageProduct(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            product_id = request.POST['id']
        except:
            product_id = ""

        if product_id:
            m_business_id = request.POST['m_business_id']
            product_name = request.POST['product_name']
            product_cost = request.POST['product_cost']
            product_availability = request.POST['product_availability'] # ('Yes', 'Yes'), ('No', 'No')

            result = MerchantPetrolPump.objects.filter(id = product_id).update(product_name = product_name, product_cost = product_cost, product_availability = product_availability)

            if result:
                return JsonResponse({'status': 'success', 'message': "Product updated successfully !!!"}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': "Failed to updated product !!!"}, status=400)

        else:
            m_business_id = request.POST['m_business_id']
            product_name = request.POST['product_name']
            product_cost = request.POST['product_cost']
            product_availability = request.POST['product_availability'] # ('Yes', 'Yes'), ('No', 'No')

            isProductIdExists = False
            isProductNameExists = MerchantPetrolPump.objects.filter(m_business_id= m_business_id, product_name = product_name)
            merchant_id = MerchantProfile.objects.get(id = m_business_id)
            merchant_object = GreenBillUser.objects.get(mobile_no = merchant_id.m_user)
            if isProductNameExists:
                return JsonResponse({'status': 'erroe', 'message': "Product with same name already exists !"}, status=400)
            else:
                result = MerchantPetrolPump.objects.create(user= merchant_object, m_business_id= m_business_id, product_id= product_id, product_name=product_name, product_cost=product_cost, product_availability= product_availability)

                if result:
                    return JsonResponse({'status': 'success', 'message': "Product added successfully !!!"}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': "Failed to add product !!!"}, status=400)


class ManageProductList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        result = MerchantPetrolPump.objects.filter(m_business_id = m_business_id)

        serializer = ManageProductListSerializer(result, many=True)
        
        if result:
            return JsonResponse({'status': "success", "data": serializer.data}, status=200)
        else:
            return JsonResponse({'status': "error"}, status=400)


class ManageNozzle(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']
        nozzle_count = request.POST['nozzle_count']

        result = NozzleCount.objects.update_or_create(business_id = m_business_id, defaults={'nozzle_count': nozzle_count})

        if result:
            return JsonResponse({'status': 'success', 'message': "Nozzle Count added successfully !!!"}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to add Nozzle Count !!!"}, status=400)


class ManageNozzleCount(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        result = NozzleCount.objects.filter(business_id = m_business_id)

        if result:
            return JsonResponse({'status': 'success', 'message': result[0].nozzle_count}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)


class AdOnProducts(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            product_id = request.POST['id']
        except:
            product_id = ""

        if product_id:
            m_business_id = request.POST['m_business_id']
            product_name = request.POST['product_name']
            product_cost = request.POST['product_cost']
            product_availability = request.POST['product_availability'] # ('Yes', 'Yes'), ('No', 'No')

            result = AddonPetrolPump.objects.filter(id = product_id).update(product_name = product_name, product_cost = product_cost, product_availability = product_availability)

            if result:
                return JsonResponse({'status': 'success', 'message': "Product updated successfully !!!"}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': "Failed to updated product !!!"}, status=400)

        else:
            m_business_id = request.POST['m_business_id']
            product_name = request.POST['product_name']
            product_cost = request.POST['product_cost']
            product_availability = request.POST['product_availability'] # ('Yes', 'Yes'), ('No', 'No')

            isProductIdExists = False
            isProductNameExists = AddonPetrolPump.objects.filter(m_business_id= m_business_id, product_name = product_name)

            if isProductNameExists:
                return JsonResponse({'status': 'erroe', 'message': "Product with same name already exists !"}, status=400)
            else:
                result = AddonPetrolPump.objects.create(m_business_id= m_business_id, product_name=product_name, product_cost=product_cost, product_availability= product_availability)

                if result:
                    return JsonResponse({'status': 'success', 'message': "Product added successfully !!!"}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': "Failed to add product !!!"}, status=400)


class AdOnProductList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        result = AddonPetrolPump.objects.filter(m_business_id = m_business_id)

        serializer = AdOnProductListSerializer(result, many=True)
        
        if result:
            return JsonResponse({'status': "success", "data": serializer.data}, status=200)
        else:
            return JsonResponse({'status': "error"}, status=400)


class DeleteSelectedFlagBill(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        bill_ids = request.POST['bill_ids']

        bill_ids_list = []

        if bill_ids:
            bill_ids_list = list(bill_ids.split(",")) 
        else:
            bill_ids_list = ""

        if bill_ids:
            for bill_id in bill_ids_list:
                SavePetrolPumpBill.objects.filter(id = bill_id).delete()
            result = True

        else:
            result = False
        
        if result:
            return JsonResponse({'status' : 'success'}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class DeleteFlagBill(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        bill_id = request.POST['bill_id']
        
        result = SavePetrolPumpBill.objects.filter(id = bill_id).delete()
        
        if result:
            return JsonResponse({'status' : 'success'}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class FlagBillList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        from_date = request.POST.get('from_date')

        to_date = request.POST.get('to_date')

        result = SavePetrolPumpBill.objects.filter(m_business_id = m_business_id, bill_flag = True).order_by('-id')

        data = []

        for bill in result:
            try:
                user_object = GreenBillUser.objects.get(id = bill.flag_by)
                flag_by_name = user_object.first_name + ' ' + user_object.last_name
            except:
                flag_by_name = ""

            flag_temp_time = str(bill.flag_update_at.time()).split('.')[0]

            data.append({
                    'id' : bill.id,
                    'mobile_no' : bill.mobile_no,
                    'invoice_no' : bill.invoice_no,
                    'amount' : bill.total_amount,
                    'created_by' : bill.worker_name,
                    'Created_date' : bill.date,
                    'flagged_by' : flag_by_name,
                    'flagged_date' : datetime.strptime(str(bill.flag_update_at.date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'flagged_time' : datetime.strptime(str(flag_temp_time), '%H:%M:%S').strftime('%H:%M'),
                    'flagged_reason' : bill.reason
                })

        total_flag_bills = 0
        for bill in data:
            total_flag_bills = total_flag_bills + 1

        new_data = []

        if from_date and to_date:
            if data:
                if from_date:
                    from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

                if to_date:
                    to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')


                for bill in data:
                    flagged_date = datetime.strptime(str(bill['flagged_date']), '%d-%m-%Y').strftime('%Y-%m-%d')
                    if from_date and to_date:    
                        if flagged_date >= from_date and flagged_date <= to_date:
                            new_data.append(bill)

                new_data.sort(key = lambda x: datetime.strptime(x['flagged_date'], '%d-%m-%Y'), reverse = True)
                total_flag_bills = 0
                for bill in new_data:
                    total_flag_bills = total_flag_bills + 1

                if new_data:
                    return JsonResponse({'status': "success", "data": new_data, "from_date":from_date,"to_date":to_date,"total_flag_bills":total_flag_bills}, status=200)
                else:
                    return JsonResponse({'status': "error"}, status=400)
        else:
            if result:
                return JsonResponse({'status': "success", "data": data, "from_date":"", "to_date":"","total_flag_bills": total_flag_bills}, status=200)
            else:
                return JsonResponse({'status': "error"}, status=400)



def petrolPumpBill(request, id):
    try:
        bill_details = SavePetrolPumpBill.objects.get(bill_url=id)

        try:
            merchant_user_object = GreenBillUser.objects.get(id = bill_details.m_user_id)

        except:
            merchant_user_object = ""

        try:

            merchant_business_object = MerchantProfile.objects.get(id = bill_details.m_business_id)

        except:
            merchant_business_object = ""


        try:
            bill_design = bill_designs.objects.get(merchant_business_id = merchant_business_object)
        except:
            bill_design = ""

        try:
            merchant_business_object = MerchantProfile.objects.get(id = bill_details.m_business_id)

            if merchant_business_object.m_business_logo:
                business_logo = merchant_business_object.m_business_logo.url
            else:

                if bill_design:
                    if bill_design.logo == "circular":
                        business_logo = "http://157.230.228.250/media/bill_design/circular-logo (2).png"
                    elif bill_design.logo == "square":
                        business_logo = "http://157.230.228.250/media/bill_design/rounded-corner-logo.png"
                    else:
                        business_logo = "http://157.230.228.250/static/assets/img/dashboard-logo.png"
                else:
                    business_logo = "http://157.230.228.250/static/assets/img/dashboard-logo.png"

            if merchant_business_object.m_address:
                business_address = merchant_business_object.m_address
            else:
                business_address = ""

        except:
            if bill_design:
                if bill_design.logo == "circular":
                    business_logo = "http://157.230.228.250/media/bill_design/circular-logo (2).png"
                elif bill_design.logo == "square":
                    business_logo = "http://157.230.228.250/media/bill_design/rounded-corner-logo.png"
                else:
                    business_logo = "http://157.230.228.250/static/assets/img/dashboard-logo.png"
            else:
                business_logo = "http://157.230.228.250/static/assets/img/dashboard-logo.png"

            business_address = ""



        ads_image_details = ""
        today = datetime.strptime(str(date.today()), '%Y-%m-%d')
        space = ads_below_bill.objects.filter(merchant = merchant_user_object, ads_type='green_bill').last()
        try:
            if space:
                expiry_date_new = datetime.strptime(space.end_date, '%Y-%m-%d')
                start_date_new = datetime.strptime(space.start_date, '%Y-%m-%d')

                if today >= start_date_new and today <= expiry_date_new:
                    startswith = str(11) + ','
                    endswith = ','+ str(11)
                    contains = ','+ str(11) + ','
                    exact = str(11)

                    green_bill_merchant_ads = ads_for_green_bills.objects.filter(
                        Q(business_category_value__startswith = startswith) | 
                        Q(business_category_value__endswith = endswith) | 
                        Q(business_category_value__contains = contains) | 
                        Q(business_category_value__exact = exact)
                    ).last()

                    if green_bill_merchant_ads:

                        start_date = datetime.strptime(green_bill_merchant_ads.start_date, '%Y-%m-%d')
                        end_date = datetime.strptime(green_bill_merchant_ads.end_date, '%Y-%m-%d')

                        if today >= start_date and today <= end_date:
                            ads_image_details = ads_for_green_bills.objects.get(id = green_bill_merchant_ads.id)
                            views = ads_below_bill.objects.get(id=space.id)
                            views.count = views.count + 1
                            views.save()
        except:
            ads_image_details = ""
        

        try:
            payment_settings = MerchantPaymentSetting.objects.get(m_business_id = bill_details.m_business_id)
        except:
            payment_settings = ""

        context = {}
        # print('PaymentSetting', payment_settings)
        if  payment_settings:

            if bill_details.payment_done == False:

                key = str(payment_settings.payu_key)
            
                SALT= str(payment_settings.payu_salt)

                # PAYU_BASE_URL = "https://test.payu.in/_payment"
                PAYU_BASE_URL = "https://secure.payu.in/_payment"

                action = ''
                firstname = str('My bill')
                email = str('shreyash.t@zappkode.com')
                phone = str(bill_details.mobile_no)
                surl = "http://157.230.228.250/my-bill-petrol-payment-link-success/"
                furl = "http://157.230.228.250/my-bill-petrol-payment-link-fail/"

                udf1 = id
                udf2 = ""
                udf3 = ""
                udf4 = ""
                udf5 = ""

                random_str =  random.randint(9999999, 99999999)

                hash_object = hashlib.sha256(b'randint(0,20)' + bytes(bill_details.id) + bytes(random_str))

                txnid=hash_object.hexdigest()[0:20]

                hashh = ''
                context = {}
                posted = {}
                posted['txnid'] = txnid
                posted['key'] = key
                productinfo = str('my bill pay link')
                amount = str(bill_details.amount)

                hashSequence = key + "|" + txnid + "|" + amount + "|" + productinfo + "|" + firstname + "|" + email + "|" + udf1 + "|" + udf2 + "|" + udf3 + "|" + udf4 + "|" + udf5 + "||||||" + SALT

                hash_string = hashSequence.encode('utf-8')

                hashh = hashlib.sha512(hash_string).hexdigest().lower()

                context['hashh'] = hashh
                context['posted'] = posted
                context['txnid'] = txnid 
                context['hash_string'] = hash_string
                context['amount'] = amount
                context['productinfo'] = productinfo
                context['udf1'] = udf1
                context['udf2'] = udf2
                context['udf3'] = udf3
                context['udf4'] = udf4
                context['firstname'] = firstname
                context['email'] = email
                context['phone'] = phone
                context['surl'] = surl
                context['furl'] = furl
                context['action'] = PAYU_BASE_URL
                context['MERCHANT_KEY'] = key
                
        # context['payment_link'] = payment_link
        context['bill_details'] = bill_details
        context['ads_image_details'] = ads_image_details
        context['business_logo'] = business_logo
        context['business_address'] = business_address
        context['bill_design'] = bill_design
        context['url_slug'] = id
        # context = {'bill_details' : bill_details,
        #  'ads_redirect_url': ads_redirect_url,
        #   'ads_image':ads_image, 
        #   'business_logo': business_logo,
        #    'business_address' : business_address,
        #     'bill_design' : bill_design, 'url_slug':id}
        # context['ads_id'] = ads_id
        return render(request, "merchant/petrol-app-bill-new.html", context)

    except:
        return render(request, 'page-404.html')
  
def view_petrol_pump_ads(request, id):
    data = []
    base_url = "http://157.230.228.250/"
    ads_details = ads_below_bill.objects.filter(active_ads = True)
    green_bill_merchant_ads = ads_for_green_bills.objects.filter(active_ads = True)
    if ads_details:
        try:
            object = ads_below_bill.objects.get(id=id)
            redirect_url = object.redirect_url
            object.count = object.count + 1
            object.save()
            redirect_url = green_bill_merchant_ads[0].redirect_url
        except:
            pass
    else:
        try: 
            redirect_url = green_bill_merchant_ads[0].redirect_url
            object = ads_for_green_bills.objects.get(id=id)
            object.count = object.count + 1
            object.save()
        except:
            pass

    
    return redirect(redirect_url)

@csrf_exempt
def payment_link_success(request):



    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount= request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    udf1 = request.POST["udf1"]
    udf2 = request.POST["udf2"]
    udf3 = request.POST["udf3"]
    udf4 = request.POST["udf4"]
    udf5 = ""
    link_url = udf1
    mihpayid = request.POST["mihpayid"]
    payment_link = SavePetrolPumpBill.objects.get(bill_url=link_url)

    try:
        payment_settings = MerchantPaymentSetting.objects.get(m_business_id = payment_link.m_business_id)
    except:
        payment_settings = ""

    SALT = str(payment_settings.payu_salt)

    retHashSeq = SALT +'|'+status+'|||||||'+ udf4 + '|' + udf3 + '|' +  udf2 +'|'+ udf1 + '|' + email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+ key

    hash_string = retHashSeq.encode('utf-8')
    
    hashh = hashlib.sha512(hash_string).hexdigest().lower()

    if status == "success":
        if hashh == posted_hash:
            
            result = SavePetrolPumpBill.objects.filter(id=payment_link.id).update(payment_done = True, payment_date = timezone.now(), transaction_id = txnid, payu_transaction_id = mihpayid)
            if result:
                sweetify.success(request, title="Success", icon='success', text='Transcation done Successfully.', timer=1500)
                return redirect(petrolPumpBill, link_url)
            else:
                sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
                return redirect(petrolPumpBill, link_url)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
            return redirect(petrolPumpBill, link_url)
    else:
        sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
        return redirect(petrolPumpBill, link_url)

@csrf_exempt
def payment_link_fail(request):
    udf1 = request.POST["udf1"]
    sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
    return redirect(petrolPumpBill, udf1)



def reject_petrol_bill(request):

    if request.method == "POST":

        bill_id = request.POST['bill_id']

        bill_object = SavePetrolPumpBill.objects.get(id=bill_id)

        bill_url = bill_object.bill_url

        rejectbillRadio = request.POST['rejectbillRadio']

        if rejectbillRadio == "1":
            reject_reason = "This is not my bill"

        elif rejectbillRadio == "2":
            reject_reason = "There are mistakes in the bill"

        result = SavePetrolPumpBill.objects.filter(id=bill_id).update(reject_status = True, reject_reason = reject_reason)

        try:

            bill_data = SavePetrolPumpBill.objects.get(id = bill_id)

            merchant_user = MerchantProfile.objects.get(id = bill_data.m_business_id)

            device = DeviceId.objects.filter(mobile_no=merchant_user.m_user, user_type = 'merchant').first()
                
            if device:

                push_service = FCMNotification(api_key=settings.API_KEY)

                result = ''

                if device:
                    registration_id = device.device_id
                else:
                    registration_id = ""

                message_title = "Rejected Bill"

                message_body = "Bill was rejected. Kindly check for details. "

                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        except:
            pass

        if result:
            sweetify.success(request, title="Success", icon='success', text='Bill Rejected Successfully.', timer=1500)
            return redirect(petrolPumpBill, id = bill_url)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Reject.', timer=1500)
            return redirect(petrolPumpBill, id = bill_url)
    else:
        return redirect(request, 'page-404.html')


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


