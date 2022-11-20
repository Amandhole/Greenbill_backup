import os
import random
import sweetify
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from subscription_plan.models import *
from users.models import *
from partner_info.models import bulkMailSmsPartnerModel
from .models import *
from app.views import is_partner


# payu
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
import datetime
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from django.contrib.auth import authenticate, login
from cryptography.fernet import Fernet

from datetime import date

from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q

from app.models import generalSetting

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def GetPartnerSubscriptionPlanById(request, id):
    month_validity = request.POST['month_validity']
    subscription = subscription_plan_details.objects.get(id=id)
    # object1 = subscription_plan_details.objects.filter(id=id).update(valid_for_month=month_validity)
    
    key="IUZdcF"
    SALT="7ViVXMy1"

    enc_key = Fernet.generate_key()
    fernet = Fernet(enc_key)
    password = request.session['password']
    encPassword = fernet.encrypt(password.encode())

    merchant_subscriptions_key = partner_subscriptions_keys.objects.create(key = enc_key.decode("utf-8"))

    firstname = str(request.user.first_name)

    if request.user.email != "":
        email = str(request.user.email)
    else:
        email = "support@greenbill.in"

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

    hash_object = hashlib.sha256(b'randint(0,20)' + bytes(subscription.id) + bytes(request.user.id) + bytes(random_str))

    txnid=hash_object.hexdigest()[0:20]

    hashh = ''
    posted['txnid']=txnid
    posted['key']=key
    productinfo = str("subscription_name-"+ subscription.subscription_name)

    subamount = float(subscription.recharge_amount) * float(month_validity)

    gst_amount = float(subamount)*0.18

    amount = float(subamount) + float(gst_amount)

    amount = str(amount)

    udf1 = str(subscription.id) # subscription id
    
    udf2 = str(request.user.id) # user object

    udf3 = str(encPassword.decode("utf-8")) # encoded Password

    udf4 = str(merchant_subscriptions_key.id) # decode key id

    udf5 = str(month_validity) # Business Ids

    udf6 = ""

    hashSequence = key + "|" + txnid + "|" + amount + "|" + productinfo + "|" + firstname + "|" + email + "|" + udf1 + "|" + udf2 + "|" + udf3 + "|" + udf4 + "|" + udf5 + "|" + udf6 + "|||||" + SALT

    hash_string = hashSequence.encode('utf-8')

    hashh = hashlib.sha512(hash_string).hexdigest().lower()

    context = {
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
        # "month_validity":month_validity,
    }

    return JsonResponse(context)

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def recharge_subscriptions(request):

    all_subscriptions_plans = subscription_plan_details.objects.all().filter(is_active=True).order_by('-id')

    partner_id = Partner_users.objects.filter(user_id=request.user).values('partner_user_id')[0]['partner_user_id']

    promotional_sms_plans = promotional_subscription_plan_model.objects.all().filter(is_active=True).order_by('-id')

    transactional_sms_plans = transactional_subscription_plan_model.objects.all().filter(is_active=True).order_by('-id')

    addons_plans = add_on_plan_model.objects.all().filter(is_active=True).order_by('-id')


    partner_user_id = PartnerProfile.objects.get(p_user = partner_id)

    partner_state = partner_user_id.p_state

    if partner_state == "Maharashtra" or partner_state == "maharashtra":
        sgst = 9
        cgst = 9
        igst = 1

    else:
        igst = 18
        sgst = 1
        cgst = 1

    subscriptions_list = []

    partner_object = GreenBillUser.objects.get(id = partner_id) 

    try:
        active_subscription_object = partner_subscriptions.objects.get(partner_id = partner_object, is_active = True)
    except:
        active_subscription_object = ""

    for subscription in all_subscriptions_plans:
        subscription.total_cost_without_gst = subscription.recharge_amount

        if subscription.user_type == "all" or subscription.user_type == "partner":
            subscriptions_list.append(subscription)
    # Test
    # key="A4MQHd"
    # SALT = "HLysMjoK"
    # PAYU_BASE_URL = "https://test.payu.in/_payment"

    # Production
    key="IUZdcF"
    SALT="7ViVXMy1"
    PAYU_BASE_URL = "https://secure.payu.in/_payment"

    action = ''

    firstname = str(request.user.first_name)

    if request.user.email != "":
        email = str(request.user.email)
    else:
        email = "support@greenbill.in"

    phone = str(request.user.mobile_no)

    surl = "http://157.230.228.250/partner-subscription-purchased-success/"

    furl = "http://157.230.228.250/partner-subscription-purchased-fail/"

    promotional_sms_surl = "http://157.230.228.250/partner-promotional-sms-subscription-purchased-success/"

    promotional_sms_furl = "http://157.230.228.250/partner-promotional-sms-subscription-purchased-fail/"

    transactional_sms_surl = "http://157.230.228.250/partner-transactional-sms-subscription-purchased-success/"

    transactional_sms_furl = "http://157.230.228.250/partner--transactional-sms-subscription-purchased-fail/"

    add_on_surl = "http://157.230.228.250/partner-add-on-subscription-purchased-success/"

    add_on_furl = "http://157.230.228.250/partner-add-on-subscription-purchased-fail/"

    # Password Encryption Start
    enc_key = Fernet.generate_key()
    fernet = Fernet(enc_key)
    password = request.session['password']
    encPassword = fernet.encrypt(password.encode())

    partner_subscriptions_key = partner_subscriptions_keys.objects.create(key = enc_key.decode("utf-8"))

    # for subscription in subscriptions_list:
    #     recharge_amount = float(subscription.recharge_amount)

    #     gst_amount = (float(recharge_amount))*0.18

    #     total_amount = float(gst_amount) + float(recharge_amount)


    #     udf1 = ""
    #     udf2 = ""
    #     udf3 = ""
    #     udf4 = ""
    #     udf5 = ""
    #     udf6 = ""

    #     posted={}



    #     for i in request.POST:
    #         posted[i]=request.POST[i]

    #     random_str =  random.randint(9999999, 99999999)

    #     hash_object = hashlib.sha256(b'randint(0,20)' + bytes(subscription.id) + bytes(request.user.id) + bytes(random_str))

    #     txnid=hash_object.hexdigest()[0:20]

    #     hashh = ''
    #     posted['txnid']=txnid
    #     posted['key']=key
    #     productinfo = str("subscription_name-"+ subscription.subscription_name)
    #     amount = str(total_amount)

    #     udf1 = str(subscription.id) # subscription id

    #     udf2 = str(request.user.id) # user object

    #     udf3 = str(encPassword.decode("utf-8")) # encoded Password

    #     udf4 = str(partner_subscriptions_key.id) # decode key id

    #     udf5 = ""

    #     udf6 = ""

    #     hashSequence = key + "|" + txnid + "|" + amount + "|" + productinfo + "|" + firstname + "|" + email + "|" + udf1 + "|" + udf2 + "|" + udf3 + "|" + udf4 + "|" + udf5 + "|" + udf6 + "|||||" + SALT

    #     hash_string = hashSequence.encode('utf-8')

    #     hashh = hashlib.sha512(hash_string).hexdigest().lower()

    #     subscription.hashh = hashh
    #     subscription.posted = posted
    #     subscription.txnid = txnid
    #     subscription.hash_string = hash_string
    #     subscription.amount = amount
    #     subscription.productinfo = productinfo
    #     subscription.udf1 = udf1
    #     subscription.udf2 = udf2
    #     subscription.udf3 = udf3
    #     subscription.udf4 = udf4
    #     subscription.udf5 = udf5
    #     subscription.udf6 = udf6

    for subscription in promotional_sms_plans:
        subscription.gst_amount = subscription.gst_amount
        subscription.state_wise_gst = float(subscription.gst_amount)/2

        subscription.total_cost_without_gst = float(subscription.total_sms_cost) - float(subscription.gst_amount)
        
        total_cost = subscription.total_sms_cost

        


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

        hash_object = hashlib.sha256(b'randint(0,20)' + bytes(subscription.id) + bytes(request.user.id) + bytes(random_str))

        txnid=hash_object.hexdigest()[0:20]

        hashh = ''
        posted['txnid']=txnid
        posted['key']=key
        productinfo = str("subscription_name-"+ subscription.subscription_name)
        amount = str(subscription.total_sms_cost)

        udf1 = str(subscription.id) # subscription id

        udf2 = str(request.user.id) # user object

        udf3 = str(encPassword.decode("utf-8")) # encoded Password

        udf4 = str(partner_subscriptions_key.id) # decode key id

        udf5 = ""

        udf6 = ""

        hashSequence = key + "|" + txnid + "|" + amount + "|" + productinfo + "|" + firstname + "|" + email + "|" + udf1 + "|" + udf2 + "|" + udf3 + "|" + udf4 + "|" + udf5 + "|" + udf6 + "|||||" + SALT

        hash_string = hashSequence.encode('utf-8')

        hashh = hashlib.sha512(hash_string).hexdigest().lower()

        subscription.hashh = hashh
        subscription.posted = posted
        subscription.txnid = txnid
        subscription.hash_string = hash_string
        subscription.amount = amount
        subscription.productinfo = productinfo
        subscription.udf1 = udf1
        subscription.udf2 = udf2
        subscription.udf3 = udf3
        subscription.udf4 = udf4
        subscription.udf5 = udf5
        subscription.udf6 = udf6

    for subscription in transactional_sms_plans:

        subscription.gst_amount = subscription.gst_amount
        subscription.state_wise_gst = float(subscription.gst_amount)/2
        total_cost = subscription.total_sms_cost

        subscription.total_cost_without_gst = float(subscription.total_sms_cost) - float(subscription.gst_amount)



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

        hash_object = hashlib.sha256(b'randint(0,20)' + bytes(subscription.id) + bytes(request.user.id) + bytes(random_str))

        txnid=hash_object.hexdigest()[0:20]

        hashh = ''
        posted['txnid']=txnid
        posted['key']=key
        productinfo = str("subscription_name-"+ subscription.subscription_name)
        amount = str(subscription.total_sms_cost)

        udf1 = str(subscription.id) # subscription id

        udf2 = str(request.user.id) # user object

        udf3 = str(encPassword.decode("utf-8")) # encoded Password

        udf4 = str(partner_subscriptions_key.id) # decode key id

        udf5 = ""

        udf6 = ""

        hashSequence = key + "|" + txnid + "|" + amount + "|" + productinfo + "|" + firstname + "|" + email + "|" + udf1 + "|" + udf2 + "|" + udf3 + "|" + udf4 + "|" + udf5 + "|" + udf6 + "|||||" + SALT

        hash_string = hashSequence.encode('utf-8')

        hashh = hashlib.sha512(hash_string).hexdigest().lower()

        subscription.hashh = hashh
        subscription.posted = posted
        subscription.txnid = txnid
        subscription.hash_string = hash_string
        subscription.amount = amount
        subscription.productinfo = productinfo
        subscription.udf1 = udf1
        subscription.udf2 = udf2
        subscription.udf3 = udf3
        subscription.udf4 = udf4
        subscription.udf5 = udf5
        subscription.udf6 = udf6


        # for subscription in addons_plans:
        #     gst_amount = subscription.gst_amount
        #     subscription.state_wise_gst = float(gst_amount)/2
        #     total_amount = subscription.recharge_amount

        #     subscription.total_cost_without_gst = float(total_amount) - float(gst_amount) 

            
        #     udf1 = ""
        #     udf2 = ""
        #     udf3 = ""
        #     udf4 = ""
        #     udf5 = ""
        #     udf6 = ""

        #     posted={}

        #     for i in request.POST:
        #         posted[i]=request.POST[i]

        #     random_str =  random.randint(9999999, 99999999)

        #     hash_object = hashlib.sha256(b'randint(0,20)' + bytes(subscription.id) + bytes(request.user.id) + bytes(random_str))

        #     txnid=hash_object.hexdigest()[0:20]

        #     hashh = ''
        #     posted['txnid']=txnid
        #     posted['key']=key
        #     productinfo = str("subscription_name-"+ subscription.add_on_name)
        #     amount = str(subscription.recharge_amount)

        #     udf1 = str(subscription.id) # subscription id

        #     udf2 = str(request.user.id) # user object

        #     udf3 = str(encPassword.decode("utf-8")) # encoded Password

        #     udf4 = str(partner_subscriptions_key.id) # decode key id

        #     udf5 = "" # Business Id

        #     udf6 = ""

        #     hashSequence = key + "|" + txnid + "|" + amount + "|" + productinfo + "|" + firstname + "|" + email + "|" + udf1 + "|" + udf2 + "|" + udf3 + "|" + udf4 + "|" + udf5 + "|" + udf6 + "|||||" + SALT

        #     hash_string = hashSequence.encode('utf-8')

        #     hashh = hashlib.sha512(hash_string).hexdigest().lower()

        #     subscription.hashh = hashh
        #     subscription.posted = posted
        #     subscription.txnid = txnid
        #     subscription.hash_string = hash_string
        #     subscription.amount = amount
        #     subscription.productinfo = productinfo
        #     subscription.udf1 = udf1
        #     subscription.udf2 = udf2
        #     subscription.udf3 = udf3
        #     subscription.udf4 = udf4
        #     subscription.udf5 = udf5
        #     subscription.udf6 = udf6
        
    action = PAYU_BASE_URL

    context = {
        "sgst_value" : sgst,
        "cgst_value" : cgst,
        "igst_value" : igst,
        "partner_user_id": partner_user_id,
        "subscriptions_list" : subscriptions_list,
        "promotional_sms_plans_list" : promotional_sms_plans,
        "transactional_sms_plans_list":transactional_sms_plans,
        # "addons_plans": addons_plans,
        "MERCHANT_KEY":key,
        "firstname" : firstname,
        "email" : email,
        "phone": phone,
        "surl": surl,
        "furl" : furl,
        "promotional_sms_surl": promotional_sms_surl,
        "promotional_sms_furl": promotional_sms_furl,
        "transactional_sms_surl": transactional_sms_surl,
        "transactional_sms_furl": transactional_sms_furl,
        "add_on_surl":add_on_surl,
        "add_on_furl":add_on_furl,
        "action": action,
        "active_subscription_object":active_subscription_object,
        "SettingNavclass": 'active',
        "settingsCollapseShow": "show",
        "MySubscriptionNavclass": 'active'
    }
        
    return render(request, "partner/subscription/subscription-recharge.html", context)

