from django.db.models.query_utils import Q
from sweetify.sweetify import success
from users.models import Merchant_users
from django import forms
from django.shortcuts import redirect, render
from .models import *
import sweetify
from django.http import JsonResponse, HttpResponseRedirect
from .forms import CustomerCashMemodetailsForm, CustomerReceiptdetailsForm
from users.models import MerchantProfile
from django.views.decorators.csrf import csrf_exempt
from my_subscription.models import *
from merchant_stamp.models import *
from owner_stamp.models import *
from promotions.models import *
import re


from bill_design.models import *
# Create your views here.
from django.conf import settings
from merchant_software_apis.models import DeviceId
import socket
from pyfcm import FCMNotification
import random
import string
import inflect
# SMS
import requests
import time
import pyshorteners
from datetime import datetime, date, timedelta

from app.views import is_merchant_or_merchant_staff, getActiveSubscriptionPlan


# def select_image_stamp(request):

#     merchant_user_object = Merchant_users.objects.get(user_id = request.user)

#     merchant_object = merchant_user_object.merchant_user_id

#     merchant_business_id = MerchantProfile,objects.get(m_user = merchant_object, m_active_account = True)



#     select_stamp_image = selectstampimage.objects.get(merchant_user = request.user, merchant_business_id = merchant_business_id)

#     return render(view_all_cash_memo)

def UnselectCashMemoStamp(request):
    print('aaaaaa')

    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    latest_selected = save_stamp_for_cashmemo.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id).last()

    if latest_selected:
        check = ''
        result = save_stamp_for_cashmemo.objects.filter(id = latest_selected.id).update(stamp_id_cashmemo = check)
        if result:
            sweetify.success(request, title="Success", icon='success', text='Stamp Uncheck Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Unchek.', timer=1000)
    else:
        sweetify.success(request, title="Oops...", icon='error', text='Stamp Select first.', timer=1000)

    return redirect(view_all_cash_memo)


def unselectreceiptstamp(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    latest_selected = save_stamp_for_receipt.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id).last()

    if latest_selected:
        check = ''
        result = save_stamp_for_receipt.objects.filter(id = latest_selected.id).update(stamp_id_cashmemo = check)
        if result:
            sweetify.success(request, title='success', icon='success', context='stamp Uncheck Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Unchek.', timer=1000)
    else:
        sweetify.success(request, title="Oops..", icon='error', text='Stamp Select first.', timer=1000)

    return redirect(view_all_receipts)


def Cash_Memo_Design_View(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    if request.method == "POST":
        design_file = request.FILES['cash_memo_file']
        paper_size = request.POST.get('paper_size')
        comments = request.POST['comments']

        obj = Cash_Memo_Design_Model.objects.create(merchant_business_id = merchant_business_id, merchant_user=request.user, memo_design_image=design_file, paper_size=paper_size, comments=comments)
        if obj:
            sweetify.success(request, title="Success", icon="success", text="Saved Successfully", timer=1500)
        else:
            sweetify.success(request, title="Success", icon="success", text="Someting went to wrong.", timer=1500)

    all_design = Cash_Memo_Design_Model.objects.filter(merchant_business_id = merchant_business_id, merchant_user=request.user).order_by('-id')
   
    context = {
        'all_design': all_design,
        'DesignNavclass': 'active',
        'DesignCollapseShow': 'show',
        'CashMemoDesignNavClass': 'active',
    }

    return render(request, "merchant/merchant_cash_memo_design/cash_memo_design.html", context)


def Delete_Memo_Design(request, id):
    memo_design_obj = Cash_Memo_Design_Model.objects.get(id=id)

    if memo_design_obj:
        memo_design_obj.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


def All_Cash_Memo_Design(request):
    """ This code for Display all data for super user"""
    qs = Cash_Memo_Design_Model.objects.all()
    unread_count = Cash_Memo_Design_Model.objects.filter(read_status=False).count()
    update_read_status = Cash_Memo_Design_Model.objects.filter(read_status=False)
    update_read_status.update(read_status=True)
    for all in qs:
        design_object = MerchantProfile.objects.filter(m_user = all.merchant_user)
        for object in design_object:
            all.m_business_name = object.m_business_name
            print('aaa')
    context = {
        "memo_list": qs,
        'MemoDesignNavClass': 'active',
    }

    return render(request, "merchant/merchant_cash_memo_design/owner_cash_memo_design.html", context)


def stamp_for_cash_memo(request):

    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True) 

    if request.method == 'POST':

        stamp_id = request.POST['chk']

        check_cashmemo_stamp = save_stamp_for_cashmemo.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)

        if check_cashmemo_stamp:

            updatecashmemo_stamp = save_stamp_for_cashmemo.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id).update(stamp_id_cashmemo = stamp_id)

            if updatecashmemo_stamp:
                sweetify.success(request, title="Success", icon="success", text= "Stamp saved Successfully", timer = 1500)

            else:
                sweetify.error(request, title="Error", icon='error', text='failed to saved', timer=1500)

        else:

            result = save_stamp_for_cashmemo.objects.create(merchant_user = request.user, merchant_business_id = merchant_business_id, stamp_id_cashmemo = stamp_id)

            if result:
                sweetify.success(request, title="Success", icon="success", text= "Stamp saved Successfully", timer = 1500)

            else:
                sweetify.error(request, title="Error", icon='error', text='failed to saved', timer=1500)

    return redirect(view_all_cash_memo)


def stamp_for_receipt(request):

    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True) 

    if request.method == 'POST':

        stamp_id = request.POST['chk']

        print('111',stamp_id)

        check_receipt_stamp = save_stamp_for_receipt.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)

        if check_receipt_stamp:

            updatereceipt_stamp = save_stamp_for_receipt.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id).update(stamp_id_cashmemo = stamp_id)

            if updatereceipt_stamp:
                sweetify.success(request, title="Success", icon="success", text= "Stamp saved Successfully", timer = 1500)

            else:
                sweetify.error(request, title="Error", icon='error', text='failed to saved', timer=1500)

        else:

            result = save_stamp_for_receipt.objects.create(merchant_user = request.user, merchant_business_id = merchant_business_id, stamp_id_cashmemo = stamp_id)

            if result:
                sweetify.success(request, title="Success", icon="success", text= "Stamp saved Successfully", timer = 1500)

            else:
                sweetify.error(request, title="Error", icon='error', text='failed to saved', timer=1500)

    return redirect(view_all_receipts)


