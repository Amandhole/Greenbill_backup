from django.shortcuts import render, redirect
from .forms import Customer_Bill_Form
from merchant_software_apis.models import CustomerBill
import sweetify
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import MerchantProfile
from category_and_tags.models import bill_category, bill_tags
from django.http import HttpResponse, JsonResponse
from app.views import is_customer

from merchant_software_apis.models import *
from parking_lot_apis.models import *
from petrol_pump_apis.models import *
from datetime import datetime, date, timedelta
# from datetime import date
from django.db.models import Q

from promotions.models import *

from promotions.models import *
from bill_design.models import *
from merchant_setting.models import *
from datetime import date

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from users.models import *
import random
import hashlib
from super_admin_settings.models import PaymentSetting
from bill_feedback.models import bill_feedback_question
from merchant_setting.models import MerchantPaymentSetting

from django.http import JsonResponse

from category_and_tags.models import *

from merchant_stamp.models import merchantusagestamp
from owner_stamp.models import *

import os 
from PIL import Image 
from PIL.ExifTags import TAGS
import base64
import string


def GetImageData(request, id):
    filtered_city_list = []

    my_bill = CustomerBill.objects.get(id = id)

    filename = my_bill.bill

    imgdata = base64.b64decode(filename)
    filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)

    # print(imgdata)

    image  = Image.open(bill)

    return JsonResponse({"data":filtered_city_list})



@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def Customer_Bill(request):
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

        bill_amt = request.POST['bill_amount']
        date = request.POST['bill_date']
        bill_tags_value = request.POST['bill_tags_value']
        
        remarks = request.POST['remarks']
        custom_business = request.POST['custom_business']

        if merchant_name and cust_category:
            bill_data = CustomerBill.objects.create(
                mobile_no=request.user.mobile_no,
                bill=bill_file,
                business_name=merchant_object,
                customer_bill_category=bill_category_object,
                bill_amount=bill_amt,
                bill_date=date,
                customer_added = True,
                bill_tags = bill_tags_value,
                remarks = remarks,
                custom_business_name = custom_business
            ).save()
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
                bill_tags = bill_tags_value,
                remarks = remarks,
                custom_business_name = custom_business
            ).save()
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
                bill_tags = bill_tags_value,
                remarks = remarks,
                custom_business_name = custom_business
            ).save()
            sweetify.success(request, title="Success", icon="success",
                                text="Bill Saved Successfully", timer=1500)
            
        else:
            bill_data = CustomerBill.objects.create(
                mobile_no=request.user.mobile_no,
                bill=bill_file,
                bill_amount=bill_amt,
                bill_date=date,
                customer_added = True,
                bill_tags = bill_tags_value,
                remarks = remarks,
                custom_business_name = custom_business
            ).save()
            sweetify.success(request, title="Success", icon="success",
                                text="Bill Saved Successfully", timer=1500)
        
    all_cust_bill = CustomerBill.objects.filter(
        mobile_no=request.user.mobile_no).order_by('-id',)

    bill_category_name = bill_category.objects.all()
    b_name = MerchantProfile.objects.all()

    customer_bill_tags = bill_tags.objects.all()

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

    context = {
        'business_name': b_name,
        'bill_category': bill_category_name,
        "customer_bill": all_cust_bill,
        "bill_tags": customer_bill_tags,
        'BillNavclass': 'active',
        "BillCollapseShow": "show",
        "AddBillsNavclass": "active"
    }
    return render(request, "customer/customer_bill/customer_bill.html", context)


@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def Edit_Customer_Bill(request):
    
    if request.method == "POST":
        idnum = request.POST['enid']

        try:
            if request.FILES['editfile']:
                CustomerBill.objects.filter(id=idnum).update(business_name=request.POST['edit_business'], customer_bill_category=request.POST['edit_category'], bill_amount=request.POST['edit_amount'], bill_date=request.POST['edit_date'], bill_tags = request.POST['edit_bill_tags_value'], remarks = request.POST["edit_remarks"], custom_business_name = request.POST["edit_custom_business"])
                bill_data = CustomerBill.objects.get(id=idnum)
                bill_data.bill = request.FILES['editfile']
                bill_data.save()
            else:
                CustomerBill.objects.filter(id=idnum).update(business_name=request.POST['edit_business'], customer_bill_category=request.POST['edit_category'], bill_amount=request.POST['edit_amount'], bill_date=request.POST['edit_date'], bill_tags = request.POST['edit_bill_tags_value'], remarks = request.POST["edit_remarks"], custom_business_name = request.POST["edit_custom_business"])

        except:
            CustomerBill.objects.filter(id=idnum).update(business_name=request.POST['edit_business'], customer_bill_category=request.POST['edit_category'], bill_amount=request.POST['edit_amount'], bill_date=request.POST['edit_date'], bill_tags = request.POST['edit_bill_tags_value'], remarks = request.POST["edit_remarks"], custom_business_name = request.POST["edit_custom_business"])


        
        sweetify.success(request, title="Success", icon='success',
                            text='Bill Updated Successfully', timer=1500)
    all_cust_bill = CustomerBill.objects.filter(
        mobile_no=request.user.mobile_no).order_by('-id')
    bill_category_name = bill_category.objects.all()
    b_name = MerchantProfile.objects.all()

    customer_bill_tags = bill_tags.objects.all()

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

    context = {
        'business_name': b_name,
        'bill_category': bill_category_name,
        "customer_bill": all_cust_bill,
        "bill_tags": customer_bill_tags,
        'BillNavclass': 'active',
        "BillCollapseShow": "show",
        "AddBillsNavclass": "active"
    }
    return render(request, "customer/customer_bill/customer_bill.html",context )


@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def delete_customer_bill(request, id):
    instance = CustomerBill.objects.get(id=id)
    status = instance.delete()

    if status:
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'error'})



def my_bill(request, id):
    # print("My bill")
    try:

        bill_details = CustomerBill.objects.get(bill_url=id)
        am = bill_details.bill_amount
        print("******")
        print(am)

        try:
            selected_stamp_id = bill_details.stamp_id
            latest_stamp_record = wstampmodels.objects.filter(id=selected_stamp_id)
        except:
            latest_stamp_record = '' 

        print("&&&")
        
        # print(business_name.id)
        try:
            merchant_business_object = MerchantProfile.objects.get(id = bill_details.business_name.id)

            print("merchant_business_object",merchant_business_object,)

            if merchant_business_object.id == 1188:
                merchant_split_image = True
            else:
                merchant_split_image = False
            merchant_user_object = GreenBillUser.objects.get(mobile_no = merchant_business_object.m_user)
        except:
            merchant_business_object = ""
            merchant_split_image = False


        print("&&&")

        try:
            merchant_user_id = Merchant_users.objects.filter(user_id = bill_details.user_id).values('merchant_user_id')[0]['merchant_user_id']

            merchant_user_object = GreenBillUser.objects.get(id = merchant_user_id)
        except:
            pass

        print("&&&")

        try:
            bill_design = bill_designs.objects.get(merchant_business_id = bill_details.business_name)
        except:
            bill_design = ""

        print("&&&")

        try:
            merchant_business_object = MerchantProfile.objects.get(id = bill_details.business_name.id)

            if merchant_business_object.m_business_logo:
                business_logo = merchant_business_object.m_business_logo.url
            else:

                if bill_design:
                    if bill_design.logo == "circular":
                        business_logo = "http://157.230.228.250/media/bill_design/circular-logo (2).png"
                    elif bill_design.logo == "square":
                        business_logo = "http://157.230.228.250/media/bill_design/rounded-corner-logo.png"
                    else:
                        business_logo = "http://157.230.228.250/static/assets/img/dashboard-logo.png"
                else:
                    business_logo = "http://157.230.228.250/static/assets/img/dashboard-logo.png"

            if merchant_business_object.m_address:
                business_address = merchant_business_object.m_address
            else:
                business_address = ""

        except:
            if bill_design:
                if bill_design.logo == "circular":
                    business_logo = "http://157.230.228.250/media/bill_design/circular-logo (2).png"
                elif bill_design.logo == "square":
                    business_logo = "http://157.230.228.250/media/bill_design/rounded-corner-logo.png"
                else:
                    business_logo = "http://157.230.228.250/static/assets/img/dashboard-logo.png"
            else:
                business_logo = "http://157.230.228.250/static/assets/img/dashboard-logo.png"

            business_address = ""

        print("&&&")
        ads_image_details = ""


        space = ads_below_bill.objects.filter(merchant = merchant_business_object.m_user, merchant_business_id = bill_details.business_name, ads_type='green_bill').last()

        today = datetime.strptime(str(date.today()), '%Y-%m-%d')

        green_bills_advertisement = ""

        try:
            if space:
                expiry_date_new = datetime.strptime(space.end_date, '%Y-%m-%d')
                start_date_new = datetime.strptime(space.start_date, '%Y-%m-%d')

                if today >= start_date_new and today <= expiry_date_new:

                    startswith = str(bill_details.business_name.id) + ','
                    endswith = ','+ str(bill_details.business_name.id)
                    contains = ','+ str(bill_details.business_name.id) + ','
                    exact = str(bill_details.business_name.id)

                    green_bill_merchant_ads = ads_for_green_bills.objects.filter(
                        Q(business_name_value__startswith = startswith) | 
                        Q(business_name_value__endswith = endswith) | 
                        Q(business_name_value__contains = contains) | 
                        Q(business_name_value__exact = exact)
                    ).last()

                    if green_bill_merchant_ads:

                        start_date = datetime.strptime(green_bill_merchant_ads.start_date, '%Y-%m-%d')
                        end_date = datetime.strptime(green_bill_merchant_ads.end_date, '%Y-%m-%d')

                        if today >= start_date and today <= end_date:
                            ads_image_details = ads_for_green_bills.objects.get(id = green_bill_merchant_ads.id)
                            green_bills_advertisement = True
                            views = ads_below_bill.objects.get(id=space.id)
                            views.count = views.count + 1
                            views.save()

                            views = ads_for_green_bills.objects.get(id=green_bill_merchant_ads.id)
                            views.count = views.count + 1
                            views.save()

            if not green_bills_advertisement:
                third_party_status = ads_below_bill.objects.filter(merchant = merchant_business_object.m_user, merchant_business_id = bill_details.business_name, ads_type='third_party', status = 1).last()
                if third_party_status:
                    expiry_date_new =  datetime.strptime(third_party_status.end_date, '%Y-%m-%d')
                    start_date_new =  datetime.strptime(third_party_status.start_date, '%Y-%m-%d')

                    if today <= expiry_date_new and today >= start_date_new:
                        ads_image_details = ads_below_bill.objects.get(id = third_party_status.id)
                        green_bills_advertisement = True
                        views = ads_below_bill.objects.get(id=third_party_status.id)
                        views.count = views.count + 1
                        views.save()

            if not green_bills_advertisement:
                ads_details = ads_below_bill.objects.filter(merchant = merchant_business_object.m_user, merchant_business_id = bill_details.business_name, active_ads = True).last()
                if ads_details:
                    ads_image_details = ads_below_bill.objects.get(id = ads_details.id)
                    green_bills_advertisement = True
                    views = ads_below_bill.objects.get(id=ads_details.id)
                    views.count = views.count + 1
                    views.save()
        except:
            ads_image_details = ""
       

   
        try:
            for_rating_1_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_object.id, for_rating = "1")
        except:
            for_rating_1_object = ""

        try:
            for_rating_2_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_object.id, for_rating = "2")
        except:
            for_rating_2_object = ""

        try:
            for_rating_3_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_object.id, for_rating = "3")
        except:
            for_rating_3_object = ""

        try:
            for_rating_4_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_object.id, for_rating = "4")
        except:
            for_rating_4_object = ""

        try:
            for_rating_5_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_object.id, for_rating = "5")
        except:
            for_rating_5_object = ""
        

        print("^%^^")
        context = {}
        upiid= ""
        try:
            
            payment_settings = MerchantPaymentSetting.objects.get(m_business_id = bill_details.business_name.id)
          
          
            choice = payment_settings.option
            print("^^^^^^^^^^^^^")
            print(choice)
            if choice == "upi_check":
                upiid = str(payment_settings.upi_id)
            
        except:
            payment_settings = ""
            upiid = ""
            choice = "none"
        print("Out")
        pay_to_do = ""
        
        
        if  choice == "payu_check" :

            if bill_details.payment_done == False:

                key = str(payment_settings.payu_key)
            
                SALT= str(payment_settings.payu_salt)

                # PAYU_BASE_URL = "https://test.payu.in/_payment"
                PAYU_BASE_URL = "https://secure.payu.in/_payment"
                # PAYU_BASE_URL = "https://info.payu.in/merchant/postservice.php?form=2"

                action = ''
                firstname = str('My bill')
                email = str('ragni.n@zappkode.com')
                phone = str(bill_details.mobile_no)
                surl = "http://157.230.228.250/my-bill-payment-link-success/"
                furl = "http://157.230.228.250/my-bill-payment-link-fail/"

                udf1 = id
                udf2 = ""
                udf3 = ""
                udf4 = ""
                udf5 = ""

                random_str =  random.randint(9999999, 99999999)

                hash_object = hashlib.sha256(b'randint(0,20)' + bytes(bill_details.id) + bytes(random_str))

                txnid=hash_object.hexdigest()[0:20]

                hashh = ''
                context = {}
                posted = {}
                posted['txnid'] = txnid
                posted['key'] = key
                productinfo = str('my bill pay link')
                amount = str(bill_details.bill_amount)

                command = 'release_settlement'

                var1 = "403993715524604663"

                hashSequence = key + "|" + txnid + "|" + amount + "|" + productinfo + "|" + firstname + "|" + email + "|" + udf1 + "|" + udf2 + "|" + udf3 + "|" + udf4 + "|" + udf5 + "||||||" + SALT

                # hashSequence = key + "|" + command + "|" + var1 + "|" + SALT

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
        else:
            
            base_link = "upi://pay?pa="+upiid+"&pn=Payee Name&tn=Payment Message&am="
            pay_to_do = base_link+str(am)+"&cu=INR"
           
        
        print(pay_to_do)
        context['merchant_split_image'] = merchant_split_image
        context['bill_details'] = bill_details
        context['business_logo'] = business_logo
        context['business_address'] = business_address
        context['bill_design'] = bill_design
        context['url_slug'] = id
        context['for_rating_1_object'] = for_rating_1_object
        context['for_rating_2_object'] = for_rating_2_object
        context['for_rating_3_object'] = for_rating_3_object
        context['for_rating_4_object'] = for_rating_4_object
        context['for_rating_5_object'] = for_rating_5_object
        
        context['latest_stamp_record'] = latest_stamp_record
        context['ads_image_details'] = ads_image_details

        context['payment_to_do'] = pay_to_do

        context['choice'] = choice
       
        return render(request, "customer/customer_bill/my-bill.html", context)

    except:
        return render(request, 'page-404.html')

