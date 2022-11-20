# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

import os
import random
import sweetify
from django.contrib import messages
from django.db.models import Sum
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
from merchant_software_apis.models import *
from customer_bill.forms import Customer_Bill_Form
from users.models import MerchantProfile, Merchant_users
from parking_lot_apis.models import *
from coupon.models import *
from django.utils import timezone
from merchant_setting.models import *
from datetime import datetime, timedelta
from django.utils import formats
from petrol_pump_apis.models import *
from datetime import date
import calendar

import filetype
from django.db.models import Q
from django.db.models import Subquery
import random
import string

# SMS
import requests
import time
import pyshorteners

from django.utils.dateparse import parse_date

from my_subscription.models import sent_bill_history, merchant_subscriptions

from bill_design.models import bill_designs

from my_subscription.models import *

from payments.models import *

from partner_my_subscription.models import *
from my_subscription.models import recharge_history,promotional_sms_subscriptions,transactional_sms_subscriptions
from partner_my_subscription.models import partner_recharge_history
from django.db.models import Count

from my_subscription.models import *
from users.models import  PartnerProfile, MerchantProfile
from users.models import Partner_users
from partner_payment.models import PartnerPaymentLinks
from partner_my_subscription.models import *
from datetime import date
from subscription_plan.models import *
from customer_info.models import Customer_Info_Model

import requests
import time
import pyshorteners
from django.core.mail import get_connection, send_mail, BadHeaderError, EmailMessage

from offers.models import *

from referral_points.models import *

from promotions.models import *