def view_all_cash_memo(request):

    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)   

    # print("merchant_user_object",merchant_user_object)
    # print("merchant_object",merchant_object)
    # print("merchant_business_id",merchant_business_id)

    if merchant_business_id.m_digital_signature:
        sign = merchant_business_id.m_digital_signature
    else:
        sign = ''

    try:
        merchant_select_stamp = merchantusagestamp.objects.filter(merchant_user_id=request.user, merchant_business_id = merchant_business_id).last()

        stamp_id = merchant_select_stamp.merchant_stamp_id_one

    except:

        stamp_id = ''

    if stamp_id:
        temp_stamp = ""
        temp_stamp = stamp_id.replace("[", "")
        temp_stamp = temp_stamp.replace("]", "")
        temp_stamp = temp_stamp.replace("'", "")
        stamp_id = temp_stamp


    new_stamp_id = stamp_id.split(", ")

    stamp_data = []
    counter = 0
    for stamp in new_stamp_id:
        if stamp:
            latest_stamp_record = wstampmodels.objects.filter(id=stamp)
            for stamp1 in latest_stamp_record:
                counter = counter + 1
                stamp_data.append({
                    "id" : stamp1.id,
                    "stamp_name" : stamp1.stamp_name,
                    "stamp_content" : stamp1.stamp_content,
                    "option_color" : stamp1.option_color,
                    "selection_design" : stamp1.selection_design,
                    "type":'stamps',
                    })
    
   
    try:
        selected_stamp = save_stamp_for_cashmemo.objects.get(merchant_business_id = merchant_business_id)
        saved_stamp_record1 = wstampmodels.objects.filter(id=selected_stamp.stamp_id_cashmemo)
        s_id = selected_stamp.stamp_id_cashmemo
    except:
        saved_stamp_record1 = '' 
        s_id = ''

    try:
        saved_stamp_image = selectstampimage.objects.get(merchant_business_id = merchant_business_id, merchant_user = request.user).m_select_image
        selected_stamp_image = merchantstampupload.objects.filter(id = saved_stamp_image)

        for stamp in selected_stamp_image:
        	stamp_data.append({
        		"id" : stamp.id,
        		"stamp_name": stamp.stamp_name,
        		"stamp_content" : "",
                "option_color" : "",
                "selection_design" : "",
                "type":'ownstamps',
        		})
        # 	print(stamp.stamp_name,'---------------------------------')

       	# print(stamp_data,'---------')
    except:
        selected_stamp_image = ''




    # if request.method == "POST":



    if request.method == "POST":
        if request.POST.get("create_form_btn") == "save_cashmemo_btn":
            # selected_cash_memo_stamp = save_stamp_for_cashmemo.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)

            # saved_stamp_for_cashmemo = usecashmemostamp.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)
            
            # try:
            #     if selected_cash_memo_stamp[0].stamp_id_cashmemo:
            #         stamp_data_id = selected_cash_memo_stamp[0].stamp_id_cashmemo
            #         is_stamp_type = 1


            #     elif saved_stamp_for_cashmemo[0].stamp_image_id:
            #         stamp_data_id = saved_stamp_for_cashmemo[0].stamp_image_id
            #         is_stamp_type = 2

            #     elif not selected_cash_memo_stamp[0].stamp_id_cashmemo:
            #         if not saved_stamp_for_cashmemo[0].stamp_image_id:
            #             stamp_data_id = ''
            #             is_stamp_type = 0
            # except:
            #     is_stamp_type = ''
            #     stamp_data_id = ''


            stamp_selected = request.POST.get('stamp_type')

            if stamp_selected == "merchant_stamp":
            	is_stamp_type = 1
            	stamp_data_id = request.POST.get('default_selected_stamp')
            elif stamp_selected == "own_stamp":
            	is_stamp_type = 2
            	stamp_data_id = request.POST.get('own_selected_stamp')
            else:
            	is_stamp_type == ''
            	stamp_data_id == ''


            try:
                memo = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_id).last()
            except:
                memo = ""

            if not memo:
                memo_no =  str("01").zfill(3)

            else:
                last_receipt = memo.memo_no

                # print("nilesh1233",last_receipt)
                
                no = int(last_receipt) + 1

                memo_no =  str(no).zfill(3)

            name = request.POST['name']
            address = request.POST['address']
            mobile_number = request.POST['mobile_number']
            date = request.POST['date']
            term_and_condition1 = request.POST.get('term_and_condition1')
            term_and_condition2 = request.POST.get('term_and_condition2')
            term_and_condition3 = request.POST.get('term_and_condition3')
            authorised = sign
            description_1 = request.POST.get('description_1')
            description_2 = request.POST.get('description_2')
            description_3 = request.POST.get('description_3')
            description_4 = request.POST.get('description_4')  
            description_5 = request.POST.get('description_5')
            description_6 = request.POST.get('description_6')
            description_7 = request.POST.get('description_7')
            description_8 = request.POST.get('description_8')
            description_9 = request.POST.get('description_9')
            description_10 = request.POST.get('description_10')

            selected_template_data = request.POST.get('selected_template_data')
            
            temp_desc = []
            if description_1:
                temp_desc.append(description_1)
            if description_2:
                temp_desc.append(description_2)
            if description_3:
                temp_desc.append(description_3)
            if description_4:
                temp_desc.append(description_4)
            if description_5:
                temp_desc.append(description_5)
            if description_6:
                temp_desc.append(description_6)
            if description_7:
                temp_desc.append(description_7)
            if description_8:
                temp_desc.append(description_8)
            if description_9:
                temp_desc.append(description_9)
            if description_10:
                temp_desc.append(description_10)
            
            temp_desc = [str(i or '') for i in temp_desc]
            
            description = ",".join(temp_desc)
           
            quantity_1 = request.POST.get('quantity_1')
            quantity_2 = request.POST.get('quantity_2')
            quantity_3 = request.POST.get('quantity_3')
            quantity_4 = request.POST.get('quantity_4')
            quantity_5 = request.POST.get('quantity_5')
            quantity_6 = request.POST.get('quantity_6')
            quantity_7 = request.POST.get('quantity_7')
            quantity_8 = request.POST.get('quantity_8')
            quantity_9 = request.POST.get('quantity_9')
            quantity_10 = request.POST.get('quantity_10')

            temp_quant = []

            if quantity_1:
                temp_quant.append(quantity_1)
            if quantity_2:
                temp_quant.append(quantity_2)
            if quantity_3:
                temp_quant.append(quantity_3)
            if quantity_4:
                temp_quant.append(quantity_4)
            if quantity_5:
                temp_quant.append(quantity_5)
            if quantity_6:
                temp_quant.append(quantity_6)
            if quantity_7:
                temp_quant.append(quantity_7)
            if quantity_8:
                temp_quant.append(quantity_8)
            if quantity_9:
                temp_quant.append(quantity_9)
            if quantity_10:
                temp_quant.append(quantity_10)

            conv = lambda i : i or ''
            temp_quant = [conv(i) for i in temp_quant]
            quantity = ",".join(temp_quant)

           
            rate_1 = request.POST.get('rate_1')
            rate_2 = request.POST.get('rate_2')
            rate_3 = request.POST.get('rate_3')
            rate_4 = request.POST.get('rate_4')
            rate_5 = request.POST.get('rate_5')
            rate_6 = request.POST.get('rate_6')
            rate_7 = request.POST.get('rate_7')
            rate_8 = request.POST.get('rate_8')
            rate_9 = request.POST.get('rate_9')
            rate_10 = request.POST.get('rate_10')
            
            temp_rate = []
            if rate_1:
                temp_rate.append(rate_1)
            if rate_2:
                temp_rate.append(rate_2)
            if rate_3:
                temp_rate.append(rate_3) 
            if rate_4:
                temp_rate.append(rate_4) 
            if rate_5:
                temp_rate.append(rate_5) 
            if rate_6:
                temp_rate.append(rate_6) 
            if rate_7:
                temp_rate.append(rate_7) 
            if rate_8:
                temp_rate.append(rate_8) 
            if rate_9:
                temp_rate.append(rate_9) 
            if rate_10:
                temp_rate.append(rate_10) 
             
            
            conv = lambda i : i or ''
            temp_rate = [conv(i) for i in temp_rate]
            rate = ",".join(temp_rate)

            # amount_1 = request.POST.get('amount_1')
            # amount_2 = request.POST.get('amount_2')
            # amount_3 = request.POST.get('amount_3')
            # amount_4 = request.POST.get('amount_4')
            # amount_5 = request.POST.get('amount_5')
            # amount_6 = request.POST.get('amount_6')
            # amount_7 = request.POST.get('amount_7')
            # amount_8 = request.POST.get('amount_8')
            # amount_9 = request.POST.get('amount_9')
            # amount_10 = request.POST.get('amount_10')

            amount_1 = ''
            amount_2 = ''
            amount_3 = ''
            amount_4 = ''
            amount_5 = ''
            amount_6 = ''
            amount_7 = ''
            amount_8 = ''
            amount_9 = ''
            amount_10 = ''  
            # print(rate_1)
            if rate_1 and quantity_1 != None:
                amount_1 = float(quantity_1)*float(rate_1)
            if rate_2 and quantity_2 != None:
                amount_2 = float(quantity_2)*float(rate_2)
            if rate_3 and quantity_3 != None:
                amount_3 = float(quantity_3)*float(rate_3)
            if rate_4 and quantity_4 != None:
                amount_4 = float(quantity_4)*float(rate_4)
            if rate_5 and quantity_5 != None:
                amount_5 = float(quantity_5)*float(rate_5)
            if rate_6 and quantity_6 != None:
                amount_6 = float(quantity_6)*float(rate_6)
            if rate_7 and quantity_7 != None:
                amount_7 = float(quantity_7)*float(rate_7)
            if rate_8 and quantity_8 != None:
                amount_8 = float(quantity_8)*float(rate_8)
            if rate_9 and quantity_9 != None:
                amount_9 = float(quantity_9)*float(rate_9)
            if rate_10 and quantity_10 != None:
                amount_10 = float(quantity_10)*float(rate_10)


            temp_amnt = []
            if amount_1:
                temp_amnt.append(amount_1)
            if amount_2:
                temp_amnt.append(amount_2)
            if amount_3:
                temp_amnt.append(amount_3)
            if amount_4:
                temp_amnt.append(amount_4)
            if amount_5:
                temp_amnt.append(amount_5)
            if amount_6:
                temp_amnt.append(amount_6)
            if amount_7:
                temp_amnt.append(amount_7)
            if amount_8:
                temp_amnt.append(amount_8)
            if amount_9:
                temp_amnt.append(amount_9)
            if amount_10:
                temp_amnt.append(amount_10)
            
            
            conv = lambda i : i or ''
            # print('conv',conv)
            temp_amnt = [conv(i) for i in temp_amnt]
            # print(temp_amnt)
            amount = ",".join(map(str,temp_amnt))

            total = 0
            for i in temp_amnt:
                # print(i)
                total = total + float(i)
            p = inflect.engine()
            total_in_words = p.number_to_words(total)

            result = CustomerCashMemoDetailModels.objects.create(merchant_business_id = merchant_business_id,
            merchant_user=request.user, name =name, 
            mobile_number=mobile_number,total=total, 
            total_in_words=total_in_words,date=date, 
            description=description, 
            quantity=quantity, 
            rate=rate,
            amount=amount, 
            memo_no =  memo_no, 
            address=address,
            authorised_sign=authorised,
            term_and_condition1=term_and_condition1,
            term_and_condition2=term_and_condition2,
            term_and_condition3=term_and_condition3,
            stamp_last_record = stamp_data_id,
            is_stamp_type = is_stamp_type,
            template_choice = selected_template_data)
            
            letters = string.ascii_letters
            digit = string.digits
            random_string = str(result.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
            
            result.memo_url = random_string

            result.save()
            context ={}
            if result:
                context['created_status'] = "1"
                sweetify.success(request, title="Success", icon="success", text= "Cash Memo Updated Successfully", timer = 1500)

            else:
                sweetify.error(request, title="Error", icon='error', text='Cash Memo Upadte Failed', timer=1500)
    

    try:
        template_selected1 = save_template_for_cashmemo.objects.filter(merchant_user=request.user).last()
        template_selected = template_selected1.template
    except:
        template_selected = ''

    
    if request.POST.get("submit_btn") == "filter_btn":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        object_list = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_id, date__range=(from_date,to_date)).order_by("-id")
        object_list_count = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_id, date__range=(from_date,to_date)).count()
        object_reject_count = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_id, rejected_cash_memo= True, date__range=(from_date,to_date)).count()
        total_cost_cash_memo = 0
        for object1 in object_list:
            if object1.total and object1.rejected_cash_memo == False:
                total_cost_cash_memo = float(object1.total) + float(total_cost_cash_memo)

    else:
        object_list = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_id).order_by("-id")
        object_list_count = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_id).count()
        object_reject_count = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_id , rejected_cash_memo= True).count()
        total_cost_cash_memo = 0
        from_date = ''
        to_date = ''
        for object1 in object_list:
            if object1.total and object1.rejected_cash_memo == False:
                total_cost_cash_memo = float(object1.total) + float(total_cost_cash_memo)



    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    forms= MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)
    tax_with_gst = 0

    for cash_memo in object_list:
        cash_memo.tax_amount = 0.18 * float(cash_memo.total) + float(cash_memo.total)
        # print('cash_memo.tax_amount',cash_memo.tax_amount)

    try:
        latest_terms_conditions = CustomerCashMemoDetailModels.objects.filter(merchant_business_id = merchant_business_id).last()
        first_condition = latest_terms_conditions.term_and_condition1

        second_condition = latest_terms_conditions.term_and_condition2

        third_condition = latest_terms_conditions.term_and_condition3
    except:
        first_condition = ''

        second_condition = ''

        third_condition = ''
    stamp_checked_id = ''
    selected_cash_memo_stamp = save_stamp_for_cashmemo.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)

    for cashmemo_stamp in selected_cash_memo_stamp:
        if cashmemo_stamp.stamp_id_cashmemo:
            stamp_checked_id = int(cashmemo_stamp.stamp_id_cashmemo)

    try:
        saved_stamp_for_cashmemo = usecashmemostamp.objects.get(merchant_user = request.user, merchant_business_id = merchant_business_id).stamp_image_id
        
    except:
        saved_stamp_for_cashmemo = ''



    # print(counter)

    context = {
        'saved_stamp_for_cashmemo': saved_stamp_for_cashmemo,
        'first_condition': first_condition,
        'selected_stamp_image': selected_stamp_image,
        'second_condition': second_condition,
        'stamp_checked_id': stamp_checked_id,
        'third_condition': third_condition,
        'template_selected': template_selected,
        'form' : forms, 
        'saved_stamp_record1': saved_stamp_record1,
        'sign' : sign, 
        'total_cost_cash_memo': total_cost_cash_memo,
        'merchant_business_id' : merchant_business_id,
        'object' : object_list,
        'object_list_count': object_list_count,
        'object_reject_count': object_reject_count,
        'counter': counter,
        'from_date': from_date,
        'to_date': to_date,
        'stamp_data' : stamp_data,
        'CashmemosNaveClass': "active", 
        'cashmemoCollapseShow': "show",
        'CashMemoNavClass': "active",
    }
    return render(request, "merchant/merchant_cash_memo_design/merchant_cash_memo.html", context)