def view_ads_record(request, id):
    try:
        data = []
        base_url = "http://157.230.228.250/"
        ads_details = ads_below_bill.objects.filter(active_ads = True, id = id)
        green_bill_merchant_ads = ads_for_green_bills.objects.filter(active_ads = True, id = id)
        if ads_details:
            try:
                object = ads_below_bill.objects.get(id=id)
                redirect_url = object.redirect_url
                object.count = object.count + 1
                object.save()
                redirect_url = green_bill_merchant_ads[0].redirect_url
            except:
                pass
        else:
            try: 
                redirect_url = green_bill_merchant_ads[0].redirect_url
                object = ads_for_green_bills.objects.get(id=id)
                object.count = object.count + 1
                object.save()
            except:
                pass

        
        return redirect(redirect_url)
    except:
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
    payment_link = CustomerBill.objects.get(bill_url=link_url)

    try:
        payment_settings = MerchantPaymentSetting.objects.get(m_business_id = payment_link.business_name.id)
    except:
        payment_settings = ""

    SALT = str(payment_settings.payu_salt)

    retHashSeq = SALT +'|'+status+'|||||||'+ udf4 + '|' + udf3 + '|' +  udf2 +'|'+ udf1 + '|' + email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+ key

    hash_string = retHashSeq.encode('utf-8')
    
    hashh = hashlib.sha512(hash_string).hexdigest().lower()

    if status == "success":
        if hashh == posted_hash:
            
            result = CustomerBill.objects.filter(id=payment_link.id).update(payment_done = True, payment_date = timezone.now(), transaction_id = txnid, payu_transaction_id = mihpayid)
            if result:
                sweetify.success(request, title="Success", icon='success', text='Transcation done Successfully.', timer=1500)
                return redirect(my_bill, link_url)
            else:
                sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
                return redirect(my_bill, link_url)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
            return redirect(my_bill, link_url)
    else:
        sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
        return redirect(my_bill, link_url)

@csrf_exempt
def payment_link_fail(request):
    udf1 = request.POST["udf1"]
    sweetify.success(request, title="Oops...", icon='error', text='Transcation Failed, Please try again.', timer=1500)
    return redirect(my_bill, udf1)


def my_bill1(request, id):
    try:
        bill_details = SavePetrolPumpBill.objects.get(bill_url=id)
        context = {'bill_details' : bill_details}
        return render(request, "customer/customer_bill/my-bill1.html", context)
    except:
        return render(request, 'page-404.html')

def my_bill2(request, id):
    try:
        bill_details = SavePetrolPumpBill.objects.get(bill_url=id)
        context = {'bill_details' : bill_details}
        return render(request, "customer/customer_bill/my-bill2.html", context)
    except:
        return render(request, 'page-404.html')

@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def my_bills_req(request):
    pass

