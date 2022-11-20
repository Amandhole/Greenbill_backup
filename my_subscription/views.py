import os
import random
import sweetify
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from subscription_plan.models import *
from users.models import Merchant_users, MerchantProfile, GreenBillUser
from .models import *
from merchant_setting.models import *
from app.views import is_merchant_or_merchant_staff
from merchant_promotion.models import bulkMailSmsMerchantCustomerModel
from django.contrib.sessions.models import Session
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
from django.db.models import Count
from cryptography.fernet import Fernet
from datetime import date

from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.conf import settings
from django.core.mail import get_connection, send_mail, BadHeaderError, EmailMessage

from referral_points.models import *

import requests
import time
import pyshorteners

from app.models import generalSetting



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def save_contact_form_subscriptions_requirements(request):

    if request.method == "POST":
        contact_name_requirement = request.POST["contact_name"]
        contact_no_requirement = request.POST["contact_no"]
        contact_email_requirement = request.POST["contact_email_id"]
        contact_requirement_form = request.POST["contact_requirements"]
        contact_subscriptions_name = request.POST["subscription_name"]

        result = contact_for_subscriptions_requirements.objects.create(contact_no=contact_no_requirement, 
            contact_email_id=contact_email_requirement, contact_name=contact_name_requirement, 
            contact_requirements=contact_requirement_form, subscription_name=contact_subscriptions_name )
    if result:
        sweetify.success(request, title="Thank You", icon='success',
                             text='Your Requirements Successfully Submitted.', timer=1500)
    else:
        sweetify.success(request, title="Oops...",
                             icon='error', text='Fail to create.', timer=1000)
    return redirect(recharge_subscriptions)


def GetAllAmountsAdon(request):
    plan_id = request.POST['plan_id']
    addons_plans = add_on_plan_model.objects.get(id=plan_id)
    
    list1 = []

    filtered_amount_list = []

    if addons_plans.recharge_amount_one:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_one
        })

    if addons_plans.recharge_amount_two:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_two
        })

    if addons_plans.recharge_amount_three:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_three
        })

    if addons_plans.recharge_amount_four:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_four
        })

    if addons_plans.recharge_amount_five:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_five
        })

    if addons_plans.recharge_amount_six:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_six
        })

    if addons_plans.recharge_amount_seven:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_seven
        })

    if addons_plans.recharge_amount_eight:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_eight
        })

    if addons_plans.recharge_amount_nine:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_nine
        })

    if addons_plans.recharge_amount_ten:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_ten
        })

    if addons_plans.recharge_amount_eleven:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_eleven
        })

    if addons_plans.recharge_amount_twelve:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_twelve
        })

    if addons_plans.recharge_amount_thirteen:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_thirteen
        })

    if addons_plans.recharge_amount_fourteen:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_fourteen
        })

    if addons_plans.recharge_amount_fifteen:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_fifteen
        })

    if addons_plans.recharge_amount_sixteen:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_sixteen
        })

    if addons_plans.recharge_amount_seventeen:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_seventeen
        })

    if addons_plans.recharge_amount_eighteen:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_eighteen
        })

    if addons_plans.recharge_amount_nineteen:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_nineteen
        })

    if addons_plans.recharge_amount_twenty:
        list1.append({
            "all_recharge_amount": addons_plans.recharge_amount_twenty
        })

    for x in list1:
        if x['all_recharge_amount'] not in filtered_amount_list:
            if x['all_recharge_amount'] != '':
                filtered_amount_list.append(x['all_recharge_amount'])
    return JsonResponse({"data":filtered_amount_list})



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def recharge_subscriptions(request):
    
    all_subscriptions_plans = subscription_plan_details.objects.all().filter(is_active=True).order_by('-id')

    promotional_sms_plans = promotional_subscription_plan_model.objects.all().filter(is_active=True).order_by('-id')

    transactional_sms_plans = transactional_subscription_plan_model.objects.all().filter(is_active=True).order_by('-id')

    addons_plans = add_on_plan_model.objects.all().filter(is_active=True).order_by('-id')

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    my_greenbill_subscription = merchant_subscriptions.objects.filter(merchant_id=merchant_id, is_active=True).last()
    
    my_promotional_subscription = promotional_sms_subscriptions.objects.filter(merchant_id=merchant_id, is_active=True).last()
    
    my_transactional_subscription = transactional_sms_subscriptions.objects.filter(merchant_id=merchant_id, is_active=True).last()

    merchant_email = merchant_object.email

    merchant_first_name = merchant_object.first_name

    merchant_last_name = merchant_object.last_name

    subscription_plan_avilability = False

    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_user_object.merchant_user_id, m_active_account = True)


    


    startswith = str(merchant_business_id.id) + ','
    endswith = ','+ str(merchant_business_id.id)
    contains = ','+ str(merchant_business_id.id) + ','
    exact = str(merchant_business_id.id)

    try:  
        subscription_object = merchant_subscriptions.objects.get(
            Q(merchant_id = merchant_object),
            Q(is_active = True),
            Q(business_ids__startswith = startswith) | 
            Q(business_ids__endswith = endswith) | 
            Q(business_ids__contains = contains) | 
            Q(business_ids__exact = exact)
        )

        subscription_plan_avilability = True


    except:
        subscription_plan_avilability = False

    # print(subscription_object)

    all_business = MerchantProfile.objects.filter(m_user=merchant_id)



    # if merchant_business_category != 11 and merchant_business_category != 12:

    #         business_id = business.id

    #         if business_id != 11:
    #             if

    business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)
    try:
        merchant_state = business_object.m_state
    except:
        merchant_state = ''

    merchant_business_category = business_object.m_business_category.id
 
    merchant_state = business_object.m_state

    for active_category in all_business:

        business_category_id = active_category.m_business_category.id

        try:

            if merchant_business_category != 11 and merchant_business_category != 12:
                if business_category_id != 11 and business_category_id != 12:
                    active_category.merchant_id = active_category.id
                    active_category.business_name = active_category.m_business_name
                    active_category.business_area = active_category.m_area

            elif merchant_business_category == 11:
                if business_category_id == 11:
                    active_category.merchant_id = active_category.id
                    active_category.business_name = active_category.m_business_name
                    active_category.business_area = active_category.m_area


            elif merchant_business_category == 12:
                if business_category_id == 12:
                    active_category.merchant_id = active_category.id
                    active_category.business_name = active_category.m_business_name
                    active_category.business_area = active_category.m_area
        except:
            pass
   
    if merchant_state == "Maharashtra" or merchant_state == "maharashtra":

        sgst = 9
        cgst = 9
        igst = 1

    else:
        igst = 18
        sgst = 1
        cgst = 1


    merchant_business_id = business_object.m_business_category.id

    active_subscription_object = getActiveSubscriptionPlan(request, business_object.id)

    subscriptions_list = []

    addons_list = []

    

    for business in all_business:

        business_id = business.id

        startswith = str(business_id) + ','
        endswith = ','+ str(business_id)
        contains = ','+ str(business_id) + ','
        exact = str(business_id)

        try:  
            subscription_object = merchant_subscriptions.objects.get(
                Q(merchant_id = merchant_object),
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )

            if subscription_object:
                business.active_subscription = True


        except:
            business.active_subscription = False


    for business in all_business:

        business_id = business.id

        startswith = str(business_id) + ','
        endswith = ','+ str(business_id)
        contains = ','+ str(business_id) + ','
        exact = str(business_id)

        try:  
            subscription_object = promotional_sms_subscriptions.objects.get(
                Q(merchant_id = merchant_object),
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )

            if subscription_object:
                business.promotional_sms_active_subscription = True

        except:
            business.promotional_sms_active_subscription = False

    for subscription in promotional_sms_plans:
        gst_amount = subscription.gst_amount
        toal_cost = subscription.total_sms_cost
        subscription.total_amount_with_gst = float(toal_cost) - float(gst_amount)
         

    for business in all_business:

        business_id = business.id

        startswith = str(business_id) + ','
        endswith = ','+ str(business_id)
        contains = ','+ str(business_id) + ','
        exact = str(business_id)

        try:  
            subscription_object = transactional_sms_subscriptions.objects.get(
                Q(merchant_id = merchant_object),
                Q(is_active = True),
                Q(business_ids__startswith = startswith) | 
                Q(business_ids__endswith = endswith) | 
                Q(business_ids__contains = contains) | 
                Q(business_ids__exact = exact)
            )

            if subscription_object:
                business.transactional_sms_active_subscription = True

        except:
            business.transactional_sms_active_subscription = False

    for subscription in transactional_sms_plans:
        gst_amount = subscription.gst_amount
        total_cost = subscription.total_sms_cost
        subscription.total_cost_with_gst = float(total_cost) - float(gst_amount) 

    for subscription in all_subscriptions_plans:

        if subscription.user_type != "partner":
        
            if subscription.customized_plan_for == "merchant":
                valid_for_users = subscription.number_of_users

                cost_per_users = subscription.cost_for_users

                total_cost = subscription.subscription_plan_cost

                subscription.including_gst = float(total_cost) - float(subscription.gst_amount)

                try:

                    subscription.total_cost_per_user = int(valid_for_users) * int(cost_per_users)
                except:
                    subscription.total_cost_per_user = ''

                merchant_name_list = list(subscription.merchant_name.split(","))
                if str(business_object.id) in merchant_name_list:
                    if subscription not in subscriptions_list: 
                        subscriptions_list.append(subscription)
            elif subscription.customized_plan_for ==  "business_category":
                valid_for_users = subscription.number_of_users

                cost_per_users = subscription.cost_for_users

                total_cost = subscription.subscription_plan_cost

                subscription.including_gst = float(total_cost) - float(subscription.gst_amount)

                try:

                    subscription.total_cost_per_user = int(valid_for_users) * int(cost_per_users)
                except:
                    subscription.total_cost_per_user = ''

                category_list = list(subscription.business_category.split(","))

                if str(merchant_business_id) in category_list:
                    if subscription not in subscriptions_list:
                        subscriptions_list.append(subscription)

            else:
                pans_gst_amount = subscription.gst_amount
                total_cost = subscription.subscription_plan_cost

                subscription.including_gst = float(total_cost) - float(subscription.gst_amount)

                valid_for_users = subscription.number_of_users

                cost_per_users = subscription.cost_for_users

                try:
                    subscription.total_cost_per_user = int(valid_for_users) * int(cost_per_users)
                except:
                    subscription.total_cost_per_user = ''

                if business_object.m_business_category.id != 11 and business_object.m_business_category.id != 12:
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

    surl = "http://157.230.228.250/subscription-purchased-success/"

    furl = "http://157.230.228.250/subscription-purchased-fail/"

    promotional_sms_surl = "http://157.230.228.250/promotional-sms-subscription-purchased-success/"

    promotional_sms_furl = "http://157.230.228.250/promotional-sms-subscription-purchased-fail/"

    transactional_sms_surl = "http://157.230.228.250/transactional-sms-subscription-purchased-success/"

    transactional_sms_furl = "http://157.230.228.250/transactional-sms-subscription-purchased-fail/"

    add_on_surl = "http://157.230.228.250/add-on-subscription-purchased-success/"

    add_on_furl = "http://157.230.228.250/add-on-subscription-purchased-fail/"

     # Password Encryption Start
    enc_key = Fernet.generate_key()
    fernet = Fernet(enc_key)
    
    print("*********************************************************")
    # print(request.session['_auth_user_id'])

    # for key, value in request.session.items():
    #     print('{} => {}'.format(key, value))
    #     # print(Session.objects.all())
    # # print(request.session['password'])
    # try:
    password = request.session['password']
    encPassword = fernet.encrypt(password.encode())
    # except:
    #     return HttpResponse("Problem Loding page !!1")
    merchant_subscriptions_key = merchant_subscriptions_keys.objects.create(key = enc_key.decode("utf-8"))

    for subscription in addons_plans:

        adon_gst_amount = subscription.gst_amount
        total_adon_cost = subscription.recharge_amount
        subscription.total_adon_cost_with_gst = float(total_adon_cost) - float(adon_gst_amount)

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
        productinfo = str("subscription_name-"+ subscription.add_on_name)
        amount = str(subscription.recharge_amount)

        udf1 = str(subscription.id) # subscription id

        udf2 = str(request.user.id) # user object

        udf3 = str(encPassword.decode("utf-8")) # encoded Password

        udf4 = str(merchant_subscriptions_key.id) # decode key id

        udf5 = str(business_object.id) # Business Id

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
    
    action = PAYU_BASE_URL

    
    
    context = {
        "sgst_value" : sgst,
        "cgst_value" : cgst,
        "igst_value" : igst,
        "merchant_email" : merchant_email,
        "merchant_first_name" : merchant_first_name,
        "merchant_last_name" : merchant_last_name,
        "subscriptions_list" : subscriptions_list,
        "merchant_mobile_no" : request.user,
        "promotional_sms_plans_list" : promotional_sms_plans,
        "transactional_sms_plans_list":transactional_sms_plans,
        "addons_plans": addons_plans,
        "addons_list" : addons_list,
        "MERCHANT_KEY": key,
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
        "all_business": all_business,
        "active_subscription_object":active_subscription_object,
        "merchant_state":merchant_state,
        "subscription_plan_avilability":subscription_plan_avilability,
        "SettingNavclass": 'active',
        "settingsCollapseShow": "show",
        "MySubscriptionNavclass": 'active',
        'my_greenbill_subscription': my_greenbill_subscription,
        'my_transactional_subscription': my_transactional_subscription,
        'my_promotional_subscription': my_promotional_subscription,
    }
        
    return render(request, "merchant/subscription/subscription-recharge1.html", context)