def save_cash_memo_template(request):
    if request.method == 'POST':
        selected_template = request.POST['selected_template'] 

        result=save_template_for_cashmemo.objects.create(merchant_user=request.user, template=selected_template)
        
    if result:
        sweetify.success(request, title="Success", icon='success', text='Template Added Successfully.', timer=1500)
    else:
        sweetify.success(request, title="Oops...",icon='error', text='Fail to Add.', timer=1000)
        
    return redirect(view_all_cash_memo)

# For sample dummy bill
def sample_dummy_bill(request): 
    return render(request, "customer/customer_bill/sample-bill-dummy.html")


@csrf_exempt
def SendCashMemoUsingWeb(request,id):
    print("*************")
    try:
        print("In try")
        if request.method == 'POST':
            mobile_number = id
            # print("Inside ")
            
            # mobile_number = request.POST.get('mobile_number')
                #memo_url = ""
            # print(id,mobile_number)
            # memo_url = "http://157.230.228.250/cash-memo/" + str(random_string) + "/"
            # sample_bill = "http://157.230.228.250/sample-bill-dummy/"
            # s = pyshorteners.Shortener()
            # print(s)
            # short_url = s.tinyurl.short(sample_bill)

            mo = request.POST.get('mobile_number')
            print("************************************")
            print(mo)
            print(mobile_number)
            short_url = "https://bit.ly/3fwlvqt"
            
            push_service = FCMNotification(api_key=settings.API_KEY)
           

            if True :
                print("Inside")
                ts = int(time.time())
                data_temp = {
                    "keyword":"Cash Memo",
                    "timeStamp":ts,
                    "dataSet":
                    [
                        {
                            "UNIQUE_ID":"GB-" + str(ts),
                            "MESSAGE":"Thank you for contacting Green Bill, tap the below link for your digital bill  " + short_url,
                            "OA":"GBBILL",
                            "MSISDN": str(mo), # Recipient's Mobile Number
                            "CHANNEL":"SMS",
                            "CAMPAIGN_NAME":"hind_user",
                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                            "USER_NAME":"hind_hsi",
                            "DLT_TM_ID":"1001096933494158", # TM ID
                            # "DLT_CT_ID":"1007162098381110505", # Template Id
                            "DLT_CT_ID":"1007162098307281560",
                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                        }
                    ]
                }
                
                url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                response = requests.post(url, json = data_temp)
                # print(response)
                if response.status_code == 200:
                    # total_amount_avilable_new = 0
                    # total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
                    # subscription_object.total_amount_avilable = total_amount_avilable_new
                    # subscription_object.save()
                    return JsonResponse({"success": True, "status": "success"})
                else:
                    return JsonResponse({"success": False, "status": "error", "message": "Fail to send SMS !!!"})
            else:
                return JsonResponse({"success": False, "status": "error", "message": "Fail to send SMS !!!"})
    except:
        return JsonResponse({"success": False, "status": "error", "message":"Failed !!!"})            

        # mobile_number = request.POST['mobile_number']


