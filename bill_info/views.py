from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
import csv
import io
from django.contrib.auth.decorators import login_required, user_passes_test
import sweetify
from users.models import Merchant_users, MerchantProfile, GreenBillUser,PartnerProfile
from merchant_software_apis.models import CustomerBill, MerchantBill
from petrol_pump_apis.models import SavePetrolPumpBill
from parking_lot_apis.models import SaveParkingLotBill
from datetime import datetime
from django.utils import formats
from merchant_setting.models import Deleted_Bills_By_Days_setting
from app.views import is_merchant_or_merchant_staff, getActiveSubscriptionPlan

from partner_my_subscription.models import *

from bill_design.models import *

from my_subscription.models import *
from merchant_setting.models import *
import string

# SMS
import requests
import time
import pyshorteners
from datetime import date
from my_subscription.models import *

from category_and_tags.models import bill_category, bill_tags

from my_subscription.models import *

from django.db.models import Q
from django.utils import timezone
import random
@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def bill_info_view(request):

    mer_user_id = Merchant_users.objects.get(user_id=request.user)  

    merchant_object = mer_user_id.merchant_user_id # merchant mob. no
    
    merchant_business_object = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)  # business name
     
    merchant_business_id = merchant_business_object.id   #business id ex 1120
    
    merchant_user = []       #list of merchant and it's users number

    merchant_user.append({
        'user_id': merchant_object
    })

    merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = merchant_business_id)
     # list of users
    for user in merchant_user_temp:
        merchant_user.append({
            'user_id': user.user_id                        # list of merchant users number
            })
         
    data = []

    base_url = "http://157.230.228.250/"

    try:
        bill_design = bill_designs.objects.get(merchant_business_id = merchant_business_object)
        bill_rating_emoji = bill_design.rating_emoji
    except:
        bill_rating_emoji = "⭐"
    try:
        print("In try")
        deleted_bill_object = Deleted_Bills_By_Days_setting.objects.get(m_user=request.user)
        print(deleted_bill_object)
        daytime = deleted_bill_object.date_entered

        days = deleted_bill_object.delete_days_merchant
        # print(daytime.date())
        # print(type(daytime))
        day = daytime.date()
        # print(day)
        # dayint = int(day)
        # print(dayint)
        panel = deleted_bill_object.delete_from_merchant
        print(panel)
    except:
        panel = "none"   
    print("Out of panel")
    print(panel)
    if panel == 1:
        print("in panel")
        parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False).order_by('-id')
        
        for bill in parking_bill_list:
            bill_date = bill.created_at.date()
            # print(type(bill_date))
            current_date = date.today() 
            # print(type(current_date))
            diff_date = (current_date-bill_date)

            print(type(diff_date))
            if diff_date.days <= int(days) :
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

                if bill.is_checkoutpin == True:
                    try:
                        mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                    except:
                        mobile_no = bill.mobile_no
                else:
                    mobile_no = bill.mobile_no

                data.append({
                    'bill_id': bill.id,
                    'invoice_no': bill.invoice_no,
                    'mobile_no': mobile_no,
                    'reject_status': bill.reject_status,
                    'amount': str(bill.amount),
                    'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                    'bill_file': bill_file,
                    'db_table': "SaveParkingLotBill",
                    'bill_url': bill.bill_url,
                    'customer_added': False,
                    'bill_ratings': ratings,
                    'rating': bill.rating,
                    'created_by': created_by,
                    'created_by_id': created_by_id,
                    'bill_flag': bill.bill_flag,
                    'flag_by': bill.flag_by,
                    'created_at': bill.created_at,
                    'is_checkoutpin': bill.is_checkoutpin,
                    'url': str(base_url) + "parking-lot-bill/" + str(bill.bill_url) + "/"
                })

        petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id).order_by('-id')

        for bill in petrol_bill_list:
            bill_date = bill.created_at.date()
             
            current_date = date.today() 
             
            diff_date = (current_date-bill_date)
            if diff_date.days <= int(day) :
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

                if bill.is_checkoutpin == True:
                    try:
                        mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                    except:
                        mobile_no = bill.mobile_no
                else:
                    mobile_no = bill.mobile_no

                data.append({
                    'bill_id': bill.id,
                    'invoice_no': bill.invoice_no,
                    'mobile_no': mobile_no,
                    'reject_status': bill.reject_status,
                    'amount': str(bill.total_amount),
                    'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                    'bill_file': bill_file,
                    'db_table': "SavePetrolPumpBill",
                    'bill_url': bill.bill_url,
                    'customer_added': False,
                    'bill_ratings': ratings,
                    'rating': bill.rating,
                    'created_by': created_by,
                    'created_by_id': created_by_id,
                    'bill_flag': bill.bill_flag,
                    'flag_by': bill.flag_by,
                    'created_at': bill.created_at,
                    'is_checkoutpin': bill.is_checkoutpin,
                    'url':str(base_url) + "petrol-pump-bill/" + str(bill.bill_url) + "/"
                })

        customer_bill_list = CustomerBill.objects.filter(business_name = merchant_business_object, customer_added = False).order_by('-id')