from merchant_payment.models import *

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

    total_users = []
    total_customers = GreenBillUser.objects.filter(is_customer = True,is_active=True).count()
    total_users.append(total_customers)

    total_merchants = MerchantProfile.objects.filter(m_user_id__isnull=False,m_disabled_account=False).count()
    total_users.append(total_merchants)

    total_partners = PartnerProfile.objects.filter(p_disabled_account=False).count()
    total_users.append(total_partners)

    total_merchants = []
    active_merchants = []
    inactive_merchants = []
    excludes = ['11', '12']

    if PromotionsAmount.objects.all():
        amount = PromotionsAmount.objects.latest('id')
        offer_amount = amount.offer_amount
    else:
        offer_amount = 0
    today = date.today()
    total_offer_amount = 0
    offer_data = OfferModel.objects.filter(created_date__date = timezone.now(), status = 1)
    for offer in offer_data:
        if offer.valid_through <= today:
            expire_status=True
        if offer.customer_merchant_count:
            if offer.offer_panel == "owner":
                try:
                    total_amount = int(offer_amount) * int(offer.customer_merchant_count)
                    total_offer_amount = total_offer_amount + total_amount
                except:
                    pass
            else:
                if offer.status == '1':
                    try:
                        total_amount = int(offer_amount) * int(offer.customer_merchant_count)
                        total_offer_amount = total_offer_amount + total_amount
                    except:
                        pass

    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        coupon_amount = data.coupon_amount
    else:
        coupon_amount = 0

    coupon_list = CouponModel.objects.filter(created_date__date = timezone.now())
    total_coupon_amount = 0
    for coupon in coupon_list:
        if coupon.valid_through >= today:
            if coupon.total_customers:
                try:
                    total_amount = int(coupon_amount) * int(coupon.total_customers)
                    total_coupon_amount = total_coupon_amount + total_amount
                except:
                    pass


    third_party_ads_below_bill = ads_below_bill.objects.filter(ads_type = 'third_party', created_date__date = timezone.now(), status = 1)
    
    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        third_party_amount = data.third_party_ads_belowbill_amount
        green_bill_bills = data.green_bill_ads_belowbill_amount
    else:
        third_party_amount = 0
        green_bill_bills = 0

    third_party_total_amount = 0
    green_bill_total_amount = 0

    for ads in third_party_ads_below_bill:
        try:
            ads_amount = float(third_party_amount) * float(ads.third_party_total_transaction)
            third_party_total_amount = float(ads.ads_below_bill_amount) + float(third_party_total_amount)
        except:
            pass

    green_bill_space = ads_below_bill.objects.filter(ads_type = 'green_bill', created_date__date = timezone.now(), active_ads = True)

    for ads in green_bill_space:
        try:
            green_bill_ads_amount = float(green_bill_bills) * float(ads.third_party_total_transaction)
            green_bill_total_amount = float(green_bill_ads_amount) + float(green_bill_total_amount)
        except:
            pass

    bill_details = recharge_history.objects.filter(is_subscription_plan = True, purchase_date__date = timezone.now())

    total_greebill_subscription = 0
    for subscription in bill_details:
        if subscription:
            try:
                greenbill_plan = subscription_plan_details.objects.get(id = subscription.subscription_plan_id)
                users_cost = float(subscription.no_of_users) * float(subscription.valid_for_month) * float(greenbill_plan.cost_for_users)
                final_total = float(users_cost) + float(subscription.cost) + float(subscription.gst_amount)
                total_greebill_subscription = float(final_total) + float(total_greebill_subscription)
            except:
                greenbill_plan = ''
                users_cost = ''
                final_total = ''
                total_greebill_subscription = ''

    adon_plan_details = recharge_history.objects.filter(is_add_on_plan = True, purchase_date__date = timezone.now())
    total_adon_subscription = 0
    for subscription in adon_plan_details:
        if subscription.cost:
            try:
                total_adon_subscription = float(total_adon_subscription) + float(subscription.cost)
            except:
                total_adon_subscription = ''

    transactional_plan_details = recharge_history.objects.filter(is_transactional_sms_plan = True, purchase_date__date = timezone.now())
    partner_transactional_plan_details = partner_recharge_history.objects.filter(is_transactional_sms_plan = True, purchase_date__date = timezone.now())
    total_transactional_subscription = 0
    total_transactional_subscription1 = 0
    total_transactional_subscription2 = 0
    for subscription in transactional_plan_details:
        if subscription.cost:
            total_transactional_subscription1 = float(total_transactional_subscription1) + float(subscription.cost)
            

    for subscription in partner_transactional_plan_details:
        if subscription.cost:
            total_transactional_subscription2 = float(total_transactional_subscription1) + float(subscription.cost)

    total_transactional_subscription = float(total_transactional_subscription1) + float(total_transactional_subscription2)

                
    promotional_plan_details = recharge_history.objects.filter(is_promotional_sms_plan = True, purchase_date__date = timezone.now())
    partner_promotional_plan_details = partner_recharge_history.objects.filter(is_promotional_sms_plan = True, purchase_date__date = timezone.now())
    total_promotional_subscription = 0
    total_promotional_subscription1 = 0
    total_promotional_subscription2 = 0
    for subscription in promotional_plan_details:
        if subscription.cost:
            total_promotional_subscription1 = float(total_promotional_subscription1) + float(subscription.cost)

    for subscription in partner_promotional_plan_details:
        if subscription.cost:
            total_promotional_subscription2 = float(total_promotional_subscription2) + float(subscription.cost)

    total_promotional_subscription = float(total_promotional_subscription1) + float(total_promotional_subscription2)


    coupon_redeem_points = RedeemCouponModel.objects.filter(coupon_redeem_date__date = timezone.now())


    total_green_points = 0
    for coupon in coupon_redeem_points:
        if coupon.green_point:
            total_green_points = int(total_green_points) + int(coupon.green_point)


    # print('bill_details',total_greebill_subscription)


    # merchants date filter
    form_date_temp1 = ''
    to_date_temp1 = ''
    # if request.POST.get("submit") == "merchants_btn":
    if request.method == 'POST':
        form_date_temp1 = request.POST["from_date1"]
        to_date_temp1 = request.POST["to_date1"]

        total_parking = MerchantProfile.objects.filter(date_joined__range=(form_date_temp1,to_date_temp1),m_business_category__id='12',m_user_id__isnull=False,m_disabled_account=False).count()
        total_merchants.append(total_parking)

        total_petrolpump =MerchantProfile.objects.filter(date_joined__range=(form_date_temp1,to_date_temp1),m_business_category__id='11',m_user_id__isnull=False,m_disabled_account=False).count()
        total_merchants.append(total_petrolpump)

        total_other_business = MerchantProfile.objects.filter(date_joined__range=(form_date_temp1,to_date_temp1),m_user_id__isnull=False,m_disabled_account=False).exclude(m_business_category__in = excludes).count()
        total_merchants.append(total_other_business)


        active_parking = MerchantProfile.objects.filter(date_joined__range=(form_date_temp1,to_date_temp1),m_business_category__id='12',m_user_id__isnull=False,m_active_account=True,m_disabled_account=False).count()
        active_merchants.append(active_parking)

        inactive_parking = MerchantProfile.objects.filter(date_joined__range=(form_date_temp1,to_date_temp1),m_business_category__id='12',m_user_id__isnull=False,m_active_account=False,m_disabled_account=False).count()
        inactive_merchants.append(inactive_parking)

        active_petrolpump = MerchantProfile.objects.filter(date_joined__range=(form_date_temp1,to_date_temp1),m_business_category__id='11',m_user_id__isnull=False,m_active_account=True,m_disabled_account=False).count()
        active_merchants.append(active_petrolpump)

        inactive_petrolpump = MerchantProfile.objects.filter(date_joined__range=(form_date_temp1,to_date_temp1),m_business_category__id='11',m_user_id__isnull=False,m_active_account=False,m_disabled_account=False).count()
        inactive_merchants.append(inactive_petrolpump)

        active_other_business = MerchantProfile.objects.filter(date_joined__range=(form_date_temp1,to_date_temp1),m_user_id__isnull=False,m_active_account=True,m_disabled_account=False).exclude(m_business_category__in = excludes).count()
        active_merchants.append(active_other_business)

        inactive_other_business = MerchantProfile.objects.filter(date_joined__range=(form_date_temp1,to_date_temp1),m_user_id__isnull=False,m_active_account=False,m_disabled_account=False).exclude(m_business_category__in = excludes).count()
        inactive_merchants.append(inactive_other_business)

        # if total_merchants:
        #     for i in total_merchants:
        #         if i == 0:
                    # sweetify.success(request, title="Oops...", icon='error', text='Matched data not found.', timer=1500)
            

        context['total_merchants'] = total_merchants
        context['active_merchants'] = active_merchants
        context['inactive_merchants'] = inactive_merchants
        context['from_date1'] = form_date_temp1
        context['to_date1'] = to_date_temp1

    else:
        total_parking = MerchantProfile.objects.filter(m_business_category__id='12',m_user_id__isnull=False,m_disabled_account=False, date_joined__date = timezone.now()).values('m_user_id').count()
        total_merchants.append(total_parking)

        total_petrolpump =MerchantProfile.objects.filter(m_business_category__id='11',m_user_id__isnull=False,m_disabled_account=False, date_joined__date = timezone.now()).values('m_user_id').count()
        total_merchants.append(total_petrolpump)

        total_other_business = MerchantProfile.objects.filter(m_user_id__isnull=False,m_disabled_account=False, date_joined__date = timezone.now()).exclude(m_business_category__in = excludes).values('m_user_id').count()
        total_merchants.append(total_other_business)

        active_parking = MerchantProfile.objects.filter(m_business_category__id='12',m_user_id__isnull=False,m_active_account=True,m_disabled_account=False, date_joined__date = timezone.now()).values('m_user_id').count()
        active_merchants.append(active_parking)

        active_petrolpump = MerchantProfile.objects.filter(m_business_category__id='11',m_user_id__isnull=False,m_active_account=True,m_disabled_account=False, date_joined__date = timezone.now()).values('m_user_id').count()
        active_merchants.append(active_petrolpump)

        active_other_business = MerchantProfile.objects.filter(m_user_id__isnull=False,m_active_account=True,m_disabled_account=False, date_joined__date = timezone.now()).exclude(m_business_category__in = excludes).values('m_user_id').count()
        active_merchants.append(active_other_business)

        inactive_parking = MerchantProfile.objects.filter(m_business_category__id='12',m_user_id__isnull=False,m_active_account=False,m_disabled_account=False, date_joined__date = timezone.now()).values('m_user_id').count()
        inactive_merchants.append(inactive_parking)

        inactive_petrolpump = MerchantProfile.objects.filter(m_business_category__id='11',m_user_id__isnull=False,m_active_account=False,m_disabled_account=False, date_joined__date = timezone.now()).values('m_user_id').count()
        inactive_merchants.append(inactive_petrolpump)

        inactive_other_business = MerchantProfile.objects.filter(m_user_id__isnull=False,m_active_account=False,m_disabled_account=False, date_joined__date = timezone.now()).exclude(m_business_category__in = excludes).values('m_user_id').count()
        inactive_merchants.append(inactive_other_business)
       


    total_users.append(total_merchants)
    
    #customer category performance date filter
    bill_categories = []
    bill_categories_count = []
    final_bill_categories = []
    final_categories_count = []
    form_date_temp2 = ''
    to_date_temp2 = ''
    # if request.POST.get("submit") == 'customer_category_btn':
    if request.method == 'POST':
        # form_date_temp2 = request.POST["from_date2"]
        # to_date_temp2 = request.POST["to_date2"]

        Customer_bills = CustomerBill.objects.filter(bill_date__range=(form_date_temp1,to_date_temp1))
        customer_bills_cat = Customer_bills.values('customer_bill_category__bill_category_name').annotate(cat_count=Count('customer_bill_category__bill_category_name')).order_by('-cat_count')
        for cat in customer_bills_cat:
            bill_categories.append(cat['customer_bill_category__bill_category_name'])
            bill_categories_count.append(cat['cat_count'])

        for i in bill_categories:
            if i != None :
                final_bill_categories.append(i)

        for j in bill_categories_count:
            if j != 0 :
                final_categories_count.append(j)

        if not final_categories_count:
            sweetify.success(request, title="Oops...", icon='error', text='Matched data not found.', timer=1500)

        context['labels'] = final_bill_categories
        context['category_count'] = final_categories_count

    else:
        Customer_bills = CustomerBill.objects.filter(created_at__date = timezone.now())
        customer_bills_cat = Customer_bills.values('customer_bill_category__bill_category_name').annotate(cat_count=Count('customer_bill_category__bill_category_name')).order_by('-cat_count')
        for cat in customer_bills_cat:
            bill_categories.append(cat['customer_bill_category__bill_category_name'])
            bill_categories_count.append(cat['cat_count'])


        for i in bill_categories:
            if i != None :
                final_bill_categories.append(i)

        for j in bill_categories_count:
            if j != 0 :
                final_categories_count.append(j)      
    
        
    new_registrations=[]
    new_merchants = MerchantProfile.objects.filter(m_disabled_account=False,date_joined__date = timezone.now()).exclude(m_business_category__in = excludes).values('m_user_id').distinct().count()
    new_registrations.append(new_merchants)

    new_customers = GreenBillUser.objects.filter(is_customer = True,date_joined__date = timezone.now()).count()
    new_registrations.append(new_customers)

    new_partners = PartnerProfile.objects.filter(p_disabled_account=False,date_joined__date = timezone.now()).count()
    new_registrations.append(new_partners)

    new_parking_merchant = MerchantProfile.objects.filter(m_business_category__id='12',m_disabled_account=False,date_joined__date = timezone.now()).values('m_user_id').distinct().count()
    new_registrations.append(new_parking_merchant)

    new_petrol_pump_merchant = MerchantProfile.objects.filter(m_business_category__id='11',m_user_id__isnull = False,m_disabled_account=False,date_joined__date = timezone.now()).values('m_user_id').distinct().count()
    new_registrations.append(new_petrol_pump_merchant)
 
    merchant_sms_data = []
    partner_sms_data = []
    merchant_digital_bills_data = []

    if request.method == 'POST':
        customer_bill = CustomerBill.objects.filter(customer_added = False, created_at__range=(form_date_temp1,to_date_temp1))
        merchant_bill = MerchantBill.objects.filter(created_at__range=(form_date_temp1,to_date_temp1))

        parking_bill_list = SaveParkingLotBill.objects.filter(is_pass = False, created_at__range=(form_date_temp1,to_date_temp1))
        petrol_bill_list = SavePetrolPumpBill.objects.filter(created_at__range=(form_date_temp1,to_date_temp1))
    else:
        customer_bill = CustomerBill.objects.filter(customer_added = False)
        merchant_bill = MerchantBill.objects.all()

        parking_bill_list = SaveParkingLotBill.objects.filter(is_pass = False)
        petrol_bill_list = SavePetrolPumpBill.objects.all()

    sent_bill_count = 0
    try:
        for bill in customer_bill:
            sent_bill_count = sent_bill_count + 1

        for bill in merchant_bill:
            sent_bill_count = sent_bill_count + 1

        for bill in parking_bill_list:
            sent_bill_count = sent_bill_count + 1

        for bill in petrol_bill_list:
            sent_bill_count = sent_bill_count + 1


        digital_sent = 0
        for bill in customer_bill:
            if bill.greenbill_digital_bill == "True":
                digital_sent = digital_sent + 1

        for bill in merchant_bill:
            if bill.greenbill_digital_bill == "True":
                digital_sent = digital_sent + 1

        for bill in parking_bill_list:
            if bill.greenbill_digital_bill == "True":
                digital_sent = digital_sent + 1

        for bill in petrol_bill_list:
            if bill.greenbill_digital_bill == "True":
                digital_sent = digital_sent + 1


        sms_sent = 0
        for bill in customer_bill:
            if bill.greenbill_sms_bill == "True":
                sms_sent = sms_sent + 1

        for bill in merchant_bill:
            if bill.greenbill_sms_bill == "True":
                sms_sent = sms_sent + 1

        for bill in parking_bill_list:
            if bill.greenbill_sms_bill == "True":
                sms_sent = sms_sent + 1

        for bill in petrol_bill_list:
            if bill.greenbill_sms_bill == "True":
                sms_sent = sms_sent + 1


        sent_bill_count = int(sent_bill_count)
    except:
        sms_sent = 0
        digital_sent = 0

    try:
        merchant_digital_bills_data.append(sms_sent)
        merchant_digital_bills_data.append(digital_sent)
    except:
        merchant_digital_bills_data.append(0)
        merchant_digital_bills_data.append(0)

    if request.method == 'POST':
        petrol_bill_notification = petrol_pump_app_setting_model.objects.filter(created_at__range=(form_date_temp1,to_date_temp1))
        parking_bill_notification = parking_app_setting_model.objects.filter(digital_bill=True, created_at__range=(form_date_temp1,to_date_temp1))
    else:
        petrol_bill_notification = petrol_pump_app_setting_model.objects.all()
        parking_bill_notification = parking_app_setting_model.objects.filter(digital_bill=True)

    try:

        petrol_notification_count = sum(petrol_bill_notification.values_list('digital_bill', flat=True))

        parking_notification_count = sum(parking_bill_notification.values_list('digital_bill', flat=True))

        total_bill_notification = petrol_notification_count + parking_notification_count

        merchant_digital_bills_data.append(total_bill_notification)
    except:

        merchant_digital_bills_data.append(0)


    if request.method == 'POST':

        try:
            total_tran_sms = transactional_sms_subscriptions.objects.filter(is_active = True, purchase_date__range=(form_date_temp1,to_date_temp1)).aggregate(Sum('total_sms'))['total_sms__sum']
            total_tran_sms_available = transactional_sms_subscriptions.objects.filter(is_active = True, purchase_date__range=(form_date_temp1,to_date_temp1)).aggregate(Sum('total_sms_avilable'))['total_sms_avilable__sum']
            transactional_sent_sms = total_tran_sms - total_tran_sms_available
            merchant_sms_data.append(transactional_sent_sms)
        except:
            merchant_sms_data.append(0)

        try:
            total_promo_sms = promotional_sms_subscriptions.objects.filter(is_active = True, purchase_date__range=(form_date_temp1,to_date_temp1)).aggregate(Sum('total_sms'))['total_sms__sum']
            total_promo_sms_available = promotional_sms_subscriptions.objects.filter(is_active = True, purchase_date__range=(form_date_temp1,to_date_temp1)).aggregate(Sum('total_sms_avilable'))['total_sms_avilable__sum']
            promotional_sent_sms = total_promo_sms - total_promo_sms_available
            merchant_sms_data.append(promotional_sent_sms)
        except:
            merchant_sms_data.append(0)

        try:
            part_total_tran_sms = partner_transactional_sms_subscriptions.objects.filter(is_active = True, purchase_date__range=(form_date_temp1,to_date_temp1)).aggregate(Sum('total_sms'))['total_sms__sum']
            part_total_tran_sms_available = partner_transactional_sms_subscriptions.objects.filter(is_active = True, purchase_date__range=(form_date_temp1,to_date_temp1)).aggregate(Sum('total_sms_avilable'))['total_sms_avilable__sum']
            part_transactional_sent_sms = part_total_tran_sms - part_total_tran_sms_available 
            partner_sms_data.append(part_transactional_sent_sms)
        except:
            partner_sms_data.append(0)
        try:
            part_total_promo_sms = partner_promotional_sms_subscriptions.objects.filter(is_active = True, purchase_date__range=(form_date_temp1,to_date_temp1)).aggregate(Sum('total_sms'))['total_sms__sum']
            part_total_promo_sms_available = partner_promotional_sms_subscriptions.objects.filter(is_active = True, purchase_date__range=(form_date_temp1,to_date_temp1)).aggregate(Sum('total_sms_avilable'))['total_sms_avilable__sum']
            promotional_sent_sms = part_total_promo_sms - part_total_promo_sms_available
            partner_sms_data.append(promotional_sent_sms)
        except:
            part_total_promo_sms = ''
            part_total_promo_sms_available = ''
            promotional_sent_sms = ''
            partner_sms_data.append(0)

     
    else:   

        try:
            total_tran_sms = transactional_sms_subscriptions.objects.filter(is_active = True).aggregate(Sum('total_sms'))['total_sms__sum']
            total_tran_sms_available = transactional_sms_subscriptions.objects.filter(is_active = True).aggregate(Sum('total_sms_avilable'))['total_sms_avilable__sum']
            transactional_sent_sms = total_tran_sms - total_tran_sms_available
            merchant_sms_data.append(transactional_sent_sms)
        except:
            merchant_sms_data.append(0)

        try:
            total_promo_sms = promotional_sms_subscriptions.objects.filter(is_active = True).aggregate(Sum('total_sms'))['total_sms__sum']
            total_promo_sms_available = promotional_sms_subscriptions.objects.filter(is_active = True).aggregate(Sum('total_sms_avilable'))['total_sms_avilable__sum']
            promotional_sent_sms = total_promo_sms - total_promo_sms_available
            merchant_sms_data.append(promotional_sent_sms)
        except:
            merchant_sms_data.append(0)

        try:
            part_total_tran_sms = partner_transactional_sms_subscriptions.objects.filter(is_active = True).aggregate(Sum('total_sms'))['total_sms__sum']
            part_total_tran_sms_available = partner_transactional_sms_subscriptions.objects.filter(is_active = True).aggregate(Sum('total_sms_avilable'))['total_sms_avilable__sum']
            part_transactional_sent_sms = part_total_tran_sms - part_total_tran_sms_available 
            partner_sms_data.append(part_transactional_sent_sms)
        except:
            partner_sms_data.append(0)
        try:
            part_total_promo_sms = partner_promotional_sms_subscriptions.objects.filter(is_active = True).aggregate(Sum('total_sms'))['total_sms__sum']
            part_total_promo_sms_available = partner_promotional_sms_subscriptions.objects.filter(is_active = True).aggregate(Sum('total_sms_avilable'))['total_sms_avilable__sum']
            promotional_sent_sms = part_total_promo_sms - part_total_promo_sms_available
            partner_sms_data.append(promotional_sent_sms)
        except:
            part_total_promo_sms = ''
            part_total_promo_sms_available = ''
            promotional_sent_sms = ''
            partner_sms_data.append(0)


    partner_subscription_billing = partner_recharge_history.objects.filter(partner_id__is_partner=True,purchase_date=date.today()).count()
    merchant_subscription_billing = recharge_history.objects.filter(merchant_id__is_merchant=True,purchase_date=date.today()).count()
    promotional_sms = promotional_sms_subscriptions.objects.filter(merchant_id__is_merchant=True,purchase_date=date.today()).count()
    transactional_sms = transactional_sms_subscriptions.objects.filter(merchant_id__is_merchant=True,purchase_date=date.today()).count()

    exe_send_and_print_bill_status1 = CustomerBill.objects.filter(created_at__date = timezone.now(), exe_bill_type = 2).count()

    exe_send_and_print_bill_status2 = MerchantBill.objects.filter(created_at__date = timezone.now(), exe_bill_type = 2).count()

    exe_send_bill_status1 = CustomerBill.objects.filter(created_at__date = timezone.now(), exe_bill_type = 1).count()

    exe_send_bill_status2 = MerchantBill.objects.filter(created_at__date = timezone.now(), exe_bill_type = 1).count()

    exe_print_bill_status = ExePrintStatus.objects.filter(created_at__date = timezone.now()).count()

    send_print_bill_count = int(exe_send_and_print_bill_status1) + int(exe_send_and_print_bill_status2)

    send_bill_count = int(exe_send_bill_status1) + int(exe_send_bill_status2)


    context={
        'send_bill_count':send_bill_count,
        'send_print_bill_count':send_print_bill_count,
        'exe_print_bill_status':exe_print_bill_status,
        'total_users':total_users,
        'total_offer_amount':total_offer_amount,
        'green_bill_total_amount': green_bill_total_amount,
        'third_party_total_amount': third_party_total_amount,
        'total_coupon_amount': total_coupon_amount,
        'total_greebill_subscription' : total_greebill_subscription,
        'total_adon_subscription': total_adon_subscription,
        'total_transactional_subscription': total_transactional_subscription,
        'total_promotional_subscription':total_promotional_subscription,
        'total_green_points': total_green_points,
        'active_merchants':active_merchants,
        'inactive_merchants':inactive_merchants,
        'total_merchants':total_merchants,
        'from_date1': form_date_temp1,
        'to_date1': to_date_temp1,

        'from_date2': form_date_temp2,
        'to_date2': to_date_temp2,

        'merchant_sms_data':merchant_sms_data,
        'partner_sms_data':partner_sms_data,

        'merchant_digital_bills_data':merchant_digital_bills_data,
        
        'new_registrations':new_registrations,

        'partner_subscription_billing_count':partner_subscription_billing,
        'merchant_subscription_billing_count':merchant_subscription_billing,

        'promotional_sms_count':promotional_sms,
        'transactional_sms_count':transactional_sms,


        'labels':final_bill_categories,
        'category_count':final_categories_count,
    }

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

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    active_promotional_plan = promotional_sms_subscriptions.objects.filter(merchant_id= request.user, is_active=True, low_sms_balance= False)

    try:
        for plan in active_promotional_plan:

            total_sms = promotional_subscription_plan_model.objects.get(id= plan.subscription_id).total_sms

            
            ten_percent_total_sms = (int(total_sms) * 10) / 100
            

            if plan.total_sms_avilable <= ten_percent_total_sms:
                check_promotional_plan = promotional_sms_subscriptions.objects.filter(id= plan.id).update(low_sms_balance= True)

                recharge_url = "http://157.230.228.250/recharge/"
                         

                s = pyshorteners.Shortener()

                short_url = s.tinyurl.short(recharge_url)


                merchant_email = GreenBillUser.objects.get(mobile_no= request.user).m_email
                
                subject = 'Low Balance'
                message = f' Hey GreenBill Merchant, \n\n I hope you’re doing well. \n\n This email is to tell you that your SMS balance is too low.Kindly recharge your account as soon as possible to keep delivering your invoices to your customers hassle-free. You can recharge for any amount according to your convenience. Below is the link for payment. \n\n Best Regards,\n\n Green Bill Team.' '\n\n Recharge Url: ' + str(recharge_url)
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [merchant_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()

    except:
        ''
    active_transactional_plan = transactional_sms_subscriptions.objects.filter(merchant_id= request.user, is_active=True, low_sms_balance= False)
    try:
        for plan in active_transactional_plan:

            total_sms = transactional_subscription_plan_model.objects.get(id= plan.subscription_id).total_sms

            ten_percent_total_sms = (int(total_sms) * 10) / 100

            if plan.total_sms_avilable <= ten_percent_total_sms:

                check_transactional_plan = transactional_sms_subscriptions.objects.filter(id= plan.id).update(low_sms_balance= True)

                recharge_url = "http://157.230.228.250/recharge/"
                         

                s = pyshorteners.Shortener()

                short_url = s.tinyurl.short(recharge_url)


                merchant_email = GreenBillUser.objects.get(mobile_no= request.user).m_email
                
                subject = 'Low Balance'
                message = f' Hey GreenBill Merchant, \n\n I hope you’re doing well. \n\n This email is to tell you that your SMS balance is too low.Kindly recharge your account as soon as possible to keep delivering your invoices to your customers hassle-free. You can recharge for any amount according to your convenience. Below is the link for payment. \n\n Best Regards,\n\n Green Bill Team.' '\n\n Recharge Url: ' + str(recharge_url)
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [merchant_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()
    except:
        ''


    active_green_bill_plan_for_current_day = merchant_subscriptions.objects.filter(merchant_id= request.user, is_active=True, expired_plan= False)

    today = date.today()
        

        
    try:
        for plans in active_green_bill_plan_for_current_day:
            expiry_date = datetime.strptime(str(plans.expiry_date), '%d-%m-%Y').strftime('%Y-%m-%d')

            if str(today) == expiry_date:

                today_expired = merchant_subscriptions.objects.filter(id=plans.id).update(expired_plan=True)

                recharge_url = "http://157.230.228.250/recharge/"
                         

                s = pyshorteners.Shortener()

                short_url = s.tinyurl.short(recharge_url)


                merchant_email = GreenBillUser.objects.get(mobile_no= request.user).m_email
                
                subject = 'Membership will be expire today'
                message = f' Hey GreenBill Merchant, \n\n This is reminder that your membership with GreenBill will be expired today. Renew today before your benefits and services are suspended. \n\n' 'RENEW NOW ' + str(recharge_url) + '\n\n if you have any questions regarding renewal process or need help, please do not hegitate to contact us at support@greenbill.in \n\n Cheers, \n Team GreenBill.'
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [merchant_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()
     
        import datetime as DT
    except:
        ''
        

    active_green_bill_plan_for_one_week = merchant_subscriptions.objects.filter(merchant_id= request.user, is_active=True, one_week_expiry= False)
    try:
        for plans in active_green_bill_plan_for_one_week:

            expiry_date = datetime.strptime(str(plans.expiry_date), '%d-%m-%Y').strftime('%Y-%m-%d')

            date_time_obj = datetime.strptime(expiry_date, '%Y-%m-%d')

            now = datetime.strptime(str(today), '%Y-%m-%d')

            week_before = date_time_obj - timedelta(days=7)

            if week_before == now:

                today_expired = merchant_subscriptions.objects.filter(id=plans.id).update(one_week_expiry=True)

                recharge_url = "http://157.230.228.250/recharge/"
                         

                s = pyshorteners.Shortener()

                short_url = s.tinyurl.short(recharge_url)


                merchant_email = GreenBillUser.objects.get(mobile_no= request.user).m_email
                
                subject = 'Membership will be expire after 1 week'
                message = f' Hey GreenBill Merchant, \n\n Your subscription is about to expire within a week. Renew today before your benefits and services are suspended. \n\n' 'RENEW NOW ' + str(recharge_url) + '\n\n if you have any questions regarding renewal process or need help, please do not hegitate to contact us at support@greenbill.in \n\n Cheers, \n Team GreenBill.'
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [merchant_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()
    except:
        ''


    active_green_bill_plan_before_one_month = merchant_subscriptions.objects.filter(merchant_id= request.user, is_active=True, one_month_expiry= False)
    try:

        for plans in active_green_bill_plan_before_one_month:

            expiry_date = datetime.strptime(str(plans.expiry_date), '%d-%m-%Y').strftime('%Y-%m-%d')

            date_time_obj = datetime.strptime(expiry_date, '%Y-%m-%d')

            now = datetime.strptime(str(today), '%Y-%m-%d')

            week_before = date_time_obj - timedelta(days=30)

            if week_before == now:

                today_expired = merchant_subscriptions.objects.filter(id=plans.id).update(one_month_expiry=True)

                recharge_url = "http://157.230.228.250/recharge/"
                         

                s = pyshorteners.Shortener()

                short_url = s.tinyurl.short(recharge_url)


                merchant_email = GreenBillUser.objects.get(mobile_no= request.user).m_email
                
                subject = 'Membership will be expire after 1 month'
                message = f' Hey GreenBill Merchant, \n\n Your membership at GreenBill is about to expire on date ' + str(plans.expiry_date) + '. We hope you are enjoying benefits of your membership \n\n Good News! There is still time to renew, and it is as easy ever - just click the link below and follow the instructions. it takes just 5 minutes of your time. \n\n Renew Now ' + str(recharge_url) + '\n\n if you have any questions regarding renewal process or need help, please do not hegitate to contact us at support@greenbill.in \n\n Cheers, \n Team GreenBill.'
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [merchant_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()

    except:
        ''

        

        # print(plans.expiry_date - DT.timedelta(days=7))

        # week_ago = expiry_date - str(DT.timedelta(days=7))

        # print('week_ago',week_ago)

        
        #     print('hi')

        #     today_expired = merchant_subscriptions.objects.filter(id=plans.subscription_id).update(one_week_expiry=True)

        #     recharge_url = "http://157.230.228.250:8001/recharge/"
                     

        #     s = pyshorteners.Shortener()

        #     short_url = s.tinyurl.short(recharge_url)


        #     merchant_email = GreenBillUser.objects.get(mobile_no= request.user).m_email
            
        #     subject = 'Low Balance'
        #     message = f' Hey GreenBill Merchant, \n\n I hope you’re doing well. \n\n This email is to tell you that your SMS balance is too low.Kindly recharge your account as soon as possible to keep delivering your invoices to your customers hassle-free. You can recharge for any amount according to your convenience. Below is the link for payment. \n\n Best Regards,\n\n Green Bill Team.' '\n\n Recharge Url: ' + str(recharge_url)
        #     email_from = settings.EMAIL_HOST_USER
           
        #     recipient_list = [merchant_email,]
            
        #     send_res = EmailMessage( subject, message, email_from, recipient_list)

        #     response = send_res.send()


    #subcript_id = promotional_sms_subscriptions.objects.get()
    # context = {} 
    # context['segment'] = 'index'
    # context['DashboardNavclass'] = 'active'
    # html_template = loader.get_template('merchant-index.html')
    context = {}
    mobile_no = ''
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
        total_online_collection = 0

        for bill in parking_bills:
            total_bills += 1

            if bill.amount and bill.payment_done == False:
                total_collection = total_collection + float(bill.amount)

            if bill.amount and bill.payment_done == True:
                total_online_collection = total_online_collection + float(bill.amount)

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
        context['total_online_collection'] = total_online_collection

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
        years_list = []
        years_next = []

        petrol_bills_years = SaveParkingLotBill.objects.order_by().values('created_at__year').distinct() 
        for year in petrol_bills_years:
            years_list.append(year['created_at__year'])
            years_next.append(year['created_at__year'] + 1)
        yearslist=zip(years_list, years_next)
        if request.POST.get('submit') == 'bills_collection_btn':
            years = request.POST["years"]
            years_value = int(years)

            search_from_year = years_value
            search_to_year = years_value + 1 

            # vehicles = MerchantParkingAddVehicle.objects.filter(m_business_id = merchant_business_id).all()
            # for vehicle in vehicles:

            vehiclestatusChart1 = []
            month3 = []
            year3 = []
            for i in range(4,13):
                y1 = years_value
                year3.append(y1)
                if i < 10:
                    m1 = "0" + str(i)
                    month3.append(m1)
                else:
                    month3.append(i)

            for j in range(1,4):
                y2 = years_value + 1
                year3.append(y2)
                if j < 10:
                    m2 = "0" + str(j)
                    month3.append(m2)
            for year,month in zip(year3,month3):
                
                parking_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__year = year, created_at__month = month).all()
                total_collection = 0

                for bill in parking_bills:
                    total_collection = total_collection + float(bill.amount)

                decimal_value = format(float(total_collection), ".2f")
                vehiclestatusChart1.append(decimal_value)

            # vehiclestatusChart_list = ','.join(map(str, vehiclestatusChart))
            # vehicle.vehiclestatusChart_list = vehiclestatusChart_list  

            context['search_from_year'] = search_from_year
            context['search_to_year'] = search_to_year 
            if years_value:
                context['years_value'] = years_value                 

   
        else:
            today = date.today()
            # vehicles = MerchantParkingAddVehicle.objects.filter(m_business_id = merchant_business_id).all()

            # for vehicle in vehicles:

            vehiclestatusChart1 = []
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
                
                parking_bills = SaveParkingLotBill.objects.filter(m_business_id = merchant_business.id, created_at__year = year, created_at__month = month).all()
                total_collection = 0

                for bill in parking_bills:
                    total_collection = total_collection + float(bill.amount)

                decimal_value = format(float(total_collection), ".2f")
                vehiclestatusChart1.append(decimal_value)

            # vehiclestatusChart_list = ','.join(map(str, vehiclestatusChart))
            # vehiclestatusChart_list = vehiclestatusChart
            context['vehiclestatusChart_list1'] = vehiclestatusChart1


        context['vehiclestatusChart_list1'] = vehiclestatusChart1
        context['current_year'] = current_year
        context['next_year'] = next_year
        context['yearslist'] = yearslist
        context['years_list'] = years_list
        # context['search_to_date'] = search_to_date  
        m_business_id = merchant_business_id
       
        space_data = MerchantParkingLotSpace.objects.filter(m_business_id = m_business_id)

        actual_space_data = []

        space_record = []
        vehical_from_date = ''
        vehical_to_date = ''
        if request.POST.get('submit') == 'vehical_type_wise_collection_btn':
            DATE_FORMAT = '%Y-%m-%d'
            vehical_from_date = request.POST['vehical_from_date']
            vehical_to_date = request.POST['vehical_to_date']

            date_time_obj = datetime.strptime(vehical_to_date, '%Y-%m-%d')
            day_later = date_time_obj + timedelta(days=1)
            x = day_later.date()
            ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

            vehical_start_date = datetime.strptime(str(vehical_from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = vehical_start_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            # vehical_end_date = datetime.strptime(str(vehical_to_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            # end_date = vehical_end_date.split('-')
            # end_date = date(int(end_date[2]), int(end_date[1]), int(end_date[0]))
            # ed_filter = end_date.strftime(DATE_FORMAT)

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
                    "total_bills_made": total_bills_made
                })

        else:

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
        context['from_date'] = vehical_from_date
        context['to_date'] = vehical_to_date

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
        total_online_collection = 0

        for bill in petrol_bills:
            total_bills += 1

            if bill.total_amount and bill.payment_done == False:
                total_collection = total_collection + float(bill.total_amount)

            if bill.total_amount and bill.payment_done == True:
                total_online_collection = total_online_collection + float(bill.total_amount)

            if bill.bill_flag == True:
                total_flagged = total_flagged + 1

        context['total_bills'] = total_bills
        context['total_collection'] = total_collection
        context['total_flagged'] = total_flagged
        context['total_online_collection'] = total_online_collection

        merchant_user_details = []

        # if request.method == "POST":
        from_date = ''
        to_date = ''
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
        years_list = []
        years_next = []
        petrol_bills_years = SavePetrolPumpBill.objects.order_by().values('created_at__year').distinct()
        for year in petrol_bills_years:
            years_list.append(year['created_at__year'])
            years_next.append(year['created_at__year'] + 1)
        yearslist=zip(years_list, years_next)

        if request.POST.get('submit') == 'bills_collection_petrol_pump':
            years = request.POST['years']
            years_value = int(years)

            search_from_year = years_value
            search_to_year = years_value + 1

            # products = MerchantPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

            # for product in products:
            productsalesChart1 = []
            month3 = []
            year3 = []
            for i in range(4,13):
                y1 = years_value
                year3.append(y1)
                if i < 10:
                    m1 = "0" + str(i)
                    month3.append(m1) 
                else:
                    month3.append(i)
            for j in range(1,4):
                y2 = years_value + 1
                year3.append(y2)
                if j < 10:
                    m2 = "0" + str(j)
                    month3.append(m2)
            for year,month in zip(year3,month3):

                petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__year = year, created_at__month = month).all()
                
                total_collection = 0

                # for bill in petrol_bills:
                    # if bill.amount:
                    #     amount1 = float(str(bill.amount))
                    #     total_collection = total_collection + amount1
                for bill in petrol_bills:
                    if bill.amount:
                        total_collection = total_collection + float(bill.total_amount)

                decimal_value = format(float(total_collection), ".2f")
                productsalesChart1.append(total_collection)


            # productsalesChart_list = ','.join(map(str, productsalesChart))
            # product.productsalesChart_list = productsalesChart_list

            context['search_from_year'] = search_from_year
            context['search_to_year'] = search_to_year 
            if years_value:
                context['years_value'] = years_value 

        else:
            # products = MerchantPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

            # for product in products:

            productsalesChart1 = []
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

                petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__year = year, created_at__month = month).all()
                
                total_collection = 0

                for bill in petrol_bills:
                    if bill.amount:
                        total_collection = total_collection + float(bill.total_amount)
                        
                decimal_value = format(float(total_collection), ".2f")
                productsalesChart1.append(decimal_value)

            # productsalesChart_list = ','.join(map(str, productsalesChart))

            # product.productsalesChart_list = productsalesChart_list

        context['productsalesChart_list1'] = productsalesChart1
        context['current_year'] = current_year
        context['next_year'] = next_year
        context['years_list'] = years_list
        context['yearslist'] = yearslist


        products = MerchantPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

        products1 = MerchantPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

        for product in products1:
            petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, product_id = product.id, created_at__date = timezone.now()).all()
            total_liter = 0
            total_amount = 0

            for bill in petrol_bills:
                if bill.volume:
                    total_liter = total_liter + float(bill.volume)
                if bill.amount:
                    total_amount = total_amount + float(bill.amount)


            product.total_liter_sold = total_liter
            product.total_amount_colleted = total_amount

            product_name_temp = "'" + product.product_name + "'"

        productSaledoughnutChart_data_temp = []
        productSaledoughnutChart_labels_temp = []
        product_start_date = ''
        product_end_date = ''
        
        if request.POST.get('submit') == 'product_sales_form_btn':

            DATE_FORMAT = '%Y-%m-%d'
            product_start_date = request.POST['product_start_date']
            product_end_date = request.POST['product_end_date']

            DATE_FORMAT = '%Y-%m-%d'
            date_time_obj = datetime.strptime(product_end_date, '%Y-%m-%d')
            day_later = date_time_obj + timedelta(days=1)
            x = day_later.date()
            ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

            billing_from_date = datetime.strptime(str(product_start_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = billing_from_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            for product in products:
                petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, product_id = product.id, created_at__gte = sd_filter, created_at__lte = ed_filter).all()


                total_liter = 0
                total_amount = 0

                for bill in petrol_bills:
                    
                    if bill.volume:
                        # print(bill.volume)
                        total_liter = total_liter + float(bill.volume)
                        # print('11',total_liter)
                    if bill.amount:
                        # print(bill.amount)
                        total_amount = total_amount + float(bill.amount)
                        # print('22',total_amount)


                product.total_liter_sold = total_liter
                product.total_amount_colleted = total_amount

                product_name_temp = "'" + product.product_name + "'"

                productSaledoughnutChart_labels_temp.append(product_name_temp)

                productSaledoughnutChart_data_temp.append(total_amount)

                # print(productSaledoughnutChart_data_temp)
                
        else:
            sd_filter = ''
            product_end_date = ''
            
            for product in products:
                petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, product_id = product.id, created_at__date = timezone.now()).all()
                total_liter = 0
                total_amount = 0

                for bill in petrol_bills:
                    if bill.volume:
                        total_liter = total_liter + float(bill.volume)
                    if bill.amount:
                        total_amount = total_amount + float(bill.amount)


                product.total_liter_sold = total_liter
                product.total_amount_colleted = total_amount

                product_name_temp = "'" + product.product_name + "'"

                productSaledoughnutChart_labels_temp.append(product_name_temp)

                productSaledoughnutChart_data_temp.append(total_amount)
        
        context['products'] = products
        context['products1'] = products1
        context['current_from_date'] = sd_filter
        context['current_to_date1'] = product_end_date
        context['productSaledoughnutChart_data'] = ','.join(map(str, productSaledoughnutChart_data_temp))
        context['productSaledoughnutChart_labels'] = ','.join(map(str, productSaledoughnutChart_labels_temp))

        addon_products = AddonPetrolPump.objects.filter(m_business_id = merchant_business_id).all()

        addonsSalesdoughnutchart_label_temp = []
        addonsSalesdoughnutchart_data_temp = []
        
        if request.POST.get('submit') == 'product_sales_form_btn':
           
            DATE_FORMAT = '%Y-%m-%d'
            date_time_obj = datetime.strptime(product_end_date, '%Y-%m-%d')
            day_later = date_time_obj + timedelta(days=1)
            x = day_later.date()
            ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

            billing_from_date = datetime.strptime(str(product_start_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = billing_from_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            for addon_product in addon_products:

                petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__gte = sd_filter, created_at__lte = ed_filter).all()

                total_sold = 0
                amount_collected = 0
                
                # for bills in petrol_bills:
                #     addon_products_temp = bills.addon_product_id
                #     addon_product_cost_temp = bills.addon_product_cost
                #     addon_quantity_temp = bills.addon_quantity
                    
                #     if addon_products_temp:
                #         bill_addon_products = list(addon_products_temp.split(","))
                #         bill_addon_costs = list(addon_product_cost_temp.split(","))
                #         addon_quantity = list(addon_quantity_temp.split(","))

                #         for product in bill_addon_products:
                #             if addon_product.id == int(product):
                #                 index = bill_addon_products.index(product)
                #                 total_sold = total_sold + int(addon_quantity[index])
                #                 amount_collected = amount_collected + float(bill_addon_costs[index]) * float(addon_quantity[index])

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

                    # amount_collected = format(float(amount_collected), ".2f")
                    # addon_product.total_sold = total_sold
                    # addon_product.amount_collected = amount_collected

                    # product_name_temp = "'" + addon_product.product_name + "'"

                    # addonsSalesdoughnutchart_label_temp.append(product_name_temp)

                    # addonsSalesdoughnutchart_data_temp.append(amount_collected)
                addon_product.total_sold = total_sold
                addon_product.amount_collected = amount_collected

                product_name_temp = "'" + addon_product.product_name + "'"

                addonsSalesdoughnutchart_label_temp.append(product_name_temp)

                addonsSalesdoughnutchart_data_temp.append(round(amount_collected, 2))
        else:
            product_start_date = ''
            product_end_date = ''
            for addon_product in addon_products:

                petrol_bills = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business.id, created_at__date = timezone.now()).all()
                
                total_sold = 0
                amount_collected = 0
                
                # for bills in petrol_bills:
                #     addon_products_temp = bills.addon_product_id
                #     addon_product_cost_temp = bills.addon_product_cost
                #     addon_quantity_temp = bills.addon_quantity
                    
                #     if addon_products_temp:
                #         bill_addon_products = list(addon_products_temp.split(","))
                #         bill_addon_costs = list(addon_product_cost_temp.split(","))
                #         addon_quantity = list(addon_quantity_temp.split(","))

                #         for product in bill_addon_products:
                #             if addon_product.id == int(product):
                #                 try:
                #                     index = bill_addon_products.index(product)
                #                     total_sold = total_sold + int(addon_quantity[index])
                #                     amount_collected = amount_collected + float(bill_addon_costs[index]) * float(addon_quantity[index])
                #                 except:
                #                     pass
                #     amount_collected = format(float(amount_collected), ".2f")

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

                # print(addonsSalesdoughnutchart_data_temp)

        
        context['addon_products'] = addon_products
        context['from_date1'] = product_start_date
        context['to_date1'] = product_end_date
        context['addonsSalesdoughnutchart_labels'] = ','.join(map(str, addonsSalesdoughnutchart_label_temp))
        context['addonsSalesdoughnutchart_data'] = ','.join(map(str, addonsSalesdoughnutchart_data_temp))
        context['start_date'] = product_start_date
        context['end_date'] = product_end_date

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

        
    context['merchant_business_category_id'] = merchant_business.m_business_category.id
    context['segment'] = 'index'
    context['DashboardNavclass'] = 'active'
    # merchant-index-other-business.html
    # print(merchant_business.m_business_category.id)
    if merchant_business.m_business_category.id == 11 or merchant_business.m_business_category.id == 12:
        html_template = loader.get_template('merchant-index.html')
    else:

        total_transaction = 0

        total_transaction1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False,created_at__date = timezone.now()).count()

        total_transaction2 = MerchantBill.objects.filter(business_name = merchant_business,created_at__date = timezone.now()).count()

        total_transaction = int(total_transaction1) + int(total_transaction2)

        context['total_transaction'] = total_transaction

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

        context['average_transaction'] = average_transaction

        customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False,created_at__date = timezone.now()).order_by('-id')

        merchant_bill = MerchantBill.objects.filter(business_name = merchant_business,created_at__date = timezone.now()).order_by('-id')

        total_sales = 0

        for bill in customer_bill:
            total_sales = total_sales + float(bill.bill_amount)

        for bill in merchant_bill:
            total_sales = total_sales + float(bill.bill_amount)

        context['total_sales'] = total_sales

        average_sales = 0

        if total_transaction != 0 and total_sales != 0:
            average_sales = total_sales/total_transaction
        else:
            average_sales = 0

        context['average_sales'] = average_sales


        billing_analysis_from_date = ''
        billing_analysis_to_date = ''
        if request.POST.get('submit') == 'billing_analysis_btn':
            DATE_FORMAT = '%Y-%m-%d'
            billing_analysis_from_date = request.POST['billing_analysis_from_date']
            billing_analysis_to_date = request.POST['billing_analysis_to_date']
            date_time_obj = datetime.strptime(billing_analysis_to_date, '%Y-%m-%d')
            day_later = date_time_obj + timedelta(days=1)
            x = day_later.date()
            ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

            billing_from_date = datetime.strptime(str(billing_analysis_from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = billing_from_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            # billing_to_date = datetime.strptime(str(billing_analysis_to_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            # end_date = billing_to_date.split('-')
            # end_date = date(int(end_date[2]), int(end_date[1]), int(end_date[0]))
            # ed_filter = end_date.strftime(DATE_FORMAT)
           

            customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')

            merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')
            parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False,created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')
            petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id,created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')
            merchant_bill1 = MerchantBill.objects.filter(bill_received_business_name = merchant_business.id, created_at__gte = sd_filter,created_at__lte = ed_filter).order_by('-id')

            startswith = str(merchant_business_id) + ','
            endswith = ','+ str(merchant_business_id)
            contains = ','+ str(merchant_business_id) + ','
            exact = str(merchant_business_id)

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
                try:
                    # if int(bill.bill_received_business_name) == merchant_business.id:
                    received_bill_count = received_bill_count + 1
                except:
                    ''

            for bill in parking_bill_list:
                sent_bill_count = sent_bill_count + 1
                if bill.reject_status == True:
                    rejected_bill_count = rejected_bill_count + 1

            for bill in petrol_bill_list:
                sent_bill_count = sent_bill_count + 1
                if bill.reject_status == True:
                    rejected_bill_count = rejected_bill_count + 1

            for recharge in recharge_his:
                received_bill_count = received_bill_count + 1

            billing_analysis_labels_temp = []
            billing_analysis_labels_temp.append("Sent Bills")
            billing_analysis_labels_temp.append("Received Bills")
            billing_analysis_labels_temp.append("Rejected Bills")
            context['billing_analysis_labels'] = billing_analysis_labels_temp

            billing_analysis_data_temp = []
            billing_analysis_data_temp.append(str(sent_bill_count))
            billing_analysis_data_temp.append(str(received_bill_count))
            billing_analysis_data_temp.append(str(rejected_bill_count))
            context['billing_analysis_data'] = billing_analysis_data_temp
            context['from_date'] = billing_analysis_from_date
            context['to_date'] = billing_analysis_to_date
            if billing_analysis_data_temp == '':
                sweetify.success(request, title="Oops...", icon='error', text='Matched data not found.', timer=1500)
        else:

            customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__date = timezone.now()).order_by('-id')
            merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now()).order_by('-id')

            merchant_bill1 = MerchantBill.objects.filter(bill_received_business_name = merchant_business.id, created_at__date = timezone.now()).order_by('-id')


            parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False,created_at__date = timezone.now()).order_by('-id')
            petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id,created_at__date = timezone.now()).order_by('-id')

            startswith = str(merchant_business_id) + ','
            endswith = ','+ str(merchant_business_id)
            contains = ','+ str(merchant_business_id) + ','
            exact = str(merchant_business_id)

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
               
            for bill in merchant_bill1:
                received_bill_count = received_bill_count + 1

            for bill in parking_bill_list:
                sent_bill_count = sent_bill_count + 1
                if bill.reject_status == True:
                    rejected_bill_count = rejected_bill_count + 1


            for bill in petrol_bill_list:
                sent_bill_count = sent_bill_count + 1
                if bill.reject_status == True:
                    rejected_bill_count = rejected_bill_count + 1

            for recharge in recharge_his:
                received_bill_count = received_bill_count + 1

            billing_analysis_labels_temp = []
            billing_analysis_labels_temp.append("Sent Bills")
            billing_analysis_labels_temp.append("Received Bills")
            billing_analysis_labels_temp.append("Rejected Bills")
            context['billing_analysis_labels'] = billing_analysis_labels_temp

            billing_analysis_data_temp = []
            billing_analysis_data_temp.append(str(sent_bill_count))
            billing_analysis_data_temp.append(str(received_bill_count))
            billing_analysis_data_temp.append(str(rejected_bill_count))
            context['billing_analysis_data'] = billing_analysis_data_temp


        if request.POST.get('submit') == 'billing_analysis_btn':
            DATE_FORMAT = '%Y-%m-%d'
            # digital_bill_from_date = request.POST['digital_bill_from_date']
            # digital_bill_to_date = request.POST['digital_bill_to_date']

            d_from_date = datetime.strptime(str(billing_analysis_from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = d_from_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            # d_to_date = datetime.strptime(str(billing_analysis_to_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            # end_date = d_to_date.split('-')
            # end_date = date(int(end_date[2]), int(end_date[1]), int(end_date[0]))
            # ed_filter = end_date.strftime(DATE_FORMAT)

            date_time_obj = datetime.strptime(billing_analysis_to_date, '%Y-%m-%d')
            day_later = date_time_obj + timedelta(days=1)
            x = day_later.date()
            ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

            # notifications = sent_bill_history.objects.filter(
            #     m_business_id = merchant_business.id,
            #     created_at__range = (sd_filter, ed_filter),
            #     digital_bill = True
            # ).count()


            # sms = sent_bill_history.objects.filter(
            #     m_business_id = merchant_business.id,
            #     created_at__range = (sd_filter, ed_filter),
            #     sms_bill = True
            # ).count()

            sent_bill_count = int(sent_bill_count)
            # sms_sent = round(sent_bill_count * 0.60)
            # digital_sent = round(sent_bill_count * 0.40)
            digital_sent = 0
            for bill in customer_bill:
                if bill.greenbill_digital_bill == "True":
                    digital_sent = digital_sent + 1

            for bill in merchant_bill:
                if bill.greenbill_digital_bill == "True":
                    digital_sent = digital_sent + 1

            for bill in parking_bill_list:
                if bill.greenbill_digital_bill == "True":
                    digital_sent = digital_sent + 1

            for bill in parking_bill_list:
                if bill.greenbill_digital_bill == "True":
                    digital_sent = digital_sent + 1

            sms_sent = 0
            for bill in customer_bill:
                if bill.greenbill_sms_bill == "True":
                    sms_sent = sms_sent + 1

            for bill in merchant_bill:
                if bill.greenbill_sms_bill == "True":
                    sms_sent = sms_sent + 1

            for bill in parking_bill_list:
                if bill.greenbill_sms_bill == "True":
                    sms_sent = sms_sent + 1

            for bill in parking_bill_list:
                if bill.greenbill_sms_bill == "True":
                    sms_sent = sms_sent + 1

            digital_billing_labels_temp = []
            digital_billing_labels_temp.append("SMS Sent")
            digital_billing_labels_temp.append("Notifications Sent")
            context['digital_billing_labels'] = digital_billing_labels_temp

            digital_billing_data_temp = []
            digital_billing_data_temp.append(str(sms_sent))
            digital_billing_data_temp.append(str(digital_sent))
            context['digital_billing_data'] = digital_billing_data_temp
            
        else:
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

            sent_bill_count = int(sent_bill_count)

            digital_sent = 0
            for bill in customer_bill:
                if bill.greenbill_digital_bill == "True":
                    digital_sent = digital_sent + 1

            for bill in merchant_bill:
                if bill.greenbill_digital_bill == "True":
                    digital_sent = digital_sent + 1

            for bill in parking_bill_list:
                if bill.greenbill_digital_bill == "True":
                    digital_sent = digital_sent + 1

            for bill in parking_bill_list:
                if bill.greenbill_digital_bill == "True":
                    digital_sent = digital_sent + 1

            sms_sent = 0
            for bill in customer_bill:
                if bill.greenbill_sms_bill == "True":
                    sms_sent = sms_sent + 1

            for bill in merchant_bill:
                if bill.greenbill_sms_bill == "True":
                    sms_sent = sms_sent + 1

            for bill in parking_bill_list:
                if bill.greenbill_sms_bill == "True":
                    sms_sent = sms_sent + 1

            for bill in parking_bill_list:
                if bill.greenbill_sms_bill == "True":
                    sms_sent = sms_sent + 1

            digital_billing_labels_temp = []
            digital_billing_labels_temp.append("SMS Sent")
            digital_billing_labels_temp.append("Notifications Sent")
            context['digital_billing_labels'] = digital_billing_labels_temp

            digital_billing_data_temp = []
            digital_billing_data_temp.append(str(sms_sent))
            digital_billing_data_temp.append(str(digital_sent))
            context['digital_billing_data'] = digital_billing_data_temp

        # unique_customer = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False).order_by('-id').distinct('mobile_no').count()
        
        today = date.today()
        current_year = today.year
        next_year = today.year + 1
        years_list = []
        years_next = []

        merchant_bills_years = MerchantBill.objects.order_by().values('created_at__year').distinct() 
        for year in merchant_bills_years:
            years_list.append(year['created_at__year'])
            years_next.append(year['created_at__year'] + 1)
        yearslist=zip(years_list, years_next)

        if request.POST.get('submit') == 'bills_collection_other_business_btn':
            years = request.POST["years"]
            years_value = int(years)

            search_from_year = years_value
            search_to_year = years_value + 1 

            current_month_number = datetime.now().strftime("%m")
            otherbillscollectionChart = []
            current_month_total = 0.00
            month3 = []
            year3 = []
            for i in range(4,13):
                y1 = years_value
                year3.append(y1)
                if i < 10:
                    m1 = "0" + str(i)
                    month3.append(m1)
                else:
                    month3.append(i)

            for j in range(1,4):
                y2 = years_value + 1
                year3.append(y2)
                if j < 10:
                    m2 = "0" + str(j)
                    month3.append(m2)
            for year,month in zip(year3,month3):
                
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
                otherbillscollectionChart.append(decimal_value)

                if int(current_month_number) == month:
                    current_month_total = decimal_value


            context['search_from_year'] = search_from_year
            context['search_to_year'] = search_to_year 
            if years_value:
                context['years_value'] = years_value 


        else:
            current_month_number = datetime.now().strftime("%m")
            current_month_total = 0.00
            otherbillscollectionChart = []
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
                
                merchant_bills = MerchantBill.objects.filter(business_name = merchant_business,created_at__year = year, created_at__month = month).all()
                # print('merchant_bills',merchant_bills)
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
                otherbillscollectionChart.append(decimal_value)

                if int(current_month_number) == month:
                    current_month_total = decimal_value
                

        context['otherbillscollectionChart'] = otherbillscollectionChart
        context['current_month_total'] = current_month_total

        # context['vehiclestatusChart_list1'] = vehiclestatusChart1
        context['current_year'] = current_year
        context['next_year'] = next_year
        context['yearslist'] = yearslist
        context['years_list'] = years_list





        if request.POST.get('submit') == 'billing_analysis_btn':
            DATE_FORMAT = '%Y-%m-%d'
            # customer_analysis_from_date = request.POST['customer_analysis_from_date']
            # customer_analysis_to_date = request.POST['customer_analysis_to_date']

            cust_from_date = datetime.strptime(str(billing_analysis_from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            start_date = cust_from_date.split('-')
            start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
            sd_filter = start_date.strftime(DATE_FORMAT)

            cust_to_date = datetime.strptime(str(billing_analysis_to_date), '%Y-%m-%d').strftime('%d-%m-%Y')
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


            if customers1 == '':
                sweetify.success(request, title="Oops...", icon='error', text='Matched data not found.', timer=1500)
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

        # Coupons Chart

        all_coupons = CouponModel.objects.filter(merchant_business_id = merchant_business.id)

        # if request.POST.get('submit') == 'promotion_btn':
        #     coupon_from_date = request.POST['promotion_from_date']
        #     coupon_to_date = request.POST['promotion_to_date']
        #     c_from_date = datetime.strptime(str(coupon_from_date), "%Y-%m-%d")
        #     c_to_date = datetime.strptime(str(coupon_to_date), "%Y-%m-%d")

        #     coupon_active_count = 0
        #     coupon_expired_count = 0
        #     check = 'no'

        #     for coupon in all_coupons:
        #         valid_to_date = datetime.strptime(str(coupon.valid_through), "%Y-%m-%d")
        #         valid_from_date = datetime.strptime(str(coupon.valid_from), "%Y-%m-%d")
        #         if valid_to_date < current_date_new:
        #             if valid_to_date >= c_from_date and valid_to_date <= c_to_date:
        #                 check = 'yes'
        #                 coupon_expired_count = coupon_expired_count + 1
        #         else:
        #             if valid_to_date >= c_from_date and valid_to_date <= c_to_date:
        #                 check = 'yes'
        #                 coupon_active_count = coupon_active_count + 1

        #     coupons_labels_temp = []
        #     coupons_labels_temp.append("Active")
        #     coupons_labels_temp.append("Expired")
        #     context['coupons_labels'] = coupons_labels_temp

        #     coupons_data_temp = []
        #     coupons_data_temp.append(str(coupon_active_count))
        #     coupons_data_temp.append(str(coupon_expired_count))
        #     context['coupons_data'] = coupons_data_temp

        #     context['coupon_expired_count'] = coupon_expired_count
        #     context['coupon_active_count'] = coupon_active_count
        #     print('aa',coupons_data_temp)
        #     # print('bb',coupon_active_count)
        #     if check == 'no':
        #         sweetify.success(request, title="Oops...", icon='error', text='Matched data not found.', timer=1500)
        # else:
        coupon_active_count = 0
        coupon_expired_count = 0

        for coupon in all_coupons:
            valid_to_date = datetime.strptime(str(coupon.valid_through), "%Y-%m-%d")
            if valid_to_date < current_date_new:
                coupon_expired_count = coupon_expired_count + 1
            else:
                coupon_active_count = coupon_active_count + 1

        coupons_labels_temp = []
        coupons_labels_temp.append("Active")
        coupons_labels_temp.append("Expired")
        context['coupons_labels'] = coupons_labels_temp

        coupons_data_temp = []
        coupons_data_temp.append(str(coupon_active_count))
        coupons_data_temp.append(str(coupon_expired_count))
        context['coupons_data'] = coupons_data_temp

        context['coupon_expired_count'] = coupon_expired_count
        context['coupon_active_count'] = coupon_active_count

            

        # Offers Chart

        all_offers = OfferModel.objects.filter(merchant_business_id = merchant_business)

        # if request.POST.get('submit') == 'promotion_btn':
        #     coupon_from_date = request.POST['promotion_from_date']
        #     coupon_to_date = request.POST['promotion_to_date']
        #     c_from_date = datetime.strptime(str(coupon_from_date), "%Y-%m-%d")
        #     c_to_date = datetime.strptime(str(coupon_to_date), "%Y-%m-%d")
        #     # print('coupon_from_date',coupon_from_date)
        #     # print('coupon_to_date',coupon_to_date)
        #     offer_active_count = 0
        #     offer_expired_count = 0
        #     offer_not_approved = 0

        #     check = 'no'
        #     print('coupon_from_date',c_from_date)
        #     print('coupon_to_date',c_to_date)
        #     print('current_date_new',current_date_new)
        #     for offer in all_offers:
        #         valid_to_date = datetime.strptime(str(offer.valid_through), "%Y-%m-%d")
        #         valid_from_date = datetime.strptime(str(offer.valid_from), "%Y-%m-%d")
        #         print('valid_to_date',valid_to_date)
        #         print('valid_from_date',valid_from_date)

        #         if valid_to_date < current_date_new:
        #             if valid_to_date >= c_from_date and valid_to_date <= c_to_date:
        #                 offer_expired_count = offer_expired_count + 1
        #         elif offer.status == "1":
        #             if valid_to_date >= c_from_date and valid_to_date <= c_to_date:
        #                 offer_active_count = offer_active_count + 1
        #         if offer.status == "0":
        #             if valid_to_date >= c_from_date and valid_to_date <= c_to_date:
        #                 offer_not_approved = offer_not_approved + 1
                
                # if valid_to_date < current_date_new:
                #     print()

                #     if valid_from_date >= c_from_date and valid_to_date <= c_to_date:
                #         offer_expired_count = offer_expired_count + 1
                #         check = 'yes'
                # elif offer.status == "1":
                #     if valid_from_date >= c_from_date and valid_to_date <= c_to_date:
                #         check = 'yes'
                #         offer_active_count = offer_active_count + 1
                # if offer.status == "0":
                #     if valid_from_date >= c_from_date and valid_to_date <= c_to_date:
                #         check = 'yes'
                #         offer_not_approved = offer_not_approved + 1

            # offer_labels_temp = []
            # offer_labels_temp.append("Active")
            # offer_labels_temp.append("Expired")
            # offer_labels_temp.append("Not Approved")
            # context['offer_labels'] = offer_labels_temp

            # offer_data_temp = []
            # offer_data_temp.append(str(offer_active_count))
            # offer_data_temp.append(str(offer_expired_count))
            # offer_data_temp.append(str(offer_not_approved))
            # context['offer_data'] = offer_data_temp

            # context['offer_expired_count'] = offer_expired_count
            # context['offer_active_count'] = offer_active_count
            # if check == 'no':
            #     sweetify.success(request, title="Oops...", icon='error', text='Matched data not found.', timer=1500)

        # else:
        offer_active_count = 0
        offer_expired_count = 0
        offer_not_approved = 0

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
        context['offer_labels'] = offer_labels_temp

        offer_data_temp = []
        offer_data_temp.append(str(offer_active_count))
        offer_data_temp.append(str(offer_expired_count))
        offer_data_temp.append(str(offer_not_approved))
        context['offer_data'] = offer_data_temp

        context['offer_expired_count'] = offer_expired_count
        context['offer_active_count'] = offer_active_count


        today = date.today()
        current_year = today.year
        current_month = today.month
        total_days = calendar.monthrange(current_year, current_month)[1]
        days_list = []
        for i in range(1,total_days+1):
            month_days = str(i) 
            days_list.append(month_days)

        monthwisebillscollectionChart = []
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
                        monthwisebillscollectionChart.append(decimal_value)
                    else:
                        total_collection = float(0)

                        decimal_value = format(float(total_collection), ".2f")
                        monthwisebillscollectionChart.append(decimal_value)

                    
        # print('monthwisebillscollectionChart',monthwisebillscollectionChart)

        context['monthwisebillscollectionChart'] = monthwisebillscollectionChart
        context['days_list'] = days_list

        exe_send_and_print_bill_status1 = CustomerBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), exe_bill_type = 2).count()

        exe_send_and_print_bill_status2 = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), exe_bill_type = 2).count()

        exe_send_bill_status1 = CustomerBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), exe_bill_type = 1).count()

        exe_send_bill_status2 = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now(), exe_bill_type = 1).count()

        exe_print_bill_status = ExePrintStatus.objects.filter(business_id = merchant_business.id, created_at__date = timezone.now()).count()

        send_print_bill_count = int(exe_send_and_print_bill_status1) + int(exe_send_and_print_bill_status2)

        send_bill_count = int(exe_send_bill_status1) + int(exe_send_bill_status2)

        context['send_print_bill_count'] = send_print_bill_count
        context['send_bill_count'] = send_bill_count
        context['exe_print_bill_status'] = exe_print_bill_status


        # html_template = loader.get_template('merchant/merchant-index-other-business-08-06-21.html')

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

        tags_list = []
        updated_bill_tags = ''
        bill_amt = request.POST['bill_amount']
        date = request.POST['bill_date']
        bill_tags_value = request.POST['bill_tags_value']
        
        remarks = request.POST['remarks']
        custom_business = request.POST['custom_business']
        invoice_no = request.POST['invoice_no']

        if bill_tags_value:
            tags_list = bill_tags_value.split(",")
            
            updated_tags_list = []
            for tag in tags_list:
                if tag.isdigit():
                    updated_tags_list.append(tag)
                else:
                    result = bill_tags.objects.create(bill_tags_name=tag,user_id=GreenBillUser.objects.get(id=request.user.id),is_customer_bill_tag=1)
                    tag = result.id
                    updated_tags_list.append(tag)

            updated_bill_tags = ','.join(map(str, updated_tags_list))      
        

        if merchant_name and cust_category:
            bill_data = CustomerBill.objects.create(
                mobile_no=request.user.mobile_no,
                bill=bill_file,
                business_name=merchant_object,
                customer_bill_category=bill_category_object,
                bill_amount=bill_amt,
                bill_date=date,
                customer_added = True,
                bill_tags = updated_bill_tags,
                remarks = remarks,
                invoice_no = invoice_no,
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
                bill_tags = updated_bill_tags,
                remarks = remarks,
                invoice_no = invoice_no,
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
                bill_tags = updated_bill_tags,
                remarks = remarks,
                invoice_no = invoice_no,
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
                bill_tags = updated_bill_tags,
                remarks = remarks,
                invoice_no = invoice_no,
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

    queryset = CustomerBill.objects.filter(mobile_no=request.user)

    all_cust_bill = CustomerBill.objects.filter(mobile_no=request.user).order_by('-id')
    
    user_id = request.user.id

    customer_bills = []

    customer_object = GreenBillUser.objects.get(id = user_id)

    bill_count = 0
    cust_bill_count = 0
    bill_flagged = 0
    bill_reject_count = 0
    total_bill_amount = 0
    total_merchant_bill_count = 0
    total_category_bill_count = 0
    total_bill_amount_online = 0

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

        customer_bill_list = CustomerBill.objects.filter(mobile_no=request.user.mobile_no, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
    else:
        customer_bill_list = CustomerBill.objects.filter(mobile_no=request.user.mobile_no, created_at__date = timezone.now(), delete_bill = False).order_by('-id')

    for bill in customer_bill_list:

        bill_count += 1
        cust_bill_count +=1

        if bill.bill_amount and bill.payment_done == False:
            total_bill_amount = total_bill_amount + float(bill.bill_amount)

        if bill.bill_amount and bill.payment_done == True and bill.customer_added == False:
            total_bill_amount_online = total_bill_amount_online + float(bill.bill_amount)

        if bill.reject_status == True:
            bill_reject_count = bill_reject_count + 1
        
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

        if bill_category_temp:
            total_category_bill_count += 1

        customer_bills.append({
            "id": bill.id,
            "business_name": business_name,
            "bill_category_name": bill_category_temp,
            "bill_amount": bill.bill_amount,
            "comments": bill.remarks,
            "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%Y-%m-%d') if bill.bill_date else '',
            "business_logo": business_logo,
            "customer_added": bill.customer_added,
            'db_table': "CustomerBill",
            # "bill_file": bill.bill,
            # "file_extension":"",
            "created_at":bill.created_at,
          
        })

    if request.method == 'POST':
        parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no, is_pass = False, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
    else:
        parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no, is_pass = False, created_at__date = timezone.now(), delete_bill = False).order_by('-id')

    for bill in parking_bill_list:

        bill_count += 1
        bill_count1 = bill_count
        
        if bill.amount and bill.payment_done == False:
            total_bill_amount = total_bill_amount + float(bill.amount)

        if bill.amount and bill.payment_done == True:
            total_bill_amount_online = total_bill_amount_online + float(bill.amount)
        
        if bill.bill_flag == True:
            bill_flagged = bill_flagged + 1

        if bill.reject_status == True:
            bill_reject_count = bill_reject_count + 1

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
            "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%Y-%m-%d'),
            "business_logo": business_logo,
            "customer_added": False,
            'db_table': "SaveParkingLotBill",
            # "bill_file": bill.bill_file,
            # "file_extension":"",
            "created_at":bill.created_at
        })

    if request.method == 'POST':
        petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
    else:
        petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no, created_at__date = timezone.now(), delete_bill = False).order_by('-id')

    for bill in petrol_bill_list:
        
        bill_count += 1

        if bill.total_amount and bill.payment_done == False:
            total_bill_amount = total_bill_amount + float(bill.total_amount)

        if bill.total_amount and bill.payment_done == True:
            total_bill_amount_online = total_bill_amount_online + float(bill.total_amount)
        
        if bill.bill_flag == True:
            bill_flagged = bill_flagged + 1

        if bill.reject_status == True:
            bill_reject_count = bill_reject_count + 1
       
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
            "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%Y-%m-%d'),
            "business_logo": business_logo,
            "customer_added": False,
            'db_table': "SavePetrolPumpBill",
            # "bill_file": bill.bill_file,
            # "file_extension":"",
            "created_at":  bill.created_at
        })

    customer_bills.sort(key=lambda r: r['created_at'], reverse = True)

    # for bill in customer_bills:
    #     try:
    #         file_type = filetype.guess(bill['bill_file'])
    #         bill['file_extension'] = file_type.extension
    #     except:
    #         bill['file_extension'] = ""

    total_merchant_bill_count = total_merchant_bill_count + cust_bill_count

    # Shopping Analysis Start

    # Analysis Category Wisw
    merchant_labels = []
    merchant_data = []
    from_date_temp1 = ''
    to_date_temp1 = ''
    # if request.POST.get('submit') == 'merchant_analysis_btn':
    if request.method == 'POST':
        merchant_labels = []
        merchant_data = []
        dat = []
        data_count1 = []
        data_count = 0 
        merchant_bill_count_doughnut = []
        from_date_temp1 = request.POST["from_date1"]
        date_from = datetime.strptime(from_date_temp1, '%Y-%m-%d').date()
        to_date_temp1 = request.POST["to_date1"]
        date_to = datetime.strptime(to_date_temp1, '%Y-%m-%d').date()

        for bill in customer_bills:
            converted_date = parse_date(bill["bill_date"])
            if converted_date >= date_from and converted_date <= date_to:
                if bill['business_name']:
                    if bill['business_name'] in merchant_labels:
                        pass
                    else:
                        merchant_labels.append(bill['business_name'])
        spend_by_bill_business1 = {new_list: 0 for new_list in merchant_labels} 


        for bill1 in customer_bills:
            converted_date = parse_date(bill1["bill_date"])
            if converted_date >= date_from and converted_date <= date_to:
                # print('c_date',c_date)
                for y in merchant_labels:
                    if bill1['business_name']:
                        if bill1['business_name'] == y:
                            spend_by_bill_business1[y] =  spend_by_bill_business1[y] + float(bill1['bill_amount'])
        for object in spend_by_bill_business1:
            dat.append(spend_by_bill_business1[object])

        for i in dat:
            decimal_value = format(float(i), ".2f")
            merchant_data.append(decimal_value)

        # print('merchant_data',merchant_data)
        if not merchant_data:
            sweetify.success(request, title="Oops...", icon='error', text='Matched data not found.', timer=1500)


        context['merchant_data'] = merchant_data
        context['merchant_labels'] =  merchant_labels
        

        name = []
        merchant_bill_count_doughnut = []
        data_count1 = 0

        for bill in customer_bills:
            converted_date = parse_date(bill["bill_date"])
            if converted_date >= date_from and converted_date <= date_to:
                if bill['business_name']:
                    if bill['business_name'] in name:
                        pass
                    else:
                        name.append(bill['business_name'])
                    
        spend_by_bill_business2 = {new_list: 0 for new_list in name} 

        for bill1 in customer_bills:
            converted_date = parse_date(bill1["bill_date"])
            if converted_date >= date_from and converted_date <= date_to:
                for y in name:
                    if bill1['business_name']:
                        if bill1['business_name'] == y:
                            spend_by_bill_business2[y] =  spend_by_bill_business2[y] + 1
                            data_count1 += 1

        for object in spend_by_bill_business2:
            merchant_bill_count_doughnut.append(spend_by_bill_business2[object])

        context['merchant_data'] = merchant_data
        context['name'] = name


    else:
        merchant_labels = []
        merchant_data = []
        dat = []
        data_count1 = []
        data_count = 0 
        merchant_bill_count_doughnut = []
        for bills in customer_bills:
            if bills['business_name']:
                if bills['business_name'] in merchant_labels:
                    pass
                else:
                    merchant_labels.append(bills['business_name'])

        spend_by_bill_business1 = {new_list: 0 for new_list in merchant_labels} 

        for oject in customer_bills:
            for y in merchant_labels:
                if oject['business_name']:
                    if oject['business_name'] == y:
                        spend_by_bill_business1[y] =  spend_by_bill_business1[y] + float(oject['bill_amount'])

        for object in spend_by_bill_business1:
            dat.append(spend_by_bill_business1[object])

        for i in dat:
            decimal_value = format(float(i), ".2f")
            merchant_data.append(decimal_value)

        context['merchant_data'] = merchant_data
        context['merchant_labels'] =  merchant_labels

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

        context['name'] = name


    # End Bill Count Merchant

    # Bill Count Category 
    category_labels = []
    category_data = []
    from_date_temp2 = ''
    to_date_temp2 = ''
    # if request.POST.get('submit') == 'category_analysis_btn':
    if request.method == 'POST':
        name1 = []
        category_labels = []
        category_data = []
        dat = []
        category_bill_count_doughnut = []
        data_count2 = 0

        for bills in customer_bills:
            converted_date = parse_date(bills["bill_date"])
            if converted_date >= date_from and converted_date <= date_to:
                if bills['bill_category_name']:
                    if bills['bill_category_name'] in name1:
                        pass
                    else:
                        name1.append(bills['bill_category_name'])

        spend_by_bill_category = {new_list: 0 for new_list in name1} 

        for oject in customer_bills:
            converted_date = parse_date(oject["bill_date"])
            if converted_date >= date_from and converted_date <= date_to:
                for x in name1:
                    if oject['bill_category_name']:
                        if oject['bill_category_name'] == x:
                            spend_by_bill_category[x] =  spend_by_bill_category[x] + 1
                            data_count2 += 1
                        
        for object in spend_by_bill_category:
            category_bill_count_doughnut.append(spend_by_bill_category[object])

        context['data'] = data
        context['name1'] = name1


        for bills in customer_bills:
            converted_date = parse_date(bills["bill_date"])
            if converted_date >= date_from and converted_date <= date_to:
                if bills['bill_category_name']:
                    if bills['bill_category_name'] in category_labels:
                        pass
                    else:
                        category_labels.append(bills['bill_category_name'])

        spend_by_bill_category = {new_list: 0 for new_list in category_labels} 

        for oject in customer_bills:
            converted_date = parse_date(oject["bill_date"])
            if converted_date >= date_from and converted_date <= date_to:
                for x in category_labels:
                    if oject['bill_category_name']:
                        if oject['bill_category_name'] == x:
                            spend_by_bill_category[x] =  spend_by_bill_category[x] + float(oject['bill_amount'])

        for object in spend_by_bill_category:
            dat.append(spend_by_bill_category[object])

        for i in dat:
            decimal_value = format(float(i), ".2f")
            category_data.append(decimal_value)

        # print('category_data',category_data)
        if not category_data:
            sweetify.success(request, title="Oops...", icon='error', text='Matched data not found.', timer=1500)


        context['category_data'] = category_data
        context['category_labels'] = category_labels

    else:
        name1 = []
        dat = []
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

        context['name1'] = name1


        for bills in customer_bills:
            if bills['bill_category_name']:
                if bills['bill_category_name'] in category_labels:
                    pass
                else:
                    category_labels.append(bills['bill_category_name'])

        spend_by_bill_category = {new_list: 0 for new_list in category_labels} 

        for oject in customer_bills:
            for x in category_labels:
                if oject['bill_category_name']:
                    if oject['bill_category_name'] == x:
                        spend_by_bill_category[x] =  spend_by_bill_category[x] + float(oject['bill_amount'])

        for object in spend_by_bill_category:
            dat.append(spend_by_bill_category[object])

        for i in dat:
            decimal_value = format(float(i), ".2f")
            category_data.append(decimal_value)
            
        # context['from_date'] = ""
        # context['to_date'] = ""

        context['category_data'] = category_data
        context['category_labels'] = category_labels

    # End Bill Count Category

    bill_category_name = bill_category.objects.all().order_by('bill_category_name')

    b_name = MerchantProfile.objects.all()

    try:
        GreenPoints = GreenPointsModel.objects.filter(mobile_no=request.user).values('green_points_count')[0]['green_points_count']

    except:
        GreenPoints = 0
    # green_points = GreenPointsModel.objects.all()

    customer_bill_tags = bill_tags.objects.filter(user_id = request.user).order_by('bill_tags_name')

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
   
    # if request.POST.get('submit') == 'shopping_analysis_btn':
    if request.method == 'POST':

        labels = []
        data = []
        dat = []
        dat12 = []
        new_labels = []


        # from_date_temp = request.POST["from_date"]
        # date_from = datetime.strptime(from_date_temp, '%Y-%m-%d').date()
        # to_date_temp = request.POST["to_date"]
        # date_to = datetime.strptime(to_date_temp, '%Y-%m-%d').date()

        for bills in customer_bills:
            converted_date = parse_date(bills["bill_date"])
            if converted_date >= date_from and converted_date <= date_to:
                if bills['bill_category_name']:
                    if bills['bill_category_name'] in labels:
                        pass
                    else:
                        labels.append(bills['bill_category_name'])

        spend_by_bill_category = {new_list: 0 for new_list in labels}

        for oject in customer_bills:
            converted_date = parse_date(oject["bill_date"])
            if converted_date >= date_from and converted_date <= date_to:
                for x in labels:
                    if oject['bill_category_name']:
                        if oject['bill_category_name'] == x:
                            spend_by_bill_category[x] =  spend_by_bill_category[x] + float(oject['bill_amount'])

        for object in spend_by_bill_category:
            dat.append(spend_by_bill_category[object])
            dat12.append(spend_by_bill_category[object])

        dat12.sort(reverse=True)

        for amount1 in dat12:
            for i, amount2 in enumerate(dat):
                if amount1 == amount2:
                    for j, category1 in  enumerate(labels):
                        if i == j:
                            new_labels.append(category1)

        category_total_amount_sum = 0
        for i in dat12:
            decimal_value = format(float(i), ".2f")
            category_total_amount_sum = category_total_amount_sum + float(decimal_value)
            data.append(decimal_value)

        
        if not data:
            sweetify.success(request, title="Oops...", icon='error', text='Matched data not found.', timer=1500)


        # context['from_date'] = request.POST["from_date"]
        # context['to_date'] = request.POST["to_date"]

    else:

        labels = []
        data = []
        dat = []
        dat12 = []

        new_labels = []

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
            dat.append(spend_by_bill_category[object])
            dat12.append(spend_by_bill_category[object])

        dat12.sort(reverse=True)

        for amount1 in dat12:
            for i, amount2 in enumerate(dat):
                if amount1 == amount2:
                    for j, category1 in  enumerate(labels):
                        if i == j:
                            new_labels.append(category1)



        category_total_amount_sum = 0
        for i in dat12:
            decimal_value = format(float(i), ".2f")
            category_total_amount_sum = category_total_amount_sum + float(decimal_value)
            data.append(decimal_value)

        #for Murchant Date filter
    data1 = []
    labels1 = []
    # if request.POST.get('submit') == 'shopping_analysis_btn':
    if request.method == 'POST':
        labels1 = []
        new_labels1 = []
        data1 = []
        dat = []
        new_data1 = []


        # from_date_temp = request.POST["from_date"]
        # date_from = datetime.strptime(from_date_temp, '%Y-%m-%d').date()
        # to_date_temp = request.POST["to_date"]
        # date_to = datetime.strptime(to_date_temp, '%Y-%m-%d').date()
        
        for bills1 in customer_bills:
            converted_date = parse_date(bills1["bill_date"])
            if converted_date >= date_from and converted_date <= date_to:
                if bills1['business_name']:
                    if bills1['business_name'] in labels1:
                        pass
                    else:
                        labels1.append(bills1['business_name'])

        spend_by_bill_business1 = {new_list1: 0 for new_list1 in labels1} 

        for oject1 in customer_bills:
            converted_date = parse_date(oject1["bill_date"])
            if converted_date >= date_from and converted_date <= date_to:
                for y in labels1:
                    if oject1['business_name']:
                        if oject1['business_name'] == y:
                            spend_by_bill_business1[y] =  spend_by_bill_business1[y] + float(oject1['bill_amount'])
        
        for object1 in spend_by_bill_business1:
            dat.append(spend_by_bill_business1[object1])
            new_data1.append(spend_by_bill_business1[object1])

        new_data1.sort(reverse=True)

        for amount1 in new_data1:
            for i, amount2 in enumerate(dat):
                if amount1 == amount2:
                    for j, business_name1 in  enumerate(labels1):
                        if i == j:
                            new_labels1.append(business_name1)

        merchant_total_amount_sum = 0
        for i in new_data1:
            decimal_value = format(float(i), ".2f")
            merchant_total_amount_sum = merchant_total_amount_sum + float(decimal_value)
            data1.append(decimal_value)

        
        if not data1:
            sweetify.success(request, title="Oops...", icon='error', text='Matched data not found.', timer=1500)
            
        # context['from_date'] = request.POST["from_date"]
        # context['to_date'] = request.POST["to_date"]

    else:

        labels1 = []
        data1 = []
        dat = []
        new_data1 = []
        new_labels1 = []

        for bills1 in customer_bills:
            if bills1['business_name']:
                if bills1['business_name'] in labels1:
                    pass
                else:
                    labels1.append(bills1['business_name'])

        spend_by_bill_business1 = {new_list1: 0 for new_list1 in labels1} 

        for oject1 in customer_bills:
            for y in labels1:
                if oject1['business_name']:
                    if oject1['business_name'] == y:
                        spend_by_bill_business1[y] =  spend_by_bill_business1[y] + float(oject1['bill_amount'])
        
        for object1 in spend_by_bill_business1:
            dat.append(spend_by_bill_business1[object1])

            new_data1.append(spend_by_bill_business1[object1])

        new_data1.sort(reverse=True)

        for amount1 in new_data1:
            for i, amount2 in enumerate(dat):
                if amount1 == amount2:
                    for j, business_name1 in  enumerate(labels1):
                        if i == j:
                            new_labels1.append(business_name1)

        merchant_total_amount_sum = 0
        for i in new_data1:
            decimal_value = format(float(i), ".2f")
            merchant_total_amount_sum = merchant_total_amount_sum + float(decimal_value)
            data1.append(decimal_value)
            


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

        'labels':new_labels,
        'data':data,
        'category_total_amount_sum':category_total_amount_sum,
        'merchant_labels' : merchant_labels,
        'merchant_data': merchant_data,
        'merchant_bill_count_doughnut' : merchant_bill_count_doughnut,

        'data1': data1,
        'merchant_total_amount_sum':merchant_total_amount_sum,
        'labels1':new_labels1,
        'category_labels':category_labels,
        'category_data':category_data,
        'category_bill_count_doughnut' : category_bill_count_doughnut,
       
        'green_points':GreenPoints,

        'from_date1':from_date_temp1,
        'to_date1':to_date_temp1,
        'coupon_list':coupon_list,

        'total_bill_amount' : total_bill_amount,

        'bill_flagged': bill_flagged,
        'total_bill_count': bill_count,

        'total_merchant_bill_count': total_merchant_bill_count,
        'total_category_bill_count': total_category_bill_count,

        'bill_reject_count': bill_reject_count,

        'total_bill_amount_online': total_bill_amount_online,
        }
    
    html_template = loader.get_template('customer-index.html')

    return HttpResponse(html_template.render(context, request))

    # labels = []
    # data = []

    # context = {}

    # queryset = CustomerBill.objects.filter(mobile_no=request.user)

    # all_cust_bill = CustomerBill.objects.filter(mobile_no=request.user.mobile_no).order_by('-id')
    
    # user_id = request.user.id

    # customer_bills = []

    # customer_object = GreenBillUser.objects.get(id = user_id)

    # bill_count = 0
    # bill_flagged = 0
    # total_bill_amount = 0
    # total_merchant_bill_count = 0
    # total_category_bill_count = 0

    # customer_bill_list = CustomerBill.objects.filter(mobile_no=request.user.mobile_no).order_by('-id')

    # for bill in customer_bill_list:

    #     bill_count += 1

    #     if bill.bill_amount:

    #         total_bill_amount = total_bill_amount + float(bill.bill_amount)

    #     # if bill.bill_flag == True:
    #     #     bill_flagged = bill_flagged + 1
        
    #     try:
    #         business_name = bill.business_name.m_business_name
    #     except:
    #         business_name = bill.custom_business_name

    #     try:
    #         bill_category_temp = bill.customer_bill_category.bill_category_name
    #     except:
    #         bill_category_temp = ""

    #     base_url = "http://157.230.228.250/"

    #     try:
    #         business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
    #     except:
    #         business_logo = ""

    #     if business_name:
    #         total_merchant_bill_count += 1

    #     if bill_category_temp:
    #         total_category_bill_count += 1

    #     customer_bills.append({
    #         "id": bill.id,
    #         "business_name": business_name,
    #         "bill_category_name": bill_category_temp,
    #         "bill_amount": bill.bill_amount,
    #         "comments": bill.remarks,
    #         "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
    #         "business_logo": business_logo,
    #         "customer_added": bill.customer_added,
    #         'db_table': "CustomerBill",
    #         "bill_file": bill.bill,
    #         "file_extension":"",
    #         "created_at":bill.created_at,
          
    #     })


    # parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no, is_pass = False).order_by('-id')

    # for bill in parking_bill_list:

    #     bill_count += 1
        
    #     if bill.amount:
    #         total_bill_amount = total_bill_amount + float(bill.amount)
        
    #     if bill.bill_flag == True:
    #         bill_flagged = bill_flagged + 1

    #     try:
    #         business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
    #     except:
    #         business_name = ""

    #     try:
    #         bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
    #     except:
    #         bill_category_temp = ""

    #     base_url = "http://157.230.228.250/"

    #     try:
    #         business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
    #         business_logo = str(base_url) + str(business_logo_temp.url)

    #     except:
    #         business_logo = ""

    #     if business_name:
    #         total_merchant_bill_count += 1

    #     if bill_category_temp:
    #         total_category_bill_count += 1

    #     customer_bills.append({
    #         "id": bill.id,
    #         "business_name": business_name,
    #         "bill_category_name": bill_category_temp,
    #         "bill_amount": bill.amount,
    #         "comments": bill.remarks,
    #         "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
    #         "business_logo": business_logo,
    #         "customer_added": False,
    #         'db_table': "SaveParkingLotBill",
    #         "bill_file": bill.bill_file,
    #         "file_extension":"",
    #         "created_at":bill.created_at
    #     })


    # petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no).order_by('-id')

    # for bill in petrol_bill_list:
        
    #     bill_count += 1

    #     if bill.total_amount:
    #         total_bill_amount = total_bill_amount + float(bill.total_amount)
        
    #     if bill.bill_flag == True:
    #         bill_flagged = bill_flagged + 1
       
    #     try:
    #         business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
    #     except:
    #         business_name = ""

    #     try:
    #         bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
    #     except:
    #         bill_category_temp = ""

    #     base_url = "http://157.230.228.250/"

    #     try:
    #         business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
    #         business_logo = str(base_url) + str(business_logo_temp.url)

    #     except:
    #         business_logo = ""

    #     if business_name:
    #         total_merchant_bill_count += 1

    #     if bill_category_temp:
    #         total_category_bill_count += 1
        
    #     customer_bills.append({
    #         "id": bill.id,
    #         "business_name": business_name,
    #         "bill_category_name": bill_category_temp,
    #         "bill_amount": bill.total_amount,
    #         "comments": bill.remarks,
    #         "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
    #         "business_logo": business_logo,
    #         "customer_added": False,
    #         'db_table': "SavePetrolPumpBill",
    #         "bill_file": bill.bill_file,
    #         "file_extension":"",
    #         "created_at":  bill.created_at
    #     })

    # customer_bills.sort(key=lambda r: r['created_at'], reverse = True)

    # for bill in customer_bills:
    #     try:
    #         file_type = filetype.guess(bill['bill_file'])
    #         bill['file_extension'] = file_type.extension
    #     except:
    #         bill['file_extension'] = ""

    # # Shopping Analysis Start

    # # Analysis Category Wisw

    # for bills in customer_bills:
    #     if bills['bill_category_name']:
    #         if bills['bill_category_name'] in labels:
    #             pass
    #         else:
    #             labels.append(bills['bill_category_name'])

    # spend_by_bill_category = {new_list: 0 for new_list in labels} 

    # for oject in customer_bills:
    #     for x in labels:
    #         if oject['bill_category_name']:
    #             if oject['bill_category_name'] == x:
    #                 spend_by_bill_category[x] =  spend_by_bill_category[x] + float(oject['bill_amount'])

    # for object in spend_by_bill_category:
    #     data.append(spend_by_bill_category[object])
        
    # context['from_date'] = ""
    # context['to_date'] = ""

    # context['data'] = data
    # context['labels'] = labels
    
    # # Merchant Analysis function
    
    # labels1 = []
    # data1 = []
    # data_count1 = []
    # data_count = 0 

    # for bills in customer_bills:
    #     if bills['business_name']:
    #         if bills['business_name'] in labels1:
    #             pass
    #         else:
    #             labels1.append(bills['business_name'])

    # spend_by_bill_business1 = {new_list: 0 for new_list in labels1} 

    # for oject in customer_bills:
    #     for y in labels1:
    #         if oject['business_name']:
    #             if oject['business_name'] == y:
    #                 spend_by_bill_business1[y] =  spend_by_bill_business1[y] + float(oject['bill_amount'])

    # for object in spend_by_bill_business1:
    #     data1.append(spend_by_bill_business1[object])

    # context['data1'] = data1
    # context['labels1'] =  labels1

    # # Shopping Analysis End
    
    # # Bill Count Merchant 

    # name = []
    # merchant_bill_count_doughnut = []
    # data_count1 = 0

    # for bills in customer_bills:
    #     if bills['business_name']:
    #         if bills['business_name'] in name:
    #             pass
    #         else:
    #             name.append(bills['business_name'])
                
    # spend_by_bill_business2 = {new_list: 0 for new_list in name} 

    # for oject in customer_bills:
    #     for y in name:
    #         if oject['business_name']:
    #             if oject['business_name'] == y:
    #                 spend_by_bill_business2[y] =  spend_by_bill_business2[y] + 1
    #                 data_count1 += 1

    # for object in spend_by_bill_business2:
    #     merchant_bill_count_doughnut.append(spend_by_bill_business2[object])

    # context['data1'] = data1
    # context['name'] = name

    # # End Bill Count Merchant

    # # Bill Count Category 

    # name1 = []
    # category_bill_count_doughnut = []
    # data_count2 = 0
    # for bills in customer_bills:
    #     if bills['bill_category_name']:
    #         if bills['bill_category_name'] in name1:
    #             pass
    #         else:
    #             name1.append(bills['bill_category_name'])

    # spend_by_bill_category = {new_list: 0 for new_list in name1} 

    # for oject in customer_bills:
    #     for x in name1:
    #         if oject['bill_category_name']:
    #             if oject['bill_category_name'] == x:
    #                 spend_by_bill_category[x] =  spend_by_bill_category[x] + 1
    #                 data_count2 += 1
                    
    # for object in spend_by_bill_category:
    #     category_bill_count_doughnut.append(spend_by_bill_category[object])

    # context['data'] = data
    # context['name1'] = name1

    # context['from_date'] = ""
    # context['to_date'] = ""

    # # End Bill Count Category

    # bill_category_name = bill_category.objects.all().order_by('bill_category_name')

    # b_name = MerchantProfile.objects.all()

    # try:
    #     GreenPoints = GreenPointsModel.objects.filter(mobile_no=request.user).values('green_points_count')[0]['green_points_count']

    # except:
    #     GreenPoints = 0
    # # green_points = GreenPointsModel.objects.all()

    # customer_bill_tags = bill_tags.objects.all().order_by('bill_tags_name')

    # for cust_bill in all_cust_bill:

    #     bill_tags1 = cust_bill.bill_tags

    #     if cust_bill.bill_tags:
    #         bill_tags_list = list(bill_tags1.split(","))

    #     else:
    #         bill_tags_list = ""

    #     bill_tags2 = []
    
    #     if bill_tags1:

    #         for x in range(len(bill_tags_list)): 

    #             try:

    #                 bill_tags1 = bill_tags.objects.get(id=bill_tags_list[x])

    #                 bill_tags2.append(bill_tags1.bill_tags_name)

    #             except:
    #                 pass

    #     bill_tags3 = ', '.join(map(str, bill_tags2))

    #     cust_bill.bill_tags_name = bill_tags3

    # from_date_temp  = ""
    # to_date_temp = ""

    # #Shopping analysis date filter

    # if request.method == 'POST':

    #     labels = []
    #     data = []

    #     from_date_temp = request.POST["from_date"]
    #     to_date_temp = request.POST["to_date"]

    #     # from_date = datetime.strptime(request.POST["from_date"], "%Y-%m-%d").date()
    #     from_date = datetime.strptime(str(request.POST["from_date"]), '%Y-%m-%d').strftime('%d-%m-%Y')
        
    #     # to_date = datetime.strptime(request.POST["to_date"], "%Y-%m-%d").date()
    #     to_date = datetime.strptime(str(request.POST["to_date"]), '%Y-%m-%d').strftime('%d-%m-%Y')

    #     # from_date = datetime.datetime.strptime(request.POST["from_date"], "%Y-%m-%d").date()
    #     # to_date = datetime.datetime.strptime(request.POST["to_date"], "%Y-%m-%d").date()
    
    #     for bills in customer_bills:
    #         if bills['bill_date'] >= from_date and bills['bill_date'] <= to_date:
    #             if bills['bill_category_name']:
    #                 if bills['bill_category_name'] in labels:
    #                     pass
    #                 else:
    #                     labels.append(bills['bill_category_name'])

    #     spend_by_bill_category = {new_list: 0 for new_list in labels}

    #     for oject in customer_bills:
    #         if oject['bill_date'] >= from_date and oject['bill_date'] <= to_date:
    #             for x in labels:
    #                 if oject['bill_category_name']:
    #                     if oject['bill_category_name'] == x:
    #                         spend_by_bill_category[x] =  spend_by_bill_category[x] + float(oject['bill_amount'])

    #     for object in spend_by_bill_category:
    #         data.append(spend_by_bill_category[object])

    #     context['from_date'] = request.POST["from_date"]
    #     context['to_date'] = request.POST["to_date"]

    #     #for Murchant Date filter

    #     labels1 = []
    #     data1 = []
        
    #     for bills1 in customer_bills:
    #         if bills1['bill_date'] >= from_date and bills1['bill_date'] <= to_date:
    #             if bills1['business_name']:
    #                 if bills1['business_name'] in labels1:
    #                     pass
    #                 else:
    #                     labels1.append(bills1['business_name'])

    #     spend_by_bill_business1 = {new_list1: 0 for new_list1 in labels1} 

    #     for oject1 in customer_bills:
    #         if oject1['bill_date'] >= from_date and oject1['bill_date'] <= to_date:
    #             for y in labels1:
    #                 if oject1['business_name']:
    #                     if oject1['business_name'] == y:
    #                         spend_by_bill_business1[y] =  spend_by_bill_business1[y] + float(oject1['bill_amount'])
        
    #     for object1 in spend_by_bill_business1:
    #         data1.append(spend_by_bill_business1[object1])
            
    #     context['from_date'] = request.POST["from_date"]
    #     context['to_date'] = request.POST["to_date"]

    # coupon_list = CouponModel.objects.all().order_by("-id")
    # parking_lot_passes = ParkingLotPass.objects.filter(mobile_no=request.user)

    # try:
    #     for objects in parking_lot_passes:
    #         bussiness_id = objects.m_business_id
    #         obj = MerchantProfile.objects.get(id=bussiness_id)
    #         objects.business_name = obj.m_business_name
    #         objects.bussiness_logo = obj.m_business_logo
    # except:
    #     pass
   
    # # billCountchart
    # context['billCountchart_labels'] = ','.join(map(str, labels))

    # # print(total_bill_amount)
    # # sdb

    # context = {
    #     "parking_lot_pass": parking_lot_passes,
    #     'business_name': b_name,
    #     'bill_category': bill_category_name,
    #     "customer_bill": customer_bills,
    #     "bill_tags": customer_bill_tags,
    #     'DashboardNavclass': 'active',
    #     'segment':'index',

    #     'labels':labels,
    #     'data':data,
    #     'merchant_bill_count_doughnut' : merchant_bill_count_doughnut,

    #     'data1': data1,
    #     'labels1':labels1,
    #     'category_bill_count_doughnut' : category_bill_count_doughnut,
       
    #     'green_points':GreenPoints,
    #     'from_date' : from_date_temp,
    #     'to_date' : to_date_temp,
    #     'coupon_list':coupon_list,

    #     'total_bill_amount' : total_bill_amount,

    #     'bill_flagged': bill_flagged,
    #     'total_bill_count': bill_count,

    #     'total_merchant_bill_count': total_merchant_bill_count,
    #     'total_category_bill_count': total_category_bill_count,
    #     }
    
    # html_template = loader.get_template('customer-index.html')

    # return HttpResponse(html_template.render(context, request))

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_index(request):

    context = {} 

    par_user_id = Partner_users.objects.get(user_id=request.user)

    total_customers = Customer_Info_Model.objects.filter(per_id=request.user).count()

    todays_customers = Customer_Info_Model.objects.filter(per_id=request.user, date_joined__date = timezone.now()).count()

    partner_object = par_user_id.partner_user_id

    customer_object1 = GreenBillUser.objects.get(mobile_no = partner_object)

    total_merchant_count = MerchantProfile.objects.filter(merchant_by_partner=customer_object1).count()

    active_merchants = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, m_active_account = True).count()

    new_registered_merchants = MerchantProfile.objects.filter(merchant_by_partner=customer_object1, date_joined__date = timezone.now()).count()

    merchant_digital_bills_data = []
        
    partner_merchant_info = MerchantProfile.objects.filter(merchant_by_partner=request.user).order_by('-id')

    all_bills = 0

    partner_object_id = PartnerProfile.objects.get(p_user = partner_object)

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



    # SMS and notification
    for merchant in partner_merchant_info:

        merchant_profile_id = MerchantProfile.objects.get(id=merchant.id)

        user_id = GreenBillUser.objects.get(mobile_no = merchant.m_user)

        if request.method == 'POST': 

            customer_bill1 = CustomerBill.objects.filter(business_name = merchant_profile_id, customer_added = False, created_at__gte = sd_filter, created_at__lte = ed_filter)

            merchant_bill1 = MerchantBill.objects.filter(business_name = merchant_profile_id, created_at__gte = sd_filter, created_at__lte = ed_filter)

            parking_bill_list1 = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile_id, is_pass = False, created_at__gte = sd_filter, created_at__lte = ed_filter)

            petrol_bill_list1 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile_id, created_at__gte = sd_filter, created_at__lte = ed_filter)
        else:
            
            customer_bill1 = CustomerBill.objects.filter(business_name = merchant_profile_id, customer_added = False, created_at__date = timezone.now())

            merchant_bill1 = MerchantBill.objects.filter(business_name = merchant_profile_id, created_at__date = timezone.now())

            parking_bill_list1 = SaveParkingLotBill.objects.filter(m_business_id = merchant_profile_id, is_pass = False, created_at__date = timezone.now())

            petrol_bill_list1 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_profile_id, created_at__date = timezone.now())


        total_bill_notification = 0
        for bill in customer_bill1:
            if bill.greenbill_digital_bill == "True":
                total_bill_notification = total_bill_notification + 1

        for bill in merchant_bill1:
            if bill.greenbill_digital_bill == "True":
                total_bill_notification = total_bill_notification + 1

        for bill in parking_bill_list1:
            if bill.greenbill_digital_bill == "True":
                total_bill_notification = total_bill_notification + 1

        for bill in petrol_bill_list1:
            if bill.greenbill_digital_bill == "True":
                total_bill_notification = total_bill_notification + 1

        total_bill_sms = 0

        for bill in customer_bill1:
            if bill.greenbill_sms_bill == "True":
                total_bill_sms = total_bill_sms + 1

        for bill in merchant_bill1:
            if bill.greenbill_sms_bill == "True":
                total_bill_sms = total_bill_sms + 1

        for bill in parking_bill_list1:
            if bill.greenbill_sms_bill == "True":
                total_bill_sms = total_bill_sms + 1

        for bill in petrol_bill_list1:
            if bill.greenbill_sms_bill == "True":
                total_bill_sms = total_bill_sms + 1

    try:
        merchant_digital_bills_data.append(total_bill_sms)
    except:
        merchant_digital_bills_data.append(0)


    try:
        merchant_digital_bills_data.append(total_bill_notification)
    except:
        merchant_digital_bills_data.append(0)

    # Total sms send
    merchant_sms_data = []
    total_transaction_sms_plan = 0
    total_promotional_sms_plan = 0
    partner_merchant_info = MerchantProfile.objects.filter(merchant_by_partner=request.user).order_by('-id')
    for merchant in partner_merchant_info:
        if request.method == 'POST': 
            transactional_sms_count = transactional_sms_subscriptions.objects.filter(is_active = True, merchant_id = merchant.m_user, purchase_date__gte = sd_filter, purchase_date__lte = ed_filter)
        else:
            transactional_sms_count = transactional_sms_subscriptions.objects.filter(is_active = True, merchant_id = merchant.m_user, purchase_date__date = timezone.now())
        for sms in transactional_sms_count:
            if sms:
                business_ids = sms.business_ids.split(',')
                if str(merchant.id) in business_ids:
                    try:
                        total_tran_sms = transactional_sms_subscriptions.objects.filter(id = sms.id, is_active = True).aggregate(Sum('total_sms'))['total_sms__sum']
                        total_tran_sms_available = transactional_sms_subscriptions.objects.filter(id = sms.id, is_active = True).aggregate(Sum('total_sms_avilable'))['total_sms_avilable__sum']
                        transactional_sent_sms = int(total_tran_sms) - int(total_tran_sms_available)
                        total_transaction_sms_plan = int(total_transaction_sms_plan) + int(transactional_sent_sms)
                    except:
                        pass
    try:
        merchant_sms_data.append(total_transaction_sms_plan)
    except:
        merchant_sms_data.append(0)


    partner_merchant_info = MerchantProfile.objects.filter(merchant_by_partner=request.user).order_by('-id')
    for merchant in partner_merchant_info:
        if request.method == 'POST': 
            promotional_sms_count = promotional_sms_subscriptions.objects.filter(is_active = True, merchant_id = merchant.m_user, purchase_date__gte = sd_filter, purchase_date__lte = ed_filter)
        else:
            promotional_sms_count = promotional_sms_subscriptions.objects.filter(is_active = True, merchant_id = merchant.m_user, purchase_date__date = timezone.now())
        for sms in promotional_sms_count:
            if sms:
                business_ids = sms.business_ids.split(',')
                if str(merchant.id) in business_ids:
                    try:
                        total_promo_sms = promotional_sms_subscriptions.objects.filter(id = sms.id, is_active = True).aggregate(Sum('total_sms'))['total_sms__sum']
                        total_promo_sms_available = promotional_sms_subscriptions.objects.filter(id = sms.id, is_active = True).aggregate(Sum('total_sms_avilable'))['total_sms_avilable__sum']
                        promotional_sent_sms = int(total_promo_sms) - int(total_promo_sms_available)
                        total_promotional_sms_plan = int(total_promotional_sms_plan) + int(promotional_sent_sms)
                    except:
                        pass
    try:
        merchant_sms_data.append(total_promotional_sms_plan)
    except:
        merchant_sms_data.append(0)

    coupon_active_count = 0
    coupon_expired_count = 0

    today = date.today()

    current_date = today.strftime("%Y-%m-%d")
    current_date_new = datetime.strptime(str(current_date), "%Y-%m-%d")

    for merchant_business in partner_merchant_info:
        all_coupons = CouponModel.objects.filter(merchant_business_id = merchant_business.id)

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
    coupons_data_temp.append(coupon_active_count)
    coupons_data_temp.append(coupon_expired_count)

    offer_active_count = 0
    offer_expired_count = 0
    offer_not_approved = 0
            
    for merchant_business in partner_merchant_info:

        all_offers = OfferModel.objects.filter(merchant_business_id = merchant_business)

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
    offer_data_temp.append(offer_active_count)
    offer_data_temp.append(offer_expired_count)
    offer_data_temp.append(offer_not_approved)

    state_labels = []
    state_data1 = []
    
    if request.method == 'POST':
        merchant_state_dict = MerchantProfile.objects.filter(merchant_by_partner=request.user, date_joined__gte = sd_filter, date_joined__lte = ed_filter).values('m_state').distinct()
        # merchants By State
        for state in merchant_state_dict:
            
            merchant_count_by_state = MerchantProfile.objects.filter(merchant_by_partner=request.user, m_state = state['m_state'], date_joined__gte = sd_filter, date_joined__lte = ed_filter).count()
            state_data1.append(merchant_count_by_state)
            states_name = "'" + state['m_state'] + "'"
            state_labels.append(states_name)
    else:
        merchant_state_dict = MerchantProfile.objects.filter(merchant_by_partner=request.user, date_joined__date = timezone.now()).values('m_state').distinct()
        # merchants By State
        for state in merchant_state_dict:
            
            merchant_count_by_state = MerchantProfile.objects.filter(merchant_by_partner=request.user, m_state = state['m_state'], date_joined__date = timezone.now()).count()
            state_data1.append(merchant_count_by_state)

            states_name = "'" + state['m_state'] + "'"
            state_labels.append(states_name)

    city_labels = []
    city_data1 = []

    if request.method == 'POST':
        merchant_city_dict = MerchantProfile.objects.filter(merchant_by_partner=request.user, date_joined__gte = sd_filter, date_joined__lte = ed_filter).values('m_city').distinct() 
        # merchants By City
        for city in merchant_city_dict:      
            merchant_count_by_city = MerchantProfile.objects.filter(merchant_by_partner=request.user, m_city = city['m_city'], date_joined__gte = sd_filter, date_joined__lte = ed_filter).count()

            city_data1.append(merchant_count_by_city)

            cities_name = "'" + city['m_city'] + "'"
            city_labels.append(cities_name)
    else:
        merchant_city_dict = MerchantProfile.objects.filter(merchant_by_partner=request.user, date_joined__date = timezone.now()).values('m_city').distinct() 
        # merchants By City
        for city in merchant_city_dict:      
            merchant_count_by_city = MerchantProfile.objects.filter(merchant_by_partner=request.user, m_city = city['m_city'], date_joined__date = timezone.now()).count()

            city_data1.append(merchant_count_by_city)

            cities_name = "'" + city['m_city'] + "'"
            city_labels.append(cities_name)


    print('aa',state_data1)       
    green_bill_plan = 0
    transactional_plan_count = 0
    promotional_plan_count = 0

    merchant_plan_data = []

    for merchant_business in partner_merchant_info:
        startswith = str(merchant_business.id) + ','
        endswith = ','+ str(merchant_business.id)
        contains = ','+ str(merchant_business.id) + ','
        exact = str(merchant_business.id)

        try:  
            subscription_object = merchant_subscriptions.objects.get(
                Q(merchant_id = merchant_business.m_user),
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )

            green_bill_plan = green_bill_plan + 1

        except:
            pass

        try:  
            subscription_object = transactional_sms_subscriptions.objects.get(
                Q(merchant_id = merchant_business.m_user),
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )
            transactional_plan_count = transactional_plan_count + 1

        except:
            pass

        try:  
            subscription_object = promotional_sms_subscriptions.objects.get(
                Q(merchant_id = merchant_business.m_user),
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )
            promotional_plan_count = promotional_plan_count + 1

        except:
            pass
    merchant_plan_data.append(green_bill_plan)
    merchant_plan_data.append(transactional_plan_count)
    merchant_plan_data.append(promotional_plan_count)

    if request.method == 'POST':
        merchant_dict_by_cat = MerchantProfile.objects.filter(merchant_by_partner=request.user, date_joined__gte = sd_filter, date_joined__lte = ed_filter).values('m_business_category').distinct()
    else:
        merchant_dict_by_cat = MerchantProfile.objects.filter(merchant_by_partner=request.user, date_joined__date = timezone.now()).values('m_business_category').distinct()
    category_name_list = []
    merchants_list_by_category = []
    import json
    for category in merchant_dict_by_cat:
        business_category_name = business_category.objects.get(id = category['m_business_category']).business_category_name
        business_category_name1 = "'" + business_category_name + "'"
        category_name_list.append(business_category_name1)

        if request.method == 'POST':
            merchant_count_by_category = MerchantProfile.objects.filter(merchant_by_partner=request.user, m_business_category = category['m_business_category'], date_joined__gte = sd_filter, date_joined__lte = ed_filter).count()
        else:
            merchant_count_by_category = MerchantProfile.objects.filter(merchant_by_partner=request.user, m_business_category = category['m_business_category'], date_joined__date = timezone.now()).count()

        merchants_list_by_category.append(merchant_count_by_category)

    # merchants_list_by_category = ("[{0}]".format(', '.join(map(str, merchants_list_by_category))))

    # category_name_list = json.dumps(category_name_list)
    
    print(category_name_list,merchants_list_by_category)
    context = {
        'merchant_plan_data': merchant_plan_data,
        'coupons_labels': coupons_labels_temp,
        'coupons_data': coupons_data_temp,
        'coupon_expired_count': coupon_expired_count,
        'coupon_active_count': coupon_active_count,
        'offer_labels': offer_labels_temp,
        'offer_data': offer_data_temp,
        'offer_expired_count': offer_expired_count,
        'offer_active_count': offer_active_count,
        'merchants_list_by_category': ','.join(map(str, merchants_list_by_category)),
        'category_name_list': ','.join(map(str, category_name_list)),
        'state_data1': ','.join(map(str, state_data1)),
        'state_labels': ','.join(map(str, state_labels)),
        'city_data1': ','.join(map(str, city_data1)),
        'city_labels': ','.join(map(str, city_labels)),
        'from_date1': from_date_temp1,
        'to_date1': to_date_temp1,
        'DashboardNavclass': "active",
        'merchantNavActiveClass': "active", 
        'MerchantInfoCollapseShow': "show",
        'MerchantListNavclass': "active",
        "total_merchant": total_merchant_count,
        "todays_customers": todays_customers,
        "total_customers": total_customers,
        'partnerListcount': active_merchants,
        'merchatListCount' : new_registered_merchants,
        'partner_object_id': partner_object_id,
        # "total_payment" : total_payment,
        # "total_payment_commision" : total_payment_commision1,
        # "partner_category": partner_category,
        "merchant_sms_data": merchant_sms_data,
        "merchant_digital_bills_data":merchant_digital_bills_data,
        # "from_date1":form_date_temp1,
        # "to_date1":to_date_temp1,
    }
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
        
    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template( 'page-404.html' )
    #     return HttpResponse(html_template.render(context, request))

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

        print(m_business_previous_id,'------------------------',m_business)
        
        MerchantProfile.objects.filter(m_user = merchant_object).update(m_active_account = False)
        # MerchantProfile.objects.filter(id=m_business_previous_id).update(m_active_account = False)
        MerchantProfile.objects.filter(id=m_business).update(m_active_account = True)
        # sweetify.success(request, title="Success", icon='success', text='Business Updated.', timer=1000)
        return redirect(merchant_index)
    else:
        # sweetify.success(request, title="Oops...", icon='error', text='Fail to Updated.', timer=1000)
        return redirect(merchant_index)


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
        print('mobile_no',mobile_no)
        print('newPassword',newPassword)
        result = GreenBillUser.objects.filter(mobile_no=mobile_no).values('id')[0]['id']
        user_object = GreenBillUser.objects.get(id=result)
        
        success = GreenBillUser.check_password(user_object, newPassword)
        
        if success == True:
            
            return JsonResponse({ 'status' : 'errorOldPass', 'msg': "New Password cannot be same as Old Password"})
        else:
            print('check')
            user_object.set_password(newPassword)
            user_object.save()
            print('user_object',user_object)
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
            address_proof = form.cleaned_data.get('address_proof')

            temp = generalSetting.objects.update_or_create(id=1, defaults={'business_name': business_name, 'business_code': business_code, 'mobile_no': mobile_no, 'email': email, 'date_format': date_format, 'currency': currency, 'android_app_url': android_app_url, 'iphone_app_url': iphone_app_url,
            'alternate_mobile_number' : alternate_mobile_number,'alternate_email' : alternate_email,'address' : address, 'pan_number' : pan_number,
            'city' : city,'area' : area,'distrct' : distrct,'state' : state,'pin_code' : pin_code,'aadhaar_number' : aadhaar_number,'gstin' : gstin,'cin' : cin,
            'tin_vat_number' : tin_vat_number,'bank_account_number' : bank_account_number,'bank_IFSC_code' : bank_IFSC_code,'bank_name' : bank_name,'bank_branch' : bank_branch, 'address_proof':address_proof,})
           
            if o_business_logo:
                generalSetting.objects.update_or_create(id=1, defaults={'o_business_logo':o_business_logo})

            if o_digital_signature:
                
                generalSetting.objects.update_or_create(id=1, defaults={'o_digital_signature':o_digital_signature})

            if o_business_stamp:
                generalSetting.objects.update_or_create(id=1, defaults={'o_business_stamp':o_business_stamp})

            if GSTIN_certificate:
                generalSetting.objects.update_or_create(id = 1, defaults={ "GSTIN_certificate" : GSTIN_certificate })

            if CIN_certificate:
                generalSetting.objects.update_or_create(id = 1, defaults={ "CIN_certificate" : CIN_certificate })
            
            if cancelled_cheque_certificate:
                generalSetting.objects.update_or_create(id = 1, defaults={ "cancelled_cheque_certificate" : cancelled_cheque_certificate })

            if udyog_adhar_certificate:
                generalSetting.objects.update_or_create(id = 1, defaults={ "udyog_adhar_certificate" : udyog_adhar_certificate })
            
            if address_proof:
                generalSetting.objects.update_or_create(id = 1, defaults={ "address_proof" : address_proof })
            


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
            # data = {
            #     'result': True,
            #     'state': 200,
            #     'message': 'Success',
            # }

            # redirect("/general-setting/")
            sweetify.success(request, title="Success...", icon='success', text='Signature updated successfully...', timer=1500)

            return redirect("/general-setting/")
            # return JsonResponse({'data': data})

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
            # data = {
            #     'result': True,
            #     'state': 200,
            #     'message': 'Success',
            # }
            # return JsonResponse({'data': data})
            sweetify.success(request, title="Success...", icon='success', text='Stamp updated successfully...', timer=1500)
            return redirect("/general-setting/")

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
            # data = {
            #     'result': True,
            #     'state': 200,
            #     'message': 'Success',
            # }
            # return JsonResponse({'data': data})
            sweetify.success(request, title="Success...", icon='success', text='Logo updated successfully...', timer=1500)
            return redirect("/general-setting/")



