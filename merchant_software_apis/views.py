import random
import os
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
from users.models import GreenBillUser, UserProfileImage, MerchantProfile, Merchant_users
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from django.utils import formats
from authentication.models import otp_validation
from django.conf import settings
from django.core.mail import send_mail
from category_and_tags.models import business_category
import base64
from django.core.files.base import ContentFile
from .models import *
import socket
from pyfcm import FCMNotification
from green_points.models import GreenPointsModel
import random
import string

# SMS
import requests
import time
import pyshorteners

import sweetify

from customer_bill.views import my_bill

from super_admin_settings.models import GreenPointsSettings

from django.db.models import Q

from my_subscription.models import *

from promotions.models import *

from bill_design.models import *

from users.models import *
import json
from datetime import datetime
from datetime import date

from bill_feedback.models import bill_feedback_question

from decimal import Decimal
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from merchant_setting.models import MerchantPaymentSetting
import random
import hashlib

from merchant_stamp.models import merchantusagestamp
from merchant_role.models import merchant_userrole

from owner_stamp.models import *
import pytesseract
import pytesseract  as ts

import PIL 
from PIL import Image
import csv
import sys
import numpy as np
from django.contrib.staticfiles import finders
from django.templatetags.static import static
import re
from partner_my_subscription.models import *
from word2number import w2n
import json


@csrf_exempt
def FetchAmountFromImage(request):
    total_amount = 0
    try:
        if request.method == "POST":
            bill = request.FILES['bill']
           
        value = Image.open(bill)
        
        text = pytesseract.image_to_string(value)
        # print(text)
        # print(type(tex))

        txt = text.split("\n")
        # print(txt)

        string1  = "TOTAL"
        string2  = "Total"
        string3  = "AMOUNT"
        string4  = "Amount"
        string5  = "Payable Amount"
        string6  = "Net Amount"
        string7  = "Total Payable Value"
        string8  = "Invoice Total"
        string9  = "Grand Total"
        string10 = "Total Amount"
        string11 = "PAYABLE AMOUNT"
        string12 = "Pes"
        string13 = "pes"
        string14 = "NET AMOUNT"
        string15 = "NET AMT"
        string16 = "GROSS AMOUNT"
        string17 = "JOCKEY"
        total_amount = ""
        print(txt)
        # print("**************************************************")
        # print(txt.split("Rs"))
        print()
        if txt[0]=="JOCKEY PREFERRED STORE":
            # print("in jockey store")
            var = ""
            # for i in txt:
            #     print(i)
            #     if "Rs:" in i or "Rs :" in i:
            #         print(i)
            #         var = i
            #         break
            print("Printing")
            for k in txt :
         
                if "NET AMOUNT" in k:
                    print(k)
                    print(type(k))
                    # print(list(k))
                    f = k.split(' ')
                    # print(f)
                    total_amount = (f[len(f)-1])
                    print(type(total_amount))
                    print(list(total_amount))
                    d = total_amount.replace(',',"")
                    print(d)
                    r = float(d)
                    e = float("{:.2f}".format(r))
                    # print(type(r))
                    total_amount = d
                    print(total_amount)
                    print(type(total_amount))
                    break
                
            
           
        else:
            print("in else ")
            for v1 in txt:
                temp2 = re.findall(r'\d+\.\d+', v1)
                if temp2:
                    print('******')
                    if v1.find(string17) != -1:
                        total_amount = "1"
                        print(total_amount)
                    elif v1.find(string10) != -1:
                        total_amount = ""
                        bill_data = re.findall(r'.\d+', v1)

                        for i in bill_data:
                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23

                    elif v1.find(string13) != -1:
                        total_amount = ""
                        bill_data = re.findall(r'.\d+', v1)
                        
                        for i in bill_data:
                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23

                    elif v1.find(string12) != -1:
                        total_amount = ""
                        bill_data = re.findall(r'.\d+', v1)
                        
                        for i in bill_data:
                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23

                    elif v1.find(string10) != -1:
                        total_amount = ""
                        bill_data = re.findall(r'.\d+', v1)
                        
                        for i in bill_data:
                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23

                    elif v1.find(string5) != -1:
                        total_amount = ""
                        bill_data = re.findall(r'.\d+', v1)
                        
                        for i in bill_data:
                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23

                    elif v1.find(string6) != -1:
                        total_amount = ""
                        bill_data = re.findall(r'.\d+', v1)
                        
                        for i in bill_data:
                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23

                    elif v1.find(string7) != -1:
                        total_amount = ""
                        bill_data = re.findall(r'.\d+', v1)
                        
                        for i in bill_data:
                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23

                    elif v1.find(string8) != -1:
                        total_amount = ""
                        bill_data = re.findall(r'.\d+', v1)
                        
                        for i in bill_data:
                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23

                    elif v1.find(string9) != -1:
                        total_amount = ""
                        bill_data = re.findall(r'.\d+', v1)
                        
                        for i in bill_data:
                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23


                    elif v1.find(string1) != -1:

                        total_amount = ""
                        bill_data = re.findall(r'.\d+', v1)
                        
                        for i in bill_data:
                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23

                    elif v1.find(string2) != -1:
                        total_amount = ""
                        bill_data = re.findall(r'.\d+', v1)
                        # print(bill_data)
                        for i in bill_data:

                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            

                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23

                    elif v1.find(string3) != -1:
                        total_amount = ""
                        bill_data = re.findall(r'.\d+', v1)
                        
                        for i in bill_data:
                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23

                    elif v1.find(string4) != -1:
                        total_amount = ""
                        print("***")
                        print(total_amount)
                        bill_data = re.findall(r'.\d+', v1)
                        
                        for i in bill_data:
                            res = bool(re.search(r"\s", i))
                            if res == True:
                                if total_amount:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = int(str(total_amount) + str(new_amt1))
                                else:
                                    new_amt1 = i.replace(" ", "")
                                    total_amount = new_amt1
                            elif "," in i[0:4]:
                                if total_amount:
                                    new_amt = i.replace(',', '')
                                    total_amount = int(str(total_amount) + str(new_amt))
                                else:
                                    new_amt = i.replace(',', '')
                                    total_amount = new_amt
                                
                            elif "." in i[0:4]:
                                total_amount = str(total_amount) + str(i)

                            else:
                                if total_amount:
                                    new_amt2 = [int(i) for i in i.split() if i.isdigit()]

                                    total_amount = int(str(total_amount) + str(new_amt2))
                                else:
                                    new_amt2 = re.findall(r'\d+', i)
                                    for amt23 in new_amt2:
                                        total_amount = amt23
                            

        
        print("PPPPPPPPPPPPPPPP")
        print(total_amount)
        print(type(total_amount))
        if bill:
            return JsonResponse({"data":total_amount})
            


    except:

        return JsonResponse({"data":total_amount})


@csrf_exempt
def FetchInvoiceNumberFromImage(request):
    invoice_no = 0
    try:
        if request.method == "POST":
            bill = request.FILES['bill']


           
        value = Image.open(bill)
        
        text = pytesseract.image_to_string(value)
                
        string1 = "INVOICE"
        string2 = "invoice"
        string3 = "Invoice"
        string4 = "Bill N"
        string5 = "BILL N"

        invoice_no = 0

        txt = text.split("\n")

        print(txt)
        
        for v1 in txt:
            if v1.find(string1) != -1:
                resultStringOne = [int(i) for i in v1.split() if i.isdigit()]
                for invoice in resultStringOne:
                    invoice_no = invoice

            elif v1.find(string2) != -1:
                resultStringOne = [int(i) for i in v1.split() if i.isdigit()]
                for invoice in resultStringOne:
                    invoice_no = invoice

            elif v1.find(string3) != -1:
                resultStringOne = [int(i) for i in v1.split() if i.isdigit()]
                for invoice in resultStringOne:
                    invoice_no = invoice

            elif v1.find(string4) != -1:
                bill = [int(i) for i in v1.split() if i.isdigit()]
                for num in bill:
                    invoice_no = num

            elif v1.find(string5) != -1:
                bill = [int(i) for i in v1.split() if i.isdigit()]
                for num in bill:
                    invoice_no = num
        
        return JsonResponse({"data":invoice_no})
    except:
        return JsonResponse({"data":invoice_no})


@csrf_exempt
def storeDeviceId(request):
    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        device_id = request.POST['device_id']
        user_type = request.POST['user_type']

        result = DeviceId.objects.update_or_create(mobile_no=mobile_no, defaults={
            'mobile_no': mobile_no, 'device_id': device_id, 'user_type': user_type
        })

        if result:
            return JsonResponse({'status': "success", "message": "device id stored or updated successfully!!!"}, status=200)
        else:
            return JsonResponse({'status': "error", "message": "failed to store or update device id !!!"}, status=400)

    else:
        return JsonResponse({'status': "error", "message": "Something went wrong !!!"}, status=400)

@csrf_exempt
def destroyDeviceId(request):
    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        user_type = request.POST['user_type']

        result = DeviceId.objects.filter(mobile_no=mobile_no, user_type=user_type).delete()
        
        if result:
            return JsonResponse({'status': "success", "message": "device id deleted successfully!!!"}, status=200)
        else:
            return JsonResponse({'status': "error", "message": "failed to delete device id !!!"}, status=400)

    else:
        return JsonResponse({'status': "error", "message": "Something went wrong !!!"}, status=400)

@csrf_exempt
def exe_print_record_maintain(request):
    if request.method == "POST":
        business_id = request.POST.get('m_business_id')

        ExePrintStatus.objects.create(business_id = business_id)

        return JsonResponse({'status': 'success'}, status=200)

