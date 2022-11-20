from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse,Http404
import os
from customer_info.models import Customer_Info_Model
from django.contrib import messages
import csv
import io
from django.contrib.auth.decorators import login_required, user_passes_test
import sweetify
from users.models import Merchant_users, GreenBillUser, MerchantProfile

from merchant_software_apis.models import CustomerBill
from petrol_pump_apis.models import SavePetrolPumpBill
from parking_lot_apis.models import SaveParkingLotBill

from datetime import datetime

from app.views import is_merchant_or_merchant_staff, getActiveTransactionalSubscriptionPlan, getActivePromotionalSubscriptionPlan

from .forms import bulkMailSmsMerchantCustomerForm
from .models import bulkMailSmsMerchantCustomerModel, smsHeaderModel, templateContentModel
from merchant_notice.models import *
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail
from owner_notice_board.sendsms import *
# Create your views here.
from datetime import datetime
import time
import datetime


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def BulkEmailCustomer(request):
    gg = GreenBillUser.objects.filter(mobile_no=7709977798).update(is_active=True)
    print('SDDD',gg)
    mer_user_id = Merchant_users.objects.get(user_id=request.user)

    merchant_object = mer_user_id.merchant_user_id
    
    merchant_business_object = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    merchant_business_id = merchant_business_object.id

    merchant_added_customer_list = Customer_Info_Model.objects.filter(mer_id = merchant_object)

    subscription = False
    if request.method == "POST":
        if subscription == True:

            customer_state_value = request.POST.get('customer_state_value')
            customer_state_value_new = customer_state_value.split(",")

            customer_city_value = request.POST.get('customer_city_value')
            customer_city_value_new = customer_city_value.split(",")

            customer_area_value = request.POST.get('customer_area_value')
            customer_area_value_new = customer_area_value.split(",")

            title = request.POST.get('title')
            message = request.POST.get('message')
            # mobile_no = request.POST.get('mobile_number')
            # email = request.POST.get('email_id')
            smsheader = request.POST.get('smsheader')
            template = request.POST.get('template')
            sent_notice = request.POST.getlist('sentnotice')
            custom_number = request.POST.get('custom-no')
            customer = request.POST.get('checksc')
            file_upload = request.FILES.get('myfile')
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
                print('custom_number_list',custom_number_list)
            print('sent_notice',sent_notice)
            # print("HELLLOOOOOO")
            # print('mobile', mobile_no)
            # print('email',email)
            print('smsheader',smsheader)
            print('template',template)
           
            # individual = merchant_added_customer_list.cust_mobile_num
            # print(individual)

            
            individual_user = request.POST.getlist('individual')
            print('individual user', individual_user)
            print('title',title)
         
            print('message',message)
            receiver_name = ''
            # for user in individual_user:
            #     user_object = Customer_Info_Model.objects.get(id=user)
            #     receiver_name.append(user_object.cust_first_name + '' + user_object.cust_last_lname)
            if custom_number: 
                receiver_name = custom_number
            if customer:
                receiver_name = 'Customer'
            if file_upload:
                receiver_name = joined_lines
            print('receiver_name')
            print(receiver_name)
            print(individual_user)  
            if customer  and custom_number_list and csv_fields:
                
                sweetify.error(request,text="Please select either from group or individual list !!!", timer=5500)
            elif custom_number_list or customer or csv_fields:
                print('OWNER')
                
            
             
                for notice in sent_notice:
                        # if notice == "sms":
                        #     notice_id = bulkMailSmsMerchantCustomerModel.objects.create(
                        #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_sent_sms=True)

                        # elif notice == "sent_mail":
                        #     notice_id = bulkMailSmsMerchantCustomerModel.objects.create(
                        #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_sent_mail=True)

                        # else:
                        #     notice_id = bulkMailSmsMerchantCustomerModel.objects.create(
                        #         owner_id=request.user, title=title, notice_file=notice_file, message=message, o_notification=True)

                    if notice == "sms":
                            
                            notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(customer_state=customer_state_value_new, customer_city=customer_city_value_new, customer_area=customer_area_value_new, owner_id=request.user, title=title, message=message,receiver_name=receiver_name, defaults= { 'title':title, 'message':message, 'o_sent_sms':True })

                    elif notice == "sent_mail":
                            
                            notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(customer_state=customer_state_value_new, customer_city=customer_city_value_new, customer_area=customer_area_value_new, owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template, receiver_name=receiver_name, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template, 'o_sent_mail':True })

                    else:
                        notice_id = Merchant_Notice_Model.objects.update_or_create(owner_id=request.user, notice_title=title, message=message, defaults= { 'notice_title':title,  'message':message, 'o_notification':True })

                        print(notice_id[0].id)

                        notice_object = Merchant_Notice_Model.objects.get(id= notice_id[0].id)
                        print('notice_object::',notice_object)
              
                if custom_number:
                    for notice in sent_notice:
                        for number in custom_number_list:
                            print('number',number)
                            try:
                                email_id = number
                                print(email_id)
                                email_from = settings.EMAIL_HOST_USER
                                print('email from',email_from)
                                recipient_list = [email_id ]
                                # recipient_list = ['shreyash.t@zappkode.com']
                                print('email to',recipient_list)
                                message = message
                               
                                plain_message = strip_tags(message)
                                print('sent message:',plain_message)
                                send_mail( title, plain_message, email_from, recipient_list)
                            except:
                                        
                                owner_notice_sent_save = ""


                if csv_fields:
                    for notice in sent_notice:
                        for number in csv_fields:
                            print('number',number)
                            try:
                                email_id = number
                                print(email_id)
                                email_from = settings.EMAIL_HOST_USER
                                print('email from',email_from)
                                recipient_list = [email_id ]
                                # recipient_list = ['shreyash.t@zappkode.com']
                                print('email to',recipient_list)
                                message = message
                               
                                plain_message = strip_tags(message)
                                print('sent message:',plain_message)
                                send_mail( title, plain_message, email_from, recipient_list)
                            except:
                                        
                                owner_notice_sent_save = ""

                if customer:
                        users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new)
                        for u in users:
                            
                            for notice in sent_notice:
                                
                                
                                if notice == "sent_mail":
                                    try:
                                        email_id = u.c_email
                                        print(email_id)
                                        email_from = settings.EMAIL_HOST_USER
                                        # print('email from',email_from)
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
                                # else:
                                #     # try:
                                #         individual_user_object = GreenBillUser.objects.get(mobile_no=individual_user)
                                #         print('owner_notice_sent_saveowner_notice_sent_save',individual_user)
                                #         owner_notice_sent_save = OwnerSentNotice.objects.create(
                                #         notice_id=notice_object, user_id=individual_user_object, notification=True)

                                #         print('owner_notice_sent_save',owner_notice_sent_save)
                                #     # except:
                                #     #     owner_notice_sent_save = ""


                
                
                sweetify.success(request, title="Success", icon='success',
                                    text='Email Send successfully!!', timer=5500)
                    # return redirect("/owner_notice_board/")
            else:
                    sweetify.error(request, title="Error", icon='error',
                                    text="Something Went Wrong!!!", timer=5500)               
        else:
            sweetify.error(request, title="Sorry", icon='error',
                                    text="You don't have active email subscription plan!!!", timer=5500)
    
    smsmail = bulkMailSmsMerchantCustomerModel.objects.filter(owner_id=merchant_object,o_sent_mail=True).order_by('-id')
    states = GreenBillUser.objects.values('c_state').distinct()
    context = {
        'cust_data': states,
        'data': smsmail,
        'customer_list': merchant_added_customer_list,
        'PromotionsNavclass': 'active',
        'BulkEmailNavclass':'active',
        'ShowPromotionsNavclass':'show',
        'bulkMailSmsMerchantCustomerForm':bulkMailSmsMerchantCustomerForm,
    }

    return render(request, 'merchant/merchant_notice_board/merchant-promotion-email.html' , context)


    