@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def my_bills(request, bill_type):
    # print("in func")
    # print(bill_type)
    try:
        # print("in try")
        deleted_bill_object = Deleted_Bills_By_Days_setting.objects.get(m_user=request.user)
        # day = deleted_bill_object.deleted_days
        # day = int(day)

        days = deleted_bill_object.delete_days_customer
        panel = deleted_bill_object.delete_from_customer
        print(days,panel)
    except:
        # print("in except")
        panel = "none"
    
    if panel == 1:
        print("in panel")
        if request.method == "POST" and not request.POST.get("submit") == "merchants_btn":
            send_bill_id = request.POST['send_bill_id']
            send_bill_to_merchant = request.POST['send_bill_to_merchant']
            send_bill_data_table = request.POST['send_bill_data_table']

            if send_bill_to_merchant:
                merchant_business_id = MerchantProfile.objects.get(id = send_bill_to_merchant)
                user_id = GreenBillUser.objects.get(mobile_no = merchant_business_id.m_user)
            
            if request.POST['send_bill_data_table'] == "CustomerBill":


                customer_bill = CustomerBill.objects.filter(id =send_bill_id)

                letters = string.ascii_letters
                digit = string.digits
                random_string = str(customer_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                customer_bill1 = MerchantBill.objects.create(user_id = customer_bill[0].user_id, mobile_no = customer_bill[0].mobile_no, email = customer_bill[0].email,
                        bill = customer_bill[0].bill, business_name = customer_bill[0].business_name, bill_received_business_name = merchant_business_id.id,
                        invoice_no = customer_bill[0].invoice_no, green_bill_transaction = customer_bill[0].green_bill_transaction, green_bill_print_transaction = customer_bill[0].green_bill_print_transaction,
                        print_transaction = customer_bill[0].print_transaction, bill_amount = customer_bill[0].bill_amount, customer_bill_category = customer_bill[0].customer_bill_category,stamp_id=customer_bill[0].stamp_id, exe_bill_type = customer_bill[0].exe_bill_type
                    )
                customer_bill_new = MerchantBill.objects.filter(id=customer_bill1.id).update(bill_url = random_string) 

                CustomerBill.objects.filter(id =customer_bill[0].id).update(delete_bill = True)
                sweetify.success(request, title="success", icon='success', text='Bill Transfer successfully !!!', timer=1500)

            elif request.POST['send_bill_data_table'] == "SaveParkingLotBill":

                parking_bill = SaveParkingLotBill.objects.filter(id=send_bill_id)

                try:
                    business_name1 = MerchantProfile.objects.get(id = parking_bill[0].m_business_id)
                except:
                    business_name1 = ""

                try:
                    bill_category_temp = bill_category.objects.get(id = parking_bill[0].bill_category_id)
                except:
                    bill_category_temp = ""

                customer_bill1 = MerchantBill.objects.create(user_id = parking_bill[0].user_id, mobile_no = parking_bill[0].mobile_no,
                        bill = parking_bill[0].bill_file, business_name = business_name1, bill_received_business_name = merchant_business_id.id,
                        invoice_no = parking_bill[0].invoice_no, 
                        bill_amount = parking_bill[0].total, customer_bill_category = bill_category_temp
                    )

                letters = string.ascii_letters
                digit = string.digits
                random_string = str(parking_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                customer_bill_new = MerchantBill.objects.filter(id=customer_bill1.id).update(bill_url = random_string) 

                SaveParkingLotBill.objects.filter(id=parking_bill[0].id).update(delete_bill = True)

                sweetify.success(request, title="success", icon='success', text='Bill Transfer successfully !!!', timer=1500)

            elif request.POST['send_bill_data_table'] == "SavePetrolPumpBill":

                petrol_pump = SavePetrolPumpBill.objects.filter(id=send_bill_id)

                business_name1 = MerchantProfile.objects.get(id = petrol_pump[0].m_business_id)
                

                try:
                    bill_category_temp = bill_category.objects.get(id = petrol_pump[0].bill_category_id)
                except:
                    bill_category_temp = ""

                customer_bill1 = MerchantBill.objects.create(user_id = petrol_pump[0].user_id, mobile_no = petrol_pump[0].mobile_no,
                    bill = petrol_pump[0].bill_file, business_name = business_name1, bill_received_business_name = merchant_business_id.id,
                    invoice_no = petrol_pump[0].invoice_no, 
                    bill_amount = petrol_pump[0].total_amount, customer_bill_category = bill_category_temp
                )

                letters = string.ascii_letters
                digit = string.digits
                random_string = str(petrol_pump[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                customer_bill_new = MerchantBill.objects.filter(id=customer_bill1.id).update(bill_url = random_string)

                SavePetrolPumpBill.objects.filter(id=petrol_pump[0].id).update(delete_bill = True)

                sweetify.success(request, title="success", icon='success', text='Bill Transfer successfully !!!', timer=1500)
            else:
                sweetify.error(request, title="error", icon='error', text='Failed to Transfer!!!', timer=1500)

        data = []

        bill_categories = bill_category.objects.all().order_by('bill_category_name')

        allocated_bill_categories = []

        bills = []

        customer_merchant_businesses = MerchantProfile.objects.filter(m_user = request.user)

        for category in bill_categories:
            if request.POST.get("submit") == "merchants_btn":
                from_date = request.POST.get("from_date1")
                to_date = request.POST.get("to_date1")

                DATE_FORMAT = '%Y-%m-%d'
                date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
                day_later = date_time_obj + timedelta(days=1)
                x = day_later.date()
                ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

                billing_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
                start_date = billing_from_date.split('-')
                start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
                sd_filter = start_date.strftime(DATE_FORMAT)

                customer_bill_count = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, customer_bill_category = category, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
                if customer_bill_count > 0:
                    if category in allocated_bill_categories:
                        continue
                    else:
                        allocated_bill_categories.append(category)

                parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, is_pass = False, bill_category_id = category.id, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
                if parking_bill_count > 0:
                    if category in allocated_bill_categories:
                        continue
                    elif category.id == 27:
                        allocated_bill_categories.append(category)

                petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = category.id, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
                if petrol_bill_count > 0:
                    if category in allocated_bill_categories:
                        continue
                    elif category.id == 26:
                        allocated_bill_categories.append(category)


            else:
                customer_bill_count = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, customer_bill_category = category, delete_bill = False).count()
                if customer_bill_count > 0:
                    if category in allocated_bill_categories:
                        continue
                    else:
                        allocated_bill_categories.append(category)

                parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, is_pass = False, bill_category_id = category.id, delete_bill = False).count()
                if parking_bill_count > 0:
                    if category in allocated_bill_categories:
                        continue
                    elif category.id == 27:
                        allocated_bill_categories.append(category)

                petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = category.id, delete_bill = False).count()
                if petrol_bill_count > 0:
                    if category in allocated_bill_categories:
                        continue
                    elif category.id == 26:
                        allocated_bill_categories.append(category)

        customer_bill_tags = bill_tags.objects.all()

        category_bills_count = 0

        for bill_categories in allocated_bill_categories:

            bill_categories.bill_count = 0

            bill_categories.color = random_color()

            if request.POST.get("submit") == "merchants_btn":       
                customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, customer_bill_category = bill_categories, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
            else:
                customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, customer_bill_category = bill_categories, delete_bill = False).order_by('-id')

            bill_categories.bills = []

            for bill in customer_bill_list:
                bill_date = bill.created_at.date()
             
                current_date = date.today() 
             
                diff_date = (current_date-bill_date).days
                if diff_date <= int(days) :
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
                        'delete_bill':bill.delete_bill,
                        'color': random_color(),
                        'category_type': 'category',
                    })

                    bill_categories.bill_count += 1
                    category_bills_count += 1

            if request.POST.get("submit") == "merchants_btn": 
                parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = bill_categories.id, is_pass = False, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
            else:
                parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = bill_categories.id, is_pass = False, delete_bill = False).order_by('-id')

            for bill in parking_bill_list:
                bill_date = bill.created_at.date()
             
                current_date = date.today() 
             
                diff_date = (current_date-bill_date).days
                if diff_date <= int(days) :
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
                        'delete_bill':bill.delete_bill,
                        'color': random_color(),
                        'category_type': 'category',
                    })

                    bill_categories.bill_count += 1 
                    category_bills_count += 1

            if request.POST.get("submit") == "merchants_btn":             
                petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = bill_categories.id, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
            else:
                petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = bill_categories.id, delete_bill = False).order_by('-id')

            for bill in petrol_bill_list:
                bill_date = bill.created_at.date()
             
                current_date = date.today() 
             
                diff_date = (current_date-bill_date).days
                if diff_date <= int(days) :
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
                        'delete_bill':bill.delete_bill,
                        'color': random_color(),
                        'category_type': 'category',
                    })

                    bill_categories.bill_count += 1
                    category_bills_count += 1

        # data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

        bill_category_name = bill_category.objects.all()
        b_name = MerchantProfile.objects.all()

        # Bill By Merchant
        
        all_merchants = MerchantProfile.objects.all().order_by('m_business_name')
        all_merchants1 = MerchantProfile.objects.all().order_by('m_business_name').count()
        
        allocated_merchants = []

        for merchants in all_merchants:

            if request.POST.get("submit") == "merchants_btn":  
                customer_bill_count = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, business_name = merchants, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
            else:
                customer_bill_count = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, business_name = merchants, delete_bill = False).count()

            if customer_bill_count > 0:
                if merchants in allocated_merchants:
                    continue
                else:
                    allocated_merchants.append(merchants)
            # print(allocated_merchants,"-------------------------------------")
            
            if request.POST.get("submit") == "merchants_btn":  
                parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchants.id, is_pass = False, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
            else:
                parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchants.id, is_pass = False, delete_bill = False).count()
            if parking_bill_count > 0:
                if merchants in allocated_merchants:
                    continue
                else:
                    allocated_merchants.append(merchants)

            if request.POST.get("submit") == "merchants_btn":  
                petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchants.id, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
            else:
                petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchants.id, delete_bill = False).count()

            if petrol_bill_count > 0:
                if merchants in allocated_merchants:
                    continue
                else:
                    allocated_merchants.append(merchants)

            if request.POST.get("submit") == "merchants_btn":  
                customer_bill_count1 = CustomerBill.objects.filter(mobile_no = request.user, business_name__isnull=True, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
            else:
                customer_bill_count1 = CustomerBill.objects.filter(mobile_no = request.user, business_name__isnull=True, delete_bill = False).count()
            # print('customer_bill_count1223',customer_bill_count1)
            if customer_bill_count1 > 0:
                buisness_name = 'Others'
                if buisness_name in allocated_merchants:
                    continue
                else:
                    allocated_merchants.append(buisness_name)

     

        bill_count = ''
        merchant_color = ''
        merchant_bills = []
        merchant_bills_count = 0
        for merchant in allocated_merchants:
            if type(merchant) != str and merchant != None:

                merchant.bill_count = 0

                merchant.color = random_color()

                if request.POST.get("submit") == "merchants_btn":
                    customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, business_name = merchant, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
                else:
                    customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, business_name = merchant, delete_bill = False).order_by('-id')

                merchant.bills = []

                for bill in customer_bill_list:
                    bill_date = bill.created_at.date()
             
                    current_date = date.today() 
             
                    diff_date = (current_date-bill_date).days
                    if diff_date <= int(days) :
                        try:
                            bill_file = bill.bill
                        except:
                            bill_file = ""

                        if bill.bill_tags:
                            bill_tags_temp = bill.bill_tags
                        else:
                            bill_tags_temp = "0"

                        merchant.bills.append({
                            'id': bill.id,
                            'amount': str(bill.bill_amount),
                            'bill_date': bill.bill_date,
                            'bill_file': bill_file,
                            'bill_category' : bill.customer_bill_category,
                            'business_name' : bill.business_name,
                            'bill_tags' : bill_tags_temp,
                            'remarks' : bill.remarks,
                            'custom_business_name': bill.custom_business_name,
                            'db_table': "CustomerBill",
                            'customer_added': bill.customer_added,
                            'bill_url': bill.bill_url,
                            'invoice_no':bill.invoice_no,
                            'delete_bill': bill.delete_bill,
                            'color': random_color(),
                            'category_type': 'merchant',
                        })

                        merchant.bill_count += 1
                        merchant_bills_count += 1

                if request.POST.get("submit") == "merchants_btn":
                    parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchant.id, is_pass = False, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
                else:
                    parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchant.id, is_pass = False, delete_bill = False).order_by('-id')
                for bill in parking_bill_list:
                    bill_date = bill.created_at.date()
             
                    current_date = date.today() 
             
                    diff_date = (current_date-bill_date).days
                    if diff_date <= int(days) :
                        try:
                            bill_file = bill.bill_file
                        except:
                            bill_file = ""
                        
                        if bill.bill_tags:
                            bill_tags_temp = bill.bill_tags
                        else:
                            bill_tags_temp = "0"

                        try:
                            business_name = MerchantProfile.objects.get(id = bill.m_business_id)
                        except:
                            business_name = ""

                        try:
                            bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
                        except:
                            bill_category_temp = ""

                        merchant.bills.append({
                            'id': bill.id,
                            'amount': str(bill.amount),
                            'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                            'bill_file': bill_file,
                            'bill_category' : bill_category_temp,
                            'business_name' : business_name,
                            'bill_tags' : bill_tags_temp,
                            'remarks' : bill.remarks,
                            'custom_business_name': "",
                            'db_table': "SaveParkingLotBill",
                            'customer_added': False,
                            'bill_url': bill.bill_url,
                            'invoice_no':bill.invoice_no,
                            'delete_bill': bill.delete_bill,
                            'color': random_color(),
                            'category_type': 'merchant',
                        })

                        merchant.bill_count += 1
                        merchant_bills_count += 1
                            
                if request.POST.get("submit") == "merchants_btn":
                    petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchant.id, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
                else:
                    petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchant.id, delete_bill = False).order_by('-id')

                for bill in petrol_bill_list:
                    bill_date = bill.created_at.date()
                    current_date = date.today() 
                    diff_date = (current_date-bill_date).days
                    if diff_date <= int(days) :
                        try:
                            bill_file = bill.bill_file
                        except:
                            bill_file = ""
                        
                        if bill.bill_tags:
                            bill_tags_temp = bill.bill_tags
                        else:
                            bill_tags_temp = "0"

                        try:
                            business_name = MerchantProfile.objects.get(id = bill.m_business_id)
                        except:
                            business_name = ""

                        try:
                            bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
                        except:
                            bill_category_temp = ""

                        merchant.bills.append({
                            'id': bill.id,
                            'amount': str(bill.total_amount),
                            'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                            'bill_file': bill_file,
                            'bill_category' : bill_category_temp,
                            'business_name' : business_name,
                            'bill_tags' : bill_tags_temp,
                            'remarks' : bill.remarks,
                            'custom_business_name': "",
                            'db_table': "SavePetrolPumpBill",
                            'customer_added': False,
                            'bill_url': bill.bill_url,
                            'invoice_no':bill.invoice_no,
                            'delete_bill': bill.delete_bill,
                            'color': random_color(),
                            'category_type': 'merchant',
                        })

                        merchant.bill_count += 1
                        merchant_bills_count += 1
                    # print('merchant.bills',merchant.bills)


            if type(merchant) == str:
                merchant_color = random_color()
                if request.POST.get("submit") == "merchants_btn":
                    customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user, business_name__isnull=True, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
                    customer_bill_list1 = CustomerBill.objects.filter(mobile_no = request.user, business_name__isnull=True, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
                else:
                    customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user, business_name__isnull=True, delete_bill = False).order_by('-id')
                    customer_bill_list1 = CustomerBill.objects.filter(mobile_no = request.user, business_name__isnull=True, delete_bill = False).count()

                bill_count = customer_bill_list1

                for bill in customer_bill_list:
                    bill_date = bill.created_at.date()
                    current_date = date.today() 
                    diff_date = (current_date-bill_date).days
                    if diff_date <= int(days) :
                        try:
                            bill_file = bill.bill
                        except:
                            bill_file = ""

                        if bill.bill_tags:
                            bill_tags_temp = bill.bill_tags
                        else:
                            bill_tags_temp = "0"

                        merchant_bills.append({
                            'id': bill.id,
                            'amount': str(bill.bill_amount),
                            'bill_date': bill.bill_date,
                            'bill_file': bill_file,
                            'bill_category' : bill.customer_bill_category,
                            'business_name' : bill.custom_business_name if bill.custom_business_name else '',
                            'bill_tags' : bill_tags_temp,
                            'remarks' : bill.remarks,
                            # 'custom_business_name': bill.custom_business_name,
                            'db_table': "CustomerBill",
                            'customer_added': bill.customer_added,
                            'bill_url': bill.bill_url,
                            'invoice_no':bill.invoice_no,
                            'delete_bill': bill.delete_bill,
                            'color': random_color(),
                            'category_type': 'merchant',
                        })
                        # merchant.bill_count += 1
                        merchant_bills_count += 1
        
        bill_tags_list = bill_tags.objects.all().order_by('bill_tags_name')

        allocated_tag_list = []

        for tag in bill_tags_list:
            startswith = str(tag.id) + ','
            endswith = ','+ str(tag.id)
            contains = ','+ str(tag.id) + ','
            exact = str(tag.id)
            if request.POST.get("submit") == "merchants_btn":
                customer_bill_count = CustomerBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(created_at__gte = sd_filter), Q(created_at__lte = ed_filter), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()
            else:
                customer_bill_count = CustomerBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()
            
            if customer_bill_count > 0:
                if tag in allocated_tag_list:
                    continue
                else:
                    allocated_tag_list.append(tag)

            if request.POST.get("submit") == "merchants_btn":
                parking_bill_count = SaveParkingLotBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(created_at__gte = sd_filter), Q(created_at__lte = ed_filter), Q(is_pass = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()
            else:
                parking_bill_count = SaveParkingLotBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(is_pass = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()

            if parking_bill_count > 0:
                if tag in allocated_tag_list:
                    continue
                else:
                    allocated_tag_list.append(tag)

            if request.POST.get("submit") == "merchants_btn":
                petrol_bill_count = SavePetrolPumpBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(created_at__gte = sd_filter), Q(created_at__lte = ed_filter), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()
            else:
                petrol_bill_count = SavePetrolPumpBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()

            if petrol_bill_count > 0:
                if tag in allocated_tag_list:
                    continue
                else:
                    allocated_tag_list.append(tag)

        tags_bills_count = 0


        for tag in allocated_tag_list:

            tag.bill_count = 0
            tag.color = random_color()

            startswith = str(tag.id) + ','
            endswith = ','+ str(tag.id)
            contains = ','+ str(tag.id) + ','
            exact = str(tag.id)

            tag.bills = []
            
            if request.POST.get("submit") == "merchants_btn":
                customer_bill_list = CustomerBill.objects.filter(Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact), Q(mobile_no=request.user.mobile_no), Q(delete_bill = False), Q(created_at__gte = sd_filter), Q(created_at__lte = ed_filter)).order_by('-id')
            else:
                customer_bill_list = CustomerBill.objects.filter(Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact), Q(delete_bill = False), Q(mobile_no=request.user.mobile_no)).order_by('-id')


            data = []

            for bill in customer_bill_list:
                bill_date = bill.created_at.date()
                current_date = date.today() 
                diff_date = (current_date-bill_date).days
                if diff_date <= int(days) :
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

                    tag.bills.append({
                        'id': bill.id,
                        'amount': str(bill.bill_amount),
                        'bill_date': bill.bill_date,
                        'bill_file': bill_file,
                        'bill_category' : bill.customer_bill_category,
                        'business_name' : business_names,
                        'bill_tags' : bill_tags_temp,
                        'remarks' : bill.remarks,
                        'custom_business_name': "",
                        'db_table': "CustomerBill",
                        'customer_added': bill.customer_added,
                        'bill_url': bill.bill_url,
                        'invoice_no':bill.invoice_no,
                        'delete_bill':bill.delete_bill,
                        'color': random_color(),
                        'category_type': 'tag',
                    })

                    tag.bill_count += 1 
                    tags_bills_count += 1

            if request.POST.get("submit") == "merchants_btn":
                parking_bill_list = SaveParkingLotBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(created_at__gte = sd_filter), Q(created_at__lte = ed_filter), Q(is_pass = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).order_by('-id')
            else:
                parking_bill_list = SaveParkingLotBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(is_pass = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).order_by('-id')

            for bill in parking_bill_list:
                bill_date = bill.created_at.date()
                current_date = date.today() 
                diff_date = (current_date-bill_date).days
                if diff_date <= int(days) :
                    try:
                        bill_file = bill.bill_file
                    except:
                        bill_file = ""
                    
                    if bill.bill_tags:
                        bill_tags_temp = bill.bill_tags
                    else:
                        bill_tags_temp = "0"

                    try:
                        business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
                    except:
                        business_name = ""

                    try:
                        bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
                    except:
                        bill_category_temp = ""


                    tag.bills.append({
                       'id': bill.id,
                        'amount': str(bill.amount),
                        'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                        'bill_file': bill_file,
                        'bill_category' : bill_category_temp,
                        'business_name' : business_name,
                        'bill_tags' : bill_tags_temp,
                        'remarks' : bill.remarks,
                        'custom_business_name': "",
                        'db_table': "SaveParkingLotBill",
                        'customer_added': False,
                        'bill_url': bill.bill_url,
                        'invoice_no':bill.invoice_no,
                        'delete_bill': bill.delete_bill,
                        'color': random_color(),
                        'category_type': 'tag',
                    })

                    tag.bill_count += 1
                    tags_bills_count += 1

            if request.POST.get("submit") == "merchants_btn":
                petrol_bill_list = SavePetrolPumpBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(created_at__gte = sd_filter), Q(created_at__lte = ed_filter), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).order_by('-id')
            else:
                petrol_bill_list = SavePetrolPumpBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).order_by('-id')

            for bill in petrol_bill_list:
                bill_date = bill.created_at.date()
                current_date = date.today() 
                diff_date = (current_date-bill_date).days
                if diff_date <= int(days) :
                    try:
                        bill_file = bill.bill_file
                    except:
                        bill_file = ""
                    
                    if bill.bill_tags:
                        bill_tags_temp = bill.bill_tags
                    else:
                        bill_tags_temp = "0"

                    try:
                        business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
                    except:
                        business_name = ""

                    try:
                        bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
                    except:
                        bill_category_temp = ""

                    tag.bills.append({
                        'id': bill.id,
                        'amount': str(bill.total_amount),
                        'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                        'bill_file': bill_file,
                        'bill_category' : bill_category_temp,
                        'business_name' : business_name,
                        'bill_tags' : bill_tags_temp,
                        'remarks' : bill.remarks,
                        'custom_business_name': "",
                        'db_table': "SavePetrolPumpBill",
                        'customer_added': False,
                        'bill_url': bill.bill_url,
                        'invoice_no':bill.invoice_no,
                        'delete_bill': bill.delete_bill,
                        'color': random_color(),
                        'category_type': 'tag',
                    })

                    tag.bill_count += 1
                    tags_bills_count += 1

        # for bill in allocated_bill_categories:
        #     category_bills_count += bill.bill_count

        # for bill in allocated_merchants:
        #     merchant_bills_count = len(bill.bills)

        
        # sorted_tag_list = sorted(allocated_tag_list, key=lambda item: item.get("tag_name"))
        if request.POST.get("submit") == "merchants_btn":
            pill_head = ''

            if bill_type == "category":
                pill_head = 'category'
            elif bill_type == "merchant":
                pill_head = 'merchant'
            elif bill_type == "tag":
                pill_head = 'tag'

            context = {
                # "bills" : bills,
                "allocated_bill_categories": allocated_bill_categories,
                "allocated_merchants": allocated_merchants,
                "allocated_tag": allocated_tag_list,
                'business_names': b_name,
                'bill_category': bill_category_name,
                "bill_tags": customer_bill_tags,
                "from_date1": from_date,
                "to_date1": to_date,
                "bill_count":bill_count,
                "merchant_color":merchant_color,
                "merchant_bills":merchant_bills,
                "custom_business_name":"Others",
                'MyBillsNavclass': 'active',
                'category_bill_count':category_bills_count,
                'merchant_bills_count':merchant_bills_count,
                'tags_bills_count': tags_bills_count,
                'pill_head':pill_head,
            }
        else:
            pill_head = ''
            if bill_type == "category":
                pill_head = 'category'
            elif bill_type == "merchant":
                pill_head = 'merchant'
            elif bill_type == "tag":
                pill_head = 'tag'

            context = {
                # "bills" : bills,
                "allocated_bill_categories": allocated_bill_categories,
                "allocated_merchants": allocated_merchants,
                "allocated_tag": allocated_tag_list,
                'business_names': b_name,
                'bill_category': bill_category_name,
                "bill_tags": customer_bill_tags,
                "customer_merchant_businesses": customer_merchant_businesses,
                "bill_count":bill_count,
                "merchant_color":merchant_color,
                "merchant_bills":merchant_bills,
                "custom_business_name":"Others",
                'MyBillsNavclass': 'active',
                'category_bill_count':category_bills_count,
                'merchant_bills_count':merchant_bills_count,
                'tags_bills_count': tags_bills_count,
                'pill_head':pill_head,
            }
    else:
        if request.method == "POST" and not request.POST.get("submit") == "merchants_btn":
            send_bill_id = request.POST['send_bill_id']
            send_bill_to_merchant = request.POST['send_bill_to_merchant']
            send_bill_data_table = request.POST['send_bill_data_table']

            if send_bill_to_merchant:
                merchant_business_id = MerchantProfile.objects.get(id = send_bill_to_merchant)
                user_id = GreenBillUser.objects.get(mobile_no = merchant_business_id.m_user)
            
            if request.POST['send_bill_data_table'] == "CustomerBill":


                customer_bill = CustomerBill.objects.filter(id =send_bill_id)

                letters = string.ascii_letters
                digit = string.digits
                random_string = str(customer_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                customer_bill1 = MerchantBill.objects.create(user_id = customer_bill[0].user_id, mobile_no = customer_bill[0].mobile_no, email = customer_bill[0].email,
                        bill = customer_bill[0].bill, business_name = customer_bill[0].business_name, bill_received_business_name = merchant_business_id.id,
                        invoice_no = customer_bill[0].invoice_no, green_bill_transaction = customer_bill[0].green_bill_transaction, green_bill_print_transaction = customer_bill[0].green_bill_print_transaction,
                        print_transaction = customer_bill[0].print_transaction, bill_amount = customer_bill[0].bill_amount, customer_bill_category = customer_bill[0].customer_bill_category,stamp_id=customer_bill[0].stamp_id, exe_bill_type = customer_bill[0].exe_bill_type
                    )
                customer_bill_new = MerchantBill.objects.filter(id=customer_bill1.id).update(bill_url = random_string) 

                CustomerBill.objects.filter(id =customer_bill[0].id).update(delete_bill = True)
                sweetify.success(request, title="success", icon='success', text='Bill Transfer successfully !!!', timer=1500)

            elif request.POST['send_bill_data_table'] == "SaveParkingLotBill":

                parking_bill = SaveParkingLotBill.objects.filter(id=send_bill_id)

                try:
                    business_name1 = MerchantProfile.objects.get(id = parking_bill[0].m_business_id)
                except:
                    business_name1 = ""

                try:
                    bill_category_temp = bill_category.objects.get(id = parking_bill[0].bill_category_id)
                except:
                    bill_category_temp = ""

                customer_bill1 = MerchantBill.objects.create(user_id = parking_bill[0].user_id, mobile_no = parking_bill[0].mobile_no,
                        bill = parking_bill[0].bill_file, business_name = business_name1, bill_received_business_name = merchant_business_id.id,
                        invoice_no = parking_bill[0].invoice_no, 
                        bill_amount = parking_bill[0].total, customer_bill_category = bill_category_temp
                    )

                letters = string.ascii_letters
                digit = string.digits
                random_string = str(parking_bill[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                customer_bill_new = MerchantBill.objects.filter(id=customer_bill1.id).update(bill_url = random_string) 

                SaveParkingLotBill.objects.filter(id=parking_bill[0].id).update(delete_bill = True)

                sweetify.success(request, title="success", icon='success', text='Bill Transfer successfully !!!', timer=1500)

            elif request.POST['send_bill_data_table'] == "SavePetrolPumpBill":

                petrol_pump = SavePetrolPumpBill.objects.filter(id=send_bill_id)

                business_name1 = MerchantProfile.objects.get(id = petrol_pump[0].m_business_id)
                

                try:
                    bill_category_temp = bill_category.objects.get(id = petrol_pump[0].bill_category_id)
                except:
                    bill_category_temp = ""

                customer_bill1 = MerchantBill.objects.create(user_id = petrol_pump[0].user_id, mobile_no = petrol_pump[0].mobile_no,
                    bill = petrol_pump[0].bill_file, business_name = business_name1, bill_received_business_name = merchant_business_id.id,
                    invoice_no = petrol_pump[0].invoice_no, 
                    bill_amount = petrol_pump[0].total_amount, customer_bill_category = bill_category_temp
                )

                letters = string.ascii_letters
                digit = string.digits
                random_string = str(petrol_pump[0].id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))

                customer_bill_new = MerchantBill.objects.filter(id=customer_bill1.id).update(bill_url = random_string)

                SavePetrolPumpBill.objects.filter(id=petrol_pump[0].id).update(delete_bill = True)

                sweetify.success(request, title="success", icon='success', text='Bill Transfer successfully !!!', timer=1500)
            else:
                sweetify.error(request, title="error", icon='error', text='Failed to Transfer!!!', timer=1500)

        data = []

        bill_categories = bill_category.objects.all().order_by('bill_category_name')

        allocated_bill_categories = []

        bills = []

        customer_merchant_businesses = MerchantProfile.objects.filter(m_user = request.user)

        for category in bill_categories:
            if request.POST.get("submit") == "merchants_btn":
                from_date = request.POST.get("from_date1")
                to_date = request.POST.get("to_date1")

                DATE_FORMAT = '%Y-%m-%d'
                date_time_obj = datetime.strptime(to_date, '%Y-%m-%d')
                day_later = date_time_obj + timedelta(days=1)
                x = day_later.date()
                ed_filter = datetime.strptime(str(x), '%Y-%m-%d')

                billing_from_date = datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%d-%m-%Y')
                start_date = billing_from_date.split('-')
                start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
                sd_filter = start_date.strftime(DATE_FORMAT)

                customer_bill_count = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, customer_bill_category = category, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
                if customer_bill_count > 0:
                    if category in allocated_bill_categories:
                        continue
                    else:
                        allocated_bill_categories.append(category)

                parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, is_pass = False, bill_category_id = category.id, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
                if parking_bill_count > 0:
                    if category in allocated_bill_categories:
                        continue
                    elif category.id == 27:
                        allocated_bill_categories.append(category)

                petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = category.id, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
                if petrol_bill_count > 0:
                    if category in allocated_bill_categories:
                        continue
                    elif category.id == 26:
                        allocated_bill_categories.append(category)


            else:
                customer_bill_count = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, customer_bill_category = category, delete_bill = False).count()
                if customer_bill_count > 0:
                    if category in allocated_bill_categories:
                        continue
                    else:
                        allocated_bill_categories.append(category)

                parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, is_pass = False, bill_category_id = category.id, delete_bill = False).count()
                if parking_bill_count > 0:
                    if category in allocated_bill_categories:
                        continue
                    elif category.id == 27:
                        allocated_bill_categories.append(category)

                petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = category.id, delete_bill = False).count()
                if petrol_bill_count > 0:
                    if category in allocated_bill_categories:
                        continue
                    elif category.id == 26:
                        allocated_bill_categories.append(category)

        customer_bill_tags = bill_tags.objects.all()

        category_bills_count = 0

        for bill_categories in allocated_bill_categories:

            bill_categories.bill_count = 0

            bill_categories.color = random_color()

            if request.POST.get("submit") == "merchants_btn":       
                customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, customer_bill_category = bill_categories, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
            else:
                customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, customer_bill_category = bill_categories, delete_bill = False).order_by('-id')

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
                    'delete_bill':bill.delete_bill,
                    'color': random_color(),
                    'category_type': 'category',
                })

                bill_categories.bill_count += 1
                category_bills_count += 1

            if request.POST.get("submit") == "merchants_btn": 
                parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = bill_categories.id, is_pass = False, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
            else:
                parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = bill_categories.id, is_pass = False, delete_bill = False).order_by('-id')

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
                    'delete_bill':bill.delete_bill,
                    'color': random_color(),
                    'category_type': 'category',
                })

                bill_categories.bill_count += 1 
                category_bills_count += 1

            if request.POST.get("submit") == "merchants_btn":             
                petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = bill_categories.id, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
            else:
                petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = bill_categories.id, delete_bill = False).order_by('-id')

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
                    'delete_bill':bill.delete_bill,
                    'color': random_color(),
                    'category_type': 'category',
                })

                bill_categories.bill_count += 1
                category_bills_count += 1

        # data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

        bill_category_name = bill_category.objects.all()
        b_name = MerchantProfile.objects.all()

        # Bill By Merchant
        
        all_merchants = MerchantProfile.objects.all().order_by('m_business_name')
        all_merchants1 = MerchantProfile.objects.all().order_by('m_business_name').count()
        
        allocated_merchants = []

        for merchants in all_merchants:

            if request.POST.get("submit") == "merchants_btn":  
                customer_bill_count = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, business_name = merchants, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
            else:
                customer_bill_count = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, business_name = merchants, delete_bill = False).count()

            if customer_bill_count > 0:
                if merchants in allocated_merchants:
                    continue
                else:
                    allocated_merchants.append(merchants)
            # print(allocated_merchants,"-------------------------------------")
            
            if request.POST.get("submit") == "merchants_btn":  
                parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchants.id, is_pass = False, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
            else:
                parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchants.id, is_pass = False, delete_bill = False).count()
            if parking_bill_count > 0:
                if merchants in allocated_merchants:
                    continue
                else:
                    allocated_merchants.append(merchants)

            if request.POST.get("submit") == "merchants_btn":  
                petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchants.id, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
            else:
                petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchants.id, delete_bill = False).count()

            if petrol_bill_count > 0:
                if merchants in allocated_merchants:
                    continue
                else:
                    allocated_merchants.append(merchants)

            if request.POST.get("submit") == "merchants_btn":  
                customer_bill_count1 = CustomerBill.objects.filter(mobile_no = request.user, business_name__isnull=True, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
            else:
                customer_bill_count1 = CustomerBill.objects.filter(mobile_no = request.user, business_name__isnull=True, delete_bill = False).count()
            # print('customer_bill_count1223',customer_bill_count1)
            if customer_bill_count1 > 0:
                buisness_name = 'Others'
                if buisness_name in allocated_merchants:
                    continue
                else:
                    allocated_merchants.append(buisness_name)

     

        bill_count = ''
        merchant_color = ''
        merchant_bills = []
        merchant_bills_count = 0
        for merchant in allocated_merchants:
            if type(merchant) != str and merchant != None:

                merchant.bill_count = 0

                merchant.color = random_color()

                if request.POST.get("submit") == "merchants_btn":
                    customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, business_name = merchant, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
                else:
                    customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, business_name = merchant, delete_bill = False).order_by('-id')

                merchant.bills = []

                for bill in customer_bill_list:

                    try:
                        bill_file = bill.bill
                    except:
                        bill_file = ""

                    if bill.bill_tags:
                        bill_tags_temp = bill.bill_tags
                    else:
                        bill_tags_temp = "0"

                    merchant.bills.append({
                        'id': bill.id,
                        'amount': str(bill.bill_amount),
                        'bill_date': bill.bill_date,
                        'bill_file': bill_file,
                        'bill_category' : bill.customer_bill_category,
                        'business_name' : bill.business_name,
                        'bill_tags' : bill_tags_temp,
                        'remarks' : bill.remarks,
                        'custom_business_name': bill.custom_business_name,
                        'db_table': "CustomerBill",
                        'customer_added': bill.customer_added,
                        'bill_url': bill.bill_url,
                        'invoice_no':bill.invoice_no,
                        'delete_bill': bill.delete_bill,
                        'color': random_color(),
                        'category_type': 'merchant',
                    })

                    merchant.bill_count += 1
                    merchant_bills_count += 1

                if request.POST.get("submit") == "merchants_btn":
                    parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchant.id, is_pass = False, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
                else:
                    parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchant.id, is_pass = False, delete_bill = False).order_by('-id')
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
                        business_name = MerchantProfile.objects.get(id = bill.m_business_id)
                    except:
                        business_name = ""

                    try:
                        bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
                    except:
                        bill_category_temp = ""

                    merchant.bills.append({
                        'id': bill.id,
                        'amount': str(bill.amount),
                        'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                        'bill_file': bill_file,
                        'bill_category' : bill_category_temp,
                        'business_name' : business_name,
                        'bill_tags' : bill_tags_temp,
                        'remarks' : bill.remarks,
                        'custom_business_name': "",
                        'db_table': "SaveParkingLotBill",
                        'customer_added': False,
                        'bill_url': bill.bill_url,
                        'invoice_no':bill.invoice_no,
                        'delete_bill': bill.delete_bill,
                        'color': random_color(),
                        'category_type': 'merchant',
                    })

                    merchant.bill_count += 1
                    merchant_bills_count += 1
                        
                if request.POST.get("submit") == "merchants_btn":
                    petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchant.id, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
                else:
                    petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchant.id, delete_bill = False).order_by('-id')

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
                        business_name = MerchantProfile.objects.get(id = bill.m_business_id)
                    except:
                        business_name = ""

                    try:
                        bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
                    except:
                        bill_category_temp = ""

                    merchant.bills.append({
                        'id': bill.id,
                        'amount': str(bill.total_amount),
                        'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                        'bill_file': bill_file,
                        'bill_category' : bill_category_temp,
                        'business_name' : business_name,
                        'bill_tags' : bill_tags_temp,
                        'remarks' : bill.remarks,
                        'custom_business_name': "",
                        'db_table': "SavePetrolPumpBill",
                        'customer_added': False,
                        'bill_url': bill.bill_url,
                        'invoice_no':bill.invoice_no,
                        'delete_bill': bill.delete_bill,
                        'color': random_color(),
                        'category_type': 'merchant',
                    })

                    merchant.bill_count += 1
                    merchant_bills_count += 1
                # print('merchant.bills',merchant.bills)


            if type(merchant) == str:
                merchant_color = random_color()
                if request.POST.get("submit") == "merchants_btn":
                    customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user, business_name__isnull=True, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).order_by('-id')
                    customer_bill_list1 = CustomerBill.objects.filter(mobile_no = request.user, business_name__isnull=True, created_at__gte = sd_filter, created_at__lte = ed_filter, delete_bill = False).count()
                else:
                    customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user, business_name__isnull=True, delete_bill = False).order_by('-id')
                    customer_bill_list1 = CustomerBill.objects.filter(mobile_no = request.user, business_name__isnull=True, delete_bill = False).count()

                bill_count = customer_bill_list1

                for bill in customer_bill_list:

                    try:
                        bill_file = bill.bill
                    except:
                        bill_file = ""

                    if bill.bill_tags:
                        bill_tags_temp = bill.bill_tags
                    else:
                        bill_tags_temp = "0"

                    merchant_bills.append({
                        'id': bill.id,
                        'amount': str(bill.bill_amount),
                        'bill_date': bill.bill_date,
                        'bill_file': bill_file,
                        'bill_category' : bill.customer_bill_category,
                        'business_name' : bill.custom_business_name if bill.custom_business_name else '',
                        'bill_tags' : bill_tags_temp,
                        'remarks' : bill.remarks,
                        # 'custom_business_name': bill.custom_business_name,
                        'db_table': "CustomerBill",
                        'customer_added': bill.customer_added,
                        'bill_url': bill.bill_url,
                        'invoice_no':bill.invoice_no,
                        'delete_bill': bill.delete_bill,
                        'color': random_color(),
                        'category_type': 'merchant',
                    })
                    # merchant.bill_count += 1
                    merchant_bills_count += 1
        
        bill_tags_list = bill_tags.objects.all().order_by('bill_tags_name')

        allocated_tag_list = []

        for tag in bill_tags_list:
            startswith = str(tag.id) + ','
            endswith = ','+ str(tag.id)
            contains = ','+ str(tag.id) + ','
            exact = str(tag.id)
            if request.POST.get("submit") == "merchants_btn":
                customer_bill_count = CustomerBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(created_at__gte = sd_filter), Q(created_at__lte = ed_filter), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()
            else:
                customer_bill_count = CustomerBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()
            
            if customer_bill_count > 0:
                if tag in allocated_tag_list:
                    continue
                else:
                    allocated_tag_list.append(tag)

            if request.POST.get("submit") == "merchants_btn":
                parking_bill_count = SaveParkingLotBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(created_at__gte = sd_filter), Q(created_at__lte = ed_filter), Q(is_pass = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()
            else:
                parking_bill_count = SaveParkingLotBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(is_pass = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()

            if parking_bill_count > 0:
                if tag in allocated_tag_list:
                    continue
                else:
                    allocated_tag_list.append(tag)

            if request.POST.get("submit") == "merchants_btn":
                petrol_bill_count = SavePetrolPumpBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(created_at__gte = sd_filter), Q(created_at__lte = ed_filter), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()
            else:
                petrol_bill_count = SavePetrolPumpBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).count()

            if petrol_bill_count > 0:
                if tag in allocated_tag_list:
                    continue
                else:
                    allocated_tag_list.append(tag)

        tags_bills_count = 0


        for tag in allocated_tag_list:

            tag.bill_count = 0
            tag.color = random_color()

            startswith = str(tag.id) + ','
            endswith = ','+ str(tag.id)
            contains = ','+ str(tag.id) + ','
            exact = str(tag.id)

            tag.bills = []
            
            if request.POST.get("submit") == "merchants_btn":
                customer_bill_list = CustomerBill.objects.filter(Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact), Q(mobile_no=request.user.mobile_no), Q(delete_bill = False), Q(created_at__gte = sd_filter), Q(created_at__lte = ed_filter)).order_by('-id')
            else:
                customer_bill_list = CustomerBill.objects.filter(Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact), Q(delete_bill = False), Q(mobile_no=request.user.mobile_no)).order_by('-id')


            data = []

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

                tag.bills.append({
                    'id': bill.id,
                    'amount': str(bill.bill_amount),
                    'bill_date': bill.bill_date,
                    'bill_file': bill_file,
                    'bill_category' : bill.customer_bill_category,
                    'business_name' : business_names,
                    'bill_tags' : bill_tags_temp,
                    'remarks' : bill.remarks,
                    'custom_business_name': "",
                    'db_table': "CustomerBill",
                    'customer_added': bill.customer_added,
                    'bill_url': bill.bill_url,
                    'invoice_no':bill.invoice_no,
                    'delete_bill':bill.delete_bill,
                    'color': random_color(),
                    'category_type': 'tag',
                })

                tag.bill_count += 1 
                tags_bills_count += 1

            if request.POST.get("submit") == "merchants_btn":
                parking_bill_list = SaveParkingLotBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(created_at__gte = sd_filter), Q(created_at__lte = ed_filter), Q(is_pass = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).order_by('-id')
            else:
                parking_bill_list = SaveParkingLotBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(is_pass = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).order_by('-id')

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
                    business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
                except:
                    business_name = ""

                try:
                    bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
                except:
                    bill_category_temp = ""


                tag.bills.append({
                   'id': bill.id,
                    'amount': str(bill.amount),
                    'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                    'bill_file': bill_file,
                    'bill_category' : bill_category_temp,
                    'business_name' : business_name,
                    'bill_tags' : bill_tags_temp,
                    'remarks' : bill.remarks,
                    'custom_business_name': "",
                    'db_table': "SaveParkingLotBill",
                    'customer_added': False,
                    'bill_url': bill.bill_url,
                    'invoice_no':bill.invoice_no,
                    'delete_bill': bill.delete_bill,
                    'color': random_color(),
                    'category_type': 'tag',
                })

                tag.bill_count += 1
                tags_bills_count += 1

            if request.POST.get("submit") == "merchants_btn":
                petrol_bill_list = SavePetrolPumpBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(created_at__gte = sd_filter), Q(created_at__lte = ed_filter), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).order_by('-id')
            else:
                petrol_bill_list = SavePetrolPumpBill.objects.filter(Q(mobile_no = request.user.mobile_no), Q(delete_bill = False), Q(bill_tags__startswith=startswith) | Q(bill_tags__endswith=endswith) | Q(bill_tags__contains=contains) | Q(bill_tags__exact=exact)).order_by('-id')

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
                    business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
                except:
                    business_name = ""

                try:
                    bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
                except:
                    bill_category_temp = ""

                tag.bills.append({
                    'id': bill.id,
                    'amount': str(bill.total_amount),
                    'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                    'bill_file': bill_file,
                    'bill_category' : bill_category_temp,
                    'business_name' : business_name,
                    'bill_tags' : bill_tags_temp,
                    'remarks' : bill.remarks,
                    'custom_business_name': "",
                    'db_table': "SavePetrolPumpBill",
                    'customer_added': False,
                    'bill_url': bill.bill_url,
                    'invoice_no':bill.invoice_no,
                    'delete_bill': bill.delete_bill,
                    'color': random_color(),
                    'category_type': 'tag',
                })

                tag.bill_count += 1
                tags_bills_count += 1

        # for bill in allocated_bill_categories:
        #     category_bills_count += bill.bill_count

        # for bill in allocated_merchants:
        #     merchant_bills_count = len(bill.bills)

        
        # sorted_tag_list = sorted(allocated_tag_list, key=lambda item: item.get("tag_name"))
        if request.POST.get("submit") == "merchants_btn":
            pill_head = ''

            if bill_type == "category":
                pill_head = 'category'
            elif bill_type == "merchant":
                pill_head = 'merchant'
            elif bill_type == "tag":
                pill_head = 'tag'

            context = {
                # "bills" : bills,
                "allocated_bill_categories": allocated_bill_categories,
                "allocated_merchants": allocated_merchants,
                "allocated_tag": allocated_tag_list,
                'business_names': b_name,
                'bill_category': bill_category_name,
                "bill_tags": customer_bill_tags,
                "from_date1": from_date,
                "to_date1": to_date,
                "bill_count":bill_count,
                "merchant_color":merchant_color,
                "merchant_bills":merchant_bills,
                "custom_business_name":"Others",
                'MyBillsNavclass': 'active',
                'category_bill_count':category_bills_count,
                'merchant_bills_count':merchant_bills_count,
                'tags_bills_count': tags_bills_count,
                'pill_head':pill_head,
            }
        else:
            pill_head = ''
            if bill_type == "category":
                pill_head = 'category'
            elif bill_type == "merchant":
                pill_head = 'merchant'
            elif bill_type == "tag":
                pill_head = 'tag'

            context = {
                # "bills" : bills,
                "allocated_bill_categories": allocated_bill_categories,
                "allocated_merchants": allocated_merchants,
                "allocated_tag": allocated_tag_list,
                'business_names': b_name,
                'bill_category': bill_category_name,
                "bill_tags": customer_bill_tags,
                "customer_merchant_businesses": customer_merchant_businesses,
                "bill_count":bill_count,
                "merchant_color":merchant_color,
                "merchant_bills":merchant_bills,
                "custom_business_name":"Others",
                'MyBillsNavclass': 'active',
                'category_bill_count':category_bills_count,
                'merchant_bills_count':merchant_bills_count,
                'tags_bills_count': tags_bills_count,
                'pill_head':pill_head,
            }
    # print("***********************")
    # print(context['category_bill_count'],context['merchant_bills_count'],context["merchant_bills"])
    # return render(request, "customer/customer_bill/category-wise-bills.html", context)

    return render(request, "customer/customer_bill/customer-bill.html", context)


