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

from my_subscription.models import *

from django.db.models import Q

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from merchant_setting.models import MerchantPaymentSetting
from merchant_role.models import merchant_userrole

import random
import hashlib

@csrf_exempt
def parkingLotMerchantLogin(request):
    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        password = request.POST['password']

        try:
            is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
            is_merchant_staff = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant_staff')[0]['is_merchant_staff']

            if is_merchant:
                
                user = authenticate(mobile_no=mobile_no, password=password)

                is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']

                if user:
                    is_business_parking_lot = MerchantProfile.objects.filter(m_user_id=user.id, m_business_category_id=12)
                else:
                    is_business_parking_lot = ""

                if user and is_merchant and is_business_parking_lot:
 
                    serializer = merchantSerializer(user)

                    base_url = "http://157.230.228.250"
                    
                    if is_business_parking_lot[0].m_business_logo:
                        m_business_logo = str(base_url) + str(is_business_parking_lot[0].m_business_logo.url)
                    else:
                        m_business_logo = None

                    merchant_user_id = Merchant_users.objects.filter(user_id = user.id).values('merchant_user_id')[0]['merchant_user_id']

                    try:
                        merchant_bussiness = MerchantProfile.objects.get(id = is_business_parking_lot[0].id, m_user = merchant_user_id)
                        print(merchant_bussiness)
                    except:
                        merchant_bussiness = ""

                    try:
                        setting = parking_app_setting_model.objects.filter(merchant_id = merchant_user_id, merchant_bussiness = merchant_bussiness)
                        header_text1 = setting[0].header_text1
                        header_text2 = setting[0].header_text2
                        header_text3 = setting[0].header_text3
                        footer_text1 = setting[0].footer_text1
                        footer_text2 = setting[0].footer_text2
                        footer_text3 = setting[0].footer_text3
                        digital_bill = setting[0].digital_bill
                        sms = setting[0].sms
                        pay_bill_at_exit_gate = setting[0].pay_bill_at_exit_gate

                    except:
                        header_text1 = ""
                        header_text2 = ""
                        header_text3 = ""
                        footer_text1 = ""
                        footer_text2 = ""
                        footer_text3 = ""
                        digital_bill = True
                        sms = False
                        pay_bill_at_exit_gate = False


                    try:
            
                        result = parking_app_setting_model.objects.get(merchant_id = merchant_user_id, merchant_bussiness = merchant_bussiness)

                        if result.exit_gate:
                            exit_gate_status = True
                            pay_bill_at_exit_gate = True

                        else:
                            exit_gate_status = False
                            pay_bill_at_exit_gate = False

                    except:

                        exit_gate_status = False
                        pay_bill_at_exit_gate = False


                    business_object = MerchantProfile.objects.get(id = is_business_parking_lot[0].id)

                    try:
                        parking_app_setting = parking_app_setting_model.objects.get(merchant_id = business_object.m_user, merchant_bussiness = merchant_bussiness)

                        manage_space = parking_app_setting.manage_space

                    except:
                        manage_space = False

                    business_data = {
                        'm_user_id': merchant_user_id,
                        'm_business_id': is_business_parking_lot[0].id,
                        'm_business_name': is_business_parking_lot[0].m_business_name,
                        'm_business_logo': m_business_logo,
                        'm_address': is_business_parking_lot[0].m_address, 
                        'm_area': is_business_parking_lot[0].m_area, 
                        'm_city': is_business_parking_lot[0].m_city,
                        'm_district' : is_business_parking_lot[0].m_district,
                        'm_state' : is_business_parking_lot[0].m_state,
                        'm_gstin': is_business_parking_lot[0].m_gstin,
                        'header_text1': header_text1,
                        'header_text2': header_text2,
                        'header_text3' : header_text3,
                        'footer_text1': footer_text1,
                        'footer_text2': footer_text2,
                        'footer_text3': footer_text3,
                        'digital_bill': digital_bill,
                        'sms': sms,
                        'exit_gate_status': exit_gate_status,
                        'pay_bill_at_exit_gate': pay_bill_at_exit_gate,
                        'manage_space': manage_space
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

                    login_status = ParkingLog.objects.filter(user_id = merchant_user_id, created_at__date = timezone.now())
                    
                    if login_status:
                        pass
                    else:
                        ParkingLog.objects.create(user_id = merchant_user_id, login_at = timezone.now())

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
                        
                        is_business_parking_lot = MerchantProfile.objects.filter(id= m_business_id, m_user_id=merchant_user_id, m_business_category_id=12)
                    else:
                        is_business_parking_lot = ""
                    
                    if user and is_merchant_staff and is_business_parking_lot:
                        
                        serializer = merchantSerializer(user)

                        base_url = "http://157.230.228.250"
                        
                        if is_business_parking_lot[0].m_business_logo:
                            m_business_logo = str(base_url) + str(is_business_parking_lot[0].m_business_logo.url)
                        else:
                            m_business_logo = None

                        merchant_user_id = Merchant_users.objects.filter(user_id = user.id).values('merchant_user_id')[0]['merchant_user_id']
                        
                        try:
                            merchant_bussiness = MerchantProfile.objects.get(id = m_business_id, m_user = merchant_user_id)
                            print(merchant_bussiness)
                        except:
                            merchant_bussiness = ""
                        try:
                            setting = parking_app_setting_model.objects.filter(merchant_id = merchant_user_id, merchant_bussiness = merchant_bussiness)
                            header_text1 = setting[0].header_text1
                            header_text2 = setting[0].header_text2
                            header_text3 = setting[0].header_text3
                            footer_text1 = setting[0].footer_text1
                            footer_text2 = setting[0].footer_text2
                            footer_text3 = setting[0].footer_text3
                            digital_bill = setting[0].digital_bill
                            sms = setting[0].sms
                            pay_bill_at_exit_gate = setting[0].pay_bill_at_exit_gate

                        except:
                            header_text1 = ""
                            header_text2 = ""
                            header_text3 = ""
                            footer_text1 = ""
                            footer_text2 = ""
                            footer_text3 = ""
                            digital_bill = True
                            sms = False
                            pay_bill_at_exit_gate = False

                        try:

                            result = parking_app_setting_model.objects.get(merchant_id = merchant_user_id, merchant_bussiness = merchant_bussiness)

                            if result.exit_gate:
                                exit_gate_status = True
                                pay_bill_at_exit_gate = True

                            else:
                                exit_gate_status = False
                                pay_bill_at_exit_gate = False

                        except:

                            exit_gate_status = False
                            pay_bill_at_exit_gate = False


                        business_object = MerchantProfile.objects.get(id = is_business_parking_lot[0].id)

                        try:
                            parking_app_setting = parking_app_setting_model.objects.get(merchant_id = business_object.m_user, merchant_bussiness = merchant_bussiness)

                            manage_space = parking_app_setting.manage_space

                        except:
                            manage_space = False

                        business_data = {
                            'm_user_id': merchant_user_id,
                            'm_business_id': is_business_parking_lot[0].id,
                            'm_business_name': is_business_parking_lot[0].m_business_name,
                            'm_business_logo': m_business_logo,
                            'm_address': is_business_parking_lot[0].m_address, 
                            'm_area': is_business_parking_lot[0].m_area, 
                            'm_city': is_business_parking_lot[0].m_city,
                            'm_district' : is_business_parking_lot[0].m_district,
                            'm_state' : is_business_parking_lot[0].m_state,
                            'm_gstin': is_business_parking_lot[0].m_gstin,
                            'header_text1': header_text1,
                            'header_text2': header_text2,
                            'header_text3' : header_text3,
                            'footer_text1': footer_text1,
                            'footer_text2': footer_text2,
                            'footer_text3': footer_text3,
                            'digital_bill': digital_bill,
                            'sms': sms,
                            'exit_gate_status': exit_gate_status,
                            'pay_bill_at_exit_gate': pay_bill_at_exit_gate,
                            'manage_space' : manage_space
                        }

                        try:
                            token = Token.objects.create(user=user)
                        except:
                            token = Token.objects.get(user_id=user.id)

                        login_status = ParkingLog.objects.filter(user_id = user.id, created_at__date = timezone.now())
                        
                        if login_status:
                            pass
                        else:
                            ParkingLog.objects.create(user_id = user.id, login_at = timezone.now())

                        # try: 
                        #     profile_image_temp = UserProfileImage.objects.filter(user=user.id)
                        # except: 
                        #     profile_image_temp = ""

                        
                        # if profile_image_temp and profile_image_temp[0].m_profile_image:
                        #     profile_image = str(base_url) + str(profile_image_temp[0].m_profile_image.url)
                        # else:
                        #     profile_image = ""

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


class getParkingLotBusinessList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']
        try:
            merchant_users_object = Merchant_users.objects.get(user_id = user_id)
           
            merchant_general_setting = MerchantProfile.objects.filter(m_user_id=user_id, m_business_category_id=12)
            
        except:
            merchant_general_setting = ""

        if merchant_general_setting: 
            serializers = merchantBusinessSerializer(merchant_general_setting, many=True)
            return JsonResponse({'status': "success", 'data': serializers.data}, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Data Not Found !!!"}, status=400)


class getParkingLotVehicleTypeList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']
        try:
            result = MerchantParkingAddVehicle.objects.filter(m_business_id= m_business_id)
            
        except:
            result = ""

        data = []

        for vehicle_type in result:
            if MerchantParkingSpaceCharges.objects.filter(m_business_id = m_business_id, vehicle_type_id = vehicle_type.id):
                # data.append(vehicle_type)

                if vehicle_type.vehicle_type == "2 - Wheeler":
                    icon_url = "http://157.230.228.250/media/vehicle-types/2-wheeler.png"

                elif vehicle_type.vehicle_type == "4 - Wheeler":
                    icon_url = "http://157.230.228.250/media/vehicle-types/4-wheeler.png"

                elif vehicle_type.vehicle_type == "3 - Wheeler":
                    icon_url = "http://157.230.228.250/media/vehicle-types/3-wheeler.png"

                elif vehicle_type.vehicle_type == "Lorry":
                    icon_url = "http://157.230.228.250/media/vehicle-types/lorry.png"

                elif vehicle_type.vehicle_type == "Truck":
                    icon_url = "http://157.230.228.250/media/vehicle-types/truck.png"

                elif vehicle_type.vehicle_type == "Special Vehicle":
                    icon_url = "http://157.230.228.250/media/vehicle-types/special-vehicle.png"

                elif vehicle_type.vehicle_type == "Cycle":
                    icon_url = "http://157.230.228.250/media/vehicle-types/cycle.png"

                elif vehicle_type.vehicle_type == "Others":
                    icon_url = "http://157.230.228.250/media/vehicle-types/others.png"

                data.append({
                    'id' : vehicle_type.id,
                    'user' : vehicle_type.user.id if vehicle_type.user else "0",
                    'm_business_id' : vehicle_type.m_business_id,
                    'vehicle_type' : vehicle_type.vehicle_type,
                    'created_at' : vehicle_type.created_at,
                    'icon_url' : icon_url,
                })

        if result: 
            # serializers = parkingLotVehicleTypeSerializer(data, many=True)
            return JsonResponse({'status': "success", 'data': data}, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Data Not Found !!!"}, status=400)


class getParkingLotSpaceList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']

        merchant_object = GreenBillUser.objects.get(id=user_id)     

        try:
            # result = MerchantParkingLotSpace.objects.filter(user_id= user_id, m_business_id= m_business_id)

            # parking_app_setting_model.objects.filter(merchant_id)

        	result = parking_app_setting_model.objects.get(merchant_id = merchant_object)

        	if result.exit_gate:
        		exit_gate_status = True

        	else:
        		exit_gate_status = False

        except:
            exit_gate_status = False

        if exit_gate_status == True: 
            # serializers = parkingLotSpaceSerializer(result, many=True)
            # return JsonResponse({'status': "success", 'data': serializers.data}, status=200, safe=False)
            return JsonResponse({'status': "success", 'message': "Exit Gate Available"}, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Data Not Found !!!"}, status=400)

class getParkingLotSpaceChargesList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']
        try:
            result = MerchantParkingSpaceCharges.objects.filter(user= user_id, m_business_id= m_business_id)
            
        except:
            result = ""

        if result: 
            serializers = parkingLotSpaceChargesSerializer(result, many=True)
            return JsonResponse({'status': "success", 'data': serializers.data}, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Data Not Found !!!"}, status=400)


class generateParkingLotInvoiceNumber(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']
        m_user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']

        merchantDetails = MerchantProfile.objects.filter(id=m_business_id, m_user_id=m_user_id, m_business_category_id=12)

        year = timezone.now().year

        try:
            invoice = InvoiceNumberParkingLot.objects.filter(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id).last()
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


class saveParkingLotBill(generics.GenericAPIView):
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
        amount = request.POST['amount']
        date = request.POST['date']
        time = request.POST['time']
        # invoice_no = request.POST['invoice_no']
        exit_gate = request.POST['exit_gate']
        worker_name = request.POST['worker_name']
        additional_hours_charges = request.POST['additional_hours_charges']
        c_unique_id_temp = request.POST['c_unique_id']
        charges_by = request.POST['charges_by']

        business_id = m_business_id

        subscription_object = getActiveSubscriptionPlan(request, business_id)

        if subscription_object:
            print('Subscription plan')
            try:
                merchant_bussiness = MerchantProfile.objects.get(id = business_id)
            except:
                merchant_bussiness = ""

            try:
                setting = parking_app_setting_model.objects.get(merchant_bussiness = merchant_bussiness)
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
                    for_hours = request.POST['for_hours']
                    for_additional_hours = request.POST['for_additional_hours']
                except:
                    for_hours = ""
                    for_additional_hours = ""

                vehicle_type_id = request.POST['vehicle_type_id']

                business_object = MerchantProfile.objects.get(id = m_business_id)

                try:
                    parking_app_setting = parking_app_setting_model.objects.get(merchant_id = business_object.m_user, merchant_bussiness = business_object)

                    manage_space = parking_app_setting.manage_space

                except:
                    manage_space = False

                try:
            
                    is_checkoutpin_temp = request.POST['is_checkoutpin']
                    
                    if is_checkoutpin_temp == "true":
                        is_checkoutpin = True
                    else:
                        is_checkoutpin = False
                except:
                    is_checkoutpin = False

                # bill_file = request.POST['bill_file']

                merchantDetails = MerchantProfile.objects.filter(id=m_business_id, m_user_id=m_user_id, m_business_category_id=12)

                year = timezone.now().year

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

                
                try:
                    # invoice = InvoiceNumberParkingLot.objects.filter(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id).last()
                    invoice = InvoiceNumberParkingLot.objects.filter(m_business_id= m_business_id).last()
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


                result = SaveParkingLotBill.objects.create(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id, mobile_no= mobile_no, vehicle_type= vehicle_type, vehicle_number= vehicle_number, amount= amount, date= date, time= time, invoice_no= invoice_no, exit_gate= exit_gate, worker_name = worker_name, additional_hours_charges = additional_hours_charges, c_unique_id = c_unique_id, is_checkoutpin = is_checkoutpin, manage_space = manage_space, charges_by = charges_by, vehicle_type_id = vehicle_type_id, for_hours = for_hours, for_additional_hours = for_additional_hours)

                bill_data = SaveParkingLotBill.objects.filter(id= result.id)

                serializer = parkingLotBillSerializer(bill_data, many=True)


                try:
                    green_points_old = GreenPointsModel.objects.filter(mobile_no=mobile_no).values('green_points_count')[0]['green_points_count']
                except:
                    green_points_old = 0

                green_points_settings_object = GreenPointsSettings.objects.get(id = 1)
                green_points = green_points_settings_object.bill_points

                SaveParkingLotBill.objects.filter(id = result.id).update(green_points_earned = str(green_points))

                green_points_new = int(green_points_old) + int(green_points)

                try:
                    GreenPointsModel.objects.update_or_create(mobile_no=mobile_no, defaults={
                        'green_points_count': green_points_new})
                except:
                    pass

                if result:
                    invoice_result = InvoiceNumberParkingLot.objects.create(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id, invoice_no= invoice_no)
                    return JsonResponse({'status': "success", 'message': "Bill Added Successfully !!!", 'data': serializer.data}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "Failed to add Bill !!!"}, status=400)
        else:
            return JsonResponse({'status':'error', 'message': "You don't have active Green Bill Subscription. Please purchase and try again."}, status=400)


class editParkingLotBill(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        id = request.POST['id']
        user_id = request.POST['user_id']
        m_user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']
        mobile_no = request.POST['mobile_no']
        vehicle_type = request.POST['vehicle_type']
        vehicle_number = request.POST['vehicle_number']
        amount = request.POST['amount']
        date = request.POST['date']
        time = request.POST['time']
        invoice_no = request.POST['invoice_no']
        # exit_gate = request.POST['exit_gate']
        exit_check = request.POST['exit_check']
        # bill_file = request.POST['bill_file']
        out_date = request.POST['out_date']
        out_time = request.POST['out_time']
        duration = request.POST['duration']

        # print(exit_check)

        if exit_check == "true":
            exit_check_status = True
        else:
            exit_check_status = False
        
        result = SaveParkingLotBill.objects.filter(id=id).update(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id, mobile_no= mobile_no, vehicle_type= vehicle_type, vehicle_number= vehicle_number, amount= amount, date= date, time= time, invoice_no= invoice_no, exit_check = exit_check_status, out_date = out_date, out_time = out_time, duration = duration)
        
        # print(exit_check_status)
        # print(result)
        if result:
            invoice_result = InvoiceNumberParkingLot.objects.create(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id, invoice_no= invoice_no)
            return JsonResponse({'status': "success", 'message': "Bill Updated Successfully !!!"}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to Update Bill !!!"}, status=400)

class parkingLotbillList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']
        m_user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']

        result = SaveParkingLotBill.objects.filter(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id, created_at__date = timezone.now(), is_pass = False, bill_flag = False)
        
        bills = []
        for res in result:
            if (res.exit_check == True and res.exit_gate == "true") or (res.exit_gate == "true" and res.manage_space == False) or (res.exit_gate == "false" and (res.exit_check == False or res.exit_check == True)):
                bills.append(res)
                
        serializer = parkingLotBillSerializer(bills, many=True)
       

        if result:
            return JsonResponse({'status': "success", 'data': serializer.data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "No Data Found !!!"}, status=400)

class parkingLotSingleBillDetails(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        id = request.POST['id']
        try:
            result = SaveParkingLotBill.objects.get(id= id)
            serializer = parkingLotBillSerializer(result)
        except:
            result = ""

        if result:
            return JsonResponse({'status': "success", 'data': serializer.data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve data !!!"}, status=400)

class parkingLotDashboardBillCalculations(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']
        m_user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']

        result = SaveParkingLotBill.objects.filter(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id, created_at__date = timezone.now(), is_pass = False, bill_flag = False)

        total_amount = 0
        result_count = 0

        # print(result)

        # print(result.count())
        
        for res in result:
            if (res.exit_check == True and res.exit_gate == "true") or (res.exit_gate == "true" and res.manage_space == False) or (res.exit_gate == "false" and (res.exit_check == False or res.exit_check == True)):
            # if res.exit_check == False or res.exit_gate == 'false':
            # if (res.exit_check == True and res.manage_space == True) or (res.manage_space == False and res.exit_check == False):
                if res.amount != "" and res.is_pass == False:
                    total_amount = total_amount + float(res.amount)
                    result_count = result_count + 1


        result1 = ParkingLotPass.objects.filter(user_id = user_id, m_business_id= m_business_id, created_at__date = timezone.now()).order_by('-id')

        total_amount_pass = 0
        total_count_pass = 0

        for parking_pass in result1:
            total_amount_pass = total_amount_pass + float(parking_pass.amount)
            total_count_pass = total_count_pass + 1
        
        if m_business_id:
            return JsonResponse({'status': "success", 'total_amount': float(total_amount), 'total_bills': result_count, 'total_amount_pass': float(total_amount_pass), 'total_pass': total_count_pass}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve data !!!"}, status=400)

@csrf_exempt
def parkingLotSendBill(request):
       
        if request.method == "POST":

            mobile_no = request.POST['mobile_no']
            bill_id = request.POST['bill_id']

            bill_object = SaveParkingLotBill.objects.get(id = bill_id)

            user_object = GreenBillUser.objects.get(id = bill_object.m_user_id)

            business_id = bill_object.m_business_id

            subscription_object = getActiveSubscriptionPlan(request, business_id) 

            if subscription_object:

                try:
                    merchant_bussiness = MerchantProfile.objects.get(id = business_id)
                except:
                    merchant_bussiness = ""

                try:
                    setting = parking_app_setting_model.objects.get(merchant_id = user_object, merchant_bussiness = merchant_bussiness)
                    digital_bill = setting.digital_bill
                    sms = setting.sms

                except:
                    digital_bill = True
                    sms = False

                customer_bill_url = "http://157.230.228.250/parking-lot-bill/" + str(bill_object.bill_url) + "/"

                s = pyshorteners.Shortener()

                short_url = s.tinyurl.short(customer_bill_url)

                if digital_bill == True:

                    if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_digital_bill_cost):

                        SaveParkingLotBill.objects.filter(id = bill_id).update(greenbill_digital_bill = True)

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

                        SaveParkingLotBill.objects.filter(id = bill_id).update(greenbill_sms_bill = True)

                        device = DeviceId.objects.filter(mobile_no=mobile_no).first()
                        push_service = FCMNotification(api_key=settings.API_KEY)

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

                            if mobile_no:

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
    # except:
    #     return render(request, 'page-404.html')

    

class saveParkingLotPass(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        m_business_id = request.POST['m_business_id']
        mobile_no = request.POST['mobile_no']
        amount = request.POST['amount']
        valid_from = datetime.strptime(request.POST['valid_from'], '%d-%m-%Y').strftime('%Y-%m-%d')
        valid_to = datetime.strptime(request.POST['valid_to'], '%d-%m-%Y').strftime('%Y-%m-%d')
        comments = request.POST["comments"]
        vehical_no = request.POST["vehical_no"]
        m_user_id = request.POST["m_user_id"]

        try:
            user_id = request.POST['user_id']
        except:
            user_id = ""

        try:
            company_id = request.POST["company_id"]
            company_name = request.POST["company_name"]
            pass_type = request.POST["pass_type"]

        except:
            company_id = ""
            company_name = ""
            pass_type = ""

        try:
            vehicle_type = request.POST["vehicle_type"]
            vehicle_type_id = request.POST["vehicle_type_id"]

        except:
            vehicle_type = ""
            vehicle_type_id = ""


        result = ParkingLotPass.objects.create(user_id = user_id, m_business_id = m_business_id, mobile_no = mobile_no, amount = amount, valid_from = valid_from, valid_to = valid_to, comments = comments, vehical_no = vehical_no, m_user_id = m_user_id, company_id = company_id, company_name = company_name, pass_type = pass_type, vehicle_type = vehicle_type, vehicle_type_id = vehicle_type_id)

        if result and mobile_no:

            if result.m_business_id:

                merchant_bussiness = MerchantProfile.objects.get(id = m_business_id)

            device = DeviceId.objects.filter(mobile_no=mobile_no, user_type='customer').first()

            if not device:
                device = DeviceId.objects.filter(mobile_no=mobile_no, user_type='merchant').first()
                
            push_service = FCMNotification(api_key=settings.API_KEY)

            if device != None:
                registration_id = device.device_id
            else:
                registration_id = ""

            message_title = "New Parking Pass"

            message_body = "You have received a Parking Pass from " + str(merchant_bussiness.m_business_name)

            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        if result:
            return JsonResponse({'status': "success", 'message': "Pass created Successfully !!!"}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to created Pass !!!"}, status=400)


class saveParkingLotBillFile(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        bill_id = request.POST['bill_id']

        bill_file_temp = request.FILES['bill_file']

        bill_object = SaveParkingLotBill.objects.get(id = bill_id)

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


def parkingLotBill(request, id):

    # for sample bill from cashmemo design for wesite sample bill on click
    try:
        if id == "954WyCu365ya":
            print(id)
            return render(request, "customer/customer_bill/sample-bill-dummy.html")
    
    except:
        return JsonResponse({'status': "error"}, status=400)
        
    try:
        bill_details = SaveParkingLotBill.objects.get(bill_url=id)

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
                    startswith = str(12) + ','
                    endswith = ','+ str(12)
                    contains = ','+ str(12) + ','
                    exact = str(12)

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
                surl = "http://157.230.228.250/my-bill-parking-payment-link-success/"
                furl = "http://157.230.228.250/my-bill-parking-payment-link-fail/"

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
        context['business_logo'] = business_logo
        context['business_address'] = business_address
        context['bill_design'] = bill_design
        context['url_slug'] = id
        context['ads_image_details'] = ads_image_details

        return render(request, "merchant/parking-app-bill-new.html", context)

    except:
        return render(request, 'page-404.html')
    

def view_parking_Lot_ads(request, id):
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
    payment_link = SaveParkingLotBill.objects.get(bill_url=link_url)

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
            
            result = SaveParkingLotBill.objects.filter(id=payment_link.id).update(payment_done = True, payment_date = timezone.now(), transaction_id = txnid, payu_transaction_id = mihpayid)
            if result:
                sweetify.success(request, title="Success", icon='success', text='Transcation done Successfully.', timer=1500)
                return redirect(parkingLotBill, link_url)
            else:
                sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
                return redirect(parkingLotBill, link_url)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
            return redirect(parkingLotBill, link_url)
    else:
        sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
        return redirect(parkingLotBill, link_url)

@csrf_exempt
def payment_link_fail(request):
    udf1 = request.POST["udf1"]
    sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
    return redirect(parkingLotBill, udf1)



class ParkingLotBusinessDetails(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']
        m_user_id = request.POST['m_user_id']

        business_details = MerchantProfile.objects.filter(id = m_business_id, m_user_id = m_user_id, m_business_category_id=12)

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
            setting = parking_app_setting_model.objects.filter(merchant_id = m_user_id, merchant_bussiness = merchant_bussiness)
            header_text1 = setting[0].header_text1
            header_text2 = setting[0].header_text2
            header_text3 = setting[0].header_text3
            footer_text1 = setting[0].footer_text1
            footer_text2 = setting[0].footer_text2
            footer_text3 = setting[0].footer_text3
            digital_bill = setting[0].digital_bill
            sms = setting[0].sms
            pay_bill_at_exit_gate = setting[0].pay_bill_at_exit_gate

        except:
            header_text1 = ""
            header_text2 = ""
            header_text3 = ""
            footer_text1 = ""
            footer_text2 = ""
            footer_text3 = ""
            digital_bill = True
            sms = False
            pay_bill_at_exit_gate = False

        try:
            
            result = parking_app_setting_model.objects.get(merchant_id = m_user_id, merchant_bussiness = merchant_bussiness)

            if result.exit_gate:
                exit_gate_status = True
                pay_bill_at_exit_gate = True

            else:
                exit_gate_status = False
                pay_bill_at_exit_gate = False

        except:

            exit_gate_status = False
            pay_bill_at_exit_gate = False

        business_object = MerchantProfile.objects.get(id = business_details[0].id)

        try:
            parking_app_setting = parking_app_setting_model.objects.get(merchant_id = business_object.m_user, merchant_bussiness = merchant_bussiness)

            manage_space = parking_app_setting.manage_space

        except:
            manage_space = False

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
            'header_text1' : header_text1,
            'header_text2' : header_text2,
            'header_text3' : header_text3,
            'footer_text1': footer_text1,
            'footer_text2' : footer_text2,
            'footer_text3' : footer_text3,
            'digital_bill': digital_bill,
            'sms': sms,
            'exit_gate_status': exit_gate_status,
            'pay_bill_at_exit_gate': pay_bill_at_exit_gate,
            'manage_space': manage_space
        }

        print(business_data)

        if business_data:
            return JsonResponse({'status': 'success', 'business_details': business_data}, status=200)
        else:
            return JsonResponse({'status': "error"}, status=400)
            

class ParkingLotSpaceAvailabilityDetails(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        m_business_id = request.POST['m_business_id']

        try:
            data= MerchantParkingLotSpace.objects.filter(m_business_id = m_business_id)
        except:
            data = ""

        from parking_lot_apis.models import SaveParkingLotBill

        data1 = []

        for data_temp in data:

            try:
                print(m_business_id)
                print(data_temp.vehicle_type)

                # temp = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, exit_gate = 'true')
                
                # space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, exit_gate = 'true').count()

                temp = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True)
                
                space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()
                
            except:
                space_avilable_count = 0

            space_avilable_count_temp = int(data_temp.spaces_count) - int(space_avilable_count)

            data1.append({
                        "id": data_temp.id,
                        "vehicle_type": data_temp.vehicle_type,
                        "space": data_temp.spaces_count,
                        "available_parking_space": str(space_avilable_count_temp),
                    })

        if data1:
            return JsonResponse({'status': 'success', 'business_details': data1}, status=200)
        else:
            return JsonResponse({'status': "error", "message": "Data not Available"}, status=400)


class GetAllPassesByUserId(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']
        m_user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']

        try:
            result = ParkingLotPass.objects.filter(user_id = user_id, m_user_id = m_user_id, m_business_id = m_business_id).order_by("-id")

            data = []

            for parking_pass in result:

                data.append({
                    "id": parking_pass.id,
                    "m_business_id": parking_pass.m_business_id,
                    "m_user_id": parking_pass.m_user_id,
                    "mobile_no" : parking_pass.mobile_no,
                    "amount" : parking_pass.amount,
                    "valid_from" : datetime.strptime(str(parking_pass.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    "valid_to" : datetime.strptime(str(parking_pass.valid_to), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    "comments" : parking_pass.comments,
                    "vehical_no" : parking_pass.vehical_no,
                    "created_at" : parking_pass.created_at,
                    "pass_type": parking_pass.pass_type,
                    "company_id": parking_pass.company_id,
                    "company_name": parking_pass.company_name,
                    "vehicle_type": parking_pass.vehicle_type
                });

        except:
            result = ""

        if result:
            return JsonResponse({'status': "success", 'data': data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve data !!!"}, status=400)

class ParkingBillAddFlag(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        bill_id = request.POST['bill_id']

        flag_by = request.POST['flag_by']

        bill_flag_status_temp = SaveParkingLotBill.objects.filter(id = bill_id)

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

        result =  SaveParkingLotBill.objects.filter(id = bill_id).update(bill_flag = bill_flag, flag_update_at = timezone.now(), flag_by = flag_by, reason_id = reason_id, reason = reason)
        
        if result:
            return JsonResponse({'status' : 'success'}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class parkingLotExitbillList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # user_id = request.POST['user_id']
        # m_user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']

        # business_object = MerchantProfile.objects.get(id = m_business_id)

        # try:
        #     parking_app_setting = parking_app_setting_model.objects.get(merchant_id = business_object.m_user)

        #     manage_space = parking_app_setting.manage_space

        # except:
        #     manage_space = False

        # # created_at__date = timezone.now(), 

        # # result = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, exit_check = False, exit_gate = 'true')
        # if manage_space == True:

        #     result = SaveParkingLotBill.objects.filter(m_business_id= m_business_id, exit_check = False)

        #     serializer = parkingLotBillSerializer(result, many=True)

        # else:
        #     result = ""

        result = SaveParkingLotBill.objects.filter(m_business_id = m_business_id, exit_check = False, manage_space = True)

        serializer = parkingLotBillSerializer(result, many=True)

        if result:
            return JsonResponse({'status': "success", 'data': serializer.data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "No Data Found !!!"}, status=400)


class SetParkingVehicleAsExit(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            pass_id =  request.POST['pass_id']

        except:
            pass_id = ""

        if pass_id:

            try:
                result1 = SaveParkingLotBill.objects.filter(pass_id = pass_id, exit_check = False).order_by('-id')[0]

            except:
                result1 = ""

            if result1:

                result = SaveParkingLotBill.objects.filter(id = result1.id).update(exit_check = True)

                if result:
                    return JsonResponse({'status' : 'success'}, status=200)
                else:
                    return JsonResponse({'status' : "error"}, status=400)

            else:
                return JsonResponse({'status' : "error", 'message':'Vehicle not Parked !!!'}, status=400)

        else:

            bill_ids = request.POST['bill_ids']

            bill_ids_list = []

            if bill_ids:
                bill_ids_list = list(bill_ids.split(",")) 
            else:
                bill_ids_list = ""

            if bill_ids:
                for bill_id in bill_ids_list:
                    SaveParkingLotBill.objects.filter(id = bill_id).update(exit_check = True)
                result = True

            else:
                result = False
        
            if result:
                return JsonResponse({'status' : 'success'}, status=200)
            else:
                return JsonResponse({'status' : "error"}, status=400)


class CheckParkingVehicleQRCode(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        bill_id = request.POST['bill_id']

        bill_object = SaveParkingLotBill.objects.get(id = bill_id)

        if bill_object.exit_check == True:
            return JsonResponse({'status' : 'success', 'message' : 'Invalid QR code'}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class parkingLotLogout(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        merchant_user_id = request.POST['merchant_user_id']

        result = ParkingLog.objects.filter(user_id = merchant_user_id, created_at__date = timezone.now()).update(logout_at = timezone.now())

        if result:
            return JsonResponse({'status' : 'success'}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)

class ParkingPassCharges(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        vehicle_type_id = request.POST['vehicle_type_id']

        result = MerchantParkingLotPassCharges.objects.filter(m_business_id = m_business_id, vehicle_type_id = vehicle_type_id)

        serializer = parkingpasschargesSerializer(result, many=True)

        # charges_list = []

        # charges_list.append({'charges': result[0].monthly_charges, 'name': 'Monthly Pass'})

        # charges_list.append({'charges': result[0].quarterly_charges, 'name': 'Quarterly Pass'})

        # charges_list.append({'charges': result[0].half_yearly_charges, 'name': 'Half Yearly Pass'})

        # charges_list.append({'charges': result[0].yearly_charges, 'name': 'Yearly Pass'})

        # charges_list.append({'charges': "0", 'name': 'Employee Pass'})

        if result:
            return JsonResponse(serializer.data, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class ParkingPassCompanies(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        result = CompniesName.objects.filter(m_business_id = m_business_id)

        serializer = parkingpasscompaniesSerializer(result, many=True)

        if result:
            return JsonResponse(serializer.data, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class saveParkingLotPassBill(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.POST['user_id']
        m_user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']
        amount = 0
        date = request.POST['date']
        time = request.POST['time']
        exit_gate = request.POST['exit_gate']
        worker_name = request.POST['worker_name']

        pass_id = request.POST['pass_id']

        pass_data = ParkingLotPass.objects.filter(id= pass_id, valid_to__gte = timezone.now())

        if pass_data:

            try:
                result_parked =  SaveParkingLotBill.objects.get(m_business_id = m_business_id, exit_check = False, manage_space = True, pass_id = pass_id)

                if result_parked:
                    is_vehicle_entered = True
                else:
                    is_vehicle_entered = False

            except:
                is_vehicle_entered = False

            if is_vehicle_entered == False:

                vehicle_number = pass_data[0].vehical_no
                mobile_no = pass_data[0].mobile_no
                company_name = pass_data[0].company_name
                vehicle_type = pass_data[0].vehicle_type
                vehicle_type_id = pass_data[0].vehicle_type_id

                business_object = MerchantProfile.objects.get(id = m_business_id)

                try:
                    parking_app_setting = parking_app_setting_model.objects.get(merchant_id = business_object.m_user, merchant_bussiness = business_object)

                    manage_space = parking_app_setting.manage_space

                except:
                    manage_space = False

                try:
            
                    is_checkoutpin_temp = request.POST['is_checkoutpin']
                    
                    if is_checkoutpin_temp == "true":
                        is_checkoutpin = True
                    else:
                        is_checkoutpin = False
                except:
                    is_checkoutpin = False
                
                result = SaveParkingLotBill.objects.create(user_id= user_id, m_user_id= m_user_id, m_business_id= m_business_id, mobile_no= mobile_no, vehicle_number= vehicle_number, amount= amount, date= date, time= time, exit_gate= exit_gate, worker_name = worker_name, is_checkoutpin = is_checkoutpin, manage_space = manage_space, is_pass = True, pass_company_name = company_name, vehicle_type = vehicle_type, vehicle_type_id = vehicle_type_id, pass_id = pass_id)
                
                if result:
                    return JsonResponse({'status': "success", 'message': "Vehicle Entered Successfully !!!", }, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "Failed to Add !!!"}, status=400)
            else:
                return JsonResponse({'status': "error", 'message': "Vehicle Already Entered !!!"}, status=400)

        else:
            return JsonResponse({'status': "error", 'message': "Invalid Pass !!!"}, status=400)


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
                SaveParkingLotBill.objects.filter(id = bill_id).delete()
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
        
        result = SaveParkingLotBill.objects.filter(id = bill_id).delete()
        
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

        result = SaveParkingLotBill.objects.filter(m_business_id = m_business_id, bill_flag = True).order_by('-id')

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
                    'amount' : bill.amount,
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
                    return JsonResponse({'status': "success", "data": new_data, "from_date":from_date,"to_date":to_date,"total_flag_bills":total_flag_bills }, status=200)
                else:
                    return JsonResponse({'status': "error"}, status=400)
        else:        
            if result:
                return JsonResponse({'status': "success", "data": data, "from_date":"", "to_date":"","total_flag_bills":total_flag_bills}, status=200)
            else:
                return JsonResponse({'status': "error"}, status=400)


class ManageVehicleType(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']
        vehicle_type = request.POST['vehicle_type']

        isVehicleTypeExists = MerchantParkingAddVehicle.objects.filter(m_business_id= m_business_id, vehicle_type = vehicle_type)

        if isVehicleTypeExists:
            return JsonResponse({'status': 'error', 'message': "Vehicle Type already exists !"}, status=400)

        else:

            result = MerchantParkingAddVehicle.objects.create(m_business_id= m_business_id, vehicle_type = vehicle_type)

            if result:
                return JsonResponse({'status': 'success', 'message': "Vehicle Type added successfully !!!"}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': "Failed to add Vehicle Type !!!"}, status=400)


class ManageVehicleTypeList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        result = MerchantParkingAddVehicle.objects.filter(m_business_id= m_business_id)

        serializer = ManageVehicleTypeListSerializer(result, many=True)

        if result:
            return JsonResponse(serializer.data, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)

class ManageVehicleTypeDelete(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        vehicle_id = request.POST['vehicle_id']
        
        result = MerchantParkingAddVehicle.objects.filter(id = vehicle_id).delete()
        
        if result:
            return JsonResponse({'status' : 'success'}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)

class ManageParkingSpace(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            space_id = request.POST['id']
        except:
            space_id = ""

        if space_id:
            m_business_id = request.POST['m_business_id']
            vehicle_type = request.POST['vehicle_type']
            spaces_count = request.POST['spaces_count']

            vehicle_type_arr = MerchantParkingAddVehicle.objects.filter(m_business_id= m_business_id, vehicle_type= vehicle_type)

            result = MerchantParkingLotSpace.objects.filter(id = space_id).update(vehicle_type = vehicle_type, vehicle_type_id = vehicle_type_arr[0].id, spaces_count = spaces_count)

            if result:
                return JsonResponse({'status': 'success', 'message': "Space updated Successfully !!!"}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': "Failed to update Space !!!"}, status=400)

        else:
            m_business_id = request.POST['m_business_id']
            vehicle_type = request.POST['vehicle_type']
            spaces_count = request.POST['spaces_count']

            isVehicleTypeExists = MerchantParkingLotSpace.objects.filter(m_business_id= m_business_id, vehicle_type = vehicle_type)

            if isVehicleTypeExists:
                return JsonResponse({'status': 'error', 'message': "Space already exists for this Vehicle Type !!!"}, status=400)

            else:

                vehicle_type_arr = MerchantParkingAddVehicle.objects.filter(m_business_id= m_business_id, vehicle_type= vehicle_type)

                result = MerchantParkingLotSpace.objects.create(m_business_id= m_business_id, vehicle_type = vehicle_type, vehicle_type_id = vehicle_type_arr[0].id, spaces_count = spaces_count)

                if result:
                    return JsonResponse({'status': 'success', 'message': "Space added Successfully !!!"}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': "Failed to add Space !!!"}, status=400)


class ManageParkingSpaceList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        try:
            space_data = MerchantParkingLotSpace.objects.filter(m_business_id= m_business_id)
        except:
            space_data = ""

        new_data = []

        for data_temp in space_data:

            space_avilable_count_temp = 0

            space_avilable_count = SaveParkingLotBill.objects.filter(m_business_id = m_business_id, vehicle_type = data_temp.vehicle_type, exit_check = False, manage_space = True).count()

            space_avilable_count_temp = int(data_temp.spaces_count) - int(space_avilable_count)

            new_data.append({
                'id': data_temp.id,
                'vehicle_type' : data_temp.vehicle_type,
                'spaces_count' : data_temp.spaces_count,
                'available_parking_space' : space_avilable_count_temp
                })

        if space_data:
            return JsonResponse({'status': 'success', 'data': new_data}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)

class ManageCharges(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            charges_id = request.POST['id']
        except:
            charges_id = ""

        if charges_id:
            m_business_id = request.POST['m_business_id']
            user_id = request.POST['user_id']
            vehicle_type = request.POST['vehicle_type']

            for_hours = request.POST['for_hours']
            charges = request.POST['charges']

            for_additional_hours = request.POST['for_additional_hours']
            additional_hours_charges = request.POST['additional_hours_charges']

            charges_by = "One Time"
            merchant_users_object = Merchant_users.objects.get(user_id = user_id)
            merchant_general_setting = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

            vehicle_type_arr = MerchantParkingAddVehicle.objects.filter(user_id = merchant_users_object.merchant_user_id,m_business_id= merchant_general_setting.id, vehicle_type= vehicle_type)

            result = MerchantParkingSpaceCharges.objects.filter(id = charges_id).update(vehicle_type_id= vehicle_type_arr[0].id, vehicle_type= vehicle_type, charges_by= charges_by, charges=charges, additional_hours_charges = additional_hours_charges, for_hours = for_hours, for_additional_hours = for_additional_hours)


            if result:
                return JsonResponse({'status': 'success', 'message': "Charges updated Successfully !!!"}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': "Failed to update Charges !!!"}, status=400)

        else:
            m_business_id = request.POST['m_business_id']
            user_id = request.POST['user_id']
            vehicle_type = request.POST['vehicle_type']

            for_hours = request.POST['for_hours']
            charges = request.POST['charges']

            for_additional_hours = request.POST['for_additional_hours']
            additional_hours_charges = request.POST['additional_hours_charges']

            charges_by = "One Time"
            merchant_users_object = Merchant_users.objects.get(user_id = user_id)

            vehicle_exists = MerchantParkingSpaceCharges.objects.filter(user_id = merchant_users_object.merchant_user_id.id,m_business_id= m_business_id, vehicle_type = vehicle_type)

            if vehicle_exists:
                return JsonResponse({'status': 'error', 'message': "Vehicle already Exists, Please change vehicle type !!!"}, status=400)
            else:
                vehicle_type_arr = MerchantParkingAddVehicle.objects.filter(user_id = merchant_users_object.merchant_user_id.id,m_business_id= m_business_id, vehicle_type= vehicle_type).first()
                print('vehicle_type_arr',vehicle_type_arr)
                result = MerchantParkingSpaceCharges.objects.create(user = merchant_users_object.merchant_user_id,m_business_id= m_business_id, vehicle_type_id= vehicle_type_arr.id, vehicle_type= vehicle_type, charges_by= charges_by, charges=charges, additional_hours_charges = additional_hours_charges, for_hours = for_hours, for_additional_hours = for_additional_hours)

                if result:
                    return JsonResponse({'status': 'success', 'message': "Charges added Successfully !!!"}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': "Failed to add Charges !!!"}, status=400)


class ManageChargesList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        result = MerchantParkingSpaceCharges.objects.filter(m_business_id = m_business_id)

        serializer = ManageChargesListSerializer(result, many=True)

        if result:
            return JsonResponse({'status' : 'success', 'data' : serializer.data}, status=200)
        else:
            return JsonResponse({'status' : "error"}, status=400)


class passPaymentList(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']
        m_user_id = request.POST['m_user_id']
        m_business_id = request.POST['m_business_id']

        result = ParkingLotPass.objects.filter(user_id = user_id, m_business_id= m_business_id, created_at__date = timezone.now()).order_by('-id')
        
        data = []

        total_amount = 0
        total_count = 0

        for parking_pass in result:

            data.append({
                "id": parking_pass.id,
                "user_id": parking_pass.user_id,
                "m_business_id": parking_pass.m_business_id,
                "m_user_id": parking_pass.m_user_id,
                "mobile_no" : parking_pass.mobile_no,
                "amount" : parking_pass.amount,
                "valid_from" : datetime.strptime(str(parking_pass.valid_from), '%Y-%m-%d').strftime('%d-%m-%Y'),
                "valid_to" : datetime.strptime(str(parking_pass.valid_to), '%Y-%m-%d').strftime('%d-%m-%Y'),
                "comments" : parking_pass.comments,
                "vehical_no" : parking_pass.vehical_no,
                "created_at" : parking_pass.created_at,
                "pass_type": parking_pass.pass_type,
                "company_id": parking_pass.company_id,
                "company_name": parking_pass.company_name,
                "vehicle_type": parking_pass.vehicle_type
            });

            total_amount = total_amount + float(parking_pass.amount)
            total_count = total_count + 1

        if result:
            return JsonResponse({'status': "success", 'data':data, 'total_amount': total_amount, 'total_pass': total_count}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "No Data Found !!!"}, status=400)


class ParkingBillLayoutSettings(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        m_business_id = request.POST['m_business_id']

        try:
            merchant_bussiness_object = MerchantProfile.objects.get(id = m_business_id)
            setting = parking_app_setting_model.objects.filter(merchant_bussiness = merchant_bussiness_object)
            header_text1 = setting[0].header_text1
            header_text2 = setting[0].header_text2
            header_text3 = setting[0].header_text3
            footer_text1 = setting[0].footer_text1
            footer_text2 = setting[0].footer_text2
            footer_text3 = setting[0].footer_text3
            digital_bill = setting[0].digital_bill
            sms = setting[0].sms
            exit_gate = setting[0].exit_gate
            manage_space = setting[0].manage_space

        except:
            header_text1 = ""
            header_text2 = ""
            header_text3 = ""
            footer_text1 = ""
            footer_text2 = ""
            footer_text3 = ""
            digital_bill = True
            sms = False
            exit_gate = False
            manage_space = setting[0].manage_space

        if m_business_id:
            return JsonResponse({'status':"success", 'header_text1': header_text1, 'header_text2':header_text2, 'header_text3':header_text3, 'footer_text1':footer_text1, 'footer_text2':footer_text2, 'footer_text3':footer_text3, 'digital_bill':digital_bill, 'sms':sms, 'bill_gate':exit_gate, 'manage_space':manage_space}, status=200, safe = False)
        else:
            return JsonResponse({'status' : "error"}, status=400)


def reject_parking_bill(request):

    if request.method == "POST":

        bill_id = request.POST['bill_id']

        bill_object = SaveParkingLotBill.objects.get(id=bill_id)

        bill_url = bill_object.bill_url

        rejectbillRadio = request.POST['rejectbillRadio']

        if rejectbillRadio == "1":
            reject_reason = "This is not my bill"

        elif rejectbillRadio == "2":
            reject_reason = "There are mistakes in the bill"

        result = SaveParkingLotBill.objects.filter(id=bill_id).update(reject_status = True, reject_reason = reject_reason)

        try:

            bill_data = SaveParkingLotBill.objects.get(id = bill_id)

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
            return redirect(parkingLotBill, id = bill_url)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Reject.', timer=1500)
            return redirect(parkingLotBill, id = bill_url)
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
