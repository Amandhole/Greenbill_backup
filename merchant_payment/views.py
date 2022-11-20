import os
import random
import sweetify

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from django.contrib.auth import update_session_auth_hash
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
from users.models import GreenBillUser, UserProfileImage, Merchant_users
from role.models import *
from merchant_role.models import merchant_role, merchant_userrole
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff, getActiveTransactionalSubscriptionPlan
from my_subscription.models import recharge_history
from offers.models import OfferModel
from referral_points.models import *
from coupon.models import *

import random
import string


from merchant_software_apis.models import CustomerBill, MerchantBill
from parking_lot_apis.models import SaveParkingLotBill
from petrol_pump_apis.models import SavePetrolPumpBill
# payu
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
import datetime
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils import timezone
# SMS
from merchant_payment.models import PaymentLinks
import requests
import time
from datetime import datetime, date
import pyshorteners

from my_subscription.models import *

from merchant_setting.models import MerchantPaymentSetting
from promotions.models import *



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def payment_upi(request):
    return HttpResponse("Hello")

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def GetPaymentLink(request):

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']
    business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)

    subscription_object = getActiveTransactionalSubscriptionPlan(request, business_object.id)
    payment_link = ""
    try:
        payment_settings = MerchantPaymentSetting.objects.get(m_business_id = business_object.id)
    except:
        payment_settings = ""

    if request.method == "POST":

        if subscription_object:

            if subscription_object.total_sms_avilable:

                if int(subscription_object.total_sms_avilable) >= int(1):

                    mobile_no = request.POST['mobile_no']
                    name = request.POST['name']
                    email = request.POST['email']
                    amount = request.POST['amount']
                    description = request.POST['description']
                    send_sms = request.POST['send_sms']

                    result = PaymentLinks.objects.create(m_business_id = business_object.id, mobile_no = mobile_no, name = name, email = email, amount = amount, description = description)

                    if result and send_sms:
                        letters = string.ascii_letters
                        digit = string.digits
                        random_string = str(result.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                        PaymentLinks.objects.filter(id=result.id).update(payment_url = random_string)

                        payment_url_temp = "http://157.230.228.250/payment-link/" + str(random_string) + "/"

                        s = pyshorteners.Shortener()

                        short_url = s.tinyurl.short(payment_url_temp)

                        payment_link = short_url
                        
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


                        base_link = "upi://pay?pa=9172508136@paytm&pn=Payee Name&tn=Payment Message&am="
                        pay_to_do = base_link+str(amount)+"&cu=INR"

                        response = requests.post(url, json = data_temp)
                        print("***************")
                        print(pay_to_do)
                    if result:
                        total_sms_avilable_new = 0
                        total_sms_avilable_new = int(subscription_object.total_sms_avilable) - int(1)
                        subscription_object.total_sms_avilable = total_sms_avilable_new
                        subscription_object.save()
                        sweetify.success(request, title="Success", icon='success', text='Payment Link created Successfully.', timer=1500)
                    else:
                        sweetify.success(request, title="Oops...", icon='error', text='Fail to create.', timer=1500)
                else:
                    sweetify.success(request, title="Oops...", icon='error', text='Insufficient Balance. Please purchase Transactional plan and try again !!!', timer=2000)     
            else:
                sweetify.success(request, title="Oops...", icon='error', text='Insufficient Balance. Please purchase Transactional plan and try again !!!', timer=2000)
        else:
            sweetify.success(request, title="Oops...", icon='error', text="You don't have active Transactional SMS plan. Please purchase and try again.", timer=2000)

    payment_link_list = PaymentLinks.objects.filter(m_business_id = business_object.id).order_by('-id')
    
    context = {
        "payment_link_list":payment_link_list,
        "payment_settings": payment_settings,
        "PaymentsNavclass":"active",
        "ShowPaymentsNavclass":"show",
        "PaymentLinkNavClass":"active",
        "payment-link":payment_link,
    }

    return render(request, 'merchant/payments/create-payment-link.html', context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def SendPaymentLink(request, id):

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']
    business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)

    subscription_object = getActiveTransactionalSubscriptionPlan(request, business_object.id)

    if subscription_object:

        if int(subscription_object.total_sms_avilable) >= int(1):

            link_id = id

            try:
                payment_link = PaymentLinks.objects.get(id = link_id)
            except:
                payment_link = ""

            try:
                business_object = MerchantProfile.objects.get(id = payment_link.m_business_id)
            except:
                business_object = ""

            if payment_link and business_object:
                letters = string.ascii_letters
                digit = string.digits
                random_string = str(payment_link.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                PaymentLinks.objects.filter(id=payment_link.id).update(payment_url = random_string)

                payment_url_temp = "http://157.230.228.250/payment-link/" + str(random_string) + "/"

                s = pyshorteners.Shortener()

                short_url = s.tinyurl.short(payment_url_temp)

                ts = int(time.time())

                # print(payment_link.mobile_no)

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
                    sweetify.success(request, title="Success", icon='success', text='Payment Link Send Successfully.', timer=1500)
                else:
                    sweetify.success(request, title="Oops...", icon='error', text='Fail to Send.', timer=1500)
            else:
                sweetify.success(request, title="Oops...", icon='error', text='Fail to Send.', timer=1500)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Insufficient Balance. Please purchase Transactional plan and try again !!!', timer=2000)
    else:
        sweetify.success(request, title="Oops...", icon='error', text="You don't have active Transactional SMS plan. Please purchase and try again.", timer=2000)

    return redirect(GetPaymentLink)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def DeletePaymentLink(request, id):
    link_id = id

    instance = PaymentLinks.objects.get(id=link_id)
    result = instance.delete()

    if result:
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})