# for habrone 
        is_merchant_partner = merchant_business_object.merchant_by_partner
        for bill in customer_bill_list:
            bill_date = bill.created_at.date()
            print(bill_date)
            current_date = date.today() 
            print(type(current_date))
            diff_date = (current_date-bill_date)
            print(type(diff_date))
            if diff_date.days <= int(days) :
                try:
                    bill_file = str(base_url) + str(bill.bill.url)
                except:
                    bill_file = ""
                
                ratings = ""

                if bill.customer_added == True:
                    url = str(base_url) + 'self-added-bill/' + str(bill.bill_url) + "/"
                else:
                    if is_merchant_partner:
                        url = str(base_url) + 'my-green-bill/' + str(bill.bill_url) + "/"
                    else:

                        url = str(base_url) + 'my-bill/' + str(bill.bill_url) + "/"

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


                if bill.is_checkoutpin == True:
                    try:
                        mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                    except:
                        mobile_no = bill.mobile_no
                else:
                    mobile_no = bill.mobile_no

                data.append({
                    'bill_id': bill.id,
                    'invoice_no': bill.invoice_no,
                    'mobile_no': mobile_no,
                    'reject_status': bill.reject_status,
                    'amount': str(bill.bill_amount),
                    'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'bill_file': bill_file,
                    'db_table': "CustomerBill",
                    'bill_url': bill.bill_url,
                    'customer_added': False,
                    'bill_ratings': ratings,
                    'rating': bill.rating,
                    'created_by': created_by,
                    'created_by_id': created_by_id,
                    'bill_flag': False,
                    'created_at': bill.created_at,
                    'is_checkoutpin': bill.is_checkoutpin,
                    'url':url,
                })

        merchant_bill_list = MerchantBill.objects.filter(business_name = merchant_business_object).order_by('-id')

        for bill in merchant_bill_list:
            bill_date = bill.created_at.date()
             
            current_date = date.today() 
             
            diff_date = (current_date-bill_date).days
            if diff_date <= int(days) :
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

                if bill.is_checkoutpin == True:
                    try:
                        mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                    except:
                        mobile_no = bill.mobile_no
                else:
                    mobile_no = bill.mobile_no

                data.append({
                    'bill_id': bill.id,
                    'invoice_no': bill.invoice_no,
                    'mobile_no': mobile_no,
                    'reject_status': bill.reject_status,
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
                    'created_at': bill.created_at,
                    'is_checkoutpin': bill.is_checkoutpin,
                    'url': str(base_url) + 'my-bill-merchant/' + str(bill.bill_url) + "/"
                })
    else:

        print("in panel1")

        parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False).order_by('-id')
        print(parking_bill_list,"--------------------------------------")
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

            if bill.is_checkoutpin == True:
                try:
                    mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                except:
                    mobile_no = bill.mobile_no
            else:
                mobile_no = bill.mobile_no

            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': mobile_no,
                'reject_status': bill.reject_status,
                'amount': str(bill.amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SaveParkingLotBill",
                'bill_url': bill.bill_url,
                'customer_added': False,
                'bill_ratings': ratings,
                'rating': bill.rating,
                'created_by': created_by,
                'created_by_id': created_by_id,
                'bill_flag': bill.bill_flag,
                'flag_by': bill.flag_by,
                'created_at': bill.created_at,
                'is_checkoutpin': bill.is_checkoutpin,
                'url': str(base_url) + "parking-lot-bill/" + str(bill.bill_url) + "/"
            })

        petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id).order_by('-id')
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

            if bill.is_checkoutpin == True:
                try:
                    mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                except:
                    mobile_no = bill.mobile_no
            else:
                mobile_no = bill.mobile_no

            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': mobile_no,
                'reject_status': bill.reject_status,
                'amount': str(bill.total_amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SavePetrolPumpBill",
                'bill_url': bill.bill_url,
                'customer_added': False,
                'bill_ratings': ratings,
                'rating': bill.rating,
                'created_by': created_by,
                'created_by_id': created_by_id,
                'bill_flag': bill.bill_flag,
                'flag_by': bill.flag_by,
                'created_at': bill.created_at,
                'is_checkoutpin': bill.is_checkoutpin,
                'url':str(base_url) + "petrol-pump-bill/" + str(bill.bill_url) + "/"
            })

        customer_bill_list = CustomerBill.objects.filter(business_name = merchant_business_object, customer_added = False).order_by('-id')
        
        print("*************")
        print(customer_bill_list)
        # for habrone condition here

        is_merchant_partner = merchant_business_object.merchant_by_partner 

        for bill in customer_bill_list:
            try:
                bill_file = str(base_url) + str(bill.bill.url)
            except:
                bill_file = ""
            
            ratings = ""

            if bill.customer_added == True:
                url = str(base_url) + 'self-added-bill/' + str(bill.bill_url) + "/"
            else:
                if is_merchant_partner:
                    url = str(base_url) + 'my-green-bill/' + str(bill.bill_url) + "/"
                else:

                    url = str(base_url) + 'my-bill/' + str(bill.bill_url) + "/"

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


            if bill.is_checkoutpin == True:
                try:
                    mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                except:
                    mobile_no = bill.mobile_no
            else:
                mobile_no = bill.mobile_no

            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': mobile_no,
                'reject_status': bill.reject_status,
                'amount': str(bill.bill_amount),
                'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "CustomerBill",
                'bill_url': bill.bill_url,
                'customer_added': False,
                'bill_ratings': ratings,
                'rating': bill.rating,
                'created_by': created_by,
                'created_by_id': created_by_id,
                'bill_flag': False,
                'created_at': bill.created_at,
                'is_checkoutpin': bill.is_checkoutpin,
                'url':url,
            })

        merchant_bill_list = MerchantBill.objects.filter(business_name = merchant_business_object).order_by('-id')

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

            if bill.is_checkoutpin == True:
                try:
                    mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
                except:
                    mobile_no = bill.mobile_no
            else:
                mobile_no = bill.mobile_no

            data.append({
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': mobile_no,
                'reject_status': bill.reject_status,
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
                'created_at': bill.created_at,
                'is_checkoutpin': bill.is_checkoutpin,
                'url': str(base_url) + 'my-bill-merchant/' + str(bill.bill_url) + "/"
            })

    data.sort(key = lambda x: x['created_at'], reverse = True)

    total_bills_created = 0
    total_amount_collected = 0
    total_flag_bills = 0
    total_reject_count = 0 

    for bill in data:
        total_bills_created = total_bills_created + 1
        if bill['reject_status'] == True:
            total_reject_count = total_reject_count + 1
        else:
            total_amount_collected = float(total_amount_collected) + float(bill['amount'])

        if bill['bill_flag'] == True:
            total_flag_bills = total_flag_bills + 1

    context= {}
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
                bill_date = datetime.strptime(str(bill['bill_date']), '%d-%m-%Y').strftime('%Y-%m-%d')
                if from_date and to_date:
                    
                    if bill_date >= from_date and bill_date <= to_date:
                        new_data.append(bill)
                elif from_date:
                    if bill_date >= from_date:
                        new_data.append(bill)

                elif to_date:
                    if bill_date <= to_date:
                        new_data.append(bill)
                

            total_bills_created = 0
            total_amount_collected = 0
            total_flag_bills = 0
            total_reject_count = 0
           

            for bill in new_data:
                total_bills_created = total_bills_created + 1
                if bill['reject_status'] == True:
                    total_reject_count = total_reject_count + 1
                else:
                    total_amount_collected = float(total_amount_collected) + float(bill['amount'])

                if bill['bill_flag'] == True:
                    total_flag_bills = total_flag_bills + 1

            # new_data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)
            new_data.sort(key = lambda x: x['created_at'], reverse = True)

            context = {
                "bills":new_data,
                'BillInfoNavClass':'active',
                'SentBillsNavClass': 'active',
                "BillInfoCollapseShow": "show",
                'merchant_user': merchant_user,
                'from_date': from_date_temp,
                'to_date': to_date_temp,
                'total_bills_created': total_bills_created,
                'total_amount_collected':total_amount_collected,
                'total_reject_count': total_reject_count,
            }
            print("in if ")
            # print(context['bills'])

        return render(request, "merchant/bill_info/bill-info.html", context)

    else:
        data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)
        context = {
            "bills":data,
            'BillInfoNavClass':'active',
            'SentBillsNavClass': 'active',
            "BillInfoCollapseShow": "show",
            'merchant_user': merchant_user,
            'merchant_business_category_id': merchant_business_object.m_business_category.id,
            'total_bills_created': total_bills_created,
            'total_amount_collected':total_amount_collected,
            'total_reject_count': total_reject_count,
        }
        print("in e")
        # print(context['bills'])

        return render(request, "merchant/bill_info/bill-info.html", context)

