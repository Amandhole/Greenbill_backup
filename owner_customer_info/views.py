
from django.shortcuts import render, redirect
from customer_info.models import Customer_Info_Model
from users.models import Merchant_users, GreenBillUser, MerchantProfile
from customer_info.forms import Customer_Info_Form, Edit_Customer_Info_Form
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomerForm
from app.views import is_owner
from merchant_software_apis.models import CustomerBill
from petrol_pump_apis.models import SavePetrolPumpBill
from parking_lot_apis.models import SaveParkingLotBill
from green_points.models import GreenPointsModel

from datetime import datetime
from datetime import date
import sweetify
from django.contrib import messages
import csv
import io
from django.http import JsonResponse, HttpResponseRedirect
from dateutil import parser
from .forms import bulkMailSmsCustomerForm
from django.core.mail import send_mail
from owner_notice_board.sendsms import *
from merchant_cashmemo_design.models import *
from .models import bulkMailSmsCustomerModel
from django.utils.html import strip_tags
from django.conf import settings
from owner_notice_board.models import OnwerNoticeBoard,OwnerSentNotice
# Create your views here.
from feedback.models import *
from customer_bill.models import *
# SMS
import requests
import time
import pyshorteners

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def owner_customer_info(request):
    bills =  GreenBillUser.objects.filter(is_customer = True,is_active=True)

    data = []
    sum = 0
    for cust_info in bills:
        mob_check=cust_info.mobile_no
        parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no=mob_check).order_by('-id')

        # bill_count1 = SaveParkingLotBill.objects.filter(mobile_no=mob_check).count()
        # print("bill_count1",bill_count1)
        try:
            bill_design = bill_designs.objects.get(merchant_business_id = merchant_business_object)
            bill_rating_emoji = bill_design.rating_emoji
        except:
            bill_rating_emoji = ""

    # parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no=mobile_no).order_by('-id')
        
        for bill in parking_bill_list:
            # sum = sum + int(float(bill.amount))

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
                # 'sum': sum,
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': bill.mobile_no,
                'amount': bill.amount,
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
        petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no=mob_check).order_by('-id')

        # bill_count2 = SavePetrolPumpBill.objects.filter(mobile_no=mob_check).count()

        # print("bill_count2",bill_count2)
        for bill in petrol_bill_list:
            # sum = sum + int(bill.amount)
            
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
                # 'sum': sum,
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': bill.mobile_no,
                'amount': (bill.amount),
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
        customer_bill_list = CustomerBill.objects.filter(mobile_no=mob_check).order_by('-id')

        # bill_count3 = CustomerBill.objects.filter(mobile_no=mob_check).count()

        # print("bill_count3",bill_count3)
        

        # sum = 0 
        for bill in customer_bill_list:

           
            
            # sum = sum + int(float(bill.bill_amount))
            # data.append({
            #     'sum': sum,
            # })
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

                
            #print("AA",bill.bill_date)
            data.append({
                # 'sum': sum,
                'bill_id': bill.id,
                'invoice_no': bill.invoice_no,
                'mobile_no': bill.mobile_no,
                'amount': (bill.bill_amount),
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
            
        # merchant_bill_list = MerchantBill.objects.filter(mobile_no=mobile_no).order_by('-id')

        # for bill in merchant_bill_list:
        #     try:
        #         bill_file = str(base_url) + str(bill.bill.url)
        #     except:
        #         bill_file = ""
            
        #     ratings = ""

        #     if bill.rating:
        #         for x in range(int(bill.rating)):
        #             ratings = " ".join((ratings, bill_rating_emoji))

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
        #         'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
        #         'bill_file': bill_file,
        #         'db_table': "MerchantBill",
        #         'customer_added': False,
        #         'bill_ratings': ratings,
        #         'rating': bill.rating,
        #         'created_by': created_by,
        #         'created_by_id': created_by_id,
        #         'bill_flag': False,
        #     })
    # sum = 0 
    # for d in data:
    #     sum = sum + int(float(d['amount']))
    #     data.append({
    #         'sum': sum,
    #     }) 
    # amount=[]
    # for counter in data:
    #     amount =(data['amount'])
    #     bills.amount = amount  
    # print(data)
    # amount1 = 0
    # for a in data:
    #     if a['amount']:
    #         amount1 = amount1 + int(float(a['amount']))
    # print(data['mobile_no'])
    # print(amount1) 
    # customer_count = 0
    # for count in data:
    #     customer_count = customer_count + 1
    
    total_bill_count = len(bills)
    
    context = {
        'data': bills,
        'total_bill_count': total_bill_count,
        'CustomerInfoNavClass': 'active',
    }

    return render(request, "super_admin/owner_customer_info/owner-customer-list.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Delete_customer(request, id):
    offer_obj = Customer_Info_Model.objects.get(id=id).delete()
    if offer_obj:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": False})





@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def customer_data_by_mobile_no(request, contact_no):

    user_id = request.user

    data = []

    base_url = "http://157.230.228.250/"

    qr = CustomerBill.objects.filter(mobile_no = contact_no , customer_added=True).count()
    print("HH",qr) 

    print("Pranit",contact_no)
    try:
    	points = GreenPointsModel.objects.get(mobile_no = contact_no)
    	total_green_point_data = points.green_points_count
    	print("JJ",total_green_point_data) 
    except:
    	total_green_point_data = '0'
    
    referral_code = GreenBillUser.objects.get(mobile_no = contact_no)
    check_referral_code = referral_code.customer_referral_code

    refer_count = GreenBillUser.objects.filter(c_used_referral_code=check_referral_code).count()
    print("SS",refer_count)

    try:
        customer_object = GreenBillUser.objects.get(mobile_no = contact_no)

        personal_details = {
                'mobile_no' : customer_object.mobile_no,
                'first_name' : customer_object.first_name,
                'last_name' : customer_object.last_name,
                'email': customer_object.email,
                'c_gender': customer_object.c_gender,
                'c_dob': customer_object.c_dob,
                'c_area': customer_object.c_area,
                'c_pincode': customer_object.c_pincode  
        }

    except:

        try:

            customer_object = Customer_Info_Model.objects.get(cust_mobile_num = contact_no)

            personal_details = {
                    'mobile_no' : customer_object.cust_mobile_num,
                    'first_name' : customer_object.cust_first_name,
                    'last_name' : customer_object.cust_last_lname,
                    'email': customer_object.cust_email,
                    'c_gender': customer_object.c_gender,
                    'c_dob': customer_object.date_of_birth,
                    'cust_profile': customer_object.cust_profile,
                    'c_area': customer_object.customer_area,
                    'c_pincode': customer_object.customer_pin_code
            }
            
        except:
            
            personal_details = {
                'mobile_no' : mobile_no,
                'first_name' : '',
                'last_name' : '',
                'email': '',
                'c_gender': '',
                'c_dob': '',
                'c_profile': '',
                'c_area': '',
                'c_pincode': ''
            }

            print(personal_details)

    share_model = Sharebillmodel.objects.filter(mobile_no = contact_no).order_by('-id')
    
    for mobile_no in share_model:
        if mobile_no.db_table == "CustomerBill":

            customer_bill_list = CustomerBill.objects.filter(mobile_no=contact_no)

            for bill in customer_bill_list: 
                if bill.customer_added == True:
                    new_bill_url = str(base_url) + 'self-added-bill/' + str(bill.bill_url) + "/"
                else:
                    new_bill_url = str(base_url) + 'my-bill/' + str(bill.bill_url) + "/"
            

            for bill in customer_bill_list:
            #     # if mobile_no == bill.mobile_no:
            #     try:
            #         bill_file = str(base_url) + str(bill.bill.url)
            #     except:
            #         bill_file = ""
                data.append({
                    'bill_id': bill.id,
                    'mobile_no': contact_no,
                    'amount': str(bill.bill_amount),
                    'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'bill_file': new_bill_url,
                    'db_table': "CustomerBill",
                    'customer_added': bill.customer_added
                })
         
        elif mobile_no.db_table == "SaveParkingLotBill":
                     
            parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no=contact_no)
            for bill in parking_bill_list:
                # if mobile_no == bill.mobile_no:
                # try:
                #     bill_file = str(base_url) + str(bill.bill_file.url)
                # except:
                #     bill_file = ""
	            data.append({
	                'bill_id': bill.id,
	                'mobile_no': contact_no,
	                'amount': str(bill.amount),
	                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
	                'bill_file': str(base_url) + 'parking-lot-bill/' + str(bill.bill_url) + "/",
	                'db_table': "SaveParkingLotBill",
	                'customer_added': False
	            })
         
        elif mobile_no.db_table == "SavePetrolPumpBill":            
            petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no=contact_no)
            for bill in petrol_bill_list:
                # if mobile_no == bill.mobile_no:
                    # try:
                    #     bill_file = str(base_url) + str(bill.bill_file.url)
                    # except:
                    #     bill_file = ""
	            data.append({
	                'bill_id': bill.id,
	                'mobile_no': contact_no,
	                'amount': str(bill.total_amount),
	                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
	                'bill_file': str(base_url) + 'petrol-pump-bill/' + str(bill.bill_url) + "/",
	                'db_table': "SavePetrolPumpBill",
	                'customer_added': False
	            })
    datalist = []
    feedback_list = Feedback.objects.all()
            # print(feedback_list)
    for feedback_data in feedback_list:
        if contact_no == feedback_data.mobile_no:
            datalist.append({
                'feedback_id': feedback_data.id,
                'mobile_no': contact_no,
                'comments': feedback_data.comments,
                'created_at': feedback_data.created_at,
                        # 'created_at': datetime.strptime(str(feedback_data.created_at), '%Y-%m-%d' '%H:%M:%S.%f').strftime('%Y-%m-%d'),
                'db_table': "Feedback",
                'customer_added': False
            })
    # sorted_data = sorted(data, key=data.bill_date)

    data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

    
    context = {
        "feedbacks": datalist, 
        "personal_details" : personal_details,
        "bills" : data,
        "feedback_datalist" : datalist,
        'CustomerInfoNavClass': 'active',
    }
    merchant_user = []

    data = []

    base_url = "http://157.230.228.250/"

    for mobile_no in share_model:
         
        if mobile_no.db_table == "SaveParkingLotBill":  

            try:
                bill_design = bill_designs.objects.get(merchant_business_id = merchant_business_object)
                bill_rating_emoji = bill_design.rating_emoji
            except:
                bill_rating_emoji = ""

            parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no=contact_no).order_by('-id')

            for bill in parking_bill_list:
                # try:
                #     bill_file = str(base_url) + str(bill.bill_file.url)
                # except:
                #     bill_file = ""

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
                    'bill_file': str(base_url) + 'parking-lot-bill/' + str(bill.bill_url) + "/",
                    'db_table': "SaveParkingLotBill",
                    'customer_added': False,
                    'bill_ratings': ratings,
                    'rating': bill.rating,
                    'created_by': created_by,
                    'created_by_id': created_by_id,
                    'bill_flag': bill.bill_flag,
                    'flag_by': bill.flag_by
                })

        if mobile_no.db_table == "SavePetrolPumpBill":       
            petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no=contact_no).order_by('-id')

            for bill in petrol_bill_list:
                # try:
                #     bill_file = str(base_url) + str(bill.bill_file.url)
                # except:
                #     bill_file = ""

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
                    'bill_file':  str(base_url) + 'petrol-pump-bill/' + str(bill.bill_url) + "/",
                    'db_table': "SavePetrolPumpBill",
                    'customer_added': False,
                    'bill_ratings': ratings,
                    'rating': bill.rating,
                    'created_by': created_by,
                    'created_by_id': created_by_id,
                    'bill_flag': bill.bill_flag,
                    'flag_by': bill.flag_by
                })

        if mobile_no.db_table== "CustomerBill":
            
            try:
                bill_design = bill_designs.objects.get(merchant_business_id = merchant_business_object)
                bill_rating_emoji = bill_design.rating_emoji
            except:
                bill_rating_emoji = ""
    
            customer_bill_list = CustomerBill.objects.filter(mobile_no=contact_no)
            for bill in customer_bill_list:
                # try:
                #     bill_file = str(base_url) + str(bill.bill.url)
                # except:
                #     bill_file = ""
                if bill.customer_added == True:
                    new_bill_url = str(base_url) + 'self-added-bill/' + str(bill.bill_url) + "/"
                else:
                    new_bill_url = str(base_url) + 'my-bill/' + str(bill.bill_url) + "/"

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
                    'bill_file': new_bill_url,
                    'db_table': "CustomerBill",
                    'customer_added': False,
                    'bill_ratings': ratings,
                    'feedback_reply': bill.feedback_reply,
                    'rating': bill.rating,
                    'created_by': created_by,
                    'created_by_id': created_by_id,
                    'bill_flag': False,
                })

    # petrol_bill_list = SavePetrolPumpBill.filter(mobile_no=mobile_no).order_by('-id')
    # for bill in petrol_bill_list:
    #     try:
    #         bill_file = str(base_url) + str(bill.bill_file.url)
    #     except:
    #         bill_file = ""
  
    #     ratings = ""    

    #     if bill.rating:
    #         for x in range(int(bill.rating)):
    #             ratings = " ".join((ratings, bill_rating_emoji))

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
    #         'amount': str(bill.total_amount),
    #         'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
    #         'bill_file': bill_file,
    #         'db_table': "SavePetrolPumpBill",
    #         'customer_added': False,
    #         'bill_ratings': ratings,
    #         'rating': bill.rating,
    #         'created_by': created_by,
    #         'created_by_id': created_by_id,
    #         'bill_flag': bill.bill_flag,
    #         'flag_by': bill.flag_by
    #     })
    data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)
    counter = 0
    for z in data :
        counter = counter+1
    received = counter -  qr
    print("received",received)
    print("QQ",counter)


    # print(data)
    context = {
    'bills': data,
    'bills_received' : received,
    'added_bills' : qr,
    'referral_used': refer_count,
    'personal_details' : personal_details,
    'total_green_point_data' : total_green_point_data,
    'CustomerInfoNavClass': 'active',
    'bulkMailSmsCustomerForm':bulkMailSmsCustomerForm,
    'my_mobile_number':contact_no,
    }

    return render(request, "super_admin/owner_customer_info/customer_data_by_mobile_no.html", context)


