import sweetify
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff, is_owner
from users.models import Merchant_users, MerchantProfile, GreenBillUser
from .models import *
from django.http import HttpResponse, JsonResponse
from category_and_tags.models import business_category


import string
from role.models import role, userrole
from authentication.models import otp_validation
import random
from merchant_role.models import merchant_role, merchant_userrole
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import message, send_mail
from users.models import GreenBillUser, Merchant_users
from django.contrib import auth
from .forms import bulkMailSmsForm
from django.core.mail import send_mail, EmailMessage, BadHeaderError, EmailMultiAlternatives
from owner_notice_board.sendsms import *

from django.utils.html import strip_tags
from django.db.models import Q
import json
from datetime import date
import time
import datetime
from datetime import date
from merchant_software_apis.models import *
from petrol_pump_apis.models import SavePetrolPumpBill
from parking_lot_apis.models import SaveParkingLotBill
from dateutil import relativedelta

import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from django.contrib.auth import authenticate, login
from cryptography.fernet import Fernet
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
from django.template import loader

import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from payments.models import OwnerPaymentLinks

from referral_points.models import *

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def ads_below_bills(request):
    excludes = ['11', '12']

    today = datetime.date.today()  

    merchant_users_objects = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_users_objects.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_users_objects.merchant_user_id, m_active_account = 1)

    created_date = MerchantProfile.objects.get(m_user = merchant_users_objects.merchant_user_id, m_active_account = 1).date_joined

    total_transaction = 0

    total_transaction1 = CustomerBill.objects.filter(business_name = merchant_business_id, customer_added = False).count()

    total_transaction2 = MerchantBill.objects.filter(business_name = merchant_business_id).count()

    total_transaction3 = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id.id).count()

    total_transaction4 = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id.id).count()

    total_transaction = total_transaction1 + total_transaction2 + total_transaction3 + total_transaction4

    date_joined = merchant_business_id.date_joined

    current_date = date.today()

    current_date_new =  datetime.datetime.strptime(str(current_date), '%Y-%m-%d')

    date_joined_new =  datetime.datetime.strptime(str(date_joined.date()), '%Y-%m-%d')

    average_transaction = 0

    if date_joined_new.month == current_date_new.month:

        average_transaction = total_transaction

    else:

        diff = (current_date_new.year - date_joined_new.year) * 12 + (current_date_new.month - date_joined_new.month)

        if total_transaction != 0 and diff != 0:
            average_transaction = total_transaction/diff
        else:
            average_transaction = 0

    if request.method == "POST" and not request.POST.get("submit") == "1":
        ads_name = request.POST.get('ads_name')
        if not ads_name:
            ads_name = request.POST.get('ads_name1')

        redirect_url = request.POST.get('redirect_url')
        if not redirect_url:
            redirect_url = request.POST.get('redirect_url1')

        ads_type = request.POST.get('ads_type')
        if not ads_type:
            ads_type = request.POST.get('ads_type1')

        if ads_type == "green_bill":
            approval_status = "1"
        else:
            approval_status = "0"
            
        start_date = request.POST.get('start_date')

        end_date = request.POST.get('end_date')

        ads_for = request.POST.get('ads_for')

 

        ads_image = request.FILES.get('ads_image')

        if not ads_image:
            ads_image = request.FILES.get('ads_image1')

        ads_image2 = request.FILES.get('ads_image2')

        ads_image3 = request.FILES.get('ads_image3')

        ads_image4 = request.FILES.get('ads_image4')

        if ads_type == "self":
            result = ads_below_bill.objects.create(
                third_party_total_transaction = average_transaction, merchant = request.user, merchant_business_id = merchant_business_id, 
                ads_type = ads_type, ads_name = ads_name, redirect_url = redirect_url,
                ads_image = ads_image, status = approval_status, ads_image_two = ads_image2, ads_image_three = ads_image3, ads_image_four = ads_image4)

        elif ads_type == "green_bill":
            from_datetime_object = datetime.datetime.strptime(str(start_date), '%Y-%m-%d')
            to_datetime_object = datetime.datetime.strptime(str(end_date), '%Y-%m-%d')
            r = relativedelta.relativedelta(to_datetime_object, from_datetime_object)
            r.months
            if int(r.months) >= 3:
                result = ads_below_bill.objects.create(
                    third_party_total_transaction = average_transaction, merchant = request.user, merchant_business_id = merchant_business_id, 
                    ads_type = ads_type, start_date = start_date, end_date = end_date, status = approval_status)
                
            else:
                result = 0
        else:
            if PromotionsAmount.objects.all():
                data1 = PromotionsAmount.objects.latest('id')
                amount = data1.third_party_ads_belowbill_amount
            else:
                amount = 0

            print(amount,'----------------------------------------')

            if amount == 0 or amount == "0" or amount == "0.00" or amount == 0.00:
                result = ads_below_bill.objects.create(ads_below_bill_amount= '0.00',third_party_total_transaction = average_transaction, merchant = request.user, merchant_business_id = merchant_business_id, ads_type = ads_type, ads_name = ads_name, redirect_url = redirect_url, ads_image = ads_image, start_date = start_date, end_date = end_date, ads_for = ads_for, ads_image_two = ads_image2, ads_image_three = ads_image3, ads_image_four = ads_image4)
            else:
                result = ads_below_bill.objects.create(ads_below_bill_amount= amount,third_party_total_transaction = average_transaction, merchant = request.user, merchant_business_id = merchant_business_id, ads_type = ads_type, ads_name = ads_name, redirect_url = redirect_url, ads_image = ads_image, start_date = start_date, end_date = end_date, ads_for = ads_for, status = approval_status, ads_image_two = ads_image2, ads_image_three = ads_image3, ads_image_four = ads_image4)

        
        if result:
            space = ads_below_bill.objects.filter(merchant = request.user, merchant_business_id = merchant_business_id, ads_type='green_bill').last()
            from_date_data = ""
            to_date_data = ""
            create_access = True
            status = 0
            active_id = ""
            if space:
                expiry_date = space.end_date
                
                expiry_date_new =  datetime.datetime.strptime(str(expiry_date), '%Y-%m-%d')
                start_date_new =  datetime.datetime.strptime(str(space.start_date), '%Y-%m-%d')
                if current_date_new <= expiry_date_new and current_date_new >= start_date_new:
                    ads_below_bill.objects.filter(merchant = request.user, merchant_business_id = merchant_business_id).update(active_ads = False)
                    create_access = False
                    to_date_data = space.end_date
                    status = 1
                    active_id = int(space.id)

            third_party_status = ads_below_bill.objects.filter(merchant = request.user, merchant_business_id = merchant_business_id, ads_type='third_party', status = 1).last()

    
            


            sweetify.success(request, title="Success", icon='success', text='Ads created Successfully !!!', timer=1500)

        elif result == 0:
            sweetify.error(request, title="Error", icon='error', text="You can't give green bill space less than 3 months!!!", timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Failed to create Ads!!!', timer=1500)

    my_ads = ads_below_bill.objects.filter(merchant = merchant_object, merchant_business_id = merchant_business_id).order_by('-id')
    
    self_ads_count = ads_below_bill.objects.filter(merchant = merchant_object, merchant_business_id = merchant_business_id, ads_type='self').count()
    third_party_count = ads_below_bill.objects.filter(merchant = merchant_object, merchant_business_id = merchant_business_id, ads_type='third_party').count()
    green_bill_count = ads_below_bill.objects.filter(merchant = merchant_object, merchant_business_id = merchant_business_id, ads_type='green_bill').count()
    


    all_ads_count = ads_below_bill.objects.filter(merchant = merchant_object, merchant_business_id = merchant_business_id).count()
    waiting_count = ads_below_bill.objects.filter(merchant = merchant_object, merchant_business_id = merchant_business_id, status=0).count()
    approved_count = ads_below_bill.objects.filter(merchant = merchant_object, merchant_business_id = merchant_business_id, status=1).count()


    
    today = datetime.date.today()

    running_ads_start_date = ""
    running_ads_end_date = ""
    for ads in my_ads:
        if ads.end_date:
            enddate = datetime.datetime.strptime(ads.end_date, "%Y-%m-%d").date()
            
            if enddate >= today:
                ads.expire_status=True
        if ads.start_date:
            if ads.ads_type != "self":
                if not running_ads_start_date:
                    running_ads_start_date = ads.start_date
                if running_ads_start_date > ads.start_date:
                    running_ads_start_date = ads.start_date
        if ads.end_date:
            if ads.ads_type != "self":
                if not running_ads_end_date:
                    running_ads_end_date = ads.end_date
                if running_ads_end_date < ads.end_date:
                    running_ads_end_date = ads.end_date

    for ads in my_ads:
        ads.ads_id = int(ads.id)    
        if ads.start_date:
            datetime_object =  datetime.datetime.strptime(str(ads.start_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            ads.start_date = datetime_object
        if ads.end_date:
            datetime_object =  datetime.datetime.strptime(str(ads.end_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            ads.end_date = datetime_object

    today = datetime.date.today()  
    space = ads_below_bill.objects.filter(merchant = request.user, merchant_business_id = merchant_business_id, ads_type='green_bill').last()
    from_date_data = ""
    to_date_data = ""
    create_access = True
    status = 0
    active_id = ""
    if space:
        expiry_date_new =  datetime.datetime.strptime(str(space.end_date), '%Y-%m-%d')
        start_date_new =  datetime.datetime.strptime(str(space.start_date), '%Y-%m-%d')

        if current_date_new >= start_date_new and current_date_new <= expiry_date_new:   
            ads_below_bill.objects.filter(merchant = request.user, merchant_business_id = merchant_business_id).update(active_ads = False)
            create_access = False
            to_date_data = space.end_date
            status = 1
            active_id = int(space.id)

    third_party_status = ads_below_bill.objects.filter(merchant = request.user, merchant_business_id = merchant_business_id, ads_type='third_party', status = 1).last()
    if not space:
        if third_party_status:

            expiry_date_new =  datetime.datetime.strptime(str(third_party_status.end_date), '%Y-%m-%d')
            start_date_new =  datetime.datetime.strptime(str(third_party_status.start_date), '%Y-%m-%d')

            if current_date_new >= start_date_new and current_date_new <= expiry_date_new:            
                ads_active_list = ads_below_bill.objects.filter(merchant = request.user, merchant_business_id = merchant_business_id, active_ads = True, ads_type = "self")

                if ads_active_list:
                    ads_below_bill.objects.filter(id = ads_active_list[0].id).update(active_ads = False)
                create_access = False
                to_date_data = third_party_status.end_date
                status = 1
                active_id = int(third_party_status.id)



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

    surl = "http://157.230.228.250/third-party-purchased-success/"

    furl = "http://157.230.228.250/third-party-purchased-fail/"

    enc_key = Fernet.generate_key()
    fernet = Fernet(enc_key)
    password = request.session['password']
    encPassword = fernet.encrypt(password.encode())

    ads_below_bills_key = ads_below_bills_keys.objects.create(key = enc_key.decode("utf-8"))

    # if PromotionsAmount.objects.all():
    #     data = PromotionsAmount.objects.latest('id')
    #     amount = data.third_party_ads_belowbill_amount
    # else:
    #     amount = 0

    for ads in my_ads:
        if ads.ads_type == "third_party":

            amount = ads.ads_below_bill_amount

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

            hash_object = hashlib.sha256(b'randint(0,20)' + bytes(ads.id) + bytes(request.user.id) + bytes(random_str))

            txnid=hash_object.hexdigest()[0:20]

            hashh = ''
            posted['txnid']=txnid
            posted['key']=key

            productinfo = str("ads_name-"+ ads.ads_name)
            amount = str(amount)

            udf1 = str(ads.id) # subscription id

            udf2 = str(request.user.id) # user object

            udf3 = str(encPassword.decode("utf-8")) # encoded Password

            udf4 = str(ads_below_bills_key.id) # decode key id

            udf5 = ""

            udf6 = ""

            hashSequence = key + "|" + txnid + "|" + amount + "|" + productinfo + "|" + firstname + "|" + email + "|" + udf1 + "|" + udf2 + "|" + udf3 + "|" + udf4 + "|" + udf5 + "|" + udf6 + "|||||" + SALT

            hash_string = hashSequence.encode('utf-8')

            hashh = hashlib.sha512(hash_string).hexdigest().lower()

            ads.hashh = hashh
            ads.posted = posted
            ads.txnid = txnid
            ads.hash_string = hash_string
            ads.amount = amount
            ads.productinfo = productinfo
            ads.udf1 = udf1
            ads.udf2 = udf2
            ads.udf3 = udf3
            ads.udf4 = udf4
            ads.udf5 = udf5
            ads.udf6 = udf6

    action = PAYU_BASE_URL


    if not running_ads_end_date:
        running_ads_end_date =  datetime.datetime.today().strftime('%Y-%m-%d')

    if not running_ads_start_date:
        running_ads_start_date = datetime.datetime.today().strftime('%Y-%m-%d')

    context = {
        'all_ads_count': all_ads_count,
        'waiting_count': waiting_count,
        'approved_count': approved_count,
        'my_ads' : my_ads,
        'running_ads_start_date': running_ads_start_date,
        'running_ads_end_date': running_ads_end_date,
        'status': status,
        'from_date_data':from_date_data,
        'to_date_data': to_date_data,
        'create_access' : create_access,
        'active_id': active_id,
        "MERCHANT_KEY":key,
        "firstname" : firstname,
        "email" : email,
        "phone": phone,
        "surl": surl,
        "furl" : furl,
        "action": action,
        'self_ads_count':self_ads_count,
        'third_party_count':third_party_count,
        'green_bill_count':green_bill_count,
        'PromotionsNavclass': "active", 
        'ShowPromotionsNavclass': "show",
        'AdsBelowBillNavClass' : 'active'
    }

    return render(request, "merchant/promotions/ads-below-bill.html", context)



@csrf_exempt
def third_party_ads_payment_success(request):
    
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount= request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    udf1 = request.POST["udf1"] # subscription id
    ads_id = request.POST["udf1"]
    udf2 = request.POST["udf2"] # user id
    user_id = request.POST["udf2"] # user id
    udf3 = request.POST["udf3"] # encoded password
    udf4 = request.POST["udf4"] # decode key id
    udf5 = request.POST["udf5"] # plan type
    udf6 = request.POST["udf6"]


    mihpayid = request.POST["mihpayid"]

    # Decode Password
    ads_below_bills_key = ads_below_bills_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(ads_below_bills_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()


    # SALT = "HLysMjoK" # Test Salt
    SALT="7ViVXMy1" # Production Salt


    merchant_object = GreenBillUser.objects.get(id=user_id)

    retHashSeq = SALT + '|' + status + '|||||'+ udf6 +'|' + udf5 + '|' + udf4 + '|' + udf3 + '|' + udf2 +'|'+ udf1 + '|' + email + '|'+ firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

    hash_string = retHashSeq.encode('utf-8')
    
    hashh = hashlib.sha512(hash_string).hexdigest().lower()

    mobile_no = merchant_object.mobile_no
    
    request.session['mobile_no'] = mobile_no
    request.session['password'] = decPassword

    user = authenticate(mobile_no=request.session['mobile_no'], password=request.session['password'])
    login(request, user)

    if status == "success":

        if hashh == posted_hash:
            letters = string.ascii_letters
            digit = string.digits
            ads_status = ads_below_bill.objects.get(id = ads_id)

            random_string = str(ads_status.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
            
            ads_below_bill.objects.filter(id = ads_id).update(payment_done = True, payment_amount = amount, transaction_id = txnid, payu_transaction_id = mihpayid, payment_date = timezone.now(), status="1")

            PromotionsPaymentHistory.objects.create(merchant = request.user, merchant_business_id = ads_status.merchant_business_id, ads_id = ads_status.id, payment_done = True, payment_amount = amount, transaction_id = txnid, payu_transaction_id = mihpayid, payment_date = timezone.now())

            OwnerPaymentLinks.objects.create(mobile_no = request.user, name = ads_status.merchant_business_id.m_business_name, 
                email = request.user.email, amount = amount, payment_done = True, payment_url = random_string, transaction_id = txnid, 
                payu_transaction_id = mihpayid, payment_mode = "PayU", promotions = True, payment_date = timezone.now(), description = "Third Party Ads")
            
            if ads_status:
                sweetify.success(request, title="Success", icon='success', text='Payment Successfully Completed.', timer=1500)
                return redirect(ads_below_bills)
            else:
                sweetify.success(request, title="Oops...", icon='error', text='Failed.', timer=1500)
                return redirect(ads_below_bills)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Failed.', timer=1500)
            return redirect(ads_below_bills)
    else:
        sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)
        return redirect(ads_below_bills)

@csrf_exempt
def third_party_ads_payment_fail(request):
    user_id = request.POST["udf2"] # user id
    udf3 = request.POST["udf3"] # encoded password
    udf4 = request.POST["udf4"] # decode key id

    # Decode Password
    ads_below_bills_key = ads_below_bills_keys.objects.get(id = int(udf4))
    fernet = Fernet(bytes(ads_below_bills_key.key, 'utf-8'))
    decPassword = fernet.decrypt(bytes(udf3, 'utf-8')).decode()

    user_object =  GreenBillUser.objects.get(id=user_id)

    mobile_no = user_object.mobile_no
    
    request.session['mobile_no'] = mobile_no
    request.session['password'] = decPassword

    user = authenticate(mobile_no=request.session['mobile_no'], password=request.session['password'])
    login(request, user)

    sweetify.success(request, title="Oops...", icon='error', text='Failed.', timer=1500)

    return redirect(ads_below_bills)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def get_ads_details_by_id(request):
    if request.method == "POST":
        id = request.POST['id']

        ads_object = ads_below_bill.objects.get(id= id)

        store_name = ads_object.business_name_value

        business_list = []

        if store_name:
            business_list = list(store_name.split(",")) 
        else:
            business_list = ""

        try:
            ads_image_url = ads_object.ads_image.url
        except:
            ads_image_url = ""

        data = {
            'id': ads_object.id,
            'ads_name': ads_object.ads_name,
            'ads_type': ads_object.ads_type,
            'ads_image': ads_image_url,
            'ads_name': ads_object.ads_name,
            'start_date': ads_object.start_date,
            'end_date': ads_object.end_date,
            'default_ads': ads_object.default_ads,
            'redirect_url': ads_object.redirect_url,
            'business_list': business_list
        }

        return JsonResponse({'status': "success", 'data' : data})
    else:
        return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def delete_ads_by_id(request, id):
    if request.method == "POST":
        data = ads_below_bill.objects.get(id= id).delete()
        sweetify.success(request, title="success", icon='success', text='Ads deleted Successfully !!!', timer=1500)
        return redirect(ads_below_bills)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Ads!!!', timer=1500)
        return redirect(ads_below_bills)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def edit_ads_by_id(request):
    if request.method == "POST":
        id = request.POST['ads_id']
        ads_name = request.POST['edit_ads_name']
        redirect_url = request.POST['edit_redirect_url']
        ads_type = request.POST['edit_ads_type']
        start_date = request.POST['edit_start_date']
        end_date = request.POST['edit_end_date']

        try:
            default_ads = request.POST['edit_default_ads']
        except:
            default_ads = ""

        if default_ads == "default_ads":
            default_ads_status = True
        else:
            default_ads_status = False

        business_name_value = request.POST['edit_business_name_value']

        try:
            ads_image = request.FILES['edit_ads_image']
        except:
            ads_image = ""

        if ads_image:
            if ads_type == "green_bill" :
                result = ads_below_bill.objects.filter(id = id).update(start_date = start_date, end_date = end_date, ads_type = ads_type, ads_name = ads_name, redirect_url = "", default_ads = default_ads_status, business_name_value = business_name_value, ads_image = "")
            else:
                result = ads_below_bill.objects.filter(id = id).update(start_date = start_date, end_date = end_date, ads_type = ads_type, ads_name = ads_name, redirect_url = redirect_url, default_ads = default_ads_status, business_name_value = business_name_value)

                ads_object = ads_below_bill.objects.get(id = id)

                ads_object.ads_image = ads_image

                ads_object.save()
                
        else:
            if ads_type == "green_bill":
                result = ads_below_bill.objects.filter(id = id).update(start_date = start_date, end_date = end_date, ads_type = ads_type, ads_name = ads_name, redirect_url = "", default_ads = default_ads_status, business_name_value = business_name_value, ads_image = "")
            else:
                result = ads_below_bill.objects.filter(id = id).update(start_date = start_date, end_date = end_date, ads_type = ads_type, ads_name = ads_name, redirect_url = redirect_url, default_ads = default_ads_status, business_name_value = business_name_value)
        if result:
            sweetify.success(request, title="Success", icon='success', text='Ads Updated Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Failed to update Ads!!!', timer=1500)
    else:
        sweetify.error(request, title="Error", icon='error', text='Something went wrong !', timer=1500)

    return redirect(ads_below_bills)


@login_required(login_url="/login/")
@user_passes_test(is_owner)
def get_all_ads_below_bill(request):

    all_ads = ads_below_bill.objects.all().order_by('-id')

    all_ads1 = ads_below_bill.objects.filter(ads_type = "self").order_by('-id') 

    all_ads_count = ads_below_bill.objects.filter(ads_type="self").count()

    waiting_count = ads_below_bill.objects.filter(ads_type="self", status=0).count()

    approved_count = ads_below_bill.objects.filter(ads_type="self", status=1).count()

    today = datetime.date.today()
    for ads in all_ads:
        if ads.end_date:
            enddate = datetime.datetime.strptime(ads.end_date, "%Y-%m-%d").date()
            if enddate >= today:
                ads.expire_status=True

    for ads in all_ads:    
        if ads.start_date:
            datetime_object =  datetime.datetime.strptime(str(ads.start_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            ads.start_date = datetime_object
        if ads.end_date:
            datetime_object =  datetime.datetime.strptime(str(ads.end_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            ads.end_date = datetime_object

    for ads in all_ads:

        business_list = []

        if ads.business_name_value:
            business_list = list(ads.business_name_value.split(",")) 
        else:
            business_list = ""

        business2 = []
    
        if business_list:

            for x in range(len(business_list)):

                try:
                    business1 = MerchantProfile.objects.get(id=business_list[x])

                    business2.append(business1.m_business_name)


                except:
                    pass

        business3 = ', '.join(map(str, business2))

        ads.business_name = business3

    context = {
        'all_ads_count': all_ads_count,
        'waiting_count': waiting_count,
        'approved_count': approved_count,
        'all_ads' : all_ads,
        'all_ads1': all_ads1,
        'PromotionNavclass': 'active',
        "PromotionCollapseShow": "show",
        "ApproveDisapproveAdsNavclass": "active"
    }

    return render(request, "super_admin/promotions/ads-below-bill-list.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner)
def approve_ads_by_id(request, id):

    if request.method == "POST":
        data = ads_below_bill.objects.filter(id = id).update(status = "1")
        sweetify.success(request, title="success", icon='success', text='Ads Approved Successfully !!!', timer=1500)
        return redirect(ads_below_bills)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Approved Ads!!!', timer=1500)
        return redirect(ads_below_bills)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def disapprove_ads_by_id(request):
    if request.method == "POST":
        id = request.POST["disapprove_ads_id"]
        reason = request.POST["reason"] 
        data = ads_below_bill.objects.filter(id = id).update(status = "2", disapproved_reason = reason)
        sweetify.success(request, title="success", icon='success', text='Ads Disapproved Successfully !!!', timer=1500)
        return redirect(ads_below_bills)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Disapproved Ads!!!', timer=1500)
        return redirect(ads_below_bills)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def set_active_ads(request):
    if request.method == "POST":

        id = request.POST["active_ads"]

        mer_user_id = Merchant_users.objects.get(user_id=request.user)

        merchant_object = mer_user_id.merchant_user_id

        result1 = ads_below_bill.objects.filter(merchant = merchant_object).update(active_ads = False)

        result2 = ads_below_bill.objects.filter(id = id, status="1").update(active_ads = True)

        if result1 and result2:
            sweetify.success(request, title="success", icon='success', text='Ads Set Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="error", icon='error', text='Failed to Set Ads!!!', timer=1500)
            return redirect(ads_below_bills)

        return redirect(ads_below_bills)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Set Ads!!!', timer=1500)
        return redirect(ads_below_bills)


# @login_required(login_url="/login/")
# @user_passes_test(is_owner)
# def ads_for_merchant(request):

#     if request.method == "POST":
#         ads_name = request.POST['ads_name']
#         redirect_url = request.POST['redirect_url']
#         ads_type = request.POST['ads_type']

#         # merchants_name_value = request.POST['merchants_name_value']
#         business_name_value = request.POST['business_name_value']

#         business_category_value = request.POST['business_category_value']

#         try:
#             ads_image = request.FILES['ads_image']
#         except:
#             ads_image = ""

#         result = ads_for_merchants.objects.create(ads_type = ads_type, ads_name = ads_name, redirect_url = redirect_url, business_name_value = business_name_value, business_category_value = business_category_value, ads_image = ads_image)

#         if result:
#             sweetify.success(request, title="Success", icon='success', text='Ads created Successfully !!!', timer=1500)
#         else:
#             sweetify.error(request, title="Error", icon='error', text='Failed to create Ads!!!', timer=1500)

#     merchant_ads = ads_for_merchants.objects.all().order_by('-id')

#     for ads in merchant_ads:

#         if ads.business_name_value:
#             business_list1 = list(ads.business_name_value.split(","))
#             business_list2 = []

#             if business_list1:
#                 for x in range(len(business_list1)):
#                     try:
#                         business_object = MerchantProfile.objects.get(id=business_list1[x])
#                         business_list2.append(business_object.m_business_name)
#                     except:
#                         pass

#             business_list3 = ', '.join(map(str, business_list2))

#             ads.business_name = business_list3

#         if ads.business_category_value:
#             business_category1 = list(ads.business_category_value.split(","))
#             business_category2 = []
#             business_category3 = None

#             if business_category1:
#                 for x in range(len(business_category1)):
#                     try:
#                         category_object = business_category.objects.get(id=business_category1[x])
#                         business_category2.append(category_object.business_category_name)
#                     except:
#                         pass

#             business_category3 = ', '.join(map(str, business_category2))

#             ads.business_category = business_category3

#     # print(merchant_ads)

#     # all_ads = ads_below_bill.objects.filter(ads_type = "green_bill", active_ads = True)

#     # merchant_list = []

#     # for ads in all_ads:
#     #     merchant_list.append(ads)

#     merchant_list = GreenBillUser.objects.filter(is_merchant = True)

#     # print(merchant_list)

#     business_list = MerchantProfile.objects.all()

#     business_category_list = business_category.objects.all()
    
#     merchant_business_list = ""

#     context = {
#         'merchant_business_list' : merchant_business_list,
#         'business_category_list' : business_category_list,
#         'merchant_ads' : merchant_ads,
#         'merchant_list':merchant_list,
#         'business_list': business_list,
#         'PromotionNavclass': 'active',
#         "PromotionCollapseShow": "show",
#         "AdsBelowAriaExpanded" : "true",
#         "AdsBelowSubCollpseShow" : "show",
#         "AdsForMerchantNavclass": "active"
#     }

#     return render(request, "super_admin/promotions/ads-for-merchants.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def add_payment_for_third_party_ads(request):
    try:
        if request.method == "POST":        
            third_party_add_id = request.POST.get('third_party_add')
            payment_mode = 'Cash'
            payment_amount = request.POST.get('payment_amount')
            try:
                ads_obj = ads_below_bill.objects.filter(id=third_party_add_id).update(payment_done=True, payment_date= datetime.datetime.now(), payment_amount=payment_amount, status = "1")
                sweetify.success(request, title="success", icon='success', text='Ads Approved Successfully !!!', timer=1500)
                return redirect(ads_for_merchant)
            except:
                sweetify.error(request, title="Error", icon='error', text='Something went wrong !!!', timer=1500)
                return redirect(ads_for_merchant)
        else:
            sweetify.error(request, title="Error", icon='error', text='Something went wrong !!!', timer=1500)
            return redirect(ads_for_merchant)
    except:
        sweetify.error(request, title="Error", icon='error', text='Something went wrong !!!', timer=1500)
        return redirect(ads_for_merchant)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def ads_for_merchant(request):

    my_ads = ads_below_bill.objects.all().order_by('-id')
    all_ads_count = ads_below_bill.objects.filter(ads_type="third_party").count()
    waiting_count = ads_below_bill.objects.filter(ads_type="third_party", approved_status=0).count()
    approved_count = ads_below_bill.objects.filter(ads_type="third_party", approved_status=1).count()
    
    today = datetime.date.today()
    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        amount = data.third_party_ads_belowbill_amount
    else:
        amount = 0
    for ads in my_ads:
        if ads.end_date:
            enddate = datetime.datetime.strptime(ads.end_date, "%Y-%m-%d").date()
            if enddate >= today:
                ads.expire_status=True

        if ads.third_party_total_transaction:
            
            ads.total_amount = float(amount) * float(ads.third_party_total_transaction)
        



    # for ads in merchant_ads:
        # if ads.days:
        #     temp_days = ""
        #     temp_days = ads.days.replace("[", "")
        #     temp_days = temp_days.replace("]", "")
        #     temp_days = temp_days.replace("'", "")
        #     ads.days = temp_days
    for ads in my_ads:    
        if ads.start_date:
            datetime_object =  datetime.datetime.strptime(str(ads.start_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            ads.start_date = datetime_object
        if ads.end_date:
            datetime_object =  datetime.datetime.strptime(str(ads.end_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            ads.end_date = datetime_object
    # for ads in merchant_ads:    
    #     if ads.start_date:
    #         datetime_object =  datetime.datetime.strptime(str(ads.start_date), '%Y-%m-%d').strftime('%d-%m-%Y')
    #         ads.start_date = datetime_object
    #     if ads.end_date:
    #         datetime_object =  datetime.datetime.strptime(str(ads.end_date), '%Y-%m-%d').strftime('%d-%m-%Y')
    #         ads.end_date = datetime_object
    for ads in my_ads:

        if ads.business_name_value:
            business_list1 = list(ads.business_name_value.split(","))
            business_list2 = []

            if business_list1:
                for x in range(len(business_list1)):
                    try:
                        business_object = MerchantProfile.objects.get(id=business_list1[x])
                        business_list2.append(business_object.m_business_name)
                    except:
                        pass

            business_list3 = ', '.join(map(str, business_list2))

            ads.business_name = business_list3

    context = {

        
        'all_ads' : my_ads,
        'all_ads_count': all_ads_count,
        'waiting_count': waiting_count,
        'approved_count': approved_count,
        'PromotionNavclass': 'active',
        "PromotionCollapseShow": "show",
        "AdsBelowAriaExpanded" : "true",
        "AdsBelowSubCollpseShow" : "show",
        "AdsForMerchantNavclass": "active"
    }

    return render(request, "super_admin/promotions/ads-for-merchants.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def approve_third_party_ads_by_id(request, id):

    if request.method == "POST":
        data = ads_below_bill.objects.filter(id = id).update(status = "1")
        sweetify.success(request, title="success", icon='success', text='Ads Approved Successfully !!!', timer=1500)
        return redirect(ads_for_merchant)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Approved Ads!!!', timer=1500)
        return redirect(ads_for_merchant)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def approve_third_party_ads(request, id):

    if request.method == "POST":
        try:
            ads_amount = ads_below_bill.objects.get(id=id)
        except:
            ads_amount = 0

        if ads_amount:
            # print(ads_amount,'--------------------',)
            if ads_amount.ads_below_bill_amount == '0.00' or ads_amount.ads_below_bill_amount == 0.00 or ads_amount.ads_below_bill_amount == 0 or ads_amount.ads_below_bill_amount == '0':
                data = ads_below_bill.objects.filter(id = id).update(approved_status = "1", active_ads = True)
                sweetify.success(request, title="success", icon='success', text='Ads Approved Successfully !!!', timer=1500)
                return redirect(ads_for_merchant)
            else:
                data = ads_below_bill.objects.filter(id = id).update(approved_status = "1")
                sweetify.success(request, title="success", icon='success', text='Ads Approved Successfully !!!', timer=1500)
                return redirect(ads_for_merchant)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Approved Ads!!!', timer=1500)
        return redirect(ads_for_merchant)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def disapprove_third_party_ads_by_id(request):
    if request.method == "POST":
        id = request.POST["disapprove_ads_id"]
        reason = request.POST["reason"] 
        data = ads_below_bill.objects.filter(id = id).update(approved_status = "2", disapproved_reason = reason)
        sweetify.success(request, title="success", icon='success', text='Ads Disapproved Successfully !!!', timer=1500)
        return redirect(ads_for_merchant)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Disapproved Ads!!!', timer=1500)
        return redirect(ads_for_merchant)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def add_third_party_amount_by_id(request):
    if request.method == "POST":
        id = request.POST["third_party_id"]
        third_party_amount = request.POST["third_party_amount"] 
        data_status = ads_below_bill.objects.filter(id = id).update(third_party_amount = third_party_amount)
        sweetify.success(request, title="success", icon='success', text='Amount Added Successfully !!!', timer=1500)
        return redirect(ads_for_merchant)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Add Amount!!!', timer=1500)
        return redirect(ads_for_merchant)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def get_merchant_ads_details_by_id(request):
    if request.method == "POST":

        id = request.POST['id']

        ads_object = ads_for_merchants.objects.get(id= id)

        # merchant_name = ads_object.merchants_name_value

        # merchant_list = []

        # if merchant_name:
        #     merchant_list = list(merchant_name.split(",")) 
        # else:
        #     merchant_list = ""


        business_category = ads_object.business_category_value

        category_list = []

        if business_category:
            category_list = list(business_category.split(",")) 
        else:
            category_list = ""


        business = ads_object.business_name_value

        business_list = []

        if business:
            business_list = list(business.split(",")) 
        else:
            business_list = ""

        try:
            ads_image_url = ads_object.ads_image.url
        except:
            ads_image_url = ""

        data = {
            'id': ads_object.id,
            'ads_name': ads_object.ads_name,
            'ads_type': ads_object.ads_type,
            'ads_image': ads_image_url,
            'redirect_url': ads_object.redirect_url,
            # 'merchant_list': merchant_list,
            'category_list': category_list,
            'business_list': business_list,
            'schedule': ads_object.schedule,
            'start_date': ads_object.start_date,
            'end_date': ads_object.end_date,
        }

        return JsonResponse({'status': "success", 'data' : data})
    else:
        return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})


@login_required(login_url="/login/")
@user_passes_test(is_owner)
def edit_merchant_ads_by_id(request):
    if request.method == "POST":
        id = request.POST['ads_id']
        ads_name = request.POST['edit_ads_name']
        redirect_url = request.POST['edit_redirect_url']
        ads_type = request.POST['edit_ads_type']

        try:
            edit_schedule = request.POST['edit_schedule']
        except:
            edit_schedule = ""

        if edit_schedule == "True":
            start_date = request.POST['edit_start_date']
            end_date = request.POST['edit_end_date']
            schedule = True
        else:
            start_date = ""
            end_date = ""
            schedule = False

        # merchants_name_value = request.POST['edit_merchants_name_value']
        business_name_value = request.POST['edit_business_name_value']
        business_category_value = request.POST['edit_business_category_value']

        try:
            ads_image = request.FILES['edit_ads_image']
        except:
            ads_image = ""

        if ads_image:

            result = ads_for_merchants.objects.filter(id = id).update(ads_type = ads_type, ads_name = ads_name, redirect_url = redirect_url, business_name_value = business_name_value, business_category_value = business_category_value, schedule = schedule, start_date = start_date, end_date = end_date)
            ads_object = ads_for_merchants.objects.get(id = id)

            ads_object.ads_image = ads_image

            ads_object.save()
                
        else:
            result = ads_for_merchants.objects.filter(id = id).update(ads_type = ads_type, ads_name = ads_name, redirect_url = redirect_url, business_name_value = business_name_value, business_category_value = business_category_value, schedule = schedule, start_date = start_date, end_date = end_date)

        if result:
            sweetify.success(request, title="Success", icon='success', text='Ads Updated Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Failed to update Ads!!!', timer=1500)
    else:
        sweetify.error(request, title="Error", icon='error', text='Something went wrong !', timer=1500)

    return redirect(ads_for_merchant)


@login_required(login_url="/login/")
@user_passes_test(is_owner)
def delete_merchant_ads_by_id(request, id):
    if request.method == "POST":
        data = ads_for_merchants.objects.get(id= id).delete()
        sweetify.success(request, title="success", icon='success', text='Ads deleted Successfully !!!', timer=1500)
        return redirect(ads_for_merchant)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Ads!!!', timer=1500)
        return redirect(ads_for_merchant)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def set_merchant_active_ads(request):

    if request.method == "POST":

        id = request.POST["active_ads"]

        result1 = ads_for_merchants.objects.filter().update(active_ads = False)

        result2 = ads_for_merchants.objects.filter(id = id).update(active_ads = True)

        if result1 and result2:
            sweetify.success(request, title="success", icon='success', text='Ads Set Successfully !!!', timer=1500)

        else:
            sweetify.error(request, title="error", icon='error', text='Failed to Set Ads!!!', timer=1500)
            return redirect(ads_for_merchant)

        return redirect(ads_for_merchant)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Set Ads!!!', timer=1500)
        return redirect(ads_for_merchant)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def ads_for_green_bill(request):
    merchant_spaces = ads_below_bill.objects.filter(ads_type='green_bill').order_by('-id')
    today = datetime.date.today()
    current_date = date.today()
    current_date_new =  datetime.datetime.strptime(str(current_date), '%Y-%m-%d')
    excludes = ['11', '12']
    if PromotionsAmount.objects.all():
        data = PromotionsAmount.objects.latest('id')
        amount = data.green_bill_ads_belowbill_amount
    else:
        amount = 0

    merchant_business_list = []

    business_category_list_new = []

    get_start_date = ""
    get_end_date = ""
    used_status = ""

    for space in merchant_spaces:

        expiry_date = space.end_date
        
        expiry_date_new =  datetime.datetime.strptime(str(expiry_date), '%Y-%m-%d')
        start_date_new =  datetime.datetime.strptime(str(space.start_date), '%Y-%m-%d')

        if current_date_new <= expiry_date_new and current_date_new >= start_date_new:

            space.usable = True

            if space.merchant_business_id.id != '11' or space.merchant_business_id.id != '12': 

                business_id = MerchantProfile.objects.get(id = space.merchant_business_id.id)

                startswith = str(business_id.id) + ','
                endswith = ','+ str(business_id.id)
                contains = ','+ str(business_id.id) + ','
                exact = str(business_id.id)

                reserved_businesses = ads_for_green_bills.objects.filter(
                    Q(business_name_value__startswith = startswith) | 
                    Q(business_name_value__endswith = endswith) | 
                    Q(business_name_value__contains = contains) | 
                    Q(business_name_value__exact = exact)
                )

                if not reserved_businesses:
                    merchant_business_list.append({
                        'business_id': business_id.id,
                        'business_name': business_id.m_business_name,
                        'branch_name': business_id.m_area,
                    })
                    try:
                        b_c_obj = business_category.objects.get(business_category_name=business_id.m_business_category)
                        business_category_list_new.append({
                            'id': b_c_obj.id,
                            'business_category_name': b_c_obj.business_category_name,
                            })
                    except:
                        pass


                if not used_status:
                    check_end_date = space.end_date

                if check_end_date == space.end_date:
                    get_end_date = space.end_date
                    get_start_date = space.start_date
                    used_status = 1

                elif get_end_date <= space.end_date:
                    get_end_date = space.end_date
                    get_start_date = space.start_date
                    used_status = 0

        if space.start_date:
            space.start_date =  datetime.datetime.strptime(str(space.start_date), '%Y-%m-%d').strftime('%d-%m-%Y')

        if space.end_date:
            space.end_date =  datetime.datetime.strptime(str(space.end_date), '%Y-%m-%d').strftime('%d-%m-%Y')

        if space.third_party_total_transaction:
            space.total_amount = float(amount) * float(space.third_party_total_transaction)

        

    
    business_category_list = business_category.objects.filter(id__in = excludes)

    if request.method == "POST":
        ads_name = request.POST['ads_name']
        redirect_url = request.POST['redirect_url']
        ads_type = request.POST['ads_type']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        business_name_value = request.POST['business_name_value']

        business_category_value = request.POST['business_category_value']


        try:
            ads_image = request.FILES['ads_image']
        except:
            ads_image = ""

        ads_image2 = request.FILES.get('ads_image2')

        ads_image3 = request.FILES.get('ads_image3')

        ads_image4 = request.FILES.get('ads_image4')

        result = ads_for_green_bills.objects.create(ads_name = ads_name, redirect_url = redirect_url, ads_type = ads_type, business_name_value = business_name_value, business_category_value = business_category_value, ads_image = ads_image, start_date = start_date, end_date = end_date, ads_image_two = ads_image2, ads_image_three = ads_image3, ads_image_four = ads_image4)

        if result:
            sweetify.success(request, title="Success", icon='success', text='Ads created Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Failed to create Ads!!!', timer=1500)

    my_ads = ads_for_green_bills.objects.all().order_by("-id")


    total_count = ads_for_green_bills.objects.all().count()
    
    for ads in my_ads:

        if ads.end_date:

            enddate = datetime.datetime.strptime(ads.end_date, "%Y-%m-%d").date()
            
            if enddate >= today:
                ads.expire_status=True

        if ads.start_date:
            datetime_object =  datetime.datetime.strptime(str(ads.start_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            ads.start_date = datetime_object
        if ads.end_date:
            datetime_object =  datetime.datetime.strptime(str(ads.end_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            ads.end_date = datetime_object

        if ads.business_name_value:
            business_list1 = list(ads.business_name_value.split(","))
            business_list2 = []

            if business_list1:
                for x in range(len(business_list1)):
                    try:
                        business_object = MerchantProfile.objects.get(id=business_list1[x])
                        business_list2.append(business_object.m_business_name)
                    except:
                        pass

            business_list3 = ', '.join(map(str, business_list2))

            ads.business_name = business_list3

        if ads.business_category_value:
            business_category1 = list(ads.business_category_value.split(","))
            business_category2 = []
            business_category3 = None

            if business_category1:
                for x in range(len(business_category1)):
                    try:
                        category_object = business_category.objects.get(id=business_category1[x])
                        business_category2.append(category_object.business_category_name)
                    except:
                        pass

            business_category3 = ', '.join(map(str, business_category2))

            ads.business_category = business_category3

    merchant_list = GreenBillUser.objects.filter(is_merchant = True)

    business_category_list = business_category.objects.filter(id__in = excludes)

    for b_c_obj in business_category_list:
        business_category_list_new.append({
            'id': b_c_obj.id,
            'business_category_name': b_c_obj.business_category_name,
            })

    # business_category_list = business_category.objects.all()

    
    context = {
        'merchant_spaces': merchant_spaces,
        'total_count': total_count,
        'my_ads' : my_ads,
        'get_end_date': get_end_date,
        'get_start_date': get_start_date,
        'merchant_business_list' : merchant_business_list,
        'business_category_list': business_category_list,
        'business_category_list_new': business_category_list_new,
        'PromotionNavclass': 'active',
        "PromotionCollapseShow": "show",
        "AdsBelowAriaExpanded" : "true",
        "AdsBelowSubCollpseShow" : "show",
        "AdsForGreenBillNavclass": "active"
    }

    return render(request, "super_admin/promotions/ads-for-green-bills.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def get_green_bill_ads_details_by_id(request):

    if request.method == "POST":

        id = request.POST['id']

        ads_object = ads_for_green_bills.objects.get(id= id)

        business_category = ads_object.business_category_value

        category_list = []

        if business_category:
            category_list = list(business_category.split(",")) 
        else:
            category_list = ""


        business = ads_object.business_name_value

        business_list = []

        if business:
            business_list = list(business.split(",")) 
        else:
            business_list = ""


        try:
            ads_image_url = ads_object.ads_image.url
        except:
            ads_image_url = ""

        data = {
            'id': ads_object.id,
            'ads_name': ads_object.ads_name,
            'ads_image': ads_image_url,
            'ads_type': ads_object.ads_type,
            # 'merchant_list': merchant_list,
            'redirect_url': ads_object.redirect_url,
            'category_list': category_list,
            'business_list': business_list,
            'schedule': ads_object.schedule,
            'start_date': ads_object.start_date,
            'end_date': ads_object.end_date,
        }

        return JsonResponse({'status': "success", 'data' : data})
    else:
        return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})


@login_required(login_url="/login/")
@user_passes_test(is_owner)
def edit_green_bill_ads_by_id(request):
    if request.method == "POST":
        id = request.POST['ads_id']
        ads_name = request.POST['edit_ads_name']
        redirect_url = request.POST['edit_redirect_url']
        ads_type = request.POST['edit_ads_type']


        try:
            edit_schedule = request.POST['edit_schedule']
        except:
            edit_schedule = ""

        if edit_schedule == "True":
            start_date = request.POST['edit_start_date']
            end_date = request.POST['edit_end_date']
            schedule = True
        else:
            start_date = ""
            end_date = ""
            schedule = False

        # merchants_name_value = request.POST['edit_merchants_name_value']
        business_name_value = request.POST['edit_business_name_value']
        business_category_value = request.POST['edit_business_category_value']


        try:
            ads_image = request.FILES['edit_ads_image']
        except:
            ads_image = ""

        if ads_image:

            result = ads_for_green_bills.objects.filter(id = id).update(redirect_url = redirect_url, ads_name = ads_name, ads_type = ads_type, business_name_value = business_name_value, business_category_value = business_category_value, schedule = schedule, start_date = start_date, end_date = end_date)
            ads_object = ads_for_green_bills.objects.get(id = id)

            ads_object.ads_image = ads_image

            ads_object.save()
                
        else:
            result = ads_for_green_bills.objects.filter(id = id).update(redirect_url = redirect_url, ads_name = ads_name, ads_type = ads_type, business_name_value = business_name_value, business_category_value = business_category_value, schedule = schedule, start_date = start_date, end_date = end_date)

        if result:
            sweetify.success(request, title="Success", icon='success', text='Ads Updated Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Failed to update Ads!!!', timer=1500)
    else:
        sweetify.error(request, title="Error", icon='error', text='Something went wrong !', timer=1500)

    return redirect(ads_for_green_bill)


@login_required(login_url="/login/")
@user_passes_test(is_owner)
def delete_green_bill_ads_by_id(request, id):
    if request.method == "POST":
        data = ads_for_green_bills.objects.get(id= id).delete()
        sweetify.success(request, title="success", icon='success', text='Ads deleted Successfully !!!', timer=1500)
        return redirect(ads_for_green_bill)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Ads!!!', timer=1500)
        return redirect(ads_for_green_bill)


@login_required(login_url="/login/")
@user_passes_test(is_owner)
def set_green_bill_active_ads(request):

    if request.method == "POST":

        id = request.POST["active_ads"]

        result1 = ads_for_green_bills.objects.filter().update(active_ads = False)

        result2 = ads_for_green_bills.objects.filter(id = id).update(active_ads = True)

        if result1 and result2:
            sweetify.success(request, title="success", icon='success', text='Ads Set Successfully !!!', timer=1500)

        else:
            sweetify.error(request, title="error", icon='error', text='Failed to Set Ads!!!', timer=1500)
            return redirect(ads_for_green_bill)

        return redirect(ads_for_green_bill)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Set Ads!!!', timer=1500)
        return redirect(ads_for_green_bill)


def deactive_ads_by_id(request,id):
    if request.method == "POST":
        data = ads_below_bill.objects.filter(id= id).update(active_ads=False)
        sweetify.success(request, title="success", icon='success', text='Ads Deactivate Successfully !!!', timer=1500)
        return redirect(ads_for_green_bill)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Deactivate Ads!!!', timer=1500)
        return redirect(ads_for_green_bill)




  # path('bulk-sms/',bulkSms,name="bulk-sms"),
  #   path('bulk-mail/',bulkMail,name="bulk-mail"),

def categorycount(request):
    category_list = ''
    category_count = ''
    if request.method == "POST":
        category_count = request.POST['category_count']

        if category_count:
            category_list = category_count.split(',')
        total = 0
        for category in category_list:
            merchant_category = MerchantProfile.objects.filter(m_business_category = business_category.objects.get(id=category)).count()
            total = total + merchant_category
        
        return JsonResponse({'status': "success", 'total_category_count':total})


# SEND SMS
@login_required(login_url="/login/")
def bulkSms(request):
    staff = GreenBillUser.objects.all()

    role_list = merchant_role.objects.all()
    category = business_category.objects.all()

    for object in staff:
        role_name = merchant_userrole.objects.filter(user_id=object.id)

        for object1 in role_name:
            object.role = object1.id
            object.role_name = object1.role
            newRole = role.objects.filter(role_name = object1.role)
            for oject2 in newRole:
                object.role_id = oject2.id

    data = bulkMailSmsModel.objects.filter(owner_id = request.user.id, o_sent_sms=True).order_by('-id')
     
    sms_data = []
    
    for sms in data:
        try :
            receiver_name = int(sms.receiver_name)
            sms_data.append({
                'created_at' : sms.created_at,
                'receiver_name':'Custom',
                'smsheader': sms.smsheader, 
                'transactional': sms.transactional, 
                'o_sent_sms': sms.o_sent_sms,
                'o_sent_mail': sms.o_sent_mail,
                'id': sms.id,
                'message':sms.message,
                'campaign_name':sms.campaign_name,
                })
        except:
            sms_data.append({
                'created_at' : sms.created_at,
                'receiver_name': sms.receiver_name ,
                'smsheader': sms.smsheader, 
                'transactional': sms.transactional, 
                'o_sent_sms': sms.o_sent_sms,
                'o_sent_mail': sms.o_sent_mail,
                'id': sms.id,
                'message':sms.message,
                'campaign_name':sms.campaign_name,
                })
 

    owner_count = GreenBillUser.objects.filter(is_staff=True).count()
    # merchant_count = GreenBillUser.objects.filter(is_merchant=True).count() #+ GreenBillUser.objects.filter(is_merchant_staff=True).count() 
    merchant_count = MerchantProfile.objects.filter(m_user_id__isnull=False,m_disabled_account=False).count()
    customer_count = GreenBillUser.objects.filter(is_customer=True).count()
    # partner_count = GreenBillUser.objects.filter(is_partner=True).count()
    partner_count = PartnerProfile.objects.filter(p_disabled_account=False).count()
    
    merchant_category_count_list = []
    for i in category:

        merchant_category_count = MerchantProfile.objects.filter(m_business_category= i.id).count()
        # print('merchant',merchant_category_count)
        merchant_category_count_list.append({
            'id' : i.id,
            'merchant_category_count' :merchant_category_count,
        })

    context = {
        'all_merchant_user': staff,
        'merchant_role_list': role_list,
        'merchant_role_name': role_name,
        'category' : category,
        'data' : sms_data,
        'owner_count':owner_count,
        'merchant_count':merchant_count,
        'customer_count':customer_count,
        'partner_count':partner_count,
        'merchant_category_count_list':merchant_category_count_list,
        'PromotionNavclass': 'active',
        "PromotionCollapseShow": "show",
        'BulkSMSNavclass':'active',
        'bulkMailSmsForm':bulkMailSmsForm,
    }
    mobile_number_owner = []
    mobile_number_merchant = []
    mobile_number_customer = []
    mobile_number_partner = []
    email_owner = []
    email_merchant = []
    email_customer = []
    email_partner = []
    notice_id = ''     
                
    if request.method == "POST":
        title = request.POST.get('title')
        message = request.POST.get('message')
        promotional = request.POST.get('promotional')
        transactional = request.POST.get('transactional')
        custom_number = request.POST.get('custom-no')
        user_group = request.POST.getlist('group')
        smsheader = request.POST.get('smsheader')
        template = request.POST.get('template_id')
        owner = request.POST.get('checkso')
        merchant = request.POST.get('checksm')
        customer = request.POST.get('checksc')
        partner = request.POST.get('checksp')
        receipent_count = request.POST.get('receipent_count')
        file_upload = request.FILES.get('myfile')
        campaign_name = request.POST.get('campaign_name')

        # print('------------------------',campaign_name)
        joined_lines = ''
        csv_fields = ''
        if file_upload:
            if not file_upload.name.endswith('.csv'):

                sweetify.error(request, title="Error", icon='error',
                                                text="Choose valid csv file!!!", timer=5500)
            else:
                file_data = file_upload.read().decode("utf-8")
                file_lines = file_data.split("\n")
                csv_fields = [line.replace('\r','') for line in file_lines if line]

                converted_list = [str(no) for no in csv_fields]
                joined_lines = ",".join(converted_list)
        custom_number_list = ''
        if custom_number:
            custom_number_list = custom_number.split(',')

        category_s = request.POST.getlist('categorychecks')

        sent_notice = request.POST.getlist('sentnotice')

        individual_user = request.POST.getlist('individual')

        receiver_name = ''
        if owner:
            receiver_name = 'owner staff'

        if merchant:
                receiver_name = 'merchant'
        if customer:
                receiver_name = 'customer'
        if partner:
                receiver_name = 'partner'
        if owner and merchant:
                receiver_name = 'owner staff, merchant'
        if owner and customer:
                receiver_name = 'owner staff, customer'
        if owner and partner:
                receiver_name = 'owner staff, partner'
        if merchant and customer:
                receiver_name = 'merchant, customer'
        if merchant and partner:
                receiver_name = 'merchant, partner'
        if customer and partner:
                receiver_name = 'customer, partner'
        if owner and merchant and customer:
                receiver_name = 'owner staff, merchant, customer'
        if owner and merchant and partner:
                receiver_name = 'owner staff, merchant, partner'
        if partner and customer and merchant:
                receiver_name = 'partner, customer, merchant'
        if partner and customer and owner:
                receiver_name = 'partner, customer, owner staff'
        if owner and merchant and customer and partner:
                receiver_name = 'owner staff, merchant, customer, partner'
        if individual_user:
                receiver_name = 'individual user'
        if category_s:
                receiver_name = 'category'
        if custom_number:
            receiver_name = custom_number
        if file_upload:
            receiver_name = joined_lines

        template_id = ''
        if template == '1':
            template_id = '1007162209490097673'
        if template == '2':
            template_id = '1007162107620813728'
        if template == '3':
            template_id = '1007162106850723917'
        if template == '4':
            template_id = '1007162106809978850'
        if template == '5':
            template_id = '1007162106793840599'
        if template == '6':
            template_id = '1007162098384997217'
        if template == '7':
            template_id = '1007162098381110505'
        if template == '8':
            template_id = '1007162098372946720'
        if template == '9':
            template_id = '1007162098368573560'
        if template == '10':
            template_id = '1007162098358759996'
        if template == '11':
            template_id = '1007162098351638761'
        if template == '12':
            template_id = '1007162098340655435'
        if template == '13':
            template_id = '1007162098336084141'
        if template == '14':
            template_id = '1007162098331673473'
        if template == '15':
            template_id = '1007162098326474514'
        if template == '16':
            template_id = '1007162098321473343'
        if template == '17':
            template_id = '1007162098316946419'
        if template == '18':
            template_id = '1007162098307281560'
        if template == '19':
            template_id = '1007161821757152482'
        if template == '20':
            template_id = '1007161814187973948'
        if template == '21':
            template_id = '1007161814167155974'
        if template == '22':
            template_id = '1007161814117326730'
        



        # if individual_user and owner and merchant and customer and category_s and custom_number_list and csv_fields:
        #     print('OWNER',owner)
        #     sweetify.error(request,text="Please select either from group or individual list !!!", timer=5500)
        if file_upload and not file_upload.name.endswith('.csv'):
            sweetify.error(request, title="Error", icon='error',
                                                text="Choose valid csv file!!!", timer=5500)
        if individual_user or owner or merchant or customer or partner or category_s or custom_number_list or csv_fields:
            # print('owner == 1',owner)
            for notice in sent_notice:
                    # if notice == "sms":
                    #     notice_id = bulkMailSmsModel.objects.create(
                    #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_sent_sms=True)

                    # elif notice == "sent_mail":
                    #     notice_id = bulkMailSmsModel.objects.create(
                    #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_sent_mail=True)

                    # else:
                    #     notice_id = bulkMailSmsModel.objects.create(
                    #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_notification=True)

                if notice == "sms":
                        
                        notice_id = bulkMailSmsModel.objects.update_or_create(campaign_name=campaign_name, owner_id=request.user, title=title, message=message,smsheader=smsheader,template=message,receiver_name=receiver_name, promotional = promotional, transactional=transactional,  defaults= { 'title':title, 'message':message, 'smsheader':smsheader, 'template':template, 'promotional':promotional, 'transactional':transactional, 'o_sent_sms':True })

                elif notice == "sent_mail":
                        
                        notice_id = bulkMailSmsModel.objects.update_or_create(campaign_name=campaign_name, owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template,receiver_name=receiver_name, promotional = promotional, transactional=transactional, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template, 'promotional':promotional, 'transactional':transactional, 'o_sent_mail':True })

                # else:
                #     notice_id = bulkMailSmsModel.objects.update_or_create(owner_id=request.user, title=title, message=message, defaults= { 'title':title, 'notice_file': notice_file, 'message':message, 'o_notification':True })

                        # print(notice_id[0].id)

                        notice_object = bulkMailSmsModel.objects.get(id= notice_id[0].id)
                        # print('notice_object::',notice_object)
          
            if custom_number_list:
                for notice in sent_notice:
                    for number in custom_number_list:
                        # print('number',number)
                        if notice == 'sms':
                            contact = number
                            if contact:
                                ts = int(time.time())
                                data_temp = {
                                            "keyword":"Bill Delivery SMS",
                                            "timeStamp":ts,
                                            "dataSet":
                                                [
                                                    {
                                                        "UNIQUE_ID":"GB-" + str(ts),
                                                        "MESSAGE": message,
                                                        "OA":smsheader,
                                                        "MSISDN": contact, # Recipient's Mobile Number
                                                        "CHANNEL":"SMS",
                                                        "CAMPAIGN_NAME":"hind_user",
                                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                        "USER_NAME":"hind_hsi",
                                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                                        "DLT_CT_ID": template_id, # Template Id
                                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                    }
                                                ]
                                            }

                                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"
                                response = requests.post(url, json = data_temp)


                            sms_response =  sendSMS(str(contact), message)
                            # print(sms_response)


            if csv_fields:
                for notice in sent_notice:
                    for number in csv_fields:
                        if notice == 'sms':
                            contact = number
                            if contact:
                                ts = int(time.time())
                                data_temp = {
                                            "keyword":"Bill Delivery SMS",
                                            "timeStamp":ts,
                                            "dataSet":
                                                [
                                                    {
                                                        "UNIQUE_ID":"GB-" + str(ts),
                                                        "MESSAGE": message,
                                                        "OA":smsheader,
                                                        "MSISDN": contact, # Recipient's Mobile Number
                                                        "CHANNEL":"SMS",
                                                        "CAMPAIGN_NAME":"hind_user",
                                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                        "USER_NAME":"hind_hsi",
                                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                                        "DLT_CT_ID": template_id, # Template Id
                                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                    }
                                                ]
                                            }

                                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"
                                response = requests.post(url, json = data_temp)


                            sms_response =  sendSMS(str(contact), message)
                            # print(sms_response)
                             
            if individual_user:
                    for notice in sent_notice:
                        for user in individual_user:
                            user_object = GreenBillUser.objects.get(id = user)

                            # print(user_object)
                            if notice == "sms":
                                contact = user_object.mobile_no
                                
                                sms_response = sendSMS(str(contact), message)
                                if contact:
    
                                    ts = int(time.time())

                                    data_temp = {
                                            "keyword":"Bill Delivery SMS",
                                            "timeStamp":ts,
                                            "dataSet":
                                                [
                                                    {
                                                        "UNIQUE_ID":"GB-" + str(ts),
                                                        "MESSAGE": message,
                                                        "OA":smsheader,
                                                        "MSISDN": contact, # Recipient's Mobile Number
                                                        "CHANNEL":"SMS",
                                                        "CAMPAIGN_NAME":"hind_user",
                                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                        "USER_NAME":"hind_hsi",
                                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                                        "DLT_CT_ID": template_id, # Template Id
                                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                    }
                                                ]
                                            }

                                    url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                    response = requests.post(url, json = data_temp)


                                    # import urllib
                                    # username = "sanjog1"
                                    # Password = "123456"
                                    # sender = "HINDAG"
                                    # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                    # temp_dict = {"text": temp_message}
                                    # message= urllib.parse.urlencode(temp_dict)
                                    # priority='ndnd'
                                    # stype='normal'

                                    # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                    # import requests

                                    # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                    # res = requests.get(url)

                                    # if response.status_code == 200:
                                    #     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                    # else:
                                    #     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                    # return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                    # print(sms_response)
                                # print(sms_response)
                                try:
                                        owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
                                except:
                                        owner_notice_sent_save = ""
                            elif notice == "sent_mail":
                                try:
                                    email_id = user_object.email
                                    
                                    email_from = settings.EMAIL_HOST_USER
                                    # print('email from',email_from)
                                    recipient_list = [email_id, 'mohini.d@zappkode.com' ]
                                    # recipient_list = ['shreyash.t@zappkode.com']
                                    # print('email to',recipient_list)
                                    message = message
                                   
                                    plain_message = strip_tags(message)
                                    # print('sent message:',plain_message)
                                    # print('file',notice_file)
                                    # sendmail = EmailMessage(
                                    #     title, message, email_from, recipient_list)

                                    # sendmail.attach(notice_file.name,
                                    #                 notice_file.read(), notice_file.content_type)

                                    # response = sendmail.send()
                                    send_mail( title, plain_message, email_from, recipient_list)
                                    # print(response)

                                    # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                    #     notice_id=notice_object, user_id=user_object, defaults = {'sent_mail':True})

                                except:
                                    
                                    owner_notice_sent_save = ""
                           

            
            if owner:
                    print('hello owner')
                    for notice in sent_notice:
                        
                            # print(user)
                            user_object = GreenBillUser.objects.filter(is_staff=True)
                            # print(user_object)
                            for user_o in user_object:
                                # print(user_o.first_name)
                                # print(user,"+", user.id)
                                if notice == "sms":
                                    # print('ownr in sms')
                                    contact = user_o.mobile_no
                                    # contact = '7387810242'
                                    # message = strip_tags(message)
                                    sms_response = sendSMS(str(contact), message)
                                    if contact:
    
                                        ts = int(time.time())

                                        data_temp = {
                                                "keyword":"Bill Delivery SMS",
                                                "timeStamp":ts,
                                                "dataSet":
                                                    [
                                                        {
                                                            "UNIQUE_ID":"GB-" + str(ts),
                                                            "MESSAGE": message,
                                                            "OA":smsheader,
                                                            "MSISDN": contact, # Recipient's Mobile Number
                                                            "CHANNEL":"SMS",
                                                            "CAMPAIGN_NAME":"hind_user",
                                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                            "USER_NAME":"hind_hsi",
                                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                                            "DLT_CT_ID":template_id, # Template Id
                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                        }
                                                    ]
                                                }

                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                        response = requests.post(url, json = data_temp)


                                        # print(data_temp)
                                        # print(response)

                                        # import urllib
                                        # username = "sanjog1"
                                        # Password = "123456"
                                        # sender = "HINDAG"
                                        # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                        # temp_dict = {"text": temp_message}
                                        # message= urllib.parse.urlencode(temp_dict)
                                        # priority='ndnd'
                                        # stype='normal'

                                        # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                        # import requests

                                        # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                        # res = requests.get(url)

                                        # if response.status_code == 200:
                                        #     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                        # else:
                                        #     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                        # return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                        # print(sms_response)
                                    try:
                                        owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        message_id=notice_object, user_id=user_o.user, defaults = {'sent_sms':True})
                                    except:
                                        owner_notice_sent_save = ""
                                elif notice == "sent_mail":
                                    try:
                                        email_id = user_o.email
                                    
                                        email_from = settings.EMAIL_HOST_USER
                                        # print('email from',email_from)
                                        # recipient_list = [email_id, 'shreyash.t@zappkode.com' ]
                                        recipient_list = ['mohini.d@zappkode.com']
                                        # print('email to',recipient_list)
                                        message = message
                                        plain_message = strip_tags(message)
                                        # print('sent message:',plain_message)
                                        # print('sent message:',message)
                                        # print('file',notice_file)
                                        # sendmail = EmailMessage(
                                        #     title, message, email_from, recipient_list)

                                        # sendmail.attach(notice_file.name,
                                        #                 notice_file.read(), notice_file.content_type)

                                        # response = sendmail.send()
                                        send_mail( title, plain_message, email_from, recipient_list)
                                        # print(response)

                                        # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        #     message_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                    except:
                                        
                                        owner_notice_sent_save = ""

                                        owner_notice_sent_save = ""
                
            if merchant:
                    for notice in sent_notice:
                        
                            # print(user)
                            user_object = GreenBillUser.objects.filter(is_merchant=True)
                            # print(user_object)
                            for user in user_object:
                                # print('users')
                                # print(user,"+", user.id,"+", user.first_name)
                                if notice == "sms":
                                    contact = user.mobile_no
                                    message = strip_tags(message)
                                    sms_response = sendSMS(str(contact), message)
                                    if contact:
    
                                        ts = int(time.time())

                                        data_temp = {
                                                "keyword":"Bill Delivery SMS",
                                                "timeStamp":ts,
                                                "dataSet":
                                                    [
                                                        {
                                                            "UNIQUE_ID":"GB-" + str(ts),
                                                            "MESSAGE": message,
                                                            "OA":smsheader,
                                                            "MSISDN": contact, # Recipient's Mobile Number
                                                            "CHANNEL":"SMS",
                                                            "CAMPAIGN_NAME":"hind_user",
                                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                            "USER_NAME":"hind_hsi",
                                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                                            "DLT_CT_ID":template_id, # Template Id
                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                        }
                                                    ]
                                                }

                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                        response = requests.post(url, json = data_temp)

                                        # import urllib
                                        # username = "sanjog1"
                                        # Password = "123456"
                                        # sender = "HINDAG"
                                        # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                        # temp_dict = {"text": temp_message}
                                        # message= urllib.parse.urlencode(temp_dict)
                                        # priority='ndnd'
                                        # stype='normal'

                                        # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                        # import requests

                                        # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                        # res = requests.get(url)

                                        # if response.status_code == 200:
                                        #     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                        # else:
                                        #     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                        # return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                        # print(sms_response)
                                    try:
                                        owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        message_id=notice_object, user_id=user.user, defaults = {'sent_sms':True})
                                    except:
                                        owner_notice_sent_save = ""
                                elif notice == "sent_mail":
                                    try:
                                        email_id = user.email
                                    
                                        email_from = settings.EMAIL_HOST_USER
                                        # print('email from',email_from)
                                        recipient_list = [email_id, 'mohini.d@zappkode.com' ]
                                        # recipient_list = ['shreyash.t@zappkode.com']
                                        # print('email to',recipient_list)
                                        message = message
                                        plain_message = strip_tags(message)
                                        # print('sent message:',plain_message)
                                        # print('sent message:',message)
                                        # print('file',notice_file)
                                        # sendmail = EmailMessage(
                                        #     title, message, email_from, recipient_list)

                                        # sendmail.attach(notice_file.name,
                                        #                 notice_file.read(), notice_file.content_type)

                                        # response = sendmail.send()
                                        send_mail( title, plain_message, email_from, recipient_list)
                                        # print(response)
                                        # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        #     message_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                    except:
                                        
                                        owner_notice_sent_save = ""
                
            if customer:
                    for notice in sent_notice:
                        
                            # print(user)
                            user_object = GreenBillUser.objects.filter(is_customer=True)
                            # print(user_object)
                            for user in user_object:
                                # print('users')
                                # print(user,"+", user.id,"+", user.first_name)
                                if notice == "sms":
                                    contact = user.mobile_no
                                    message = strip_tags(message)
                                    if contact:
    
                                        ts = int(time.time())

                                        data_temp = {
                                                "keyword":"Bill Delivery SMS",
                                                "timeStamp":ts,
                                                "dataSet":
                                                    [
                                                        {
                                                            "UNIQUE_ID":"GB-" + str(ts),
                                                            "MESSAGE": message,
                                                            "OA":smsheader,
                                                            "MSISDN": contact, # Recipient's Mobile Number
                                                            "CHANNEL":"SMS",
                                                            "CAMPAIGN_NAME":"hind_user",
                                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                            "USER_NAME":"hind_hsi",
                                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                                            "DLT_CT_ID":template_id, # Template Id
                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                        }
                                                    ]
                                                }

                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                        response = requests.post(url, json = data_temp)

                                        # import urllib
                                        # username = "sanjog1"
                                        # Password = "123456"
                                        # sender = "HINDAG"
                                        # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                        # temp_dict = {"text": temp_message}
                                        # message= urllib.parse.urlencode(temp_dict)
                                        # priority='ndnd'
                                        # stype='normal'

                                        # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                        # import requests

                                        # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                        # res = requests.get(url)

                                        # if response.status_code == 200:
                                        #     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                        # else:
                                        #     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                        # return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                        # print(sms_response)
                                        # sms_response = sendSMS(str(contact), message)
                                    try:
                                        owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        message_id=notice_object, user_id=user.user, defaults = {'sent_sms':True})
                                    except:
                                        owner_notice_sent_save = ""
                                elif notice == "sent_mail":
                                    try:
                                        email_id = user.email
                                    
                                        email_from = settings.EMAIL_HOST_USER
                                        # print('email from',email_from)
                                        recipient_list = [email_id, 'mohini.d@zappkode.com' ]
                                        # recipient_list = ['shreyash.t@zappkode.com']
                                        # print('email to',recipient_list)
                                        message = message
                                        # print('sent message:',message)
                                        plain_message = strip_tags(message)
                                        # print('sent message:',plain_message)
                                        # print('file',notice_file)
                                        # sendmail = EmailMessage(
                                        #     title, message, email_from, recipient_list)

                                        # sendmail.attach(notice_file.name,
                                        #                 notice_file.read(), notice_file.content_type)

                                        # response = sendmail.send()
                                        send_mail( title, plain_message, email_from, recipient_list)
                                        # print(response)
                                        # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        #     message_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                    except:
                                        
                                        owner_notice_sent_save = ""


                
            if partner:
                    for notice in sent_notice:
                        
                            # print(user)
                            user_object = GreenBillUser.objects.filter(is_partner=True)
                            # print(user_object)
                            for user in user_object:
                                # print('users')
                                # print(user,"+", user.id,"+", user.first_name)
                                if notice == "sms":
                                    contact = user.mobile_no
                                    message = strip_tags(message)
                                    if contact:
    
                                        ts = int(time.time())

                                        data_temp = {
                                                "keyword":"Bill Delivery SMS",
                                                "timeStamp":ts,
                                                "dataSet":
                                                    [
                                                        {
                                                            "UNIQUE_ID":"GB-" + str(ts),
                                                            "MESSAGE": message,
                                                            "OA":smsheader,
                                                            "MSISDN": contact, # Recipient's Mobile Number
                                                            "CHANNEL":"SMS",
                                                            "CAMPAIGN_NAME":"hind_user",
                                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                            "USER_NAME":"hind_hsi",
                                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                                            "DLT_CT_ID":template_id, # Template Id
                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                        }
                                                    ]
                                                }

                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                        response = requests.post(url, json = data_temp)

                                        # import urllib
                                        # username = "sanjog1"
                                        # Password = "123456"
                                        # sender = "HINDAG"
                                        # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                        # temp_dict = {"text": temp_message}
                                        # message= urllib.parse.urlencode(temp_dict)
                                        # priority='ndnd'
                                        # stype='normal'

                                        # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                        # import requests

                                        # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                        # res = requests.get(url)

                                        # if response.status_code == 200:
                                        #     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                        # else:
                                        #     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                        # return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                        # print(sms_response)
                                        # sms_response = sendSMS(str(contact), message)
                                    try:
                                        owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        message_id=notice_object, user_id=user.user, defaults = {'sent_sms':True})
                                    except:
                                        owner_notice_sent_save = ""
                                elif notice == "sent_mail":
                                    try:
                                        email_id = user.email
                                    
                                        email_from = settings.EMAIL_HOST_USER
                                        # print('email from',email_from)
                                        recipient_list = [email_id, 'mohini.d@zappkode.com' ]
                                        # recipient_list = ['shreyash.t@zappkode.com']
                                        # print('email to',recipient_list)
                                        message = message
                                        # print('sent message:',message)
                                        plain_message = strip_tags(message)
                                        # print('sent message:',plain_message)
                                        # print('file',notice_file)
                                        # sendmail = EmailMessage(
                                        #     title, message, email_from, recipient_list)

                                        # sendmail.attach(notice_file.name,
                                        #                 notice_file.read(), notice_file.content_type)

                                        # response = sendmail.send()
                                        send_mail( title, plain_message, email_from, recipient_list)
                                        # print(response)
                                        # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        #     message_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                    except:
                                        
                                        owner_notice_sent_save = ""
                                    False

                                


            if category:
                    for roleid in category_s:
                        # print('cca')
                        # print(roleid)
                        user_list = business_category.objects.filter(id=roleid)
                        for u in user_list:
                            print(u.business_category_name)
                        bb = MerchantProfile.objects.filter(m_business_category = u)
                        # print(bb)
                        for user_data in bb:
                            for user_data in bb:
                                # print('user_data',user_data)
                                users = GreenBillUser.objects.filter(mobile_no=user_data.m_user )
                                # print(users)
                                for u in users:
                                    for notice in sent_notice:
                                        if notice == "sms":
                                            # print(user_data.m_user)
                                            contact = u.mobile_no
                                            # print('contact',contact)
                                            # print(contact)
                                            message = strip_tags(message)
                                            if contact:
    
                                                ts = int(time.time())

                                                data_temp = {
                                                        "keyword":"Bill Delivery SMS",
                                                        "timeStamp":ts,
                                                        "dataSet":
                                                            [
                                                                {
                                                                    "UNIQUE_ID":"GB-" + str(ts),
                                                                    "MESSAGE": message,
                                                                    "OA":smsheader,
                                                                    "MSISDN": contact, # Recipient's Mobile Number
                                                                    "CHANNEL":"SMS",
                                                                    "CAMPAIGN_NAME":"hind_user",
                                                                    "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                                    "USER_NAME":"hind_hsi",
                                                                    "DLT_TM_ID":"1001096933494158", # TM ID
                                                                    "DLT_CT_ID":template_id, # Template Id
                                                                    "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                }
                                                            ]
                                                        }

                                                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                response = requests.post(url, json = data_temp)

                                              
                                            try:
                                                owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                                message_id=notice_object, user_id=user_data.m_user, defaults = {'sent_sms':True})
                                            except:
                                                owner_notice_sent_save = ""


                                        elif notice == "sent_mail":
                                            print('mail')
                                            try:
                                                # print('mail2')
                                                # email_id = user_data.m_company_email
                                                email_id = u.email
                                                # print('email_id',email_id)
                                                email_from = settings.EMAIL_HOST_USER
                                                # print('email from',email_from)
                                                recipient_list = [email_id, 'mohini.d@zappkode.com' ]
                                                # recipient_list = ['shreyash.t@zappkode.com']
                                                # print('email to',recipient_list)
                                                message = message
                                                # print('sent message:',message)
                                                plain_message = strip_tags(message)
                                                # print('sent message:',plain_message)
                                                # print('file',notice_file)
                                                # sendmail = EmailMessage(
                                                #     title, message, email_from, recipient_list)

                                                # sendmail.attach(notice_file.name,
                                                #                 notice_file.read(), notice_file.content_type)

                                                # response = sendmail.send()
                                                send_mail( title, plain_message, email_from, recipient_list)
                                                # print(response)
                                                owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                                    message_id=notice_object, user_id=user_data.m_user, defaults = {'sent_mail':True})

                                            except:
                                                owner_notice_sent_save = ""



            sweetify.success(request, title="Success", icon='success',
                                text='Notice Send successfully!!', timer=5500)
                # return redirect("/owner_notice_board/")
        else:
                sweetify.error(request, title="Error", icon='error',
                                text="Please select either from group or individual list or owner !!!", timer=5500)
        # else:
        #     sweetify.error(request, "Please Provide Valid Data")                

    return render(request, 'super_admin/promotions/bulk_sms.html', context)


def deleteBulksms(request,id):
    if request.method == "POST":
        instance = bulkMailSmsModel.objects.get(id=id)
        instance.delete()

        return JsonResponse({'success':True})
    return HttpResponse('done!!')




# SEND EMAIL
@login_required(login_url="/login/")
def bulkMail(request):
    staff = GreenBillUser.objects.all()
    print('objects')
    # print(staff)
    role_list = merchant_role.objects.all()
    category = business_category.objects.all()
    # print(staff)
    for object in staff:
        role_name = merchant_userrole.objects.filter(user_id=object.id)
        # print(role_name)
        for object1 in role_name:
            object.role = object1.id
            object.role_name = object1.role
            newRole = role.objects.filter(role_name = object1.role)
            for oject2 in newRole:
                object.role_id = oject2.id
        # print(role_name)
    # owner = staff.filter(is_staff=True)
    data = bulkMailSmsModel.objects.filter(owner_id = request.user.id, o_sent_mail=True).order_by('-id')

    context = {
        'all_merchant_user': staff,
        'merchant_role_list': role_list,
        'merchant_role_name': role_name,
        'category' : category,
        'data' : data,
        # 'notice_data': notice_data,
        'PromotionNavclass': 'active',
        "PromotionCollapseShow": "show",
        'BulkEmailNavclass':'active',
        'bulkMailSmsForm':bulkMailSmsForm,
    }
    mobile_number_owner = []
    mobile_number_merchant = []
    mobile_number_customer = []
    mobile_number_partner = []
    email_owner = []
    email_merchant = []
    email_customer = []
    email_partner = []
    notice_id = ''     
    # notice_object = ''                 
    if request.method == "POST":
        title = request.POST.get('title')
        message = request.POST.get('message')
        user_group = request.POST.getlist('group')
        smsheader = request.POST.get('smsheader')
        template_id = request.POST.get('template')
        owner = request.POST.get('checkso')
        merchant = request.POST.get('checksm')
        customer = request.POST.get('checksc')
        partner = request.POST.get('checksp')
        file_upload = request.FILES.get('myfile')
        custom_number = request.POST.get('custom-no')
        joined_lines = ''
        csv_fields = ''
        if file_upload:
            if not file_upload.name.endswith('.csv'):
                sweetify.error(request, title="Error", icon='error',
                                                text="Choose valid csv file!!!", timer=5500)
            else:
                file_data = file_upload.read().decode("utf-8")
                file_lines = file_data.split("\n")
                csv_fields = [line.replace('\r','') for line in file_lines if line]

                converted_list = [str(no) for no in csv_fields]
                joined_lines = ",".join(converted_list)

        custom_number_list = ''
        if custom_number:
            custom_number_list = custom_number.split(',')
        print('smsheader',smsheader)
        print('template',template_id)
        print('owner',owner)
        print('merchant',merchant)
        print('customer',customer)
        print('partner',partner)


        category_s = request.POST.getlist('categorychecks')

        sent_notice = request.POST.getlist('sentnotice')
        print('sent_notice',sent_notice)
        individual_user = request.POST.getlist('individual')
        print('title',title)
     
        print('message',message)
        print('user_group',user_group)
        
        print(individual_user)  
        if owner:
            receiver_name = 'owner staff'

        if merchant:
                receiver_name = 'merchant'
        if customer:
                receiver_name = 'customer'
        if partner:
                receiver_name = 'partner'
        if owner and merchant:
                receiver_name = 'owner staff, merchant'
        if owner and customer:
                receiver_name = 'owner staff, customer'
        if owner and partner:
                receiver_name = 'owner staff, partner'
        if merchant and customer:
                receiver_name = 'merchant, customer'
        if merchant and partner:
                receiver_name = 'merchant, partner'
        if customer and partner:
                receiver_name = 'customer, partner'
        if owner and merchant and customer:
                receiver_name = 'owner staff, merchant, customer'
        if owner and merchant and partner:
                receiver_name = 'owner staff, merchant, partner'
        if partner and customer and merchant:
                receiver_name = 'partner, customer, merchant'
        if partner and customer and owner:
                receiver_name = 'partner, customer, owner staff'
        if owner and merchant and customer and partner:
                receiver_name = 'owner staff, merchant, customer, partner'
        if individual_user:
                receiver_name = 'individual user'
        if category_s:
                receiver_name = 'category'
        if file_upload:
                receiver_name = joined_lines
        if custom_number: 
            receiver_name = custom_number
        # print('received by')
        # print(receiver_name)
        if individual_user and owner and merchant and customer and category_s and csv_fields and custom_number_list:
            print('OWNER',owner)
            sweetify.error(request,text="Please select either from group or individual list !!!", timer=5500)
        elif  individual_user or owner or merchant or customer or partner or category_s or csv_fields or custom_number_list:
            print('owner == 1',owner)
            for notice in sent_notice:
                    # if notice == "sms":
                    #     notice_id = bulkMailSmsModel.objects.create(
                    #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_sent_sms=True)

                    # elif notice == "sent_mail":
                    #     notice_id = bulkMailSmsModel.objects.create(
                    #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_sent_mail=True)

                    # else:
                    #     notice_id = bulkMailSmsModel.objects.create(
                    #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_notification=True)

                if notice == "sms":
                        
                        notice_id = bulkMailSmsModel.objects.update_or_create(owner_id=request.user, title=title, message=message,receiver_name=receiver_name,smsheader=smsheader,template=template_id,  defaults= { 'title':title, 'message':message, 'o_sent_sms':True })

                elif notice == "sent_mail":
                        
                        notice_id = bulkMailSmsModel.objects.update_or_create(owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template_id,receiver_name=receiver_name, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template, 'o_sent_mail':True })

                # else:
                #     notice_id = bulkMailSmsModel.objects.update_or_create(owner_id=request.user, title=title, message=message, defaults= { 'title':title, 'notice_file': notice_file, 'message':message, 'o_notification':True })

                        print(notice_id[0].id)

                        notice_object = bulkMailSmsModel.objects.get(id= notice_id[0].id)
                        print('notice_object::',notice_object)
          

                             
            if individual_user:
                    for notice in sent_notice:
                        for user in individual_user:
                            user_object = GreenBillUser.objects.get(id = user)

                            print(user_object)
                            if notice == "sms":
                                contact = user_object.mobile_no
                                message = strip_tags(message)
                                sms_response = sendSMS(str(contact), message)
                                if contact:
    
                                    ts = int(time.time())

                                    data_temp = {
                                            "keyword":"Bill Delivery SMS",
                                            "timeStamp":ts,
                                            "dataSet":
                                                [
                                                    {
                                                        "UNIQUE_ID":"GB-" + str(ts),
                                                        "MESSAGE": message,
                                                        "OA":smsheader,
                                                        "MSISDN": contact, # Recipient's Mobile Number
                                                        "CHANNEL":"SMS",
                                                        "CAMPAIGN_NAME":"hind_user",
                                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                        "USER_NAME":"hind_hsi",
                                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                                        "DLT_CT_ID": template_id, # Template Id
                                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                    }
                                                ]
                                            }

                                    url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                    response = requests.post(url, json = data_temp)

                                    # import urllib
                                    # username = "sanjog1"
                                    # Password = "123456"
                                    # sender = "HINDAG"
                                    # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                    # temp_dict = {"text": temp_message}
                                    # message= urllib.parse.urlencode(temp_dict)
                                    # priority='ndnd'
                                    # stype='normal'

                                    # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                    # import requests

                                    # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                    # res = requests.get(url)

                                    # if response.status_code == 200:
                                    #     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                    # else:
                                    #     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                    # return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                    # print(sms_response)
                                print(sms_response)
                                try:
                                        owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
                                except:
                                        owner_notice_sent_save = ""
                            elif notice == "sent_mail":
                                try:
                                    email_id = user_object.email
                                    
                                    email_from = settings.EMAIL_HOST_USER
                                    print('email from',email_from)
                                    recipient_list = [email_id, 'mohini.d@zappkode.com' ]
                                    # recipient_list = ['shreyash.t@zappkode.com']
                                    print('email to',recipient_list)
                                    message = message
                                   
                                    plain_message = strip_tags(message)
                                    print('sent message:',plain_message)
                                    # print('file',notice_file)
                                    # sendmail = EmailMessage(
                                    #     title, message, email_from, recipient_list)

                                    # sendmail.attach(notice_file.name,
                                    #                 notice_file.read(), notice_file.content_type)

                                    # response = sendmail.send()
                                    send_mail( title, plain_message, email_from, recipient_list)
                                    # print(response)

                                    # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                    #     notice_id=notice_object, user_id=user_object, defaults = {'sent_mail':True})

                                except:
                                    
                                    owner_notice_sent_save = ""
                           

            
            if owner:
                    print('hello owner')
                    for notice in sent_notice:
                        
                            # print(user)
                            user_object = GreenBillUser.objects.filter(is_staff=True)
                            # print(user_object)
                            for user_o in user_object:
                                # print(user_o.first_name)
                                # print(user,"+", user.id)
                                if notice == "sms":
                                    print('ownr in sms')
                                    contact = user_o.mobile_no
                                    message = strip_tags(message)
                                    sms_response = sendSMS(str(contact), message)
                                    if contact:
    
                                        ts = int(time.time())

                                        data_temp = {
                                                "keyword":"Bill Delivery SMS",
                                                "timeStamp":ts,
                                                "dataSet":
                                                    [
                                                        {
                                                            "UNIQUE_ID":"GB-" + str(ts),
                                                            "MESSAGE": message,
                                                            "OA":smsheader,
                                                            "MSISDN": contact, # Recipient's Mobile Number
                                                            "CHANNEL":"SMS",
                                                            "CAMPAIGN_NAME":"hind_user",
                                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                            "USER_NAME":"hind_hsi",
                                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                                            "DLT_CT_ID":template_id, # Template Id
                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                        }
                                                    ]
                                                }

                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                        response = requests.post(url, json = data_temp)

                                        # import urllib
                                        # username = "sanjog1"
                                        # Password = "123456"
                                        # sender = "HINDAG"
                                        # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                        # temp_dict = {"text": temp_message}
                                        # message= urllib.parse.urlencode(temp_dict)
                                        # priority='ndnd'
                                        # stype='normal'

                                        # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                        # import requests

                                        # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                        # res = requests.get(url)

                                        # if response.status_code == 200:
                                        #     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                        # else:
                                        #     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                        # return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                        # print(sms_response)
                                    try:
                                        owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        message_id=notice_object, user_id=user_o.user, defaults = {'sent_sms':True})
                                    except:
                                        owner_notice_sent_save = ""
                                elif notice == "sent_mail":
                                    try:
                                        email_id = user_o.email
                                    
                                        email_from = settings.EMAIL_HOST_USER
                                        print('email from',email_from)
                                        # recipient_list = [email_id, 'shreyash.t@zappkode.com' ]
                                        recipient_list = ['shreyash.t@zappkode.com']
                                        print('email to',recipient_list)
                                        message = message
                                        plain_message = strip_tags(message)
                                        print('sent message:',plain_message)
                                        print('sent message:',message)
                                        # print('file',notice_file)
                                        # sendmail = EmailMessage(
                                        #     title, message, email_from, recipient_list)

                                        # sendmail.attach(notice_file.name,
                                        #                 notice_file.read(), notice_file.content_type)

                                        # response = sendmail.send()
                                        send_mail( title, plain_message, email_from, recipient_list)
                                        # print(response)

                                        # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        #     message_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                    except:
                                        
                                        owner_notice_sent_save = ""

                                        owner_notice_sent_save = ""
                
            if merchant:
                    for notice in sent_notice:
                        
                            # print(user)
                            user_object = GreenBillUser.objects.filter(is_merchant=True)
                            # print(user_object)
                            for user in user_object:
                                # print('users')
                                # print(user,"+", user.id,"+", user.first_name)
                                if notice == "sms":
                                    contact = user.mobile_no
                                    message = strip_tags(message)
                                    sms_response = sendSMS(str(contact), message)
                                    if contact:
    
                                        ts = int(time.time())

                                        data_temp = {
                                                "keyword":"Bill Delivery SMS",
                                                "timeStamp":ts,
                                                "dataSet":
                                                    [
                                                        {
                                                            "UNIQUE_ID":"GB-" + str(ts),
                                                            "MESSAGE": message,
                                                            "OA":smsheader,
                                                            "MSISDN": contact, # Recipient's Mobile Number
                                                            "CHANNEL":"SMS",
                                                            "CAMPAIGN_NAME":"hind_user",
                                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                            "USER_NAME":"hind_hsi",
                                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                                            "DLT_CT_ID":template_id, # Template Id
                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                        }
                                                    ]
                                                }

                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                        response = requests.post(url, json = data_temp)

                                        # import urllib
                                        # username = "sanjog1"
                                        # Password = "123456"
                                        # sender = "HINDAG"
                                        # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                        # temp_dict = {"text": temp_message}
                                        # message= urllib.parse.urlencode(temp_dict)
                                        # priority='ndnd'
                                        # stype='normal'

                                        # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                        # import requests

                                        # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                        # res = requests.get(url)

                                        # if response.status_code == 200:
                                        #     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                        # else:
                                        #     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                        # return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                        # print(sms_response)
                                    try:
                                        owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        message_id=notice_object, user_id=user.user, defaults = {'sent_sms':True})
                                    except:
                                        owner_notice_sent_save = ""
                                elif notice == "sent_mail":
                                    try:
                                        email_id = user.email
                                    
                                        email_from = settings.EMAIL_HOST_USER
                                        print('email from',email_from)
                                        recipient_list = [email_id, 'mohini.d@zappkode.com' ]
                                        # recipient_list = ['shreyash.t@zappkode.com']
                                        print('email to',recipient_list)
                                        message = message
                                        plain_message = strip_tags(message)
                                        print('sent message:',plain_message)
                                        print('sent message:',message)
                                        # print('file',notice_file)
                                        # sendmail = EmailMessage(
                                        #     title, message, email_from, recipient_list)

                                        # sendmail.attach(notice_file.name,
                                        #                 notice_file.read(), notice_file.content_type)

                                        # response = sendmail.send()
                                        send_mail( title, plain_message, email_from, recipient_list)
                                        # print(response)
                                        # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        #     message_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                    except:
                                        
                                        owner_notice_sent_save = ""
                
            if customer:
                    for notice in sent_notice:
                        
                            # print(user)
                            user_object = GreenBillUser.objects.filter(is_customer=True)
                            # print(user_object)
                            for user in user_object:
                                print('users')
                                print(user,"+", user.id,"+", user.first_name)
                                if notice == "sms":
                                    contact = user.mobile_no
                                    message = strip_tags(message)
                                    if contact:
    
                                        ts = int(time.time())

                                        data_temp = {
                                                "keyword":"Bill Delivery SMS",
                                                "timeStamp":ts,
                                                "dataSet":
                                                    [
                                                        {
                                                            "UNIQUE_ID":"GB-" + str(ts),
                                                            "MESSAGE": message,
                                                            "OA":smsheader,
                                                            "MSISDN": contact, # Recipient's Mobile Number
                                                            "CHANNEL":"SMS",
                                                            "CAMPAIGN_NAME":"hind_user",
                                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                            "USER_NAME":"hind_hsi",
                                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                                            "DLT_CT_ID":template_id, # Template Id
                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                        }
                                                    ]
                                                }

                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                        response = requests.post(url, json = data_temp)

                                        # import urllib
                                        # username = "sanjog1"
                                        # Password = "123456"
                                        # sender = "HINDAG"
                                         # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                        # temp_dict = {"text": temp_message}
                                        # message= urllib.parse.urlencode(temp_dict)
                                        # priority='ndnd'
                                        # stype='normal'

                                        # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                        # import requests

                                        # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                        # res = requests.get(url)

                                        # if response.status_code == 200:
                                        #     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                        # else:
                                        #     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                        # return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                        # print(sms_response)
                                        # sms_response = sendSMS(str(contact), message)
                                    try:
                                        owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        message_id=notice_object, user_id=user.user, defaults = {'sent_sms':True})
                                    except:
                                        owner_notice_sent_save = ""
                                elif notice == "sent_mail":
                                    try:
                                        email_id = user.email
                                    
                                        email_from = settings.EMAIL_HOST_USER
                                        print('email from',email_from)
                                        recipient_list = [email_id, 'mohini.d@zappkode.com' ]
                                        # recipient_list = ['shreyash.t@zappkode.com']
                                        print('email to',recipient_list)
                                        message = message
                                        print('sent message:',message)
                                        plain_message = strip_tags(message)
                                        print('sent message:',plain_message)
                                        # print('file',notice_file)
                                        # sendmail = EmailMessage(
                                        #     title, message, email_from, recipient_list)

                                        # sendmail.attach(notice_file.name,
                                        #                 notice_file.read(), notice_file.content_type)

                                        # response = sendmail.send()
                                        send_mail( title, plain_message, email_from, recipient_list)
                                        # print(response)
                                        # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        #     message_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                    except:
                                        
                                        owner_notice_sent_save = ""


                
            if partner:
                    for notice in sent_notice:
                        
                            # print(user)
                            user_object = GreenBillUser.objects.filter(is_partner=True)
                            # print(user_object)
                            for user in user_object:
                                print('users')
                                print(user,"+", user.id,"+", user.first_name)
                                if notice == "sms":
                                    contact = user.mobile_no
                                    message = strip_tags(message)
                                    if contact:
    
                                        ts = int(time.time())

                                        data_temp = {
                                                "keyword":"Bill Delivery SMS",
                                                "timeStamp":ts,
                                                "dataSet":
                                                    [
                                                        {
                                                            "UNIQUE_ID":"GB-" + str(ts),
                                                            "MESSAGE": message,
                                                            "OA":smsheader,
                                                            "MSISDN": contact, # Recipient's Mobile Number
                                                            "CHANNEL":"SMS",
                                                            "CAMPAIGN_NAME":"hind_user",
                                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                            "USER_NAME":"hind_hsi",
                                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                                            "DLT_CT_ID":template_id, # Template Id
                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                        }
                                                    ]
                                                }

                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                        response = requests.post(url, json = data_temp)

                                        # import urllib
                                        # username = "sanjog1"
                                        # Password = "123456"
                                        # sender = "HINDAG"
                                        # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                        # temp_dict = {"text": temp_message}
                                        # message= urllib.parse.urlencode(temp_dict)
                                        # priority='ndnd'
                                        # stype='normal'

                                        # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                        # import requests

                                        # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                        # res = requests.get(url)

                                        # if response.status_code == 200:
                                        #     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                        # else:
                                        #     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                        # return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                        # print(sms_response)
                                        # sms_response = sendSMS(str(contact), message)
                                    try:
                                        owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        message_id=notice_object, user_id=user.user, defaults = {'sent_sms':True})
                                    except:
                                        owner_notice_sent_save = ""
                                elif notice == "sent_mail":
                                    try:
                                        email_id = user.email
                                    
                                        email_from = settings.EMAIL_HOST_USER
                                        print('email from',email_from)
                                        recipient_list = [email_id, 'mohini.d@zappkode.com' ]
                                        # recipient_list = ['shreyash.t@zappkode.com']
                                        print('email to',recipient_list)
                                        message = message
                                        print('sent message:',message)
                                        plain_message = strip_tags(message)
                                        print('sent message:',plain_message)
                                        # print('file',notice_file)
                                        # sendmail = EmailMessage(
                                        #     title, message, email_from, recipient_list)

                                        # sendmail.attach(notice_file.name,
                                        #                 notice_file.read(), notice_file.content_type)

                                        # response = sendmail.send()
                                        send_mail( title, plain_message, email_from, recipient_list)
                                        # print(response)
                                        # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                        #     message_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                    except:
                                        
                                        owner_notice_sent_save = ""
                                    False

                                


            if category:
                    for roleid in category_s:
                        print('cca')
                        print(roleid)
                        user_list = business_category.objects.filter(id=roleid)
                        for u in user_list:
                            print(u.business_category_name)
                        bb = MerchantProfile.objects.filter(m_business_category = u)
                        print(bb)
                        for user_data in bb:
                            for user_data in bb:
                                print('user_data',user_data)
                                users = GreenBillUser.objects.filter(mobile_no=user_data.m_user )
                                print(users)
                                for u in users:
                                    for notice in sent_notice:
                                        if notice == "sms":
                                            # print(user_data.m_user)
                                            contact = u.mobile_no
                                            message = strip_tags(message)
                                            print('contact',contact)
                                            print(contact)
                                            print(message)
                                            if contact:
    
                                                ts = int(time.time())

                                                data_temp = {
                                                        "keyword":"Bill Delivery SMS",
                                                        "timeStamp":ts,
                                                        "dataSet":
                                                            [
                                                                {
                                                                    "UNIQUE_ID":"GB-" + str(ts),
                                                                    "MESSAGE": message,
                                                                    "OA":smsheader,
                                                                    "MSISDN": contact, # Recipient's Mobile Number
                                                                    "CHANNEL":"SMS",
                                                                    "CAMPAIGN_NAME":"hind_user",
                                                                    "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                                    "USER_NAME":"hind_hsi",
                                                                    "DLT_TM_ID":"1001096933494158", # TM ID
                                                                    "DLT_CT_ID":template_id, # Template Id
                                                                    "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                }
                                                            ]
                                                        }

                                                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                response = requests.post(url, json = data_temp)

                                                # import urllib
                                                # username = "sanjog1"
                                                # Password = "123456"
                                                # sender = "HINDAG"
                                                # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                                # temp_dict = {"text": temp_message}
                                                # message= urllib.parse.urlencode(temp_dict)
                                                # priority='ndnd'
                                                # stype='normal'

                                                # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                                # import requests

                                                # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                                # res = requests.get(url)

                                                # if response.status_code == 200:
                                                #     return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                                # else:
                                                #     return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                                # return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                                # print(sms_response)
                                                # sms_response = sendSMS(str(contact), message)
                                                print(sms_response)
                                            try:
                                                owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                                message_id=notice_object, user_id=user_data.m_user, defaults = {'sent_sms':True})
                                            except:
                                                owner_notice_sent_save = ""


                                        elif notice == "sent_mail":
                                            print('mail')
                                            try:
                                                print('mail2')
                                                # email_id = user_data.m_company_email
                                                email_id = u.email
                                                print('email_id',email_id)
                                                email_from = settings.EMAIL_HOST_USER
                                                print('email from',email_from)
                                                recipient_list = [email_id, 'mohini.d@zappkode.com' ]
                                                # recipient_list = ['shreyash.t@zappkode.com']
                                                print('email to',recipient_list)
                                                message = message
                                                print('sent message:',message)
                                                plain_message = strip_tags(message)
                                                print('sent message:',plain_message)
                                                # print('file',notice_file)
                                                # sendmail = EmailMessage(
                                                #     title, message, email_from, recipient_list)

                                                # sendmail.attach(notice_file.name,
                                                #                 notice_file.read(), notice_file.content_type)

                                                # response = sendmail.send()
                                                send_mail( title, plain_message, email_from, recipient_list)
                                                # print(response)
                                                owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                                    message_id=notice_object, user_id=user_data.m_user, defaults = {'sent_mail':True})

                                            except:
                                                owner_notice_sent_save = ""



            if csv_fields:
                for notice in sent_notice:
                    for number in csv_fields:
                        try:
                            email_id = number
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [email_id ]
                            message = message
                           
                            plain_message = strip_tags(message)
                            send_mail( title, plain_message, email_from, recipient_list)
                        except:
                                    
                            owner_notice_sent_save = ""

            if custom_number:
                for notice in sent_notice:
                    for number in custom_number_list:
                        try:
                            email_id = number
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [email_id ]
                            message = message
                           
                            plain_message = strip_tags(message)
                            send_mail( title, plain_message, email_from, recipient_list)
                        except:
                                    
                            owner_notice_sent_save = ""

            sweetify.success(request, title="Success", icon='success',
                                text='Notice Send successfully!!', timer=5500)
                # return redirect("/owner_notice_board/")
        else:
                sweetify.error(request, title="Error", icon='error',
                                text="Please select either from group or individual list or owner !!!", timer=5500)
        # else:
        #     sweetify.error(request, "Please Provide Valid Data")                

    return render(request, 'super_admin/promotions/bulk_mail.html', context)



def deleteBulkmail(request,id):
    if request.method == "POST":
        instance = bulkMailSmsModel.objects.get(id=id)
        instance.delete()

        return JsonResponse({'success':True})
    return HttpResponse('done!!')




# SCHEDULED EMAIL/SMS


@login_required(login_url="/login/")
def scheduleBulkMailSms(request):
        print('--------------- SCHEDULED EMAIL/SMS -------------------')
        staff = GreenBillUser.objects.filter()
        role_list = merchant_role.objects.all()
        # print(staff)
        for object in staff:
            role_name = merchant_userrole.objects.filter(user_id=object.id)
            # print(role_name)
            for object1 in role_name:
                object.role = object1.id
                object.role_name = object1.role
                newRole = role.objects.filter(role_name = object1.role)
                for oject2 in newRole:
                    object.role_id = oject2.id
       
        category = business_category.objects.all()
        data = bulkMailSmsModel.objects.filter(owner_id = request.user.id).order_by('-id')

        
        if request.method == "POST":
            title = request.POST.get('title')
            message = request.POST.get('message')
            user_group = request.POST.getlist('group')
            category_s = request.POST.getlist('categorychecks')
            print('category', category_s)
            sent_notice = request.POST.getlist('sentnotice')
            print('sent_notice',sent_notice)
            individual_user = request.POST.getlist('individual')
            print('title',title)
            individual = request.POST.getlist('individual')
            print('individual list', individual_user)
            print('individual',individual)
            individualuser = ''
            for i in individual:
                print(i)
                individualuser = i.split(',')
                print('XRAY',individualuser)
            print('message',message)
            print('user_group',user_group)
            smsheader = request.POST.get('smsheader')
            template = request.POST.get('template')
            owner = request.POST.get('checkso')
            merchant = request.POST.get('checksm')
            customer = request.POST.get('checksc')
            partner = request.POST.get('checksp')
            date = request.POST.get('date')
            sms = request.POST.get('sms')
            email = request.POST.get('email')
            print('SMS',sms)
            print('EMAIL',email)
            print('date:::', date)
            print('smsheader',smsheader)
            print('template',template_id)
            print('owner',owner)
            print('merchant',merchant)
            print('customer',customer)
            print('partner',partner)
            
           
            
         
            if individualuser and owner and merchant and customer and category_s :
                print('OWNER',owner)
                sweetify.error(request,text="Please select either from group or individual list !!!", timer=5500)
            elif  individualuser or owner or merchant or customer or partner or category_s:
                print('owner == 1',owner)
                print('indidual', individualuser)
                print('category', category_s)
                for notice in sent_notice:
                        # if notice == "sms":
                        #     notice_id = bulkMailSmsModel.objects.create(
                        #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_sent_sms=True)

                        # elif notice == "sent_mail":
                        #     notice_id = bulkMailSmsModel.objects.create(
                        #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_sent_mail=True)

                        # else:
                        #     notice_id = bulkMailSmsModel.objects.create(
                        #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_notification=True)

                    if notice == "sms":
                            
                            notice_id = bulkMailSmsModel.objects.update_or_create(owner_id=request.user, title=title, message=message, defaults= { 'title':title, 'message':message, 'o_sent_sms':True })

                    elif notice == "sent_mail":
                            
                            notice_id = bulkMailSmsModel.objects.update_or_create(owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template, 'o_sent_mail':True })

                    # else:
                    #     notice_id = bulkMailSmsModel.objects.update_or_create(owner_id=request.user, title=title, message=message, defaults= { 'title':title, 'notice_file': notice_file, 'message':message, 'o_notification':True })

                            print(notice_id[0].id)

                            notice_object = bulkMailSmsModel.objects.get(id= notice_id[0].id)
                            print('notice_object::',notice_object)
                        
                if individualuser:
                        # for notice in sent_notice:
                            for user in individualuser:
                                user_object = GreenBillUser.objects.get(id = user)

                                print(user_object)
                                if notice == "sms":
                                    contact = user_object.mobile_no
                                    message = strip_tags(message)
                                    sms_response = sendSMS(str(contact), message)
                                    if contact:
    
                                        ts = int(time.time())

                                        data_temp = {
                                                "keyword":"Bill Delivery SMS",
                                                "timeStamp":ts,
                                                "dataSet":
                                                    [
                                                        {
                                                            "UNIQUE_ID":"GB-" + str(ts),
                                                            "MESSAGE": message,
                                                            "OA":smsheader,
                                                            "MSISDN": contact, # Recipient's Mobile Number
                                                            "CHANNEL":"SMS",
                                                            "CAMPAIGN_NAME":"hind_user",
                                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                            "USER_NAME":"hind_hsi",
                                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                                            "DLT_CT_ID":template_id, # Template Id
                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                        }
                                                    ]
                                                }

                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                        response = requests.post(url, json = data_temp)

                                        # import urllib
                                        # username = "sanjog1"
                                        # Password = "123456"
                                        # sender = "HINDAG"
                                        # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                        # temp_dict = {"text": temp_message}
                                        # message= urllib.parse.urlencode(temp_dict)
                                        # priority='ndnd'
                                        # stype='normal'

                                        # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                        # import requests

                                        # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                        # res = requests.get(url)

                                        if response.status_code == 200:
                                            return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                        else:
                                            return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                        return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                        print(sms_response)
                                    try:
                                            owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                            message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
                                    except:
                                            owner_notice_sent_save = ""
                                elif notice == "sent_mail":
                                    try:
                                        email_id = user_object.email
                                        
                                        email_from = settings.EMAIL_HOST_USER
                                        print('email from',email_from)
                                        # recipient_list = [email_id, 'shreyash.t@zappkode.com' ]
                                        recipient_list = ['shreyash.t@zappkode.com']
                                        print('email to',recipient_list)
                                        message = message
                                    
                                        plain_message = strip_tags(message)
                                        print('sent message:',plain_message)
                                        # print('file',notice_file)
                                        # sendmail = EmailMessage(
                                        #     title, message, email_from, recipient_list)

                                        # sendmail.attach(notice_file.name,
                                        #                 notice_file.read(), notice_file.content_type)

                                        # response = sendmail.send()
                                        
                                        # schedule.every().day.at("1:53").do(
                                        send_mail( title, plain_message, email_from, recipient_list)
                                        
                                    except:
                                        
                                        owner_notice_sent_save = ""
                            

                
                if owner:
                        print('hello owner')
                        for notice in sent_notice:
                            
                                # print(user)
                                user_object = GreenBillUser.objects.filter(is_staff=True)
                                # print(user_object)
                                for user_o in user_object:
                                    # print(user_o.first_name)
                                    # print(user,"+", user.id)
                                    if notice == "sms":
                                        print('ownr in sms')
                                        contact = user_o.mobile_no
                                        message = strip_tags(message)
                                        if contact:
    
                                            ts = int(time.time())

                                            data_temp = {
                                                    "keyword":"Bill Delivery SMS",
                                                    "timeStamp":ts,
                                                    "dataSet":
                                                        [
                                                            {
                                                                "UNIQUE_ID":"GB-" + str(ts),
                                                                "MESSAGE": message,
                                                                "OA":smsheader,
                                                                "MSISDN": contact, # Recipient's Mobile Number
                                                                "CHANNEL":"SMS",
                                                                "CAMPAIGN_NAME":"hind_user",
                                                                "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                                "USER_NAME":"hind_hsi",
                                                                "DLT_TM_ID":"1001096933494158", # TM ID
                                                                "DLT_CT_ID":template_id, # Template Id
                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                            }
                                                        ]
                                                    }

                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                            response = requests.post(url, json = data_temp)

                                            # import urllib
                                            # username = "sanjog1"
                                            # Password = "123456"
                                            # sender = "HINDAG"
                                            # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                            # temp_dict = {"text": temp_message}
                                            # message= urllib.parse.urlencode(temp_dict)
                                            # priority='ndnd'
                                            # stype='normal'

                                            # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                            # import requests

                                            # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                            # res = requests.get(url)

                                            if response.status_code == 200:
                                                return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                            else:
                                                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                            return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                            print(sms_response)
                                            sms_response = sendSMS(str(contact), message)
                                        try:
                                            owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                            message_id=notice_object, user_id=user_o.m_user, defaults = {'sent_sms':True})
                                        except:
                                            owner_notice_sent_save = ""
                                    elif notice == "sent_mail":
                                        try:
                                            email_id = user_o.email
                                        
                                            email_from = settings.EMAIL_HOST_USER
                                            print('email from',email_from)
                                            # recipient_list = [email_id, 'shreyash.t@zappkode.com' ]
                                            recipient_list = ['shreyash.t@zappkode.com']
                                            print('email to',recipient_list)
                                            message = message
                                            plain_message = strip_tags(message)
                                            print('sent message:',plain_message)
                                            print('sent message:',message)

                                            send_mail( title, plain_message, email_from, recipient_list)
                                            # print(response)
                                            
                                        except:
                                            
                                            owner_notice_sent_save = ""

                                            owner_notice_sent_save = ""
                    
                if merchant:
                        for notice in sent_notice:
                            
                                # print(user)
                                user_object = GreenBillUser.objects.filter(is_merchant=True)
                                # print(user_object)
                                for user in user_object:
                                    # print('users')
                                    # print(user,"+", user.id,"+", user.first_name)
                                    if notice == "sms":
                                        contact = user.mobile_no
                                        message = strip_tags(message)
                                        if contact:
    
                                            ts = int(time.time())

                                            data_temp = {
                                                    "keyword":"Bill Delivery SMS",
                                                    "timeStamp":ts,
                                                    "dataSet":
                                                        [
                                                            {
                                                                "UNIQUE_ID":"GB-" + str(ts),
                                                                "MESSAGE": message,
                                                                "OA":smsheader,
                                                                "MSISDN": contact, # Recipient's Mobile Number
                                                                "CHANNEL":"SMS",
                                                                "CAMPAIGN_NAME":"hind_user",
                                                                "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                                "USER_NAME":"hind_hsi",
                                                                "DLT_TM_ID":"1001096933494158", # TM ID
                                                                "DLT_CT_ID":template_id, # Template Id
                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                            }
                                                        ]
                                                    }

                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                            response = requests.post(url, json = data_temp)

                                            # import urllib
                                            # username = "sanjog1"
                                            # Password = "123456"
                                            # sender = "HINDAG"
                                            # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                            # temp_dict = {"text": temp_message}
                                            # message= urllib.parse.urlencode(temp_dict)
                                            # priority='ndnd'
                                            # stype='normal'

                                            # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                            # import requests

                                            # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                            # res = requests.get(url)

                                            if response.status_code == 200:
                                                return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                            else:
                                                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                            return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                            print(sms_response)
                                            sms_response = sendSMS(str(contact), message)
                                        try:
                                            owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                            message_id=notice_object, user_id=user.m_user, defaults = {'sent_sms':True})
                                        except:
                                            owner_notice_sent_save = ""
                                    elif notice == "sent_mail":
                                        try:
                                            email_id = user.email
                                        
                                            email_from = settings.EMAIL_HOST_USER
                                            print('email from',email_from)
                                            # recipient_list = [email_id, 'shreyash.t@zappkode.com' ]
                                            recipient_list = ['shreyash.t@zappkode.com']
                                            print('email to',recipient_list)
                                            message = message
                                            plain_message = strip_tags(message)
                                            print('sent message:',plain_message)
                                            print('sent message:',message)
                                            # print('file',notice_file)
                                            # sendmail = EmailMessage(
                                            #     title, message, email_from, recipient_list)

                                            # sendmail.attach(notice_file.name,
                                            #                 notice_file.read(), notice_file.content_type)

                                            # response = sendmail.send()
                                            send_mail( title, plain_message, email_from, recipient_list)
                                            # print(response)
                                            # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                            #     message_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                        except:
                                            
                                            owner_notice_sent_save = ""
                    
                if customer:
                        for notice in sent_notice:
                            
                                # print(user)
                                user_object = GreenBillUser.objects.filter(is_customer=True)
                                # print(user_object)
                                for user in user_object:
                                    print('users')
                                    print(user,"+", user.id,"+", user.first_name)
                                    if notice == "sms":
                                        contact = user.mobile_no
                                        message = strip_tags(message)
                                        if contact:
    
                                            ts = int(time.time())

                                            data_temp = {
                                                    "keyword":"Bill Delivery SMS",
                                                    "timeStamp":ts,
                                                    "dataSet":
                                                        [
                                                            {
                                                                "UNIQUE_ID":"GB-" + str(ts),
                                                                "MESSAGE": message,
                                                                "OA":smsheader,
                                                                "MSISDN": contact, # Recipient's Mobile Number
                                                                "CHANNEL":"SMS",
                                                                "CAMPAIGN_NAME":"hind_user",
                                                                "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                                "USER_NAME":"hind_hsi",
                                                                "DLT_TM_ID":"1001096933494158", # TM ID
                                                                "DLT_CT_ID":template_id, # Template Id
                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                            }
                                                        ]
                                                    }

                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                            response = requests.post(url, json = data_temp)

                                            # import urllib
                                            # username = "sanjog1"
                                            # Password = "123456"
                                            # sender = "HINDAG"
                                            # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                            # temp_dict = {"text": temp_message}
                                            # message= urllib.parse.urlencode(temp_dict)
                                            # priority='ndnd'
                                            # stype='normal'

                                            # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                            # import requests

                                            # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                            # res = requests.get(url)

                                            if response.status_code == 200:
                                                return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                            else:
                                                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                            return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                            print(sms_response)
                                            sms_response = sendSMS(str(contact), message)
                                        try:
                                            owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                            message_id=notice_object, user_id=user.m_user, defaults = {'sent_sms':True})
                                        except:
                                            owner_notice_sent_save = ""
                                    elif notice == "sent_mail":
                                        try:
                                            email_id = user.email
                                        
                                            email_from = settings.EMAIL_HOST_USER
                                            print('email from',email_from)
                                            # recipient_list = [email_id, 'shreyash.t@zappkode.com' ]
                                            recipient_list = ['shreyash.t@zappkode.com']
                                            print('email to',recipient_list)
                                            message = message
                                            print('sent message:',message)
                                            plain_message = strip_tags(message)
                                            print('sent message:',plain_message)
                                            # print('file',notice_file)
                                            # sendmail = EmailMessage(
                                            #     title, message, email_from, recipient_list)

                                            # sendmail.attach(notice_file.name,
                                            #                 notice_file.read(), notice_file.content_type)

                                            # response = sendmail.send()
                                            send_mail( title, plain_message, email_from, recipient_list)
                                            # print(response)
                                            # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                            #     message_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                        except:
                                            
                                            owner_notice_sent_save = ""


                    
                if partner:
                        for notice in sent_notice:
                            
                                # print(user)
                                user_object = GreenBillUser.objects.filter(is_partner=True)
                                # print(user_object)
                                for user in user_object:
                                    print('users')
                                    print(user,"+", user.id,"+", user.first_name)
                                    if notice == "sms":
                                        contact = user.mobile_no
                                        message = strip_tags(message)
                                        if contact:
    
                                            ts = int(time.time())

                                            data_temp = {
                                                    "keyword":"Bill Delivery SMS",
                                                    "timeStamp":ts,
                                                    "dataSet":
                                                        [
                                                            {
                                                                "UNIQUE_ID":"GB-" + str(ts),
                                                                "MESSAGE": message,
                                                                "OA":smsheader,
                                                                "MSISDN": contact, # Recipient's Mobile Number
                                                                "CHANNEL":"SMS",
                                                                "CAMPAIGN_NAME":"hind_user",
                                                                "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                                "USER_NAME":"hind_hsi",
                                                                "DLT_TM_ID":"1001096933494158", # TM ID
                                                                "DLT_CT_ID":template_id, # Template Id
                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                            }
                                                        ]
                                                    }

                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                            response = requests.post(url, json = data_temp)

                                            # import urllib
                                            # username = "sanjog1"
                                            # Password = "123456"
                                            # sender = "HINDAG"
                                            # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                            # temp_dict = {"text": temp_message}
                                            # message= urllib.parse.urlencode(temp_dict)
                                            # priority='ndnd'
                                            # stype='normal'

                                            # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                            # import requests

                                            # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                            # res = requests.get(url)

                                            if response.status_code == 200:
                                                return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                            else:
                                                return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                            return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                            print(sms_response) 
                                            sms_response = sendSMS(str(contact), message)
                                        try:
                                            owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                            message_id=notice_object, user_id=user.m_user, defaults = {'sent_sms':True})
                                        except:
                                            owner_notice_sent_save = ""
                                    elif notice == "sent_mail":
                                        try:
                                            email_id = user.email
                                        
                                            email_from = settings.EMAIL_HOST_USER
                                            print('email from',email_from)
                                            # recipient_list = [email_id, 'shreyash.t@zappkode.com' ]
                                            recipient_list = ['shreyash.t@zappkode.com']
                                            print('email to',recipient_list)
                                            message = message
                                            print('sent message:',message)
                                            plain_message = strip_tags(message)
                                            print('sent message:',plain_message)
                                            # print('file',notice_file)
                                            # sendmail = EmailMessage(
                                            #     title, message, email_from, recipient_list)

                                            # sendmail.attach(notice_file.name,
                                            #                 notice_file.read(), notice_file.content_type)

                                            # response = sendmail.send()
                                            send_mail( title, plain_message, email_from, recipient_list)
                                            # print(response)
                                            # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                            #     message_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                        except:
                                            
                                            owner_notice_sent_save = ""
                                        False

                                    


                if category:
                        for roleid in category_s:
                            print('cca')
                            print(roleid)
                            user_list = business_category.objects.filter(id=roleid)
                            for user in user_list:
                                print('business category')
                                print(user.business_category_name)
                            bb = MerchantProfile.objects.filter(m_business_category = user)
                            print('bb')
                            print(bb)
                            for user_data in bb:
                                print('user_data',user_data)
                                users = GreenBillUser.objects.filter(mobile_no=user_data.m_user )
                                print(users)
                                for u in users:
                                    for notice in sent_notice:
                                        if notice == "sms":
                                            # print(user_data.m_user)
                                            contact = u.mobile_no
                                            message = strip_tags(message)
                                            print('contact',contact)
                                            print(contact)
                                            if contact:
    
                                                ts = int(time.time())

                                                data_temp = {
                                                        "keyword":"Bill Delivery SMS",
                                                        "timeStamp":ts,
                                                        "dataSet":
                                                            [
                                                                {
                                                                    "UNIQUE_ID":"GB-" + str(ts),
                                                                    "MESSAGE": message,
                                                                    "OA":smsheader,
                                                                    "MSISDN": contact, # Recipient's Mobile Number
                                                                    "CHANNEL":"SMS",
                                                                    "CAMPAIGN_NAME":"hind_user",
                                                                    "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                                                    "USER_NAME":"hind_hsi",
                                                                    "DLT_TM_ID":"1001096933494158", # TM ID
                                                                    "DLT_CT_ID":template_id, # Template Id
                                                                    "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                }
                                                            ]
                                                        }

                                                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                response = requests.post(url, json = data_temp)

                                                # import urllib
                                                # username = "sanjog1"
                                                # Password = "123456"
                                                # sender = "HINDAG"
                                                # temp_message = "Thank you for saving paper. Here is your digital bill " + str(customer_bill_url) + " To view all your bills, download Green bill App."
                                                # temp_dict = {"text": temp_message}
                                                # message= urllib.parse.urlencode(temp_dict)
                                                # priority='ndnd'
                                                # stype='normal'

                                                # var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                                                # import requests

                                                # url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                                                # res = requests.get(url)

                                                if response.status_code == 200:
                                                    return JsonResponse({'status':'success', 'message': 'SMS send successfully'}, status=200)
                                                else:
                                                    return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)

                                                return JsonResponse({'status':'success',  'message': 'SMS send successfully'}, status=200)
                                                print(sms_response)
                                            sms_response = sendSMS(str(contact), message)
                                            print(sms_response)
                                            try:
                                                owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                                message_id=notice_object, user_id=user_data.m_user, defaults = {'sent_sms':True})
                                            except:
                                                owner_notice_sent_save = ""


                                        elif notice == "sent_mail":
                                            print('mail')
                                            try:
                                                print('mail2')
                                                # email_id = user_data.m_company_email
                                                email_id = u.email
                                                print('email_id',email_id)
                                                email_from = settings.EMAIL_HOST_USER
                                                print('email from',email_from)
                                                # recipient_list = [email_id, 'shreyash.t@zappkode.com' ]
                                                recipient_list = ['shreyash.t@zappkode.com']
                                                print('email to',recipient_list)
                                                message = message
                                                print('sent message:',message)
                                                plain_message = strip_tags(message)
                                                print('sent message:',plain_message)
                                                # print('file',notice_file)
                                                # sendmail = EmailMessage(
                                                #     title, message, email_from, recipient_list)

                                                # sendmail.attach(notice_file.name,
                                                #                 notice_file.read(), notice_file.content_type)

                                                # response = sendmail.send()
                                                send_mail( title, plain_message, email_from, recipient_list)
                                                # print(response)
                                                owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                                    message_id=notice_object, user_id=user_data.m_user, defaults = {'sent_mail':True})

                                            except:
                                                owner_notice_sent_save = ""


                                

                sweetify.success(request, title="Success", icon='success',
                                    text='Notice Send', timer=5500)
                    # return redirect("/owner_notice_board/")
            else:
                    print("OUT OF LOOP")
                    sweetify.error(request, title="Error", icon='error',
                                    text="Please select either from group or individual list  !!!", timer=5500)
            

        context = {
            'all_user': staff,
           
            'merchant_role_list': role_list,
            'merchant_role_name': role_name,
            # 'notice_data': notice_data,
            'category': category,
            'data':data,
            'PromotionNavclass': 'active',
            "PromotionCollapseShow": "show",
            'schedulebulkmailandsmsNavclass':'active',
            'bulkMailSmsForm':bulkMailSmsForm,

        }

            

        return render(request, 'super_admin/promotions/schedule_bulk_mail_sms.html' ,context)