def GetMerchantBillTransfer(request):
    bil_id = request.POST['bill_id']
    db_table = request.POST['bill_id']

# @login_required(login_url="/customer-login/")
# @user_passes_test(is_customer, login_url="/customer-login/")
# def send_bill_customer(request):


#     return redirect('my_bills')


def random_color():

    hex_digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

    digit_array = []

    from random import randint

    for i in range(6):
        digit_array.append(hex_digits[randint(0,15)])
    joined_digits = ''.join(digit_array)

    color = '#' + joined_digits

    return color

# @login_required(login_url="/customer-login/")
# @user_passes_test(is_customer, login_url="/customer-login/")
# def bills_by_bill_category(request):

#     data = []

#     bill_categories = bill_category.objects.all()

#     allocated_bill_categories = []

#     for category in bill_categories:
#         customer_bill_count = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, customer_bill_category = category).count()
#         if customer_bill_count > 0:
#             if category in allocated_bill_categories:
#                 continue
#             else:
#                 allocated_bill_categories.append(category)
#                 # allocated_bill_categories.append(category)

#         parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no).count()
#         if parking_bill_count > 0:
#             if category in allocated_bill_categories:
#                 continue
#             elif category.id == 27:
#                 allocated_bill_categories.append(category)
#                 # allocated_bill_categories.append(category)

