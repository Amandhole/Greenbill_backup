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
from users.models import GreenBillUser, UserProfileImage, Merchant_users, Partner_users, PartnerProfile
from role.models import *
from dateutil import parser
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_partner, getPartnerActiveTransactionalSubscriptionPlan
from partner_my_subscription.models import *

import random
import string

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
import requests
import time
import pyshorteners
from datetime import datetime
from partner_my_subscription.models import *

from partner_setting.models import PartnerPaymentSetting


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def GetPaymentLink(request):

    partner_id = Partner_users.objects.filter(user_id=request.user).values('partner_user_id')[0]['partner_user_id']

    subscription_object = getPartnerActiveTransactionalSubscriptionPlan(request, partner_id)

    try:
        payment_settings = PartnerPaymentSetting.objects.get(partner_id = partner_id)
    except:
        payment_settings = ""

    try:
    	business_object = PartnerProfile.objects.get(p_user = partner_id)
    except:
    	business_object = ""

    if request.method == "POST":

        if subscription_object:

            if int(subscription_object.total_sms_avilable) >= int(1):

                mobile_no = request.POST['mobile_no']
                name = request.POST['name']
                email = request.POST['email']
                amount = request.POST['amount']
                description = request.POST['description']
                send_sms = request.POST['send_sms']

                result = PartnerPaymentLinks.objects.create(partner_id = partner_id, mobile_no = mobile_no, name = name, email = email, amount = amount, description = description)

                if result and send_sms:
                    letters = string.ascii_letters
                    digit = string.digits
                    random_string = str(result.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                    PartnerPaymentLinks.objects.filter(id=result.id).update(payment_url = random_string)

                    payment_url_temp = "http://157.230.228.250/partner-payment-link/" + str(random_string) + "/"

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
                                    "MESSAGE":"Hey Green Bill user, " + business_object.p_business_name + " has shared payment link for " + "Rs. " + result.amount + ". Click link " + short_url + " to pay now.",
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
                    sweetify.success(request, title="Success", icon='success', text='Payment Link created Successfully.', timer=1500)
                else:
                    sweetify.success(request, title="Oops...", icon='error', text='Fail to create.', timer=1500)

            else:
                sweetify.success(request, title="Oops...", icon='error', text='Insufficient Balance. Please purchase Transactional plan and try again !!!', timer=2000)
        else:
            sweetify.success(request, title="Oops...", icon='error', text="You don't have active Transactional SMS plan. Please purchase and try again.", timer=2000)

    payment_link_list = PartnerPaymentLinks.objects.filter(partner_id = partner_id).order_by('-id')

    context = {
        "payment_link_list": payment_link_list,
        "payment_settings": payment_settings,
        "PaymentsNavclass":"active",
        "ShowPaymentsNavclass":"show",
        "PaymentLinkNavClass":"active",
    }

    return render(request, 'partner/payments/create-payment-link.html', context)

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def SendPaymentLink(request, id):

    partner_id = Partner_users.objects.filter(user_id=request.user).values('partner_user_id')[0]['partner_user_id']

    subscription_object = getPartnerActiveTransactionalSubscriptionPlan(request, partner_id)

    if subscription_object:

        if int(subscription_object.total_sms_avilable) >= int(1):

            link_id = id

            try:
                payment_link = PartnerPaymentLinks.objects.get(id = link_id)
            except:
                payment_link = ""

            try:
            	business_object = PartnerProfile.objects.get(p_user = payment_link.partner_id)
            except:
            	business_object = ""

            if payment_link and business_object:
                letters = string.ascii_letters
                digit = string.digits
                random_string = str(payment_link.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                PartnerPaymentLinks.objects.filter(id=payment_link.id).update(payment_url = random_string)

                payment_url_temp = "http://157.230.228.250/partner-payment-link/" + str(random_string) + "/"

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
                                    "MESSAGE":"Hey Green Bill user, " + business_object.p_business_name + " has shared payment link for " + "Rs. " + payment_link.amount + ". Click link " + short_url + " to pay now.",
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

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def DeletePaymentLink(request, id):
    link_id = id

    instance = PartnerPaymentLinks.objects.get(id=link_id)
    result = instance.delete()

    if result:
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})