# Customer Parking Lot Passes
@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def Parking_Lot_Passes(request):
    parking_lot_passes = ParkingLotPass.objects.filter(mobile_no=request.user).order_by('-id')
    try:
        today = date.today()
        data = []
        for obj in parking_lot_passes:
            if obj.valid_to >= today:
                data.append(obj)

        for objects in data:
            if objects.valid_to >= today: 
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
        "parking_lot_pass": data,
        
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
        print('merchant_business_id',merchant_business_id)

        customer_bill_list = CustomerBill.objects.filter(Q(business_name = merchant_business_object), (Q(mobile_no__icontains = keywords) | Q(invoice_no__icontains = keywords))).order_by('-id')

        for bill in customer_bill_list:
            try:
                bill_file = str(base_url) + str(bill.bill.url)
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
                'amount': str(bill.bill_amount),
                'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "CustomerBill",
                'customer_added': False,
                'bill_ratings': ratings,
                'rating': bill.rating,
                'created_by': created_by,
                'created_by_id': created_by_id,
                'bill_flag': False,
            })

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

        merchant_bill_list = MerchantBill.objects.filter(Q(business_name = merchant_business_object), (Q(mobile_no__icontains = keywords) | Q(invoice_no__icontains = keywords))).order_by('-id')

        for bill in merchant_bill_list:
            try:
                bill_file = str(base_url) + str(bill.bill.url)
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
                'amount': str(bill.bill_amount),
                'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "MerchantBill",
                'customer_added': False,
                'bill_ratings': ratings,
                'rating': bill.rating,
                'created_by': created_by,
                'created_by_id': created_by_id,
                'bill_flag': False,
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


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def search(request):
    
    if request.method == "POST":

       

        keywords = request.POST.get("search_keyword")
        print('KK',keywords)
        data = []

        base_url = "http://157.230.228.250/"

        # try:
        #     bill_design = bill_designs.objects.get(merchant_business_id = merchant_business_object)
        #     bill_rating_emoji = bill_design.rating_emoji
        # except:
        #     bill_rating_emoji = ""

        # parking_bill_list = SaveParkingLotBill.objects.filter(Q(m_business_id = merchant_business_id), 
        # (Q(mobile_no__icontains = keywords) | Q(invoice_no__icontains = keywords))).order_by('-id')
        # print(GreenBillUser.objects.get(mobile_no=keywords))
        try:
            merchant = MerchantProfile.objects.filter(m_user = GreenBillUser.objects.get(mobile_no=keywords))
        except:
            merchant = ''
        # print(merchant)

        for bill in merchant:
            
            

            data.append({
                'mobile_no' : bill.m_user,
                'business_name': bill.m_business_name,
                'category':bill.m_business_category,
                'city': bill.m_city,
                'district': bill.m_district,
                'area': bill.m_area,
                
            })

        

       

        context = {"bills":data}

    else:
        context = {"bills":""}

    return render(request,'search.html',context)