@csrf_exempt
def subscription_purchased_success(request):
    
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount= request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    udf1 = request.POST["udf1"] # subscription id
    subscription_id = request.POST["udf1"]
    udf2 = request.POST["udf2"] # user id
    user_id = request.POST["udf2"] # user id
    udf3 = request.POST["udf3"] # encoded password
    udf4 = request.POST["udf4"] # decode key id
    udf5 = request.POST["udf5"] # plan type
    udf6 = request.POST["udf6"]

    mihpayid = request.POST["mihpayid"]

    # Decode Password
    partner_subscriptions_key = partner_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(partner_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()


    # SALT = "HLysMjoK" # Test Salt
    SALT="7ViVXMy1" # Production Salt

    partner_id = Partner_users.objects.filter(user_id=user_id).values('partner_user_id')[0]['partner_user_id']

    partner_object = GreenBillUser.objects.get(id=partner_id)

    retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

    hash_string = retHashSeq.encode('utf-8')
    
    hashh = hashlib.sha512(hash_string).hexdigest().lower()

    mobile_no = partner_object.mobile_no
    
    request.session['mobile_no'] = mobile_no
    request.session['password'] = decPassword

    user = authenticate(mobile_no=request.session['mobile_no'], password=request.session['password'])
    login(request, user)

    if status == "success":

        if hashh == posted_hash:

            subscription_object = subscription_plan_details.objects.get(id=subscription_id)

            valid_for_month = udf5
            per_bill_cost = subscription_object.per_bill_cost
            per_digital_bill_cost = subscription_object.per_digital_bill_cost
            total_amount = float(subscription_object.recharge_amount)
            subscription_plan_cost = float(subscription_object.subscription_plan_cost)
            per_url_cost = float(subscription_object.per_url_cost)

            print("************wwwww*")
            print(per_url_cost)

            today = date.today()
            d1 = today.strftime("%d-%m-%Y")
            start_date = datetime.datetime.strptime(d1, "%d-%m-%Y")
            delta_period = int(subscription_object.valid_for_month)
            end_date = start_date + relativedelta(months=delta_period)
            expiry_date = end_date.strftime("%d-%m-%Y")

            try:
                check_subscription_available = partner_subscriptions.objects.get(partner_id = partner_object, is_active = True)
            except:
                check_subscription_available = ""

            if check_subscription_available:

                partner_subscriptions.objects.update(partner_id = partner_object, is_active = False)

            subscription_active_status = True

            subscription =  partner_subscriptions.objects.create(
                
                subscription_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                partner_id = partner_object, 

                valid_for_month = valid_for_month,
                per_url_cost = per_url_cost,
                per_bill_cost = per_bill_cost,

                per_digital_bill_cost = per_digital_bill_cost,
                total_amount_avilable = subscription_object.recharge_amount,
                is_active = subscription_active_status,

                purchase_cost = amount,
                expiry_date = expiry_date,

                transaction_id = txnid,
                payu_transaction_id = mihpayid,

            )
            print(subscription)
            try:
                last_id = partner_recharge_history.objects.filter().last()
                invoice_no = 'GB' + str(last_id.id+1)
            except:
                invoice_no = 'GB' + str(1)
            partner_recharge_history.objects.create(

                subscription_plan_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name, 
                partner_id = partner_object,

                valid_for_month = valid_for_month,

                per_bill_cost = per_bill_cost,

                per_digital_bill_cost = per_digital_bill_cost,

                per_url_cost = per_url_cost,

                cost = subscription_plan_cost,

                is_subscription_plan = True,
                expiry_date = expiry_date,

                transaction_id = txnid,
                payu_transaction_id = mihpayid,
                invoice_no = invoice_no
            )

            if subscription:
                sweetify.success(request, title="Success", icon='success', text='Subscription purchased Successfully.', timer=1500)
                return redirect(recharge_subscriptions)
            else:
                sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)
                return redirect(recharge_subscriptions)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)
            return redirect(recharge_subscriptions)
    else:
        sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)
        return redirect(recharge_subscriptions)