def PaymentLink(request, id):
    link_url = id

    try:
        payment_link = PaymentLinks.objects.get(payment_url=link_url)
    except:
        payment_link = ""

    try:
        payment_settings = MerchantPaymentSetting.objects.get(m_business_id = payment_link.m_business_id)
    except:
        payment_settings = ""

    if payment_link and payment_settings:

        if payment_link.payment_done == False:

            key = str(payment_settings.payu_key)
        
            SALT= str(payment_settings.payu_salt)

            # PAYU_BASE_URL = "https://test.payu.in/_payment"
            PAYU_BASE_URL = "https://secure.payu.in/_payment"

            action = ''
            firstname = str(payment_link.name)
            email = str(payment_link.email)
            phone = str(payment_link.mobile_no)
            surl = "http://157.230.228.250/merchant-payment-link-success/"
            furl = "http://157.230.228.250/merchant-payment-link-fail/"

            udf1 = link_url
            udf2 = ""
            udf3 = ""
            udf4 = ""
            udf5 = ""

            random_str =  random.randint(9999999, 99999999)

            hash_object = hashlib.sha256(b'randint(0,20)' + bytes(payment_link.id) + bytes(random_str))

            txnid=hash_object.hexdigest()[0:20]

            hashh = ''
            context = {}
            posted = {}
            posted['txnid'] = txnid
            posted['key'] = key
            productinfo = str(payment_link.description)
            amount = str(payment_link.amount)

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
            context['payment_link'] = payment_link
        
        else:
            context = {}
            context['amount'] = payment_link.amount
            context['payment_link'] = payment_link

        return render(request, 'merchant/payments/payment-link.html', context)

    else:
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

    payment_link = PaymentLinks.objects.get(payment_url=link_url)

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
            
            result = PaymentLinks.objects.filter(id=payment_link.id).update(payment_done = True, payment_date = timezone.now(), transaction_id = txnid, payu_transaction_id = mihpayid)

            if result:
                sweetify.success(request, title="Success", icon='success', text='Transcation done Successfully.', timer=1500)
                return redirect(PaymentLink, link_url)
            else:
                sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
                return redirect(PaymentLink, link_url)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
            return redirect(PaymentLink, link_url)
    else:
        sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
        return redirect(PaymentLink, link_url)

