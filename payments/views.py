import os
import random
import sweetify
# import datetime
from offers.models import OfferModel
from referral_points.models import *
from coupon.models import *
from bill_design.models import *
from partner_my_subscription.models import *
from promotions.models import *
from my_subscription.models import *
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

from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner, generalSetting

import random
import string

# payu
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
# import datetime
from datetime import datetime, date, timedelta
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils import timezone

# SMS
import requests
import time
import pyshorteners

from super_admin_settings.models import PaymentSetting
from merchant_payment.models import PaymentLinks
from partner_payment.models import PartnerPaymentLinks

from merchant_software_apis.models import DeviceId

from pyfcm import FCMNotification
from django.conf import settings
import socket
from django.db.models import Q

@login_required(login_url="/merchant-login/")
def payments(request):
	context = {
		"PaymentsNavclass": "active"
	}
	return render(request, "merchant/payments.html",context)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def GetPaymentLink(request):

    try:
        payment_settings = PaymentSetting.objects.latest('id')
    except:
        payment_settings = ""

    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        name = request.POST['name']
        email = request.POST['email']
        amount_temp = request.POST['amount']
        description = request.POST['description']
        send_sms = request.POST['send_sms']
        amount = (amount_temp)
        result = OwnerPaymentLinks.objects.create(mobile_no = mobile_no, name = name, email = email, amount = amount, description = description)

        business_object = generalSetting.objects.get(id = 1)

        if result and send_sms:
            letters = string.ascii_letters
            digit = string.digits
            random_string = str(result.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

            OwnerPaymentLinks.objects.filter(id=result.id).update(payment_url = random_string)

            payment_url_temp = "http://157.230.228.250/owner-payment-link/" + str(random_string) + "/"

            s = pyshorteners.Shortener()

            short_url = s.tinyurl.short(payment_url_temp)

            ts = int(time.time())
            # amount_temp = float(result.amount)
            data_temp = {
                "keyword":"Payment Link",
                "timeStamp":ts,
                "dataSet":
                    [
                        {
                            "UNIQUE_ID":"GB-" + str(ts),
                            "MESSAGE":"Hey Green Bill user, " + business_object.business_name + " has shared payment link for " + "Rs. " + str(amount) + ". Click link " + short_url + " to pay now.",
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
            sweetify.success(request, title="Success", icon='success', text='Payment Link created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to create.', timer=1500)

    payment_link_list = OwnerPaymentLinks.objects.filter(promotions = False).order_by('-id')
    # payment_link_list = OwnerPaymentLinks.objects.filter(Q(promotions = False) | ~Q(mobile_no = '')).order_by('-id')

    payment_link_list1 = OwnerPaymentLinks.objects.filter(Q(promotions = False) & ~Q(mobile_no = '')).order_by('-id')


    context = {
        "payment_link_list": payment_link_list,
        "payment_link_list1": payment_link_list1,
        "payment_settings": payment_settings,
        "PaymentsNavclass":"active",
        "ShowPaymentsNavclass":"show",
        "PaymentLinkNavClass":"active",
    }

    return render(request, 'super_admin/payments/create-payment-link.html', context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def SendPaymentLink(request, id):

    link_id = id

    try:
        payment_link = OwnerPaymentLinks.objects.get(id = link_id)
    except:
        payment_link = ""

    try:
    	business_object = generalSetting.objects.get(id = 1)
    except:
    	business_object = ""

    if payment_link and business_object:
        letters = string.ascii_letters
        digit = string.digits
        random_string = str(payment_link.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

        OwnerPaymentLinks.objects.filter(id=payment_link.id).update(payment_url = random_string)

        payment_url_temp = "http://157.230.228.250/owner-payment-link/" + str(random_string) + "/"

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
                            "MESSAGE":"Hey Green Bill user, " + business_object.business_name + " has shared payment link for " + "Rs. " + payment_link.amount + ". Click link " + short_url + " to pay now.",
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
            sweetify.success(request, title="Success", icon='success', text='Payment Link Send Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Send.', timer=1500)
    else:
        sweetify.success(request, title="Oops...", icon='error', text='Fail to Send.', timer=1500)

    return redirect(GetPaymentLink)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def DeletePaymentLink(request, id):
    link_id = id

    instance = OwnerPaymentLinks.objects.get(id=link_id)
    result = instance.delete()

    if result:
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})


def PaymentLink(request, id):
    link_url = id

    try:
        payment_link = OwnerPaymentLinks.objects.get(payment_url=link_url)
    except:
        payment_link = ""

    try:
        payment_settings = PaymentSetting.objects.latest('id')
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
            surl = "http://157.230.228.250/owner-payment-link-success/"
            furl = "http://157.230.228.250/owner-payment-link-fail/"

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

        return render(request, 'super_admin/payments/payment-link.html', context)

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

    payment_link = OwnerPaymentLinks.objects.get(payment_url=link_url)

    try:
        payment_settings = PaymentSetting.objects.latest('id')
    except:
        payment_settings = ""

    SALT = str(payment_settings.payu_salt)

    retHashSeq = SALT +'|'+status+'|||||||'+ udf4 + '|' + udf3 + '|' +  udf2 +'|'+ udf1 + '|' + email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+ key

    hash_string = retHashSeq.encode('utf-8')
    
    hashh = hashlib.sha512(hash_string).hexdigest().lower()

    if status == "success":
        if hashh == posted_hash:
            
            result = OwnerPaymentLinks.objects.filter(id=payment_link.id).update(payment_done = True, payment_date = timezone.now(), transaction_id = txnid, payu_transaction_id = mihpayid)
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

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def ReceivedPayments(request):
    # if request.method == "POST":
    if request.POST.get('submit') == 'Save':
        payment_mode = request.POST['payment_mode']
        payment_amount = request.POST['payment_amount']
        Received_from = request.POST['Received_from']
        transaction_for = request.POST['transaction_for']
        if payment_mode == 'Online':
            payment_through = request.POST['manual_transaction_id']
        if payment_mode == 'Cheque':
            payment_through = request.POST['check_no']
        
        if payment_mode == 'Cash':
            payment_through = ''
        result = OwnerPaymentLinks.objects.create(name = Received_from, description = transaction_for, amount = payment_amount, payment_done = True, payment_mode=payment_mode, check_transaction_id = payment_through, payment_date=timezone.now())

        sweetify.success(request, title="Success", icon='success',text='Payment Added Successfully.', timer=1500)

    all_merchants = MerchantProfile.objects.all()
    all_partner = PartnerProfile.objects.all()
    data_status = OfferModel.objects.filter(offer_panel='merchant', status=1)
    total_offers = OfferModel.objects.filter(offer_panel='merchant', status=1).count()
    coupon_list = CouponModel.objects.filter(coupon_panel='merchant').order_by('-id')
    total_coutpon_count = CouponModel.objects.filter(coupon_panel='merchant').count()
    approved_ads = ads_below_bill.objects.filter(ads_type="third_party", status=1)
    approved_ads_count = ads_below_bill.objects.filter(ads_type="third_party", status=1).count()
    received_payments = OwnerPaymentLinks.objects.filter(payment_done = True).order_by('-id')

    data = []
    total_payment = 0.0
    total_payments_count = (total_offers + total_coutpon_count + approved_ads_count)
    trans_id = '' 
    mode = ''

    if PromotionsAmount.objects.all():
        data3 = PromotionsAmount.objects.latest('id')
        amount = data3.third_party_ads_belowbill_amount
    else:
        amount = 0

    third_party_mode = ''

    for ads in approved_ads: 
        if ads.transaction_id:
            third_party_mode = 'PayU'
        else:
            third_party_mode = 'Cash'
        data.append({
            'payment_date':ads.created_date,
            'name': ads.ads_type,
            'transaction_id':'---',
            'mode':third_party_mode,
            'description': ads.merchant_business_id,
            'amount': float(ads.ads_below_bill_amount),
            })

        total_payment = total_payment + (float(amount) * float(ads.third_party_total_transaction))


    for merchant in all_merchants:
        startswith = str(merchant.id) + ','
        endswith = ','+ str(merchant.id)
        contains = ','+ str(merchant.id) + ','
        exact = str(merchant.id)

        recharge_his = recharge_history.objects.filter(
            Q(merchant_id = merchant.m_user),
            Q(business_ids__startswith = startswith) | 
            Q(business_ids__endswith = endswith) | 
            Q(business_ids__contains = contains) | 
            Q(business_ids__exact = exact)
        ).order_by('-id')

        for recharge in recharge_his:
            if recharge.is_subscription_plan == True:
                subscription_plan = subscription_plan_details.objects.filter(id=recharge.subscription_plan_id)

                if not subscription_plan:
                    final_amount = 0
                for subscription in subscription_plan:
                    try:
                        users_cost = float(recharge.no_of_users) * float(recharge.valid_for_month) * float(subscription.cost_for_users)
                        final_amount = float(users_cost) + float(recharge.cost) + float(recharge.gst_amount)
                    except:
                        final_amount = 0
            else:
                final_amount = recharge.cost


            purchase_date = timezone.localtime(recharge.purchase_date).strftime("%Y-%m-%d")

            data.append({
                'payment_date': recharge.purchase_date,
                'name': merchant,
                'transaction_id':'---',
                'mode':recharge.mode,
                'description': recharge.subscription_name,
                'amount': str(final_amount),
                })
            total_payments_count += 1
            total_payment = total_payment + float(final_amount)

    for partner in all_partner:
        partner_recharge_history_list = partner_recharge_history.objects.filter(partner_id = partner.p_user).order_by("-id")

        for recharge in partner_recharge_history_list:
            purchase_date = timezone.localtime(recharge.purchase_date).strftime("%Y-%m-%d")

            data.append({
                'payment_date': recharge.purchase_date,
                'name': partner,
                'transaction_id':'---',
                'mode': recharge.mode,
                'description': recharge.subscription_name,
                'amount': recharge.cost,
            })

            total_payments_count += 1
            total_payment = total_payment + float(recharge.cost)

    if PromotionsAmount.objects.all():
        data2 = PromotionsAmount.objects.latest('id')
        coupon_amount = data2.coupon_amount
    else:
        coupon_amount = 0

    for coupon in coupon_list:
        obj = MerchantProfile.objects.get(id=coupon.merchant_business_id).m_business_name
        data.append({
            'payment_date':coupon.created_date,
            'name': obj,
            'transaction_id':'---',
            'mode':'Cash',
            'description': coupon.coupon_name,
            'amount': float(coupon_amount) * float(coupon.total_customers),
            })

        total_payment = total_payment + (float(coupon_amount) * float(coupon.total_customers))


    if PromotionsAmount.objects.all():
        data1 = PromotionsAmount.objects.latest('id')
        offer_amount = data1.offer_amount
    else:
        offer_amount = 0

    for offer in data_status:
        data.append({
            'payment_date':offer.created_date,
            'name': offer.merchant_business_name,
            'transaction_id':'---',
            'mode':'Cash',
            'description': offer.offer_name,
            'amount': float(offer_amount) * float(offer.customer_merchant_count),
            })

        total_payment = total_payment + (float(offer_amount) * float(offer.customer_merchant_count))


    for payments in received_payments:
        total_payments_count += 1
        total_payment = total_payment + float(payments.amount)
        if payments.transaction_id:
            trans_id = payments.transaction_id
            mode = 'PayU'
        else:
            trans_id = payments.check_transaction_id
            mode = payments.payment_mode

        data.append({
            'payment_date':payments.payment_date,
            'name':payments.name,
            'transaction_id':trans_id,
            'mode':mode,
            'description':payments.description,
            'amount':payments.amount,
            })
    

    if request.POST.get('submit') == 'search_payments':
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
                if from_date and to_date:
                    payment_date = timezone.localtime(bill['payment_date']).strftime("%Y-%m-%d")
                    if payment_date >= from_date and payment_date <= to_date:
                        new_data.append(bill)
        
        total_payment = 0.0
        total_payments_count = 0
        for payment in new_data:
            total_payment = total_payment + float(payment['amount'])
            total_payments_count = total_payments_count + 1

        new_data.sort(key = lambda x: timezone.localtime(x['payment_date']).strftime("%Y-%m-%d"), reverse = True)

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
        # for payment in received_payments:
            
        # print(received_payments)
        data.sort(key = lambda x: timezone.localtime(x['payment_date']).strftime("%Y-%m-%d"), reverse = True)

        context = {
            "received_payments" : data,
            "total_payment" : total_payment,
            "total_payments_count" : total_payments_count,
            "PaymentsNavclass":"active",
            "ShowPaymentsNavclass":"show",
            "ReceivedPaymentsNavClass":"active",
        }

    return render(request, 'super_admin/payments/received-payments.html', context)
    

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def SendPaymentToMerchantAndPartnerManually(request):
    if request.POST.get('submit') != 'search':
        if request.method == 'POST':
            user = request.POST['user']
            amount = request.POST['amount']
            payment_mode = request.POST['payment_mode']
            description = request.POST['description']
            bank_id = request.POST.get('bank_id')
            cheque_id = request.POST.get('cheque_id')
            merchant_business = request.POST.get('merchant_business')
            if not merchant_business:
                merchant_business = ''
            partner_id = request.POST.get('partner_id')
            if not partner_id:
                partner_id = ''

            print(user)

            result = SendPaymentManually.objects.create(business_id = merchant_business, partner_id = partner_id, bank_transaction_id = bank_id,
                cheque_id = cheque_id, payment_mode = payment_mode, description = description, amount = amount, payment_for = user)

            if user == 'merchant':
                if payment_mode == 'Cash':
                    transaction_id = 'Cash'

                elif payment_mode == 'Bank':
                    transaction_id = 'Bank = ' + bank_id

                elif payment_mode == 'Cheque':
                    transaction_id = 'Cheque = ' + cheque_id

                received_payments = PaymentLinks.objects.create(m_business_id = merchant_business, payment_done = True, amount = amount, 
                    description =description, payment_date = timezone.now(), transaction_id = transaction_id)


                merchant_user = MerchantProfile.objects.get(id = merchant_business)

                device = DeviceId.objects.filter(mobile_no=merchant_user.m_user, user_type = 'merchant').first()
            
                if device:

                    push_service = FCMNotification(api_key=settings.API_KEY)

                    result = ''

                    if device:
                        registration_id = device.device_id
                    else:
                        registration_id = ""

                    message_title = "Received Payments"

                    message_body = "You have received new payment. "

                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)


            else:
                if payment_mode == 'Cash':
                    transaction_id = 'Cash'

                elif payment_mode == 'Bank':
                    transaction_id = 'Bank = ' + bank_id

                elif payment_mode == 'Cheque':
                    transaction_id = 'Cheque = ' + cheque_id

                PartnerPaymentLinks.objects.create(partner_id = partner_id, payment_done = True, amount = amount, description = description,
                    payment_date = timezone.now(), transaction_id = transaction_id)

            if result:
                sweetify.success(request, title="Success", icon='success',text='Payment sent Successfully.', timer=1500)
            else:
                sweetify.success(request, title="Oops...", icon='error', text='Something went Wrong.', timer=1500)


    merchants = MerchantProfile.objects.filter(m_disabled_account = False).order_by('-id')
    partners = PartnerProfile.objects.filter(p_disabled_account = False)
    total_payments_count = 0
    total_payment = 0
    from_date1 = ''
    to_date1 = ''
    if request.POST.get('submit') == 'search':
        DATE_FORMAT = '%Y-%m-%d'
        from_date1 = request.POST['from_date']
        to_date1 = request.POST['to_date']

        date_time_obj = datetime.strptime(to_date1, '%Y-%m-%d')
        day_later = date_time_obj + timedelta(days=1)
        x = day_later.date()
        ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

        start_date1 = datetime.strptime(str(from_date1), '%Y-%m-%d').strftime('%d-%m-%Y')
        start_date = start_date1.split('-')
        start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
        sd_filter = start_date.strftime(DATE_FORMAT)

        payments = SendPaymentManually.objects.filter(created_at__gte = sd_filter, created_at__lte = ed_filter).order_by('-id')
        
        for payment in payments:
            total_payment = float(total_payment) + float(payment.amount)
            total_payments_count = total_payments_count + 1
            if payment.business_id:
                payment.merchant = MerchantProfile.objects.get(id = payment.business_id).m_business_name
            else:
                payment.merchant = ""
    else:
        payments = SendPaymentManually.objects.all().order_by('-id')
        
        for payment in payments:
            if payment.amount != "":
                total_payment = float(total_payment) + float(payment.amount)
            total_payments_count = total_payments_count + 1
            if payment.business_id:
                payment.merchant = MerchantProfile.objects.get(id = payment.business_id).m_business_name
            else:
                payment.merchant = ""

    context = {
        "merchants": merchants,
        "total_payment": total_payment,
        "total_payments_count": total_payments_count,
        "from_date": from_date1,
        "to_date": to_date1,
        "payments": payments,
        "partners": partners,
        "PaymentsNavclass":"active",
        "ShowPaymentsNavclass":"show",
        "PaymentSendNavClass":"active",
    }
    return render(request, 'super_admin/payments/send-payments.html', context)