@csrf_exempt
def send_bill(request):
    if request.method == "POST":
        checkoutpin = request.POST.get('checkoutpin')
        mobile_no = request.POST.get('mobile_no')
        invoice_num = request.POST.get('invoice_num')

        if invoice_num == '0':
            invoice_num = ""

        try:
            send_bill_to = request.POST['send_bill_to']
        except:
            send_bill_to = ""

        if not mobile_no:
            try:
                mobile_no = GreenBillUser.objects.get(c_unique_id = checkoutpin).mobile_no
                send_bill_to = "is_customer"
            except:
                mobile_no = ""

            if not mobile_no:
                return JsonResponse({'status' : 'error'}, status=200)

        bill = request.FILES['bill']
        email = request.POST['email']
        bill_amount = request.POST.get('bill_amount')
        send_bill_type = request.POST.get('send_bill_type')

        if not bill_amount:
            bill_amount = 0

        stamp_id = request.POST.get('stamp_selected_id')

        try:
            business_id = request.POST['business_id']
        except:
            business_id = ""

        customer_bill_url = ""

        m_business_id = request.POST['m_business_id']

        user_id = request.POST['user_id']

        transaction_type = request.POST['transaction_type']

        if transaction_type == "green_bill_transaction":
            green_bill_transaction = True
            green_bill_print_transaction = False
            print_transaction = False
        elif transaction_type == "green_bill_print_transaction":
            green_bill_print_transaction = True
            green_bill_transaction = False
            print_transaction = False
        elif transaction_type == "print_transaction":
            print_transaction = True
            green_bill_transaction = False
            green_bill_print_transaction = False

        if (request.POST['mobile_no'] and request.POST['check_sms'] == '1') or (request.POST['email'] and request.POST['check_email'] == '1' or request.POST.get('checkoutpin')):


            try:
                m_business_id = request.POST['m_business_id']
                merchant_business_object = MerchantProfile.objects.get(id = m_business_id)
            except:
                merchant_business_object = ""

            business_category_name = merchant_business_object.m_business_category.business_category_name

            print(merchant_business_object.m_business_category.business_category_name)

            bill_category_id = bill_category.objects.filter(bill_category_name__contains = business_category_name).values('id')[0]['id']
            
            if bill_category_id:
                bill_category_object = bill_category.objects.get(id = bill_category_id)
            else:
                bill_category_object = ""

            green_points_settings_object = GreenPointsSettings.objects.get(id = 1)
            green_points = green_points_settings_object.bill_points

            if send_bill_to == "is_customer":

                year = timezone.now().year

                try:
                    invoice = InvoiceNumberSoftwareBill.objects.filter(m_business_id= m_business_id).last()
                except:
                    invoice = ""
                if invoice_num:
                    invoice_no = invoice_num
                else:
                    if not invoice:
                        invoice_no = str(year) + str("/") + str("01").zfill(5)
                    else:
                        last_invoice = invoice.invoice_no
                        split_list = last_invoice.split("/")
                        last_no = split_list[1]
                        no = int(last_no) + 1
                        invoice_no = str(year) + str("/") + str(no).zfill(5)
                    InvoiceNumberSoftwareBill.objects.create(invoice_no= invoice_no,user_id=user_id,m_business_id= m_business_id)

                customer_bill = CustomerBill.objects.create(user_id = user_id, mobile_no = mobile_no,
                    email = email, bill = bill, green_points_earned = str(green_points), business_name = merchant_business_object,
                    invoice_no = invoice_no, green_bill_transaction = green_bill_transaction, green_bill_print_transaction = green_bill_print_transaction,
                    print_transaction = print_transaction, bill_amount = bill_amount, customer_bill_category = bill_category_object,stamp_id=stamp_id, exe_bill_type = send_bill_type
                )
                try:
                    if request.POST.get('checkoutpin'):
                        CustomerBill.objects.filter(id = customer_bill.id).update(is_checkoutpin = True)
                except:
                    pass

                history_result1 = sent_bill_history.objects.create(user_id = user_id,
                            mobile_no = mobile_no, m_business_id = merchant_business_object.id, green_bill_transaction = green_bill_transaction,
                            green_bill_print_transaction = green_bill_print_transaction, print_transaction = print_transaction, bill_amount = bill_amount,
                            customer_bill = True, is_exe = True
                        )

                if customer_bill:
                    subscription_object = getActiveSubscriptionPlanSoftware(request, merchant_business_object.id)
                    if subscription_object:
                        history_result = sent_bill_history.objects.create(subscription_id = subscription_object.id, user_id = user_id,
                            mobile_no = mobile_no, m_business_id = merchant_business_object.id, green_bill_transaction = green_bill_transaction,
                            green_bill_print_transaction = green_bill_print_transaction, print_transaction = print_transaction, bill_amount = bill_amount,
                            customer_bill = True, is_exe = True
                        )
                        if not invoice_num:
                            invoice_result = InvoiceNumberSoftwareBill.objects.create(user_id = user_id, m_business_id= m_business_id, invoice_no = invoice_no)

            elif send_bill_to == "is_merchant":
                business_name = MerchantProfile.objects.get(id = business_id)

                year = timezone.now().year

                try:
                    invoice = InvoiceNumberSoftwareBill.objects.filter(m_business_id= m_business_id).last()
                except:
                    invoice = ""

                if invoice_num:
                    invoice_no = invoice_num
                else:

                    if not invoice:
                        invoice_no = str(year) + str("/") + str("01").zfill(5)
                    else:
                        last_invoice = invoice.invoice_no
                        split_list = last_invoice.split("/")
                        last_no = split_list[1]
                        no = int(last_no) + 1
                        invoice_no = str(year) + str("/") + str(no).zfill(5)
                    InvoiceNumberSoftwareBill.objects.create(invoice_no= invoice_no,user_id=user_id,m_business_id= m_business_id)


                customer_bill = MerchantBill.objects.create(user_id = user_id, mobile_no = mobile_no, email = email,
                    bill = bill, business_name = merchant_business_object, bill_received_business_name = business_name.id,
                    invoice_no = invoice_no, green_bill_transaction = green_bill_transaction, green_bill_print_transaction = green_bill_print_transaction,
                    print_transaction = print_transaction, bill_amount = bill_amount, customer_bill_category = bill_category_object,stamp_id=stamp_id, exe_bill_type = send_bill_type
                )
                try:
                    if request.POST.get('checkoutpin'):
                        MerchantBill.objects.filter(id = customer_bill.id).update(is_checkoutpin = True)
                except:
                    pass

                if customer_bill:
                    subscription_object = getActiveSubscriptionPlanSoftware(request, merchant_business_object.id)

                    history_result = sent_bill_history.objects.create(subscription_id = subscription_object.id, user_id = user_id,
                        mobile_no = mobile_no, m_business_id = merchant_business_object.id, green_bill_transaction = green_bill_transaction,
                        green_bill_print_transaction = green_bill_print_transaction, print_transaction = print_transaction, bill_amount = bill_amount,
                        merchant_bill = True,is_exe = True
                    )

                    if not invoice_num:

                        invoice_result = InvoiceNumberSoftwareBill.objects.create(user_id = user_id, m_business_id= m_business_id, invoice_no = invoice_no)

            letters = string.ascii_letters
            digit = string.digits
            random_string = str(customer_bill.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
            
            if customer_bill and send_bill_to == "is_customer":
               customer_bill_new = CustomerBill.objects.filter(id=customer_bill.id).update(bill_url = random_string)

            elif customer_bill and send_bill_to == "is_merchant":
               customer_bill_new = MerchantBill.objects.filter(id=customer_bill.id).update(bill_url = random_string) 

            try: 
                # green_points_old = GreenPointsModel.objects.filter(mobile_no=mobile_no).values('green_points_count')[0]['green_points_count']
                green_points_old = GreenPointsModel.objects.filter(mobile_no=mobile_no).values('green_points_count')[0]['green_points_count']
                
            except:
                green_points_old = 0

            green_points_new = int(green_points_old) + int(green_points)

            try:
                if send_bill_to == "is_customer":
                    # GreenPointsModel.objects.update_or_create(mobile_no=mobile_no, defaults={
                    #     'green_points_count': green_points_new})
                    GreenPointsModel.objects.update_or_create(mobile_no=mobile_no, defaults={
                    'green_points_count': green_points_new})

            except:
                print("except")

            try:
                if send_bill_to == "is_customer":

                    if GreenPointsModel.objects.filter(mobile_no = mobile_no):

                        device = DeviceId.objects.filter(mobile_no=mobile_no, user_type='customer').first()

                        if device: 
                        
                            push_service = FCMNotification(api_key=settings.API_KEY)

                            registration_id = device.device_id

                            message_title = "Green Point"

                            message_body = "Yay! You have earned <Number> Green Points. " + str(merchant_business_object.m_business_name)     

                            results1 = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)    
            except:
                pass       

            if send_bill_to == "is_customer":
                bill_url = CustomerBill.objects.filter(id=customer_bill.id).values('bill_url')[0]['bill_url']
                customer_bill_url = "http://157.230.228.250/my-bill/" + str(bill_url) + "/"

            elif send_bill_to == "is_merchant":
                bill_url = MerchantBill.objects.filter(id=customer_bill.id).values('bill_url')[0]['bill_url']
                customer_bill_url = "http://157.230.228.250/my-bill-merchant/" + str(bill_url) + "/"

        if send_bill_to == "is_customer":
            device = DeviceId.objects.filter(mobile_no=mobile_no, user_type='customer').first()

        elif send_bill_to == "is_merchant":
            device = DeviceId.objects.filter(mobile_no=mobile_no, user_type='merchant').first()

        push_service = FCMNotification(api_key=settings.API_KEY)
        result = ''

        if device:
            registration_id = device.device_id
        else:
            registration_id = ""

        message_title = "Receiving New Bill"

        message_body = "You have received a digital bill from . " + str(merchant_business_object.m_business_name) + str(customer_bill_url)

        subscription_object = getActiveSubscriptionPlanSoftware(request, merchant_business_object.id)

        total_amount_avilable = float(subscription_object.total_amount_avilable)
        per_digital_bill_cost = float(subscription_object.per_digital_bill_cost)
        per_bill_cost = float(subscription_object.per_bill_cost)

        if total_amount_avilable >= per_digital_bill_cost:
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        else:
            result['failure'] == 1
        
        if result['failure'] != 1 and request.POST['mobile_no']:
            if send_bill_to == "is_customer":
                CustomerBill.objects.filter(id=customer_bill.id).update(greenbill_digital_bill = True)
            elif send_bill_to == "is_merchant":
                MerchantBill.objects.filter(id=customer_bill.id).update(greenbill_digital_bill = True)
            total_amount_avilable_new = total_amount_avilable - per_digital_bill_cost
            subscription_object.total_amount_avilable = total_amount_avilable_new
            subscription_object.save()

            history_result.digital_bill = True
            history_result.bill_cost = str(per_digital_bill_cost)
            history_result.save()

            return JsonResponse({'status':'success_notify', 'result': result}, status=200)
        
        else:

            if ((request.POST['mobile_no'] and request.POST['check_sms'] == '1') or (request.POST.get('checkoutpin'))):

                # customer_bill = CustomerBill.objects.create(mobile_no = mobile_no, bill = bill)

                if send_bill_to == "is_customer":
                    CustomerBill.objects.filter(id=customer_bill.id).update(greenbill_sms_bill = True)
                elif send_bill_to == "is_merchant":
                    MerchantBill.objects.filter(id=customer_bill.id).update(greenbill_sms_bill = True)

                s = pyshorteners.Shortener()
                short_url = s.tinyurl.short(customer_bill_url)

                ts = int(time.time())
                my_bill_url = short_url

                
                if int(merchant_business_object.id) == 1188:
                    
                    data_temp = {
                            "keyword":"Babu Moshay Bill",
                            "timeStamp":ts,
                            "dataSet":
                                [
                                    {
                                        "UNIQUE_ID":"GB-" + str(ts),
                                        "MESSAGE": "Thanks for ordering with Babu Moshay 8408888707. To view your bill click " + short_url + ". To manage all your bills at one place download GreenBill App.",
                                        "OA":"GBBILL",
                                        "MSISDN": str(mobile_no), # Recipient's Mobile Number
                                        "CHANNEL":"SMS",
                                        "CAMPAIGN_NAME":"hind_user",
                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                        "USER_NAME":"hind_hsi",
                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                        "DLT_CT_ID":"1007163671333233008", # Template Id
                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                    }
                                ]
                            }
                # elif int(merchant_business_object.id) == 1285:
                    
                #     data_temp = {
                #             "keyword":"Shri Eye Care Netralay and Optical Bill",
                #             "timeStamp":ts,
                #             "dataSet":
                #                 [
                #                     {
                #                         "UNIQUE_ID":"GB-" + str(ts),
                #                         "MESSAGE": "Thanks for ordering with Shri Eye Care Netralay and Optical. To view your bill click " + short_url + ". To manage all your bills at one place download GreenBill App.",
                #                         "OA":"GBBILL",
                #                         "MSISDN": str(mobile_no), # Recipient's Mobile Number
                #                         "CHANNEL":"SMS",
                #                         "CAMPAIGN_NAME":"hind_user",
                #                         "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                #                         "USER_NAME":"hind_hsi",
                #                         "DLT_TM_ID":"1001096933494158", # TM ID
                #                         "DLT_CT_ID":"1007163671333233008", # Template Id
                #                         "DLT_PE_ID":"1001659120000037015" # PE ID 
                #                     }
                #                 ]
                #             }
                else:
                    data_temp = {
                            "keyword":"Bill Delivery SMS",
                            "timeStamp":ts,
                            "dataSet":
                                [
                                    {
                                        "UNIQUE_ID":"GB-" + str(ts),
                                        "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
                                        "OA":"GBBILL",
                                        "MSISDN": str(mobile_no), # Recipient's Mobile Number
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
                
                if total_amount_avilable >= per_bill_cost:
                    response = requests.post(url, json = data_temp)
                    total_amount_avilable_new = total_amount_avilable - per_bill_cost
                    subscription_object.total_amount_avilable = total_amount_avilable_new
                    subscription_object.save()

                    history_result.sms_bill = True
                    history_result.bill_cost = str(per_bill_cost)
                    history_result.save()

                else:
                    return JsonResponse({'status' : 'error'}, status=200)


            if request.POST['email'] and request.POST['check_email'] == '1':

                subject = 'Bill Receipt'
                message = f'Hey Green Bill user, view and download your bill here. {customer_bill_url}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email,] 
                send_mail_res = send_mail( subject, message, email_from, recipient_list)

            if request.POST['check_email'] == '1' and request.POST['check_sms'] == '1':
                if response.status_code == 200 and send_mail_res:
                    return JsonResponse({'status':'success'}, status=200)

            elif request.POST['check_sms'] == '1':
                if response.status_code == 200:
                    return JsonResponse({'status':'success_sms'}, status=200)

            elif request.POST['check_email'] == '1':
                if send_mail_res:
                    return JsonResponse({'status':'success_email'}, status=200)
            else:
                return JsonResponse({'status' : 'error'}, status=200)
    else:
        return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)

@csrf_exempt
def send_bill_sms(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        bill = request.FILES['bill']

        
        if mobile_no:

            customer_bill_url = "http://157.230.228.250" + str(customer_bill.bill.url)

            import urllib
            username = "sanjog1"
            Password = "123456"
            sender = "HINDAG"
            temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + "To view all your bills, download Green bill App."
            temp_dict = {"text": temp_message}
            message= urllib.parse.urlencode(temp_dict)
            priority='ndnd'
            stype='normal'

            var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

            import requests

            url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

            res = requests.get(url)

            if res.status_code == 200:
                return JsonResponse({'status':'success', 'mobile_no' : mobile_no, 'message': 'SMS sent successfully'}, status=200)
            else:
                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

            # subject = 'Bill Receipt'
            # message = f'Please find bill: {otp}'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [email,] 
            # send_mail( subject, message, email_from, recipient_list)

            return JsonResponse({'status':'success',  'message': 'SMS sent successfully'}, status=200)
        else:
                return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
    else:
        return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)

@csrf_exempt
def send_bill_email(request):
    if request.method == "POST":
        email = request.POST['email']
        bill = request.FILES['bill']

        if email:

            customer_bill = CustomerBill.objects.create(email = email, bill = bill)

            customer_bill_url = "http://157.230.228.250" + str(customer_bill.bill.url)

            subject = 'Bill Receipt'
            message = f'Hey Green Bill user, view and download your bill here. {customer_bill_url}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,] 
            send_mail( subject, message, email_from, recipient_list)

            return JsonResponse({'status':'success',  'message': 'Email send successfully'}, status=200)
        else:
                return JsonResponse({'status':'error',  'message': "Failed to send Email"}, status=400)
    else:
        return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)

@csrf_exempt
def send_bill_sms_and_email(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        email = request.POST['email']
        bill = request.FILES['bill']

        if mobile_no and email:

            customer_bill = CustomerBill.objects.create(email = email, bill = bill)

            customer_bill_url = "http://157.230.228.250" + str(customer_bill.bill.url)

            # SMS
            import urllib
            username = "sanjog1"
            Password = "123456"
            sender = "HINDAG"
            temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + "To view all your bills, download Green bill App."
            temp_dict = {"text": temp_message}
            message= urllib.parse.urlencode(temp_dict)
            priority='ndnd'
            stype='normal'
            var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""
            import requests
            url = "http://trans.smsfresh.co/api/sendmsg.php?" + var
            res = requests.get(url)

            # Email
            subject = 'Bill Receipt'
            message = f'Hey Green Bill user, view and download your bill here. {customer_bill_url}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,] 
            send_mail( subject, message, email_from, recipient_list)

            return JsonResponse({'status':'success',  'message': 'SMS and Email send successfully'}, status=200)
        else:
            return JsonResponse({'status':'error',  'message': "Failed to send SMS and Email. Please send valid Mobile number and Email"}, status = 400)
    else:
        return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)
        

@csrf_exempt
def send_bill_website(request):

    if request.method == "POST":
        mobile_no = request.POST['mobile_no']

        print('mobile_no',mobile_no)
        # print(mobile_no.replace('+91', ''))
        mobile_no_new = mobile_no.replace('+91', '')

        ts = int(time.time())

        data_temp = {
                "keyword":"Send Sample Bill",
                "timeStamp":ts,
                "dataSet":
                    [
                        {
                            "UNIQUE_ID":"GB-" + str(ts),
                            "MESSAGE":"Thank you for contacting Green Bill, tap the below link for your digital bill https://bit.ly/3fwlvqt",
                            "OA":"GBBILL",
                            "MSISDN": str(mobile_no_new), # Recipient's Mobile Number
                            "CHANNEL":"SMS",
                            "CAMPAIGN_NAME":"hind_user",
                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                            "USER_NAME":"hind_hsi",
                            "DLT_TM_ID":"1001096933494158", # TM ID
                            "DLT_CT_ID":"1007162098307281560", # Template Id
                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                        }
                    ]
                }

        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

        response = requests.post(url, json = data_temp)

        if response.status_code == 200:
            return JsonResponse({'status':'success'}, status=200)
        else:
            return JsonResponse({'status':'error'}, status=400)

    else:
        return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)