def test_sms(request):

   #  import requests

   #  import time
  
   #  ts = time.time()

   #  # http://157.230.228.250/self-added-bill/502sNRQ426eT/

   #  data_temp = {
            # "keyword":"DEMO",
            # "timeStamp":ts,
            # "dataSet":
   #            [
   #                {
   #                    "UNIQUE_ID":"735694wew", # https://bit.ly/3sKHq09
   #                    "MESSAGE":"Hey Green Bill user to view or download your bill click on link https://tinyurl.com/yfka5v4n to view all your bills download Green Bill App",
   #                    "OA":"GBPARK",
   #                    "MSISDN":"7709977798",
   #                    "CHANNEL":"SMS",
   #                    "CAMPAIGN_NAME":"hind_user",
   #                    "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
   #                    "USER_NAME":"hind_hsi",
   #                    "DLT_TM_ID":"1001096933494158",
   #                    "DLT_CT_ID":"1007161814187973948", # Template Id
   #                    "DLT_PE_ID":"1001659120000037015" 
   #                }
   #            ]
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
                context['from_date'] = from_date
                context['to_date'] = to_date

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
            
            print('amount_collected',amount_collected)
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

        total_transaction1 = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False).count()

        total_transaction2 = MerchantBill.objects.filter(business_name = merchant_business).count()

        total_transaction = total_transaction1 + total_transaction2

        context['total_transaction'] = total_transaction

        date_joined = merchant_business.date_joined

        today = date.today()

        current_date = today.strftime("%Y-%m-%d")
        current_date_new = datetime.strptime(str(current_date), "%Y-%m-%d")
        date_joined_new = datetime.strptime(str(date_joined.date()), "%Y-%m-%d")
        diff = current_date_new - date_joined_new

        total_days = diff.days

        average_transaction = 0

        if total_transaction != 0 and total_days != 0:
            average_transaction = total_transaction/total_days
        else:
            average_transaction = 0

        context['average_transaction'] = average_transaction

        customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False).order_by('-id')

        merchant_bill = MerchantBill.objects.filter(business_name = merchant_business).order_by('-id')

        total_sales = 0

        for bill in customer_bill:
            total_sales = total_sales + float(bill.bill_amount)

        for bill in merchant_bill:
            total_sales = total_sales + float(bill.bill_amount)

        context['total_sales'] = total_sales

        average_sales = 0

        if total_transaction != 0 and total_sales != 0:
            average_sales = total_sales/total_transaction
        else:
            average_sales = 0

        context['average_sales'] = average_sales

        customer_bill = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__date = timezone.now()).order_by('-id')

        merchant_bill = MerchantBill.objects.filter(business_name = merchant_business, created_at__date = timezone.now()).order_by('-id')

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

            if int(bill.bill_received_business_name) == merchant_business.id:
                received_bill_count = received_bill_count + 1

        billing_analysis_labels_temp = []
        billing_analysis_labels_temp.append("Sent Bills")
        billing_analysis_labels_temp.append("Received Bills")
        billing_analysis_labels_temp.append("Rejected Bills")
        context['billing_analysis_labels'] = billing_analysis_labels_temp

        billing_analysis_data_temp = []
        billing_analysis_data_temp.append(str(sent_bill_count))
        billing_analysis_data_temp.append(str(received_bill_count))
        billing_analysis_data_temp.append(str(rejected_bill_count))
        context['billing_analysis_data'] = billing_analysis_data_temp


        notifications = sent_bill_history.objects.filter(
            m_business_id = merchant_business.id,
            created_at__date = timezone.now(),
            digital_bill = True
        ).count()

        sms = sent_bill_history.objects.filter(
            m_business_id = merchant_business.id,
            created_at__date = timezone.now(),
            sms_bill = True
        ).count()

        digital_billing_labels_temp = []
        digital_billing_labels_temp.append("SMS Sent")
        digital_billing_labels_temp.append("Notifications Sent")
        context['digital_billing_labels'] = digital_billing_labels_temp

        digital_billing_data_temp = []
        digital_billing_data_temp.append(str(sms))
        digital_billing_data_temp.append(str(notifications))
        context['digital_billing_data'] = digital_billing_data_temp

        # unique_customer = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False).order_by('-id').distinct('mobile_no').count()

        new_customers = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, created_at__date = timezone.now()).distinct()

        new_customer_count = 0
        for customer in new_customers:
            bill_count = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = customer.mobile_no).count()
            if bill_count == 2:
                new_customer_count = new_customer_count + 1
            
        total_customers = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False).distinct()

        total_customer_count = total_customers.count()

        new_customers_value = 0

        if new_customer_count != 0 and total_customer_count != 0:
            new_customers_value = int((new_customer_count * 100)/total_customer_count)
            new_customers_text = str(new_customer_count)
        else:
            new_customers_value = 0
            new_customers_text = 0

        context['new_customers_text'] = str(new_customers_text)
        context['new_customers_value'] = str(new_customers_value)

        returning_customers_count = 0
        for customer in new_customers:
            bill_count = CustomerBill.objects.filter(business_name = merchant_business, customer_added = False, mobile_no = customer.mobile_no).count()
            if bill_count >= 2:
                returning_customers_count = returning_customers_count + 1

        if returning_customers_count != 0 and total_customer_count != 0:
            returning_customers_value = int((returning_customers_count * 100)/total_customer_count)
            returning_customers_text = str(returning_customers_count)
        else:
            returning_customers_value = 0
            returning_customers_text = 0

        context['returning_customers_text'] = str(returning_customers_text)
        context['returning_customers_value'] = str(returning_customers_value)

        # Coupons Chart

        all_coupons = CouponModel.objects.filter(merchant_business_id = merchant_business.id)

        coupon_active_count = 0
        coupon_expired_count = 0

        for coupon in all_coupons:
            valid_to_date = datetime.strptime(str(coupon.valid_through), "%Y-%m-%d")
            if valid_to_date < current_date_new:
                coupon_expired_count = coupon_expired_count + 1
            else:
                coupon_active_count = coupon_active_count + 1

        coupons_labels_temp = []
        coupons_labels_temp.append("Active")
        coupons_labels_temp.append("Expired")
        context['coupons_labels'] = coupons_labels_temp

        coupons_data_temp = []
        coupons_data_temp.append(str(coupon_active_count))
        coupons_data_temp.append(str(coupon_expired_count))
        context['coupons_data'] = coupons_data_temp

        context['coupon_expired_count'] = coupon_expired_count
        context['coupon_active_count'] = coupon_active_count

        # Offers Chart

        all_offers = OfferModel.objects.filter(merchant_business_id = merchant_business)

        offer_active_count = 0
        offer_expired_count = 0
        offer_not_approved = 0

        for offer in all_offers:
            valid_to_date = datetime.strptime(str(offer.valid_through), "%Y-%m-%d")
            if valid_to_date < current_date_new:
                offer_expired_count = offer_expired_count + 1
            elif offer.status == "1":
                offer_active_count = offer_active_count + 1
            if offer.status == "0":
                offer_not_approved = offer_not_approved + 1

        offer_labels_temp = []
        offer_labels_temp.append("Active")
        offer_labels_temp.append("Expired")
        offer_labels_temp.append("Not Approved")
        context['offer_labels'] = offer_labels_temp

        offer_data_temp = []
        offer_data_temp.append(str(offer_active_count))
        offer_data_temp.append(str(offer_expired_count))
        offer_data_temp.append(str(offer_not_approved))
        context['offer_data'] = offer_data_temp

        context['offer_expired_count'] = offer_expired_count
        context['offer_active_count'] = offer_active_count

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