#         petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no).count()
#         if petrol_bill_count > 0:
#             if category in allocated_bill_categories:
#                 continue
#             elif category.id == 26:
#                 allocated_bill_categories.append(category)

#     customer_bill_tags = bill_tags.objects.all()

#     for bill_categories in allocated_bill_categories:
        
#         customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, customer_bill_category = bill_categories).order_by('-id')

#         bill_categories.bills = []

#         for bill in customer_bill_list:
#             try:
#                 bill_file = bill.bill
#             except:
#                 bill_file = ""

#             if bill.bill_tags:
#                 bill_tags_temp = bill.bill_tags
#             else:
#                 bill_tags_temp = "0"

#             bill_categories.bills.append({
#                 'id': bill.id,
#                 'amount': str(bill.bill_amount),
#                 'bill_date': bill.bill_date,
#                 'bill_file': bill_file,
#                 'bill_category' : bill.customer_bill_category,
#                 'business_name' : bill.business_name,
#                 'bill_tags' : bill_tags_temp,
#                 'remarks' : bill.remarks,
#                 'custom_business_name': bill.custom_business_name,
#                 'db_table': "CustomerBill",
#                 'customer_added': bill.customer_added
#             })

#         parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = bill_categories.id).order_by('-id')
#         for bill in parking_bill_list:
#             try:
#                 bill_file = bill.bill_file
#             except:
#                 bill_file = ""
            