def get_template_by_header(request):
    smsheader = request.POST['smsheader']
    Template = templateContentModel.objects.filter(request_user = request.user, status='Approved')
    list1 = []
    filtered_city_list = []
    for obj in Template:
        if obj.sms_header:
            if smsheader in obj.sms_header:
                list1.append({
                    "template_content": obj.template_content
                })
    for x in list1:
        if x['template_content'] not in filtered_city_list:
            if x['template_content'] != '':
                filtered_city_list.append(x['template_content'])
    return JsonResponse({"data":filtered_city_list})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def get_customer_count_by_state_city_area(request):
    customer_state_value = request.POST['customer_state_value']
    customer_city_value = request.POST['customer_city_value']
    customer_area_value = request.POST['customer_area_value']

    list1 = []

    total_count = 0

    if customer_state_value and customer_city_value and customer_area_value:
        customer_state_value_new = customer_state_value.split(",")
        customer_city_value_new = customer_city_value.split(",")
        customer_area_value_new = customer_area_value.split(",")
        
        for cust_area in customer_area_value_new:
            total_count = total_count + (GreenBillUser.objects.filter(c_area = cust_area, is_customer=True).count())

    elif customer_state_value and customer_city_value:
        customer_state_value_new = customer_state_value.split(",")
        customer_city_value_new = customer_city_value.split(",")

        for cust_state in customer_state_value_new:
            for cust_city in customer_city_value_new:
                total_count = total_count + (GreenBillUser.objects.filter(c_state = cust_state, c_city = cust_city,is_customer=True).count())

    elif customer_state_value:
        customer_state_value_new = customer_state_value.split(",")

        for cust_state in customer_state_value_new:
            total_count = total_count + (GreenBillUser.objects.filter(c_state = cust_state,is_customer=True).count())

    list1.append(total_count)

    return JsonResponse({"data":list1})


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def BulkSmsCustomer(request):
    
    mer_user_id = Merchant_users.objects.get(user_id=request.user)
    merchant_object = mer_user_id.merchant_user_id
    
    merchant_business_object = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    merchant_business_id = merchant_business_object.id

    merchant_added_customer_list = GreenBillUser.objects.filter(is_customer=True)

    merchant_added_customer_count = GreenBillUser.objects.filter(is_customer=True).count()

    try:
        smsid = bulkMailSmsMerchantCustomerModel.objects.filter().last().id
    except:
        smsid = ""
    # print('SMSMS',smsid)
    customer_addresswise_count = ""
    if request.method == "POST":
        
        customer_state_value = request.POST.get('customer_state_value')
        customer_state_value_new = customer_state_value.split(",")

        customer_city_value = request.POST['customer_city_value']
        if customer_city_value:
            customer_city_value_new = customer_city_value.split(",")
        else:
            customer_city_value_new = ''

        customer_area_value = request.POST['customer_area_value']
        if customer_area_value:
            customer_area_value_new = customer_area_value.split(",")
        else:
            customer_area_value_new = ''

        # customer_city_value = request.POST.get('customer_city_value')
        # customer_city_value_new = customer_city_value.split(",")

        # customer_area_value = request.POST.get('customer_area_value')
        # customer_area_value_new = customer_area_value.split(",")

        title = request.POST.get('title')
        message = request.POST.get('message')
        campaign_name = request.POST.get('campaign_name')
        # smsheader = request.POST.get('smsheader')
        template = request.POST.get('template_id')
        unique_template_id = templateContentModel.objects.get(request_user = request.user, status='Approved', template_content=template).template_id
        sent_notice = request.POST.getlist('sentnotice')
        transactional = request.POST.get('transactional')
        if transactional == "transactional":
            smsheader = request.POST.get('smsheader')
        else:
            smsheader = request.POST.get('smsheader1')

        custom_number = request.POST.get('custom-no')
        customer = request.POST.get('checksc')
        file_upload = request.FILES.get('myfile')
        joined_lines = ''
        csv_fields = ''
        receipent_count = ''
        if file_upload:
            if not file_upload.name.endswith('.csv'):
                sweetify.error(request, title="Error", icon='error',
                                                text="Choose valid csv file!!!", timer=5500)
            else:
                file_data = file_upload.read().decode("utf-8")
                file_lines = file_data.split("\n")
                csv_fields = [line.replace('\r','') for line in file_lines if line]

                converted_list = [str(no) for no in csv_fields]
                receipent_count = len(converted_list)
                joined_lines = ",".join(converted_list)

       
        custom_number_list = ''
        if custom_number:
            custom_number_list = custom_number.split(',')
        
        receipent_count = request.POST.get('receipent_count')
        receiver_name = ''
        if customer: 
            receiver_name = 'Customer'
        if custom_number: 
            # receiver_name = custom_number
            receiver_name = "Custom"

        if file_upload:
            receiver_name = joined_lines

        
        # template_id = ''
        # if template == '1':
        #     template_id = '1007162209490097673'
        # if template == '2':
        #     template_id = '1007162107620813728'
        # if template == '3':
        #     template_id = '1007162106850723917'
        # if template == '4':
        #     template_id = '1007162106809978850'
        # if template == '5':
        #     template_id = '1007162106793840599'
        # if template == '6':
        #     template_id = '1007162098384997217'
        # if template == '7':
        #     template_id = '1007162098381110505'
        # if template == '8':
        #     template_id = '1007162098372946720'
        # if template == '9':
        #     template_id = '1007162098368573560'
        # if template == '10':
        #     template_id = '1007162098358759996'
        # if template == '11':
        #     template_id = '1007162098351638761'
        # if template == '12':
        #     template_id = '1007162098340655435'
        # if template == '13':
        #     template_id = '1007162098336084141'
        # if template == '14':
        #     template_id = '1007162098331673473'
        # if template == '15':
        #     template_id = '1007162098326474514'
        # if template == '16':
        #     template_id = '1007162098321473343'
        # if template == '17':
        #     template_id = '1007162098316946419'
        # if template == '18':
        #     template_id = '1007162098307281560'
        # if template == '19':
        #     template_id = '1007161821757152482'
        # if template == '20':
        #     template_id = '1007161814187973948'
        # if template == '21':
        #     template_id = '1007161814167155974'
        # if template == '22':
        #     template_id = '1007161814117326730'
       
        if customer  and custom_number_list and csv_fields:
            sweetify.error(request,text="Please select either from group or individual list !!!", timer=5500)
        elif custom_number_list or customer or csv_fields:
            for notice in sent_notice:
                   
                if notice == "sms":
                        if customer_city_value_new != '' and customer_area_value_new != '':
                            notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(customer_state=customer_state_value_new, customer_city=customer_city_value_new, customer_area=customer_area_value_new, owner_id=request.user,campaign_name=campaign_name, title=title, message=message,smsheader=smsheader,template=template, receiver_name=receiver_name, transactional=transactional, defaults= { 'title':title, 'message':message, 'smsheader':smsheader, 'template':template, 'receiver_name':receiver_name, 'o_sent_sms':True })
                        elif customer_city_value_new != '' and customer_area_value_new == '':
                            notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(customer_state=customer_state_value_new, customer_city=customer_city_value_new, owner_id=request.user, title=title, message=message,smsheader=smsheader, campaign_name=campaign_name,template=template, receiver_name=receiver_name, transactional=transactional, defaults= { 'title':title, 'message':message, 'smsheader':smsheader, 'template':template, 'receiver_name':receiver_name, 'o_sent_sms':True })
                        elif customer_city_value_new == '' and customer_area_value_new == '':
                            notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(customer_state=customer_state_value_new, owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template, receiver_name=receiver_name, campaign_name=campaign_name, transactional=transactional, defaults= { 'title':title, 'message':message, 'smsheader':smsheader, 'template':template, 'receiver_name':receiver_name, 'o_sent_sms':True })
                
                elif notice == "sent_mail":
                        if customer_city_value_new != '' and customer_area_value_new != '':
                            notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(customer_state=customer_state_value_new, customer_city=customer_city_value_new, customer_area=customer_area_value_new, owner_id=request.user, title=title, campaign_name=campaign_name, message=message,smsheader=smsheader,template=template, receiver_name=receiver_name, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template, 'receiver_name':receiver_name, 'o_sent_mail':True })
                        elif customer_city_value_new != '' and customer_area_value_new == '':
                            notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(customer_state=customer_state_value_new, customer_city=customer_city_value_new, owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template, campaign_name=campaign_name, receiver_name=receiver_name, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template, 'receiver_name':receiver_name, 'o_sent_mail':True })
                        elif customer_city_value_new == '' and customer_area_value_new == '':
                            notice_id = bulkMailSmsMerchantCustomerModel.objects.update_or_create(customer_state=customer_state_value_new, owner_id=request.user, title=title, message=message,smsheader=smsheader,template=template, campaign_name=campaign_name, receiver_name=receiver_name, defaults= { 'title':title,  'message':message, 'smsheader':smsheader, 'template':template, 'receiver_name':receiver_name, 'o_sent_mail':True })

                else:
                    notice_id = Merchant_Notice_Model.objects.update_or_create(owner_id=request.user, notice_title=title, message=message, defaults= { 'notice_title':title,  'message':message, 'o_notification':True })

                    notice_object = Merchant_Notice_Model.objects.get(id= notice_id[0].id)
          
            if transactional == 'transactional':
                merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']
                business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)

                subscription_object = getActiveTransactionalSubscriptionPlan(request, business_object.id)

                if subscription_object:
                    if subscription_object.total_sms_avilable:

                        if int(float(subscription_object.total_sms_avilable)):

                            if customer:
                                if customer_city_value_new != '' and customer_area_value_new != '':
                                    users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new)
                                    if users:
                                        customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new).count()
                                        customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                        customer_addresswise_count = customer_count

                                        for u in users:
                                            for notice in sent_notice:
                                                if notice == "sms":
                                                        contact = u.mobile_no
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
                                                                                "DLT_CT_ID":unique_template_id, # Template Id
                                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                            }
                                                                        ]
                                                                    }

                                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                            response = requests.post(url, json = data_temp)

                                                        
                                                        sms_response = sendSMS(str(contact), message)
                                                        # print(sms_response)
                                                        # try:
                                                        #     print('success')
                                                        #         # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                                        #         # message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
                                                        # except:
                                                        #         owner_notice_sent_save = ""
                                                        # sms_response = sendSMS(str(contact), message)
                                                        # print(sms_response)
                                        if response.status_code == 200:
                                            total_sms_avilable_new = 0
                                            if customer:
                                                total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                                subscription_object.total_sms_avilable = total_sms_avilable_new
                                            else:
                                                total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                                subscription_object.total_sms_avilable = total_sms_avilable_new

                                            subscription_object.save()

                                            bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                            
                                            sweetify.success(request, title="Success", icon='success',
                                                                    text='SMS Send successfully!!', timer=5500)
                                        else:
                                            bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                            sweetify.error(request, title="Error", icon='error',
                                                            text="Something Went Wrong!!!", timer=5500)

                                    else:
                                        sweetify.error(request, title="Error", icon='error',text="Customers in this area not found.", timer=5500)
                                
                                elif customer_city_value_new != '' and customer_area_value_new == '':
                                    users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new)
                                    if users:
                                        customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new).count()
                                        customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                        customer_addresswise_count = customer_count

                                        for u in users:
                                            for notice in sent_notice:
                                                if notice == "sms":
                                                        contact = u.mobile_no
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
                                                                                "DLT_CT_ID":unique_template_id, # Template Id
                                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                            }
                                                                        ]
                                                                    }

                                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                            response = requests.post(url, json = data_temp)

                                                        
                                                        sms_response = sendSMS(str(contact), message)
                                                        # print(sms_response)
                                                        # try:
                                                        #     print('success')
                                                        #         # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                                        #         # message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
                                                        # except:
                                                        #         owner_notice_sent_save = ""
                                                        # sms_response = sendSMS(str(contact), message)
                                                        # print(sms_response)
                                        if response.status_code == 200:
                                            total_sms_avilable_new = 0
                                            if customer:
                                                total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                                subscription_object.total_sms_avilable = total_sms_avilable_new
                                            else:
                                                total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                                subscription_object.total_sms_avilable = total_sms_avilable_new

                                            subscription_object.save()

                                            bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                            
                                            sweetify.success(request, title="Success", icon='success',
                                                                    text='SMS Send successfully!!', timer=5500)
                                        else:
                                            bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                            sweetify.error(request, title="Error", icon='error',
                                                            text="Something Went Wrong!!!", timer=5500)

                                    else:
                                        sweetify.error(request, title="Error", icon='error',text="Customers in this area not found.", timer=5500)
                                
                                elif customer_city_value_new == '' and customer_area_value_new == '':
                                    users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new)
                                    if users:
                                        customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new).count()
                                        customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                        customer_addresswise_count = customer_count

                                        for u in users:
                                            for notice in sent_notice:
                                                if notice == "sms":
                                                        contact = u.mobile_no
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
                                                                                "DLT_CT_ID":unique_template_id, # Template Id
                                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                            }
                                                                        ]
                                                                    }

                                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                            response = requests.post(url, json = data_temp)

                                                        
                                                        sms_response = sendSMS(str(contact), message)
                                                        # print(sms_response)
                                                        # try:
                                                        #     print('success')
                                                        #         # owner_notice_sent_save = bulkMailSmsSent.objects.update_or_create(
                                                        #         # message_id=notice_object, user_id=user_object.m_user, defaults = {'sent_sms':True})
                                                        # except:
                                                        #         owner_notice_sent_save = ""
                                                        # sms_response = sendSMS(str(contact), message)
                                                        # print(sms_response)
                                        if response.status_code == 200:
                                            total_sms_avilable_new = 0
                                            if customer:
                                                total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                                subscription_object.total_sms_avilable = total_sms_avilable_new
                                            else:
                                                total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                                subscription_object.total_sms_avilable = total_sms_avilable_new

                                            subscription_object.save()

                                            bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                            
                                            sweetify.success(request, title="Success", icon='success',
                                                                    text='SMS Send successfully!!', timer=5500)
                                        else:
                                            bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                            sweetify.error(request, title="Error", icon='error',
                                                            text="Something Went Wrong!!!", timer=5500)

                                    else:
                                        sweetify.error(request, title="Error", icon='error',text="Customers in this area not found.", timer=5500)
                            if custom_number_list:
                                for notice in sent_notice:
                                    for number in custom_number_list:
                                       
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
                                                                    "DLT_CT_ID":unique_template_id, # Template Id
                                                                    "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                }
                                                            ]
                                                        }

                                                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                response = requests.post(url, json = data_temp)
                                               
                                            
                                            sms_response = sendSMS(str(contact), message)                                                                                   

                            
                                if response.status_code == 200:
                                    total_sms_avilable_new = 0
                                    if customer:
                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                        subscription_object.total_sms_avilable = total_sms_avilable_new
                                    else:
                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                        subscription_object.total_sms_avilable = total_sms_avilable_new

                                    subscription_object.save()

                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
                                    sweetify.success(request, title="Success", icon='success',
                                                            text='SMS Send successfully!!', timer=5500)
                                else:
                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                    sweetify.error(request, title="Error", icon='error',
                                                    text="Something Went Wrong!!!", timer=5500)

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
                                                                    "DLT_CT_ID":unique_template_id, # Template Id
                                                                    "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                }
                                                            ]
                                                        }

                                                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                response = requests.post(url, json = data_temp)

                                                
                                            sms_response = sendSMS(str(contact), message)
                            
                                if response.status_code == 200:
                                    total_sms_avilable_new = 0
                                    if customer:
                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                        subscription_object.total_sms_avilable = total_sms_avilable_new
                                    else:
                                        total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                        subscription_object.total_sms_avilable = total_sms_avilable_new
            
                                    subscription_object.save()

                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                    
                                    sweetify.success(request, title="Success", icon='success',
                                                            text='SMS Send successfully!!', timer=5500)
                                else:
                                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                    sweetify.error(request, title="Error", icon='error',
                                                    text="Something Went Wrong!!!", timer=5500)

                        else:
                            bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                            sweetify.success(request, title="Oops...", icon='error', text='Insufficient Balance. Please purchase Transactional plan and try again !!!', timer=2000)
                    else:
                        bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                        sweetify.success(request, title="Oops...", icon='error', text='Insufficient Balance. Please purchase Transactional plan and try again !!!', timer=2000)
                else:
                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                    sweetify.success(request, title="Oops...", icon='error', text="You don't have active Transactional SMS plan. Please purchase and try again.", timer=2000)
           
            if transactional == 'promotional':
                merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']
                business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)

                subscription_object = getActivePromotionalSubscriptionPlan(request, business_object.id)

                if subscription_object and subscription_object.total_sms_avilable:
                    if int(float(subscription_object.total_sms_avilable)):
                        if customer:
                            if customer_city_value_new != '' and customer_area_value_new != '':
                                users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new)
                                if users:
                                    customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new, c_area__in=customer_area_value_new).count()
                                    customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                    customer_addresswise_count = customer_count

                                    for u in users:
                                        for notice in sent_notice:
                                            if notice == "sms":
                                                    contact = u.mobile_no
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
                                                                            "DLT_CT_ID":unique_template_id, # Template Id
                                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                        }
                                                                    ]
                                                                }

                                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                        response = requests.post(url, json = data_temp)

                                                    sms_response = sendSMS(str(contact), message)
                                    if response.status_code == 200:
                                        total_sms_avilable_new = 0
                                        if customer:
                                            total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                            subscription_object.total_sms_avilable = total_sms_avilable_new
                                        else:
                                            total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                            subscription_object.total_sms_avilable = total_sms_avilable_new

                                        subscription_object.save()

                                        bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                        
                                        sweetify.success(request, title="Success", icon='success',
                                                                text='SMS Send successfully!!', timer=3000)
                                    else:
                                        bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                        sweetify.error(request, title="Error", icon='error',
                                                        text="Something Went Wrong!!!", timer=3000)
                                    
                                else:
                                    sweetify.error(request, title="Error", icon='error',text="Customers in this area not found.", timer=5500)
                            elif customer_city_value_new != '' and customer_area_value_new == '':
                                users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new)
                                if users:
                                    customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new, c_city__in=customer_city_value_new).count()
                                    customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                    customer_addresswise_count = customer_count

                                    for u in users:
                                        for notice in sent_notice:
                                            if notice == "sms":
                                                    contact = u.mobile_no
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
                                                                            "DLT_CT_ID":unique_template_id, # Template Id
                                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                        }
                                                                    ]
                                                                }

                                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                        response = requests.post(url, json = data_temp)

                                                        
                                                    
                                                    sms_response = sendSMS(str(contact), message)
                                    if response.status_code == 200:
                                        total_sms_avilable_new = 0
                                        if customer:
                                            total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                            subscription_object.total_sms_avilable = total_sms_avilable_new
                                        else:
                                            total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                            subscription_object.total_sms_avilable = total_sms_avilable_new

                                        subscription_object.save()

                                        bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                        
                                        sweetify.success(request, title="Success", icon='success',
                                                                text='SMS Send successfully!!', timer=3000)
                                    else:
                                        bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                        sweetify.error(request, title="Error", icon='error',
                                                        text="Something Went Wrong!!!", timer=3000)
                                    
                                else:
                                    sweetify.error(request, title="Error", icon='error',text="Customers in this area not found.", timer=3000)
                            elif customer_city_value_new == '' and customer_area_value_new == '':
                                users = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new)
                                if users:
                                    customer_count = GreenBillUser.objects.filter(is_customer=True, c_state__in=customer_state_value_new).count()
                                    customer_sms_count = bulkMailSmsMerchantCustomerModel.objects.filter(id = notice_id[0].id).update(sms_count=customer_count)
                                    customer_addresswise_count = customer_count

                                    for u in users:
                                        for notice in sent_notice:
                                            if notice == "sms":
                                                    contact = u.mobile_no
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
                                                                            "DLT_CT_ID":unique_template_id, # Template Id
                                                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                                        }
                                                                    ]
                                                                }

                                                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                                        response = requests.post(url, json = data_temp)

                                                        
                                                    
                                                    sms_response = sendSMS(str(contact), message)
                                    if response.status_code == 200:
                                        total_sms_avilable_new = 0
                                        if customer:
                                            total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                            subscription_object.total_sms_avilable = total_sms_avilable_new
                                        else:
                                            total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                            subscription_object.total_sms_avilable = total_sms_avilable_new

                                        subscription_object.save()

                                        bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered ')
                                        
                                        sweetify.success(request, title="Success", icon='success',
                                                                text='SMS Send successfully!!', timer=3000)
                                    else:
                                        bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                        sweetify.error(request, title="Error", icon='error',
                                                        text="Something Went Wrong!!!", timer=3000)
                                    
                                else:
                                    sweetify.error(request, title="Error", icon='error',text="Customers in this area not found.", timer=3000)
                        if custom_number_list:
                            for notice in sent_notice:
                                for number in custom_number_list:
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
                                                                "DLT_CT_ID":unique_template_id, # Template Id
                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                            }
                                                        ]
                                                    }

                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                            response = requests.post(url, json = data_temp)

                                        
                                        sms_response = sendSMS(str(contact), message)
                                        

                        
                            if response.status_code == 200:
                                total_sms_avilable_new = 0
                                if customer:
                                    total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                    subscription_object.total_sms_avilable = total_sms_avilable_new
                                else:
                                    total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                    subscription_object.total_sms_avilable = total_sms_avilable_new
                                
                                subscription_object.save()
                                    
                                bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered')

                                sweetify.success(request, title="Success", icon='success',
                                                        text='SMS Send successfully!!', timer=5500)
                            else:
                                bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                sweetify.error(request, title="Error", icon='error',
                                                text="Something Went Wrong!!!", timer=5500)

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
                                                                "DLT_CT_ID":unique_template_id, # Template Id
                                                                "DLT_PE_ID":"1001659120000037015" # PE ID 
                                                            }
                                                        ]
                                                    }

                                            url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                                            response = requests.post(url, json = data_temp)

                                        
                                        sms_response = sendSMS(str(contact), message)

                        
                            if response.status_code == 200:
                                total_sms_avilable_new = 0
                                if customer:
                                    total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int(customer_addresswise_count)
                                    subscription_object.total_sms_avilable = total_sms_avilable_new
                                else:
                                    total_sms_avilable_new = int(float(subscription_object.total_sms_avilable)) - int('0' + receipent_count)
                                    subscription_object.total_sms_avilable = total_sms_avilable_new
                                
                                subscription_object.save()
                                    
                                bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'Delivered')

                                sweetify.success(request, title="Success", icon='success',
                                                        text='SMS Send successfully!!', timer=5500)
                            else:
                                bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                                sweetify.error(request, title="Error", icon='error',
                                                text="Something Went Wrong!!!", timer=5500)

                    else:
                        bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status="failed to Deliver")
                        sweetify.success(request, title="Oops...", icon='error', text='Insufficient Balance. Please purchase promotional plan and try again !!!', timer=2000)
                else:
                    bulkMailSmsMerchantCustomerModel.objects.filter(id=smsid+1).update(sent_status= 'failed to Deliver')
                    sweetify.success(request, title="Oops...", icon='error', text="You don't have active promotional SMS plan. Please purchase and try again.", timer=2000)
           

            
    
    smsmail = bulkMailSmsMerchantCustomerModel.objects.filter(owner_id=merchant_object,o_sent_sms=True).order_by('-id')
    
    sms_data = []
    
    for sms in smsmail:
        try :
            receiver_name = int(sms.receiver_name)
            sms_data.append({
                'created_at' : sms.created_at,
                'receiver_name':'Custom',
                'smsheader': sms.smsheader, 
                'transactional': sms.transactional, 
                'sms_count': sms.sms_count,
                'sent_status': sms.sent_status,
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
                'sms_count': sms.sms_count,
                'sent_status': sms.sent_status,
                'id': sms.id,
                'message':sms.message,
                'campaign_name':sms.campaign_name,
                })
 
    promotional_remaining_sms = ''
    promotional_used_sms = ''
    transactional_remaining_sms = ''
    transactional_used_sms = ''
    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']
    business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)
    if getActiveTransactionalSubscriptionPlan(request, business_object.id):
        tran_subscription_object = getActiveTransactionalSubscriptionPlan(request, business_object.id)
        transactional_remaining_sms = int(tran_subscription_object.total_sms_avilable) if tran_subscription_object.total_sms_avilable else 0
        transactional_used_sms = int(tran_subscription_object.total_sms) - transactional_remaining_sms
    else:
        pass

    if getActivePromotionalSubscriptionPlan(request, business_object.id):
        promo_subscription_object = getActivePromotionalSubscriptionPlan(request, business_object.id)
        promotional_remaining_sms = int(promo_subscription_object.total_sms_avilable) if promo_subscription_object.total_sms_avilable else 0
        promotional_used_sms = int(promo_subscription_object.total_sms) - promotional_remaining_sms

    else:
        pass
    states = GreenBillUser.objects.values('c_state').distinct()
    header = smsHeaderModel.objects.filter(request_user = request.user, Active_status = True)
    Template = templateContentModel.objects.filter(request_user = request.user, status='Approved')

    context = {
        'header': header,
        'Template': Template,
        'cust_data': states,
        'data': sms_data,
        'customer_list': merchant_added_customer_list,
        'PromotionsNavclass': 'active',
        'ShowPromotionsNavclass':'show',
        'BulkSMSNavclass':'active',
        "customer_addresswise_count":customer_addresswise_count,
        'merchant_added_customer_count':merchant_added_customer_count,
        'transactional_used_sms':transactional_used_sms,
        'transactional_remaining_sms':transactional_remaining_sms,
        'promotional_remaining_sms':promotional_remaining_sms,
        'promotional_used_sms':promotional_used_sms,
        'bulkMailSmsMerchantCustomerForm':bulkMailSmsMerchantCustomerForm,
    }

    return render(request, 'merchant/merchant_notice_board/merchant-promotion-sms.html' , context)
    
    