def CashMemoSendMemoSMSWeb(request,id):

    mer_user_id = Merchant_users.objects.get(user_id=request.user)

    merchant_object = mer_user_id.merchant_user_id
    
    merchant_business_object = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    merchant_business_id = merchant_business_object.id

    subscription_object = getActiveSubscriptionPlan(request, merchant_business_id)

    if request.POST and subscription_object:
        if subscription_object.total_amount_avilable and subscription_object.per_bill_cost:

            if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

                id = id
                memo_object = CustomerCashMemoDetailModels.objects.get(id = id)
                letters = string.ascii_letters
                digit = string.digits
                random_string = str(id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                
                memo_object.memo_url = random_string

                memo_object.save()

                mobile_number = request.POST.get('mobile_number')
                #memo_url = ""

                memo_url = "http://157.230.228.250/cash-memo/" + str(random_string) + "/"

                s = pyshorteners.Shortener()
                short_url = s.tinyurl.short(memo_url)

                device = DeviceId.objects.filter(mobile_no=mobile_number, user_type='customer').first()

                push_service = FCMNotification(api_key=settings.API_KEY)

                if device != None:
                    registration_id = device.device_id

                    message_title = "Receiving New Cash Memo"

                    message_body = "You have received a Cash Memo from. " + str(memo_object.merchant_business_id.m_business_name) + str(memo_url)

                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

                    total_amount_avilable_new = 0
                    total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_digital_bill_cost)
                    subscription_object.total_amount_avilable = total_amount_avilable_new
                    subscription_object.save()

                    return JsonResponse({'status':'success', 'message': 'Notification send successfully'}, status=200)

                else:

                    if mobile_number:

                        

                        ts = int(time.time())

                        data_temp = {
                                "keyword":"Cash Memo",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Hey Green Bill user to view or download your cash memo click on link " + short_url,
                                            "OA":"GBBILL",
                                            "MSISDN": str(mobile_number), # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098381110505", # Template Id
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

                            return JsonResponse({"success": True, "status": "success"})
                        else:
                            return JsonResponse({"success": False, "status": "error", "message": "Fail to send SMS !!!"})
                    else:
                        return JsonResponse({"success": False, "status": "error", "message": "Fail to send SMS !!!"})
            else:
                return JsonResponse({"success": False, "status": "error", "message":"Insufficient Balance. Please purchase new plan and try again !!!"})
        else:
            return JsonResponse({"success": False, "status": "error", "message":"Insufficient Balance. Please purchase new plan and try again !!!"})

    else:
        return JsonResponse({"success": False, "status": "error", "message":"You don't have active Green Bill Subscription. Please purchase and try again."})



def cash_memo(request, id):


    # print(id)

    # try:
        memo_details = CustomerCashMemoDetailModels.objects.get(memo_url=id)

        merchant_user_id = memo_details.merchant_user

        cashmemo_template1=save_template_for_cashmemo.objects.filter(merchant_user=merchant_user_id).last()

        if cashmemo_template1:
            cashmemo_template = cashmemo_template1.template
        else:
            cashmemo_template = ''
        memo_record = CustomerCashMemoDetailModels.objects.filter(memo_url=id)
        # print(memo_record)

        description = memo_details.description.split(',')
        quantity = memo_details.quantity.split(',')
        rate = memo_details.rate.split(',')
        amount = memo_details.amount.split(',')

        form = MerchantProfile.objects.get(id = memo_details.merchant_business_id.id)

        latest_stamp_record=""
        stamp_uploaded_image = ''
        if memo_details.is_stamp_type == '1':
            if memo_details.stamp_last_record:
                latest_stamp_record = wstampmodels.objects.filter(id=memo_details.stamp_last_record)
                
        elif memo_details.is_stamp_type == '2':
            if memo_details.stamp_last_record:
                stamp_uploaded_image = merchantstampupload.objects.filter(id = memo_details.stamp_last_record)
        else:
            pass

        if form.m_digital_signature:
            sign = form.m_digital_signature
        else:
            sign = ''

        try:
            bill_design = bill_designs.objects.get(merchant_business_id = form)
        except:
            bill_design = ''

        try:
            merchant_business_object = MerchantProfile.objects.get(id = form)

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

        ads_image_details = ""


        space = ads_below_bill.objects.filter(merchant = form.m_user, merchant_business_id = form, ads_type='green_bill').last()

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
                third_party_status = ads_below_bill.objects.filter(merchant = form.m_user, merchant_business_id = form, ads_type='third_party', status = 1).last()
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
                ads_details = ads_below_bill.objects.filter(merchant = form.m_user, merchant_business_id = form, active_ads = True).last()
                if ads_details:
                    ads_image_details = ads_below_bill.objects.get(id = ads_details.id)
                    green_bills_advertisement = True
                    views = ads_below_bill.objects.get(id=ads_details.id)
                    views.count = views.count + 1
                    views.save()
        except:
            ads_image_details = ""

        try:
            cash_memo_head_url = cash_memo_template_images.objects.get(template_id = cashmemo_template)
        except:
            cash_memo_head_url = ""

        business_logo = form.m_business_logo

        context = {
            'template_selected': cashmemo_template,
            'stamp_uploaded_image': stamp_uploaded_image,
            'sign': sign,
            'bill_design':bill_design,
            'business_logo': business_logo,
            'business_address':business_address,
            'ads_image_details':ads_image_details,
            'memo_record': memo_record,
            'memo_details' : memo_details,
            'latest_stamp_record': latest_stamp_record,
            'description' : description,
            'quantity' : quantity,
            'rate' : rate,
            'amount' : amount,
            'form': form,
            'cash_memo_head_url':cash_memo_head_url,
        }

        return render(request, "merchant/merchant_cash_memo_design/cash_memo.html", context)

    # except:
    #     return render(request, 'page-404.html')

def view_ads_record_cashmemo(request, id):
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


def delete_cash_memo(request, id):

    coupon_obj = CustomerCashMemoDetailModels.objects.get(id=id).delete()

    if coupon_obj:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})