#             if bill.bill_tags:
#                 bill_tags_temp = bill.bill_tags
#             else:
#                 bill_tags_temp = "0"

#             try:
#                 business_name = MerchantProfile.objects.get(id = bill.m_business_id)
#             except:
#                 business_name = ""

#             try:
#                 bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
#             except:
#                 bill_category_temp = ""

#             bill_categories.bills.append({
#                 'id': bill.id,
#                 'amount': str(bill.amount),
#                 'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
#                 'bill_file': bill_file,
#                 'bill_category' : bill_category_temp,
#                 'business_name' : business_name,
#                 'bill_tags' : bill_tags_temp,
#                 'remarks' : bill.remarks,
#                 'custom_business_name': "",
#                 'db_table': "SaveParkingLotBill",
#                 'customer_added': False
#             })
                

#         petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, bill_category_id = bill_categories.id).order_by('-id')
#         for bill in petrol_bill_list:
#             try:
#                 bill_file = bill.bill_file
#             except:
#                 bill_file = ""
            
#             if bill.bill_tags:
#                 bill_tags_temp = bill.bill_tags
#             else:
#                 bill_tags_temp = "0"

#             try:
#                 business_name = MerchantProfile.objects.get(id = bill.m_business_id)
#             except:
#                 business_name = ""