@login_required(login_url="/merchant-login/")
def BillInfoSendBillSMSWeb(request, id):
    
    bill_id = id
    mobile_no = request.POST["mobile_no"]
    db_table = request.POST["db_table"]


    mer_user_id = Merchant_users.objects.get(user_id=request.user)

    merchant_object = mer_user_id.merchant_user_id
    
    merchant_business_object = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    merchant_business_id = merchant_business_object.id

    subscription_object = getActiveSubscriptionPlan(request, merchant_business_id)

    if subscription_object and mobile_no:

        if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

            if db_table == "CustomerBill":
                bill_object = CustomerBill.objects.get(id = bill_id)
                amount = bill_object.bill_amount
                customer_bill_url = "http://157.230.228.250/my-bill/" + str(bill_object.bill_url) + "/"
                merchant_bill = False
                customer_bill = True
                parking_bill = False
                petrol_bill = False


            elif db_table == "MerchantBill":
                bill_object = MerchantBill.objects.get(id = bill_id)
                amount = bill_object.bill_amount
                customer_bill_url = "http://157.230.228.250/my-bill-merchant/" + str(bill_object.bill_url) + "/"
                merchant_bill = True
                customer_bill = False
                parking_bill = False
                petrol_bill = False

            elif db_table == "SaveParkingLotBill":
                bill_object = SaveParkingLotBill.objects.get(id = bill_id)
                amount = bill_object.amount
                customer_bill_url = "http://157.230.228.250/parking-lot-bill/" + str(bill_object.bill_url) + "/"
                merchant_bill = False
                customer_bill = False
                parking_bill = True
                petrol_bill = False

            elif db_table == "SavePetrolPumpBill":
                bill_object = SavePetrolPumpBill.objects.get(id = bill_id)
                amount = bill_object.total_amount
                customer_bill_url = "http://157.230.228.250/petrol-pump-bill/" + str(bill_object.bill_url) + "/"
                merchant_bill = False
                customer_bill = False
                parking_bill = False
                petrol_bill = True

            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(customer_bill_url)

            if db_table == "CustomerBill" or db_table == "MerchantBill":

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

            elif db_table == "SaveParkingLotBill":

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

            elif db_table == "SavePetrolPumpBill":

                ts = int(time.time())
                data_temp = {
                        "keyword":"Bill Delivery SMS",
                        "timeStamp":ts,
                        "dataSet":
                            [
                                {
                                    "UNIQUE_ID":"GB-" + str(ts),
                                    "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
                                    "OA":"GBPUMP",
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

                sent_bill_history.objects.create(subscription_id = subscription_object.id, user_id = request.user.id,
                    mobile_no = mobile_no, m_business_id = merchant_business_object.id, bill_amount = amount,
                    merchant_bill = merchant_bill, customer_bill = customer_bill, parking_bill = parking_bill, petrol_bill = petrol_bill,
                    sms_bill = True, bill_cost = subscription_object.per_bill_cost
                )

                return JsonResponse({"success": True, "status": "success"})
            else:
                return JsonResponse({"success": False, "status": "error", "message": "Fail to send SMS !!!"})
        else:
            return JsonResponse({"success": False, "status": "error", "message":"Insufficient Balance. Please purchase new plan and try again !!!"})
    else:
        return JsonResponse({"success": False, "status": "error", "message":"You don't have active Green Bill Subscription. Please purchase and try again."})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def received_bills_view(request):

    mer_user_id = Merchant_users.objects.get(user_id=request.user)

    merchant_object = mer_user_id.merchant_user_id
    
    merchant_business_object = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
    
    current_business_name = merchant_business_object.m_business_name

    # print('aa',merchant_business_object.id)

    merchant_business_name = MerchantProfile.objects.filter(m_user = request.user)

    business_name_dictionary = []
    for business in merchant_business_name:
        if merchant_business_object.id != business.id:
            business_name_dictionary.append({
                'id': business.id,
                'send_merchant_business': business.m_business_name,

            })

    # print('dict',business_name_dictionary)


    # print('merchant_business_name',merchant_business_name)

    data = []

    merchant_bill_list = MerchantBill.objects.filter(bill_received_business_name = merchant_business_object.id).order_by('-id')
    
    # print(merchant_bill_list)

    # print(merchant_bill_list)

    base_url = "http://157.230.228.250/"

    for bill in merchant_bill_list:
        try:
            bill_file = str(base_url) + str(bill.bill.url)  
            
        except:
            bill_file = ""
        
        try:
            user_object = GreenBillUser.objects.get(id = bill.user_id)
            created_by_id = user_object.id
            created_by = user_object.first_name + ' ' + user_object.last_name
        except:
            created_by = ""
            created_by_id = ""

        if bill.is_checkoutpin == True:
            try:
                mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
            except:
                mobile_no = bill.mobile_no
        else:
            mobile_no = bill.mobile_no


        data.append({
            'bill_id': bill.id,
            'invoice_no': bill.invoice_no,
            'mobile_no': mobile_no,
            'amount': str(bill.bill_amount),
            'business': bill.business_name,
            'date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
            'bill_file': bill.bill,
            'db_table': "MerchantBill",
            'customer_added': False,
            'created_by': created_by,
            'created_by_id': created_by_id,
            'bill_flag': False,
            'bill_url': bill.bill_url,
            'created_at': bill.created_at,
        })

    startswith = str(merchant_business_object.id) + ','
    endswith = ','+ str(merchant_business_object.id)
    contains = ','+ str(merchant_business_object.id) + ','
    exact = str(merchant_business_object.id)

    recharge_his = recharge_history.objects.filter(
        Q(merchant_id = merchant_object),
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
        try:
            data.append({
                'bill_id': recharge.id,
                'invoice_no': recharge.invoice_no,
                'mobile_no': '',
                'amount': str(final_amount),
                'business': 'Green Bill',
                'date': datetime.strptime(str(purchase_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'bill_file': '',
                'db_table': "recharge_history",
                'customer_added': '',
                'created_by': '',
                'created_by_id': '',
                'bill_flag': '',
                'bill_url': '',
                'created_at': recharge.purchase_date,
            })
        except:
            pass

    data.sort(key = lambda x: x['created_at'], reverse = True)
    # data.sort(key = lambda x: datetime.strptime(x['created_at'], '%d-%m-%Y'), reverse = True)

    received_bills = 0
    received_amount = 0

    for a in data:
        received_bills = received_bills + 1
    for b in data:
        received_amount =  float(received_amount) + float(b['amount'])
    
    if request.method == "POST":
        user = request.POST.get('user')
        from_date = request.POST['from_date']
        from_date_temp1 = from_date
        to_date = request.POST['to_date']
        to_date_temp1 = to_date

        new_data = []

        if data:
            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')
                
            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')
                
            for bill in data:
                if from_date and to_date:
                    bill_date = datetime.strptime(str(bill['date']), '%d-%m-%Y').strftime('%Y-%m-%d')
                    if bill_date >= from_date and bill_date <= to_date:
                        new_data.append(bill)

                elif from_date:
                    bill_date = datetime.strptime(str(bill['date']), '%d-%m-%Y').strftime('%Y-%m-%d')
                    if bill_date >= from_date:
                        new_data.append(bill)

                elif to_date:
                    bill_date = datetime.strptime(str(bill['date']), '%d-%m-%Y').strftime('%Y-%m-%d')
                    if bill_date <= to_date:
                        new_data.append(bill)

                        

        received_amount = 0
        received_bills = 0

        for z in new_data:
            received_amount =  float(received_amount) + float(z['amount'])
        received_bills = len(new_data)
        # new_data.sort(key = lambda x: datetime.strptime(x['date'], '%d-%m-%Y'), reverse = True)
        data.sort(key = lambda x: x['created_at'], reverse = True)   
        context = {
                'business_name_dictionary': business_name_dictionary,
                "bills":new_data,
                'BillInfoNavClass':'active',
                'ReceivedBillsNavClass': 'active',
                "BillInfoCollapseShow": "show",
                'from_date': from_date_temp1,
                'to_date': to_date_temp1,
                'mobile_no': request.user,
                'received_amount' : received_amount,
                'received_bills' : received_bills,
                }      
        return render(request, "merchant/bill_info/received-bills.html", context)

    else:
        data.sort(key = lambda x: datetime.strptime(x['date'], '%d-%m-%Y'), reverse = True)
        context = {
        'business_name_dictionary': business_name_dictionary,
        "bills":data,
        'BillInfoNavClass':'active',
        'ReceivedBillsNavClass': 'active',
        "BillInfoCollapseShow": "show",
        'mobile_no': request.user,
        'received_bills' : received_bills,
        'received_amount' : received_amount,

    }

    return render(request, "merchant/bill_info/received-bills.html", context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def send_bill_to_merchant(request):
    if request.method == "POST":
        if request.POST['merchant_business_id'] == 'customer':

            send_bill_id = request.POST['send_bill_id']
            merchant_bill = MerchantBill.objects.filter(id =send_bill_id)

            letters = string.ascii_letters
            digit = string.digits
            random_string = str(merchant_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

            customer_bill = CustomerBill.objects.create(user_id = merchant_bill[0].user_id, mobile_no = merchant_bill[0].mobile_no,
                email = merchant_bill[0].email, bill = merchant_bill[0].bill, business_name = merchant_bill[0].business_name,
                invoice_no = merchant_bill[0].invoice_no, green_bill_transaction = merchant_bill[0].green_bill_transaction, green_bill_print_transaction = merchant_bill[0].green_bill_print_transaction,
                print_transaction = merchant_bill[0].print_transaction, bill_amount = merchant_bill[0].bill_amount, customer_bill_category = merchant_bill[0].customer_bill_category,stamp_id=merchant_bill[0].stamp_id, exe_bill_type = merchant_bill[0].exe_bill_type
            )

            history_result1 = sent_bill_history.objects.create(user_id = merchant_bill[0].user_id,
                mobile_no = merchant_bill[0].mobile_no, m_business_id = merchant_bill[0].business_name.id, green_bill_print_transaction = merchant_bill[0].green_bill_print_transaction,
                print_transaction = merchant_bill[0].print_transaction, bill_amount = merchant_bill[0].bill_amount,
                customer_bill = True
            )

            customer_bill_new = CustomerBill.objects.filter(id=customer_bill.id).update(bill_url = random_string) 

            MerchantBill.objects.filter(id =send_bill_id).delete()

            if customer_bill_new:
                sweetify.success(request, title="success", icon='success', text='Bill Transfer successfully !!!', timer=1500)
                return redirect(received_bills_view)
            else:
                sweetify.error(request, title="error", icon='error', text='Failed to Transfer!!!', timer=1500)
                return redirect(received_bills_view)

        else:
            send_bill_id = request.POST['send_bill_id']
            merchant_bill = MerchantBill.objects.filter(id =send_bill_id)

            merchant_business_id = request.POST['merchant_business_id']

            letters = string.ascii_letters
            digit = string.digits
            random_string = str(merchant_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

            merchant_bill1 = MerchantBill.objects.create(user_id = merchant_bill[0].user_id, mobile_no = merchant_bill[0].mobile_no, email = merchant_bill[0].email,
                bill = merchant_bill[0].bill, business_name = merchant_bill[0].business_name, bill_received_business_name = merchant_business_id,
                invoice_no = merchant_bill[0].invoice_no, green_bill_transaction = merchant_bill[0].green_bill_transaction, green_bill_print_transaction = merchant_bill[0].green_bill_print_transaction,
                print_transaction = merchant_bill[0].print_transaction, bill_amount = merchant_bill[0].bill_amount, customer_bill_category = merchant_bill[0].customer_bill_category,stamp_id=merchant_bill[0].stamp_id, exe_bill_type = merchant_bill[0].exe_bill_type
            )

            # startswith = str(merchant_bill[0].business_name.id) + ','
            # endswith = ','+ str(merchant_bill[0].business_name.id)
            # contains = ','+ str(merchant_bill[0].business_name.id) + ','
            # exact = str(merchant_bill[0].business_name.id)
            # try:
            #     subscription_object = merchant_subscriptions.objects.get(
            #         Q(is_active = True),
            #         Q(business_ids__startswith = startswith) | 
            #         Q(business_ids__endswith = endswith) | 
            #         Q(business_ids__contains = contains) | 
            #         Q(business_ids__exact = exact)
            #     )
            # except:
            #     subscription_object = ""

            # if subscription_object:
            #     history_result = sent_bill_history.objects.create(subscription_id = subscription_object.id, user_id = merchant_bill[0].user_id,
            #         mobile_no = merchant_bill[0].mobile_no, m_business_id = merchant_bill[0].business_name.id, green_bill_transaction = merchant_bill[0].green_bill_transaction, green_bill_print_transaction = merchant_bill[0].green_bill_print_transaction,
            #         print_transaction = merchant_bill[0].print_transaction, bill_amount = merchant_bill[0].bill_amount,
            #         merchant_bill = True
            #     )
            merchant_bill_new = MerchantBill.objects.filter(id=merchant_bill1.id).update(bill_url = random_string) 

            merchant_bill = MerchantBill.objects.filter(id =send_bill_id).delete()

            if merchant_bill_new:
                sweetify.success(request, title="success", icon='success', text='Bill Transfer successfully !!!', timer=1500)
                return redirect(received_bills_view)
            else:
                sweetify.error(request, title="error", icon='error', text='Failed to Transfer!!!', timer=1500)
                return redirect(received_bills_view)
            

    #     id = request.POST["send_bill_id"]
    #     merchant_name = request.POST["send_bill_to_merchant"]
    #     object = MerchantBill.objects.filter(bill_received_business_name = merchant_name)
        
    #     merchant_bill_list = MerchantBill.objects.filter(id = id).update(bill_received_business_name = merchant_name)

    #     sweetify.success(request, title="success", icon='success', text='Bill Transfer successfully !!!', timer=1500)
    #     return redirect(received_bills_view)
    # else: 
    



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def rejected_bills_view(request):

    mer_user_id = Merchant_users.objects.get(user_id=request.user)

    merchant_object = mer_user_id.merchant_user_id

    merchant_business_object = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    data = []

    customer_bill = CustomerBill.objects.filter(reject_status = True, customer_added = False, business_name = merchant_business_object).order_by("-id")

    for bill in customer_bill:

        if bill.is_checkoutpin == True:
            try:
                mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
            except:
                mobile_no = bill.mobile_no
        else:
            mobile_no = bill.mobile_no

        data.append({
            "id": bill.id,
            "invoice_no": bill.invoice_no,
            "mobile_no": mobile_no,
            "bill_amount": bill.bill_amount,
            "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
            'db_table': "CustomerBill",
            'reject_reason': bill.reject_reason,
            'created_at': bill.created_at,
        })


    parking_bill = SaveParkingLotBill.objects.filter(reject_status = True, m_business_id = merchant_business_object.id).order_by("-id")

    for bill in parking_bill:

        if bill.is_checkoutpin == True:
            try:
                mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
            except:
                mobile_no = bill.mobile_no
        else:
            mobile_no = bill.mobile_no

        data.append({
            "id": bill.id,
            "invoice_no": bill.invoice_no,
            "mobile_no": mobile_no,
            "bill_amount": bill.amount,
            "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
            'db_table': "SaveParkingLotBill",
            'reject_reason': bill.reject_reason,
            'created_at': bill.created_at,
        })

    petrol_bill = SavePetrolPumpBill.objects.filter(reject_status = True, m_business_id = merchant_business_object.id).order_by("-id")

    for bill in petrol_bill:

        if bill.is_checkoutpin == True:
            try:
                mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
            except:
                mobile_no = bill.mobile_no
        else:
            mobile_no = bill.mobile_no

        data.append({
            "id": bill.id,
            "invoice_no": bill.invoice_no,
            "mobile_no": mobile_no,
            "bill_amount": bill.total_amount,
            "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
            'db_table': "SavePetrolPumpBill",
            'reject_reason': bill.reject_reason,
            'created_at': bill.created_at,
        })

    merch_bill = MerchantBill.objects.filter(reject_status =True, business_name = merchant_business_object.id).order_by("-id")

    for bill in merch_bill:

        if bill.is_checkoutpin == True:
            try:
                mobile_no = GreenBillUser.objects.get(mobile_no = bill.mobile_no).c_unique_id
            except:
                mobile_no = bill.mobile_no
        else:
            mobile_no = bill.mobile_no

        data.append({
            "id" : bill.id,
            "invoice_no": bill.invoice_no,
            "mobile_no": mobile_no,
            "bill_amount": bill.bill_amount,
            "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%Y-%m-%d'),
            'db_table': "MerchantBill",
            'reject_reason': bill.reject_reason,
            'created_at': bill.created_at,
            })


    # data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)
    data.sort(key = lambda x: x['created_at'], reverse = True)
    rejected_amt = 0
    rejected_bills = 0
    for s in data:
        rejected_amt =  float(rejected_amt) + float(s['bill_amount'])

    for j in data:
        rejected_bills = rejected_bills + 1  


    if request.method == "POST":
        user = request.POST.get("user")
        from_date = request.POST['from_date']
        from_date_var = from_date
        to_date = request.POST['to_date']
        to_date_var = to_date

        new_data = []

        if data:
            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')

            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')

            for bill in data:

                # if user and from_date and to_date:
                #     if bill['created_by_id'] == int(user):
                #         if bill['bill_date'] >= from_date and bill['bill_date'] <= to_date:
                #             new_data.append(bill)

                if from_date and to_date:
                    bill_date = datetime.strptime(str(bill['bill_date']), '%Y-%m-%d').strftime('%Y-%m-%d')
                    if bill_date >= from_date and bill_date <= to_date:
                        new_data.append(bill)

                # if from_date and to_date:
                #     bill_date = datetime.strptime(str(bill['bill_date']), '%d-%m-%Y').strftime('%Y-%m-%d')
                #     if bill_date >= from_date and bill_date <= to_date:
                #         new_data.append(bill)

                # elif user and from_date :
                #     if bill['created_by_id'] == int(user) and bill['bill_date'] >= from_date:
                #         new_data.append(bill)

                # elif user and to_date:
                #     if bill['created_by_id'] == int(user) and bill['bill_date'] <= to_date:
                #         new_data.append(bill)

                # elif from_date:
                #     if bill['bill_date'] >= from_date:
                #         new_data.append(bill)

                # elif to_date:
                #     if bill['bill_date'] <= to_date:
                #         new_data.append(bill)

                # elif user:
                #     if bill['created_by_id'] == int(user):
                #         new_data.append(bill)

            new_data.sort(key = lambda x: x['created_at'], reverse = True)
        rejected_amt = 0
        rejected_bills = 0
        for z in new_data:
        	rejected_amt =  float(rejected_amt) + float(z['bill_amount'])
        rejected_bills = len(new_data)
        context = {
                    "bills":new_data,
                    'BillInfoNavClass':'active',
                    'RejectedBillsNavClass': 'active',
                    "BillInfoCollapseShow": "show",
                    #'merchant_user': merchant_user,
                    #'total_flag_bills':total_flag_bills,
                    #'custom_user': int(user),
                    'from_date': from_date_var,
                    'to_date': to_date_var,
                    'rejected_amt' : rejected_amt,
                    'rejected_bills' : rejected_bills,
                }

    else:
    	context = {
                    "bills": data,
			        'BillInfoNavClass':'active',
			        'RejectedBillsNavClass': 'active',
			        "BillInfoCollapseShow": "show",
			        'rejected_amt' : rejected_amt,
			        'rejected_bills' : rejected_bills,
    }
    return render(request, "merchant/bill_info/rejected-bills.html", context)

    # context = {
    #     "bills": data,
    #     'BillInfoNavClass':'active',
    #     'RejectedBillsNavClass': 'active',
    #     "BillInfoCollapseShow": "show",
    #     'rejected_amt' : rejected_amt,
    #     'rejected_bills' : rejected_bills,
    # }

    # return render(request, "merchant/bill_info/rejected-bills.html", context)


    # context = {
    #     "bills": data,
    #     'BillInfoNavClass':'active',
    #     'RejectedBillsNavClass': 'active',
    #     "BillInfoCollapseShow": "show",
    # }

    # return render(request, "merchant/bill_info/rejected-bills.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def delete_rejected_bill_view(request, id):

    if request.method == "POST":

        db_table = request.POST["db_table"]
        # print("##########################")
        # print(db_table)

        if db_table == "CustomerBill":
            instance = CustomerBill.objects.get(id=id)

        elif db_table == "SaveParkingLotBill":
            instance = SaveParkingLotBill.objects.get(id=id)

        elif db_table == "SavePetrolPumpBill":
            instance = SavePetrolPumpBill.objects.get(id=id)
        else:
            instance = MerchantBill.objects.get(id=id)
        
        # print("##########################")
        # print(db_table)
        status = instance.delete()

        if status:
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'error'})
    else: 
        return JsonResponse({'status':'error'})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def delete_selected_rejected_bills_view(request):

    if request.method == "POST":

        bill_ids = request.POST.getlist('bill_id[]')
        print(bill_ids)
        
        if bill_ids:

            for bill_id in bill_ids:
                print("******************")
                print(bill_id)

                split_data = bill_id.split("~")

                id = split_data[0]

                db_table = split_data[1]
                print("##########################")
                print(db_table)
                if db_table == "CustomerBill":
                    instance = CustomerBill.objects.get(id=id)

                elif db_table == "SaveParkingLotBill":
                    instance = SaveParkingLotBill.objects.get(id=id)

                elif db_table == "SavePetrolPumpBill":
                    instance = SavePetrolPumpBill.objects.get(id=id)
                else:
                    instance = MerchantBill.objects.get(id=id)


                instance.delete()

                result = True
        else:
            result = False
        
        if result:
            sweetify.success(request, title="Success", icon='success', text='Bills deleted Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="error", icon='error', text='Please Select Bill !!!', timer=1500)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Bill!!!', timer=1500)
        
    return redirect(rejected_bills_view)

def owner_sent_bills_view(request):

    # merchant_bill_list = MerchantBill.objects.all()         

    all_merchants = MerchantProfile.objects.all()

    all_partner = PartnerProfile.objects.all()

    base_url = "http://157.230.228.250/"

    data = []

    # for bill in merchant_bill_list:
    #     try:
    #         bill_file = str(base_url) + str(bill.bill.url)
    #     except:
    #         bill_file = ""
    #     try:
    #         user_object = GreenBillUser.objects.get(id = bill.user_id)
    #         created_by_id = user_object.id
    #         created_by = user_object.first_name + ' ' + user_object.last_name
    #     except:
    #         created_by = ""
    #         created_by_id = ""

    #     data.append({
    #         'bill_id': bill.id,
    #         'invoice_no': bill.invoice_no,
    #         'mobile_no': bill.mobile_no,
    #         'amount': str(bill.bill_amount),
    #         'business': bill.business_name,
    #         'date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
    #         'bill_file': bill.bill,
    #         'db_table': "MerchantBill",
    #         'customer_added': False,
    #         'created_by': created_by,
    #         'created_by_id': created_by_id,
    #         'bill_flag': False,
    #         'bill_url': bill.bill_url,
    #         'created_at': bill.created_at,            
    #     })

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
                        if recharge.mode == "cashwithoutbill":
                            users_cost = float(recharge.no_of_users) * float(recharge.valid_for_month) * float(subscription.cost_for_users)
                            final_amount = float(users_cost) + float(recharge.cost) 
                        else:
                            users_cost = float(recharge.no_of_users) * float(recharge.valid_for_month) * float(subscription.cost_for_users)
                            final_amount = float(users_cost) + float(recharge.cost) + float(recharge.gst_amount)
                        
                    except:
                        final_amount = 0
            else:
                final_amount = recharge.cost


            purchase_date = timezone.localtime(recharge.purchase_date).strftime("%Y-%m-%d")

            data.append({
                'bill_id': recharge.id,
                'invoice_no': recharge.invoice_no,
                'mobile_no': '',
                'amount': str(final_amount),
                # 'business': 'Green Bill',
                'business': merchant,
                'date': datetime.strptime(str(purchase_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'bill_file': '',
                'db_table': "recharge_history",
                'customer_added': '',
                'created_by': '',
                'created_by_id': '',
                'bill_flag': '',
                'bill_url': '',
                'created_at': recharge.purchase_date, 
            })

    for partner in all_partner:

        partner_recharge_history_list = partner_recharge_history.objects.filter(partner_id = partner.p_user).order_by("-id")

        for recharge in partner_recharge_history_list:

            # print("recharge.id",recharge.id)
            purchase_date = timezone.localtime(recharge.purchase_date).strftime("%Y-%m-%d")

            data.append({
                'bill_id': recharge.id,
                'invoice_no': recharge.invoice_no,
                'mobile_no': '',
                'amount': recharge.cost,
                'business': partner,
                'date': datetime.strptime(str(purchase_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'bill_file': '',
                'db_table': "partner_recharge_history",
                'customer_added': '',
                'created_by': '',
                'created_by_id': '',
                'bill_flag': '',
                'bill_url': '',
                'created_at': recharge.purchase_date, 
            })

    # data.sort(key = lambda x: datetime.strptime(x['date'], '%d-%m-%Y'), reverse = True)
    data.sort(key = lambda x: x['created_at'], reverse = True)

    received_bills = 0
    received_amount = 0

    for a in data:
        received_bills = received_bills + 1
    for b in data:
        received_amount =  float(received_amount) + float(b['amount'])

    if request.method == "POST":
        user = request.POST.get('user')
        from_date = request.POST['from_date']
        from_date_temp1 = from_date
        to_date = request.POST['to_date']
        to_date_temp1 = to_date

        new_data = []

        if data:
            if from_date:
                from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%Y-%m-%d')
                
            if to_date:
                to_date = datetime.strptime(str(to_date), '%Y-%m-%d').strftime('%Y-%m-%d')
                
            for bill in data:
                if from_date and to_date:
                    bill_date = datetime.strptime(str(bill['date']), '%d-%m-%Y').strftime('%Y-%m-%d')
                    if bill_date >= from_date and bill_date <= to_date:
                        new_data.append(bill)

                elif from_date:
                    bill_date = datetime.strptime(str(bill['date']), '%d-%m-%Y').strftime('%Y-%m-%d')
                    if bill_date >= from_date:
                        new_data.append(bill)

                elif to_date:
                    bill_date = datetime.strptime(str(bill['date']), '%d-%m-%Y').strftime('%Y-%m-%d')
                    if bill_date <= to_date:
                        new_data.append(bill)
                        

        received_amount = 0
        received_bills = 0
        new_data.sort(key = lambda x: x['created_at'], reverse = True)
        for z in new_data:
            received_amount =  float(received_amount) + float(z['amount'])
        received_bills = len(new_data)
            
        context = {
                "bills":new_data,
                'BillInfoNavClass':'active',
                'SentBillsNavClass': 'active',
                "BillInfoCollapseShow": "show",
                'from_date': from_date_temp1,
                'to_date': to_date_temp1,
                'received_amount' : received_amount,
                'received_bills' : received_bills,
                }      
        return render(request, "super_admin/bill_info/sent-bills.html", context)

    else:
        context = {
            "bills":data,
            'received_amount' : received_amount,
            'received_bills' : received_bills,
            'BillInfoNavClass':'active',
            'SentBillsNavClass': 'active',
            "BillInfoCollapseShow": "show",
        }

    return render(request, "super_admin/bill_info/sent-bills.html", context)



def delete_sentbill(request,id,db_table):
    try:
        if db_table == "recharge_history":
            recharge_his_id = recharge_history.objects.get(id=id)
            # print("&&&&&&&&&&&&&&&&")
            # print(recharge_his_id)
            if recharge_his_id.delete():
                # print("*******************1")
                # print(recharge_his_id)
                sweetify.success(request, title="Success 1...", icon='success', text='Deleted successfully...', timer=1500)
                return redirect(owner_sent_bills_view)
            else:
                # print("*******************2")
                # print(recharge_his_id)
                sweetify.error(request, title="Success 2...", icon='success', text='error', timer=1500)
                return redirect(owner_sent_bills_view)
        else:
            # print("*******************3")
            # print(recharge_his_id)
            partenr_id=partner_recharge_history.objects.get(id=id)
            # print(partenr_id)
            # partenr_id.delete()
            # print(partenr_id)
            if partenr_id.delete():
                # print("*******************30")
                # print(recharge_his_id)
                sweetify.success(request, title="Success 4...", icon='success', text='Deleted successfully...', timer=1500)
                return redirect(owner_sent_bills_view)
            else:
                # print("*******************322")
                # print(recharge_his_id)
                sweetify.error(request, title="Success 5...", icon='success', text='error', timer=1500)
                return redirect(owner_sent_bills_view)
    except:
        # print("********222***********3")
        # print(recharge_his_id)
        sweetify.error(request, title="Oops...", icon='success', text='error', timer=1500)
        return redirect(owner_sent_bills_view)


# @login_required(login_url="/login/")
# @user_passes_test(is_owner, login_url="/login/")
def owner_category_bills_view(request):

    bill_categories = bill_category.objects.all().order_by('bill_category_name')

    allocated_bill_categories = []

    bills = []

    for category in bill_categories:
        customer_bill_count = CustomerBill.objects.filter(customer_bill_category = category).count()
        if customer_bill_count > 0:
            if category in allocated_bill_categories:
                continue
            else:
                allocated_bill_categories.append(category)

        parking_bill_count = SaveParkingLotBill.objects.filter(is_pass = False, bill_category_id = category.id).count()
        if parking_bill_count > 0:
            if category in allocated_bill_categories:
                continue
            elif category.id == 27:
                allocated_bill_categories.append(category)

        petrol_bill_count = SavePetrolPumpBill.objects.filter(bill_category_id = category.id).count()
        if petrol_bill_count > 0:
            if category in allocated_bill_categories:
                continue
            elif category.id == 26:
                allocated_bill_categories.append(category)


    for bill_categories in allocated_bill_categories:

        bill_categories.bill_count = 0

        bill_categories.color = random_color()

        customer_bill_list = CustomerBill.objects.filter(customer_bill_category = bill_categories).order_by('-id')

        bill_categories.bills = []

        for bill in customer_bill_list:
            try:
                bill_file = bill.bill
            except:
                bill_file = ""

            if bill.bill_tags:
                bill_tags_temp = bill.bill_tags
            else:
                bill_tags_temp = "0"

            try:
                business_name1 = MerchantProfile.objects.get(id = bill.business_name.id)
                business_names = business_name1.m_business_name
                business_logo = business_name1.m_business_logo
            except:
                business_names = ""
                business_logo = ''

            bill_categories.bills.append({
                'id': bill.id,
                'amount': str(bill.bill_amount),
                'bill_date': bill.bill_date,
                'bill_file': bill_file,
                'bill_category' : bill.customer_bill_category,
                'business_name' : business_names,
                'bill_tags' : bill_tags_temp,
                'remarks' : bill.remarks,
                'business_logo': business_logo,
                'custom_business_name': bill.custom_business_name,
                'db_table': "CustomerBill",
                'customer_added': bill.customer_added,
                'bill_url': bill.bill_url,
                'invoice_no':bill.invoice_no,
                'color': random_color()
            })


            bill_categories.bill_count += 1

        parking_bill_list = SaveParkingLotBill.objects.filter(bill_category_id = bill_categories.id, is_pass = False).order_by('-id')
        for bill in parking_bill_list:
            try:
                bill_file = bill.bill_file
            except:
                bill_file = ""
            
            if bill.bill_tags:
                bill_tags_temp = bill.bill_tags
            else:
                bill_tags_temp = "0"

            try:
                business_name1 = MerchantProfile.objects.get(id = bill.m_business_id)
                business_name = business_name1.m_business_name
                business_logo = business_name1.m_business_logo
            except:
                business_name = ""
                business_logo = ""

            try:
                bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
            except:
                bill_category_temp = ""

            bill_categories.bills.append({
                'id': bill.id,
                'amount': str(bill.amount),
                'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                'bill_file': bill_file,
                'bill_category' : bill_category_temp,
                'business_name' : business_name,
                'bill_tags' : bill_tags_temp,
                'remarks' : bill.remarks,
                'business_logo': business_logo,
                'custom_business_name': "",
                'db_table': "SaveParkingLotBill",
                'customer_added': False,
                'bill_url': bill.bill_url,
                'invoice_no':bill.invoice_no,
                'color': random_color()
            })

            bill_categories.bill_count += 1  

        petrol_bill_list = SavePetrolPumpBill.objects.filter(bill_category_id = bill_categories.id).order_by('-id')
        for bill in petrol_bill_list:
            try:
                bill_file = bill.bill_file
            except:
                bill_file = ""
            
            if bill.bill_tags:
                bill_tags_temp = bill.bill_tags
            else:
                bill_tags_temp = "0"

            try:
                business_name1 = MerchantProfile.objects.get(id = bill.m_business_id)
                business_name = business_name1.m_business_name
                business_logo = business_name1.m_business_logo
            except:
                business_name = ""
                business_logo = ""

            try:
                bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
            except:
                bill_category_temp = ""

            bill_categories.bills.append({
                'id': bill.id,
                'amount': str(bill.total_amount),
                'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                'bill_file': bill_file,
                'bill_category' : bill_category_temp,
                'business_name' : business_name,
                'bill_tags' : bill_tags_temp,
                'remarks' : bill.remarks,
                'business_logo': business_logo,
                'custom_business_name': "",
                'db_table': "SavePetrolPumpBill",
                'customer_added': False,
                'bill_url': bill.bill_url,
                'invoice_no':bill.invoice_no,
                'color': random_color()
            })

            bill_categories.bill_count += 1

    customer_bill_tags = bill_tags.objects.all()
    context = {
        'allocated_bill_categories': allocated_bill_categories,
        'BillInfoNavClass':'active',
        'CategoryWiseBillsNavClass': 'active',
        "BillInfoCollapseShow": "show",
    }

    return render(request, "super_admin/bill_info/categorywise-bills.html", context)


def random_color():

    hex_digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

    digit_array = []

    from random import randint

    for i in range(6):
        digit_array.append(hex_digits[randint(0,15)])
    joined_digits = ''.join(digit_array)

    color = '#' + joined_digits

    return color

