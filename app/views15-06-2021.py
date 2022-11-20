# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

import os
import random
import sweetify
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from role.models import permission, userrole, module
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
from .models import emailSetting, generalSetting
from django.contrib.auth.forms import SetPasswordForm
from users.models import GreenBillUser, UserProfileImage
from authentication.models import otp_validation
from category_and_tags.models import business_category

 
import random

import json
import os
from io import BytesIO
from django.shortcuts import render
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse

#for customer index
from users.models import MerchantProfile
from category_and_tags.models import bill_category, bill_tags
import datetime
from green_points.models import GreenPointsModel
from merchant_software_apis.models import CustomerBill, MerchantBill
from customer_bill.forms import Customer_Bill_Form
from users.models import MerchantProfile, Merchant_users
from parking_lot_apis.models import *
from coupon.models import CouponModel
from django.utils import timezone
from merchant_setting.models import *
from datetime import datetime
from django.utils import formats
from petrol_pump_apis.models import *
from datetime import date
import filetype
from django.db.models import Q

import random
import string

# SMS
import requests
import time
import pyshorteners

from my_subscription.models import sent_bill_history, merchant_subscriptions

from bill_design.models import bill_designs

from my_subscription.models import *

from payments.models import *

from partner_my_subscription.models import *

def is_merchant_or_merchant_staff(user):
    try:
        return user.is_authenticated and (user.is_merchant is True or user.is_merchant_staff is True)
    except is_merchant.DoesNotExist:
        return False

def is_partner(user):
    try:
        return user.is_authenticated and (user.is_partner is True)
    except is_partner.DoesNotExist:
        return False

def is_customer(user):
    try:
        return user.is_authenticated and (user.is_customer is True)
    except is_customer.DoesNotExist:
        return False