def view_all_receipts(request):

    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    try:
        merchant_select_stamp = merchantusagestamp.objects.filter(merchant_user_id=request.user, merchant_business_id = merchant_business_id).last()

        stamp_id = merchant_select_stamp.merchant_stamp_id_one

    except:

        stamp_id = ''

    if stamp_id:
        temp_stamp = ""
        temp_stamp = stamp_id.replace("[", "")
        temp_stamp = temp_stamp.replace("]", "")
        temp_stamp = temp_stamp.replace("'", "")
        stamp_id = temp_stamp


    new_stamp_id = stamp_id.split(", ")

    stamp_data = []
    counter = 0
    for stamp in new_stamp_id:
        if stamp:
            latest_stamp_record = wstampmodels.objects.filter(id=stamp)
            for stamp1 in latest_stamp_record:
                counter = counter + 1

                stamp_data.append({
                    "id" : stamp1.id,
                    "stamp_name" : stamp1.stamp_name,
                    "stamp_content" : stamp1.stamp_content,
                    "option_color" : stamp1.option_color,
                    "selection_design" : stamp1.selection_design,
                    "type":'stamps',
                    })

    # print('11',stamp_data)

    if merchant_business_id.m_digital_signature:
        sign = merchant_business_id.m_digital_signature
    else:
        sign = ''

    context = {}

    try:
        selected_stamp = save_stamp_for_receipt.objects.get(merchant_business_id = merchant_business_id)
        saved_stamp_record1 = wstampmodels.objects.filter(id=selected_stamp.stamp_id_cashmemo)
        s_id = selected_stamp.stamp_id_cashmemo
    except:
        saved_stamp_record1 = ''
        s_id = ''

    try:
        saved_stamp_image = selectstampimage.objects.get(merchant_business_id = merchant_business_id, merchant_user = request.user).m_select_image
        selected_stamp_image = merchantstampupload.objects.filter(id = saved_stamp_image)

        for stamp in selected_stamp_image:
            stamp_data.append({
                "id" : stamp.id,
                "stamp_name": stamp.stamp_name,
                "stamp_content" : "",
                "option_color" : "",
                "selection_design" : "",
                "type":'ownstamps',
                })
    except:
        selected_stamp_image = ''

    # print('22222222211',saved_stamp_record1)
        
    if request.method == "POST":
        # print('hoy n salya')

        if request.POST.get("create_form_btn") == "save_receipt_btn":


            # selected_receipt_stamp = save_stamp_for_receipt.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)
            # saved_stamp_for_receipt = usereceiptrstamp.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)
            # try:
            #     if selected_receipt_stamp[0].stamp_id_cashmemo:
            #         stamp_data_id = selected_receipt_stamp[0].stamp_id_cashmemo
            #         is_stamp_type = 1                

            #     elif saved_stamp_for_receipt[0].stamp_image_id:
            #         stamp_data_id = saved_stamp_for_receipt[0].stamp_image_id
            #         is_stamp_type = 2

            #     elif not selected_receipt_stamp[0].stamp_id_cashmemo:
            #         if not saved_stamp_for_receipt[0].stamp_image_id:
            #             stamp_data_id = ''
            #             is_stamp_type = 0
            # except:
            #     stamp_data_id = ''
            #     is_stamp_type = 0

            stamp_selected = request.POST.get('stamp_type')

            if stamp_selected == "merchant_stamp":
                is_stamp_type = 1
                stamp_data_id = request.POST.get('default_selected_stamp')
            elif stamp_selected == "own_stamp":
                is_stamp_type = 2
                stamp_data_id = request.POST.get('own_selected_stamp')
            else:
                is_stamp_type == ''
                stamp_data_id == ''


            form = CustomerReceiptdetailsForm(request.POST,request.FILES)

            if form.is_valid():
        
                try:
                    receipt = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_id).last()
                except:
                    receipt = ""

                if not receipt:
                    receipt_no =  str("01").zfill(3)

                else:
                    last_receipt = receipt.receipt_no
                    no = int(last_receipt) + 1
                    receipt_no =  str(no).zfill(3)

                mobile_number = request.POST.get('mobile_number') 
                cash_received_from = request.POST.get('cash_received_from')
                
                # rs = request.POST.get('rs')
                amount_for = request.POST.get('amount_for')
                date = request.POST.get('date')
                # date = datetime.date.today()
                template_choice = request.POST.get('template_choice')
                total = request.POST.get('total')
                received_in_cash = request.POST.get('cash')
                print('received_in_cash',received_in_cash)
                received_in_cheque = request.POST.get('cheque'),
                received_in_other = request.POST.get('other'),
               
                term_and_condition1 = request.POST.get('term_and_condition1')
                term_and_condition2 = request.POST.get('term_and_condition2')
                term_and_condition3 = request.POST.get('term_and_condition3')

                selected_template = request.POST.get('selected_template')
                # authorised = request.FILES['authorised_sign']
                authorised = sign
                
                
                p = inflect.engine()
                print(total)
                rs = p.number_to_words(total)
                print("**********************")
                print(rs)
                result = CustomerReceiptDetailsModels.objects.create(merchant_business_id = merchant_business_id,
                merchant_user=request.user,
                receipt_no = receipt_no,
                mobile_number = mobile_number,

                cash_received_from = cash_received_from,
                rs = rs,
                amount_for = amount_for,
                date = date, 
                template_choice = selected_template, 
                total = total,
                received_in_cash=received_in_cash,
                received_in_cheque=received_in_cheque,
                received_in_other=received_in_other,
                authorised_sign=authorised,
                term_and_condition1 = term_and_condition1,
                term_and_condition2 = term_and_condition2,
                term_and_condition3 = term_and_condition3, 
                stamp_last_record = stamp_data_id,
                is_stamp_type = is_stamp_type,   
                )
                
                letters = string.ascii_letters
                digit = string.digits
                random_string = str(result.id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                
                result.receipt_url = random_string

                result.save()

                context['created_status'] = "1"

                sweetify.success(request, title="Success", icon="success", text= "Receipt Created Successfully", timer = 1500)

            else:
                sweetify.error(request, title="Error", icon='error', text='Failed to Create !!!', timer=1500)


    if request.POST.get("submit_btn") == "filter_btn":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        object_list = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_id,  date__range=(from_date,to_date)).order_by("-id")
        object_list_count = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_id, date__range=(from_date,to_date)).count()
        object_reject_count = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_id, rejected_receipt= True ,date__range=(from_date,to_date)).count()
        total_cost_receipt = 0
        for object1 in object_list:
            if object1.total and object1.rejected_receipt == False:
                total_cost_receipt = float(object1.total) + float(total_cost_receipt)

    else:
        object_list = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_id).order_by("-id")
        object_list_count = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_id).count()
        object_reject_count = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_id, rejected_receipt = True).count()
        total_cost_receipt = 0
        from_date = ''
        to_date = ''
        for object1 in object_list:
            if object1.total and  object1.rejected_receipt == False:
                total_cost_receipt = float(object1.total) + float(total_cost_receipt)
    
    # object_list = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_id.id).order_by("-id")

    merchant_users_object = Merchant_users.objects.get(user_id = request.user)
   
    form = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = 1)

    for receipt in object_list:
        receipt.tax_amount = 0.18*float(receipt.total) + float(receipt.total)
    
    try:
        latest_term_condition = CustomerReceiptDetailsModels.objects.filter(merchant_business_id = merchant_business_id).last()
        first_condition = latest_term_condition.term_and_condition1
        second_condition = latest_term_condition.term_and_condition2
        third_condition = latest_term_condition.term_and_condition3
    except:
        first_condition = ""
        second_condition = ""
        third_condition = ""

    try:
        template_selected1 = save_template_for_receipt.objects.filter(merchant_user = request.user).last()
        template_selected = template_selected1.template
    except:
        template_selected = ''

    
    check_receipt_stamp = save_stamp_for_receipt.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)
    stamp_checked_id = ''
    # try:
    selected_receipt_stamp = save_stamp_for_receipt.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)
    for receipt_stamp in check_receipt_stamp:
        if receipt_stamp.stamp_id_cashmemo:
            stamp_checked_id = int(receipt_stamp.stamp_id_cashmemo)

    try:
        saved_stamp_for_receipt = usereceiptrstamp.objects.get(merchant_user = request.user, merchant_business_id = merchant_business_id).stamp_image_id
        
    except:
        saved_stamp_for_receipt  = ''

    try:
        stamp_img_receipt = usereceiptrstamp.objects.get(merchant_user = request.user, merchant_business_id = merchant_business_id).stamp_image_id

    except:
        stamp_img_receipt = ''
    # except:
    #     stamp_checked_id = ''
    context['saved_stamp_for_receipt'] = saved_stamp_for_receipt
    context['stamp_img_receipt'] = stamp_img_receipt
    context['first_condition'] = first_condition
    context['selected_stamp_image'] = selected_stamp_image
    context['second_condition'] = second_condition
    context['third_condition'] = third_condition
    context['latest_stamp_record'] = stamp_data
    context['stamp_checked_id'] = stamp_checked_id
    context['object'] = object_list
    context['form'] = form
    context['sign'] = sign
    context['counter'] = counter
    context['saved_stamp_record1'] = saved_stamp_record1
    context['template_selected'] = template_selected
    context['object_list_count'] = object_list_count
    context['object_reject_count'] = object_reject_count
    context['total_cost_receipt'] = total_cost_receipt
    context['from_date'] = from_date
    context['to_date'] = to_date
    context['CashmemosNaveClass'] = "active"
    context['cashmemoCollapseShow'] = "show"
    context['ReceiptsNavClass'] = "active"
    
    return render(request, "merchant/merchant_cash_memo_design/merchant_receipts.html", context)