def PaymentLink(request, id):
    link_url = id

    try:
        payment_link = PartnerPaymentLinks.objects.get(payment_url=link_url)
    except:
        payment_link = ""

    try:
        payment_settings = PartnerPaymentSetting.objects.get(partner_id = payment_link.partner_id)
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
            surl = "http://157.230.228.250/partner-payment-link-success/"
            furl = "http://157.230.228.250/partner-payment-link-fail/"

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

        return render(request, 'partner/payments/payment-link.html', context)

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

    payment_link = PartnerPaymentLinks.objects.get(payment_url=link_url)

    try:
        payment_settings = PartnerPaymentSetting.objects.get(partner_id = payment_link.partner_id)
    except:
        payment_settings = ""

    SALT = str(payment_settings.payu_salt)

    retHashSeq = SALT +'|'+status+'|||||||'+ udf4 + '|' + udf3 + '|' +  udf2 +'|'+ udf1 + '|' + email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+ key

    hash_string = retHashSeq.encode('utf-8')
    
    hashh = hashlib.sha512(hash_string).hexdigest().lower()

    if status == "success":
        if hashh == posted_hash:
            
            result = PartnerPaymentLinks.objects.filter(id=payment_link.id).update(payment_done = True, payment_date = timezone.now(), transaction_id = txnid, payu_transaction_id = mihpayid)
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

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def ReceivedPayments(request):

    partner_id = Partner_users.objects.filter(user_id=request.user).values('partner_user_id')[0]['partner_user_id']

    mobile_no = GreenBillUser.objects.get(id = partner_id)

    received_payments = PartnerPaymentLinks.objects.filter(partner_id = mobile_no, payment_done = True).order_by('-id')

    total_payments_count = PartnerPaymentLinks.objects.filter(partner_id =mobile_no, payment_done = True).count()

    total_payment = 0.0

    for payment in received_payments:
        total_payment = total_payment + float(payment.amount)

    data = []
    
    for bill in received_payments:

        try:
            bill_file = str(base_url) + str(bill.bill.url)
        except:
            bill_file = ""
        
       
        bill.payment_date_new = datetime.strptime(str(bill.payment_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d')

        
    print('data',data)
    if request.method == "POST":
        user = request.POST.get('user')
        from_date = request.POST['from_date']
        from_date_temp = from_date
        to_date = request.POST['to_date']
        to_date_temp = to_date

        new_data = []

        if received_payments:
            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

            for bill in received_payments:
                
                if from_date and to_date:
                    if bill.payment_date_new >= from_date and bill.payment_date_new <= to_date:
                        new_data.append(bill)

                elif from_date:
                    if bill.payment_date_new >= from_date:
                        new_data.append(bill)

                elif to_date:
                    if bill.payment_date_new <= to_date:
                        new_data.append(bill)
        
        total_payment = 0.0

        total_payments_count = len(new_data)

        for payment in new_data:
            total_payment = total_payment + float(payment.amount)

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
        total_payment = 0.0

        for payment in received_payments:
            total_payment = total_payment + float(payment.amount)

        context = {
            "received_payments" : received_payments,
            "total_payment" : total_payment,
            "total_payments_count" : total_payments_count,
            "PaymentsNavclass":"active",
            "ShowPaymentsNavclass":"show",
            "ReceivedPaymentsNavClass":"active",
        }

    return render(request, 'partner/payments/received-payments.html', context)
                

    context = {
        "received_payments" : received_payments,
        "total_payment" : total_payment,
        "total_payments_count" : total_payments_count,
        "PaymentsNavclass":"active",
        "ShowPaymentsNavclass":"show",
        "ReceivedPaymentsNavClass":"active",
        # 'payment_date': payment_date,
    }

    # context = {
    #     "received_payments" : received_payments,
    #     "total_payment" : total_payment,
    #     "total_payments_count" : total_payments_count,
    #     "PaymentsNavclass":"active",
    #     "ShowPaymentsNavclass":"show",
    #     "ReceivedPaymentsNavClass":"active",
    # }

    return render(request, 'partner/payments/received-payments.html', context)


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def PaymentHistory(request):

    partner_id = Partner_users.objects.filter(user_id=request.user).values('partner_user_id')[0]['partner_user_id']

    payment_history = partner_recharge_history.objects.filter(partner_id = partner_id).order_by('-id')

    partner_promotional_subscription = partner_promotional_sms_subscriptions.objects.filter(partner_id = request.user)

    payemt_data = []
    payment_mode = 'PayU'

    total_amount_spent = 0.0
    total_transaction_count = 0
    
    for bill in payment_history:
        bill.purchase_date_new = datetime.strptime(str(bill.purchase_date.date()), '%Y-%m-%d').strftime('%Y-%m-%d')
    
    if request.method == "POST":
        user = request.POST.get('user')
        from_date = request.POST['from_date']
        from_date_var = from_date
        to_date = request.POST['to_date']
        to_date_var = to_date

        new_data = []

        if payment_history:
            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')



            for bill in payment_history:
                
                if from_date and to_date:
                    if bill.purchase_date_new >= from_date and bill.purchase_date_new <= to_date:
                        new_data.append(bill)
                        total_amount_spent = total_amount_spent + float(bill.cost)
                        total_transaction_count = total_transaction_count + 1

                elif from_date:
                    if bill.purchase_date_new >= from_date:
                        new_data.append(bill)
                        total_amount_spent = total_amount_spent + float(bill.cost)
                        total_transaction_count = total_transaction_count + 1

                elif to_date:
                    if bill.purchase_date_new <= to_date:
                        new_data.append(bill)
                        total_amount_spent = total_amount_spent + float(bill.cost)
                        total_transaction_count = total_transaction_count + 1


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
        for payment in payment_history:
            total_amount_spent = total_amount_spent + float(payment.cost)
            total_transaction_count = total_transaction_count + 1
        context = {
        "payment_history" : payment_history,
        "total_amount_spent" : total_amount_spent,
        "total_transaction_count" : total_transaction_count,
        "PaymentsNavclass":"active",
        "ShowPaymentsNavclass":"show",
        "PaymentHistoryNavClass":"active",
    }

    return render(request, 'partner/payments/payment-history.html', context)