#             try:
#                 bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
#             except:
#                 bill_category_temp = ""

#             bill_categories.bills.append({
#                 'id': bill.id,
#                 'amount': str(bill.total_amount),
#                 'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
#                 'bill_file': bill_file,
#                 'bill_category' : bill_category_temp,
#                 'business_name' : business_name,
#                 'bill_tags' : bill_tags_temp,
#                 'remarks' : bill.remarks,
#                 'custom_business_name': "",
#                 'db_table': "SavePetrolPumpBill",
#                 'customer_added': False
#             })

#             # print(bill_categories.bills)

#     # print(allocated_bill_categories)

#     # data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

#     bill_category_name = bill_category.objects.all()
#     b_name = MerchantProfile.objects.all()

#     context = {
#         "allocated_bill_categories" : allocated_bill_categories,
#         'business_name': b_name,
#         'bill_category': bill_category_name,
#         "bill_tags": customer_bill_tags,
#         "BillByCategoryNavclass": "active"
#     }

#     return render(request, "customer/customer_bill/category-wise-bills.html", context)

@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def Edit_My_Bills(request): 

    if request.method == "POST":
        
        bill_id = request.POST['bill_id']
        updated_bill_tags = ''
        db_table = request.POST['edit_db_table']
        tags_list = []
        bill_tags_value = request.POST['edit_bill_tags_value']
        edit_amount_exe = request.POST['edit_amount']
        edit_category_exe =  request.POST['edit_category']

        category_type_var = request.POST['category_type']

        tags_list = bill_tags_value.split(",")
        

        # print("edit_amount_exe",edit_amount_exe)

        if bill_tags_value:
            updated_tags_list = []
            for tag in tags_list:
                if tag.isdigit():
                    updated_tags_list.append(tag)
                else:
                    result = bill_tags.objects.create(bill_tags_name=tag,user_id=GreenBillUser.objects.get(id=request.user.id),is_customer_bill_tag=1)
                    tag = result.id
                    updated_tags_list.append(tag)

            updated_bill_tags = ','.join(map(str, updated_tags_list))
        

        

        if db_table == "CustomerBill":
            # print('11',bill_id)
            try:
                CustomerBill.objects.filter(id=bill_id).update(business_name=request.POST.get('edit_business'), customer_bill_category = edit_category_exe, bill_amount = edit_amount_exe, bill_tags = updated_bill_tags, remarks = request.POST.get("edit_remarks"), custom_business_name = request.POST.get("edit_custom_business"))


                # if request.FILES['editfile']:
                #     CustomerBill.objects.filter(id=bill_id).update(business_name=request.POST.get('edit_business'), customer_bill_category=request.POST.get('edit_category'), bill_amount=request.POST.get('edit_amount'), bill_date=request.POST['edit_date'], bill_tags = updated_bill_tags, remarks = request.POST.get("edit_remarks"), custom_business_name = request.POST.get("edit_custom_business"), invoice_no = request.POST.get("edit_invoice_no"))
                #     bill_data = CustomerBill.objects.get(id=bill_id)
                #     bill_data.bill = request.FILES['editfile']
                #     bill_data.save()
                #     print('bill_data',bill_data)
                # else:
                #     CustomerBill.objects.filter(id=bill_id).update(business_name=request.POST.get('edit_business'), customer_bill_category=request.POST.get('edit_category'), bill_amount=request.POST.get('edit_amount'), bill_date=request.POST['edit_date'], bill_tags = updated_bill_tags, remarks = request.POST.get("edit_remarks"), custom_business_name = request.POST.get("edit_custom_business"), invoice_no = request.POST.get("edit_invoice_no"))
                #     print('tryelse')
            except:

                CustomerBill.objects.filter(id=bill_id).update(business_name=request.POST.get('edit_business'), customer_bill_category=request.POST.get('edit_category'), bill_amount=request.POST.get('edit_amount'), bill_tags = updated_bill_tags, remarks = request.POST.get("edit_remarks"), custom_business_name = request.POST.get("edit_custom_business"))
                # print('tryexcept')

        elif db_table == "SaveParkingLotBill":
            # print('parking')
            SaveParkingLotBill.objects.filter(id=bill_id).update(bill_category_id=request.POST.get('edit_category'), bill_tags = updated_bill_tags, remarks = request.POST.get("edit_remarks"))

        elif db_table == "SavePetrolPumpBill":
           # print("petrol")
           SavePetrolPumpBill.objects.filter(id=bill_id).update(bill_category_id=request.POST.get('edit_category'), bill_tags = updated_bill_tags, remarks = request.POST.get("edit_remarks"))

        sweetify.success(request, title="Success", icon='success', text='Bill Updated Successfully', timer=1500)

    return redirect(my_bills, bill_type=category_type_var)