# def search_individual(request):
#     if request.method == "POST":
#         search_str = json.loads(request.body).get('searchText')
#         individual = GreenBillUser.objects.filter(
#             mobile_no__icontains = search_str) | GreenBillUser.objects.filter(
#                 first_name__icontains = search_str) | GreenBillUser.objects.filter(
#                     last_name__icontains  = search_str)

#         data = individual.values()
#         return JsonResponse(list(data), safe=False)


def ActiveGreenBillAds(request, id):
    if request.method == "POST":
        print('id',id)
        merchant_space = ads_below_bill.objects.filter(ads_type='green_bill', active_ads=True).update(take_space = False)

        merchant_space = ads_below_bill.objects.filter(id=id).update(take_space = True)

        return JsonResponse({'status': 'success', 'msg': 'Ads Activated successfully'})
    else:
        return JsonResponse({"status": "error", 'msg': "Something went wrong"})


def DeleteGreenBillAds(request, id):
    ads_obj = ads_below_bill.objects.get(id=id).delete()
    if ads_obj:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": False})

def StoreAds_clicks(request):
    ads_id = request.POST['ads_id']

    table = request.POST['ads_from']
    if table == 'merchant_ads':
        existing_clicks = ads_below_bill.objects.get(id = ads_id).clicks
        updated_clicks = int(existing_clicks) + 1
        ads_below_bill.objects.filter(id = ads_id).update(clicks = updated_clicks)
        return JsonResponse({"status": 'success'})
    else:
        existing_clicks = ads_for_green_bills.objects.get(id = ads_id).clicks
        updated_clicks = int(existing_clicks) + 1
        ads_for_green_bills.objects.filter(id = ads_id).update(clicks = updated_clicks)
        return JsonResponse({"status": 'success'})