def getPartnerActivePromotionalSubscriptionPlan(request, partner_id):

    subscription_object = ""

    if partner_id:
        try:
            subscription_object = partner_promotional_sms_subscriptions.objects.get(is_active = True, partner_id = partner_id)
            return subscription_object
        except:
            return subscription_object
    else:
        return subscription_object


def getPartnerActiveTransactionalSubscriptionPlan(request, partner_id):

    subscription_object = ""

    if partner_id:
        try:
            subscription_object = partner_transactional_sms_subscriptions.objects.get(is_active = True, partner_id = partner_id)
            return subscription_object
        except:
            return subscription_object
    else:
        return subscription_object



@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def customerPaymentHistory(request):
    customer_bill = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, payment_done=True, customer_added=False)
    parking_bill = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, payment_done=True)
    petrol_bill = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, payment_done=True)

    data = []
    for bill in customer_bill:
        data.append({
            'invoice_no' : bill.invoice_no,
            'mobile_no' : bill.mobile_no,
            'amount' : float(bill.bill_amount),
            'created_at' : bill.created_at,
            'date': datetime.strptime(str(bill.bill_date), '%d-%m-%Y').strftime('%d-%m-%Y'),
            'transaction_id' : bill.transaction_id,
            # 'business_name' : bill.business_name,
            })
    for bill in parking_bill:
        data.append({
            'invoice_no' : bill.invoice_no,
            'mobile_no' : bill.mobile_no,
            'amount' : float(bill.amount),
            'created_at' : bill.created_at,
            'date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
            'transaction_id' : bill.transaction_id,
            # 'business_name' : bill.business_name,
            })
    for bill in petrol_bill:
        data.append({
            'invoice_no' : bill.invoice_no,
            'mobile_no' : bill.mobile_no,
            'amount' : float(bill.amount),
            'created_at' : bill.created_at,
            'transaction_id' : bill.transaction_id,
            'date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
            # 'business_name' : bill.business_name,
            })
        # total_amount_spent
        # total_bill_count
    total_amount_spent = 0
    for total in data:
        total_amount_spent = total_amount_spent + float(total['amount'])
        
    total_bill_count = len(data)

    if request.method == "POST":
        user = request.POST.get('user')
        from_date = request.POST['from_date']
        from_date_var = from_date
        to_date = request.POST['to_date']
        to_date_var = to_date

        new_data = []

        if data:
            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
                

            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            print('a',from_date)
            for bill in data:
                
                if from_date and to_date:

                    if bill ['date'] >= from_date and bill['date'] <= to_date:
                        new_data.append(bill)

                elif from_date:
                    # bill_date = datetime.strptime(str(bill['date']), '%d-%m-%d').strftime('%Y-%m-%d')
                    print('bill_date',bill['date'])
                    if bill['date'] <= from_date:
                        print('abcd')
                        new_data.append(bill)

                elif to_date:
                    
                    if bill['date'] <= to_date:
                        new_data.append(bill)

        total_amount_spent = 0
        for z in new_data:
            total_amount_spent = total_amount_spent + float(z['amount'])
        
        total_bill_count = len(new_data)

        context = {
            'from_date': from_date_var,
            'to_date': to_date_var,
            "payment_history" : new_data,
        }
        return render(request, 'customer/payment-history.html', context)
    else:
        data.sort(key = lambda x: datetime.strptime(x['date'], '%d-%m-%Y'), reverse = True)
        context = {
            'payment_history':data,
            'total_amount_spent':total_amount_spent,
            'total_bill_count':total_bill_count,
        }
    return render(request, 'customer/payment-history.html', context)


def Download_customer_app(request):
    return render(request,"customer/download_customer_app.html")


def test_sms(result):

    ts = int(time.time())

    sms_data_temp = {
            "keyword":"Web Forgot Password OTP",
            "timeStamp":ts,
            "dataSet":
                [
                    {
                        "UNIQUE_ID":"GB-" + str(ts),
                        "MESSAGE":"Dear Green Bill user, Use " + str(123456) + " as OTP to reset your password.",
                        "OA":"GRBILL",
                        "MSISDN":str(770997779), # Recipient's Mobile Number
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

    print(response.content)
    print(response.text)
    print(response.json)
    print(response.reason)

    return response