def deletebulksmsemail(request,id):
    instance = bulkMailSmsMerchantCustomerModel.objects.get(id=id).delete()

    return JsonResponse({'success':True})



def smsHeader(request):
    if request.method == "POST":
        request_header = request.POST.get('request_header')
        print('request_header',request_header)

        
        
        header = smsHeaderModel.objects.create(header_content= request_header, request_user = request.user)
        print(header)
        # if template:
        #     return JsonResponse({"success": True, "status": "success"})
        # else:
        #     return JsonResponse({"success": True, "status": "error"})

        if header:
            return JsonResponse({"success": True, "status": "success"})
        else:
            return JsonResponse({"success": True, "status": "error"})


def smsTemplate(request):
    if request.method == "POST":
        

        request_template = request.POST.get('request_template')
        print('request_template',request_template)
        print(request.user)
        
        template = templateContentModel.objects.create(template_content= request_template, request_user = request.user)
        # if template:
        #     return JsonResponse({"success": True, "status": "success"})
        # else:
        #     return JsonResponse({"success": True, "status": "error"})

        if template:
            return JsonResponse({"success": True, "status": "success"})
        else:
            return JsonResponse({"success": True, "status": "error"})



def download_sample_contact_file(request):
    path = 'sample_email_sms_files/sample_contacts.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="sample_email_sms_files/sample_contacts.csv")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
    