def is_owner(user):
    try:
        return user.is_authenticated and (user.is_staff is True)
    except is_staff.DoesNotExist:
        return False

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def index(request):
    context = {}
    context['segment'] = 'index'
    context['DashboardNavclass'] = 'active'
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def index12(request):
    context = {}

    context['total_merchants'] = GreenBillUser.objects.filter(is_merchant = True).count()
    context['total_customers'] = GreenBillUser.objects.filter(is_customer = True).count()
    context['total_partners'] = GreenBillUser.objects.filter(is_partner = True).count()

    total_payments = 0

    recharge_amount_history = recharge_history.objects.all()
    for recharge in recharge_amount_history:
        total_payments = total_payments + float(recharge.cost)

    payment_links = OwnerPaymentLinks.objects.all()
    for link in payment_links:
        total_payments = total_payments + float(link.amount)

    partner_recharge_amount_history = partner_recharge_history.objects.all()
    for recharge in partner_recharge_amount_history:
        total_payments = total_payments + float(recharge.cost)

    context['total_payments'] = total_payments

    context['segment'] = 'index'
    context['DashboardNavclass'] = 'active'
    html_template = loader.get_template( 'index12.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_index(request):
    # context = {} 
    # context['segment'] = 'index'
    # context['DashboardNavclass'] = 'active'
    # html_template = loader.get_template('merchant-index.html')
    context = {}

    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_users_object.merchant_user_id

    merchant_business = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

    merchant_business_id = merchant_business.id

    merchant_user = []

    merchant_user.append({
        'user_id': merchant_object
    })

    merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = merchant_business_id)

    for user in merchant_user_temp:
        merchant_user.append({
            'user_id': user.user_id
            })

    context['merchant_users'] = merchant_user

    # merchant_business.m_business_category.id = 11

    if merchant_business.m_business_category.id == 12:


        # Parking Dashboard ==>>

        parking_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__date = timezone.now(), is_pass = False).all()
        # parking_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id).all()

        total_bills = 0
        total_collection = 0
        total_flagged = 0

        for bill in parking_bills:
            total_bills += 1
            total_collection = total_collection + float(bill.amount)

            if bill.bill_flag == True:
                total_flagged = total_flagged + 1

        parking_pass = ParkingLotPass.objects.filter(m_business_id = merchant_business.id, created_at__date = timezone.now()).all()

        total_pass_collection = 0
        total_pass = 0

        for pass_temp in parking_pass:
            total_pass_collection = total_pass_collection + float(pass_temp.amount)
            total_pass = total_pass + 1

        context['total_bills'] = total_bills
        context['total_collection'] = total_collection + total_pass_collection
        context['total_flagged'] = total_flagged

        merchant_user_details = []

        # if request.method == "POST":
        if request.POST.get('submit') == 'user_collection_btn':

            custom_user = request.POST['user']
            from_date = request.POST['from_date']
            from_date_temp = from_date
            to_date = request.POST['to_date']
            to_date_temp = to_date

            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')

            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%d-%m-%Y')

            for user in merchant_user:

                total_collection_bill = 0
                total_flagged = 0

                total_hours = ""

                parking_logs = ParkingLog.objects.filter(user_id = user['user_id'].id, created_at__date = timezone.now())

                if parking_logs:
                    login_at = parking_logs[0].login_at
                    logout_at = parking_logs[0].logout_at
                    # total_hours = logout_at - login_at
                else:
                    login_at = ""
                    logout_at = ""
                    total_hours = ""
                   
                bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, user_id = user['user_id'].id, is_pass = False).all()

                new_bills = []

                for bill in bills:
                    # print(bill.date)
                    # print(from_date)
                    if custom_user and from_date and to_date:
                        if bill.m_user_id == custom_user:
                            if bill.date >= from_date and bill.date <= to_date:
                                new_bills.append(bill)

                    elif from_date and to_date:
                        if bill.date >= from_date and bill.date <= to_date:
                            new_bills.append(bill)

                    elif custom_user and from_date:
                        if bill.m_user_id == custom_user and bill.date >= from_date:
                            new_bills.append(bill)

                    elif custom_user and to_date:
                        if bill.m_user_id == custom_user and bill.date <= to_date:
                            new_bills.append(bill)

                    elif from_date:
                        if bill.date >= from_date:
                            new_bills.append(bill)

                    elif to_date:
                        if bill.date <= to_date:
                            new_bills.append(bill)

                    elif custom_user:
                        if bill.m_user_id == custom_user:
                            new_bills.append(bill)

                total_bills = 0

                for bill in new_bills:

                    total_bills += 1

                    total_collection_bill = total_collection_bill + float(bill.amount)

                    if bill.bill_flag == True and bill.flag_by == str(user['user_id'].id):
                        total_flagged = total_flagged + 1

                name = user['user_id'].first_name + ' ' + user['user_id'].last_name


                parking_pass = ParkingLotPass.objects.filter(m_business_id = merchant_business.id, user_id = user['user_id'].id).all()

                new_pass = []

                for pass_temp in parking_pass:
                    pass_date = datetime.strptime(str(pass_temp.created_at.date()), '%Y-%m-%d').strftime('%d-%m-%Y')
                    if custom_user and from_date and to_date:
                        if pass_temp.user_id == custom_user:
                            if pass_date >= from_date and pass_date <= to_date:
                                new_pass.append(pass_temp)

                    elif from_date and to_date:
                        if pass_date >= from_date and pass_date <= to_date:
                            new_pass.append(pass_temp)

                    elif custom_user and from_date:
                        if pass_date == custom_user and pass_date >= from_date:
                            new_pass.append(pass_temp)

                    elif custom_user and to_date:
                        if pass_date == custom_user and pass_date <= to_date:
                            new_pass.append(pass_temp)

                    elif from_date:
                        if pass_date >= from_date:
                            new_pass.append(pass_temp)

                    elif to_date:
                        if pass_date <= to_date:
                            new_pass.append(pass_temp)

                    elif custom_user:
                        if pass_temp.m_user_id == custom_user:
                            new_pass.append(pass_temp)

                total_pass_collection = 0
                total_pass = 0
                
                for pass_temp in new_pass:
                    total_pass_collection = total_pass_collection + float(pass_temp.amount)
                    total_pass = total_pass + 1

                if custom_user:
                    if int(user['user_id'].id) == int(custom_user):
                        merchant_user_details.append({
                            'name': name,
                            'total_bills': total_bills,
                            'total_collection_bill': total_collection_bill,
                            'login_at': login_at,
                            'logout_at': logout_at,
                            'total_flagged': total_flagged,
                            'total_hours' : total_hours,
                            'total_pass_colletion': total_pass_collection,
                            'total_pass' : total_pass,
                            'total_collection': total_collection_bill + total_pass_collection
                        })
                else:
                    merchant_user_details.append({
                        'name': name,
                        'total_bills': total_bills,
                        'total_collection_bill': total_collection_bill,
                        'login_at': login_at,
                        'logout_at': logout_at,
                        'total_flagged': total_flagged,
                        'total_hours' : total_hours,
                        'total_pass_colletion': total_pass_collection,
                        'total_pass' : total_pass,
                        'total_collection': total_collection_bill + total_pass_collection
                    })

                if custom_user:
                    context['custom_user'] = int(custom_user)
                context['from_date'] = from_date_temp
                context['to_date'] = to_date_temp

        else:

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


                merchant_user_details.append({
                    'name': name,
                    'total_bills': total_bills,
                    'total_collection_bill': total_collection_bill,
                    'login_at': login_at,
                    'logout_at': logout_at,
                    'total_flagged': total_flagged,
                    'total_hours' : total_hours,
                    'total_pass_colletion': total_pass_collection,
                    'total_pass' : total_pass,
                    'total_collection': total_collection_bill + total_pass_collection
                })
                    
        context['merchant_user_details'] = merchant_user_details

        today = date.today()
        current_year = today.year
        next_year = today.year + 1
        if request.POST.get('submit') == 'bills_collection_btn':
            from_date_temp = request.POST["from_date1"]
            to_date_temp = request.POST["to_date1"]

            vehicles = MerchantParkingAddVehicle.objects.filter(m_business_id = merchant_business_id).all()
            for vehicle in vehicles:

                vehiclestatusChart = []
                month3 = []
                year3 = []
                for i in range(4,13):
                    if i < 10:
                        m1 = "0" + str(i)
                        month3.append(m1) 
                    else:
                        month3.append(i)
                for j in range(1,4):
                    if j < 10:
                        m2 = "0" + str(j)
                        month3.append(m2)

                for month in month3:
                    
                    petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, vehicle_type = vehicle.vehicle_type, created_at__lte = to_date_temp, created_at__gte = from_date_temp,created_at__month = month).all()
                    print('petrol_bills',petrol_bills)
                    total_collection = 0

                    for bill in petrol_bills:
                        total_collection = total_collection + float(bill.amount)

                    vehiclestatusChart.append(total_collection)

                vehiclestatusChart_list = ','.join(map(str, vehiclestatusChart))
                vehicle.vehiclestatusChart_list = vehiclestatusChart_list                   

        else:
            today = date.today()
            vehicles = MerchantParkingAddVehicle.objects.filter(m_business_id = merchant_business_id).all()

            for vehicle in vehicles:

                vehiclestatusChart = []
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
                    
                    petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, vehicle_type = vehicle.vehicle_type, created_at__year = year, created_at__month = month).all()
                    total_collection = 0

                    for bill in petrol_bills:
                        total_collection = total_collection + float(bill.amount)

                    vehiclestatusChart.append(total_collection)

                vehiclestatusChart_list = ','.join(map(str, vehiclestatusChart))
                vehicle.vehiclestatusChart_list = vehiclestatusChart_list

        context['vehiclestatusChart_list'] = vehicles
        context['current_year'] = current_year
        context['next_year'] = next_year

        m_business_id = merchant_business_id
       
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
                "total_bills_made": total_bills_made
            })

        context['space_data'] = actual_space_data

        today = date.today()

        dailybillsChart = []
        dailyTotalCollectionChart = []

        start_date = str(today) + " 00:00:01"
        end_date = str(today) + " 04:00:00"
        petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 04:00:01"
        end_date = str(today) + " 08:00:00"
        petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 08:00:01"
        end_date = str(today) + " 12:00:00"
        petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 12:00:01"
        end_date = str(today) + " 16:00:00"
        petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 16:00:01"
        end_date = str(today) + " 20:00:00"
        petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 20:00:01"
        end_date = str(today) + " 23:59:59"
        petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.amount)
        dailyTotalCollectionChart.append(total_collection)

        dailybillsChart_list = ','.join(map(str, dailybillsChart))
        context['dailybillsChart_list'] = dailybillsChart_list

        dailyTotalCollectionChart_list = ','.join(map(str, dailyTotalCollectionChart))
        context['dailyTotalCollectionChart_list'] = dailyTotalCollectionChart_list

        vehicles = MerchantParkingAddVehicle.objects.filter(m_business_id = merchant_business_id).all()

        for vehicle in vehicles:

            vehiclestatusChart = []

            for i in range(1,13):
                year = today.year

                if i < 10:
                    month = "0" + str(i)

                petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, vehicle_type = vehicle.vehicle_type, created_at__year = year, created_at__month = month).all()
                
                total_collection = 0

                for bill in petrol_bills:
                    total_collection = total_collection + float(bill.amount)
                # print(total_collection)

                vehiclestatusChart.append(total_collection)

            vehiclestatusChart_list = ','.join(map(str, vehiclestatusChart))

            vehicle.vehiclestatusChart_list = vehiclestatusChart_list

        context['vehiclestatusChart_list'] = vehicles

        productwiseCollectionchart_labels_temp = []
        productwiseCollectionchart_data_temp = []

        productWiseBillsdoughnutChart_labels_temp = []
        productWiseBillsdoughnutChart_data_temp = []

        for space in actual_space_data:
            vehicle_type_temp = "'" + space["vehicle_type"] + "'"
            productwiseCollectionchart_labels_temp.append(vehicle_type_temp)
            productwiseCollectionchart_data_temp.append(round(space['total_bills_made'],2))
            productWiseBillsdoughnutChart_labels_temp.append(vehicle_type_temp)
            productWiseBillsdoughnutChart_data_temp.append(space['vehicle_parked_count'])

        context['productwiseCollectionchart_labels'] = ','.join(map(str, productwiseCollectionchart_labels_temp))
        context['productwiseCollectionchart_data'] = ','.join(map(str, productwiseCollectionchart_data_temp))
        context['productWiseBillsdoughnutChart_labels'] = ','.join(map(str, productWiseBillsdoughnutChart_labels_temp))
        context['productWiseBillsdoughnutChart_data'] = ','.join(map(str, productWiseBillsdoughnutChart_data_temp))
        

    elif merchant_business.m_business_category.id == 11:
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__date = timezone.now()).all()
        # parking_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id).all()

        total_bills = 0
        total_collection = 0
        total_flagged = 0

        for bill in petrol_bills:
            total_bills += 1
            total_collection = total_collection + float(bill.total_amount)

            if bill.bill_flag == True:
                total_flagged = total_flagged + 1

        context['total_bills'] = total_bills
        context['total_collection'] = total_collection
        context['total_flagged'] = total_flagged

        merchant_user_details = []

        # if request.method == "POST":
        if request.POST.get('submit') == 'user_collection_petrol_pump':
            custom_user = request.POST['user']
            from_date = request.POST['from_date']
            from_date_temp = from_date
            to_date = request.POST['to_date']
            to_date_temp = to_date

            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')

            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%d-%m-%Y')

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
                   
                bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, user_id = user['user_id'].id).all()

                new_bills = []

                for bill in bills:
                    # print(bill.date)
                    # print(from_date)
                    if custom_user and from_date and to_date:
                        if bill.m_user_id == custom_user:
                            if bill.date >= from_date and bill.date <= to_date:
                                new_bills.append(bill)

                    elif from_date and to_date:
                        if bill.date >= from_date and bill.date <= to_date:
                            new_bills.append(bill)

                    elif custom_user and from_date:
                        if bill.m_user_id == custom_user and bill.date >= from_date:
                            new_bills.append(bill)

                    elif custom_user and to_date:
                        if bill.m_user_id == custom_user and bill.date <= to_date:
                            new_bills.append(bill)

                    elif from_date:
                        if bill.date >= from_date:
                            new_bills.append(bill)

                    elif to_date:
                        if bill.date <= to_date:
                            new_bills.append(bill)

                    elif custom_user:
                        if bill.m_user_id == custom_user:
                            new_bills.append(bill)

                    

                total_bills = 0

                for bill in new_bills:

                    total_bills += 1

                    total_collection = total_collection + float(bill.total_amount)

                    if bill.bill_flag == True and bill.flag_by == str(user['user_id'].id):
                        total_flagged = total_flagged + 1

                name = user['user_id'].first_name + ' ' + user['user_id'].last_name

                if custom_user:
                    if int(user['user_id'].id) == int(custom_user):
                        merchant_user_details.append({
                            'name': name,
                            'total_bills': total_bills,
                            'total_collection': total_collection,
                            'login_at': login_at,
                            'logout_at': logout_at,
                            'total_flagged': total_flagged,
                        })
                else:
                    merchant_user_details.append({
                        'name': name,
                        'total_bills': total_bills,
                        'total_collection': total_collection,
                        'login_at': login_at,
                        'logout_at': logout_at,
                        'total_flagged': total_flagged,
                    })
                if custom_user:
                    context['custom_user'] = int(custom_user)
                context['from_date'] = from_date_temp
                context['to_date'] = to_date_temp

        else:

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
                merchant_user_details.append({
                    'name': name,
                    'total_bills': total_bills,
                    'total_collection': total_collection,
                    'login_at': login_at,
                    'logout_at': logout_at,
                    'total_flagged': total_flagged,
                })
                    
        context['merchant_user_details'] = merchant_user_details

        today = date.today()
        current_year = today.year
        next_year = today.year + 1
        if request.POST.get('submit') == 'bills_collection_petrol_pump':
            from_date_temp = request.POST['from_date2']
            to_date_temp = request.POST['to_date2']

            products = MerchantPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

            for product in products:
                productsalesChart = []
                month3 = []
                year3 = []
                for i in range(4,13):
                    # y1 = today.year
                    # year3.append(y1)
                    if i < 10:
                        m1 = "0" + str(i)
                        month3.append(m1) 
                    else:
                        month3.append(i)
                for j in range(1,4):
                    # y2 = today.year + 1
                    # year3.append(y2)
                    if j < 10:
                        m2 = "0" + str(j)
                        month3.append(m2)
                for month in month3:

                    petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, product_id = product.id,created_at__lte = to_date_temp, created_at__gte = from_date_temp, created_at__month = month).all()
                    
                    total_collection = 0.0

                    for bill in petrol_bills:
                        if bill.amount:
                            total_collection = total_collection + float(bill.amount)

                    productsalesChart.append(total_collection)

                productsalesChart_list = ','.join(map(str, productsalesChart))
                product.productsalesChart_list = productsalesChart_list

        else:
            products = MerchantPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

            for product in products:

                productsalesChart = []
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

                    petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, product_id = product.id, created_at__year = year, created_at__month = month).all()
                    
                    total_collection = 0.0

                    for bill in petrol_bills:
                        if bill.amount:
                            total_collection = total_collection + float(bill.amount)

                    productsalesChart.append(total_collection)

                productsalesChart_list = ','.join(map(str, productsalesChart))

                product.productsalesChart_list = productsalesChart_list

        context['productsalesChart_list'] = products
        context['current_year'] = current_year
        context['next_year'] = next_year


        products = MerchantPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

        productSaledoughnutChart_data_temp = []
        productSaledoughnutChart_labels_temp = []

        for product in products:
            petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, product_id = product.id, created_at__date = timezone.now()).all()
            total_liter = 0
            total_amount = 0

            for bill in petrol_bills:
                total_liter = total_liter + float(bill.volume)
                total_amount = total_amount + float(bill.amount)


            product.total_liter_sold = total_liter
            product.total_amount_colleted = total_amount

            product_name_temp = "'" + product.product_name + "'"

            productSaledoughnutChart_labels_temp.append(product_name_temp)

            productSaledoughnutChart_data_temp.append(total_amount)

        context['products'] = products

        context['productSaledoughnutChart_data'] = ','.join(map(str, productSaledoughnutChart_data_temp))
        context['productSaledoughnutChart_labels'] = ','.join(map(str, productSaledoughnutChart_labels_temp))

        addon_products = AddonPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

        addonsSalesdoughnutchart_label_temp = []
        addonsSalesdoughnutchart_data_temp = []

        for addon_product in addon_products:

            petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__date = timezone.now()).all()

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

            product_name_temp = "'" + addon_product.product_name + "'"

            addonsSalesdoughnutchart_label_temp.append(product_name_temp)

            addonsSalesdoughnutchart_data_temp.append(amount_collected)

        context['addon_products'] = addon_products
        context['addonsSalesdoughnutchart_labels'] = ','.join(map(str, addonsSalesdoughnutchart_label_temp))
        context['addonsSalesdoughnutchart_data'] = ','.join(map(str, addonsSalesdoughnutchart_data_temp))

        today = date.today()

        dailybillsChart = []
        dailyTotalCollectionChart = []

        start_date = str(today) + " 00:00:01"
        end_date = str(today) + " 04:00:00"
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.total_amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 04:00:01"
        end_date = str(today) + " 08:00:00"
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.total_amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 08:00:01"
        end_date = str(today) + " 12:00:00"
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.total_amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 12:00:01"
        end_date = str(today) + " 16:00:00"
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.total_amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 16:00:01"
        end_date = str(today) + " 20:00:00"
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.total_amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 20:00:01"
        end_date = str(today) + " 23:59:59"
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.total_amount)
        dailyTotalCollectionChart.append(total_collection)

        dailybillsChart_list = ','.join(map(str, dailybillsChart))
        context['dailybillsChart_list'] = dailybillsChart_list

        dailyTotalCollectionChart_list = ','.join(map(str, dailyTotalCollectionChart))
        context['dailyTotalCollectionChart_list'] = dailyTotalCollectionChart_list

        products = MerchantPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

        for product in products:

            productsalesChart = []

            for i in range(1,13):
                year = today.year

                if i < 10:
                    month = "0" + str(i)

                petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, product_id = product.id, created_at__year = year, created_at__month = month).all()
                
                total_collection = 0.0

                for bill in petrol_bills:
                    if bill.amount:
                        total_collection = total_collection + float(bill.amount)

                productsalesChart.append(total_collection)

            productsalesChart_list = ','.join(map(str, productsalesChart))

            product.productsalesChart_list = productsalesChart_list

        context['productsalesChart_list'] = products

    context['merchant_business_category_id'] = merchant_business.m_business_category.id
    context['segment'] = 'index'
    context['DashboardNavclass'] = 'active'
    # merchant-index-other-business.html
    # print(merchant_business.m_business_category.id)
    if merchant_business.m_business_category.id == 11 or merchant_business.m_business_category.id == 12:
        html_template = loader.get_template('merchant-index.html')
    else:

        total_transaction = 0

        total_transaction1 = CustomerBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), customer_added = False).count()

        total_transaction2 = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now()).count()

        total_transaction = total_transaction1 + total_transaction2

        context['total_transaction'] = total_transaction

        customer_bill = CustomerBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), customer_added = False).order_by('-id')

        merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now()).order_by('-id')

        total_collection = 0

        feedback_bill = []

        for bill in customer_bill:
            total_collection = total_collection + float(bill.bill_amount)

            try:
                bill_design = bill_designs.objects.get(merchant_business_id = bill.business_name.id)
                bill_rating_emoji = bill_design.rating_emoji
            except:
                bill_rating_emoji = "⭐"

            ratings = ""

            if bill.rating:
                for x in range(int(bill.rating)):
                    ratings = " ".join((ratings, bill_rating_emoji))
                
            bill.ratings = ratings

            if bill.feedback_submit == True:
                feedback_bill.append(bill)

        for bill in merchant_bill:
            total_collection = total_collection + float(bill.bill_amount)

            try:
                bill_design = bill_designs.objects.get(merchant_business_id = bill.business_name)
                bill_rating_emoji = bill_design.rating_emoji
            except:
                bill_rating_emoji = "⭐"

            ratings = ""

            if bill.rating:
                for x in range(int(bill.rating)):
                    ratings = " ".join((ratings, bill_rating_emoji))
                
            bill.ratings = ratings

            if bill.feedback_submit == True:
                feedback_bill.append(bill)

        context['feedback_bill'] = feedback_bill

        context['total_collection'] = total_collection

        average_billing = 0

        context['average_billing'] = average_billing

        context['print_transaction'] = sent_bill_history.objects.filter(
            m_business_id = merchant_business.id,
            created_at__date = timezone.now(),
            print_transaction = True
        ).count()

        context['green_bill_transaction'] = sent_bill_history.objects.filter(
            m_business_id = merchant_business.id,
            created_at__date = timezone.now(),
            green_bill_transaction = True
        ).count()

        context['green_bill_print_transaction'] = sent_bill_history.objects.filter(
            m_business_id = merchant_business.id,
            created_at__date = timezone.now(),
            green_bill_print_transaction = True
        ).count()

        context['total_transaction'] = context['green_bill_transaction'] + context['green_bill_print_transaction']

        total_rejected_transaction = 0

        total_rejected_transaction1 = CustomerBill.objects.filter(
            business_name = merchant_business, created_at__date = timezone.now(), reject_status = True, customer_added = False
        ).count()

        total_rejected_transaction2 = MerchantBill.objects.filter(
            business_name = merchant_business, created_at__date = timezone.now(), reject_status = True, customer_added = False
        ).count()

        context['total_rejected_transaction'] = total_rejected_transaction1 + total_rejected_transaction2

        subscription_object = getActiveSubscriptionPlan(request, merchant_business.id)

        context['subscription_object'] = subscription_object

        if subscription_object:
            percentage = ((float(subscription_object.recharge_amount) - float(subscription_object.total_amount_avilable))/subscription_object.recharge_amount) * 100
            remaining_subscription_percentage = 100 - percentage
            context['remaining_subscription_percentage'] = remaining_subscription_percentage

        html_template = loader.get_template('merchant-index-other-business.html')

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def customer_index_add_bill(request):
    if request.method == "POST":
        bill_form = Customer_Bill_Form(request.POST, request.FILES)
        
        bill_file = request.FILES['cust_bill']

        try:
         merchant_name = request.POST['business_name']
        except:
            merchant_name = ''

        if merchant_name:
            merchant_object = MerchantProfile.objects.get(id=merchant_name)

        cust_category = request.POST['customer_bill_category']

        if cust_category:
            bill_category_object = bill_category.objects.get(id=cust_category)

        bill_amt = request.POST['bill_amount']
        date = request.POST['bill_date']
        bill_tags_value = request.POST['bill_tags_value']
        
        remarks = request.POST['remarks']
        custom_business = request.POST['custom_business']

        if merchant_name and cust_category:
            bill_data = CustomerBill.objects.create(
                mobile_no=request.user.mobile_no,
                bill=bill_file,
                business_name=merchant_object,
                customer_bill_category=bill_category_object,
                bill_amount=bill_amt,
                bill_date=date,
                customer_added = True,
                bill_tags = bill_tags_value,
                remarks = remarks,
                custom_business_name = custom_business
            )
            sweetify.success(request, title="Success", icon="success",
                                text="Bill Saved Successfully", timer=1500)
            
            
        elif merchant_name: 
            bill_data = CustomerBill.objects.create(
                mobile_no=request.user.mobile_no,
                bill= bill_file,
                business_name=merchant_object,
                bill_amount=bill_amt,
                bill_date=date,
                customer_added = True,
                bill_tags = bill_tags_value,
                remarks = remarks,
                custom_business_name = custom_business
            )

            sweetify.success(request, title="Success", icon="success",
                                text="Bill Saved Successfully", timer=1500)
            
        elif cust_category:
            bill_data = CustomerBill.objects.create(
                mobile_no=request.user.mobile_no,
                bill=bill_file,
                customer_bill_category=bill_category_object,
                bill_amount=bill_amt,
                bill_date=date,
                customer_added = True,
                bill_tags = bill_tags_value,
                remarks = remarks,
                custom_business_name = custom_business
            )

            sweetify.success(request, title="Success", icon="success",
                                text="Bill Saved Successfully", timer=1500)
            
        else:
            bill_data = CustomerBill.objects.create(
                mobile_no=request.user.mobile_no,
                bill=bill_file,
                bill_amount=bill_amt,
                bill_date=date,
                customer_added = True,
                bill_tags = bill_tags_value,
                remarks = remarks,
                custom_business_name = custom_business
            )

            sweetify.success(request, title="Success", icon="success", text="Bill Saved Successfully", timer=1500)

        # print(bill_data)

        letters = string.ascii_letters
        digit = string.digits
        random_string = str(bill_data.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

        CustomerBill.objects.filter(id = bill_data.id).update(bill_url = random_string)

        return redirect("/customer-index/")

# @login_required(login_url="/customer-login/")
# @user_passes_test(is_customer, login_url="/customer-login/")
# def customer_index1(request):
#     #shopping Category data

#     labels = []
#     data = []

#     queryset = CustomerBill.objects.filter(mobile_no=request.user)
  
#     # date in yyyy/mm/dd format 
#     # d1 = datetime.date(2020, 1, 3)
#     # d2 = datetime.date(2021, 1, 30) 

#     for bills in queryset:
#         if bills.customer_bill_category:
#             if bills.customer_bill_category.bill_category_name in labels:
#                 print("available")
#             else:
#                 labels.append(bills.customer_bill_category.bill_category_name)

#     spend_by_bill_category = {new_list: 0 for new_list in labels} 

#     customer_bills = CustomerBill.objects.filter(mobile_no=request.user)

#     for oject in customer_bills:
#         for x in labels:
#             if oject.customer_bill_category:
#                 if oject.customer_bill_category.bill_category_name == x:
#                     spend_by_bill_category[x] =  spend_by_bill_category[x] + oject.bill_amount

#     for object in spend_by_bill_category:
#         data.append(spend_by_bill_category[object])

#     context = {
#             "ShoppingAnalysisNavclass": "active",
#             "ShoppingAnalysisCollapseShow": "show",
#             "ShoppingAnalysisCategoryNavclass": "active"
#     }

#     context['from_date'] = ""
#     context['to_date'] = ""

#     context['data'] = data
#     context['labels'] = labels
    


#     #merchant function
    
#     labels1 = []
#     data1 = []

#     queryset1 = CustomerBill.objects.filter(mobile_no=request.user)
  
#     # date in yyyy/mm/dd format 
#     # d1 = datetime.date(2020, 1, 3)
#     # d2 = datetime.date(2021, 1, 30) 

#     for bills1 in queryset1:
#         if bills1.business_name:
#             if bills1.business_name.m_business_name in labels1:
#                 print("available")
#             else:
#                 labels1.append(bills1.business_name.m_business_name)

#     spend_by_bill_business1 = {new_list: 0 for new_list in labels1} 

#     customer_bills1 = CustomerBill.objects.filter(mobile_no=request.user)

#     for oject in customer_bills1:
#         for y in labels1:
#             if oject.business_name:
#                 if oject.business_name.m_business_name == y:
#                     spend_by_bill_business1[y] =  spend_by_bill_business1[y] + oject.bill_amount

#     for object in spend_by_bill_business1:
#         data1.append(spend_by_bill_business1[object])

    
#     context['data1'] = data1
#     context['labels1'] = labels1

#     #form fatching data in the table

#     all_cust_bill = CustomerBill.objects.filter(
#         mobile_no=request.user).order_by('-id')
#     bill_category_name = bill_category.objects.all().order_by('bill_category_name')
#     b_name = MerchantProfile.objects.all()

#     try:
#         GreenPoints = GreenPointsModel.objects.filter(mobile_no=request.user).values('green_points_count')[0]['green_points_count']

#     except:
#         GreenPoints = 0
#     # green_points = GreenPointsModel.objects.all()
#     customer_bill_tags = bill_tags.objects.all().order_by('bill_tags_name')

#     for cust_bill in all_cust_bill:

#         bill_tags1 = cust_bill.bill_tags

#         if cust_bill.bill_tags:
#             bill_tags_list = list(bill_tags1.split(","))

#         else:
#             bill_tags_list = ""

#         bill_tags2 = []
    
#         if bill_tags1:

#             for x in range(len(bill_tags_list)): 

#                 try:

#                     bill_tags1 = bill_tags.objects.get(id=bill_tags_list[x])

#                     bill_tags2.append(bill_tags1.bill_tags_name)

#                 except:

#                     print("hello")

#         bill_tags3 = ', '.join(map(str, bill_tags2))

#         cust_bill.bill_tags_name = bill_tags3

#     from_date_temp  = ""
#     to_date_temp = ""

#     #for date filter
#     if request.method == 'POST':

#         labels = []
#         data = []

#         from_date_temp = request.POST["from_date"]
#         to_date_temp = request.POST["to_date"]

#         from_date = datetime.strptime(request.POST["from_date"], "%Y-%m-%d").date()
#         to_date = datetime.strptime(request.POST["to_date"], "%Y-%m-%d").date()
    
#         for bills in queryset:
#             if bills.bill_date >= from_date and bills.bill_date <= to_date:
#                 if bills.customer_bill_category:
#                     if bills.customer_bill_category.bill_category_name in labels:
#                         print("available")
#                     else:
#                         labels.append(bills.customer_bill_category.bill_category_name)

#         spend_by_bill_category = {new_list: 0 for new_list in labels}

#         customer_bills = CustomerBill.objects.filter(mobile_no=request.user)

#         for oject in customer_bills:
#             if oject.bill_date >= from_date and oject.bill_date <= to_date:
#                 for x in labels:
#                     if oject.customer_bill_category:
#                         if oject.customer_bill_category.bill_category_name == x:
#                             spend_by_bill_category[x] =  spend_by_bill_category[x] + oject.bill_amount

#         for object in spend_by_bill_category:
#             data.append(spend_by_bill_category[object])

#         context['from_date'] = request.POST["from_date"]
#         context['to_date'] = request.POST["to_date"]

#         #for Murchant Date filter
#         labels1 = []
#         data1 = []

#         #from_date = datetime.datetime.strptime(request.POST["from_date"], "%Y-%m-%d").date()
#         #to_date = datetime.datetime.strptime(request.POST["to_date"], "%Y-%m-%d").date()
        
#         for bills1 in queryset1:
#             if bills1.bill_date >= from_date and bills1.bill_date <= to_date:
#                 if bills1.business_name:
#                     if bills1.business_name.m_business_name in labels1:
#                         print("available")
#                     else:
#                         labels1.append(bills1.business_name.m_business_name)

#         spend_by_bill_business1 = {new_list1: 0 for new_list1 in labels1} 

#         customer_bills1 = CustomerBill.objects.filter(mobile_no=request.user)

#         # print(from_date)
#         # print(to_date)

#         for oject1 in customer_bills1:
#             if oject1.bill_date >= from_date and oject1.bill_date <= to_date:
#                 for y in labels1:
#                     if oject1.business_name:
#                         if oject1.business_name.m_business_name == y:
#                             spend_by_bill_business1[y] =  spend_by_bill_business1[y] + oject1.bill_amount

#         for object1 in spend_by_bill_business1:
#             data1.append(spend_by_bill_business1[object1])

#         context['from_date'] = request.POST["from_date"]
#         context['to_date'] = request.POST["to_date"]
#     coupon_list = CouponModel.objects.all().order_by("-id")
#     parking_lot_passes = ParkingLotPass.objects.filter(mobile_no=request.user)
#     try:
#         for objects in parking_lot_passes:
#             bussiness_id = objects.m_business_id
#             obj = MerchantProfile.objects.get(id=bussiness_id)
#             objects.business_name = obj.m_business_name
#             objects.bussiness_logo = obj.m_business_logo
#     except:
#         pass

#     context = {
#         "parking_lot_pass": parking_lot_passes,
#         'business_name': b_name,
#         'bill_category': bill_category_name,
#         "customer_bill": all_cust_bill,
#         "bill_tags": customer_bill_tags,
#         'DashboardNavclass': 'active',
#         'segment':'index',
#         'labels':labels,
#         'data':data,
#         'data1': data1,
#         'labels1':labels1,
        
#         'green_points':GreenPoints,
#         'from_date' : from_date_temp,
#         'to_date' : to_date_temp,
#         'coupon_list':coupon_list,
        
#         }
    
#     html_template = loader.get_template('customer-index.html')

#     return HttpResponse(html_template.render(context, request))
    
# @login_required(login_url="/customer-login/")
# @user_passes_test(is_customer, login_url="/customer-login/")
# def customer_index(request):
#     #shopping Category data

#     labels = []
#     data = []

#     context = {}

#     queryset = CustomerBill.objects.filter(mobile_no=request.user)
  
#     # date in yyyy/mm/dd format 
#     # d1 = datetime.date(2020, 1, 3)
#     # d2 = datetime.date(2021, 1, 30)

#     #form fatching data in the table

#     all_cust_bill = CustomerBill.objects.filter(mobile_no=request.user).order_by('-id')

#     user_id = request.user.id

#     customer_bills = []

#     customer_bill_list = CustomerBill.objects.filter(mobile_no=request.user).order_by('-id')

#     customer_object = GreenBillUser.objects.get(id = user_id)

#     for bill in customer_bill_list:

#         try:
#             business_name = bill.business_name.m_business_name
#         except:
#             business_name = bill.custom_business_name

#         try:
#             bill_category_temp = bill.customer_bill_category.bill_category_name
#         except:
#             bill_category_temp = ""

#         base_url = "http://157.230.228.250/"

#         try:
#             business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
#         except:
#             business_logo = ""


#         customer_bills.append({
#                     "id": bill.id,
#                     "business_name": business_name,
#                     "bill_category_name": bill_category_temp,
#                     "bill_amount": bill.bill_amount,
#                     "comments": bill.remarks,
#                     "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
#                     "business_logo": business_logo,
#                     "customer_added": bill.customer_added,
#                     'db_table': "CustomerBill",
#                     "bill_file": bill.bill,
#                     "file_extension":"",
#                     "created_at":bill.created_at
#                 })


#     parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no, is_pass = False).order_by('-id')

#     for bill in parking_bill_list:

#         try:
#             business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
#         except:
#             business_name = ""

#         try:
#             bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
#         except:
#             bill_category_temp = ""

#         base_url = "http://157.230.228.250/"

#         try:
#             business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
#             business_logo = str(base_url) + str(business_logo_temp.url)

#         except:
#             business_logo = ""


#         customer_bills.append({
#                     "id": bill.id,
#                     "business_name": business_name,
#                     "bill_category_name": bill_category_temp,
#                     "bill_amount": bill.amount,
#                     "comments": bill.remarks,
#                     "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
#                     "business_logo": business_logo,
#                     "customer_added": False,
#                     'db_table': "SaveParkingLotBill",
#                     "bill_file": bill.bill_file,
#                     "file_extension":"",
#                     "created_at":bill.created_at
#                 })


#     petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no).order_by('-id')

#     for bill in petrol_bill_list:

#         try:
#             business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
#         except:
#             business_name = ""

#         try:
#             bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
#         except:
#             bill_category_temp = ""

#         base_url = "http://157.230.228.250/"

#         try:
#             business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
#             business_logo = str(base_url) + str(business_logo_temp.url)

#         except:
#             business_logo = ""


#         customer_bills.append({
#                     "id": bill.id,
#                     "business_name": business_name,
#                     "bill_category_name": bill_category_temp,
#                     "bill_amount": bill.total_amount,
#                     "comments": bill.remarks,
#                     "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
#                     "business_logo": business_logo,
#                     "customer_added": False,
#                     'db_table': "SavePetrolPumpBill",
#                     "bill_file": bill.bill_file,
#                     "file_extension":"",
#                     "created_at":  bill.created_at
#                 })

#     # customer_bills.sort(key = lambda x: datetime.strptime(x['created_at'], '%d-%m-%Y'), reverse = True)

#     customer_bills.sort(key=lambda r: r['created_at'], reverse = True)

#     for bill in customer_bills:
#         try:
#             file_type = filetype.guess(bill['bill_file'])
#             bill['file_extension'] = file_type.extension
#         except:
#             bill['file_extension'] = ""


#     # Shopping Analysis Start

#     # Analysis Category

#     for bills in customer_bills:
#         if bills['bill_category_name']:
#             if bills['bill_category_name'] in labels:
#                 pass
#             else:
#                 labels.append(bills['bill_category_name'])

#     spend_by_bill_category = {new_list: 0 for new_list in labels} 

#     for oject in customer_bills:
#         for x in labels:
#             if oject['bill_category_name']:
#                 if oject['bill_category_name'] == x:
#                     spend_by_bill_category[x] =  spend_by_bill_category[x] + float(oject['bill_amount'])

#     for object in spend_by_bill_category:
#         data.append(spend_by_bill_category[object])

#     context['from_date'] = ""
#     context['to_date'] = ""

#     context['data'] = data
#     context['labels'] = labels
    
#     # Merchant Analysis function
    
#     labels1 = []
#     data1 = []

#     for bills in customer_bills:
#         if bills['business_name']:
#             if bills['business_name'] in labels1:
#                 pass
#             else:
#                 labels1.append(bills['business_name'])

#     spend_by_bill_business1 = {new_list: 0 for new_list in labels1} 

#     for oject in customer_bills:
#         for y in labels1:
#             if oject['business_name']:
#                 if oject['business_name'] == y:
#                     spend_by_bill_business1[y] =  spend_by_bill_business1[y] + float(oject['bill_amount'])

#     for object in spend_by_bill_business1:
#         data1.append(spend_by_bill_business1[object])

#     context['data1'] = data1
#     context['labels1'] = labels1

#     # Shopping Analysis End

#     bill_category_name = bill_category.objects.all().order_by('bill_category_name')
#     b_name = MerchantProfile.objects.all()

#     try:
#         GreenPoints = GreenPointsModel.objects.filter(mobile_no=request.user).values('green_points_count')[0]['green_points_count']

#     except:
#         GreenPoints = 0
#     # green_points = GreenPointsModel.objects.all()
#     customer_bill_tags = bill_tags.objects.all().order_by('bill_tags_name')

#     for cust_bill in all_cust_bill:

#         bill_tags1 = cust_bill.bill_tags

#         if cust_bill.bill_tags:
#             bill_tags_list = list(bill_tags1.split(","))

#         else:
#             bill_tags_list = ""

#         bill_tags2 = []
    
#         if bill_tags1:

#             for x in range(len(bill_tags_list)): 

#                 try:

#                     bill_tags1 = bill_tags.objects.get(id=bill_tags_list[x])

#                     bill_tags2.append(bill_tags1.bill_tags_name)

#                 except:

#                     print("hello")

#         bill_tags3 = ', '.join(map(str, bill_tags2))

#         cust_bill.bill_tags_name = bill_tags3

#     from_date_temp  = ""
#     to_date_temp = ""

#     #Shopping analysis date filter

#     if request.method == 'POST':

#         labels = []
#         data = []

#         from_date_temp = request.POST["from_date"]
#         to_date_temp = request.POST["to_date"]

#         # from_date = datetime.strptime(request.POST["from_date"], "%Y-%m-%d").date()
#         from_date = datetime.strptime(str(request.POST["from_date"]), '%Y-%m-%d').strftime('%d-%m-%Y')
        
#         # to_date = datetime.strptime(request.POST["to_date"], "%Y-%m-%d").date()
#         to_date = datetime.strptime(str(request.POST["to_date"]), '%Y-%m-%d').strftime('%d-%m-%Y')

#         # from_date = datetime.datetime.strptime(request.POST["from_date"], "%Y-%m-%d").date()
#         # to_date = datetime.datetime.strptime(request.POST["to_date"], "%Y-%m-%d").date()
    
#         for bills in customer_bills:
#             if bills['bill_date'] >= from_date and bills['bill_date'] <= to_date:
#                 if bills['bill_category_name']:
#                     if bills['bill_category_name'] in labels:
#                         pass
#                     else:
#                         labels.append(bills['bill_category_name'])

#         spend_by_bill_category = {new_list: 0 for new_list in labels}

#         for oject in customer_bills:
#             if oject['bill_date'] >= from_date and oject['bill_date'] <= to_date:
#                 for x in labels:
#                     if oject['bill_category_name']:
#                         if oject['bill_category_name'] == x:
#                             spend_by_bill_category[x] =  spend_by_bill_category[x] + float(oject['bill_amount'])

#         for object in spend_by_bill_category:
#             data.append(spend_by_bill_category[object])

#         context['from_date'] = request.POST["from_date"]
#         context['to_date'] = request.POST["to_date"]

#         #for Murchant Date filter

#         labels1 = []
#         data1 = []
        
#         for bills1 in customer_bills:
#             if bills1['bill_date'] >= from_date and bills1['bill_date'] <= to_date:
#                 if bills1['business_name']:
#                     if bills1['business_name'] in labels1:
#                         pass
#                     else:
#                         labels1.append(bills1['business_name'])

#         spend_by_bill_business1 = {new_list1: 0 for new_list1 in labels1} 

#         for oject1 in customer_bills:
#             if oject1['bill_date'] >= from_date and oject1['bill_date'] <= to_date:
#                 for y in labels1:
#                     if oject1['business_name']:
#                         if oject1['business_name'] == y:
#                             spend_by_bill_business1[y] =  spend_by_bill_business1[y] + float(oject1['bill_amount'])

#         for object1 in spend_by_bill_business1:
#             data1.append(spend_by_bill_business1[object1])

#         context['from_date'] = request.POST["from_date"]
#         context['to_date'] = request.POST["to_date"]

#     coupon_list = CouponModel.objects.all().order_by("-id")
#     parking_lot_passes = ParkingLotPass.objects.filter(mobile_no=request.user)

#     try:
#         for objects in parking_lot_passes:
#             bussiness_id = objects.m_business_id
#             obj = MerchantProfile.objects.get(id=bussiness_id)
#             objects.business_name = obj.m_business_name
#             objects.bussiness_logo = obj.m_business_logo
#     except:
#         pass

#     context = {
#         "parking_lot_pass": parking_lot_passes,
#         'business_name': b_name,
#         'bill_category': bill_category_name,
#         "customer_bill": customer_bills,
#         "bill_tags": customer_bill_tags,
#         'DashboardNavclass': 'active',
#         'segment':'index',
#         'labels':labels,
#         'data':data,
#         'data1': data1,
#         'labels1':labels1,
        
#         'green_points':GreenPoints,
#         'from_date' : from_date_temp,
#         'to_date' : to_date_temp,
#         'coupon_list':coupon_list,
        
#         }
    
#     html_template = loader.get_template('customer-index1.html')

#     return HttpResponse(html_template.render(context, request))

@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def customer_index(request):

    labels = []
    data = []

    context = {}

    queryset = CustomerBill.objects.filter(mobile_no=request.user.mobile_no)

    all_cust_bill = CustomerBill.objects.filter(mobile_no=request.user.mobile_no).order_by('-id')
    
    user_id = request.user.id

    customer_bills = []

    customer_object = GreenBillUser.objects.get(id = user_id)

    bill_count = 0
    bill_flagged = 0
    total_bill_amount = 0
    total_merchant_bill_count = 0
    total_category_bill_count = 0

    customer_bill_list = CustomerBill.objects.filter(mobile_no=request.user.mobile_no).order_by('-id')

    for bill in customer_bill_list:

        bill_count += 1

        if bill.bill_amount:

            total_bill_amount = total_bill_amount + float(bill.bill_amount)

        # if bill.bill_flag == True:
        #     bill_flagged = bill_flagged + 1
        
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

        if business_name:
            total_merchant_bill_count += 1

        if bill_category_temp:
            total_category_bill_count += 1

        customer_bills.append({
            "id": bill.id,
            "business_name": business_name,
            "bill_category_name": bill_category_temp,
            "bill_amount": bill.bill_amount,
            "comments": bill.remarks,
            "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
            "business_logo": business_logo,
            "customer_added": bill.customer_added,
            'db_table': "CustomerBill",
            "bill_file": bill.bill,
            "file_extension":"",
            "created_at":bill.created_at,
          
        })


    parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no, is_pass = False).order_by('-id')

    for bill in parking_bill_list:

        bill_count += 1
        
        if bill.amount:
            total_bill_amount = total_bill_amount + float(bill.amount)
        
        if bill.bill_flag == True:
            bill_flagged = bill_flagged + 1

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

        if business_name:
            total_merchant_bill_count += 1

        if bill_category_temp:
            total_category_bill_count += 1

        customer_bills.append({
            "id": bill.id,
            "business_name": business_name,
            "bill_category_name": bill_category_temp,
            "bill_amount": bill.amount,
            "comments": bill.remarks,
            "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
            "business_logo": business_logo,
            "customer_added": False,
            'db_table': "SaveParkingLotBill",
            "bill_file": bill.bill_file,
            "file_extension":"",
            "created_at":bill.created_at
        })


    petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no).order_by('-id')

    for bill in petrol_bill_list:
        
        bill_count += 1

        if bill.total_amount:
            total_bill_amount = total_bill_amount + float(bill.total_amount)
        
        if bill.bill_flag == True:
            bill_flagged = bill_flagged + 1
       
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

        if business_name:
            total_merchant_bill_count += 1

        if bill_category_temp:
            total_category_bill_count += 1
        
        customer_bills.append({
            "id": bill.id,
            "business_name": business_name,
            "bill_category_name": bill_category_temp,
            "bill_amount": bill.total_amount,
            "comments": bill.remarks,
            "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
            "business_logo": business_logo,
            "customer_added": False,
            'db_table': "SavePetrolPumpBill",
            "bill_file": bill.bill_file,
            "file_extension":"",
            "created_at":  bill.created_at
        })

    customer_bills.sort(key=lambda r: r['created_at'], reverse = True)

    for bill in customer_bills:
        try:
            file_type = filetype.guess(bill['bill_file'])
            bill['file_extension'] = file_type.extension
        except:
            bill['file_extension'] = ""

    # Shopping Analysis Start

    # Analysis Category Wisw

    for bills in customer_bills:
        if bills['bill_category_name']:
            if bills['bill_category_name'] in labels:
                pass
            else:
                labels.append(bills['bill_category_name'])

    spend_by_bill_category = {new_list: 0 for new_list in labels} 

    for oject in customer_bills:
        for x in labels:
            if oject['bill_category_name']:
                if oject['bill_category_name'] == x:
                    spend_by_bill_category[x] =  spend_by_bill_category[x] + float(oject['bill_amount'])

    for object in spend_by_bill_category:
        data.append(spend_by_bill_category[object])
        
    context['from_date'] = ""
    context['to_date'] = ""

    context['data'] = data
    context['labels'] = labels
    
    # Merchant Analysis function
    
    labels1 = []
    data1 = []
    data_count1 = []
    data_count = 0 

    for bills in customer_bills:
        if bills['business_name']:
            if bills['business_name'] in labels1:
                pass
            else:
                labels1.append(bills['business_name'])

    spend_by_bill_business1 = {new_list: 0 for new_list in labels1} 

    for oject in customer_bills:
        for y in labels1:
            if oject['business_name']:
                if oject['business_name'] == y:
                    spend_by_bill_business1[y] =  spend_by_bill_business1[y] + float(oject['bill_amount'])

    for object in spend_by_bill_business1:
        data1.append(spend_by_bill_business1[object])

    context['data1'] = data1
    context['labels1'] =  labels1

    # Shopping Analysis End
    
    # Bill Count Merchant 

    name = []
    merchant_bill_count_doughnut = []
    data_count1 = 0

    for bills in customer_bills:
        if bills['business_name']:
            if bills['business_name'] in name:
                pass
            else:
                name.append(bills['business_name'])
                
    spend_by_bill_business2 = {new_list: 0 for new_list in name} 

    for oject in customer_bills:
        for y in name:
            if oject['business_name']:
                if oject['business_name'] == y:
                    spend_by_bill_business2[y] =  spend_by_bill_business2[y] + 1
                    data_count1 += 1

    for object in spend_by_bill_business2:
        merchant_bill_count_doughnut.append(spend_by_bill_business2[object])

    context['data1'] = data1
    context['name'] = name

    # End Bill Count Merchant

    # Bill Count Category 

    name1 = []
    category_bill_count_doughnut = []
    data_count2 = 0
    for bills in customer_bills:
        if bills['bill_category_name']:
            if bills['bill_category_name'] in name1:
                pass
            else:
                name1.append(bills['bill_category_name'])

    spend_by_bill_category = {new_list: 0 for new_list in name1} 

    for oject in customer_bills:
        for x in name1:
            if oject['bill_category_name']:
                if oject['bill_category_name'] == x:
                    spend_by_bill_category[x] =  spend_by_bill_category[x] + 1
                    data_count2 += 1
                    
    for object in spend_by_bill_category:
        category_bill_count_doughnut.append(spend_by_bill_category[object])

    context['data'] = data
    context['name1'] = name1

    context['from_date'] = ""
    context['to_date'] = ""

    # End Bill Count Category

    bill_category_name = bill_category.objects.all().order_by('bill_category_name')

    b_name = MerchantProfile.objects.all()

    try:
        GreenPoints = GreenPointsModel.objects.filter(mobile_no=request.user).values('green_points_count')[0]['green_points_count']

    except:
        GreenPoints = 0
    # green_points = GreenPointsModel.objects.all()

    customer_bill_tags = bill_tags.objects.all().order_by('bill_tags_name')

    for cust_bill in all_cust_bill:

        bill_tags1 = cust_bill.bill_tags

        if cust_bill.bill_tags:
            bill_tags_list = list(bill_tags1.split(","))

        else:
            bill_tags_list = ""

        bill_tags2 = []
    
        if bill_tags1:

            for x in range(len(bill_tags_list)): 

                try:

                    bill_tags1 = bill_tags.objects.get(id=bill_tags_list[x])

                    bill_tags2.append(bill_tags1.bill_tags_name)

                except:
                    pass

        bill_tags3 = ', '.join(map(str, bill_tags2))

        cust_bill.bill_tags_name = bill_tags3

    from_date_temp  = ""
    to_date_temp = ""

    #Shopping analysis date filter

    if request.method == 'POST':

        labels = []
        data = []

        from_date_temp = request.POST["from_date"]
        to_date_temp = request.POST["to_date"]

        # from_date = datetime.strptime(request.POST["from_date"], "%Y-%m-%d").date()
        from_date = datetime.strptime(str(request.POST["from_date"]), '%Y-%m-%d').strftime('%d-%m-%Y')
        
        # to_date = datetime.strptime(request.POST["to_date"], "%Y-%m-%d").date()
        to_date = datetime.strptime(str(request.POST["to_date"]), '%Y-%m-%d').strftime('%d-%m-%Y')

        # from_date = datetime.datetime.strptime(request.POST["from_date"], "%Y-%m-%d").date()
        # to_date = datetime.datetime.strptime(request.POST["to_date"], "%Y-%m-%d").date()
    
        for bills in customer_bills:
            if bills['bill_date'] >= from_date and bills['bill_date'] <= to_date:
                if bills['bill_category_name']:
                    if bills['bill_category_name'] in labels:
                        pass
                    else:
                        labels.append(bills['bill_category_name'])

        spend_by_bill_category = {new_list: 0 for new_list in labels}

        for oject in customer_bills:
            if oject['bill_date'] >= from_date and oject['bill_date'] <= to_date:
                for x in labels:
                    if oject['bill_category_name']:
                        if oject['bill_category_name'] == x:
                            spend_by_bill_category[x] =  spend_by_bill_category[x] + float(oject['bill_amount'])

        for object in spend_by_bill_category:
            data.append(spend_by_bill_category[object])

        context['from_date'] = request.POST["from_date"]
        context['to_date'] = request.POST["to_date"]

        #for Murchant Date filter

        labels1 = []
        data1 = []
        
        for bills1 in customer_bills:
            if bills1['bill_date'] >= from_date and bills1['bill_date'] <= to_date:
                if bills1['business_name']:
                    if bills1['business_name'] in labels1:
                        pass
                    else:
                        labels1.append(bills1['business_name'])

        spend_by_bill_business1 = {new_list1: 0 for new_list1 in labels1} 

        for oject1 in customer_bills:
            if oject1['bill_date'] >= from_date and oject1['bill_date'] <= to_date:
                for y in labels1:
                    if oject1['business_name']:
                        if oject1['business_name'] == y:
                            spend_by_bill_business1[y] =  spend_by_bill_business1[y] + float(oject1['bill_amount'])
        
        for object1 in spend_by_bill_business1:
            data1.append(spend_by_bill_business1[object1])
            
        context['from_date'] = request.POST["from_date"]
        context['to_date'] = request.POST["to_date"]

    coupon_list = CouponModel.objects.all().order_by("-id")
    parking_lot_passes = ParkingLotPass.objects.filter(mobile_no=request.user)

    try:
        for objects in parking_lot_passes:
            bussiness_id = objects.m_business_id
            obj = MerchantProfile.objects.get(id=bussiness_id)
            objects.business_name = obj.m_business_name
            objects.bussiness_logo = obj.m_business_logo
    except:
        pass
   
    # billCountchart
    context['billCountchart_labels'] = ','.join(map(str, labels))

    # print(total_bill_amount)
    # sdb

    context = {
        "parking_lot_pass": parking_lot_passes,
        'business_name': b_name,
        'bill_category': bill_category_name,
        "customer_bill": customer_bills,
        "bill_tags": customer_bill_tags,
        'DashboardNavclass': 'active',
        'segment':'index',

        'labels':labels,
        'data':data,
        'merchant_bill_count_doughnut' : merchant_bill_count_doughnut,

        'data1': data1,
        'labels1':labels1,
        'category_bill_count_doughnut' : category_bill_count_doughnut,
       
        'green_points':GreenPoints,
        'from_date' : from_date_temp,
        'to_date' : to_date_temp,
        'coupon_list':coupon_list,

        'total_bill_amount' : total_bill_amount,

        'bill_flagged': bill_flagged,
        'total_bill_count': bill_count,

        'total_merchant_bill_count': total_merchant_bill_count,
        'total_category_bill_count': total_category_bill_count,
        }
    
    html_template = loader.get_template('customer-index.html')

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_index(request):
    context = {} 
    context['segment'] = 'index'
    context['DashboardNavclass'] = 'active'
    html_template = loader.get_template('partner-index.html')
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    
    try:
        # load_template      = request.path.split('/')[-1]
        # context['segment'] = load_template
        # context['DashboardNavclass'] = 'active'

        # html_template = loader.get_template( load_template )
        # return HttpResponse(html_template.render(context, request))

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def module_permission(request):
    sale_items = {'Monday':'Mocha 2x1','Tuesday':'Latte 2x1'}
    return {'SALE_ITEMS': sale_items}

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            oldpass = form.cleaned_data['password']
            newPass = request.POST['password1']
            if oldpass != newPass :
                # success = User.check_password(request.user, oldpass)
                success = request.user.check_password(oldpass)
                if success == True:
                    request.user.set_password(newPass)
                    request.user.save()
                    update_session_auth_hash(request, request.user)  # Important!
                    return JsonResponse({'status':'success'})
                else: 
                    return JsonResponse({'status':'error'})
            else:
                return JsonResponse({'status':'errorPass', 'msg': 'Please enter different password'})
        else:
            return False
    else:
        return render(request, 'error-404.html')


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def chanage_merchnat_business_view(request):
    if request.method == 'POST':
        merchant_users_object = Merchant_users.objects.get(user_id = request.user)
        merchant_object = GreenBillUser.objects.get(id = merchant_users_object.merchant_user_id.id)

        m_business_previous_id = request.POST["m_business_previous_id"]
        m_business = request.POST["m_business_change"]
        
        MerchantProfile.objects.filter(m_user = merchant_object).update(m_active_account = False)
        # MerchantProfile.objects.filter(id=m_business_previous_id).update(m_active_account = False)
        MerchantProfile.objects.filter(id=m_business).update(m_active_account = True)
        # sweetify.success(request, title="Success", icon='success', text='Business Updated.', timer=1000)
        return redirect(merchant_index)
    else:
        # sweetify.success(request, title="Oops...", icon='error', text='Fail to Updated.', timer=1000)
        return redirect(merchant_index)
        