def website_demo_bill(request):
    context = {}
    return render(request, "super_admin/website-demo-bill.html", context)

@csrf_exempt
def get_is_merchant_or_customer(request):

    if request.method == "POST":

        mobile_no = request.POST['mobile_no']

        # try:
        user_details = GreenBillUser.objects.get(mobile_no = mobile_no)

        data = {
            'is_customer' : user_details.is_customer,
            'is_merchant' : user_details.is_merchant,
            'is_merchant_staff' : user_details.is_merchant_staff
        }

        return JsonResponse({'status':'success', 'data': data}, status=200)

        # except:
        #     return JsonResponse({'status':'error', 'message': "User not available !!!"}, status=400)

    else:
        return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)

@csrf_exempt
def get_merchant_business(request):

    if request.method == "POST":

        mobile_no = request.POST['mobile_no']

        try:
            user_object = GreenBillUser.objects.get(mobile_no = mobile_no)
            merchant_profile = Merchant_users.objects.get(user_id = user_object)
            merchant_object = GreenBillUser.objects.get(mobile_no = merchant_profile.merchant_user_id)

            merchant_business = MerchantProfile.objects.filter(m_user = merchant_object)

            data = []

            for business in merchant_business:

                if business.m_area:
                    merchant_bussiness_name = business.m_business_name + " (" + business.m_area + ")"
                else:
                    merchant_bussiness_name = business.m_business_name

                data.append({
                        'business_id': business.id,
                        'business_name' : merchant_bussiness_name
                    })

            return JsonResponse({'status':'success', 'data': data}, status=200)

        except:
            return JsonResponse({'status':'error', 'message': "User not available !!!"}, status=400)

    else:
        return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)

def search_view_bill(request, id):
    pass
    # try:
    #     pass
    # except:
    #     return render(request, 'page-404.html')

def my_bill_merchant(request, id):

    try:

        bill_details = MerchantBill.objects.get(bill_url=id)

        Green_user_id = GreenBillUser.objects.get(mobile_no = bill_details.mobile_no)

        merchant_profile_id = MerchantProfile.objects.get(id = bill_details.business_name.id)

        try:
            selected_stamp_id = bill_details.stamp_id
            latest_stamp_record = wstampmodels.objects.filter(id=selected_stamp_id)
        except:
            latest_stamp_record = ''

        merchant_user_id = Merchant_users.objects.filter(user_id = bill_details.user_id).values('merchant_user_id')[0]['merchant_user_id']

        merchant_user_object = GreenBillUser.objects.get(id = merchant_user_id)

        try:
            merchant_business_object = MerchantProfile.objects.get(id = bill_details.business_name.id)
        except:
            merchant_business_object = ""

        try:
            bill_design = bill_designs.objects.get(merchant_business_id = merchant_business_object)
        except:
            bill_design = ""

        try:
            merchant_business_object = MerchantProfile.objects.get(id = bill_details.business_name.id)

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

        

        ads_id = ""
        ads_redirect_url = ""
        ads_image = ""
        ads_image_details = ""
        

        space = ads_below_bill.objects.filter(merchant = merchant_business_object.m_user, merchant_business_id = bill_details.business_name, ads_type='green_bill').last()

        today = datetime.strptime(str(date.today()), '%Y-%m-%d')

        green_bills_advertisement = ""
        
        try:
            if space:
                expiry_date_new = datetime.strptime(space.end_date, '%Y-%m-%d')
                start_date_new = datetime.strptime(space.start_date, '%Y-%m-%d')

                if today >= start_date_new and today <= expiry_date_new:

                    startswith = str(bill_details.business_name.id) + ','
                    endswith = ','+ str(bill_details.business_name.id)
                    contains = ','+ str(bill_details.business_name.id) + ','
                    exact = str(bill_details.business_name.id)

                    green_bill_merchant_ads = ads_for_green_bills.objects.filter(
                        Q(business_name_value__startswith = startswith) | 
                        Q(business_name_value__endswith = endswith) | 
                        Q(business_name_value__contains = contains) | 
                        Q(business_name_value__exact = exact)
                    ).last()

                    if green_bill_merchant_ads:

                        start_date = datetime.strptime(green_bill_merchant_ads.start_date, '%Y-%m-%d')
                        end_date = datetime.strptime(green_bill_merchant_ads.end_date, '%Y-%m-%d')

                        if today >= start_date and today <= end_date:
                            ads_image_details = ads_for_green_bills.objects.get(id = green_bill_merchant_ads.id)
                            green_bills_advertisement = True
                            views = ads_below_bill.objects.get(id=space.id)
                            views.count = views.count + 1
                            views.save()

            if not green_bills_advertisement:
                third_party_status = ads_below_bill.objects.filter(merchant = merchant_business_object.m_user, merchant_business_id = bill_details.business_name, ads_type='third_party', status = 1).last()
                if third_party_status:
                    expiry_date_new =  datetime.strptime(third_party_status.end_date, '%Y-%m-%d')
                    start_date_new =  datetime.strptime(third_party_status.start_date, '%Y-%m-%d')

                    if today <= expiry_date_new and today >= start_date_new:
                        ads_image_details = ads_below_bill.objects.get(id = third_party_status.id)
                        green_bills_advertisement = True
                        views = ads_below_bill.objects.get(id=third_party_status.id)
                        views.count = views.count + 1
                        views.save()

            if not green_bills_advertisement:
                ads_details = ads_below_bill.objects.filter(merchant = merchant_business_object.m_user, merchant_business_id = bill_details.business_name, active_ads = True).last()
                if ads_details:
                    ads_image_details = ads_below_bill.objects.get(id = ads_details.id)
                    green_bills_advertisement = True
                    views = ads_below_bill.objects.get(id=ads_details.id)
                    views.count = views.count + 1
                    views.save()
        except:
            ads_image_details = ""

        try:
            for_rating_1_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_object.id, for_rating = "1")
        except:
            for_rating_1_object = ""

        try:
            for_rating_2_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_object.id, for_rating = "2")
        except:
            for_rating_2_object = ""

        try:
            for_rating_3_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_object.id, for_rating = "3")
        except:
            for_rating_3_object = ""

        try:
            for_rating_4_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_object.id, for_rating = "4")
        except:
            for_rating_4_object = ""

        try:
            for_rating_5_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_object.id, for_rating = "5")
        except:
            for_rating_5_object = ""

        try:
            payment_settings = MerchantPaymentSetting.objects.get(m_business_id = bill_details.business_name.id)
        except:
            payment_settings = ""
        context = {}
        print('PaymentSetting', payment_settings)
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
                surl = "http://157.230.228.250/my-bill-merchant-payment-link-success/"
                furl = "http://157.230.228.250/my-bill-merchant-payment-link-fail/"

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
                amount = str(bill_details.bill_amount)

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
        context['ads_redirect_url'] = ads_redirect_url
        context['ads_image'] = ads_image
        context['business_logo'] = business_logo
        context['business_address'] = business_address
        context['bill_design'] = bill_design
        context['url_slug'] = id
        context['for_rating_1_object'] = for_rating_1_object
        context['for_rating_2_object'] = for_rating_2_object
        context['for_rating_3_object'] = for_rating_3_object
        context['for_rating_4_object'] = for_rating_4_object
        context['for_rating_5_object'] = for_rating_5_object
        # context['ads_id'] = ads_id
        context['latest_stamp_record'] = latest_stamp_record
        context['ads_image_details'] = ads_image_details

        # context = {
        #     'bill_details' : bill_details, 'ads_redirect_url': ads_redirect_url, 
        #     'ads_image':ads_image, 'business_logo': business_logo, 'business_address' : business_address, 
        #     'bill_design' : bill_design, 'url_slug':id, 'for_rating_1_object' : for_rating_1_object,
        #     'for_rating_2_object': for_rating_2_object, 'for_rating_3_object': for_rating_3_object,
        #     'for_rating_4_object': for_rating_4_object, 'for_rating_5_object' : for_rating_5_object,
        # }

        return render(request, "customer/customer_bill/my-bill-merchant.html", context)

    except:
        return render(request, 'page-404.html')

def view_merchant_ads(request, id):
    try:
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
    except:
        return render(request, 'page-404.html')



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
    payment_link = MerchantBill.objects.get(bill_url=link_url)

    try:
        payment_settings = MerchantPaymentSetting.objects.get(m_business_id = payment_link.business_name.id)
    except:
        payment_settings = ""

    SALT = str(payment_settings.payu_salt)

    retHashSeq = SALT +'|'+status+'|||||||'+ udf4 + '|' + udf3 + '|' +  udf2 +'|'+ udf1 + '|' + email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+ key

    hash_string = retHashSeq.encode('utf-8')
    
    hashh = hashlib.sha512(hash_string).hexdigest().lower()

    if status == "success":
        if hashh == posted_hash:
            
            result = MerchantBill.objects.filter(id=payment_link.id).update(payment_done = True, payment_date = timezone.now(), transaction_id = txnid, payu_transaction_id = mihpayid)
            if result:
                sweetify.success(request, title="Success", icon='success', text='Transcation done Successfully.', timer=1500)
                return redirect(my_bill_merchant, link_url)
            else:
                sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
                return redirect(my_bill_merchant, link_url)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
            return redirect(my_bill_merchant, link_url)
    else:
        sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
        return redirect(my_bill_merchant, link_url)

@csrf_exempt
def payment_link_fail(request):
    udf1 = request.POST["udf1"]
    sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
    return redirect(my_bill_merchant, udf1)




def reject_merchant_bill(request):

    if request.method == "POST":

        bill_id = request.POST['bill_id']

        bill_object = MerchantBill.objects.get(id=bill_id)

        bill_url = bill_object.bill_url

        rejectbillRadio = request.POST['rejectbillRadio']

        if rejectbillRadio == "1":
            reject_reason = "This is not my bill"

        elif rejectbillRadio == "2":
            reject_reason = "There are mistakes in the bill"

        result = MerchantBill.objects.filter(id=bill_id).update(reject_status = True, reject_reason = reject_reason)


        try:

            bill_object = MerchantBill.objects.get(id=bill_id)

            merchant_user = MerchantProfile.objects.get(id = bill_object.business_name.id)

            device = DeviceId.objects.filter(mobile_no=merchant_user.m_user, user_type = 'merchant').first()
                
            if device:

                push_service = FCMNotification(api_key=settings.API_KEY)

                result = ''

                if device:
                    registration_id = device.device_id
                else:
                    registration_id = ""

                message_title = "Rejected Bill"

                message_body = "Bill was rejected. Kindly check for details "

                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        except:
            pass

        if result:
            sweetify.success(request, title="Success", icon='success', text='Bill Rejected Successfully.', timer=1500)
            return redirect(my_bill_merchant, id = bill_url)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Reject.', timer=1500)
            return redirect(my_bill_merchant, id = bill_url)
    else:
        return redirect(request, 'page-404.html')


def reject_customer_bill(request):

    if request.method == "POST":

        bill_id = request.POST['bill_id']

        bill_object = CustomerBill.objects.get(id=bill_id)

        bill_url = bill_object.bill_url

        rejectbillRadio = request.POST['rejectbillRadio']

        if rejectbillRadio == "1":
            reject_reason = "This is not my bill"

        elif rejectbillRadio == "2":
            reject_reason = "There are mistakes in the bill"

        result = CustomerBill.objects.filter(id=bill_id).update(reject_status = True, reject_reason = reject_reason)

        # try:

        bill_object = CustomerBill.objects.get(id=bill_id)

        merchant_user = MerchantProfile.objects.get(id = bill_object.business_name.id)

        device = DeviceId.objects.filter(mobile_no=merchant_user.m_user, user_type = 'merchant').first()
        try:   
            if device:

                push_service = FCMNotification(api_key=settings.API_KEY)

                result = ''

                if device:
                    registration_id = device.device_id
                else:
                    registration_id = ""

                message_title = "Rejected Bill"

                message_body = "Bill was rejected. Kindly check for details "

                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)


        except:
            pass

        if result:
            sweetify.success(request, title="Success", icon='success', text='Bill Rejected Successfully.', timer=1500)
            return redirect(my_bill, id = bill_url)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Reject.', timer=1500)
            return redirect(my_bill, id = bill_url)
    else:
        return redirect(request, 'page-404.html')