@csrf_exempt
def subscription_purchased_fail(request):
    user_id = request.POST["udf2"] # user id
    udf3 = request.POST["udf3"] # encoded password
    udf4 = request.POST["udf4"] # decode key id

    # Decode Password
    partner_subscriptions_key = partner_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(partner_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()

    user_object =  GreenBillUser.objects.get(id=user_id)

    mobile_no = user_object.mobile_no
    
    request.session['mobile_no'] = mobile_no
    request.session['password'] = decPassword

    user = authenticate(mobile_no=request.session['mobile_no'], password=request.session['password'])
    login(request, user)

    sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

    return redirect(recharge_subscriptions)


@csrf_exempt
def promotional_sms_subscription_purchased_success(request):
    
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount= request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    udf1 = request.POST["udf1"] # subscription id
    subscription_id = request.POST["udf1"]
    udf2 = request.POST["udf2"] # user id
    user_id = request.POST["udf2"] # user id
    udf3 = request.POST["udf3"] # encoded password
    udf4 = request.POST["udf4"] # decode key id
    udf5 = request.POST["udf5"] # plan type
    udf6 = request.POST["udf6"]
    mihpayid = request.POST["mihpayid"]

    # Decode Password
    partner_subscriptions_key = partner_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(partner_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()


    # SALT = "HLysMjoK" # Test Salt
    SALT="7ViVXMy1" # Production Salt

    partner_id = Partner_users.objects.filter(user_id=user_id).values('partner_user_id')[0]['partner_user_id']

    partner_object = GreenBillUser.objects.get(id=partner_id)

    retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

    hash_string = retHashSeq.encode('utf-8')
    
    hashh = hashlib.sha512(hash_string).hexdigest().lower()

    mobile_no = partner_object.mobile_no
    
    request.session['mobile_no'] = mobile_no
    request.session['password'] = decPassword

    user = authenticate(mobile_no=request.session['mobile_no'], password=request.session['password'])
    login(request, user)

    if status == "success":

        if hashh == posted_hash:

            subscription_object = promotional_subscription_plan_model.objects.get(id=subscription_id)

            total_sms = subscription_object.total_sms
            per_sms_cost = subscription_object.per_sms_cost
            total_sms_cost = float(subscription_object.total_sms_cost)
            subscription_plan_cost = float(subscription_object.total_sms_cost)
            total_sms_avilable = total_sms

            try:
                check_subscription_available = partner_promotional_sms_subscriptions.objects.get(partner_id = partner_object, is_active = True)
            except:
                check_subscription_available = ""

            if check_subscription_available:

                partner_promotional_sms_subscriptions.objects.update(partner_id = partner_object, is_active = False)

            subscription_active_status = True

            subscription =  partner_promotional_sms_subscriptions.objects.create(

                subscription_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                partner_id = partner_object, 

                total_sms = total_sms,
                per_sms_cost = per_sms_cost,

                total_sms_avilable = total_sms_avilable,

                is_active = subscription_active_status,
                purchase_cost = subscription_plan_cost,

                transaction_id = txnid,
                payu_transaction_id = mihpayid,
            )
            try:
                last_id = partner_recharge_history.objects.filter().last()
                invoice_no = 'GB' + str(last_id.id+1)
            except:
                invoice_no = 'GB' + str(1)
            partner_recharge_history.objects.create(

                subscription_plan_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name, 
                partner_id = partner_object,

                total_sms = total_sms,
                per_sms_cost = per_sms_cost,

                cost = subscription_plan_cost,

                is_promotional_sms_plan = True,

                transaction_id = txnid,
                payu_transaction_id = mihpayid,
                invoice_no =invoice_no,
            )

            if subscription:
                sweetify.success(request, title="Success", icon='success', text='Subscription purchased Successfully.', timer=1500)
                return redirect(recharge_subscriptions)
            else:
                sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)
                return redirect(recharge_subscriptions)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)
            return redirect(recharge_subscriptions)
    else:
        sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)
        return redirect(recharge_subscriptions)


