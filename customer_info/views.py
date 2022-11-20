from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .forms import Customer_Info_Form, Edit_Customer_Info_Form
from .models import Customer_Info_Model
from django.contrib import messages
import csv
import io
from owner_customer_info.forms import bulkMailSmsCustomerForm
from feedback.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
import sweetify
from users.models import Merchant_users, GreenBillUser, MerchantProfile

from merchant_software_apis.models import CustomerBill
from petrol_pump_apis.models import SavePetrolPumpBill
from parking_lot_apis.models import SaveParkingLotBill

from datetime import datetime

from app.views import is_merchant_or_merchant_staff, getActiveSubscriptionPlan

from my_subscription.models import *
from authentication.models import StateCityData

# SMS
import requests
import time
import pyshorteners

from users.models import Merchant_users, MerchantProfile, GreenBillUser
from merchant_software_apis.models import CustomerBill, MerchantBill
from django.utils import formats
from app.views import is_merchant_or_merchant_staff, getActiveSubscriptionPlan
from bill_design.models import *
from my_subscription.models import *
from merchant_cashmemo_design.models import *
from django.utils import timezone




@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def Customer_Info(request):

    mer_user_id = Merchant_users.objects.get(user_id=request.user)
    print("___________________________________")
    print(request.user)
    print(type(request.user))
    # print(list(request.user))
    print(mer_user_id)
    print(type(mer_user_id))
    # print(list(mer_user_id))
    merchant_object = mer_user_id.merchant_user_id
    
    merchant_business_object = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    merchant_business_id = merchant_business_object.id

    parking_bill_list = SaveParkingLotBill.objects.filter(m_business_id = merchant_business_id, is_pass = False).order_by('-id')
    petrol_bill_list = SavePetrolPumpBill.objects.filter(m_business_id = merchant_business_id).order_by('-id')
    customer_bill_list = CustomerBill.objects.filter(business_name = merchant_business_object, customer_added = False).order_by('-id')
    merchant_bill_list = MerchantBill.objects.filter(business_name = merchant_business_object, customer_added = False).order_by('-id')
    merchant_added_customer_list = Customer_Info_Model.objects.filter(mer_id = merchant_object,merchant_business_id=merchant_business_id).order_by('-id')

    info_form = Customer_Info_Form(request.POST)
    if request.method == "POST":
        mobile_no = request.POST.get('cust_mobile_num')
        is_customer = Customer_Info_Model.objects.filter(cust_mobile_num = mobile_no)
        is_customer1 = GreenBillUser.objects.filter(mobile_no = mobile_no)

        info_form = Customer_Info_Form(request.POST)
        if is_customer1:
            sweetify.error(request, title="Soory", icon='error', text='Number is already exists', timer=1500)

        else:
            if info_form.is_valid():
                user = Customer_Info_Model.objects.update_or_create(
                    mer_id=mer_user_id.merchant_user_id,
                    merchant_business_id =merchant_business_object,
                    cust_first_name=info_form.cleaned_data['cust_first_name'],
                    cust_last_lname=info_form.cleaned_data['cust_last_lname'],
                    cust_email=info_form.cleaned_data['cust_email'],
                    cust_mobile_num=info_form.cleaned_data['cust_mobile_num'],
                    customer_state=info_form.cleaned_data['customer_state'],
                    customer_city=info_form.cleaned_data['customer_city'],
                    customer_area=info_form.cleaned_data['customer_area'],
                    customer_pin_code=info_form.cleaned_data['customer_pin_code'],

                )

                sweetify.success(request, title="Success", icon='success',
                                 text='Customer Added Successful.', timer=1500)
            else:
                sweetify.error(request, title="Error", icon='error',
                               text='Customer Added Failed', timer=1500)

    customer_info_data = []

    for customer in merchant_added_customer_list:
        customer_info_data.append({
            "mobile_no" : customer.cust_mobile_num,
            "name" : customer.cust_first_name + ' ' + customer.cust_last_lname,
            "email" : customer.cust_email,
            "state" : customer.customer_state,
            "city": customer.customer_city,
            "pincode": customer.customer_pin_code,
            "area": customer.customer_area,
            "date": timezone.localtime(customer.date_joined).strftime("%Y-%m-%d"),
            })

    for bill in parking_bill_list:
        try:
            user = GreenBillUser.objects.get(mobile_no = bill.mobile_no, is_customer = True)
            date = timezone.localtime(user.date_joined).strftime("%Y-%m-%d")

            count = count + 1
            name = user.first_name + ' ' + user.last_name
            email = user.email
            state = user.c_state 
            area = user.c_area
            pincode = user.c_pincode
            city = user.c_city
            customer_info_data.append({
            'mobile_no':mobile_no,
            'name': name,
            'email':email,
            'state':state,
            'area': area,
            'pincode': pincode,
            'city':city,
            'date': datetime.strptime(str(user.date_joined), '%Y-%m-%d').strftime('%Y-%m-%d'),
            })
        except:
            customer_info_data.append({
                'mobile_no': bill.mobile_no,
                'name': '',
                'email':'',
                'state':'',
                'area': '',
                'pincode':'',
                'city':'',
                'date': timezone.localtime(bill.created_at).strftime("%Y-%m-%d"),
            });

    for bill in petrol_bill_list:

        try:
            user = GreenBillUser.objects.get(mobile_no = bill.mobile_no, is_customer = True)
            date = timezone.localtime(user.date_joined).strftime("%Y-%m-%d")
            count = count + 1
            name = user.first_name + ' ' + user.last_name
            email = user.email
            state = user.c_state 
            area = user.c_area
            pincode = user.c_pincode
            city = user.c_city
            customer_info_data.append({
            'mobile_no':mobile_no,
            'name': name,
            'email':email,
            'state':state,
            'area': area,
            'pincode': pincode,
            'city':city,
            'date': date,
            })
        except:
            customer_info_data.append({
                'mobile_no': bill.mobile_no,
                'name': '',
                'email':'',
                'state':'',
                'area': '',
                'pincode': '',
                'city':'',
                'date': timezone.localtime(bill.created_at).strftime("%Y-%m-%d"),
            });

    for bill in customer_bill_list:

        try:
            user = GreenBillUser.objects.get(mobile_no = bill.mobile_no, is_customer = True)
            date = timezone.localtime(user.date_joined).strftime("%Y-%m-%d")
            count = count + 1
            name = user.first_name + ' ' + user.last_name
            email = user.email
            state = user.c_state 
            area = user.c_area
            pincode = user.c_pincode 
            city = user.c_city
            customer_info_data.append({
            'mobile_no':mobile_no,
            'name': name,
            'email':email,
            'state':state,
            'area': area,
            'pincode': pincode,
            'city':city,
            'date': date,
            })
        except:
            customer_info_data.append({
                'mobile_no': bill.mobile_no,
                'name': '',
                'email':'',
                'state':'',
                'area':'',
                'pincode': '',
                'city':'',
                'date': timezone.localtime(bill.created_at).strftime("%Y-%m-%d"),
            });

    for bill in merchant_bill_list:
        try:
            user = GreenBillUser.objects.get(mobile_no = bill.mobile_no, is_customer = True)
            date = timezone.localtime(user.date_joined).strftime("%Y-%m-%d")
            count = count + 1
            name = user.first_name + ' ' + user.last_name
            email = user.email
            state = user.c_state 
            area = user.c_area
            pincode = user.c_pincode
            city = user.c_city
            customer_info_data.append({
            'mobile_no':mobile_no,
            'name': name,
            'email':email,
            'state':state,
            'area': area,
            'pincode': pincode,
            'city':city,
            'date': date,
            })
        except:
            customer_info_data.append({
                'mobile_no': bill.mobile_no,
                'name': '',
                'email':'',
                'state':'',
                'area': '',
                'pincode': '',
                'city':'',
                'date': timezone.localtime(bill.created_at).strftime("%Y-%m-%d"),
            });

    
    customer_info_data1 = []
    customer_info_data2 = []
    new_customer_data = []
    filtered_list = []
    filtered_list2 = []
    count = 0
    count2 = 0
    total_count = 0

    customer_receipt = CustomerReceiptDetailsModels.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_object).order_by('-id')

    for user in customer_receipt:
        try:
            customer_info_data2.append({
                'mobile_no': user.mobile_number,
                'name': user.cash_received_from,
                'email':'',
                'state':'',
                'area':'',
                'pincode':'',
                'city':'',
                'date': datetime.strptime(str(user.date), '%Y-%m-%d').strftime('%Y-%m-%d'),
                })
        except:
            customer_info_data2.append({
                'mobile_no': user.mobile_number,
                'name': '',
                'email':'',
                'state':'',
                'area': '',
                'pincode': '',
                'city':'',
                'date': '',
                })
    for x in customer_info_data2:
        if x['mobile_no'] not in filtered_list:
            if x['mobile_no'] != '':
                filtered_list.append(x['mobile_no'])

                customer_info_data.append({
                    'mobile_no': x['mobile_no'],
                    'name': x['name'],
                    'email':'',
                    'state':'',
                    'area':'',
                    'pincode':'',
                    'city':'',
                    'date': x['date'],
                    })



    customer_cash_memo = CustomerCashMemoDetailModels.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_object).order_by('-id')

    for user in customer_cash_memo:
        try:
            customer_info_data1.append({
                'mobile_no': user.mobile_number,
                'name': user.name,
                'email':'',
                'state':'',
                'area':'',
                'pincode':'',
                'city':'',
                'date': datetime.strptime(str(user.date), '%Y-%m-%d').strftime('%Y-%m-%d'),
                })
        except:
            customer_info_data1.append({
                'mobile_no': user.mobile_number,
                'name': '',
                'email':'',
                'state':'',
                'area':'',
                'pincode':'',
                'city':'',
                'date': '',
                })

    for x in customer_info_data1:
        if x['mobile_no'] not in filtered_list:
            if x['mobile_no'] != '':
                filtered_list.append(x['mobile_no'])

                customer_info_data.append({
                    'mobile_no': x['mobile_no'],
                    'name': x['name'],
                    'email':'',
                    'state':'',
                    'area':'',
                    'pincode':'',
                    'city':'',
                    'date': x['date'],
                    })

        

        

    total_count = count + count2
    for unique in customer_info_data:
        if unique['mobile_no'] not in filtered_list2:
            filtered_list2.append(unique['mobile_no'])
            new_customer_data.append({
                "mobile_no" : unique['mobile_no'],
                "name" : unique['name'],
                "email" : unique['email'],
                "state" : unique['state'],
                'area':unique['area'],
                'pincode':unique['pincode'],
                "city": unique['city'],
                "date": unique['date'],
            })

    total_count = len(new_customer_data)
    new_customer_data.sort(key = lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse = True)
    States = StateCityData.objects.values('state').distinct().order_by('state')
    context = {
        'total_count': total_count,
        'customer_info_data': new_customer_data,
        'CustomerInfoNavClass': 'active',
        "States": States,

    }

    if merchant_business_object.m_business_category.id == 11 or merchant_business_object.m_business_category.id == 12:
        return render(request, "page-404.html")
    else:
        return render(request, "merchant/customer_info/customer_info.html", context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def Customer_CSV_Upload(request):
    mer_user_id = Merchant_users.objects.get(user_id=request.user)
    customer_info = Customer_Info_Model.objects.filter(mer_id=request.user)
    context = {
        'mer_info_data': customer_info,
        'CustomerInfoNavClass': 'active',
    }
    csv_file = request.FILES['csvfileupload']
    if csv_file.name.endswith('.csv'):
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Customer_Info_Model.objects.update_or_create(
                mer_id=mer_user_id.merchant_user_id,
                cust_first_name=column[0],
                cust_last_lname=column[1],
                cust_email=column[2],
                cust_mobile_num=column[3],
                customer_area=column[4],
                customer_pin_code=column[5]
            )
        sweetify.success(request, title="Success", icon='success',
                         text='Data Uploaded Successfully.', timer=1500)
        return redirect("/customer-info/")
    else:
        sweetify.error(request, title="Error", icon='error',
                       text='File Must Be .CSV.', timer=1500)
        # return render(request, "customer_info/customer_info.html", context)

    return render(request, "merchant/customer_info/customer_info.html", context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def Edit_Cust_info(request):
    # mer_info = Customer_Info_Model.objects.filter(mer_id=request.user)
    # context = {
    #     'mer_info_data': mer_info,
    #     'CustomerInfoNavClass': 'active',
    # }

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
            # return redirect('/customer-info/')
        else:
            sweetify.error(request, title="Error", icon='error',
                           text='Customer Upadte Failed', timer=1500)
            # return HttpResponseRedirect("/customer-info/")
    return redirect(Customer_Info)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def Delete_Customer(request, id):
    if request.method == "POST":
        cust = Customer_Info_Model.objects.get(id=id)
        cust.delete()
        return JsonResponse({"success": True})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def Check_Contact(request, id):
    mobile_no = id
    mer_user_id = Merchant_users.objects.get(user_id=request.user)

    try:
        mob_num = Customer_Info_Model.objects.get(cust_mobile_num=mobile_no, mer_id=mer_user_id.merchant_user_id)
    except:
        mob_num = ""

    try:
        mob_num1 = GreenBillUser.objects.get(mobile_no=mobile_no)
    except:
        mob_num1 = ""
        
    if mob_num and mob_num1:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def customer_info_by_mobile_no(request, mobile_no):

    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    try:
        feedback_emoji = bill_designs.objects.get(merchant_business_id = merchant_business_id).rating_emoji
    except:
        feedback_emoji = '😊'

    user_id = request.user

    data = []

    base_url = "http://157.230.228.250/"
    personal_details = {}
    # try:
    #     customer_object = GreenBillUser.objects.get(mobile_no = mobile_no, is_customer = True)
    #     if customer_object.is_customer == True:
    #         mobile_no = customer_object.mobile_no
    #         first_name = customer_object.first_name 
    #         last_name = customer_object.last_name
    #         email = customer_object.email
    #         gender = customer_object.c_gender
    #         dob = customer_object.c_dob
    #         area = customer_object.c_area
    #         pincode = customer_object.c_pincode
    #         personal_details = {
    #                 'mobile_no' : mobile_no,
    #                 'first_name' : first_name,
    #                 'last_name' : last_name,
    #                 'email': email,
    #                 'c_gender': gender,
    #                 'c_dob': dob,
    #                 'c_area': area,
    #                 'c_pincode': pincode  
    #         }

    # except:
    #     mobile_no = mobile_no
    #     first_name = "" 
    #     last_name = ""
    #     email = ""
    #     gender = ""
    #     dob = ""
    #     area = ""
    #     pincode = ""

    try:

        customer2 = Customer_Info_Model.objects.get(cust_mobile_num = mobile_no)
        mobile_no = customer2.cust_mobile_num
        first_name = customer2.cust_first_name 
        last_name = customer2.cust_last_lname
        email = customer2.cust_email
        gender = ""
        dob = ""
        area = customer2.customer_area
        pincode = customer2.customer_pin_code

        personal_details = {
                'mobile_no' : mobile_no,
                'first_name' : first_name,
                'last_name' : last_name,
                'email': email,
                'c_gender': gender,
                'c_dob': dob,
                # 'cust_profile': customer2.cust_profile,
                'c_area': area,
                'c_pincode':pincode 
        }
        
    except:

        mobile_no = mobile_no
        first_name = "" 
        last_name = ""
        email = ""
        gender = ""
        dob = ""
        area = ""
        pincode = ""
        
        # personal_details = {
        #     'mobile_no' : mobile_no,
        #     'first_name' : '',
        #     'last_name' : '',
        #     'email': '',
        #     'c_gender': '',
        #     'c_dob': '',
        #     # 'c_profile': '',
        #     'c_area': '',
        #     'c_pincode': ''
        # }

    # print('personal_details',personal_details)        
    customer_bill_list = CustomerBill.objects.filter(mobile_no=mobile_no)

    for bill in customer_bill_list:
        # if mobile_no == bill.mobile_no:
        try:
            bill_file = str(base_url) + str(bill.bill.url)
            
            if bill.customer_added == True:
                url = str(base_url) + 'self-added-bill/' + str(bill.bill_url) + "/"
            else:
                url = str(base_url) + 'my-bill/' + str(bill.bill_url) + "/"
            # url = str(base_url) + "my-bill/" + str(bill.bill_url) +"/"
        except:
            bill_file = ""

        data.append({
            'bill_id': bill.id,
            'mobile_no': mobile_no,
            'amount': str(bill.bill_amount),
            'bill_date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
            'bill_file': bill_file,
            'db_table': "CustomerBill",
            'url':url,
            'customer_added': bill.customer_added
        })
            
    parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no=mobile_no)
    for bill in parking_bill_list:
        # if mobile_no == bill.mobile_no:
        try:
            bill_file = str(base_url) + str(bill.bill_file.url)
            url = str(base_url) + "parking-lot-bill/" + str(bill.bill_url) + "/"
        except:
            bill_file = ""
        data.append({
            'bill_id': bill.id,
            'mobile_no': mobile_no,
            'amount': str(bill.amount),
            'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
            'bill_file': bill_file,
            'db_table': "SaveParkingLotBill",
            'customer_added': False,
            'url':url,
        })
            
    petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no=mobile_no)
    for bill in petrol_bill_list:
        # if mobile_no == bill.mobile_no:
            try:
                bill_file = str(base_url) + str(bill.bill_file.url)
                url = str(base_url) + "petrol-pump-bill/" + str(bill.bill_url) + "/"
            except:
                bill_file = ""
            data.append({
                'bill_id': bill.id,
                'mobile_no': mobile_no,
                'amount': str(bill.total_amount),
                'bill_date': datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                'bill_file': bill_file,
                'db_table': "SavePetrolPumpBill",
                'customer_added': False,
                'url' : url
            })
    datalist = []
    feedback_list = Feedback.objects.all()
    # print(feedback_list)
    for feedback_data in feedback_list:
        if mobile_no == feedback_data.mobile_no:
            datalist.append({
                'feedback_id': feedback_data.id,
                'mobile_no': mobile_no,
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

    try:
        bill_design = bill_designs.objects.get(merchant_business_id = merchant_business_object)
        bill_rating_emoji = bill_design.rating_emoji
    except:
        bill_rating_emoji = ""

    parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no=mobile_no).order_by('-id')

    for bill in parking_bill_list:
        try:
        	url = str(base_url) + "parking-lot-bill/" + str(bill.bill_url) + "/"
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
            'flag_by': bill.flag_by,
            'url':url,
        })
    petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no=mobile_no).order_by('-id')

    for bill in petrol_bill_list:
        try:
            bill_file = str(base_url) + str(bill.bill_file.url)
            url = str(base_url) + "petrol-pump-bill/" + str(bill.bill_url) + "/"
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
            'flag_by': bill.flag_by,
            'url':url,
        })
    customer_bill_list = CustomerBill.objects.filter(mobile_no=mobile_no)
    for bill in customer_bill_list:
        try:
            bill_file = str(base_url) + str(bill.bill.url)
            url = str(base_url) + "my-bill/" + str(bill.bill_url) + "/"
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
            'feedback_reply': bill.feedback_reply,
            'rating': bill.rating,
            'created_by': created_by,
            'created_by_id': created_by_id,
            'bill_flag': False,
            'url':url,
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


    print(personal_details)
    context = {
    'feedback_emoji': feedback_emoji,
    'bills': data,
    'mobile_no': mobile_no,
    'personal_details' : personal_details,
    'CustomerInfoNavClass': 'active',
    'bulkMailSmsCustomerForm':bulkMailSmsCustomerForm,
    }
    return render(request, "merchant/customer_info/customer_info_by_mobile_no.html", context)