def customer_update_bill_feedback(request):
    
    if request.method == "POST":

        bill_id = request.POST['bill_id']

        bill_object = CustomerBill.objects.get(id=bill_id)

        bill_url = bill_object.bill_url

        feedback_selected_option = request.POST['FeedbackOption']

        feedback_question = request.POST['feedback_question']

        result = CustomerBill.objects.filter(id=bill_id).update(feedback_submit = True, 
            feedback_question = feedback_question, feedback_selected_option = feedback_selected_option
        )

        if result:
            sweetify.success(request, title="Success", icon='success', text='Feedback submited Successfully.', timer=1500)
            return redirect(my_bill, id = bill_url)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Submit.', timer=1500)
            return redirect(my_bill, id = bill_url)
    else:
        return redirect(request, 'page-404.html')


def merchant_update_bill_feedback(request):
    
    if request.method == "POST":

        bill_id = request.POST['bill_id']

        bill_object = MerchantBill.objects.get(id=bill_id)

        bill_url = bill_object.bill_url

        feedback_selected_option = request.POST['FeedbackOption']

        feedback_question = request.POST['feedback_question']

        result = MerchantBill.objects.filter(id=bill_id).update(feedback_submit = True, 
            feedback_question = feedback_question, feedback_selected_option = feedback_selected_option
        )

        if result:
            sweetify.success(request, title="Success", icon='success', text='Feedback submited Successfully.', timer=1500)
            return redirect(my_bill_merchant, id = bill_url)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Submit.', timer=1500)
            return redirect(my_bill_merchant, id = bill_url)
    else:
        return redirect(request, 'page-404.html')


def update_customer_bill_rating(request, id):
    rating = request.POST["rating"]
    bill_details = CustomerBill.objects.filter(bill_url=id).update(rating = rating)
    return JsonResponse({'status':'success'})

def update_merchant_bill_rating(request, id):
    rating = request.POST["rating"]
    bill_details = MerchantBill.objects.filter(bill_url=id).update(rating = rating)
    return JsonResponse({'status':'success'})