# // $.notify({
# // 	icon: 'flaticon-alarm-1',
# // 	title: 'Atlantis Lite',
# // 	message: 'Free Bootstrap 4 Admin Dashboard',
# // },{
# // 	type: 'info',
# // 	placement: {
# // 		from: "bottom",
# // 		align: "right"
# // 	},
# // 	time: 1000,
# // });


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def chanage_merchnat_branch_view(request):
    if request.method == 'POST':
        merchant_users_object = Merchant_users.objects.get(user_id = request.user)
        merchant_object = GreenBillUser.objects.get(id = merchant_users_object.merchant_user_id.id)

        m_business_previous_id = request.POST["m_business_previous_id"]
        m_business = request.POST.get("m_business_category")
        
        MerchantProfile.objects.filter(m_user = merchant_object).update(m_active_account = False)
        # MerchantProfile.objects.filter(id=m_business_previous_id).update(m_active_account = False)
        MerchantProfile.objects.filter(id=m_business).update(m_active_account = True)
        # sweetify.success(request, title="Success", icon='success', text='Business Updated.', timer=1000)
        return redirect(merchant_index)
    else:
        # sweetify.success(request, title="Oops...", icon='error', text='Fail to Updated.', timer=1000)
        return redirect(merchant_index)
        



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def email_setting(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST)

        if email_form.is_valid():
            email_type = email_form.cleaned_data.get("email_type")
            smtp_username = email_form.cleaned_data.get("smtp_username")
            smtp_password = email_form.cleaned_data.get("smtp_password")
            smtp_server = email_form.cleaned_data.get("smtp_server")
            smtp_port = email_form.cleaned_data.get("smtp_port")
            smtp_security = email_form.cleaned_data.get("smtp_security")

            emailSetting.objects.update_or_create(email_type=email_type, defaults={
                'email_type': email_type, 'smtp_username': smtp_username, 'smtp_password': smtp_password, 'smtp_server': smtp_server, 'smtp_port': smtp_port, 'smtp_security': smtp_security
            })

            sweetify.success(request, title="Success", icon='success',
                             text='Email Setting Stored Successfully !!!')
            return redirect('/email-setting/')
        else:
            sweetify.error(request, title="error",
                           icon='danger', text='Failed !!!')
    else:
        email_form = EmailForm()
        if emailSetting.objects.all():
            email_data = emailSetting.objects.latest('id')
        else:
            email_data = None
    
    context = {
            'email_form': email_form,
            'email_data': email_data,
            "SettingsNavclass": "active",
            "settingsCollapseShow": "show",
            "EmailSettingsNavclass": "active"
    }

    return render(request, "email_setting.html", context)