@csrf_exempt
def payment_link_fail(request):
    udf1 = request.POST["udf1"]
    sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
    return redirect(PaymentLink, udf1)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def ReceivedPayments(request):

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']
    business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)
    print('received_payments',business_object.id)

    data = []

    received_payments = PaymentLinks.objects.filter(m_business_id = business_object.id, payment_done = True).order_by('-id')

    # print('received_payments',received_payments)
    
    for payment in received_payments:
        if payment.description:
            description = payment.description
        else:
            description = ''
        data.append({
            'mobile_no': payment.mobile_no,
            'amount' : payment.amount,
            'payment_date' : payment.payment_date,
            'transaction_id' : payment.transaction_id,
            'created_at' : payment.created_at,
            'payment_date_new':datetime.strptime(str(payment.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d'),
            'description':  description,
        })

        payment.payment_date = datetime.strptime(str(payment.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d')
    
    customer_bill = CustomerBill.objects.filter(business_name = business_object,payment_done = True)
    
    for customer in customer_bill:
        data.append({
            'mobile_no': customer.mobile_no,
            'amount' : customer.bill_amount,
            'payment_date' : customer.payment_date,
            'transaction_id' : customer.transaction_id,
            'created_at' : customer.created_at,
            'payment_date_new':datetime.strptime(str(customer.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d'),
            'description':  '',
        })

    merchant_bill = MerchantBill.objects.filter(business_name = business_object,payment_done = True)
    print('merchant_bill',merchant_bill)
    
    for merchant in merchant_bill:
        data.append({
            'mobile_no': merchant.mobile_no,
            'amount' : merchant.bill_amount,
            'payment_date' : merchant.payment_date,
            'transaction_id' : merchant.transaction_id,
            'created_at' : merchant.created_at,
            'payment_date_new':datetime.strptime(str(merchant.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d') if merchant.payment_date else "",
            'description':  '',
        })

    parking_bill = SaveParkingLotBill.objects.filter(m_business_id = business_object.id, payment_done = True) 
    for parking in parking_bill:
        data.append({
            'mobile_no': parking.mobile_no,
            'amount' : parking.amount,
            'payment_date' : parking.payment_date,
            'transaction_id' : parking.transaction_id,
            'created_at' : parking.created_at,
            'payment_date_new':datetime.strptime(str(parking.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d'),
            'description':  '',
        })

    petrol_bill = SavePetrolPumpBill.objects.filter(m_business_id = business_object.id, payment_done=True)
    for petrol in petrol_bill:
        data.append({
            'mobile_no': petrol.mobile_no,
            'amount' : petrol.amount,
            'payment_date' : petrol.payment_date,
            'transaction_id' : petrol.transaction_id,
            'created_at' : petrol.created_at,
            'payment_date_new' : datetime.strptime(str(petrol.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d'),
            'description':  '',
        })

    total_payments_count =  len(data)

    # bill.payment_date_new = datetime.strptime(str(bill.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d')

    # for bill in data:
    #     try:
    #         bill_file = str(base_url) + str(bill.bill.url)
    #     except:
    #         bill_file = ""
        # bill.payment_date_new = datetime.strptime(str(bill.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d')

    total_payment = 0.00

    for payment in data:
        total_payment = total_payment + float(payment['amount'])
    # print('data',data)

    if request.method == "POST":
        user = request.POST.get('user')
        from_date = request.POST['from_date']
        from_date_temp = from_date
        to_date = request.POST['to_date']
        to_date_temp = to_date

        new_data = []

        if data:
            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

            for bill in data:
                print(bill['payment_date_new'])
                print(from_date)
                print(to_date)
                if from_date and to_date:
                    if bill['payment_date_new'] >= from_date and bill['payment_date_new'] <= to_date:
                        print('ada')
                        new_data.append(bill)

                elif from_date:
                    if bill['payment_date_new'] >= from_date:
                        new_data.append(bill)

                elif to_date:
                    if bill['payment_date_new'] <= to_date:
                        new_data.append(bill)
        
        total_payment = 0.00
        total_payments_count = 0

        for payment in new_data:
            total_payment = total_payment + float(payment['amount'])

        total_payments_count = len(new_data)

        context = {
                'from_date': from_date_temp,
                'to_date': to_date_temp,
                "received_payments" : new_data,
                "total_payment" : total_payment,
                "total_payments_count" : total_payments_count,
                "PaymentsNavclass":"active",
                "ShowPaymentsNavclass":"show",
                "ReceivedPaymentsNavClass":"active",
            }
    
    else:

        context = {
            "received_payments" : data,
            "total_payment" : total_payment,
            "total_payments_count" : total_payments_count,
            "PaymentsNavclass":"active",
            "ShowPaymentsNavclass":"show",
            "ReceivedPaymentsNavClass":"active",
        }

    return render(request, 'merchant/payments/received-payments.html', context)
    
    #     # bill.payment_date = datetime.strptime(str(bill.payment_date).date, '%Y-%m-%d').strftime('%Y-%m-%d'),

        
    # print('data',data)
    # if request.method == "POST":
    #     user = request.POST.get('user')
    #     from_date = request.POST['from_date']
    #     from_date_temp = from_date
    #     to_date = request.POST['to_date']
    #     to_date_temp = to_date

    #     new_data = []

    #     if received_payments:
    #         if from_date:
    #             from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

    #         if to_date:
    #             to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

    #         for bill in received_payments:
                
    #             if from_date and to_date:
    #                 if bill.payment_date_new >= from_date and bill.payment_date_new <= to_date:
    #                     new_data.append(bill)

    #             elif from_date:
    #                 if bill.payment_date_new >= from_date:
    #                     new_data.append(bill)

    #             elif to_date:
    #                 if bill.payment_date_new <= to_date:
    #                     new_data.append(bill)
        
    #     total_payment = 0.0

    #     for payment in new_data:
    #         total_payment = total_payment + float(payment.amount)

    #     context = {
    #             'from_date': from_date_temp,
    #             'to_date': to_date_temp,
    #             "received_payments" : new_data,
    #             "total_payment" : total_payment,
    #             "total_payments_count" : total_payments_count,
    #             "PaymentsNavclass":"active",
    #             "ShowPaymentsNavclass":"show",
    #             "ReceivedPaymentsNavClass":"active",
    #         }
    
    # else:
    #     total_payment = 0.0

    #     for payment in received_payments:
    #         total_payment = total_payment + float(payment.amount)

    #     context = {
    #         "received_payments" : received_payments,
    #         "total_payment" : total_payment,
    #         "total_payments_count" : total_payments_count,
    #         "PaymentsNavclass":"active",
    #         "ShowPaymentsNavclass":"show",
    #         "ReceivedPaymentsNavClass":"active",
    #     }    

    

    # return render(request, 'merchant/payments/received-payments.html', context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def PaymentHistory(request):

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)

    business_id = business_object.id

    total_transaction_count = 0
    count1 = 0
    count2 = 0
    count3 = 0

    startswith = str(business_id) + ','
    endswith = ','+ str(business_id)
    contains = ','+ str(business_id) + ','
    exact = str(business_id)
            
    payment_history = recharge_history.objects.filter(
        Q(merchant_id = merchant_object),
        Q(business_ids__startswith = startswith) | 
        Q(business_ids__endswith = endswith) | 
        Q(business_ids__contains = contains) | 
        Q(business_ids__exact = exact)
    ).order_by('-id')

    payment_history_new = []

    my_ads_payment = PromotionsPaymentHistory.objects.filter(merchant = merchant_object, merchant_business_id = business_id, payment_done = True).order_by('-id')

    for history in payment_history:
        count1 = count1 + 1
        history.pay_business_name = "Green Bill"
        payment_history_new.append(history)
        print('recharge_history',history.mode)

    merchant_bill = MerchantBill.objects.filter(bill_received_business_name = business_id, payment_done = True).order_by('-id')

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

    for bill in my_ads_payment:
        count3 = count3 + 1
        bill.pay_business_name = "Green Bill"

        bill.subscription_name = "Third Party Ads"

        bill.purchase_date = bill.payment_date

        bill.cost = bill.payment_amount

        bill.transaction_id = bill.transaction_id

        payment_history_new.append(bill)

    # sorted_payment_history = sorted(payment_history_new, key=lambda item: item.get("purchase_date"))
    
    offer_merchant_user_object = Merchant_users.objects.get(user_id = request.user)
    offer_merchant_object = offer_merchant_user_object.merchant_user_id
    merchant_business_id = MerchantProfile.objects.get(m_user = offer_merchant_object, m_active_account = True)
    data = OfferModel.objects.filter(merchant_business_id = merchant_business_id,offer_panel='merchant', status=1).order_by("-id")

    if PromotionsAmount.objects.all():
        amount = PromotionsAmount.objects.latest('id')
        offer_amount = amount.offer_amount
    else:
        offer_amount = 0

    today = date.today()
    total_amount_spent = 0.0

    for offer in data:
        # if offer.valid_through > today:
        count3 = count3 + 1

        offer.pay_business_name = "Offer"

        offer.subscription_name = offer.offer_name

        offer.cost = float(offer_amount) * float(offer.customer_merchant_count)

        total_amount_spent = total_amount_spent + (float(offer_amount) * float(offer.customer_merchant_count))

        offer.purchase_date = offer.created_date

        payment_history_new.append(offer)

    coupon_merchant_id = MerchantProfile.objects.get(m_user = offer_merchant_object, m_active_account = True).id

    coupon_list = CouponModel.objects.filter(merchant_business_id = coupon_merchant_id, coupon_panel = "merchant").order_by('-id')

    print(coupon_list, merchant_business_id)
    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        coupon_amount = data.coupon_amount
    else:
        coupon_amount = 0

    today = date.today()
    for coupon in coupon_list:
        # if coupon.valid_through > today:
        count3 = count3 + 1

        coupon.pay_business_name = "Coupon"

        coupon.subscription_name = coupon.coupon_name

        coupon.cost = float(coupon_amount) * float(coupon.total_customers)

        total_amount_spent = total_amount_spent + (float(coupon_amount) * float(coupon.total_customers))

        coupon.purchase_date = datetime(coupon.valid_from.year, coupon.valid_from.month, coupon.valid_from.day)

        payment_history_new.append(coupon)



    total_transaction_count = count1 + count2 + count3

    sorted_payment_history = sorted(payment_history_new, key=lambda object1: object1.purchase_date.replace(tzinfo=None), reverse=True)


    # total_transaction_count = 0

    for payment in payment_history_new:
        if payment.pay_business_name != "Offer" and payment.pay_business_name != "Coupon":
            if payment.cost:
                total_amount_spent = total_amount_spent + float(payment.cost)
            # total_transaction_count = total_transaction_count + 1
    
    for bill in sorted_payment_history:
        bill.purchase_date_new = datetime.strptime(str(bill.purchase_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d') if bill.purchase_date else ""
    
    if request.method == "POST":
        user = request.POST.get('user')
        from_date = request.POST['from_date']
        from_date_var = from_date
        to_date = request.POST['to_date']
        to_date_var = to_date
        total_transaction_count = 0
        count = 0
        new_data = []

        if sorted_payment_history:
            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

            for bill in sorted_payment_history:
                if from_date and to_date:
                    if bill.purchase_date_new >= from_date and bill.purchase_date_new <= to_date:
                        count = count + 1
                        new_data.append(bill)

                elif from_date:
                    if bill.purchase_date_new >= from_date:
                        new_data.append(bill)

                elif to_date:
                    if bill.purchase_date_new <= to_date:
                        new_data.append(bill)

            total_amount_spent = 0
            total_transaction_count = count
            for payment in new_data:
                if payment.cost:
                    total_amount_spent = total_amount_spent + float(payment.cost)
                    # total_transaction_count = total_transaction_count + 1
               
        context = {
                'from_date': from_date_var,
                'to_date': to_date_var,
                "payment_history" : new_data,
                "total_amount_spent" : total_amount_spent,
                "total_transaction_count" : total_transaction_count,
                "PaymentsNavclass":"active",
                "ShowPaymentsNavclass":"show",
                "PaymentHistoryNavClass":"active",
            }
    else:

        context = {
        "payment_history" : sorted_payment_history,
        "total_amount_spent" : total_amount_spent,
        "total_transaction_count" : total_transaction_count,
        # "offer_data":data,
        "PaymentsNavclass":"active",
        "ShowPaymentsNavclass":"show",
        "PaymentHistoryNavClass":"active",
        }

    return render(request, 'merchant/payments/payment-history.html', context)