def ViewAllCashMemoByNumber(request, mobile_no):

    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    cash_memo = CustomerCashMemoDetailModels.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id, mobile_number = mobile_no).order_by('-id')
    cash_memo1 = CustomerCashMemoDetailModels.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id, mobile_number = mobile_no).last()
    try:
        mob_no = cash_memo1.mobile_number
    except:
        mob_no = ''
    try:
        name = cash_memo1.name
    except:
        name = ''
    total_cash_memo = CustomerCashMemoDetailModels.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id, mobile_number = mobile_no).count
    context = {
    'mobile_number': mobile_no,
    'name': name,
    'cash_memo': cash_memo,
    'total_cash_memo': total_cash_memo,
    'CustomerInfoNavClass': 'active',
    }
    return render(request, "merchant/customer_info/view-cashmemo-details.html", context)


def ViewAllReceiptMemoByNumber(request, mobile_no):

    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    receipt = CustomerReceiptDetailsModels.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id, mobile_number = mobile_no).order_by('-id')


    receipt1 = CustomerReceiptDetailsModels.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id, mobile_number = mobile_no).last()

    # try:
    #     mob_no = receipt1.mobile_number
    # except:
    #     mob_no = ''
    try:
        name = receipt1.cash_received_from
    except:
        name = ''

    total_receipt = CustomerReceiptDetailsModels.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id, mobile_number = mobile_no).count

    context = {
    'receipt': receipt,
    'mobile_number': mobile_no,
    'name': name,
    'total_receipt': total_receipt,
    'CustomerInfoNavClass': 'active',
    }
    return render(request, "merchant/customer_info/view-receipt-details.html", context)



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def CustomerInfoSendBillSMSWeb(request, id):
    bill_id = id
    mobile_no = request.POST["mobile_no"]
    db_table = request.POST["db_table"]
    print('id',bill_id)
    print('mobile_no',mobile_no)
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