def ViewAllCashMemoByNumber(request, contact_no):

    cash_memo = CustomerCashMemoDetailModels.objects.filter( mobile_number = contact_no).order_by('-id')
    cash_memo1 = CustomerCashMemoDetailModels.objects.filter( mobile_number = contact_no).last()
    try:
        mob_no = cash_memo1.mobile_number
    except:
        mob_no = ''
    try:
        name = cash_memo1.name
    except:
        name = ''
    total_cash_memo = CustomerCashMemoDetailModels.objects.filter( mobile_number = contact_no).count
    context = {
    'mobile_number': contact_no,
    'name': name,
    'cash_memo': cash_memo,
    'total_cash_memo': total_cash_memo,
    'CustomerInfoNavClass': 'active',
    }
    return render(request, "super_admin/owner_customer_info/views-cash-memo-details.html", context)


def ViewAllReceiptMemoByNumber(request, contact_no):


    receipt = CustomerReceiptDetailsModels.objects.filter( mobile_number = contact_no).order_by('-id')


    receipt1 = CustomerReceiptDetailsModels.objects.filter( mobile_number = contact_no).last()

     
    try:
        name = receipt1.cash_received_from
    except:
        name = ''

    total_receipt = CustomerReceiptDetailsModels.objects.filter( mobile_number = contact_no).count

    context = {
    'receipt': receipt,
    'mobile_number': contact_no,
    'name': name,
    'total_receipt': total_receipt,
    'CustomerInfoNavClass': 'active',
    }
    return render(request, "super_admin/owner_customer_info/views-receipt-details.html", context)





@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Edit_Customer_info(request):
    if request.method == "POST":
        id = request.POST['mid']
        info_form = Edit_Customer_Info_Form(request.POST)
        if info_form.is_valid():
            user = Customer_Info_Model.objects.filter(id=id).update(
                cust_first_name=info_form.cleaned_data['edit_fname'],
                cust_last_lname=info_form.cleaned_data['edit_lname'],
                cust_email=info_form.cleaned_data['edit_email'],
                cust_mobile_num=info_form.cleaned_data['edit_mobile'],
                customer_area=info_form.cleaned_data['edit_area'],
                customer_pin_code=info_form.cleaned_data['edit_pin_code'],
            )
            sweetify.success(request, title="Success", icon='success',
                             text='Customer Updated Successfully.', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error',
                           text='Customer Upadte Failed', timer=1500)
    return redirect(owner_customer_info)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def CustomerInfoSendBillSMSWeb(request, id):
    bill_id = id
    mobile_no = request.POST["mobile_no"]
    db_table = request.POST["db_table"]

    if mobile_no:
        
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
            return JsonResponse({"success": True, "status": "success"})
        else:
            return JsonResponse({"success": False, "status": "error", "message":"You don't have active Green Bill Subscription. Please purchase and try again."})