def save_receipt_template(request):
    if request.method == 'POST':
        selected_template = request.POST['template_choice'] 

        result=save_template_for_receipt.objects.create(merchant_user=request.user, template=selected_template)
        
    if result:
        sweetify.success(request, title="Success", icon='success', text='Template Added Successfully.', timer=1500)
    else:
        sweetify.success(request, title="Oops...",icon='error', text='Fail to Add.', timer=1000)
        
    return redirect(view_all_receipts)    


def ReceiptSendWebSms(request, id):

    mer_user_id = Merchant_users.objects.get(user_id=request.user)

    merchant_object = mer_user_id.merchant_user_id
    
    merchant_business_object = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    merchant_business_id = merchant_business_object.id

    subscription_object = getActiveSubscriptionPlan(request, merchant_business_id)

    if request.POST and subscription_object:
        if subscription_object.total_amount_avilable and subscription_object.per_bill_cost:

            if float(subscription_object.total_amount_avilable) >= float(subscription_object.per_bill_cost):

                id = id
                receipt_object = CustomerReceiptDetailsModels.objects.get(id = id)
                letters = string.ascii_letters
                digit = string.digits
                random_string = str(id) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
                
                receipt_object.receipt_url = random_string
                receipt_object.save()

                mobile_number = request.POST.get('mobile_number')
                db_table = request.POST.get('db_table')
                #receipt_url = ""

                receipt_url = "http://157.230.228.250/receipt/" + str(random_string) + "/"

                s = pyshorteners.Shortener()
                short_url = s.tinyurl.short(receipt_url)


                device = DeviceId.objects.filter(mobile_no=mobile_number, user_type='customer').first()
                push_service = FCMNotification(api_key=settings.API_KEY)

                if device != None:
                    registration_id = device.device_id

                    message_title = "Receiving New Receipt"

                    message_body = "You have received a Payment Receipt from . " + str(receipt_object.merchant_business_id.m_business_name) + str(receipt_url)

                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

                    total_amount_avilable_new = 0
                    total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_digital_bill_cost)
                    subscription_object.total_amount_avilable = total_amount_avilable_new
                    subscription_object.save()

                    return JsonResponse({'status':'success', 'message': 'Notification send successfully'}, status=200)

                else:
                    if mobile_number:

                        # receipt_url = "http://157.230.228.250/receipt/" + str(random_string) + "/"

                        # s = pyshorteners.Shortener()
                        # short_url = s.tinyurl.short(receipt_url)

                        ts = int(time.time())

                        data_temp = {
                                "keyword":"Cash Receipt",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Hey Green Bill user to view or download your receipt click on link " + short_url,
                                            "OA":"GBBILL",
                                            "MSISDN": str(mobile_number), # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098384997217", # Template Id
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
                            return JsonResponse({"success": True, "status": "success"})
                        else:
                            return JsonResponse({"success": False, "status": "error", "message": "Fail to send SMS !!!"})
                    else:
                        return JsonResponse({"success": False, "status": "error", "message": "Fail to send SMS !!!"})
            else:
                return JsonResponse({"success": False, "status": "error", "message":"Insufficient Balance. Please purchase new plan and try again !!!"})
    
        else:
            return JsonResponse({"success": False, "status": "error", "message":"Insufficient Balance. Please purchase new plan and try again !!!"})

    else:
        return JsonResponse({"success": False, "status": "error", "message":"You don't have active Green Bill Subscription. Please purchase and try again."})

def receipt(request, id):
    try:
        memo_record = CustomerReceiptDetailsModels.objects.filter(receipt_url=id)
        receipt_details = CustomerReceiptDetailsModels.objects.get(receipt_url=id)   

        merchant_user_id = receipt_details.merchant_business_id.id     

        selected_template1 = save_template_for_receipt.objects.filter(merchant_user=merchant_user_id).last()

        try:
            selected_template = selected_template1.template
        except:
            selected_template = ""
   
        form = MerchantProfile.objects.get(id = receipt_details.merchant_business_id.id)

        # if receipt_details.stamp_last_record:
        #     latest_stamp_record = wstampmodels.objects.filter(id=receipt_details.stamp_last_record)
        # else:
        #     latest_stamp_record = ''

        latest_stamp_record=""
        stamp_uploaded_image = ''
        if receipt_details.is_stamp_type == '1':
            if receipt_details.stamp_last_record:
                latest_stamp_record = wstampmodels.objects.filter(id=receipt_details.stamp_last_record)
                
        elif receipt_details.is_stamp_type == '2':
            if receipt_details.stamp_last_record:
                stamp_uploaded_image = merchantstampupload.objects.filter(id = receipt_details.stamp_last_record)
        else:
            pass

        authorise = authorised_sign.objects.all()
        auth = ''
        sign = ''
        for auth in authorise:
            auth = auth.selection

        if form.m_digital_signature:
            sign = form.m_digital_signature
        else:
            sign = ''


        try:
            bill_design = bill_designs.objects.get(merchant_business_id = form)
        except:
            bill_design = ''

        try:
            merchant_business_object = MerchantProfile.objects.get(id = form)

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

        ads_image_details = ""


        space = ads_below_bill.objects.filter(merchant = form.m_user, merchant_business_id = form, ads_type='green_bill').last()

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
                third_party_status = ads_below_bill.objects.filter(merchant = form.m_user, merchant_business_id = form, ads_type='third_party', status = 1).last()
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
                ads_details = ads_below_bill.objects.filter(merchant = form.m_user, merchant_business_id = form, active_ads = True).last()
                if ads_details:
                    ads_image_details = ads_below_bill.objects.get(id = ads_details.id)
                    green_bills_advertisement = True
                    views = ads_below_bill.objects.get(id=ads_details.id)
                    views.count = views.count + 1
                    views.save()
        except:
            ads_image_details = ""

        business_logo = form.m_business_logo


        context = {
            'bill_design':bill_design,
            'business_logo': business_logo,
            'business_address':business_address,
            'ads_image_details':ads_image_details,
            'template_selected': selected_template,
            'receipt_details' : receipt_details,
            'latest_stamp_record': latest_stamp_record,
            'stamp_uploaded_image': stamp_uploaded_image,
            'memo_record': memo_record, 
            # 'receipt_details': receipt_details,
            # 'merchant_user_id':'Yaman',
            'sign': sign,
            'form': form,
        }

        return render(request, "merchant/merchant_cash_memo_design/receipt.html", context)

    except:
        return render(request, 'page-404.html')


def delete_receipt(request, id):

    coupon_obj = CustomerReceiptDetailsModels.objects.get(id=id).delete()

    if coupon_obj:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


def saved_cashmemo_stamp_by_id(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    cashmemo = usecashmemostamp.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)

    if request.method == 'POST':
        stamp_image_id = request.POST['img_id']

        if cashmemo:
            usecashmemostamp.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id).update(stamp_image_id = stamp_image_id)

        else:
            usecashmemostamp.objects.create(merchant_user = request.user, merchant_business_id = merchant_business_id, stamp_image_id = stamp_image_id)

        sweetify.success(request, title="Success", icon='success', text='Stamp saved Successfully.', timer=1500)

    return redirect(view_all_cash_memo)