def password_reset_request(request):
    password_reset_form = PasswordResetForm(request.POST)
    password_reset_form = PasswordResetForm()
    
    return render(request, "accounts/password_reset_form.html", {'password_reset_form' : password_reset_form})

def password_reset_request_merchant(request):
    password_reset_form = PasswordResetForm(request.POST)
    password_reset_form = PasswordResetForm()
    
    return render(request, "accounts/password_reset_form_merchant.html", {'password_reset_form' : password_reset_form})

def password_reset_request_customer(request):
    password_reset_form = PasswordResetForm(request.POST)
    password_reset_form = PasswordResetForm()
    
    return render(request, "accounts/password_reset_form_customer.html", {'password_reset_form' : password_reset_form})

def password_reset_request_partner(request):
    password_reset_form = PasswordResetForm(request.POST)
    password_reset_form = PasswordResetForm()
    
    return render(request, "accounts/password_reset_form_partner.html", {'password_reset_form' : password_reset_form})

def generate_otp_password(request):
    
    mobile_no = request.POST['mobile_no']
    if mobile_no:
        result = GreenBillUser.objects.filter(mobile_no=mobile_no)

        if result:

            if result[0].is_staff:
                otp = random.randint(99999, 999999)
                otp_validation.objects.update_or_create(mobile_no=mobile_no, defaults={'otp': otp})
                associated_users = GreenBillUser.objects.filter(Q(mobile_no=mobile_no))
                
                if associated_users.exists():
                    for user in associated_users:
                        try:

                            ts = int(time.time())
                            sms_data_temp = {
                                "keyword":"Web Forgot Password OTP",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Dear Green Bill user, Use " + str(otp) + " as OTP to reset your password.",
                                            "OA":"GRBILL",
                                            "MSISDN":str(mobile_no), # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098368573560", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                            response = requests.post(url, json = sms_data_temp)

                            if response.status_code == 200:
                                return JsonResponse({'status': 'success', 'mobile_no' : mobile_no})
                            else:
                                return JsonResponse({'status' : 'error', 'msg': "Failed to send otp"}) 

                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')

            elif result[0].is_merchant or result[0].is_merchant_staff:
                return JsonResponse({'status' : 'error', 'msg': "Mobile Number is registered as Merchant or Merchant user. So please Use Merchant Web Panel."})
            elif result[0].is_customer:
                return JsonResponse({'status' : 'error', 'msg': "Mobile Number is registered as Customer. So please Use Customer Web Panel."})
            elif result[0].is_partner:
                return JsonResponse({'status' : 'error', 'msg': "Mobile Number is registered as Partner. So please Use Partner Web Panel."})  
        else :
            return JsonResponse({'status' : 'error', 'msg': "Mobile Number is not registered"})
    else:
        return JsonResponse({'status': 'error'})

def generate_otp_password_customer(request):
    
    mobile_no = request.POST['mobile_no']
    if mobile_no:
        result = GreenBillUser.objects.filter(mobile_no=mobile_no)

        if result:

            if result[0].is_customer:
                otp = random.randint(99999, 999999)
                otp_validation.objects.update_or_create(mobile_no=mobile_no, defaults={'otp': otp})
                associated_users = GreenBillUser.objects.filter(Q(mobile_no=mobile_no))
                
                if associated_users.exists():
                    for user in associated_users:
                        try:
                            ts = int(time.time())

                            sms_data_temp = {
                                    "keyword":"Web Forgot Password OTP",
                                    "timeStamp":ts,
                                    "dataSet":
                                        [
                                            {
                                                "UNIQUE_ID":"GB-" + str(ts),
                                                "MESSAGE":"Dear Green Bill user, Use " + str(otp) + " as OTP to reset your password.",
                                                "OA":"GRBILL",
                                                "MSISDN":str(mobile_no), # Recipient's Mobile Number
                                                "CHANNEL":"SMS",
                                                "CAMPAIGN_NAME":"hind_user",
                                                "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                "USER_NAME":"hind_hsi",
                                                "DLT_TM_ID":"1001096933494158", # TM ID
                                                "DLT_CT_ID":"1007162098368573560", # Template Id
                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                            }
                                        ]
                                    }

                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                            response = requests.post(url, json = sms_data_temp)

                            if response.status_code == 200:
                                return JsonResponse({'status': 'success', 'mobile_no' : mobile_no})
                            else:
                                return JsonResponse({'status' : 'error', 'msg': "Failed to send otp"}) 

                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')

            elif result[0].is_merchant or result[0].is_merchant_staff:
                return JsonResponse({'status' : 'error', 'msg': "Mobile Number is registered as Merchant or Merchant user. So please Use Merchant Web Panel."})
            elif result[0].is_staff:
                return JsonResponse({'status' : 'error', 'msg': "Mobile Number is registered as Owner or Owner Staff. So please Use Owner Web Panel."})
            elif result[0].is_partner:
                return JsonResponse({'status' : 'error', 'msg': "Mobile Number is registered as Partner. So please Use Partner Web Panel."})  
        else :
            return JsonResponse({'status' : 'error', 'msg': "Mobile Number is not registered"})
    else:
        return JsonResponse({'status': 'error'})


def generate_otp_password_merchant(request):
    
    mobile_no = request.POST['mobile_no']
    if mobile_no:
        result = GreenBillUser.objects.filter(mobile_no=mobile_no)

        if result:

            if result[0].is_merchant_staff or result[0].is_merchant:
                otp = random.randint(99999, 999999)
                otp_validation.objects.update_or_create(mobile_no=mobile_no, defaults={'otp': otp})
                associated_users = GreenBillUser.objects.filter(Q(mobile_no=mobile_no))
               
                if associated_users.exists():
                    for user in associated_users:
                        try:
                            ts = int(time.time())

                            sms_data_temp = {
                                "keyword":"Web Forgot Password OTP",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Dear Green Bill user, Use " + str(otp) + " as OTP to reset your password.",
                                            "OA":"GRBILL",
                                            "MSISDN":str(mobile_no), # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098368573560", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                            response = requests.post(url, json = sms_data_temp)

                            if response.status_code == 200:
                                return JsonResponse({'status': 'success', 'mobile_no' : mobile_no})
                            else:
                                return JsonResponse({'status' : 'error', 'msg': "Failed to send otp"}) 

                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')

            elif result[0].is_customer:
                return JsonResponse({'status' : 'error', 'msg': "Mobile Number is registered as Customer. So please Use Customer Web Panel."})
            elif result[0].is_staff:
                return JsonResponse({'status' : 'error', 'msg': "Mobile Number is registered as Owner or Owner Staff. So please Use Owner Web Panel."})
            elif result[0].is_partner:
                return JsonResponse({'status' : 'error', 'msg': "Mobile Number is registered as Partner. So please Use Partner Web Panel."})  
        else :
            return JsonResponse({'status' : 'error', 'msg': "Mobile Number is not registered"})
    else:
        return JsonResponse({'status': 'error'})

def generate_otp_password_partner(request):
    
    mobile_no = request.POST['mobile_no']
    if mobile_no:
        result = GreenBillUser.objects.filter(mobile_no=mobile_no)

        if result:

            if result[0].is_partner:
                otp = random.randint(99999, 999999)
                otp_validation.objects.update_or_create(mobile_no=mobile_no, defaults={'otp': otp})
                associated_users = GreenBillUser.objects.filter(Q(mobile_no=mobile_no))
                
                if associated_users.exists():
                    for user in associated_users:
                        try:
                            ts = int(time.time())
                            
                            sms_data_temp = {
                                "keyword":"Web Forgot Password OTP",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Dear Green Bill user, Use " + str(otp) + " as OTP to reset your password.",
                                            "OA":"GRBILL",
                                            "MSISDN":str(mobile_no), # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098368573560", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                            response = requests.post(url, json = sms_data_temp)

                            if response.status_code == 200:
                                return JsonResponse({'status': 'success', 'mobile_no' : mobile_no})
                            else:
                                return JsonResponse({'status' : 'error', 'msg': "Failed to send otp"}) 

                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')

            elif result[0].is_merchant or result[0].is_merchant_staff:
                return JsonResponse({'status' : 'error', 'msg': "Mobile Number is registered as Merchant or Merchant user. So please Use Merchant Web Panel."})
            elif result[0].is_staff:
                return JsonResponse({'status' : 'error', 'msg': "Mobile Number is registered as Owner or Owner Staff. So please Use Owner Web Panel."})
            elif result[0].is_customer:
                return JsonResponse({'status' : 'error', 'msg': "Mobile Number is registered as Customer. So please Use Customer Web Panel."})  
        else :
            return JsonResponse({'status' : 'error', 'msg': "Mobile Number is not registered"})
    else:
        return JsonResponse({'status': 'error'})


def otp_validation_password(request):
   
    if request.method == "POST":
        otp_temp = request.POST['otp']
        mobile_no = request.POST['mobile_no']

        otp = otp_validation.objects.filter(mobile_no=mobile_no).values('otp')[0]['otp']
        
        if otp == otp_temp:
            return JsonResponse({ 'status' : 'success', 'mobile_no' : mobile_no })
        else:
            return JsonResponse({ 'status' : 'error'})

def password_change_success(request):
    
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        newPassword = request.POST['newPassword']
        result = GreenBillUser.objects.filter(mobile_no=mobile_no).values('id')[0]['id']
        user_object = GreenBillUser.objects.get(id=result)
        
        success = GreenBillUser.check_password(user_object, newPassword)
        
        if success == True:
            
            return JsonResponse({ 'status' : 'errorOldPass', 'msg': "New Password cannot be same as Old Password"})
        else:
            
            user_object.set_password(newPassword)
            user_object.save()
            if result:
                return JsonResponse({ 'status' : 'success' , 'msg': "Password Changed Successfully!!!"})
            else:
                return JsonResponse({ 'status' : 'error', 'msg': "Something Went Wrong !!!"})

# @login_required(login_url="/login/")
# @user_passes_test(is_owner, login_url="/login/")
# def general_setting(request):
#     if request.method == "POST":
#         form = generalSettingForm(request.POST, request.FILES)

#         if form.is_valid():
#             business_name = form.cleaned_data.get("business_name")
#             business_code = form.cleaned_data.get("business_code")
#             mobile_no = form.cleaned_data.get("mobile_no")
#             email = form.cleaned_data.get("email")
#             date_format = form.cleaned_data.get("date_format")
#             currency = form.cleaned_data.get("currency")
#             android_app_url = form.cleaned_data.get("android_app_url")
#             iphone_app_url = form.cleaned_data.get("iphone_app_url")
#             o_business_logo = form.cleaned_data.get("o_business_logo")
#             o_digital_signature = form.cleaned_data.get("o_digital_signature")
#             o_business_stamp = form.cleaned_data.get("o_business_stamp")

#             temp = generalSetting.objects.update_or_create(id=1, defaults={'business_name': business_name, 'business_code': business_code, 'mobile_no': mobile_no, 'email': email, 'date_format': date_format, 'currency': currency, 'android_app_url': android_app_url, 'iphone_app_url': iphone_app_url})

#             if o_business_logo:
#                 generalSetting.objects.update_or_create(id=1, defaults={'o_business_logo':o_business_logo})

#             if o_digital_signature:
                
#                 generalSetting.objects.update_or_create(id=1, defaults={'o_digital_signature':o_digital_signature})

#             if o_business_stamp:
#                 generalSetting.objects.update_or_create(id=1, defaults={'o_business_stamp':o_business_stamp})


#             sweetify.success(request, title="Success", icon='success',
#                              text='Business Settings Stored Successfully !!!')
#             return redirect('/general-setting/')
#         else:
#             sweetify.error(request, title="error",
#                            icon='error', text='Failed !!!')
#     else:
#         user = request.user
#         if generalSetting.objects.all():
#             data = generalSetting.objects.latest('id')
#         else:
#             data = None
            
#         form = generalSettingForm()

#         context = {
#             'form' : form,
#             'data': data,
#             "SettingsNavclass": "active",
#             "settingsCollapseShow": "show",
#             "GeneralSettingsNavclass": "active"
#         }
            
#         return render(request, "general_setting.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def general_setting(request):
    if request.method == "POST":
        form = generalSettingForm(request.POST, request.FILES)

        if form.is_valid():
            business_name = form.cleaned_data.get("business_name")
            business_code = form.cleaned_data.get("business_code")
            mobile_no = form.cleaned_data.get("mobile_no")
            email = form.cleaned_data.get("email")
            alternate_mobile_number  = form.cleaned_data.get('alternate_mobile_number')
            alternate_email  = form.cleaned_data.get('alternate_email')
            address  = form.cleaned_data.get('address')
            city  = form.cleaned_data.get('city')
            area  = form.cleaned_data.get('area')
            distrct  = form.cleaned_data.get('distrct')
            state  = form.cleaned_data.get('state')
            pin_code  = form.cleaned_data.get('pin_code')
            pan_number = form.cleaned_data.get('pan_number')
            aadhaar_number  = form.cleaned_data.get('aadhaar_number')
            gstin  = form.cleaned_data.get('gstin')
            cin  = form.cleaned_data.get('cin')
            tin_vat_number  = form.cleaned_data.get('tin_vat_number')
            bank_account_number  = form.cleaned_data.get('bank_account_number')
            bank_IFSC_code  = form.cleaned_data.get('bank_IFSC_code')
            bank_name  = form.cleaned_data.get('bank_name')
            bank_branch  = form.cleaned_data.get('bank_branch')
            cancelled_cheque_certificate = form.cleaned_data.get('cancelled_cheque_certificate')
            GSTIN_certificate = form.cleaned_data.get('GSTIN_certificate')
            CIN_certificate = form.cleaned_data.get('CIN_certificate')
            udyog_adhar_certificate = form.cleaned_data.get('udyog_adhar_certificate')
            date_format = form.cleaned_data.get("date_format")
            currency = form.cleaned_data.get("currency")
            android_app_url = form.cleaned_data.get("android_app_url")
            iphone_app_url = form.cleaned_data.get("iphone_app_url")
            o_business_logo = form.cleaned_data.get("o_business_logo")
            o_digital_signature = form.cleaned_data.get("o_digital_signature")
            o_business_stamp = form.cleaned_data.get("o_business_stamp")

            temp = generalSetting.objects.update_or_create(id=1, defaults={'business_name': business_name, 'business_code': business_code, 'mobile_no': mobile_no, 'email': email, 'date_format': date_format, 'currency': currency, 'android_app_url': android_app_url, 'iphone_app_url': iphone_app_url,
            'alternate_mobile_number' : alternate_mobile_number,'alternate_email' : alternate_email,'address' : address, 'pan_number' : pan_number,
            'city' : city,'area' : area,'distrct' : distrct,'state' : state,'pin_code' : pin_code,'aadhaar_number' : aadhaar_number,'gstin' : gstin,'cin' : cin,
            'tin_vat_number' : tin_vat_number,'bank_account_number' : bank_account_number,'bank_IFSC_code' : bank_IFSC_code,'bank_name' : bank_name,'bank_branch' : bank_branch})
           
            if o_business_logo:
                generalSetting.objects.update_or_create(id=1, defaults={'o_business_logo':o_business_logo})

            if o_digital_signature:
                
                generalSetting.objects.update_or_create(id=1, defaults={'o_digital_signature':o_digital_signature})

            if o_business_stamp:
                generalSetting.objects.update_or_create(id=1, defaults={'o_business_stamp':o_business_stamp})

            if GSTIN_certificate:
                generalSetting.objects.update_or_create(id = 1, defaults={ "m_GSTIN_certificate" : GSTIN_certificate })

            if CIN_certificate:
                generalSetting.objects.update_or_create(id = 1, defaults={ "m_CIN_certificate" : CIN_certificate })
            
            if cancelled_cheque_certificate:
                generalSetting.objects.update_or_create(id = 1, defaults={ "cancelled_cheque_certificate" : cancelled_cheque_certificate })

            if udyog_adhar_certificate:
                generalSetting.objects.update_or_create(id = 1, defaults={ "udyog_adhar_certificate" : udyog_adhar_certificate })
            


            sweetify.success(request, title="Success", icon='success',
                             text='Business Settings Stored Successfully !!!')
            return redirect('/general-setting/')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!')
    else:
        user = request.user
        if generalSetting.objects.all():
            data = generalSetting.objects.latest('id')
        else:
            data = None
            
        form = generalSettingForm()

        context = {
            'form' : form,
            'data': data,
            "SettingsNavclass": "active",
            "settingsCollapseShow": "show",
            "GeneralSettingsNavclass": "active"
        }
            
        return render(request, "general_setting.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def owner_business_logo_remove(request):
    generalSetting.objects.update_or_create(id = 1, defaults={ "o_business_logo" : ""})
    return redirect(general_setting)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def owner_business_stamp_remove(request):
    generalSetting.objects.update_or_create(id = 1, defaults={ "o_business_stamp" : ""})
    return redirect(general_setting)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def owner_digital_signature_remove(request):
    generalSetting.objects.update_or_create(id = 1, defaults={ "o_digital_signature" : ""})
    return redirect(general_setting)




@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def upload_signature_img(request):
    if request.method == 'POST':
        form = FileUploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
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

            im = Image.open(request.FILES['docfile']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            newdoc = generalSetting.objects.get(id=1)
            newdoc.o_digital_signature.save('owner_signature.png', image_file)
            newdoc.save()
            data = {
                'result': True,
                'state': 200,
                'message': 'Success',
            }

            # redirect("/general-setting/")

            return JsonResponse({'data': data})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def upload_stamp_img(request):
    if request.method == 'POST':
        form = stampuploadform(data=request.POST, files=request.FILES)
        if form.is_valid():
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

            im = Image.open(request.FILES['stampfile']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            newdoc = generalSetting.objects.get(id=1)
            newdoc.o_business_stamp.save('owner_stamp.png', image_file)
            newdoc.save()
            data = {
                'result': True,
                'state': 200,
                'message': 'Success',
            }
            return JsonResponse({'data': data})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def upload_logo_img(request):
    if request.method == 'POST':
        form = logouploadform(data=request.POST, files=request.FILES)
        if form.is_valid():
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

            im = Image.open(request.FILES['logofile']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            newdoc = generalSetting.objects.get(id=1)
            newdoc.o_business_logo.save('owner_stamp.png', image_file)
            newdoc.save()
            data = {
                'result': True,
                'state': 200,
                'message': 'Success',
            }
            return JsonResponse({'data': data})




# Customer Parking Lot Passes
@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def Parking_Lot_Passes(request):
    parking_lot_passes = ParkingLotPass.objects.filter(mobile_no=request.user).order_by('-id')
    try:
        for objects in parking_lot_passes:
            bussiness_id = objects.m_business_id
            obj = MerchantProfile.objects.get(id=bussiness_id)
            objects.business_name = obj.m_business_name
            objects.bussiness_logo = obj.m_business_logo
            objects.qr_code = "GreenBill~Parking Pass~" + str(objects.id)
    except:
        pass

    context = {
        "ParkingLotPassNavclass": 'active',
        "BillCollapseShow": "show",
        "AddBillsNavclass": "active",
        "parking_lot_pass": parking_lot_passes,
        
    }
    return render(request, "customer/parking_lot_pass/parking_lot_passes.html", context)


# @login_required(login_url="/merchant-login/")
# @user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")   
# def Merchant_Parking_Lot_Passes(request):
#     parking_lot_passes = ParkingLotPass.objects.filter(mobile_no=request.user)
#     try:
#         for objects in parking_lot_passes:
#             bussiness_id = objects.m_business_id
#             obj = MerchantProfile.objects.get(id=bussiness_id)
#             objects.business_name = obj.m_business_name
#             objects.bussiness_logo = obj.m_business_logo
#     except:
#         pass
#     context = {
#         "ParkingLotPassNavclass": 'active',
#         "ParkingLotCollapseShow": "show",
#         "ParkingLotNavclass": "active",
#         "parking_lot_pass": parking_lot_passes,
        
#     }
#     return render(request, "merchant/merchant_pass/merchant_passes.html", context)



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_search(request):

    if request.method == "POST":

        mer_user_id = Merchant_users.objects.get(user_id=request.user)

        merchant_object = mer_user_id.merchant_user_id
        
        merchant_business_object = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

        merchant_business_id = merchant_business_object.id

        keywords = request.POST["search_keyword"].strip()

        data = []

        base_url = "http://157.230.228.250/"

        try:
            bill_design = bill_designs.objects.get(merchant_business_id = merchant_business_object)
            bill_rating_emoji = bill_design.rating_emoji
        except:
            bill_rating_emoji = ""

        parking_bill_list = SaveParkingLotBill.objects.filter(Q(m_business_id = merchant_business_id), (Q(mobile_no__icontains = keywords) | Q(invoice_no__icontains = keywords))).order_by('-id')

        for bill in parking_bill_list:
            try:
                bill_file = str(base_url) + str(bill.bill_file.url)
            except:
                bill_file = ""

            ratings = ""    

            if bill.rating:
                for x in range(int(bill.rating)):
                    ratings = " ".join((ratings, bill_rating_emoji))

            try:
                user_object = GreenBillUser.objects.get(id = bill.user_id)
                created_by_id = user_object.id
                created_by = user_object.first_name + ' ' + user_object.last_name
            except:
                created_by_id = ""
                created_by = ""

            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': bill.mobile_no,
                'amount': str(bill.amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SaveParkingLotBill",
                'customer_added': False,
                'bill_ratings': ratings,
                'rating': bill.rating,
                'created_by': created_by,
                'created_by_id': created_by_id,
                'bill_flag': bill.bill_flag,
                'flag_by': bill.flag_by
            })

        petrol_bill_list = SavePetrolPumpBill.objects.filter(Q(m_business_id = merchant_business_id), (Q(mobile_no__icontains = keywords) | Q(invoice_no__icontains = keywords))).order_by('-id')
        for bill in petrol_bill_list:
            try:
                bill_file = str(base_url) + str(bill.bill_file.url)
            except:
                bill_file = ""
            
            ratings = ""    

            if bill.rating:
                for x in range(int(bill.rating)):
                    ratings = " ".join((ratings, bill_rating_emoji))

            try:
                user_object = GreenBillUser.objects.get(id = bill.user_id)
                created_by_id = user_object.id
                created_by = user_object.first_name + ' ' + user_object.last_name
            except:
                created_by = ""
                created_by_id = ""

            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': bill.mobile_no,
                'amount': str(bill.total_amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SavePetrolPumpBill",
                'customer_added': False,
                'bill_ratings': ratings,
                'rating': bill.rating,
                'created_by': created_by,
                'created_by_id': created_by_id,
                'bill_flag': bill.bill_flag,
                'flag_by': bill.flag_by
            })

        data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

        context = {"bills":data}

    else:
        context = {"bills":""}

    return render(request, "merchant-search.html", context)


def test_sms(request):

   #  import requests

   #  import time
  
   #  ts = time.time()

   #  # http://157.230.228.250/self-added-bill/502sNRQ426eT/

   #  data_temp = {
			# "keyword":"DEMO",
			# "timeStamp":ts,
			# "dataSet":
   #  			[
   #  				{
   #      				"UNIQUE_ID":"735694wew", # https://bit.ly/3sKHq09
   #      				"MESSAGE":"Hey Green Bill user to view or download your bill click on link https://tinyurl.com/yfka5v4n to view all your bills download Green Bill App",
   #      				"OA":"GBPARK",
   #      				"MSISDN":"7709977798",
   #      				"CHANNEL":"SMS",
   #      				"CAMPAIGN_NAME":"hind_user",
   #      				"CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
   #      				"USER_NAME":"hind_hsi",
   #      				"DLT_TM_ID":"1001096933494158",
   #      				"DLT_CT_ID":"1007161814187973948", # Template Id
   #      				"DLT_PE_ID":"1001659120000037015" 
   #  				}
   #  			]
			# }

    # data_temp = {
    #         "keyword":"DEMO",
    #         "timeStamp":ts,
    #         "dataSet":
    #             [
    #                 {
    #                     "UNIQUE_ID":"735694wew", # https://bit.ly/3sKHq09
    #                     "MESSAGE":"Hey, Green Bill User, Please use OPT 123456 to log in into your account.",
    #                     "OA":"GBPARK",
    #                     "MSISDN":"7709977798",
    #                     "CHANNEL":"SMS",
    #                     "CAMPAIGN_NAME":"hind_user",
    #                     "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
    #                     "USER_NAME":"hind_hsi",
    #                     "DLT_TM_ID":"1001096933494158",
    #                     "DLT_CT_ID":"1007161814187973948", # Template Id
    #                     "DLT_PE_ID":"1001659120000037015" 
    #                 }
    #             ]
    #         }

    # data_temp = {
    #         "keyword":"DEMO",
    #         "timeStamp":ts,
    #         "dataSet":
    #             [
    #                 {
    #                     "UNIQUE_ID":"735694wew", # https://bit.ly/3sKHq09
    #                     "MESSAGE":"Thank you for choosing GreenBill as your digital billing buddy. Your registration is complete please visit website or download GB Merchant App to login",
    #                     "OA":"GBPARK",
    #                     "MSISDN":"8956662377, 7709977798", 
    #                     "CHANNEL":"SMS",
    #                     "CAMPAIGN_NAME":"hind_user",
    #                     "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
    #                     "USER_NAME":"hind_hsi",
    #                     "DLT_TM_ID":"1001096933494158",
    #                     "DLT_CT_ID":"1007161814117326730", # Template Id
    #                     "DLT_PE_ID":"1001659120000037015" 
    #                 }
    #             ]
    #         }

    # data_temp = {
    #     "keyword":"DEMO",
    #     "timeStamp":"071818163530",
    #     "dataSet":
    #         [
    #             {
    #             "UNIQUE_ID":"735694wew",
    #             "MESSAGE":"This is a testing message to test single short SMS on AIRTEL DLT.",
    #             "OA":"DGMATE",
    #             "MSISDN":"7709977798",
    #             "CHANNEL":"SMS",
    #             "CAMPAIGN_NAME":"hind_user",
    #             "CIRCLE_NAME":"DLT_PROMOTIONAL_SMS",
    #             "USER_NAME":"hind_hpro",
    #             "DLT_TM_ID":"1001096933494158",
    #             "DLT_CT_ID":"",
    #             "DLT_PE_ID":"1001751517438613463"
    #             }
    #         ]
    #     }

    # url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

    # # # response = requests.post('http://digimate.airtel.in:15181/BULK_API/InstantJsonPush', data = json.dumps(data_temp), headers={'Content-Type':'application/json'})
    # response = requests.post(url, json = data_temp)

    import requests
    import time
    ts = int(time.time())

    data_temp = {
            "keyword":"Welcome Message",
            "timeStamp":ts,
            "dataSet":
                [
                    {
                        "UNIQUE_ID":"GB-" + str(ts),
                        "MESSAGE":"Thank you for registering on Green Bill. Welcome to the Green Bill Community. Feel free to get in touch with us at www.greenbill.in",
                        "OA":"GBPUMP",
                        "MSISDN":"7709977798", # Recipient's Mobile Number
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

    # import pyshorteners

    # s = pyshorteners.Shortener()
    # print(s.tinyurl.short('http://157.230.228.250/self-added-bill/502sNRQ426eT/'))

    if response.status_code == 200:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_index1(request):
    # context = {} 
    # context['segment'] = 'index'
    # context['DashboardNavclass'] = 'active'
    # html_template = loader.get_template('merchant-index.html')
    context = {}

    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_users_object.merchant_user_id

    merchant_business = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

    merchant_business_id = merchant_business.id

    merchant_user = []

    merchant_user.append({
        'user_id': merchant_object
    })

    merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = merchant_business_id)

    for user in merchant_user_temp:
        merchant_user.append({
            'user_id': user.user_id
            })

    context['merchant_users'] = merchant_user

    # merchant_business.m_business_category.id = 11

    if merchant_business.m_business_category.id == 12:


        # Parking Dashboard ==>>

        parking_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__date = timezone.now(), is_pass = False).all()
        # parking_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id).all()

        total_bills = 0
        total_collection = 0
        total_flagged = 0

        for bill in parking_bills:
            total_bills += 1
            total_collection = total_collection + float(bill.amount)

            if bill.bill_flag == True:
                total_flagged = total_flagged + 1

        parking_pass = ParkingLotPass.objects.filter(m_business_id = merchant_business.id, created_at__date = timezone.now()).all()

        total_pass_collection = 0
        total_pass = 0

        for pass_temp in parking_pass:
            total_pass_collection = total_pass_collection + float(pass_temp.amount)
            total_pass = total_pass + 1

        context['total_bills'] = total_bills
        context['total_collection'] = total_collection + total_pass_collection
        context['total_flagged'] = total_flagged

        merchant_user_details = []

        if request.method == "POST":
            custom_user = request.POST['user']
            from_date = request.POST['from_date']
            from_date_temp = from_date
            to_date = request.POST['to_date']
            to_date_temp = to_date

            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')

            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%d-%m-%Y')

            for user in merchant_user:

                total_collection_bill = 0
                total_flagged = 0

                total_hours = ""

                parking_logs = ParkingLog.objects.filter(user_id = user['user_id'].id, created_at__date = timezone.now())

                if parking_logs:
                    login_at = parking_logs[0].login_at
                    logout_at = parking_logs[0].logout_at
                    # total_hours = logout_at - login_at
                else:
                    login_at = ""
                    logout_at = ""
                    total_hours = ""
                   
                bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, user_id = user['user_id'].id, is_pass = False).all()

                new_bills = []

                for bill in bills:
                    # print(bill.date)
                    # print(from_date)
                    if custom_user and from_date and to_date:
                        if bill.m_user_id == custom_user:
                            if bill.date >= from_date and bill.date <= to_date:
                                new_bills.append(bill)

                    elif from_date and to_date:
                        if bill.date >= from_date and bill.date <= to_date:
                            new_bills.append(bill)

                    elif custom_user and from_date:
                        if bill.m_user_id == custom_user and bill.date >= from_date:
                            new_bills.append(bill)

                    elif custom_user and to_date:
                        if bill.m_user_id == custom_user and bill.date <= to_date:
                            new_bills.append(bill)

                    elif from_date:
                        if bill.date >= from_date:
                            new_bills.append(bill)

                    elif to_date:
                        if bill.date <= to_date:
                            new_bills.append(bill)

                    elif custom_user:
                        if bill.m_user_id == custom_user:
                            new_bills.append(bill)

                total_bills = 0

                for bill in new_bills:

                    total_bills += 1

                    total_collection_bill = total_collection_bill + float(bill.amount)

                    if bill.bill_flag == True and bill.flag_by == str(user['user_id'].id):
                        total_flagged = total_flagged + 1

                name = user['user_id'].first_name + ' ' + user['user_id'].last_name


                parking_pass = ParkingLotPass.objects.filter(m_business_id = merchant_business.id, user_id = user['user_id'].id).all()

                new_pass = []

                for pass_temp in parking_pass:
                    pass_date = datetime.strptime(str(pass_temp.created_at.date()), '%Y-%m-%d').strftime('%d-%m-%Y')
                    if custom_user and from_date and to_date:
                        if pass_temp.user_id == custom_user:
                            if pass_date >= from_date and pass_date <= to_date:
                                new_pass.append(pass_temp)

                    elif from_date and to_date:
                        if pass_date >= from_date and pass_date <= to_date:
                            new_pass.append(pass_temp)

                    elif custom_user and from_date:
                        if pass_date == custom_user and pass_date >= from_date:
                            new_pass.append(pass_temp)

                    elif custom_user and to_date:
                        if pass_date == custom_user and pass_date <= to_date:
                            new_pass.append(pass_temp)

                    elif from_date:
                        if pass_date >= from_date:
                            new_pass.append(pass_temp)

                    elif to_date:
                        if pass_date <= to_date:
                            new_pass.append(pass_temp)

                    elif custom_user:
                        if pass_temp.m_user_id == custom_user:
                            new_pass.append(pass_temp)

                total_pass_collection = 0
                total_pass = 0
                
                for pass_temp in new_pass:
                    total_pass_collection = total_pass_collection + float(pass_temp.amount)
                    total_pass = total_pass + 1

                if custom_user:
                    if int(user['user_id'].id) == int(custom_user):
                        merchant_user_details.append({
                            'name': name,
                            'total_bills': total_bills,
                            'total_collection_bill': total_collection_bill,
                            'login_at': login_at,
                            'logout_at': logout_at,
                            'total_flagged': total_flagged,
                            'total_hours' : total_hours,
                            'total_pass_colletion': total_pass_collection,
                            'total_pass' : total_pass,
                            'total_collection': total_collection_bill + total_pass_collection
                        })
                else:
                    merchant_user_details.append({
                        'name': name,
                        'total_bills': total_bills,
                        'total_collection_bill': total_collection_bill,
                        'login_at': login_at,
                        'logout_at': logout_at,
                        'total_flagged': total_flagged,
                        'total_hours' : total_hours,
                        'total_pass_colletion': total_pass_collection,
                        'total_pass' : total_pass,
                        'total_collection': total_collection_bill + total_pass_collection
                    })

                if custom_user:
                    context['custom_user'] = int(custom_user)
                context['from_date'] = from_date_temp
                context['to_date'] = to_date_temp

        else:

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


                merchant_user_details.append({
                    'name': name,
                    'total_bills': total_bills,
                    'total_collection_bill': total_collection_bill,
                    'login_at': login_at,
                    'logout_at': logout_at,
                    'total_flagged': total_flagged,
                    'total_hours' : total_hours,
                    'total_pass_colletion': total_pass_collection,
                    'total_pass' : total_pass,
                    'total_collection': total_collection_bill + total_pass_collection
                })
                    
        context['merchant_user_details'] = merchant_user_details

        m_business_id = merchant_business_id
       
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
                "total_bills_made": total_bills_made
            })

        context['space_data'] = actual_space_data

        today = date.today()

        dailybillsChart = []
        dailyTotalCollectionChart = []

        start_date = str(today) + " 00:00:01"
        end_date = str(today) + " 04:00:00"
        petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 04:00:01"
        end_date = str(today) + " 08:00:00"
        petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 08:00:01"
        end_date = str(today) + " 12:00:00"
        petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 12:00:01"
        end_date = str(today) + " 16:00:00"
        petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 16:00:01"
        end_date = str(today) + " 20:00:00"
        petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 20:00:01"
        end_date = str(today) + " 23:59:59"
        petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.amount)
        dailyTotalCollectionChart.append(total_collection)

        dailybillsChart_list = ','.join(map(str, dailybillsChart))
        context['dailybillsChart_list'] = dailybillsChart_list

        dailyTotalCollectionChart_list = ','.join(map(str, dailyTotalCollectionChart))
        context['dailyTotalCollectionChart_list'] = dailyTotalCollectionChart_list

        vehicles = MerchantParkingAddVehicle.objects.filter(m_business_id = merchant_business_id).all()

        for vehicle in vehicles:

            vehiclestatusChart = []

            for i in range(1,13):
                year = today.year

                if i < 10:
                    month = "0" + str(i)

                petrol_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, vehicle_type = vehicle.vehicle_type, created_at__year = year, created_at__month = month).all()
                
                total_collection = 0

                for bill in petrol_bills:
                    total_collection = total_collection + float(bill.amount)
                # print(total_collection)

                vehiclestatusChart.append(total_collection)

            vehiclestatusChart_list = ','.join(map(str, vehiclestatusChart))

            vehicle.vehiclestatusChart_list = vehiclestatusChart_list

        context['vehiclestatusChart_list'] = vehicles

        productwiseCollectionchart_labels_temp = []
        productwiseCollectionchart_data_temp = []

        productWiseBillsdoughnutChart_labels_temp = []
        productWiseBillsdoughnutChart_data_temp = []

        for space in actual_space_data:
            vehicle_type_temp = "'" + space["vehicle_type"] + "'"
            productwiseCollectionchart_labels_temp.append(vehicle_type_temp)
            productwiseCollectionchart_data_temp.append(round(space['total_bills_made'],2))
            productWiseBillsdoughnutChart_labels_temp.append(vehicle_type_temp)
            productWiseBillsdoughnutChart_data_temp.append(space['vehicle_parked_count'])

        context['productwiseCollectionchart_labels'] = ','.join(map(str, productwiseCollectionchart_labels_temp))
        context['productwiseCollectionchart_data'] = ','.join(map(str, productwiseCollectionchart_data_temp))
        context['productWiseBillsdoughnutChart_labels'] = ','.join(map(str, productWiseBillsdoughnutChart_labels_temp))
        context['productWiseBillsdoughnutChart_data'] = ','.join(map(str, productWiseBillsdoughnutChart_data_temp))
        

    elif merchant_business.m_business_category.id == 11:
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__date = timezone.now()).all()
        # parking_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id).all()

        total_bills = 0
        total_collection = 0
        total_flagged = 0

        for bill in petrol_bills:
            total_bills += 1
            total_collection = total_collection + float(bill.total_amount)

            if bill.bill_flag == True:
                total_flagged = total_flagged + 1

        context['total_bills'] = total_bills
        context['total_collection'] = total_collection
        context['total_flagged'] = total_flagged

        merchant_user_details = []

        if request.method == "POST":
            custom_user = request.POST['user']
            from_date = request.POST['from_date']
            from_date_temp = from_date
            to_date = request.POST['to_date']
            to_date_temp = to_date

            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')

            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%d-%m-%Y')

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
                   
                bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, user_id = user['user_id'].id).all()

                new_bills = []

                for bill in bills:
                    # print(bill.date)
                    # print(from_date)
                    if custom_user and from_date and to_date:
                        if bill.m_user_id == custom_user:
                            if bill.date >= from_date and bill.date <= to_date:
                                new_bills.append(bill)

                    elif from_date and to_date:
                        if bill.date >= from_date and bill.date <= to_date:
                            new_bills.append(bill)

                    elif custom_user and from_date:
                        if bill.m_user_id == custom_user and bill.date >= from_date:
                            new_bills.append(bill)

                    elif custom_user and to_date:
                        if bill.m_user_id == custom_user and bill.date <= to_date:
                            new_bills.append(bill)

                    elif from_date:
                        if bill.date >= from_date:
                            new_bills.append(bill)

                    elif to_date:
                        if bill.date <= to_date:
                            new_bills.append(bill)

                    elif custom_user:
                        if bill.m_user_id == custom_user:
                            new_bills.append(bill)

                    

                total_bills = 0

                for bill in new_bills:

                    total_bills += 1

                    total_collection = total_collection + float(bill.total_amount)

                    if bill.bill_flag == True and bill.flag_by == str(user['user_id'].id):
                        total_flagged = total_flagged + 1

                name = user['user_id'].first_name + ' ' + user['user_id'].last_name

                if custom_user:
                    if int(user['user_id'].id) == int(custom_user):
                        merchant_user_details.append({
                            'name': name,
                            'total_bills': total_bills,
                            'total_collection': total_collection,
                            'login_at': login_at,
                            'logout_at': logout_at,
                            'total_flagged': total_flagged,
                        })
                else:
                    merchant_user_details.append({
                        'name': name,
                        'total_bills': total_bills,
                        'total_collection': total_collection,
                        'login_at': login_at,
                        'logout_at': logout_at,
                        'total_flagged': total_flagged,
                    })
                if custom_user:
                    context['custom_user'] = int(custom_user)
                context['from_date'] = from_date_temp
                context['to_date'] = to_date_temp

        else:

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
                merchant_user_details.append({
                    'name': name,
                    'total_bills': total_bills,
                    'total_collection': total_collection,
                    'login_at': login_at,
                    'logout_at': logout_at,
                    'total_flagged': total_flagged,
                })
                    
        context['merchant_user_details'] = merchant_user_details

        products = MerchantPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

        productSaledoughnutChart_data_temp = []
        productSaledoughnutChart_labels_temp = []

        for product in products:
            petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, product_id = product.id, created_at__date = timezone.now()).all()
            total_liter = 0
            total_amount = 0

            for bill in petrol_bills:
                total_liter = total_liter + float(bill.volume)
                total_amount = total_amount + float(bill.amount)


            product.total_liter_sold = total_liter
            product.total_amount_colleted = total_amount

            product_name_temp = "'" + product.product_name + "'"

            productSaledoughnutChart_labels_temp.append(product_name_temp)

            productSaledoughnutChart_data_temp.append(total_amount)

        context['products'] = products

        context['productSaledoughnutChart_data'] = ','.join(map(str, productSaledoughnutChart_data_temp))
        context['productSaledoughnutChart_labels'] = ','.join(map(str, productSaledoughnutChart_labels_temp))

        addon_products = AddonPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

        addonsSalesdoughnutchart_label_temp = []
        addonsSalesdoughnutchart_data_temp = []

        for addon_product in addon_products:

            petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__date = timezone.now()).all()

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

            product_name_temp = "'" + addon_product.product_name + "'"

            addonsSalesdoughnutchart_label_temp.append(product_name_temp)

            addonsSalesdoughnutchart_data_temp.append(amount_collected)

        context['addon_products'] = addon_products
        context['addonsSalesdoughnutchart_labels'] = ','.join(map(str, addonsSalesdoughnutchart_label_temp))
        context['addonsSalesdoughnutchart_data'] = ','.join(map(str, addonsSalesdoughnutchart_data_temp))

        today = date.today()

        dailybillsChart = []
        dailyTotalCollectionChart = []

        start_date = str(today) + " 00:00:01"
        end_date = str(today) + " 04:00:00"
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.total_amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 04:00:01"
        end_date = str(today) + " 08:00:00"
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.total_amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 08:00:01"
        end_date = str(today) + " 12:00:00"
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.total_amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 12:00:01"
        end_date = str(today) + " 16:00:00"
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.total_amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 16:00:01"
        end_date = str(today) + " 20:00:00"
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.total_amount)
        dailyTotalCollectionChart.append(total_collection)

        start_date = str(today) + " 20:00:01"
        end_date = str(today) + " 23:59:59"
        petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__range=(start_date, end_date)).all()
        dailybillsChart.append(petrol_bills.count())

        total_collection = 0
        for bill in petrol_bills:
            total_collection = total_collection + float(bill.total_amount)
        dailyTotalCollectionChart.append(total_collection)

        dailybillsChart_list = ','.join(map(str, dailybillsChart))
        context['dailybillsChart_list'] = dailybillsChart_list

        dailyTotalCollectionChart_list = ','.join(map(str, dailyTotalCollectionChart))
        context['dailyTotalCollectionChart_list'] = dailyTotalCollectionChart_list

        products = MerchantPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

        for product in products:

            productsalesChart = []

            for i in range(1,13):
                year = today.year

                if i < 10:
                    month = "0" + str(i)

                petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, product_id = product.id, created_at__year = year, created_at__month = month).all()
                
                total_collection = 0.0

                for bill in petrol_bills:
                    if bill.amount:
                        total_collection = total_collection + float(bill.amount)

                productsalesChart.append(total_collection)

            productsalesChart_list = ','.join(map(str, productsalesChart))

            product.productsalesChart_list = productsalesChart_list

        context['productsalesChart_list'] = products

    context['merchant_business_category_id'] = merchant_business.m_business_category.id
    context['segment'] = 'index'
    context['DashboardNavclass'] = 'active'
    # merchant-index-other-business.html
    # print(merchant_business.m_business_category.id)
    if merchant_business.m_business_category.id == 11 or merchant_business.m_business_category.id == 12:
        html_template = loader.get_template('merchant-index.html')
    else:

        total_transaction = 0

        total_transaction1 = CustomerBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), customer_added = False).count()

        total_transaction2 = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now()).count()

        total_transaction = total_transaction1 + total_transaction2

        context['total_transaction'] = total_transaction

        customer_bill = CustomerBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), customer_added = False).order_by('-id')

        merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now()).order_by('-id')

        total_collection = 0

        feedback_bill = []

        for bill in customer_bill:
            total_collection = total_collection + float(bill.bill_amount)

            try:
                bill_design = bill_designs.objects.get(merchant_business_id = bill.business_name.id)
                bill_rating_emoji = bill_design.rating_emoji
            except:
                bill_rating_emoji = "⭐"

            ratings = ""

            if bill.rating:
                for x in range(int(bill.rating)):
                    ratings = " ".join((ratings, bill_rating_emoji))
                
            bill.ratings = ratings

            if bill.feedback_submit == True:
                feedback_bill.append(bill)

        for bill in merchant_bill:
            total_collection = total_collection + float(bill.bill_amount)

            try:
                bill_design = bill_designs.objects.get(merchant_business_id = bill.business_name)
                bill_rating_emoji = bill_design.rating_emoji
            except:
                bill_rating_emoji = "⭐"

            ratings = ""

            if bill.rating:
                for x in range(int(bill.rating)):
                    ratings = " ".join((ratings, bill_rating_emoji))
                
            bill.ratings = ratings

            if bill.feedback_submit == True:
                feedback_bill.append(bill)

        context['feedback_bill'] = feedback_bill

        context['total_collection'] = total_collection

        average_billing = 0

        context['average_billing'] = average_billing

        context['print_transaction'] = sent_bill_history.objects.filter(
            m_business_id = merchant_business.id,
            created_at__date = timezone.now(),
            print_transaction = True
        ).count()

        context['green_bill_transaction'] = sent_bill_history.objects.filter(
            m_business_id = merchant_business.id,
            created_at__date = timezone.now(),
            green_bill_transaction = True
        ).count()

        context['green_bill_print_transaction'] = sent_bill_history.objects.filter(
            m_business_id = merchant_business.id,
            created_at__date = timezone.now(),
            green_bill_print_transaction = True
        ).count()

        context['total_transaction'] = context['green_bill_transaction'] + context['green_bill_print_transaction']

        total_rejected_transaction = 0

        total_rejected_transaction1 = CustomerBill.objects.filter(
            business_name = merchant_business, created_at__date = timezone.now(), reject_status = True, customer_added = False
        ).count()

        total_rejected_transaction2 = MerchantBill.objects.filter(
            business_name = merchant_business, created_at__date = timezone.now(), reject_status = True, customer_added = False
        ).count()

        context['total_rejected_transaction'] = total_rejected_transaction1 + total_rejected_transaction2

        subscription_object = getActiveSubscriptionPlan(request, merchant_business.id)

        context['subscription_object'] = subscription_object

        if subscription_object:
            percentage = ((float(subscription_object.recharge_amount) - float(subscription_object.total_amount_avilable))/subscription_object.recharge_amount) * 100
            remaining_subscription_percentage = 100 - percentage
            context['remaining_subscription_percentage'] = remaining_subscription_percentage

        html_template = loader.get_template('merchant/merchant-index-other-business-08-06-21.html')

    return HttpResponse(html_template.render(context, request))


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