@csrf_exempt
def promotional_sms_subscription_purchased_fail(request):
    user_id = request.POST["udf2"] # user id
    udf3 = request.POST["udf3"] # encoded password
    udf4 = request.POST["udf4"] # decode key id

    # Decode Password
    partner_subscriptions_key = partner_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(partner_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()

    user_object =  GreenBillUser.objects.get(id=user_id)

    mobile_no = user_object.mobile_no
    
    request.session['mobile_no'] = mobile_no
    request.session['password'] = decPassword

    user = authenticate(mobile_no=request.session['mobile_no'], password=request.session['password'])
    login(request, user)

    sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

    return redirect(recharge_subscriptions)


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def my_subscription(request):

    partner_id = Partner_users.objects.filter(user_id=request.user).values('partner_user_id')[0]['partner_user_id']

    partner_object = GreenBillUser.objects.get(id=partner_id)

    subscription_object = ""

    try:
        subscription_object = partner_subscriptions.objects.get(partner_id = partner_object, is_active = True)

        per_bill_cost = subscription_object.per_bill_cost
        per_receipt_cost = subscription_object.per_receipt_cost
        per_cash_memo_cost = subscription_object.per_cash_memo_cost

        per_url_cost = subscription_object.per_url_cost
        per_digital_bill_cost = subscription_object.per_digital_bill_cost
        per_digital_receipt_cost = subscription_object.per_digital_receipt_cost
        per_digital_cash_memo_cost = subscription_object.per_digital_cash_memo_cost

        subscription_name = subscription_object.subscription_name
        recharge_amount = subscription_object.recharge_amount

        purchase_date = subscription_object.purchase_date
        purchase_cost = subscription_object.purchase_cost
        total_amount_avilable = subscription_object.total_amount_avilable

        expiry_date = subscription_object.expiry_date
        
    except:
        per_bill_cost = ""
        per_receipt_cost = ""
        per_cash_memo_cost = ""
        per_url_cost = ""

        per_digital_bill_cost = ""
        per_digital_receipt_cost = ""
        per_digital_cash_memo_cost = ""

        subscription_name = ""
        recharge_amount = ""
        purchase_date = ""
        purchase_cost = ""
        total_amount_avilable = ""

        expiry_date = ""

    try:
        subscription_object = partner_promotional_sms_subscriptions.objects.get(partner_id = partner_object, is_active = True)

        promotional_sms_subscription_name = subscription_object.subscription_name
        promotional_sms_purchase_date = subscription_object.purchase_date
        promotional_sms_purchase_cost = subscription_object.purchase_cost
        promotional_sms_total_sms = int(subscription_object.total_sms)
        promotional_sms_per_sms_cost = subscription_object.per_sms_cost
        promotional_sms_total_sms_avilable = int(subscription_object.total_sms_avilable)
        
    except:

        promotional_sms_subscription_name = ""
        promotional_sms_purchase_date = ""
        promotional_sms_purchase_cost = ""
        promotional_sms_total_sms = ""
        promotional_sms_per_sms_cost = ""
        promotional_sms_total_sms_avilable = ""

    try:
        subscription_object = partner_transactional_sms_subscriptions.objects.get(partner_id = partner_object, is_active = True)

        transactional_sms_subscription_name = subscription_object.subscription_name
        transactional_sms_purchase_date = subscription_object.purchase_date
        transactional_sms_purchase_cost = subscription_object.purchase_cost
        transactional_sms_total_sms = int(subscription_object.total_sms)
        transactional_sms_per_sms_cost = subscription_object.per_sms_cost
        transactional_sms_total_sms_avilable = int(subscription_object.total_sms_avilable)
        
    except:
        transactional_sms_subscription_name = ""
        transactional_sms_purchase_date = ""
        transactional_sms_purchase_cost = ""
        transactional_sms_total_sms = ""
        transactional_sms_per_sms_cost = ""
        transactional_sms_total_sms_avilable = ""


    transactional_smsplan = bulkMailSmsPartnerModel.objects.filter(owner_id=partner_object,transactional="transactional",o_sent_sms=True).order_by('-id')
    promotional_smsplan = bulkMailSmsPartnerModel.objects.filter(owner_id=partner_object,transactional="promotional",o_sent_sms=True).order_by('-id')

    context = {
        "purchase_cost" : purchase_cost,
        "subscription_object": subscription_object,

        "per_bill_cost" : per_bill_cost,
        "per_receipt_cost" : per_receipt_cost,
        "per_cash_memo_cost" : per_cash_memo_cost,
        "per_url_cost":per_url_cost,
        "per_digital_bill_cost" : per_digital_bill_cost,
        "per_digital_receipt_cost" : per_digital_receipt_cost,
        "per_digital_cash_memo_cost" : per_digital_cash_memo_cost,
        "recharge_amount":recharge_amount,

        "subscription_name" : subscription_name,
        "purchase_date" : purchase_date,
        "total_amount_avilable" : total_amount_avilable,

        "expiry_date": expiry_date,

        "transactional_smsplan":transactional_smsplan,
        "promotional_smsplan":promotional_smsplan,

        "promotional_sms_subscription_name" : promotional_sms_subscription_name,
        "promotional_sms_purchase_date" : promotional_sms_purchase_date,
        "promotional_sms_purchase_cost" : promotional_sms_purchase_cost,
        "promotional_sms_total_sms" : promotional_sms_total_sms,
        "promotional_sms_per_sms_cost" : promotional_sms_per_sms_cost,
        "promotional_sms_total_sms_avilable" : promotional_sms_total_sms_avilable,

        "transactional_sms_subscription_name" : transactional_sms_subscription_name,
        "transactional_sms_purchase_date" : transactional_sms_purchase_date,
        "transactional_sms_purchase_cost" : transactional_sms_purchase_cost,
        "transactional_sms_total_sms" : transactional_sms_total_sms,
        "transactional_sms_per_sms_cost" : transactional_sms_per_sms_cost,
        "transactional_sms_total_sms_avilable" : transactional_sms_total_sms_avilable,

        "SettingNavclass": 'active',
        "settingsCollapseShow": "show",
        "MySubscriptionNavclass": 'active'
    }

    return render(request, "partner/subscription/my-subscription.html", context)


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def my_subscription_history(request):

    partner_id = Partner_users.objects.filter(user_id=request.user).values('partner_user_id')[0]['partner_user_id']

    partner_object = GreenBillUser.objects.get(id=partner_id)

    recharge_his = partner_recharge_history.objects.filter(partner_id = partner_object).order_by("-id")

    for recharge in recharge_his:

        if recharge.mode ==  "cashwithoutbill":
            
            total = recharge.cost 
            end_value = round(total)
            recharge.end_value = end_value
        else:

            igst = (recharge.cost) * 0.18
            total = recharge.cost + igst
            end_value = round(total)

            recharge.end_value = end_value
        print("_______________________________")
        print(end_value)
    
    context = {
        "recharge_history" : recharge_his,
        "SettingNavclass": 'active',
        "settingsCollapseShow": "show",
        "MySubscriptionNavclass": 'active'
    }
   

    return render(request, "partner/subscription/my-recharge-history.html", context)



@csrf_exempt
def transactional_sms_subscription_purchased_success(request):
    
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount= request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    udf1 = request.POST["udf1"] # subscription id
    subscription_id = request.POST["udf1"]
    udf2 = request.POST["udf2"] # user id
    user_id = request.POST["udf2"] # user id
    udf3 = request.POST["udf3"] # encoded password
    udf4 = request.POST["udf4"] # decode key id
    udf5 = request.POST["udf5"] # Business Ids
    udf6 = request.POST["udf6"]
    business_ids = udf5
    mihpayid = request.POST["mihpayid"]

    # Decode Password
    merchant_subscriptions_key = partner_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(merchant_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()


    # SALT = "HLysMjoK" # Test Salt
    SALT="7ViVXMy1" # Production Salt

    partner_id = Partner_users.objects.filter(user_id=user_id).values('partner_user_id')[0]['partner_user_id']

    partner_object = GreenBillUser.objects.get(id=partner_id)

    user_object =  GreenBillUser.objects.get(id=user_id)

    retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

    hash_string = retHashSeq.encode('utf-8')
    
    hashh = hashlib.sha512(hash_string).hexdigest().lower()

    mobile_no = user_object.mobile_no
    
    request.session['mobile_no'] = mobile_no
    request.session['password'] = decPassword

    user = authenticate(mobile_no=request.session['mobile_no'], password=request.session['password'])
    login(request, user)

    if status == "success":

        if hashh == posted_hash:

            subscription_object = transactional_subscription_plan_model.objects.get(id=subscription_id)

            total_sms = subscription_object.total_sms
            per_sms_cost = subscription_object.per_sms_cost
            total_sms_cost = float(subscription_object.total_sms_cost)
            subscription_plan_cost = float(subscription_object.total_sms_cost)
            total_sms_avilable = total_sms

            try:
                check_subscription_available = partner_transactional_sms_subscriptions.objects.get(partner_id = partner_object, is_active = True)
            except:
                check_subscription_available = ""

            if check_subscription_available:

                partner_transactional_sms_subscriptions.objects.update(partner_id = partner_object, is_active = False)

            subscription_active_status = True

            subscription =  partner_transactional_sms_subscriptions.objects.create(
                subscription_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                partner_id = partner_object, 

                total_sms = total_sms,
                per_sms_cost = per_sms_cost,

                total_sms_avilable = total_sms_avilable,

                is_active = subscription_active_status,
                purchase_cost = subscription_plan_cost,

                transaction_id = txnid,
                payu_transaction_id = mihpayid,
            )
            try:
                last_id = partner_recharge_history.objects.filter().last()
                invoice_no = 'GB' + str(last_id.id+1)
            except:
                invoice_no = 'GB' + str(1)
            partner_recharge_history.objects.create(
                subscription_plan_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name, 
                partner_id = partner_object,

                total_sms = total_sms,
                per_sms_cost = per_sms_cost,

                cost = subscription_plan_cost,

                is_transactional_sms_plan = True,

                transaction_id = txnid,
                payu_transaction_id = mihpayid,
                invoice_no = invoice_no,

            )

            if subscription:
                sweetify.success(request, title="Success", icon='success', text='Subscription purchased Successfully.', timer=1500)
                return redirect(recharge_subscriptions)

        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

            return redirect(recharge_subscriptions)
    else:

        sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

@csrf_exempt
def transactional_sms_subscription_purchased_fail(request):
    user_id = request.POST["udf2"] # user id
    udf3 = request.POST["udf3"] # encoded password
    udf4 = request.POST["udf4"] # decode key id

    # Decode Password
    partner_subscriptions_key = partner_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(partner_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()

    user_object =  GreenBillUser.objects.get(id=user_id)

    mobile_no = user_object.mobile_no
    
    request.session['mobile_no'] = mobile_no
    request.session['password'] = decPassword

    user = authenticate(mobile_no=request.session['mobile_no'], password=request.session['password'])
    login(request, user)

    sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

    return redirect(recharge_subscriptions)


# Add On's Purchase
@csrf_exempt
def add_on_subscription_purchased_success(request):
    
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount= request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    udf1 = request.POST["udf1"] # subscription id
    subscription_id = request.POST["udf1"]
    udf2 = request.POST["udf2"] # user id
    user_id = request.POST["udf2"] # user id
    udf3 = request.POST["udf3"] # encoded password
    udf4 = request.POST["udf4"] # decode key id
    udf5 = request.POST["udf5"]
    udf6 = request.POST["udf6"]

    mihpayid = request.POST["mihpayid"]

    # Decode Password
    partner_subscriptions_key = partner_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(partner_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()


    # SALT = "HLysMjoK" # Test Salt
    SALT="7ViVXMy1" # Production Salt

    partner_id = Partner_users.objects.filter(user_id=user_id).values('partner_user_id')[0]['partner_user_id']

    partner_object = GreenBillUser.objects.get(id=partner_id)

    retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

    hash_string = retHashSeq.encode('utf-8')
    
    hashh = hashlib.sha512(hash_string).hexdigest().lower()

    mobile_no = partner_object.mobile_no
    
    request.session['mobile_no'] = mobile_no
    request.session['password'] = decPassword

    user = authenticate(mobile_no=request.session['mobile_no'], password=request.session['password'])
    login(request, user)

    if status == "success":

        if hashh == posted_hash:

            subscription_object = add_on_plan_model.objects.get(id=subscription_id)

            per_bill_cost = subscription_object.per_bill_cost
            per_receipt_cost = subscription_object.per_receipt_cost
            per_cash_memo_cost = subscription_object.per_cash_memo_cost
            per_digital_bill_cost = subscription_object.per_digital_bill_cost
            per_digital_receipt_cost = subscription_object.per_digital_receipt_cost
            per_digital_cash_memo_cost = subscription_object.per_digital_cash_memo_cost

            try:
                check_subscription_available = partner_subscriptions.objects.get(partner_id = partner_object, is_active = True)
            except:
                check_subscription_available = ""

            if check_subscription_available:

                total_amount = float(check_subscription_available.total_amount_avilable) + float(subscription_object.recharge_amount)

                subscription =  partner_subscriptions.objects.filter(id = check_subscription_available.id).update(

                    per_bill_cost = per_bill_cost,
                    per_receipt_cost = per_receipt_cost,
                    per_cash_memo_cost = per_cash_memo_cost,

                    per_digital_bill_cost = per_digital_bill_cost,
                    per_digital_receipt_cost = per_digital_receipt_cost,
                    per_digital_cash_memo_cost = per_digital_cash_memo_cost,

                    total_amount_avilable = total_amount,

                )
                try:
                    last_id = partner_recharge_history.objects.filter().last()
                    invoice_no = 'GB' + str(last_id.id+1)
                except:
                    invoice_no = 'GB' + str(1)
                partner_recharge_history.objects.create(
                
                subscription_plan_id = subscription_object.id,
                subscription_name = subscription_object.add_on_name,
                partner_id = partner_object,

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
                    sweetify.success(request, title="Success", icon='success', text='Add On purchased Successfully.', timer=1500)
                    return redirect(recharge_subscriptions)

        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

            return redirect(recharge_subscriptions)
    else:

        sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

@csrf_exempt
def add_on_subscription_purchased_fail(request):
    user_id = request.POST["udf2"] # user id
    udf3 = request.POST["udf3"] # encoded password
    udf4 = request.POST["udf4"] # decode key id

    # Decode Password
    partner_subscriptions_key = partner_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(partner_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()

    user_object =  GreenBillUser.objects.get(id=user_id)

    mobile_no = user_object.mobile_no
    
    request.session['mobile_no'] = mobile_no
    request.session['password'] = decPassword

    user = authenticate(mobile_no=request.session['mobile_no'], password=request.session['password'])
    login(request, user)

    sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

    return redirect(recharge_subscriptions)




def my_subscription_bill(request,id):

    try:
        try:
            logo = generalSetting.objects.get(id=1) 
            owner_logo = logo.o_digital_signature
        except:
            owner_logo = '' 
        bill_details = partner_recharge_history.objects.get(id=id)
        try:
            all_business = PartnerProfile.objects.get(p_user=bill_details.partner_id , p_active_account = True)
            partner_state = all_business.p_state
            partner_city = all_business.p_city
            partner_area = all_business.p_area
            partner_pincode = all_business.p_pin_code
            partner_mobile_number = all_business.p_user
            partner_business_name = all_business.p_business_name
            partner_gstin_number = all_business.p_gstin
            p_business_bill_name = all_business.p_business_name_for_billing
            p_monbile_bill_number = all_business.p_billing_phone
            p_bill_adress = all_business.p_billing_address
        except:
            partner_state = ""
            partner_city = ''
            partner_area = ''
            partner_pincode = ''
            partner_mobile_number = ''
            partner_business_name = ''
            partner_gstin_number = ''
            p_business_bill_name = ''
            p_monbile_bill_number = ''
            p_bill_adress = ''
        gst_amount = ''
        gst = ''
        if bill_details.is_subscription_plan == True:
            
            subscription_plan = subscription_plan_details.objects.filter(id=bill_details.subscription_plan_id)

            # print('aa',subscription_plan)
            
            for subscription in subscription_plan:

                if bill_details.mode == "cashwithoutbill":
                    gst_amount = subscription.gst_amount
                    subscription_amount = subscription.subscription_plan_cost
                    subscription.total_cost_gst = float(subscription_amount)
                    subscription.current_plan = 1
                else:
                    gst_amount = subscription.gst_amount
                    subscription_amount = subscription.subscription_plan_cost
                    subscription.total_cost_gst = float(subscription_amount) + float(gst_amount)
                    subscription.current_plan = 1

                # plan_Subtotal = bill_details.cost

                # print("plan_Subtotal",plan_Subtotal)


        elif bill_details.is_promotional_sms_plan == True:
            subscription_plan = promotional_subscription_plan_model.objects.filter(id=bill_details.subscription_plan_id)
            # print('abc',subscription_plan)
            for subscription in  subscription_plan:

                if bill_details.mode == "cashwithoutbill":
                    gst_amount = subscription.gst_amount
                    gst = float(gst_amount)/2
                    subscription_amount = subscription.total_sms_cost
                    subscription.total_cost_gst = float(subscription_amount) 

                    subscription.current_plan = 2
                else:
                    gst_amount = subscription.gst_amount
                    gst = float(gst_amount)/2
                    subscription_amount = subscription.total_sms_cost
                    subscription.total_cost_gst = float(subscription_amount) + float(gst_amount)

                    subscription.current_plan = 2


        elif bill_details.is_transactional_sms_plan == True:
            subscription_plan = transactional_subscription_plan_model.objects.filter(id=bill_details.subscription_plan_id)

            for subscription in subscription_plan:

                if bill_details.mode == "cashwithoutbill":
                    gst_amount = subscription.gst_amount
                    gst = float(subscription.gst_amount)/2
                    subscription_amount = subscription.total_sms_cost
                    subscription.total_cost_gst = float(subscription_amount) 

                    plan_Subtotal = bill_details.cost

                    subscription.current_plan = 3
                else:
                    gst_amount = subscription.gst_amount
                    gst = float(subscription.gst_amount)/2
                    subscription_amount = subscription.total_sms_cost
                    subscription.total_cost_gst = float(subscription_amount) + float(gst_amount)

                    plan_Subtotal = bill_details.cost

                    subscription.current_plan = 3

        elif bill_details.is_add_on_plan == True:
            subscription_plan = add_on_plan_model.objects.filter(id=bill_details.subscription_plan_id)
            for subscription in  subscription_plan:

                if bill_details.mode == "cashwithoutbill":

                    gst_amount = subscription.gst_amount
                    subscription_amount = subscription.recharge_amount
                    subscription.total_cost_gst = float(subscription_amount) 
                    subscription.current_plan = 4

                else:
                    gst_amount = subscription.gst_amount
                    subscription_amount = subscription.recharge_amount
                    subscription.total_cost_gst = float(subscription_amount) + float(gst_amount)
                    subscription.current_plan = 4

        tax_amount = bill_details.cost

        print("tax_amount",tax_amount)
        print("gst_amount",gst_amount)
        print("gst",gst)



        # total_gst = (int(tax_amount)/100)*18

        # total_amount = int(tax_amount)

        if partner_state ==  "Maharashtra" or partner_state == "maharashtra":

            instate = True
            outstate = False

        else:
            outstate = True
            instate = False

        # print(total_amount)

        sgst = (bill_details.cost) * 0.09
        cgst = (bill_details.cost) * 0.09
        igst = (bill_details.cost) * 0.18

        if bill_details.mode == "cashwithoutbill":
            total = bill_details.cost 
            print(total)
            round_of = total % 1

            end_value = round(total)
        else:

            total = bill_details.cost + igst

            round_of = total % 1

            end_value = round(total)

        context = {'bill_details' : bill_details,
                    'partner_state' : partner_state,
                    'gst_amount': gst_amount,
                    'p_business_bill_name':p_business_bill_name,
                    'p_monbile_bill_number':p_monbile_bill_number,
                    'sgst': sgst,
                    'cgst': cgst,
                    'igst': igst,
                    'partner_mobile_number': partner_mobile_number,
                    'partner_business_name': partner_business_name,
                    'partner_gstin_number': partner_gstin_number,
                    'p_bill_adress':p_bill_adress,
                    'owner_logo': owner_logo,
                    'mode':bill_details.mode,
                    'partner_city' : partner_city,
                    'partner_area' : partner_area,
                    'partner_pincode' : partner_pincode, 
                    'subscription_plan' : subscription_plan, 
                    'instate' : instate,
                    'outstate' : outstate,
                    'total':total,
                    'round_of':round_of,
                    'end_value':end_value,
                    'business_logo':'http://157.230.228.250/media/green-bill-logo.jpg'
                }
        return render(request, "partner/subscription/my-subscription-bill-partner.html",context)
    except:
        return render(request, 'page-404.html')