@csrf_exempt
def merchantsoftwarelogin(request):

    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        password = request.POST['password']

        try:
            is_merchant = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
            is_merchant_staff = GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_merchant_staff')[0]['is_merchant_staff']

            if is_merchant: 

                user = authenticate(mobile_no=mobile_no, password=password)

                if user:
                    merchant_bussiness = MerchantProfile.objects.filter(Q(m_user = user.id),
                        ~Q(m_business_category = 11) & ~Q(m_business_category = 12)
                    )

                    if merchant_bussiness:
                        if merchant_bussiness[0].m_area:
                            merchant_bussiness_name = merchant_bussiness[0].m_business_name + " (" + merchant_bussiness[0].m_area + ")"
                        else:
                            merchant_bussiness_name = merchant_bussiness[0].m_business_name

                        business_data = {
                            'user_id': user.id,
                            'mobile_no': user.mobile_no,
                            'm_business_id': merchant_bussiness[0].id,
                            'm_business_name': merchant_bussiness_name
                        }

                        return JsonResponse({'status': 'success', 'data': business_data}, status=200)

                    else:
                        return JsonResponse({'status': 'error', 'message': "Invalid Business !!!"}, status=400)

                else:
                    return JsonResponse({'status': 'error', 'message': "Invalid credentials !!!"}, status=400)


            elif is_merchant_staff:

                assign_roles = merchant_userrole.objects.filter(role__role_name ="Exe User",user__mobile_no = mobile_no)

                # assign_roles = merchant_userrole.objects.filter(Q(role__role_name ="Exe User")|Q(role__role_name ="Admin"),user__mobile_no = mobile_no)
                if assign_roles:

                    user = authenticate(mobile_no=mobile_no, password=password)

                    if user:

                        m_business_id = Merchant_users.objects.filter(user_id = user.id).values('m_business_id')[0]['m_business_id']
                        
                        merchant_bussiness = MerchantProfile.objects.filter(id = m_business_id)

                        if merchant_bussiness:

                            if merchant_bussiness[0].m_area:
                                merchant_bussiness_name = merchant_bussiness[0].m_business_name + " (" + merchant_bussiness[0].m_area + ")"
                            else:
                                merchant_bussiness_name = merchant_bussiness[0].m_business_name

                            business_data = {
                                'user_id': user.id,
                                'mobile_no': user.mobile_no,
                                'm_business_id': merchant_bussiness[0].id,
                                'm_business_name': merchant_bussiness_name
                            }

                            return JsonResponse({'status': 'success', 'data': business_data}, status=200)

                        else:
                            return JsonResponse({'status': 'error', 'message': "Invalid Business !!!"}, status=400)

                    else:
                        return JsonResponse({'status': 'error', 'message': "Invalid credentials !!!"}, status=400)
                else:
                    return JsonResponse({'status': 'error', 'message': "Invalid credentials !!!"}, status=400)

            else:
                return JsonResponse({'status': 'error', 'message': "Invalid User !!!"}, status=400)

        except:
            return JsonResponse({'status': 'error', 'message': "User not register !!!"}, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': "Something went wrong !!!"}, status=400)


@csrf_exempt
def check_subscription_available(request):

    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        m_business_id = request.POST['m_business_id']

        try:

            user_object = GreenBillUser.objects.get(mobile_no = mobile_no)
            merchant_profile = Merchant_users.objects.get(user_id = user_object)

            merchant_object = GreenBillUser.objects.get(mobile_no = merchant_profile.merchant_user_id)

            merchant_business = MerchantProfile.objects.get(id = m_business_id)

            business_id = merchant_business.id

            startswith = str(business_id) + ','
            endswith = ','+ str(business_id)
            contains = ','+ str(business_id) + ','
            exact = str(business_id)
      
            subscription_object = merchant_subscriptions.objects.get(
                Q(merchant_id = merchant_object),
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )

            total_amount_avilable = float(subscription_object.total_amount_avilable)

            per_bill_cost = float(subscription_object.per_bill_cost)

            per_digital_bill_cost = float(subscription_object.per_digital_bill_cost)

            if total_amount_avilable >= per_bill_cost and total_amount_avilable >= per_digital_bill_cost:
                amount_status = True
            else:
                amount_status = False

            if subscription_object and amount_status == True:
                return JsonResponse({'status': 'success', 'message': "Subscription Available", 'amount_status': amount_status}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': "<div class='row justify-content-center'>You do not have sufficient Balance to Send Bill.</div>"}, status=400)

        except:
            return JsonResponse({'status': 'error', 'message': "<div class='row justify-content-center'>You do not have active Subscription Plan.</div>"}, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': "Something went wrong !!!"}, status=400)


def getActiveSubscriptionPlanSoftware(request, business_id):

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


@csrf_exempt
def getMerchantBusinesses(request):
    if request.method == "POST":
        print("ok")

        user_id = request.POST['user_id']

        merchant_user = Merchant_users.objects.get(user_id = user_id)
        business_data = []
        filter_business_list = []
        if user_id:
            merchantBusiness1 = MerchantProfile.objects.filter(m_user = merchant_user.merchant_user_id)
            for i in merchantBusiness1:
                subscription_object = getActiveSubscriptionPlanSoftware(request, i.id)
                if subscription_object:
                    if int(i.m_business_category.id) != 11 and int(i.m_business_category.id) != 12:
                        bills = sent_bill_history.objects.filter(user_id = user_id,is_exe=True).last()
                        print('bills',bills)
                        if bills:
                            b_id = bills.m_business_id
                            if int(i.id) == int(b_id):
                                business_data.append({
                                                'id': i.id,
                                                'm_business_name': i.m_business_name + '(' + i.m_area + ')'
                                            })
                                for j in merchantBusiness1:
                                    if subscription_object:
                                        if int(j.m_business_category.id) != 11 and int(j.m_business_category.id) != 12:
                                            if int(j.id) == int(b_id):
                                                pass
                                            else:
                                                business_data.append({
                                                        'id': j.id,
                                                        'm_business_name': j.m_business_name + '(' + j.m_area + ')'
                                                    })
                        else:
                            business_data.append({
                                'id': i.id,
                                'm_business_name': i.m_business_name + '(' + i.m_area + ')'
                            })



            return JsonResponse({'status': 'success', 'data': business_data}, status=200)

        else:
            return JsonResponse({'status': 'error', 'message': "Invalid Business !!!"}, status=400)


@csrf_exempt
def getStampNames(request):
    if request.method == "POST":

        user_id = request.POST['user_id']
        # user_id = request.POST['user_id']

        try:
            stamp1 = merchant_select_stamp = merchantusagestamp.objects.filter(merchant_user_id = user_id).last()
            stamp_id = stamp1.merchant_stamp_id_one
        except:
            stamp_id = ""

        if stamp_id:
            temp_stamp = ""
            temp_stamp = stamp_id.replace("[", "")
            temp_stamp = temp_stamp.replace("]", "")
            temp_stamp = temp_stamp.replace("'", "")
            stamp_id = temp_stamp

        new_stamp_id = stamp_id.split(", ")

        stamp_data = []
        
        for stamp in new_stamp_id:
            if stamp:
                latest_stamp_record = wstampmodels.objects.filter(id=stamp)
                for stamp1 in latest_stamp_record:
                    stamp_data.append({
                        'id':stamp1.id,
                        'stamp_content':stamp1.stamp_content,
                        })

        return JsonResponse({'status': 'success', 'data': stamp_data}, status=200)

    else:
        return JsonResponse({'status': 'error', 'message': "Invalid Stamp Names !!!"}, status=400)



@csrf_exempt
def get_sample_bill(request):
    ts = int(time.time())
    print(ts)
    print("ok")

    if request.method == "POST":
        print("ok")
        mobile_no = request.POST['mobile_no']

        print('mobile_no',mobile_no)
        
        mobile_no_new = mobile_no.replace('+91', '')

        ts = int(time.time())

        data_temp = {
                "keyword":"Send Sample Bill",
                "timeStamp":ts,
                "dataSet":
                    [
                        {
                            "UNIQUE_ID":"GB-" + str(ts),
                            "MESSAGE":"Thank you for contacting Green Bill, tap the below link for your digital bill https://bit.ly/3fwlvqt",
                            "OA":"GBBILL",
                            "MSISDN": str(mobile_no_new), # Recipient's Mobile Number
                            "CHANNEL":"SMS",
                            "CAMPAIGN_NAME":"hind_user",
                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                            "USER_NAME":"hind_hsi",
                            "DLT_TM_ID":"1001096933494158", # TM ID
                            "DLT_CT_ID":"1007162098307281560", # Template Id
                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                        }
                    ]
                }

        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

        response = requests.post(url, json = data_temp)

        if response.status_code == 200:
            return JsonResponse({'status':'success'}, status=200)
        else:
            return JsonResponse({'status':'error'}, status=400)

    else:
        return JsonResponse({'status':'error', 'message': "Something Went Wrong !!!"}, status=400)

@csrf_exempt
def GreenBillCommonSendBillApi1(request):
    if request.method == "POST":
        merchant_mobile_number = request.POST.get('merchant_mobile_number')
        customer_mobile_number = request.POST.get('customer_mobile_number')
        invoice_number = request.POST.get('bill_no')
        # bill_amount = request.POST.get('total_amount')
        
        food_quantity = request.POST.get('quantity')
        food_rate = request.POST.get('rate')

        particulars = request.POST.get('particulars')
        if not particulars:
            particulars = ''

        maximum_retail_price = request.POST.get('maximum_retail_price')
        if not maximum_retail_price:
            maximum_retail_price = ''

        unit = request.POST.get('unit')
        if not unit:
            unit = ''

        discount_in_percentage = request.POST.get('discount_in_percentage')
        if not discount_in_percentage:
            discount_in_percentage = ''

        amount = request.POST.get('amount')
        if not amount:
            amount = ''

        total_amount = request.POST.get('total_amount')
        if not total_amount:
            total_amount = ''

        net_amount = request.POST.get('net_amount')
        if not net_amount:
            net_amount = ''

        cgst = request.POST.get('cgst')
        if not cgst:
            cgst = ''

        sgst = request.POST.get('sgst')
        if not sgst:
            sgst = ''     

        igst = request.POST.get('igst')
        if not igst:
            igst = ''

        hsn = request.POST.get('hsn')
        if not hsn:
            hsn = ''

        pack = request.POST.get('pack')
        if not pack:
            pack = ''

        is_merchant = GreenBillUser.objects.filter(mobile_no = merchant_mobile_number)

        partner_number = "8999476918"

        partner_id = GreenBillUser.objects.get(mobile_no = "8999476918")

        if is_merchant:

            try:
                subscription_object = partner_subscriptions.objects.get(partner_id = partner_id, is_active = True)
            except:
                subscription_object = ""

            if subscription_object:

                if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

                    user_id = GreenBillUser.objects.get(mobile_no = merchant_mobile_number)

                    merchant_business_object = MerchantProfile.objects.filter(m_user = user_id).last()

                    business_category_name = merchant_business_object.m_business_category.business_category_name

                    bill_category_id = bill_category.objects.filter(bill_category_name = business_category_name).values('id')[0]['id']
                    
                    if bill_category_id:
                        bill_category_object = bill_category.objects.get(id = bill_category_id)
                    else:
                        bill_category_object = ""

                    green_points_settings_object = GreenPointsSettings.objects.get(id = 1)

                    green_points = green_points_settings_object.bill_points

                    is_available = GreenBillUser.objects.filter(mobile_no = customer_mobile_number)

                    customer_bill = CustomerBill.objects.create(user_id = user_id, mobile_no = customer_mobile_number,
                            email = user_id.m_email, green_points_earned = str(green_points), business_name = merchant_business_object,
                            invoice_no = invoice_number, customer_bill_category = bill_category_object,
                            food_quantity = food_quantity, food_rate = food_rate
                        )

                    CustomerBill.objects.filter(id = customer_bill.id).update(unit = unit, pack = pack, hsn = hsn, particular = particulars, 
                        cgst = cgst, sgst = sgst, igst = igst, amount = amount, total_amount = total_amount, net_amount = net_amount, 
                        maximum_retail_price = maximum_retail_price)

                    history_result1 = sent_bill_history.objects.create(subscription_id = subscription_object.id, user_id = user_id,
                            mobile_no = customer_mobile_number, m_business_id = merchant_business_object.id, bill_amount = net_amount,
                            customer_bill = True
                        )

                    letters = string.ascii_letters
                    digit = string.digits
                    random_string = str(customer_bill.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                    
                    customer_bill_new = CustomerBill.objects.filter(id=customer_bill.id).update(bill_url = random_string)

                    bill_url = CustomerBill.objects.filter(id=customer_bill.id).values('bill_url')[0]['bill_url']

                    customer_bill_url = "http://157.230.228.250/my-green-bill/" + str(bill_url) + "/"

                    if is_available[0].is_customer:

                        print("is_customer")

                        try: 
                            green_points_old = GreenPointsModel.objects.filter(mobile_no=customer_mobile_number).values('green_points_count')[0]['green_points_count']   
                        except:
                            green_points_old = 0

                        green_points_new = int(green_points_old) + int(green_points)

                        GreenPointsModel.objects.update_or_create(mobile_no=customer_mobile_number, defaults={'green_points_count': green_points_new})

                        device = DeviceId.objects.filter(mobile_no=customer_mobile_number).first()

                        push_service = FCMNotification(api_key=settings.API_KEY)

                        if device != None:

                            CustomerBill.objects.filter(id=customer_bill.id).update(greenbill_digital_bill = True)

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
                            if customer_mobile_number:

                                s = pyshorteners.Shortener()

                                short_url = s.tinyurl.short(customer_bill_url)

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
                                                    "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
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
                                    return JsonResponse({'status':'success', 'message': 'SMS sent successfully'}, status=200)
                                else:
                                    return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                            else:
                                return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                    else:
                        if customer_mobile_number:

                            s = pyshorteners.Shortener()

                            short_url = s.tinyurl.short(customer_bill_url)

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
                                                "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
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
                                return JsonResponse({'status':'success', 'message': 'SMS sent successfully'}, status=200)
                            else:
                                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                        else:
                            return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                else:
                    return JsonResponse({'status':'error', 'message': "You don't have Sufficient Available Amount !!!"}, status=400)
            else:
                return JsonResponse({'status':'error', 'message': "You don't have any active subscription plan !!!"}, status=400)
        else:
            return JsonResponse({'status':'error', 'message': "Merchant could not be Found !!!"}, status=400)


@csrf_exempt
def CommonSendBillGreenBillApi2(request):
    if request.method == "POST":
        merchant_mobile_number = request.POST.get('merchant_mobile_number')
        customer_mobile_number = request.POST.get('customer_mobile_number')
        invoice_number = request.POST.get('bill_no')

        cdn_code = request.POST.get('cdn_code')
        if not cdn_code:
            cdn_code = ''
        mult_f = request.POST.get('mult_f')
        if not mult_f:
            mult_f = ''
        trade = request.POST.get('trade')
        if not trade:
            trade = ''
        bill_bb = request.POST.get('bill_bb')
        if not bill_bb:
            bill_bb = '' 
        bill2 = request.POST.get('bill2')
        if not bill2:
            bill2 = '' 
        dm_no = request.POST.get('dm_no')
        if not dm_no:
            dm_no = '' 
        con_bill = request.POST.get('con_bill')
        if not con_bill:
            con_bill = '' 
        ad_bill = request.POST.get('ad_bill')
        if not ad_bill:
            ad_bill = '' 
        absbas10 = request.POST.get('bas10')
        if not absbas10:
            absbas10 = '' 

        try:
            amount10 = request.POST['amount10']
        except:
            amount10 = ''

        try:
            sch10 = request.POST['sch10']
        except:
            sch10 = ''

        dis10 = request.POST.get('dis10')
        if not dis10:
            dis10 = ''
        cd10 = request.POST.get('cd10')
        if not cd10:
            cd10 = ''
        net10 = request.POST.get('net10')
        if not net10:
            net10 = ''
        gd10 = request.POST.get('gd10')
        if not gd10:
            gd10 = ''
        gst10 = request.POST.get('gst10')
        if not gst10:
            gst10 = ''
        gr_code9 = request.POST.get('gr_code9')
        if not gr_code9:
            gr_code9 = ''
        product = request.POST.get('product')
        if not product:
            product = ''
        product_i = request.POST.get('product_i')
        if not product_i:
            product_i = ''
        old_code = request.POST.get('old_code')
        if not old_code:
            old_code = ''
        spid = request.POST.get('spid')
        if not spid:
            spid = ''
        h_code = request.POST.get('h_code')
        if not h_code:
            h_code = ''
        brand = request.POST.get('brand')
        if not brand:
            brand = ''
        weight = request.POST.get('weight')
        if not weight:
            weight = ''
        wt_unit = request.POST.get('wt_unit')
        if not wt_unit:
            wt_unit = ''

        it_weight = request.POST.get('it_weight')
        if not it_weight:
            it_weight = ''

        qty_c = request.POST.get('qty_c')
        if not qty_c:
            qty_c = ''
        unit_c = request.POST.get('unit_c')
        if not unit_c:
            unit_c = ''
        pst1 = request.POST.get('pst1')
        if not pst1:
            pst1 = ''
        mst1 = request.POST.get('mst1')
        if not mst1:
            mst1 = ''
        roff = request.POST.get('roff')
        if not roff:
            roff = ''
        t_qty = request.POST.get('t_qty')
        if not t_qty:
            t_qty = ""
        freeval = request.POST.get('freeval')
        if not freeval:
            freeval = ''

        t_qty_c = request.POST.get('t_qty_c')
        if not t_qty_c:
            t_qty_c = ''

        dis_c = request.POST.get('dis_c')
        if not dis_c:
            dis_c = ''

        cd_c = request.POST.get('cd_c')
        if not cd_c:
            cd_c = ''

        bas10rate = request.POST.get('bas10rate')
        if not bas10rate:
            bas10rate = ''

        bas10amt = request.POST.get('bas10amt')
        if not bas10amt:
            bas10amt = ''

        sno_c = request.POST.get('sno_c')
        if not sno_c:
            sno_c = ''

        gst_c = request.POST.get('gst_c')
        if not gst_c:
            gst_c = ''

        rate_c = request.POST.get('rate_c')
        if not rate_c:
            rate_c = ''

        bas10_c = request.POST.get('bas10_c')
        if not bas10_c:
            bas10_c = ''

        sch_c = request.POST.get('sch_c')
        if not sch_c:
           sch_c = ''
            
        bas10sch = request.POST.get('bas10sch')
        if not bas10sch:
            bas10sch = ''

        bas10cd = request.POST.get('bas10cd')
        if not bas10cd:
            bas10cd = ""

        bas10dis = request.POST.get('bas10dis')
        if not bas10dis:
            bas10dis = ''

        bas10tle = request.POST.get('bas10tle')
        if not bas10tle:
            bas10tle = ''

        absbas10net = request.POST.get('bas10net')
        if not absbas10net:
            absbas10net = ''

        maximum_retail_price = request.POST.get('maximum_retail_price')
        if not maximum_retail_price:
            maximum_retail_price = ''

        rate = request.POST.get('rate')
        if not rate:
            rate = ''

        quantity = request.POST.get('quantity')
        if not quantity:
            quantity = ''

        cash = request.POST.get('cash')
        if not cash:
            cash = ''

        discount_in_percentage = request.POST.get('discount')

        is_merchant = GreenBillUser.objects.filter(mobile_no = merchant_mobile_number)

        partner_number = "8999476918"

        partner_id = GreenBillUser.objects.get(mobile_no = "8999476918")

        if is_merchant:

            try:
                subscription_object = partner_subscriptions.objects.get(partner_id = partner_id, is_active = True)
            except:
                subscription_object = ""

            if subscription_object:

                if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

                    user_id = GreenBillUser.objects.get(mobile_no = merchant_mobile_number)

                    merchant_business_object = MerchantProfile.objects.filter(m_user = user_id).last()

                    business_category_name = merchant_business_object.m_business_category.business_category_name

                    bill_category_id = bill_category.objects.filter(bill_category_name = business_category_name).values('id')[0]['id']
                    
                    if bill_category_id:
                        bill_category_object = bill_category.objects.get(id = bill_category_id)
                    else:
                        bill_category_object = ""

                    green_points_settings_object = GreenPointsSettings.objects.get(id = 1)

                    green_points = green_points_settings_object.bill_points

                    is_available = GreenBillUser.objects.filter(mobile_no = customer_mobile_number)

                    customer_bill = CustomerBill.objects.create(user_id = user_id, mobile_no = customer_mobile_number,
                            email = user_id.m_email, green_points_earned = str(green_points), business_name = merchant_business_object,
                            invoice_no = invoice_number, customer_bill_category = bill_category_object, 
                        )

                    CustomerBill.objects.filter(id = customer_bill.id).update(cdn_code = cdn_code, mult_f = mult_f, trade = trade, bill_bb = bill_bb,
                        bill2 = bill2, dm_no = dm_no, con_bill = con_bill, ad_bill = ad_bill, bas10 = absbas10, amt10 = amount10, sch10 = sch10, dis10 = dis10,
                        cd10 = cd10, net10 = net10, gd10 = gd10, gst10 = gst10, gr_code9 = gr_code9, product = product, product_i = product_i, old_code = old_code,
                        spid = spid, h_code = h_code, brand = brand, weight = weight, wt_unit = wt_unit, it_weight = it_weight,
                        qty_c = qty_c, unit_c = unit_c, pst1 = pst1, mst1 = mst1, roff = roff, t_qty = t_qty, freeval = freeval,
                        t_qty_c = t_qty_c, dis_c = dis_c, cd_c = cd_c, bas10rate = bas10rate, bas10amt = bas10amt, sno_c = sno_c, gst_c = gst_c, rate_c = rate_c,
                        bas10_c = bas10_c, sch_c = sch_c, bas10sch = bas10sch, bas10cd = bas10cd, bas10tle = bas10tle, bas10net = absbas10net, maximum_retail_price = maximum_retail_price,
                        cash = cash, food_rate = rate, food_quantity = quantity)

                    history_result1 = sent_bill_history.objects.create(subscription_id = subscription_object.id, user_id = user_id,
                            mobile_no = customer_mobile_number, m_business_id = merchant_business_object.id,
                            customer_bill = True
                        )

                    letters = string.ascii_letters
                    digit = string.digits
                    random_string = str(customer_bill.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                    
                    customer_bill_new = CustomerBill.objects.filter(id=customer_bill.id).update(bill_url = random_string)

                    bill_url = CustomerBill.objects.filter(id=customer_bill.id).values('bill_url')[0]['bill_url']

                    customer_bill_url = "http://157.230.228.250/my-green-bill/" + str(bill_url) + "/"

                    if is_available[0].is_customer:

                        print("is_customer")

                        try: 
                            green_points_old = GreenPointsModel.objects.filter(mobile_no=customer_mobile_number).values('green_points_count')[0]['green_points_count']   
                        except:
                            green_points_old = 0

                        green_points_new = int(green_points_old) + int(green_points)

                        GreenPointsModel.objects.update_or_create(mobile_no=customer_mobile_number, defaults={'green_points_count': green_points_new})

                        device = DeviceId.objects.filter(mobile_no=customer_mobile_number).first()

                        push_service = FCMNotification(api_key=settings.API_KEY)

                        if device != None:

                            CustomerBill.objects.filter(id=customer_bill.id).update(greenbill_digital_bill = True)

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
                            if customer_mobile_number:

                                s = pyshorteners.Shortener()

                                short_url = s.tinyurl.short(customer_bill_url)

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
                                                    "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
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
                                    return JsonResponse({'status':'success', 'message': 'SMS sent successfully'}, status=200)
                                else:
                                    return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                            else:
                                return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                    else:
                        if customer_mobile_number:

                            s = pyshorteners.Shortener()

                            short_url = s.tinyurl.short(customer_bill_url)

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
                                                "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
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
                                return JsonResponse({'status':'success', 'message': 'SMS sent successfully'}, status=200)
                            else:
                                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                        else:
                            return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                else:
                    return JsonResponse({'status':'error', 'message': "You don't have Sufficient Available Amount !!!"}, status=400)
            else:
                return JsonResponse({'status':'error', 'message': "You don't have any active subscription plan !!!"}, status=400)
        else:
            return JsonResponse({'status':'error', 'message': "Merchant could not be Found !!!"}, status=400)


@csrf_exempt
def GreenBillCommon3Api(request):
    if request.method == "POST":
        merchant_mobile_number = request.POST.get('merchant_mobile_number')
        customer_mobile_number = request.POST.get('customer_mobile_number')
        bill_number = request.POST.get('bill')

        series = request.POST.get('series')
        if not series:
            series = ''

        c_code = request.POST.get('c_code')
        if not c_code:
            c_code = ''

        br_code = request.POST.get('br_code')
        if not br_code:
            br_code = ''

        c_name = request.POST.get('c_name')
        if not c_name:
            c_name = '' 

        c_add1 = request.POST.get('c_add1')
        if not c_add1:
            c_add1 = '' 

        c_add2 = request.POST.get('c_add2')
        if not c_add2:
            c_add2 = ''

        c_place = request.POST.get('c_place')
        if not c_place:
            c_place = '' 

        transfer = request.POST.get('transfer')
        if not transfer:
            transfer = '' 

        trns_name = request.POST.get('trns_name')
        if not trns_name:
            trns_name = '' 

        try:
            bill_bb = request.POST['bill_bb']
        except:
            bill_bb = ''

        try:
            bill_dd = request.POST['bill_dd']
        except:
            bill_dd = ''

        bill2 = request.POST.get('bill2')
        if not bill2:
            bill2 = ''

        bill1 = request.POST.get('bill1')
        if not bill1:
            bill1 = ''

        n_b_amt = request.POST.get('n_b_amt')
        if not n_b_amt:
            n_b_amt = ''

        truck_no = request.POST.get('truck_no')
        if not truck_no:
            truck_no = ''

        truck_driver = request.POST.get('truck_driver')
        if not truck_driver:
            truck_driver = ''

        truck_license_no = request.POST.get('truck_license_no')
        if not truck_license_no:
            truck_license_no = ''

        transport_name = request.POST.get('transport_name')
        if not transport_name:
            transport_name = ''

        pan_number = request.POST.get('c_pan_no')
        if not pan_number:
            pan_number = ''

        r_off = request.POST.get('r_off')
        if not r_off:
            r_off = ''

        dm_ser = request.POST.get('dm_ser')
        if not dm_ser:
            dm_ser = ''

        dm_no = request.POST.get('dm_no')
        if not dm_no:
            dm_no = ''

        con_date = request.POST.get('con_date')
        if not con_date:
            con_date = ''

        con_bill = request.POST.get('con_bill')
        if not con_bill:
            con_bill = ''

        ad_series = request.POST.get('ad_series')
        if not ad_series:
            ad_series = ''

        pst9 = request.POST.get('pst9')
        if not pst9:
            pst9 = ''

        c_cst = request.POST.get('c_cst')
        if not c_cst:
            c_cst = ''

        dvd_pay = request.POST.get('dvd_pay')
        if not dvd_pay:
            dvd_pay = ''

        finance = request.POST.get('finance')
        if not finance:
            finance = ''

        fn_code = request.POST.get('fn_code')
        if not fn_code:
            fn_code = ''

        dn_pay = request.POST.get('dn_pay')
        if not dn_pay:
            dn_pay = ''

        fn_id = request.POST.get('fn_id')
        if not fn_id:
            fn_id = ""

        code_org = request.POST.get('code_org')
        if not code_org:
            code_org = ''

        sm_org = request.POST.get('sm_org')
        if not sm_org:
            sm_org = ''

        fsaaino = request.POST.get('fsaaino')
        if not fsaaino:
            fsaaino = ''

        n_name = request.POST.get('n_name')
        if not n_name:
            n_name = ''

        hin_name = request.POST.get('hin_name')
        if not hin_name:
            hin_name = ''

        n_add1 = request.POST.get('n_add1')
        if not n_add1:
            n_add1 = ''

        n_add2 = request.POST.get('n_add2')
        if not n_add2:
            n_add2 = ''

        n_place = request.POST.get('n_place')
        if not n_place:
            n_place = ''

        sman = request.POST.get('sman')
        if not sman:
            sman = ''

        cash = request.POST.get('cash')
        if not cash:
            cash = ''

        discount_in_percentage = request.POST.get('discount')

        is_merchant = GreenBillUser.objects.filter(mobile_no = merchant_mobile_number)

        partner_number = "8999476918"

        partner_id = GreenBillUser.objects.get(mobile_no = "8999476918")

        if is_merchant:

            try:
                subscription_object = partner_subscriptions.objects.get(partner_id = partner_id, is_active = True)
            except:
                subscription_object = ""

            if subscription_object:

                if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

                    user_id = GreenBillUser.objects.get(mobile_no = merchant_mobile_number)

                    merchant_business_object = MerchantProfile.objects.filter(m_user = user_id).last()

                    business_category_name = merchant_business_object.m_business_category.business_category_name

                    bill_category_id = bill_category.objects.filter(bill_category_name = business_category_name).values('id')[0]['id']
                    
                    if bill_category_id:
                        bill_category_object = bill_category.objects.get(id = bill_category_id)
                    else:
                        bill_category_object = ""

                    green_points_settings_object = GreenPointsSettings.objects.get(id = 1)

                    green_points = green_points_settings_object.bill_points

                    is_available = GreenBillUser.objects.filter(mobile_no = customer_mobile_number)

                    customer_bill = CustomerBill.objects.create(user_id = user_id, mobile_no = customer_mobile_number,
                            email = user_id.m_email, green_points_earned = str(green_points), business_name = merchant_business_object,
                            invoice_no = bill_number, customer_bill_category = bill_category_object)

                    CustomerBill.objects.filter(id = customer_bill.id).update(series = series, c_code = c_code, br_code = br_code,
                        c_name = c_name, c_add1 = c_add1, c_add2 = c_add2, c_place = c_place, transfer = transfer, trns_name = trns_name, bill_bb = bill_bb,
                        bill2 = bill2, bill1 = bill1, n_b_amt = n_b_amt, truck_no = truck_no, truck_driver = truck_driver, truck_license_no = truck_license_no,
                        transport_name = transport_name, c_pan_no = pan_number, r_off = r_off, dm_ser = dm_ser, dm_no = dm_no, con_date = con_date, con_bill = con_bill, ad_series = ad_series,
                        pst9 = pst9, c_cst = c_cst, dvd_pay = dvd_pay, finance = finance, fn_code = fn_code, dn_pay = dn_pay, fn_id = fn_id, code_org = code_org,
                        sm_org = sm_org, fsaaino = fsaaino, n_name = n_name, hin_name = hin_name, n_add1 = n_add1, n_add2 = n_add2, n_place = n_place, sman = sman, cash = cash)

                    history_result1 = sent_bill_history.objects.create(subscription_id = subscription_object.id, user_id = user_id,
                            mobile_no = customer_mobile_number, m_business_id = merchant_business_object.id,
                            customer_bill = True
                        )

                    letters = string.ascii_letters
                    digit = string.digits
                    random_string = str(customer_bill.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                    
                    customer_bill_new = CustomerBill.objects.filter(id=customer_bill.id).update(bill_url = random_string)

                    bill_url = CustomerBill.objects.filter(id=customer_bill.id).values('bill_url')[0]['bill_url']

                    customer_bill_url = "http://157.230.228.250/my-green-bill/" + str(bill_url) + "/"

                    if is_available[0].is_customer:

                        print("is_customer")

                        try: 
                            green_points_old = GreenPointsModel.objects.filter(mobile_no=customer_mobile_number).values('green_points_count')[0]['green_points_count']   
                        except:
                            green_points_old = 0

                        green_points_new = int(green_points_old) + int(green_points)

                        GreenPointsModel.objects.update_or_create(mobile_no=customer_mobile_number, defaults={'green_points_count': green_points_new})

                        device = DeviceId.objects.filter(mobile_no=customer_mobile_number).first()

                        push_service = FCMNotification(api_key=settings.API_KEY)

                        if device != None:

                            CustomerBill.objects.filter(id=customer_bill.id).update(greenbill_digital_bill = True)

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
                            if customer_mobile_number:

                                s = pyshorteners.Shortener()

                                short_url = s.tinyurl.short(customer_bill_url)

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
                                                    "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
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
                                    return JsonResponse({'status':'success', 'message': 'SMS sent successfully'}, status=200)
                                else:
                                    return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                            else:
                                return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                    else:
                        if customer_mobile_number:

                            s = pyshorteners.Shortener()

                            short_url = s.tinyurl.short(customer_bill_url)

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
                                                "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
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
                                return JsonResponse({'status':'success', 'message': 'SMS sent successfully'}, status=200)
                            else:
                                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                        else:
                            return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                else:
                    return JsonResponse({'status':'error', 'message': "You don't have Sufficient Available Amount !!!"}, status=400)
            else:
                return JsonResponse({'status':'error', 'message': "You don't have any active subscription plan !!!"}, status=400)
        else:
            return JsonResponse({'status':'error', 'message': "Merchant could not be Found !!!"}, status=400)

@csrf_exempt
def GreenBillSendBillApi(request):
    if request.method == "POST":
        merchant_mobile_number = request.POST.get('merchant_mobile_number')
        customer_mobile_number = request.POST.get('customer_mobile_number')
        invoice_number = request.POST.get('bill_no')
        bill_amount = request.POST.get('total_amount')
        
        food_quantity = request.POST.get('quantity')
        food_rate = request.POST.get('rate')
        food_amount = request.POST.get('amount')
        food_discount_parcentage = request.POST.get('discount')

        particulars = request.POST.get('particulars')
        if not particulars:
            particulars = ''

        service_charge = request.POST.get('service_charge')
        if not service_charge:
            service_charge = ''

        table_number = request.POST.get('table_number')
        if not table_number:
            table_number = ''

        waiter_name = request.POST.get('waiter_name')
        if not waiter_name:
            waiter_name = ""

        food_item_names = request.POST.get('food_item_names')
        if not food_item_names:
            food_item_names = ''
        bar_item_names = request.POST.get('bar_item_names')

        if not bar_item_names:
            bar_item_names = ''

        bar_quantity = request.POST.get('bar_quantity')
        if not bar_quantity:
            bar_quantity = ''

        bar_rate = request.POST.get('bar_rate')
        if not bar_rate:
            bar_rate = ''

        bar_amount = request.POST.get('bar_amount')
        if not bar_amount:
            bar_amount = ''

        bar_discount_percentage = request.POST.get('bar_discount')

        print(bar_discount_percentage)

        if not bar_discount_percentage:
            bar_discount_percentage = ''

        if not food_discount_parcentage:
            food_discount_parcentage = ''

        extra_add = request.POST.get('extra_additional_amount')

        if not extra_add:
            extra_add = ''

        cash = request.POST.get('cash')
        if not cash:
            cash = ''

        card = request.POST.get('card')
        if not card:
            card = ''

        digital_pay = request.POST.get('digital_pay')
        if not digital_pay:
            digital_pay = ''

        discount_in_percentage = request.POST.get('discount_in_percentage')
        if not discount_in_percentage:
            discount_in_percentage = ''

        cgst = request.POST.get('cgst')
        if not cgst:
            cgst = ''

        sgst = request.POST.get('sgst')
        if not sgst:
            sgst = ''

        igst = request.POST.get('igst')
        if not igst:
            igst = ''

        hsn = request.POST.get('hsn')
        if not hsn:
            hsn = ''

        pack = request.POST.get('pack')
        if not pack:
            pack = ''

        unit = request.POST.get('unit')
        if not unit:
            unit = ''

        truck_no = request.POST.get('truck_no')
        if not truck_no:
            truck_no = '' 

        truck_driver = request.POST.get('truck_driver')
        if not truck_driver:
            truck_driver = '' 

        truck_license_no = request.POST.get('truck_license_no')
        if not truck_license_no:
            truck_license_no = ''

        transport_name = request.POST.get('transport_name')
        if not transport_name:
            transport_name = ''

        pan_number = request.POST.get('pan_number')
        if not pan_number:
            pan_number = ''


        is_merchant = GreenBillUser.objects.filter(mobile_no = merchant_mobile_number)

        partner_number = "8999476918"

        partner_id = GreenBillUser.objects.get(mobile_no = "8999476918")

        if is_merchant:

            try:
                subscription_object = partner_subscriptions.objects.get(partner_id = partner_id, is_active = True)
            except:
                subscription_object = ""

            if subscription_object:

                if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

                    user_id = GreenBillUser.objects.get(mobile_no = merchant_mobile_number)

                    merchant_business_object = MerchantProfile.objects.filter(m_user = user_id).last()

                    business_category_name = merchant_business_object.m_business_category.business_category_name

                    bill_category_id = bill_category.objects.filter(bill_category_name = business_category_name).values('id')[0]['id']
                    
                    if bill_category_id:
                        bill_category_object = bill_category.objects.get(id = bill_category_id)
                    else:
                        bill_category_object = ""

                    green_points_settings_object = GreenPointsSettings.objects.get(id = 1)

                    green_points = green_points_settings_object.bill_points

                    is_available = GreenBillUser.objects.filter(mobile_no = customer_mobile_number)

                    customer_bill = CustomerBill.objects.create(user_id = user_id, mobile_no = customer_mobile_number, is_hebrone = True,
                            email = user_id.m_email, green_points_earned = str(green_points), business_name = merchant_business_object,
                            invoice_no = invoice_number, bill_amount = bill_amount, customer_bill_category = bill_category_object,
                            food_quantity = food_quantity, food_rate = food_rate, food_amount = food_amount,
                            food_discount_parcentage = food_discount_parcentage, truck_no = truck_no, 
                        )

                    CustomerBill.objects.filter(id = customer_bill.id).update(extra_add = extra_add, table_number = table_number, waiter_name = waiter_name,
                        food_item_names = food_item_names, bar_item_names = bar_item_names, bar_quantity = bar_quantity, bar_rate = bar_rate, bar_amount = bar_amount,
                        bar_discount_percentage = bar_discount_percentage, cash = cash, card = card, digital_pay = digital_pay, service_charge = service_charge,
                        discount_in_percentage = discount_in_percentage, pan_number = pan_number, transport_name = transport_name, cgst = cgst, sgst = sgst, igst = igst,
                        truck_license_no = truck_license_no, truck_driver = truck_driver, unit = unit, pack = pack, hsn = hsn, particular = particulars)

                    history_result1 = sent_bill_history.objects.create(subscription_id = subscription_object.id, user_id = user_id,
                            mobile_no = customer_mobile_number, m_business_id = merchant_business_object.id, bill_amount = bill_amount,
                            customer_bill = True
                        )

                    letters = string.ascii_letters
                    digit = string.digits
                    random_string = str(customer_bill.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                    
                    customer_bill_new = CustomerBill.objects.filter(id=customer_bill.id).update(bill_url = random_string)

                    bill_url = CustomerBill.objects.filter(id=customer_bill.id).values('bill_url')[0]['bill_url']

                    customer_bill_url = "http://157.230.228.250/my-green-bill/" + str(bill_url) + "/"

                    if is_available[0].is_customer:

                        print("is_customer")

                        try: 
                            green_points_old = GreenPointsModel.objects.filter(mobile_no=customer_mobile_number).values('green_points_count')[0]['green_points_count']   
                        except:
                            green_points_old = 0

                        green_points_new = int(green_points_old) + int(green_points)

                        GreenPointsModel.objects.update_or_create(mobile_no=customer_mobile_number, defaults={'green_points_count': green_points_new})

                        device = DeviceId.objects.filter(mobile_no=customer_mobile_number).first()

                        push_service = FCMNotification(api_key=settings.API_KEY)

                        if device != None:

                            CustomerBill.objects.filter(id=customer_bill.id).update(greenbill_digital_bill = True)

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
                            if customer_mobile_number:

                                s = pyshorteners.Shortener()

                                short_url = s.tinyurl.short(customer_bill_url)

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
                                                    "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
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
                                    return JsonResponse({'status':'success', 'message': 'SMS sent successfully'}, status=200)
                                else:
                                    return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                            else:
                                return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                    else:
                        if customer_mobile_number:

                            s = pyshorteners.Shortener()

                            short_url = s.tinyurl.short(customer_bill_url)

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
                                                "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
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
                                return JsonResponse({'status':'success', 'message': 'SMS sent successfully'}, status=200)
                            else:
                                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                        else:
                            return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                else:
                    return JsonResponse({'status':'error', 'message': "You don't have Sufficient Available Amount !!!"}, status=400)
            else:
                return JsonResponse({'status':'error', 'message': "You don't have any active subscription plan !!!"}, status=400)
        else:
            return JsonResponse({'status':'error', 'message': "Merchant could not be Found !!!"}, status=400)


@csrf_exempt
def CiferonSendBill(request):
    if request.method == "POST":

        merchant_unique_id = request.POST['merchant_unique_id']

        try:
            merchant_business_object = MerchantProfile.objects.get(m_unique_id = merchant_unique_id)
        except:
            merchant_business_object = ''

        customer_mobile_number = request.POST.get('customer_mobile_number')

        invoice_number = request.POST.get('invoice_number')

        table_number = request.POST.get('table_number')

        if not table_number:
            table_number = ''

        waiter_name = request.POST.get('waiter_name')

        if not waiter_name:
            waiter_name = ''

        pax_number = request.POST.get('pax_number')

        if not pax_number:
            pax_number = ''

        food_details = request.POST.get('order_details')

        food_discount_parcentage = request.POST.get('food_discount_percentage')

        if not food_discount_parcentage:
            food_discount_parcentage = ''

        loyalty_points = request.POST.get('loyalty_points')

        if not loyalty_points:
            loyalty_points = ''

        packaging = request.POST.get('packaging')

        if not packaging:
            packaging = ''

        delivery = request.POST.get('delivery')
        if not delivery:
            delivery = ''

        decoration = request.POST.get('decoration')
        if not decoration:
            decoration = ''

        partner_number = "8999476918"           

        partner_id = GreenBillUser.objects.get(mobile_no = "8999476918")
        
        if merchant_business_object:
            
            try:
                subscription_object = partner_subscriptions.objects.get(partner_id = partner_id, is_active = True)
            except:
                subscription_object = ""

            if subscription_object:

                if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

                    user_id = GreenBillUser.objects.get(mobile_no = merchant_business_object.m_user)

                    business_category_name = merchant_business_object.m_business_category.business_category_name

                    bill_category_id = bill_category.objects.filter(bill_category_name = business_category_name).values('id')[0]['id']
                    
                    if bill_category_id:
                        bill_category_object = bill_category.objects.get(id = bill_category_id)
                    else:
                        bill_category_object = ""

                    green_points_settings_object = GreenPointsSettings.objects.get(id = 1)

                    green_points = green_points_settings_object.bill_points

                    is_available = GreenBillUser.objects.filter(mobile_no = customer_mobile_number)

                    customer_bill = CustomerBill.objects.create(user_id = user_id, mobile_no = customer_mobile_number, is_ciprone = True,
                            email = user_id.m_email, green_points_earned = str(green_points), business_name = merchant_business_object,
                            invoice_no = invoice_number, customer_bill_category = bill_category_object, waiter_name = waiter_name,
                            pax_number = pax_number, food_details = food_details, table_number = table_number,
                            loyalty_points = loyalty_points, packaging = packaging, decoration = decoration, delivery = delivery, food_discount_parcentage = food_discount_parcentage 
                        )
                    history_result1 = sent_bill_history.objects.create(subscription_id = subscription_object.id, user_id = user_id,
                            mobile_no = customer_mobile_number, m_business_id = merchant_business_object.id, 
                            customer_bill = True
                        )

                    letters = string.ascii_letters
                    digit = string.digits
                    random_string = str(customer_bill.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                    
                    customer_bill_new = CustomerBill.objects.filter(id=customer_bill.id).update(bill_url = random_string)

                    bill_url = CustomerBill.objects.filter(id=customer_bill.id).values('bill_url')[0]['bill_url']

                    customer_bill_url = "http://157.230.228.250/my-green-bill/" + str(bill_url) + "/"

                    if is_available[0].is_customer:

                        try: 
                            green_points_old = GreenPointsModel.objects.filter(mobile_no=customer_mobile_number).values('green_points_count')[0]['green_points_count']   
                        except:
                            green_points_old = 0

                        green_points_new = int(green_points_old) + int(green_points)

                        GreenPointsModel.objects.update_or_create(mobile_no=customer_mobile_number, defaults={'green_points_count': green_points_new})

                        device = DeviceId.objects.filter(mobile_no=customer_mobile_number).first()

                        push_service = FCMNotification(api_key=settings.API_KEY)

                        if device != None:

                            CustomerBill.objects.filter(id=customer_bill.id).update(greenbill_digital_bill = True)

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
                            if customer_mobile_number:

                                s = pyshorteners.Shortener()

                                short_url = s.tinyurl.short(customer_bill_url)

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
                                                    "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
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
                                    return JsonResponse({'status':'success', 'message': 'SMS sent successfully'}, status=200)
                                else:
                                    return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                            else:
                                return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                    else:
                        if customer_mobile_number:

                            s = pyshorteners.Shortener()

                            short_url = s.tinyurl.short(customer_bill_url)

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
                                                "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
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
                                return JsonResponse({'status':'success', 'message': 'SMS sent successfully'}, status=200)
                            else:
                                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                        else:
                            return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                else:
                    return JsonResponse({'status':'error', 'message': "You don't have Sufficient Available Amount !!!"}, status=400)
            else:
                return JsonResponse({'status':'error', 'message': "You don't have any active subscription plan !!!"}, status=400)
        else:
            return JsonResponse({'status':'error', 'message': "Merchant could not be Found !!!"}, status=400)


import ast
@csrf_exempt
def HabronSendBill(request):
    try:
    # if 1==1:
        if request.method=='POST':
            
            received_json_data = json.loads(request.body.decode("utf-8"))
            
            merchant_mobile_number = str(received_json_data["merchant_mobile_number"])
            customer_mobile_number = str(received_json_data["customer_mobile_number"])
            invoice_number = str(received_json_data['invoice_number'])
            bill_date = str(received_json_data['bill_date'])
            bill_gross_amount = str(received_json_data['bill_gross_amount'])
            bill_discount = str(received_json_data['bill_discount'])
            bill_amount = str(received_json_data['bill_amount'])
            customer_name =  str(received_json_data['customer_name'])
            item_details = received_json_data['Item_details']
            is_merchant = str(GreenBillUser.objects.filter(mobile_no = merchant_mobile_number))
            print("all done")

            user_id = GreenBillUser.objects.get(mobile_no = merchant_mobile_number)
            print(user_id)
            merchant_business_object = MerchantProfile.objects.filter(m_user = user_id)
            print(list(merchant_business_object))
            for i in list(merchant_business_object):
                print("********")
                print(i.m_business_category)
                if str(i.m_business_category) == "Parking Lot":
                    continue
                elif str(i.m_business_category) == "Petrol Pump":
                    continue
                else:
                    merchant_business_object = i
                    break


            print(merchant_business_object)
            partner_number = "7676767676"

            partner_id = GreenBillUser.objects.get(mobile_no = "7676767676")
            print("Ss")
            if is_merchant:
                print("Ss")
                try:
                    subscription_object_for_link = partner_subscriptions.objects.filter(partner_id = partner_id, is_active = True).last()
                    subscription_object = merchant_subscriptions.objects.filter(merchant_id = user_id, is_active = True).last()
                except:
                    subscription_object = ""
                    subscription_object_for_link = ""

                print(subscription_object,subscription_object_for_link)
                if subscription_object:
                    print("Ss")
                    if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):
                        print("Ss")
                        user_id = GreenBillUser.objects.get(mobile_no = merchant_mobile_number)

                        merchant_business_object = MerchantProfile.objects.filter(m_user = user_id).last()

                        business_category_name = merchant_business_object.m_business_category.business_category_name
                        

                        bill_category_id = bill_category.objects.filter(bill_category_name = business_category_name).values('id')[0]['id']
                        
                        if bill_category_id:
                            bill_category_object = bill_category.objects.get(id = bill_category_id)
                        else:
                            bill_category_object = ""

                        green_points_settings_object = GreenPointsSettings.objects.get(id = 1)

                        green_points = green_points_settings_object.bill_points

                        is_available = GreenBillUser.objects.filter(mobile_no = customer_mobile_number)
                       

                        customer_bill = CustomerBill.objects.create(user_id = user_id, mobile_no = customer_mobile_number, is_hebrone = True,
                                        email = user_id.m_email, green_points_earned = str(green_points), business_name = merchant_business_object,
                                        invoice_no = invoice_number, bill_amount = bill_amount, customer_bill_category = bill_category_object,
                                        bill_gross_amount = bill_gross_amount, bill_discount= bill_discount, customer_name = customer_name,
                                        item_details = item_details,bill_date = bill_date,
                                    )
                        history_result1 = sent_bill_history.objects.create(subscription_id = subscription_object.id, user_id = user_id,
                                mobile_no = customer_mobile_number, m_business_id = merchant_business_object.id, bill_amount = bill_amount,
                                customer_bill = True
                            )
                        # print("Saved !!1")
                        letters = string.ascii_letters
                        digit = string.digits
                        random_string = str(customer_bill.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                        # print("random_string")
                        customer_bill_new = CustomerBill.objects.filter(id=customer_bill.id).update(bill_url = random_string)
                        # print("customer_bill_new")
                        bill_url = CustomerBill.objects.filter(id=customer_bill.id).values('bill_url')[0]['bill_url']

                       
                        # if GreenBillUser.objects.filter(mobile_no = '7020598727' ):
                        #    customer_bill_url = "http://157.230.228.250/vyasji_bill/" + str(bill_url) + "/"
                
                        # else:  
                            # print("bill_url")
                        customer_bill_url = "http://157.230.228.250/my-green-bill/" + str(bill_url) + "/"

                            # print("_______________________________________")
                            # print(list(is_available))
                        print("isss")
                        if len(list(is_available))>0:

                            print("is_customer")

                            try: 
                                green_points_old = GreenPointsModel.objects.filter(mobile_no=customer_mobile_number).values('green_points_count')[0]['green_points_count']   
                            except:
                                green_points_old = 0

                            green_points_new = int(green_points_old) + int(green_points)

                            GreenPointsModel.objects.update_or_create(mobile_no=customer_mobile_number, defaults={'green_points_count': green_points_new})

                            device = DeviceId.objects.filter(mobile_no=customer_mobile_number).first()

                            print(device)

                            push_service = FCMNotification(api_key=settings.API_KEY)
                            print(push_service)

                            if device != None:

                                CustomerBill.objects.filter(id=customer_bill.id).update(greenbill_digital_bill = True)

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
                                print("***********")
                                print(total_amount_avilable_new,subscription_object.per_digital_bill_cost)
                                return JsonResponse({'status':'success', 'message': 'Notification send successfully'}, status=200)

                            else:
                                # print("_______________________________________")
                                # print(customer_mobile_number)
                                if customer_mobile_number:
                                    # print("_______________________________________")
                                    # print("Inside valid green bill user decive locked ")
                                    s = pyshorteners.Shortener()

                                    short_url = s.tinyurl.short(customer_bill_url)

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
                                                        "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
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
                                    CustomerBill.objects.filter(id=customer_bill.id).update(greenbill_sms_bill = True)
                                    if response.status_code == 200:
                                        s = pyshorteners.Shortener()

                                        short_url = s.tinyurl.short(customer_bill_url)

                                        total_amount_avilable_new = 0
                                        total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
                                        subscription_object.total_amount_avilable = total_amount_avilable_new
                                        subscription_object.save()
                                        print("()@*@)")
                                        print(total_amount_avilable_new,subscription_object.per_bill_cost)
                                        return JsonResponse({'status':'success', 'message': 'SMS sent successfully'}, status=200)
                                    else:
                                        return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                                else:
                                    return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                        else:
                            print("_______________________________________")
                            print(customer_mobile_number)
                            if customer_mobile_number:
                                s = pyshorteners.Shortener()

                                short_url = s.tinyurl.short(customer_bill_url)
                                print("inside")
                                total_amount_avilable_new = 0
                                if subscription_object_for_link.per_url_cost == None:
                                    return JsonResponse({'status':'url plan is not purchases'}, status=400)
                                print(subscription_object_for_link.per_url_cost)
                                print("#$$")
                                total_amount_avilable_new = float(subscription_object_for_link.total_amount_avilable) - float(subscription_object_for_link.per_url_cost)
                                print("#$$")
                                subscription_object_for_link.total_amount_avilable = total_amount_avilable_new
                                subscription_object_for_link.save()
                                print("***********")
                                print(total_amount_avilable_new,subscription_object_for_link.per_url_cost)
                                return JsonResponse({'status':'success', 'url': short_url}, status=200)
                            
                    else:
                        return JsonResponse({'status':'error', 'message': "You don't have Sufficient Available Amount !!!"}, status=400)
                else:
                    return JsonResponse({'status':'error', 'message': "You don't have any active subscription plan !!!"}, status=400)
            else:
                return JsonResponse({'status':'error', 'message': "Merchant could not be Found !!!"}, status=400)

        return HttpResponse("Data Saved Successfully ")
    except :
        return HttpResponse("Problem Saving Data ")


def my_green_bill(request,id):
    print("IIIIIIIIIIII")
    try:
        # print("in try")
        print(id)
        bill_habrone_details = CustomerBill.objects.get(bill_url=id)
      

        print(bill_habrone_details)
        merchant_user_id = bill_habrone_details.user_id

        print(type(merchant_user_id))

        # merchant_mobile_number = bill_habrone_details.mobile_no

        user_id = GreenBillUser.objects.get(mobile_no = merchant_user_id)
        print("*************************************")
        print(id,merchant_user_id,user_id)

       
        form1 = MerchantProfile.objects.filter(m_user = user_id)

        # print(form1)
        # print("form done")
        for i in list(form1) :
            # print(type(i.m_business_category.business_category_name),i.m_business_category.business_category_name)
            if i.m_business_category.business_category_name == "Parking Lot":
                # print("In 1")
                pass
            elif i.m_business_category.business_category_name =="Petrol Pump":
                # print("In 2")
                pass
            else:
                # print("In 3")
                form = i
        # print("IIIIIIIIIIIIIII")
        # print(form)
        try:
            bill_design = bill_designs.objects.get(merchant_business_id = form)
        except:
            bill_design = ''

        print(bill_design)
        try:
            merchant_business_object = MerchantProfile.objects.get(id = form)

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

        print("bussiness logo")
        print(business_logo)

        ads_image_details = ""


        space = ads_below_bill.objects.filter(merchant = form.m_user, merchant_business_id = form, ads_type='green_bill').last()

        print(space)
        today = datetime.strptime(str(date.today()), '%Y-%m-%d')

        green_bills_advertisement = ""

        try:
            if space:
                expiry_date_new = datetime.strptime(space.end_date, '%Y-%m-%d')
                start_date_new = datetime.strptime(space.start_date, '%Y-%m-%d')

                if today >= start_date_new and today <= expiry_date_new:

                    startswith = str(bill_details.business_name.id) + ','
                    endswith = ','+ str(bill_details.business_name.id)
                    contains = ','+ str(bill_details.business_name.id) + ','
                    exact = str(bill_details.business_name.id)

                    green_bill_merchant_ads = ads_for_green_bills.objects.filter(
                        Q(business_name_value__startswith = startswith) | 
                        Q(business_name_value__endswith = endswith) | 
                        Q(business_name_value__contains = contains) | 
                        Q(business_name_value__exact = exact)
                    ).last()

                    if green_bill_merchant_ads:

                        start_date = datetime.strptime(green_bill_merchant_ads.start_date, '%Y-%m-%d')
                        end_date = datetime.strptime(green_bill_merchant_ads.end_date, '%Y-%m-%d')

                        if today >= start_date and today <= end_date:
                            ads_image_details = ads_for_green_bills.objects.get(id = green_bill_merchant_ads.id)
                            green_bills_advertisement = True
                            views = ads_below_bill.objects.get(id=space.id)
                            views.count = views.count + 1
                            views.save()

                            views = ads_for_green_bills.objects.get(id=green_bill_merchant_ads.id)
                            views.count = views.count + 1
                            views.save()

            if not green_bills_advertisement:
                third_party_status = ads_below_bill.objects.filter(merchant = form.m_user, merchant_business_id = form, ads_type='third_party', status = 1).last()
                if third_party_status:
                    expiry_date_new =  datetime.strptime(third_party_status.end_date, '%Y-%m-%d')
                    start_date_new =  datetime.strptime(third_party_status.start_date, '%Y-%m-%d')

                    if today <= expiry_date_new and today >= start_date_new:
                        ads_image_details = ads_below_bill.objects.get(id = third_party_status.id)
                        green_bills_advertisement = True
                        views = ads_below_bill.objects.get(id=third_party_status.id)
                        views.count = views.count + 1
                        views.save()

            if not green_bills_advertisement:
                ads_details = ads_below_bill.objects.filter(merchant = form.m_user, merchant_business_id = form, active_ads = True).last()
                if ads_details:
                    ads_image_details = ads_below_bill.objects.get(id = ads_details.id)
                    green_bills_advertisement = True
                    views = ads_below_bill.objects.get(id=ads_details.id)
                    views.count = views.count + 1
                    views.save()
        except:
            ads_image_details = ""

        print("YYYYY")
        business_logo = form.m_business_logo

        s = bill_habrone_details.item_details
        print(s)
        f = s.replace("]", "")
        print(type(f))
        we = eval(s)
        print(eval(s))
        print(type(we))
        
        print(we[0])
        print(type(we[0]))
        context = {
            'bill_design':bill_design,
            'business_logo': business_logo,
            'business_address':business_address,
            'ads_image_details':ads_image_details,
            # 'template_selected': selected_template,
            'receipt_details' : bill_habrone_details,
            'bill_record': we,
            # 'stamp_uploaded_image': stamp_uploaded_image,
            # 'memo_record': memo_record, 
            # 'sign': sign,
            'form': form,
        }

        print("context done")

        if merchant_user_id == '7020598727':
            return render(request, "merchant/bill_design/vyasj-billi.html",context)

        else:
            return render(request, "partner/customer_bill/bill_from_habrone.html",context)

    except:
        print("in expecr")
        return render(request, 'page-404.html')


import ast
@csrf_exempt
def testingHebroneSendBill(request):
    print("********yyyy")

    try:
        print("in try")
        if request.method=='POST':
            print("In post")
            # print("In method")
            # print(request.body)
            received_json_data = json.loads(request.body.decode("utf-8"))
            # print("###########")
            # print(received_json_data)
            merchant_mobile_number = str(received_json_data["merchant_mobile_number"])
            customer_mobile_number = str(received_json_data["customer_mobile_number"])
            invoice_number = str(received_json_data['invoice_number'])
            bill_date = str(received_json_data['bill_date'])
            bill_gross_amount = str(received_json_data['bill_gross_amount'])
            bill_discount = str(received_json_data['bill_discount'])
            bill_amount = str(received_json_data['bill_amount'])
            customer_name =  str(received_json_data['customer_name'])
            item_details = received_json_data['Item_details']
            is_merchant = str(GreenBillUser.objects.filter(mobile_no = merchant_mobile_number))

            partner_number = "8308014241"

            partner_id = GreenBillUser.objects.get(mobile_no = "8308014241")
            print("*********************")
            print(partner_id)
            print(type(item_details))
            if is_merchant:

                try:
                    subscription_object = partner_subscriptions.objects.get(partner_id = partner_id, is_active = True)
                except:
                    subscription_object = ""

                if 1==1:
                    # print("_______________________________________")
                    # print(subscription_object.total_amount_avilable)
                    # print(subscription_object.per_bill_cost)

                    # if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):
                    if 1==1:
                        user_id = GreenBillUser.objects.get(mobile_no = merchant_mobile_number)

                        merchant_business_object = MerchantProfile.objects.filter(m_user = user_id).last()

                        business_category_name = merchant_business_object.m_business_category.business_category_name
                        

                        bill_category_id = bill_category.objects.filter(bill_category_name = business_category_name).values('id')[0]['id']
                        
                        if bill_category_id:
                            bill_category_object = bill_category.objects.get(id = bill_category_id)
                        else:
                            bill_category_object = ""

                        green_points_settings_object = GreenPointsSettings.objects.get(id = 1)

                        green_points = green_points_settings_object.bill_points

                        is_available = GreenBillUser.objects.filter(mobile_no = customer_mobile_number)
                        print("_______________________________________")
                        print(list(is_available))

                        customer_bill = CustomerBill.objects.create(user_id = user_id, mobile_no = customer_mobile_number, is_hebrone = True,
                                        email = user_id.m_email, green_points_earned = str(green_points), business_name = merchant_business_object,
                                        invoice_no = invoice_number, bill_amount = bill_amount, customer_bill_category = bill_category_object,
                                        bill_gross_amount = bill_gross_amount, bill_discount= bill_discount, customer_name = customer_name,
                                        item_details = item_details,bill_date = bill_date,
                                    )
                        history_result1 = sent_bill_history.objects.create(subscription_id = subscription_object.id, user_id = user_id,
                                mobile_no = customer_mobile_number, m_business_id = merchant_business_object.id, bill_amount = bill_amount,
                                customer_bill = True
                            )
                        # print("Saved !!1")
                        letters = string.ascii_letters
                        digit = string.digits
                        random_string = str(customer_bill.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                        # print("random_string")
                        customer_bill_new = CustomerBill.objects.filter(id=customer_bill.id).update(bill_url = random_string)
                        # print("customer_bill_new")
                        bill_url = CustomerBill.objects.filter(id=customer_bill.id).values('bill_url')[0]['bill_url']

                        # print("bill_url")
                        customer_bill_url = "http://157.230.228.250/my-green-bill/" + str(bill_url) + "/"

                        print("_____________________eeeeeeeeeeeeeeeeeeegrg__________________")
                        print(bill_url)

                        if len(list(is_available))>0:

                            print("is_customer")

                            try: 
                                green_points_old = GreenPointsModel.objects.filter(mobile_no=customer_mobile_number).values('green_points_count')[0]['green_points_count']   
                            except:
                                green_points_old = 0

                            green_points_new = int(green_points_old) + int(green_points)

                            GreenPointsModel.objects.update_or_create(mobile_no=customer_mobile_number, defaults={'green_points_count': green_points_new})

                            device = DeviceId.objects.filter(mobile_no=customer_mobile_number).first()

                            push_service = FCMNotification(api_key=settings.API_KEY)

                            if device != None:

                                CustomerBill.objects.filter(id=customer_bill.id).update(greenbill_digital_bill = True)

                                try:
                                    registration_id = device.device_id
                                except:
                                    registration_id = ''

                                message_title = "New Bill"

                                message_body = "Hey Green Bill user, view and download your bill here. " + str(customer_bill_url)

                                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

                                # total_amount_avilable_new = 0
                                # total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_digital_bill_cost)
                                # subscription_object.total_amount_avilable = total_amount_avilable_new
                                # subscription_object.save()

                                return JsonResponse({'status':'success', 'message': 'Notification send successfully'}, status=200)

                            else:
                                print("_______________rr________________________")
                                print(customer_mobile_number)
                                if customer_mobile_number:
                                    print("_______________________________________")
                                    print("Inside valid green bill user decive locked ")
                                    s = pyshorteners.Shortener()
                                    print("**rrrwqqs*")
                                    short_url = s.tinyurl.short(customer_bill_url)
                                    print("**rrrss*")
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
                                                        "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
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

                                    print("**rrr*")
                                    response = requests.post(url, json = data_temp)
                                    print("***")
                                    if response.status_code == 200:
                                        # total_amount_avilable_new = 0
                                        # total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
                                        # subscription_object.total_amount_avilable = total_amount_avilable_new
                                        # subscription_object.save()
                                        return JsonResponse({'status':'success', 'message': 'SMS sent successfully'}, status=200)
                                    else:
                                        return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                                else:
                                    return JsonResponse({'status':'error',  'message': "Failed to send SMS. Please send valid Mobile No."}, status=403)
                        else:
                            # print("_______________________________________")
                            # print(customer_mobile_number)
                            if customer_mobile_number:
                                s = pyshorteners.Shortener()
                                short_url = s.tinyurl.short(customer_bill_url)
                                return JsonResponse({'status':'success', 'url': short_url}, status=200)
                            
                    else:
                        return JsonResponse({'status':'error', 'message': "You don't have Sufficient Available Amount !!!"}, status=400)
                else:
                    return JsonResponse({'status':'error', 'message': "You don't have any active subscription plan !!!"}, status=400)
            else:
                return JsonResponse({'status':'error', 'message': "Merchant could not be Found !!!"}, status=400)

        return HttpResponse("Data Saved Successfully ")
    except :
        return HttpResponse("Problem Saving Data ")

   






def getPartnerActiveSubscriptionPlanSoftware(request, partner_id):

    subscription_object = ""

    if partner_id:
        
        try:
            subscription_object = partner_subscriptions.objects.get(partner_id = partner_id, is_active = True)

            return subscription_object

        except:
            return subscription_object
    else:
        return subscription_object

@csrf_exempt
def check_status_subscription_availlabilty(request):
    business_id = request.POST['m_business_id']
    subscription_object = ""

    if business_id:
        startswith = str(business_id) + ','
        endswith = ','+ str(business_id)
        contains = ','+ str(business_id) + ','
        exact = str(business_id)
        
        try:
            subscription = merchant_subscriptions.objects.get(
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )

            subscription_object = 1

        except:
            subscription_object = 0
    else:
        subscription_object = 0

    return JsonResponse({'status': 'success','data':subscription_object}, status=200)


@csrf_exempt
def GetMerchantBusinessIdsByNumber(request):

    mobile_no = request.POST['merchant_mobile_no']

    user_id = GreenBillUser.objects.get(mobile_no = mobile_no)

    merchant_data = []

    if user_id:

        if user_id.is_merchant:

            merchant_user_object = MerchantProfile.objects.filter(m_user = user_id)

            for merchant_obj in merchant_user_object:

                merchant_data.append({
                        'm_unique_id': merchant_obj.m_unique_id,
                        'business_name': merchant_obj.m_business_name,
                    })

            return JsonResponse({'status': 'success', 'merchant_data': merchant_data}, status=200)

        else:

            return JsonResponse({'status':'error', 'message': "Merchant could not be Found !!!"}, status=400)

    else:
        return JsonResponse({'status':'error', 'message': "Number could not be Found !!!"}, status=400)





 