@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def bills_by_merchant(request):

    data = []

    all_merchants = MerchantProfile.objects.all()

    allocated_merchants = []

    for merchants in all_merchants:
        customer_bill_count = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, business_name = merchants).count()
        if customer_bill_count > 0:
            if merchants in allocated_merchants:
                continue
            else:
                allocated_merchants.append(merchants)

        parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchants.id).count()
        if parking_bill_count > 0:
            if merchants in allocated_merchants:
                continue
            else:
                allocated_merchants.append(merchants)

        petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchants.id).count()
        if petrol_bill_count > 0:
            if merchants in allocated_merchants:
                continue
            else:
                allocated_merchants.append(merchants)

    for merchant in allocated_merchants:
        
        customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user.mobile_no, business_name = merchant).order_by('-id')

        merchant.bills = []

        for bill in customer_bill_list:
            try:
                bill_file = bill.bill
            except:
                bill_file = ""

            if bill.bill_tags:
                bill_tags_temp = bill.bill_tags
            else:
                bill_tags_temp = "0"

            merchant.bills.append({
                'id': bill.id,
                'amount': str(bill.bill_amount),
                'bill_date': bill.bill_date,
                'bill_file': bill_file,
                'bill_category' : bill.customer_bill_category,
                'business_name' : bill.business_name,
                'bill_tags' : bill_tags_temp,
                'remarks' : bill.remarks,
                'custom_business_name': bill.custom_business_name,
                'db_table': "CustomerBill",
                'customer_added': bill.customer_added
            })

        parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchant.id).order_by('-id')
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
                business_name = MerchantProfile.objects.get(id = bill.m_business_id)
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
            except:
                bill_category_temp = ""

            merchant.bills.append({
                'id': bill.id,
                'amount': str(bill.amount),
                'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                'bill_file': bill_file,
                'bill_category' : bill_category_temp,
                'business_name' : business_name,
                'bill_tags' : bill_tags_temp,
                'remarks' : bill.remarks,
                'custom_business_name': "",
                'db_table': "SaveParkingLotBill",
                'customer_added': False
            })
                

        petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = request.user.mobile_no, m_business_id = merchant.id).order_by('-id')
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
                business_name = MerchantProfile.objects.get(id = bill.m_business_id)
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
            except:
                bill_category_temp = ""

            merchant.bills.append({
                'id': bill.id,
                'amount': str(bill.total_amount),
                'bill_date': datetime.strptime(bill.date, "%d-%m-%Y").date(),
                'bill_file': bill_file,
                'bill_category' : bill_category_temp,
                'business_name' : business_name,
                'bill_tags' : bill_tags_temp,
                'remarks' : bill.remarks,
                'custom_business_name': "",
                'db_table': "SavePetrolPumpBill",
                'customer_added': False
            })

    bill_category_name = bill_category.objects.all()
    
    b_name = MerchantProfile.objects.all()

    customer_bill_tags = bill_tags.objects.all()

    context = {
        "allocated_merchants" : allocated_merchants,
        'business_name': b_name,
        'bill_category': bill_category_name,
        "bill_tags": customer_bill_tags,
        "BillByMerchantNavclass": "active"
    }

    return render(request, "customer/customer_bill/Bill-merchant-wise-bills.html", context)


@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def Edit_bills_by_merchant(request): 

    if request.method == "POST":
        
        bill_id = request.POST['bill_id']

        db_table = request.POST['edit_db_table']

        if db_table == "CustomerBill":
            try:
                if request.FILES['editfile']:
                    CustomerBill.objects.filter(id=bill_id).update(business_name=request.POST['edit_business'], customer_bill_category=request.POST['edit_category'], bill_amount=request.POST['edit_amount'], bill_date=request.POST['edit_date'], bill_tags = request.POST['edit_bill_tags_value'], remarks = request.POST["edit_remarks"], custom_business_name = request.POST["edit_custom_business"])
                    bill_data = CustomerBill.objects.get(id=bill_id)
                    bill_data.bill = request.FILES['editfile']
                    bill_data.save()
                else:
                    CustomerBill.objects.filter(id=bill_id).update(business_name=request.POST['edit_business'], customer_bill_category=request.POST['edit_category'], bill_amount=request.POST['edit_amount'], bill_date=request.POST['edit_date'], bill_tags = request.POST['edit_bill_tags_value'], remarks = request.POST["edit_remarks"], custom_business_name = request.POST["edit_custom_business"])

            except:
                CustomerBill.objects.filter(id=bill_id).update(business_name=request.POST['edit_business'], customer_bill_category=request.POST['edit_category'], bill_amount=request.POST['edit_amount'], bill_date=request.POST['edit_date'], bill_tags = request.POST['edit_bill_tags_value'], remarks = request.POST["edit_remarks"], custom_business_name = request.POST["edit_custom_business"])

        elif db_table == "SaveParkingLotBill":
            SaveParkingLotBill.objects.filter(id=bill_id).update(bill_category_id=request.POST['edit_category'], bill_tags = request.POST['edit_bill_tags_value'], remarks = request.POST["edit_remarks"])

        elif db_table == "SavePetrolPumpBill":
            SavePetrolPumpBill.objects.filter(id=bill_id).update(bill_category_id=request.POST['edit_category'], bill_tags = request.POST['edit_bill_tags_value'], remarks = request.POST["edit_remarks"])

        sweetify.success(request, title="Success", icon='success', text='Bill Updated Successfully', timer=1500)

    return redirect(bills_by_merchant)


@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def Delete_My_Bills(request, id):
    category_type_var = request.POST['category_type']

    if request.POST["db_table"] == "CustomerBill":
        
        status = CustomerBill.objects.filter(id=id).update(delete_bill = True)

    elif request.POST["db_table"] == "SaveParkingLotBill":
        status = SaveParkingLotBill.objects.filter(id=id).update(delete_bill = True)

    elif request.POST["db_table"] == "SavePetrolPumpBill":
        status = SavePetrolPumpBill.objects.filter(id=id).update(delete_bill = True)
    


    if status:
        return JsonResponse({'status':'success', 'category':category_type_var})
    else:
        return JsonResponse({'status':'error', 'category': category_type_var})


@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def Delete_merchant_bills(request, id):
    category_type_var = request.POST['category_type']
    
    if request.POST["db_table"] == "CustomerBill":
        
        status = CustomerBill.objects.filter(id=id).update(delete_bill = True)
        

    elif request.POST["db_table"] == "SaveParkingLotBill":
        status = SaveParkingLotBill.objects.filter(id=id).update(delete_bill = True)

    elif request.POST["db_table"] == "SavePetrolPumpBill":
        status = SavePetrolPumpBill.objects.filter(id=id).update(delete_bill = True)
    
    if status:
        return JsonResponse({'status':'success', 'category':category_type_var})
    else:
        return JsonResponse({'status':'error', 'category':category_type_var})


def new_bill_design(request):
    return render(request, "customer/customer_bill/new-bill-design.html")


def self_added_bill_view(request, id):

    try:

        bill_details = CustomerBill.objects.get(bill_url=id)

        ads = ads_for_green_bills.objects.filter(active_ads = True)

        try:
            ads_redirect_url = ads[0].redirect_url
            ads_image = ads[0].ads_image
        except:
            ads_redirect_url = ""
            ads_image = ""

        context = {'bill_details' : bill_details, 'ads_redirect_url': ads_redirect_url, 'ads_image':ads_image,}

        return render(request, "customer/customer_bill/self-added-bill.html", context)

    except:
        return render(request, 'page-404.html')


def get_merchant_business_by_category_id(request, id):
    bill_category_object = bill_category.objects.get(id = id)
    merchant_business = MerchantProfile.objects.filter(m_business_category__business_category_name__contains = bill_category_object.bill_category_name)

    data = []
    if merchant_business:
        for business in merchant_business:

            data.append({
                "id": business.id,
                "business_name": business.m_business_name + " (" + business.m_area + ")"
            })

    return JsonResponse(data, safe = False)


def sample_dummy_bill(request):
    
    return render(request, "customer/customer_bill/sample-bill-dummy.html")