def download_sample_email_file(request):
    path = 'sample_email_sms_files/sample_emails.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="sample_email_sms_files/sample_emails.csv")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def get_city_by_state_ids_in_merchant_bulk_sms(request):

    customer_state_value = request.POST['customer_state_value']

    customer_state_value_new = customer_state_value.split(",")

    list1 = []

    filtered_city_list = []

    for cust_state in customer_state_value_new:

        cus_state_id = GreenBillUser.objects.filter(c_state = cust_state)

        for city in cus_state_id:
            list1.append({
                "c_city": city.c_city
            })
        
    for x in list1:
        if x['c_city'] not in filtered_city_list:
            if x['c_city'] != '':
                filtered_city_list.append(x['c_city'])
    print(filtered_city_list)

    return JsonResponse({"data":filtered_city_list})


def get_area_by_city_names_in_merchant_bulk_sms(request):

    customer_city_value = request.POST['customer_city_value']

    customer_city_value_new = customer_city_value.split(",")

    list1 = []

    filtered_area_list = []

    for area in customer_city_value_new:

        cust_id = GreenBillUser.objects.filter(c_city=area)

        for area in cust_id:
            list1.append({
                "c_area": area.c_area
            })
        
    for x in list1:
        if x['c_area'] not in filtered_area_list:
            filtered_area_list.append(x['c_area'])

    return JsonResponse({"data":filtered_area_list})

def get_city_by_state_ids_in_merchant_bulk_email(request):

    customer_state_value = request.POST['customer_state_value']

    customer_state_value_new = customer_state_value.split(",")

    list1 = []

    filtered_city_list = []

    for cust_state in customer_state_value_new:

        cus_state_id = GreenBillUser.objects.filter(c_state = cust_state)

        for city in cus_state_id:
            list1.append({
                "c_city": city.c_city
            })
        
    for x in list1:
        if x['c_city'] not in filtered_city_list:
            if x['c_city'] != '':
                filtered_city_list.append(x['c_city'])
    print(filtered_city_list)

    return JsonResponse({"data":filtered_city_list})


def get_area_by_city_names_in_merchant_bulk_email(request):

    customer_city_value = request.POST['customer_city_value']

    customer_city_value_new = customer_city_value.split(",")

    list1 = []

    filtered_area_list = []

    for area in customer_city_value_new:

        cust_id = GreenBillUser.objects.filter(c_city=area)

        for area in cust_id:
            list1.append({
                "c_area": area.c_area
            })
        
    for x in list1:
        if x['c_area'] not in filtered_area_list:
            filtered_area_list.append(x['c_area'])

    return JsonResponse({"data":filtered_area_list})