def uncheck_cashmemo_stamp_by_id(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    cashmemo = usecashmemostamp.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)
    stamp_image_id = ''
    
    if receipt:
        if cashmemo[0].stamp_image_id:
            usecashmemostamp.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id).update(stamp_image_id = stamp_image_id)
            sweetify.success(request, title="Success", icon='success', text='Stamp Uncheck Successfully.', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Already Unselected', timer=1500)

    else:
        sweetify.error(request, title="Error", icon='error', text='Saved stamp first', timer=1500)

    return redirect(view_all_cash_memo)

def saved_receipt_stamp_by_id(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    receipt = usereceiptrstamp.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)

    if request.method == 'POST':
        stamp_image_id = request.POST['img_id']

        if receipt:
            usereceiptrstamp.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id).update(stamp_image_id = stamp_image_id)

        else:
            usereceiptrstamp.objects.create(merchant_user = request.user, merchant_business_id = merchant_business_id, stamp_image_id = stamp_image_id)

        sweetify.success(request, title="Success", icon='success', text='Stamp saved Successfully.', timer=1500)

    return redirect(view_all_receipts)

def  uncheck_receipt_stamp_by_id(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    receipt = usereceiptrstamp.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)
    stamp_image_id = ''
    
    if receipt:
        if receipt[0].stamp_image_id:
            usereceiptrstamp.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id).update(stamp_image_id = stamp_image_id)
            sweetify.success(request, title="Success", icon='success', text='Stamp Uncheck Successfully.', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Already Unselected', timer=1500)

    else:
        sweetify.error(request, title="Error", icon='error', text='Saved stamp first', timer=1500)

    return redirect(view_all_receipts)


def RejectCashMemoBill(request):
    cash_memo_url = ''
    if request.method == 'POST':
        bill_id = request.POST['bill_id']

        rejectbillRadio = request.POST['rejectbillRadio']

        result = CustomerCashMemoDetailModels.objects.filter(id = bill_id).update(rejected_cash_memo = True, rejected_reason = rejectbillRadio)

        cash_memo_url = CustomerCashMemoDetailModels.objects.get(id = bill_id).memo_url

        if result:
            sweetify.success(request, title="Success", icon='success', text='Cash Memo Rejected Successfully.', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Something went wrong', timer=1500)
    else:
        sweetify.error(request, title="Error", icon='error', text='Something went wrong', timer=1500)

    return HttpResponseRedirect('/cash-memo/'+str(cash_memo_url)+'/')

def RejectReceiptBill(request):
    receipt_memo_url = ''
    if request.method == 'POST':
        bill_id = request.POST['bill_id']

        rejectbillRadio = request.POST['rejectbillRadio']

        result = CustomerReceiptDetailsModels.objects.filter(id = bill_id).update(rejected_receipt = True, rejected_reason = rejectbillRadio)

        receipt_memo_url = CustomerReceiptDetailsModels.objects.get(id = bill_id).receipt_url

        if result:
            sweetify.success(request, title="Success", icon='success', text='Receipt Rejected Successfully.', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Something went wrong', timer=1500)
    else:
        sweetify.error(request, title="Error", icon='error', text='Something went wrong', timer=1500)

    return HttpResponseRedirect('/receipt/'+str(receipt_memo_url)+'/')

def ViewCustomerCashMemo(request):
    cash_memo_list = CustomerCashMemoDetailModels.objects.filter(mobile_number = request.user, rejected_cash_memo = False).order_by('-id')
    cash_memo_count = CustomerCashMemoDetailModels.objects.filter(mobile_number = request.user, rejected_cash_memo = False).count()
    total_cost_cashmemo = 0
    for cash_memo in cash_memo_list:
        total_cost_cashmemo = float(cash_memo.total) + float(total_cost_cashmemo) 
    context = {
        'data': cash_memo_list,
        'cash_memo_count': cash_memo_count,
        'total_cost_cashmemo': total_cost_cashmemo,
        'CsutomerCashmemosNaveClass': "active", 
        'CustomercashmemoCollapseShow': "show",
        'CustomerCashMemoNavClass': "active",
    }
    return render(request, "customer/customer_cash_memo&receipt/customer-cashmemo.html", context)


def ViewCustomerReceipts(request):
    receipt_list = CustomerReceiptDetailsModels.objects.filter(mobile_number = request.user, rejected_receipt = False).order_by('-id')
    total_receipt= CustomerReceiptDetailsModels.objects.filter(mobile_number = request.user, rejected_receipt = False).count()
    total_cost_receipt = 0
    for receipt in receipt_list:
        total_cost_receipt = float(receipt.total) + float(total_cost_receipt)
    context = {
        'data': receipt_list,
        'total_receipt':total_receipt,
        'total_cost_receipt':total_cost_receipt,
        'CsutomerCashmemosNaveClass': "active", 
        'CustomercashmemoCollapseShow': "show",
        'CustomerReceiptsNavClass': "active",
    }
    return render(request, "customer/customer_cash_memo&receipt/customer-receipt.html", context)

def SaveAndUpdateCashMemoTemplate(request):
    selected_template = request.POST['selected_template']
    result = save_template_for_cashmemo.objects.filter(merchant_user = request.user).last()
    if result:
        save_template_for_cashmemo.objects.filter(id = result.id).update(template = selected_template)
        sweetify.success(request, title="Success", icon='success', text='Template Updated Successfully.', timer=1500)
    else:
        save_template_for_cashmemo.objects.create(merchant_user = request.user, template = selected_template)
        sweetify.success(request, title="Success", icon='success', text='Template Added Successfully.', timer=1500)

    return redirect(CashMemoReceiptSettings)

def SaveAndUpdateReceiptTemplate(request):
    template_choice = request.POST['template_choice']
    result = save_template_for_receipt.objects.filter(merchant_user = request.user).last()
    if result:
        save_template_for_receipt.objects.filter(id = result.id).update(template = template_choice)
        sweetify.success(request, title="Success", icon='success', text='Template Updated Successfully.', timer=1500)
    else:
        save_template_for_receipt.objects.create(merchant_user = request.user, template = template_choice)
        sweetify.success(request, title="Success", icon='success', text='Template Added Successfully.', timer=1500)

    return redirect(CashMemoReceiptSettings)

def CashMemoReceiptSettings(request):

    cashmemotemplate = save_template_for_cashmemo.objects.filter(merchant_user = request.user).last()

    template1 = ''
    if cashmemotemplate:
        if cashmemotemplate.template == '1':
            template1 = "Template 1"
        elif cashmemotemplate.template == '2':
            template1 = "Template 2"
        elif cashmemotemplate.template == '3':   
            template1 = "Template 3" 

    receipttemplate = save_template_for_receipt.objects.filter(merchant_user = request.user).last()

    template2 = ''

    if receipttemplate:
        if receipttemplate.template == '1':
            template2 = "Template 1"
        elif receipttemplate.template == '2':
            template2 = "Template 2"
        elif receipttemplate.template == '3':   
            template2 = "Template 3" 

    context = {
        'template1': template1,
        'template2': template2,
        'CashmemosNaveClass': "active", 
        'cashmemoCollapseShow': "show",
        'CashMemoSettingNavClass': "active",
    }
    return render(request, "merchant/merchant_cash_memo_design/setting1.html", context)