@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def get_plan_by_id(request, id):

    business_ids = request.POST['business_ids']
    no_of_users = request.POST['no_of_users']
    month_validity = request.POST['month_validity']
    merchant_gst = request.POST['merchant_gst']
    
    subscription = subscription_plan_details.objects.get(id=id)
    object1 = subscription_plan_details.objects.filter(id=id).update(valid_for_month=month_validity, merchant_number_of_users = no_of_users, merchant_gst = merchant_gst)

    # Test
    # key="A4MQHd"
    # SALT = "HLysMjoK"
    # PAYU_BASE_URL = "https://test.payu.in/_payment"

    # Production
    key="IUZdcF"
    SALT="7ViVXMy1"
    # PAYU_BASE_URL = "https://secure.payu.in/_payment"

    # Password Encryption Start
    

    merchant_subscriptions_key = merchant_subscriptions_keys.objects.create(key = enc_key.decode("utf-8"))

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


    cost_for_users = subscription.cost_for_users
    cost_per_user_plan = float(cost_for_users) * float(no_of_users) * float(month_validity)
    data = float(cost_per_user_plan) + float(subscription.subscription_plan_cost)
    gst_amount = (18 * float(data))/100
    amount1 = float(gst_amount) + float(data)
    
    amount = str(amount1)

    udf1 = str(subscription.id) # subscription id
    
    udf2 = str(request.user.id) # user object

    udf3 = str(encPassword.decode("utf-8")) # encoded Password

    udf4 = str(merchant_subscriptions_key.id) # decode key id

    udf5 = str(business_ids) # Business Ids

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
    udf5 = request.POST["udf5"] # Business Ids
    udf6 = request.POST["udf6"]
    business_ids = udf5

    mihpayid = request.POST["mihpayid"]

    # Decode Password
    merchant_subscriptions_key = merchant_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(merchant_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()


    # SALT = "HLysMjoK" # Test Salt
    SALT="7ViVXMy1" # Production Salt

    merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    user_object =  GreenBillUser.objects.get(id=user_id)

    merchant_business_id = MerchantProfile.objects.get(m_user = user_object, m_active_account = True)

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

            subscription_object = subscription_plan_details.objects.get(id=subscription_id)

            per_bill_cost = subscription_object.per_bill_cost
            per_digital_bill_cost = subscription_object.per_digital_bill_cost

            total_amount = float(subscription_object.recharge_amount)
            subscription_plan_cost = float(subscription_object.subscription_plan_cost)

            today = date.today()
            d1 = today.strftime("%d-%m-%Y")
            start_date = datetime.datetime.strptime(d1, "%d-%m-%Y")
            delta_period = int(subscription_object.valid_for_month)
            end_date = start_date + relativedelta(months=delta_period)
            expiry_date = end_date.strftime("%d-%m-%Y")

            business_ids_list = list(business_ids.split(","))

            subscription_available_referral_count = 0

            subscription_available_referral_count = merchant_subscriptions.objects.filter(merchant_id = merchant_object).count()

            for business_id in business_ids_list:
                startswith = str(business_id) + ','
                endswith = ','+ str(business_id)
                contains = ','+ str(business_id) + ','
                exact = str(business_id)

                try:
                    check_subscription_available = merchant_subscriptions.objects.get(
                        Q(merchant_id = merchant_object),
                        Q(is_active = True),
                        Q(business_ids__startswith = startswith) | 
                        Q(business_ids__endswith = endswith) | 
                        Q(business_ids__contains = contains) | 
                        Q(business_ids__exact = exact)
                    )
                except:
                    check_subscription_available = ""

                count_check = 0

                referral_amount_obj = ReferralModel.objects.all().last()

                refferant_amount = referral_amount_obj.recharge_amount_per_referent

                refferal_amount = referral_amount_obj.recharge_amount_per_refferal

                if merchant_business_id.subscription_count == 0:
                    MerchantProfile.objects.filter(m_user = user_object, m_active_account = True).update(subscription_count=1)
                    if merchant_object.m_used_referral_code:
                        referral_merchant_id = GreenBillUser.objects.filter(merchant_referral_code=merchant_object.m_used_referral_code)
                        
                        merchant_profile_obj = MerchantProfile.objects.filter(id=referral_merchant_id)

                        for business in merchant_profile_obj: 
                            subscription_detail = merchant_subscriptions.objects.filter(merchant_id=business, is_active=True).last()

                            new_subscription_amount = subscription_detail.total_amount_avilable + refferant_amount

                            merchant_subscriptions.objects.filter(merchant_id=business, is_active=True).update(total_amount_avilable=new_subscription_amount)
                else:
                    count_check = 1
                    count = merchant_business_id.subscription_count + 1
                    MerchantProfile.objects.filter(m_user = user_object, m_active_account = True).update(subscription_count=count)


                if check_subscription_available:

                    business_ids_list_temp = list((check_subscription_available.business_ids).split(","))

                    
                    business_ids_list_temp.remove(business_id)

                    business_ids_new = ""

                    business_ids_new = ','.join(business_ids_list_temp)

                    avilable_amount = float(total_amount) + float(check_subscription_available.total_amount_avilable)
                    
                    update_result = merchant_subscriptions.objects.filter(id = check_subscription_available.id).update(business_ids = business_ids_new)

                    get_updated_suscription = merchant_subscriptions.objects.get(id = check_subscription_available.id)

                    if get_updated_suscription.business_ids == "":
                        merchant_subscriptions.objects.filter(id = get_updated_suscription.id).update(is_active = False)
                else:
                    if count_check == 0:
                        avilable_amount = float(total_amount) + float(refferal_amount)
                    else:
                        avilable_amount = float(total_amount)

            subscription_active_status = True

            subscription =  merchant_subscriptions.objects.create(
                subscription_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                merchant_id = merchant_object,
                business_ids = business_ids,

                valid_for_month = subscription_object.valid_for_month,

                per_bill_cost = per_bill_cost,

                per_digital_bill_cost = per_digital_bill_cost,

                recharge_amount = total_amount,
                total_amount_avilable = avilable_amount,
                is_active = subscription_active_status,

                purchase_cost = subscription_plan_cost,
                expiry_date = expiry_date,

                no_of_users = subscription_object.merchant_number_of_users,

                gst_amount = subscription_object.merchant_gst,

                transaction_id = txnid,
                payu_transaction_id = mihpayid,
                merchant_business_id = merchant_business_id.id,
            )
            try:
                last_id = recharge_history.objects.filter().last()
                invoice_no = 'GB' + str(last_id.id+1)
            except:
                invoice_no = 'GB' + str(1)
            
            recharge_history.objects.create(
                subscription_plan_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                merchant_id = merchant_object,
                business_ids = business_ids,

                valid_for_month = subscription_object.valid_for_month,

                per_bill_cost = per_bill_cost,

                per_digital_bill_cost = per_digital_bill_cost,

                cost = subscription_plan_cost,

                is_subscription_plan = True,
                expiry_date = expiry_date,

                no_of_users = subscription_object.merchant_number_of_users,

                gst_amount = subscription_object.merchant_gst,

                transaction_id = txnid,
                payu_transaction_id = mihpayid,
                invoice_no = invoice_no,
                merchant_business_id = merchant_business_id.id,
            )

            if merchant_object.m_used_referral_code and subscription_available_referral_count == 0:

                referral_object = ReferralModel.objects.get(id = 1)

                if referral_object.recharge_amount_per_refferal:

                    referral_user_object = GreenBillUser.objects.get(merchant_referral_code = merchant_object.m_used_referral_code)

                    # try:
                    referral_merchant_subscriptions_object = merchant_subscriptions.objects.filter(merchant_id = referral_user_object, is_active = True).order_by('-id')
                    # except:
                    #     referral_merchant_subscriptions_object = ""

                    if referral_merchant_subscriptions_object:
                        referral_merchant_subscriptions_total_amount = 0
                        referral_merchant_subscriptions_total_amount = float(referral_merchant_subscriptions_object[0].total_amount_avilable) + float(referral_object.recharge_amount_per_refferal)
                        
                        merchant_subscriptions.objects.filter(
                            id = referral_merchant_subscriptions_object[0].id
                            ).update(total_amount_avilable = referral_merchant_subscriptions_total_amount)

                        ReferralHistory.objects.create(
                            referent_mobile_no = merchant_object.mobile_no,
                            referral_mobile_no = referral_user_object.mobile_no,
                            is_referral = True,
                            is_referent = False,
                            earned_recharge_points = referral_object.recharge_amount_per_refferal
                        )

                if referral_object.recharge_amount_per_referent:
                    subscription.total_amount_avilable = float(total_amount) + float(referral_object.recharge_amount_per_referent)
                    subscription.save()

                    ReferralHistory.objects.create(
                        referent_mobile_no = merchant_object.mobile_no,
                        referral_mobile_no = referral_user_object.mobile_no,
                        is_referral = False,
                        is_referent = True,
                        earned_recharge_points = referral_object.recharge_amount_per_referent
                    )

            if subscription:
                reacharge_bill = recharge_history.objects.filter(merchant_id= merchant_object).last()

                recharge_bill_url = "http://157.230.228.250/my-subscription-bill/" + str(reacharge_bill.id) + "/"
                 

                s = pyshorteners.Shortener()

                short_url = s.tinyurl.short(recharge_bill_url)


                merchant_email = GreenBillUser.objects.get(mobile_no= request.user).m_email
                subject = 'Thank You For Buying Promotional Subscription Plan'
                message = f' Dear Merchant, \n\n Thank You for your Purchase!!! \n\n Your Green Bill for your recent purchase updated in your Merchant Portal. \n\nYou can view your invoice on your Green Bill Merchant App or Merchant Web Portal.\n Best Regards,\n\n Green Bill Team.' '\n\n Invoice Url: ' + str(recharge_bill_url)
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [merchant_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()

                sweetify.success(request, title="Success", icon='success', text='Subscription purchased Successfully.', timer=1500)
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
    merchant_subscriptions_key = merchant_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(merchant_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()

    user_object =  GreenBillUser.objects.get(id=user_id)

    mobile_no = user_object.mobile_no
    
    request.session['mobile_no'] = mobile_no
    request.session['password'] = decPassword

    user = authenticate(mobile_no=request.session['mobile_no'], password=request.session['password'])
    login(request, user)

    sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

    return redirect(recharge_subscriptions)



# SMS Promotional Plan

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def get_promotional_sms_plan_by_id(request, id):

    business_ids = request.POST['business_ids']
    
    subscription = promotional_subscription_plan_model.objects.get(id=id)

    # Test
    # key="A4MQHd"
    # SALT = "HLysMjoK"
    # PAYU_BASE_URL = "https://test.payu.in/_payment"

    # Production
    key="IUZdcF"
    SALT="7ViVXMy1"
    # PAYU_BASE_URL = "https://secure.payu.in/_payment"

    # Password Encryption Start
    enc_key = Fernet.generate_key()
    fernet = Fernet(enc_key)
    password = request.session['password']
    encPassword = fernet.encrypt(password.encode())

    merchant_subscriptions_key = merchant_subscriptions_keys.objects.create(key = enc_key.decode("utf-8"))

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
    productinfo = str("Promotional_SMS_Subscription_Plan-"+ subscription.subscription_name)
    amount = str(subscription.total_sms_cost)

    udf1 = str(subscription.id) # subscription id
    
    udf2 = str(request.user.id) # user object

    udf3 = str(encPassword.decode("utf-8")) # encoded Password

    udf4 = str(merchant_subscriptions_key.id) # decode key id

    udf5 = str(business_ids) # Business Ids

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
    }

    return JsonResponse(context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def get_adon_sms_plan_by_id(request, id):
  

    business_ids = request.POST['business_ids']

    adon_amount = request.POST['adon_amount']
    gst_amount = float(adon_amount)*0.18

    Gst_amount = (float(adon_amount)*0.18)+float(adon_amount)

    subscription = add_on_plan_model.objects.filter(id=id).update(actual_final_amount = Gst_amount, gst_amount = gst_amount)
    
    subscription = add_on_plan_model.objects.get(id=id)

    # Test
    # key="A4MQHd"
    # SALT = "HLysMjoK"
    # PAYU_BASE_URL = "https://test.payu.in/_payment"

    # Production
    key="IUZdcF"
    SALT="7ViVXMy1"

    PAYU_BASE_URL = "https://secure.payu.in/_payment"

    # Password Encryption Start
    enc_key = Fernet.generate_key()
    fernet = Fernet(enc_key)
    password = request.session['password']
    encPassword = fernet.encrypt(password.encode())

    merchant_subscriptions_key = merchant_subscriptions_keys.objects.create(key = enc_key.decode("utf-8"))

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
    productinfo = str("Adon_SMS_Subscription_Plan-"+ subscription.add_on_name)

    amount = str(Gst_amount)

    udf1 = str(subscription.id) # subscription id
    
    udf2 = str(request.user.id) # user object

    udf3 = str(encPassword.decode("utf-8")) # encoded Password

    udf4 = str(merchant_subscriptions_key.id) # decode key id

    udf5 = str(business_ids) # Business Ids

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
    }

    return JsonResponse(context)

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
    udf5 = request.POST["udf5"] # Business Ids
    udf6 = request.POST["udf6"]
    business_ids = udf5
    mihpayid = request.POST["mihpayid"]

    # Decode Password
    merchant_subscriptions_key = merchant_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(merchant_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()


    # SALT = "HLysMjoK" # Test Salt
    SALT="7ViVXMy1" # Production Salt

    merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    user_object =  GreenBillUser.objects.get(id=user_id)

    merchant_business_id = MerchantProfile.objects.get(m_user = user_object, m_active_account = True)

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

            subscription_object = promotional_subscription_plan_model.objects.get(id=subscription_id)

            total_sms = subscription_object.total_sms
            per_sms_cost = subscription_object.per_sms_cost
            total_sms_cost = float(subscription_object.total_sms_cost)
            subscription_plan_cost = float(subscription_object.total_sms_cost)
            total_sms_avilable = total_sms

            business_ids_list = list(business_ids.split(","))

            for business_id in business_ids_list:
                startswith = str(business_id) + ','
                endswith = ','+ str(business_id)
                contains = ','+ str(business_id) + ','
                exact = str(business_id)

                try:
                    check_subscription_available = promotional_sms_subscriptions.objects.get(
                        Q(merchant_id = merchant_object),
                        Q(is_active = True),
                        Q(business_ids__startswith = startswith) | 
                        Q(business_ids__endswith = endswith) | 
                        Q(business_ids__contains = contains) | 
                        Q(business_ids__exact = exact)
                    )
                except:
                    check_subscription_available = ""

                if check_subscription_available:

                    business_ids_list_temp = list((check_subscription_available.business_ids).split(","))
                    
                    business_ids_list_temp.remove(business_id)

                    business_ids_new = ""

                    business_ids_new = ','.join(business_ids_list_temp)
                    
                    update_result = promotional_sms_subscriptions.objects.filter(id = check_subscription_available.id).update(business_ids = business_ids_new)

                    get_updated_suscription = promotional_sms_subscriptions.objects.get(id = check_subscription_available.id)

                    if get_updated_suscription.business_ids == "":
                        promotional_sms_subscriptions.objects.filter(id = get_updated_suscription.id).update(is_active = False)

            subscription_active_status = True

            subscription =  promotional_sms_subscriptions.objects.create(
                subscription_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                merchant_id = merchant_object,
                business_ids = business_ids,

                total_sms = total_sms,
                per_sms_cost = per_sms_cost,

                total_sms_avilable = total_sms_avilable,

                is_active = subscription_active_status,
                purchase_cost = subscription_plan_cost,

                transaction_id = txnid,
                payu_transaction_id = mihpayid,
                # merchant_business_id = merchant_business_id.id,
            )

            try:
                last_id = recharge_history.objects.filter().last()
                invoice_no = 'GB' + str(last_id.id+1)
            except:
                invoice_no = 'GB' + str(1)

            recharge_history.objects.create(
                subscription_plan_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                merchant_id = merchant_object,
                business_ids = business_ids,

                total_sms = total_sms,
                per_sms_cost = per_sms_cost,

                cost = subscription_plan_cost,

                is_promotional_sms_plan = True,

                transaction_id = txnid,
                payu_transaction_id = mihpayid,
                invoice_no = invoice_no,
                merchant_business_id = merchant_business_id.id
            )

            if subscription:
                reacharge_bill = recharge_history.objects.filter(merchant_id= merchant_object).last()

                recharge_bill_url = "http://157.230.228.250/my-subscription-bill/" + str(reacharge_bill.id) + "/"
                 

                s = pyshorteners.Shortener()

                short_url = s.tinyurl.short(recharge_bill_url)


                merchant_email = GreenBillUser.objects.get(mobile_no= request.user).m_email
                subject = 'Thank You For Buying Promotional Subscription Plan'
                message = f' Dear Merchant, \n\n Thank You for your Purchase!!! \n\n Your Green Bill for your recent purchase updated in your Merchant Portal. \n\nYou can view your invoice on your Green Bill Merchant App or Merchant Web Portal.\n Best Regards,\n\n Green Bill Team.' '\n\n Invoice Url: ' + str(recharge_bill_url)
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [merchant_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()

                sweetify.success(request, title="Success", icon='success', text='Subscription purchased Successfully.', timer=1500)
                return redirect(recharge_subscriptions)

        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

            return redirect(recharge_subscriptions)
    else:

        sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

@csrf_exempt
def promotional_sms_subscription_purchased_fail(request):
    user_id = request.POST["udf2"] # user id
    udf3 = request.POST["udf3"] # encoded password
    udf4 = request.POST["udf4"] # decode key id

    # Decode Password
    merchant_subscriptions_key = merchant_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(merchant_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()

    user_object =  GreenBillUser.objects.get(id=user_id)

    mobile_no = user_object.mobile_no
    
    request.session['mobile_no'] = mobile_no
    request.session['password'] = decPassword

    user = authenticate(mobile_no=request.session['mobile_no'], password=request.session['password'])
    login(request, user)

    sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

    return redirect(recharge_subscriptions)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def my_subscription(request):
    all_subscriptions_plans = subscription_plan_details.objects.all().filter(is_active=True).order_by('-id')

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)

    try:


        business_id = business_object.id

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
        per_bill_cost = subscription_object.per_bill_cost
        per_url_cost = subscription_object.per_url_cost
        per_receipt_cost = subscription_object.per_receipt_cost
        per_cash_memo_cost = subscription_object.per_cash_memo_cost

        per_digital_bill_cost = subscription_object.per_digital_bill_cost
        per_digital_receipt_cost = subscription_object.per_digital_receipt_cost
        per_digital_cash_memo_cost = subscription_object.per_digital_cash_memo_cost

        subscription_name = subscription_object.subscription_name
        recharge_amount = subscription_object.purchase_cost
        valid_for_month = subscription_object.valid_for_month
      

        purchase_date = subscription_object.purchase_date
        purchase_cost = subscription_object.purchase_cost
        total_amount_avilable = subscription_object.total_amount_avilable

        expiry_date = subscription_object.expiry_date

        if subscription_object.no_of_users:

            no_of_users = subscription_object.no_of_users
            

        else:
            no_of_users = 0  
        
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
        valid_for_month = ""
        purchase_date = ""
        purchase_cost = ""
        total_amount_avilable = ""

        expiry_date = ""
        no_of_users = ""

    try:

        business_id = business_object.id

        startswith = str(business_id) + ','
        endswith = ','+ str(business_id)
        contains = ','+ str(business_id) + ','
        exact = str(business_id)
                
        subscription_object = promotional_sms_subscriptions.objects.get(
            Q(merchant_id = merchant_object),
            Q(is_active = True),
            Q(business_ids__startswith = startswith) | 
            Q(business_ids__endswith = endswith) | 
            Q(business_ids__contains = contains) | 
            Q(business_ids__exact = exact)
        )

        promotional_sms_subscription_name = subscription_object.subscription_name
        promotional_sms_purchase_date = subscription_object.purchase_date
        promotional_sms_purchase_cost = subscription_object.purchase_cost
        promotional_sms_total_sms = int(subscription_object.total_sms)
        promotional_sms_per_sms_cost = subscription_object.per_sms_cost
        promotional_sms_total_sms_avilable = int(subscription_object.total_sms_avilable)
        promotional_used_sms = promotional_sms_total_sms - promotional_sms_total_sms_avilable

        
    except:

        promotional_sms_subscription_name = ""
        promotional_sms_purchase_date = ""
        promotional_sms_purchase_cost = ""
        promotional_sms_total_sms = ""
        promotional_sms_per_sms_cost = ""
        promotional_sms_total_sms_avilable = ""
        promotional_used_sms = ""

    try:
        business_id = business_object.id

        startswith = str(business_id) + ','
        endswith = ','+ str(business_id)
        contains = ','+ str(business_id) + ','
        exact = str(business_id)
                
        subscription_object = transactional_sms_subscriptions.objects.get(
            Q(merchant_id = merchant_object),
            Q(is_active = True),
            Q(business_ids__startswith = startswith) | 
            Q(business_ids__endswith = endswith) | 
            Q(business_ids__contains = contains) | 
            Q(business_ids__exact = exact)
        )

        transactional_sms_subscription_name = subscription_object.subscription_name
        transactional_sms_purchase_date = subscription_object.purchase_date
        transactional_sms_purchase_cost = subscription_object.purchase_cost
        transactional_sms_total_sms = int(subscription_object.total_sms)
        transactional_sms_per_sms_cost = subscription_object.per_sms_cost
        transactional_sms_total_sms_avilable = int(subscription_object.total_sms_avilable)
        transactional_used_sms = transactional_sms_total_sms - transactional_sms_total_sms_avilable

    except:
        transactional_sms_subscription_name = ""
        transactional_sms_purchase_date = ""
        transactional_sms_purchase_cost = ""
        transactional_sms_total_sms = ""
        transactional_sms_per_sms_cost = ""
        transactional_sms_total_sms_avilable = ""
        transactional_used_sms = ""


    # petrol_bill_sms = petrol_pump_app_setting_model.objects.filter(merchant_id=merchant_object,sms=True)
    # petrol_sms_count = sum(petrol_bill_sms.values_list('sms', flat=True))

    # x = petrol_pump_app_setting_model.objects.filter(merchant_id=merchant_object,sms=True).values('created_at').annotate(event_count = Count('sms')).order_by('-id')    
    # print('petrol_sms_count',x)

    # parking_bill_sms = parking_app_setting_model.objects.filter(merchant_id=merchant_object,sms=True)
    # parking_sms_count = sum(parking_bill_sms.values_list('sms', flat=True))
    # print('parking_sms_count',parking_sms_count)

    # parking_sms = []
    # parking_sms = zip(petrol_bill_sms,parking_bill_sms)
    # print('parking_sms',parking_sms)
    # for j in parking_sms:
    #     print('sms123',j)


    # total_bill_sms = petrol_sms_count + parking_sms_count
    # merchant_digital_bills_data.append(total_bill_sms)

    # petrol_bill_notification = petrol_pump_app_setting_model.objects.filter(merchant_id=merchant_object,digital_bill=True)
    # petrol_notification_count = sum(petrol_bill_notification.values_list('digital_bill', flat=True))
    # print('petrol_notification_count',petrol_notification_count)


    # parking_bill_notification = parking_app_setting_model.objects.filter(merchant_id=merchant_object,digital_bill=True)
    # parking_notification_count = sum(parking_bill_notification.values_list('digital_bill', flat=True))
    # print('parking_notification_count',parking_notification_count)  

    transactional_smsplan = bulkMailSmsMerchantCustomerModel.objects.filter(owner_id=merchant_object,transactional="transactional",o_sent_sms=True).order_by('-id')
    receipent_count = GreenBillUser.objects.filter(is_customer=True).count()

    promotional_smsplan = bulkMailSmsMerchantCustomerModel.objects.filter(owner_id=merchant_object,transactional="promotional",o_sent_sms=True).order_by('-id')

    # total_bill_notification = petrol_notification_count + parking_notification_count
    # merchant_digital_bills_data.append(total_bill_notification) 

    context = {
        "purchase_cost" : purchase_cost,
        "per_url_cost":per_url_cost,
        "per_bill_cost" : per_bill_cost,
        "per_receipt_cost" : per_receipt_cost,
        "per_cash_memo_cost" : per_cash_memo_cost,

        "per_digital_bill_cost" : per_digital_bill_cost,
        "per_digital_receipt_cost" : per_digital_receipt_cost,
        "per_digital_cash_memo_cost" : per_digital_cash_memo_cost,

        "subscription_name" : subscription_name,
        "recharge_amount":recharge_amount,
        "valid_for_month":valid_for_month,
        "no_of_users":no_of_users,
        "purchase_date" : purchase_date,
        "total_amount_avilable" : total_amount_avilable,

        "expiry_date": expiry_date,

        "promotional_sms_subscription_name" : promotional_sms_subscription_name,
        "promotional_sms_purchase_date" : promotional_sms_purchase_date,
        "promotional_sms_purchase_cost" : promotional_sms_purchase_cost,
        "promotional_sms_total_sms" : promotional_sms_total_sms,
        "promotional_sms_per_sms_cost" : promotional_sms_per_sms_cost,
        "promotional_sms_total_sms_avilable" : promotional_sms_total_sms_avilable,
        "promotional_used_sms":promotional_used_sms,

        "transactional_sms_subscription_name" : transactional_sms_subscription_name,
        "transactional_sms_purchase_date" : transactional_sms_purchase_date,
        "transactional_sms_purchase_cost" : transactional_sms_purchase_cost,
        "transactional_sms_total_sms" : transactional_sms_total_sms,
        "transactional_sms_per_sms_cost" : transactional_sms_per_sms_cost,
        "transactional_sms_total_sms_avilable" : transactional_sms_total_sms_avilable,
        "transactional_used_sms":transactional_used_sms,

        "transactional_smsplan":transactional_smsplan,
        "promotional_smsplan":promotional_smsplan,
        "receipent_count":receipent_count,

        "SettingNavclass": 'active',
        "settingsCollapseShow": "show",
        "MySubscriptionNavclass": 'active',
    
    }

    return render(request, "merchant/subscription/my-subscription.html", context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def my_subscription_history(request):

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = True)

    business_id = business_object.id

    startswith = str(business_id) + ','
    endswith = ','+ str(business_id)
    contains = ','+ str(business_id) + ','
    exact = str(business_id)
    
    recharge_his = recharge_history.objects.filter(
        Q(merchant_id = merchant_object),
        Q(business_ids__startswith = startswith) | 
        Q(business_ids__endswith = endswith) | 
        Q(business_ids__contains = contains) | 
        Q(business_ids__exact = exact)
    ).order_by('-id')


    print(recharge_his)
    rech = recharge_history.objects.filter(merchant_id= merchant_object).last()
    iscashwithoutbill = rech.mode 

    print(rech)
    print(iscashwithoutbill)
    for recharge in recharge_his:
        if recharge.is_subscription_plan == True:
            try:
                subscription_plan = subscription_plan_details.objects.filter(id=recharge.subscription_plan_id)
                
                for subscription in subscription_plan:
                    if recharge.mode =="cashwithoutbill":
                        users_cost = float(recharge.no_of_users) * float(recharge.valid_for_month) * float(subscription.cost_for_users)
                        recharge.final_total = float(users_cost) + float(recharge.cost) 
                    else:
                    
                        users_cost = float(recharge.no_of_users) * float(recharge.valid_for_month) * float(subscription.cost_for_users)
                        recharge.final_total = float(users_cost) + float(recharge.cost) + float(recharge.gst_amount)
            except: 
                recharge.final_total = 0
        elif recharge.is_add_on_plan == True: 
            recharge.final_total = float(recharge.cost) + float(recharge.gst_amount) 
                
    
    # print("QAWS",rech)
    
    context = {
        "recharge_history" : recharge_his,
        "SettingNavclass": 'active',
        "settingsCollapseShow": "show",
        "MySubscriptionNavclass": 'active'
    }

    return render(request, "merchant/subscription/my-recharge-history.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def delete_merchant_recharge_history(request,id):
    if request.method == "POST":
        instance = recharge_history.objects.get(id=id)
        instance.delete()
        return JsonResponse({'status': 'success', 'msg': 'Recharge history deleted successfully'})
    else:
        return JsonResponse({"status": "error", 'msg': "Hello Something went wrong"})


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


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def get_transactional_sms_plan_by_id(request, id):

    business_ids = request.POST['business_ids']
    
    subscription = transactional_subscription_plan_model.objects.get(id=id)

    # Test
    # key="A4MQHd"
    # SALT = "HLysMjoK"
    # PAYU_BASE_URL = "https://test.payu.in/_payment"

    # Production
    key="IUZdcF"
    SALT="7ViVXMy1"
    # PAYU_BASE_URL = "https://secure.payu.in/_payment"

    # Password Encryption Start
    enc_key = Fernet.generate_key()
    fernet = Fernet(enc_key)
    password = request.session['password']
    encPassword = fernet.encrypt(password.encode())

    merchant_subscriptions_key = merchant_subscriptions_keys.objects.create(key = enc_key.decode("utf-8"))

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
    productinfo = str("Transactional_SMS_Subscription_Plan-"+ subscription.subscription_name)
    amount = str(subscription.total_sms_cost)

    udf1 = str(subscription.id) # subscription id
    
    udf2 = str(request.user.id) # user object

    udf3 = str(encPassword.decode("utf-8")) # encoded Password

    udf4 = str(merchant_subscriptions_key.id) # decode key id

    udf5 = str(business_ids) # Business Ids

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
    }

    return JsonResponse(context)


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
    merchant_subscriptions_key = merchant_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(merchant_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()


    # SALT = "HLysMjoK" # Test Salt
    SALT="7ViVXMy1" # Production Salt

    merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    user_object =  GreenBillUser.objects.get(id=user_id)

    merchant_business_id = MerchantProfile.objects.get(m_user = user_object, m_active_account = True)

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

            # print("total_sms_avilable",total_sms_avilable)

            business_ids_list = list(business_ids.split(","))

            for business_id in business_ids_list:
                startswith = str(business_id) + ','
                endswith = ','+ str(business_id)
                contains = ','+ str(business_id) + ','
                exact = str(business_id)

                try:
                    check_subscription_available = transactional_sms_subscriptions.objects.get(
                        Q(merchant_id = merchant_object),
                        Q(is_active = True),
                        Q(business_ids__startswith = startswith) | 
                        Q(business_ids__endswith = endswith) | 
                        Q(business_ids__contains = contains) | 
                        Q(business_ids__exact = exact)
                    )
                except:
                    check_subscription_available = ""

                if check_subscription_available:

                    business_ids_list_temp = list((check_subscription_available.business_ids).split(","))
                    
                    business_ids_list_temp.remove(business_id)

                    business_ids_new = ""

                    business_ids_new = ','.join(business_ids_list_temp)
                    
                    update_result = transactional_sms_subscriptions.objects.filter(id = check_subscription_available.id).update(business_ids = business_ids_new)

                    get_updated_suscription = transactional_sms_subscriptions.objects.get(id = check_subscription_available.id)

                    if get_updated_suscription.business_ids == "":
                        transactional_sms_subscriptions.objects.filter(id = get_updated_suscription.id).update(is_active = False)

            subscription_active_status = True

            subscription =  transactional_sms_subscriptions.objects.create(
                subscription_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                merchant_id = merchant_object,
                business_ids = business_ids,

                total_sms = total_sms,
                per_sms_cost = per_sms_cost,

                total_sms_avilable = total_sms_avilable,

                is_active = subscription_active_status,
                purchase_cost = subscription_plan_cost,

                transaction_id = txnid,
                payu_transaction_id = mihpayid,
                # merchant_business_id = merchant_business_id.id,
            )
            try:
                last_id = recharge_history.objects.filter().last()
                invoice_no = 'GB' + str(last_id.id+1)
            except:
                invoice_no = 'GB' + str(1)
            recharge_history.objects.create(
                subscription_plan_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                merchant_id = merchant_object,
                business_ids = business_ids,

                total_sms = total_sms,
                per_sms_cost = per_sms_cost,

                cost = subscription_plan_cost,

                is_transactional_sms_plan = True,

                transaction_id = txnid,
                payu_transaction_id = mihpayid,
                invoice_no = invoice_no,
                merchant_business_id = merchant_business_id.id
            )

            if subscription:


                reacharge_bill = recharge_history.objects.filter(merchant_id= merchant_object).last()

                recharge_bill_url = "http://157.230.228.250/my-subscription-bill/" + str(reacharge_bill.id) + "/"
                 

                s = pyshorteners.Shortener()

                short_url = s.tinyurl.short(recharge_bill_url)


                merchant_email = GreenBillUser.objects.get(mobile_no= request.user).m_email
                subject = 'Thank You For Buying Transactional Subscription Plan'
                message = f' Dear Merchant, \n\n Thank You for your Purchase!!! \n\n Your Green Bill for your recent purchase updated in your Merchant Portal. \n\nYou can view your invoice on your Green Bill Merchant App or Merchant Web Portal.\n Best Regards,\n\n Green Bill Team.' '\n\n Invoice Url: ' + str(recharge_bill_url)
                email_from = settings.EMAIL_HOST_USER
               
                recipient_list = [merchant_email,]
                
                send_res = EmailMessage( subject, message, email_from, recipient_list)

                response = send_res.send()

                response = send_res.send()
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
    merchant_subscriptions_key = merchant_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(merchant_subscriptions_key.key, 'utf-8'))
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
    udf5 = request.POST["udf5"] # Business Id
    udf6 = request.POST["udf6"]
    business_ids = udf5
    mihpayid = request.POST["mihpayid"]

    # Decode Password
    merchant_subscriptions_key = merchant_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(merchant_subscriptions_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()


    # SALT = "HLysMjoK" # Test Salt
    SALT="7ViVXMy1" # Production Salt

    merchant_id = Merchant_users.objects.filter(user_id=user_id).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    user_object =  GreenBillUser.objects.get(id=user_id)

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

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

            subscription_object = add_on_plan_model.objects.get(id=subscription_id)

            # per_bill_cost = subscription_object.per_bill_cost
            # per_receipt_cost = subscription_object.per_receipt_cost
            # per_cash_memo_cost = subscription_object.per_cash_memo_cost
            # per_digital_bill_cost = subscription_object.per_digital_bill_cost
            # per_digital_receipt_cost = subscription_object.per_digital_receipt_cost
            # per_digital_cash_memo_cost = subscription_object.per_digital_cash_memo_cost

            business_id = udf5

            startswith = str(business_id) + ','
            endswith = ','+ str(business_id)
            contains = ','+ str(business_id) + ','
            exact = str(business_id)

            try:
                check_subscription_available = merchant_subscriptions.objects.get(
                    Q(merchant_id = merchant_object),
                    Q(is_active = True),
                    Q(business_ids__startswith = startswith) | 
                    Q(business_ids__endswith = endswith) | 
                    Q(business_ids__contains = contains) | 
                    Q(business_ids__exact = exact)
                )
            except:
                check_subscription_available = ""

            if check_subscription_available:
                

                total_amount = float(check_subscription_available.total_amount_avilable) + float(subscription_object.actual_final_amount)

                subscription =  merchant_subscriptions.objects.filter(id = check_subscription_available.id).update(

                    # per_bill_cost = per_bill_cost,
                    # per_receipt_cost = per_receipt_cost,
                    # per_cash_memo_cost = per_cash_memo_cost,

                    # per_digital_bill_cost = per_digital_bill_cost,
                    # per_digital_receipt_cost = per_digital_receipt_cost,
                    # per_digital_cash_memo_cost = per_digital_cash_memo_cost,

                    total_amount_avilable = total_amount,
                    gst_amount = subscription_object.gst_amount,

                )
                try:
                    last_id = recharge_history.objects.filter().last()
                    invoice_no = 'GB' + str(last_id.id+1)
                except:
                    invoice_no = 'GB' + str(1)
                recharge_history.objects.create(
                    
                    subscription_plan_id = subscription_object.id,
                    subscription_name = subscription_object.add_on_name,
                    merchant_id = merchant_object,
                    business_ids = business_id,

                    # per_bill_cost = per_bill_cost,
                    # per_receipt_cost = per_receipt_cost,
                    # per_cash_memo_cost = per_cash_memo_cost,

                    # per_digital_bill_cost = per_digital_bill_cost,
                    # per_digital_receipt_cost = per_digital_receipt_cost,
                    # per_digital_cash_memo_cost = per_digital_cash_memo_cost,

                    cost = subscription_object.actual_final_amount,

                    is_add_on_plan = True,

                    transaction_id = txnid,
                    payu_transaction_id = mihpayid,
                    gst_amount = subscription_object.gst_amount,
                    invoice_no = invoice_no,
                    merchant_business_id = merchant_business_id.id

                )

                if subscription:
                    reacharge_bill = recharge_history.objects.filter(merchant_id= merchant_object).last()

                    recharge_bill_url = "http://157.230.228.250/my-subscription-bill/" + str(reacharge_bill.id) + "/"
                     

                    s = pyshorteners.Shortener()

                    short_url = s.tinyurl.short(recharge_bill_url)


                    merchant_email = GreenBillUser.objects.get(mobile_no= request.user).m_email
                    subject = 'Thank You For Buying Promotional Subscription Plan'
                    message = f' Dear Merchant, \n\n Thank You for your Purchase!!! \n\n Your Green Bill for your recent purchase updated in your Merchant Portal. \n\nYou can view your invoice on your Green Bill Merchant App or Merchant Web Portal.\n Best Regards,\n\n Green Bill Team.' '\n\n Invoice Url: ' + str(recharge_bill_url)
                    email_from = settings.EMAIL_HOST_USER
                   
                    recipient_list = [merchant_email,]
                    
                    send_res = EmailMessage( subject, message, email_from, recipient_list)

                    response = send_res.send()
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
    merchant_subscriptions_key = merchant_subscriptions_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(merchant_subscriptions_key.key, 'utf-8'))
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
    # tr
    print("In func")
    try:
        logo = generalSetting.objects.get(id=1) 
        owner_logo = logo.o_digital_signature
    except:
        owner_logo = '' 
    bill_details = recharge_history.objects.get(id=id)

    users_cost = 0
    final_total = 0
    gst = ''
    subtotal = ''
    igst = ''
    number_of_users = ''
    try:
        all_business = MerchantProfile.objects.get(id=bill_details.business_ids)
        merchant_state = all_business.m_state
        merchant_city = all_business.m_city
        merchant_area = all_business.m_area
        merchant_pincode = all_business.m_pin_code
        merchant_business_name = all_business.m_business_name
        merchant_mobile_no = all_business.m_user
        gstin_number = all_business.m_gstin
        merchant_address = all_business.m_billing_address
        merchant_bill_mobile_no = all_business.m_billing_phone
        merchant_bill_name = all_business.m_business_name_for_billing

        
    except:
        merchant_state = ''
        merchant_city = ''
        merchant_area = ''
        merchant_pincode = ''
        merchant_business_name = ''
        merchant_mobile_no = ''
        gstin_number = ''
        merchant_address = ''
        merchant_bill_mobile_no = ''
        merchant_bill_name = ''

    # print("*********************************************")
    # print(bill_details.is_transactional_sms_plan,bill_details.is_subscription_plan,bill_details.is_promotional_sms_plan)
    if bill_details.is_transactional_sms_plan == True:
        subscription_plan = transactional_subscription_plan_model.objects.filter(id=bill_details.subscription_plan_id)

        for subscription in subscription_plan:

            if bill_details.mode == "cashwithoutbill":
                gst = float(subscription.gst_amount)/2
                igst = subscription.gst_amount
                final_total = bill_details.cost 
                recharge_amount = bill_details.cost
                subtotal = float(final_total) 

                plan_Subtotal = float(users_cost) + float(recharge_amount)

                amount_without_float, amount_round_off = divmod(final_total, 1)

                subscription.current_plan = 3
            else:

                gst = float(subscription.gst_amount)/2
                igst = subscription.gst_amount
                final_total = bill_details.cost 
                recharge_amount = bill_details.cost
                subtotal = float(final_total) - float(subscription.gst_amount)

                plan_Subtotal = float(users_cost) + float(recharge_amount)

                amount_without_float, amount_round_off = divmod(final_total, 1)

                subscription.current_plan = 3
            # print("*********************************************")
            # print(final_total,amount_without_float,amount_round_off)

    if bill_details.is_subscription_plan == True:
        
        subscription_plan = subscription_plan_details.objects.filter(id=bill_details.subscription_plan_id)
        # print("^^^^^^^^^^^^^^^^^^^^^^^^^")
        # print(subscription_plan)
        number_of_users = bill_details.no_of_users

        gst_amount = bill_details.gst_amount

        recharge_amount = bill_details.cost

        subscription_cost_for_user = subscription_plan[0].cost_for_users

        valid_for_month = bill_details.valid_for_month

        bill_details.sgst = float(gst_amount)/2
        
        for subscription in subscription_plan:

            if bill_details.mode == "cashwithoutbill":
                users_cost = float(number_of_users) * float(valid_for_month) * float(subscription.cost_for_users)
                final_total = float(users_cost) + float(recharge_amount) 
                plan_Subtotal = float(users_cost) + float(recharge_amount)

                amount_without_float, amount_round_off = divmod(final_total, 1)
                
                subscription.current_plan = 1
 
            else:

                users_cost = float(number_of_users) * float(valid_for_month) * float(subscription.cost_for_users)
                final_total = float(users_cost) + float(recharge_amount) + float(gst_amount)
                plan_Subtotal = float(users_cost) + float(recharge_amount)

                amount_without_float, amount_round_off = divmod(final_total, 1)
                
                subscription.current_plan = 1
            # print("*********************************************")
            # print(final_total,amount_without_float,amount_round_off)

    if bill_details.is_promotional_sms_plan == True:
        subscription_plan = promotional_subscription_plan_model.objects.filter(id=bill_details.subscription_plan_id)
        for subscription in subscription_plan:

            if bill_details.mode == "cashwithoutbill":
                gst = float(subscription.gst_amount)/2
                igst = subscription.gst_amount
                final_total = bill_details.cost 
                recharge_amount = bill_details.cost
                subtotal = float(final_total) 

                plan_Subtotal = float(users_cost) + float(recharge_amount)

                amount_without_float, amount_round_off = divmod(final_total, 1)
                subscription.current_plan = 2
            else:
                gst = float(subscription.gst_amount)/2
                igst = subscription.gst_amount
                final_total = bill_details.cost 
                recharge_amount = bill_details.cost
                subtotal = float(final_total) - float(subscription.gst_amount)

                plan_Subtotal = float(users_cost) + float(recharge_amount)

                amount_without_float, amount_round_off = divmod(final_total, 1)
                subscription.current_plan = 2
            # print("*********************************************")
            # print(final_total,amount_without_float,amount_round_off)

    

    if bill_details.is_add_on_plan == True:
        subscription_plan = add_on_plan_model.objects.filter(id=bill_details.subscription_plan_id)
        for subscription in subscription_plan:

            if bill_details.mode == "cashwithoutbill":
                if bill_details.gst_amount:
                    gst = float(bill_details.gst_amount)/2
                    igst = bill_details.gst_amount
                    final_total = bill_details.cost 
                    subtotal = float(final_total) + float(bill_details.gst_amount)

                recharge_amount = bill_details.cost

                try:
                    plan_Subtotal = float(users_cost) + float(recharge_amount)
                except:
                    plan_Subtotal = ""
                    
                   
                    amount_without_float, amount_round_off = divmod(final_total, 1)
                    subscription.current_plan = 4
            else:
                if bill_details.gst_amount:
                    gst = float(bill_details.gst_amount)/2
                    igst = bill_details.gst_amount
                    final_total = bill_details.cost 
                    subtotal = float(final_total) 

                recharge_amount = bill_details.cost

                try:
                    plan_Subtotal = float(users_cost) + float(recharge_amount)
                except:
                    plan_Subtotal = ""
                    
                   
                    amount_without_float, amount_round_off = divmod(final_total, 1)
                    subscription.current_plan = 4

            # print("*********************************************")
            # print(final_total,amount_without_float,amount_round_off)
    tax_amount = bill_details.cost
    # total_gst = (int(tax_amount)/100)*18

    # total_amount = int(tax_amount)
    try:
        all_business = MerchantProfile.objects.get(id=bill_details.business_ids)
        merchant_state = all_business.m_state
        merchant_city = all_business.m_city
        merchant_area = all_business.m_area
        merchant_pincode = all_business.m_pin_code
        merchant_business_name = all_business.m_business_name
        merchant_mobile_no = all_business.m_user
        gstin_number = all_business.m_gstin
        merchant_address = all_business.m_billing_address
        merchant_bill_mobile_no = all_business.m_billing_phone
        merchant_bill_name = all_business.m_business_name_for_billing
    except:
        merchant_state = ''
        merchant_city = ''
        merchant_area = ''
        merchant_pincode = ''
        merchant_business_name = ''
        merchant_mobile_no = ''
        gstin_number = ''
        merchant_address = ''
        merchant_bill_mobile_no = ''
        merchant_bill_name = ''
    

    if merchant_state ==  "Maharashtra" or merchant_state == "maharashtra":

        instate = True
        outstate = False

    else:
        outstate = True
        instate = False

    # print(amount_round_off)
    
    try:
        plan_Subtotal = plan_Subtotal
        amount_without_float = amount_without_float
        amount_round_off = amount_round_off
    except:
        plan_Subtotal = 0
        amount_without_float = 0
        amount_round_off = 0

    context = {
                'bill_details' : bill_details,
                'merchant_state': merchant_state,
                'merchant_city': merchant_city,
                'merchant_area': merchant_area,
                'merchant_pincode': merchant_pincode,
                'subscription_plan' : subscription_plan, 
                'merchant_business_name' : merchant_business_name,
                'merchant_mobile_no' : merchant_mobile_no,
                'gstin_number' : gstin_number,
                'gst': gst,
                'mode':bill_details.mode,
                'igst': igst,
                'subtotal': subtotal,
                'users_cost': users_cost,
                'final_total': final_total,
                'plan_Subtotal': plan_Subtotal,
                'amount_without_float': amount_without_float,
                'amount_round_off': amount_round_off,
                'instate' : instate,
                'outstate' : outstate,
                'owner_logo' : owner_logo,
                'number_of_users':number_of_users,
                'subscription_cost_for_user':subscription_cost_for_user,
                'valid_for_month':valid_for_month,
                'merchant_address' : merchant_address,
                'merchant_bill_mobile_no' : merchant_bill_mobile_no,
                'merchant_bill_name' : merchant_bill_name,
                # 'total_gst' : total_gst,
                # 'total_amount' : total_amount,
     'business_logo':'http://157.230.228.250/media/green-bill-logo.jpg'}
    return render(request, "merchant/subscription/my-subscription-bill.html",context)
    # except:
    #     return render(request, 'page-404.html')