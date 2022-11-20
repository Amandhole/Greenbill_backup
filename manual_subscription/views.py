import os
import random
import sweetify
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from subscription_plan.models import *
from users.models import Merchant_users, MerchantProfile, GreenBillUser, PartnerProfile
from my_subscription.models import *
from app.views import is_merchant_or_merchant_staff


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

from referral_points.models import *
from partner_my_subscription.models import *

# Create your views here.

# @login_required(login_url="/login/")
# @user_passes_test(is_superuser, login_url="/login/")
def recharge_manual_subscriptions(request):

    all_subscriptions_plans = subscription_plan_details.objects.all().filter(is_active=True).order_by('-id')

    promotional_sms_plans = promotional_subscription_plan_model.objects.all().filter(is_active=True).order_by('-id')

    transactional_sms_plans = transactional_subscription_plan_model.objects.all().filter(is_active=True).order_by('-id')

    addons_plans = add_on_plan_model.objects.all().filter(is_active=True).order_by('-id')

    merchant = MerchantProfile.objects.all().filter(m_disabled_account=False)

    transactional_merchant = transactional_subscription_plan_model.objects.all()
    promotional_merchant = promotional_subscription_plan_model.objects.all()

    merchant_names = []
    
    # for tran_plan in transactional_merchant:
    #     b_id = tran_plan.merchant_name.split(',')
    #     m_names = []
    #     for l in b_id:

    #         if l:
    #             m_name = MerchantProfile.objects.get(id=l).m_business_name
    #             m_names.append(m_name)
    #         else:
    #             m_name = None
    #             m_names.append(m_name)

    #     merchant_names.append({
    #         'merchant_names':m_names,
    #         'subscription':tran_plan.subscription_name,
    #         })




 
    context = {
        "subscriptions_list" : all_subscriptions_plans,
        "promotional_sms_plans_list" : promotional_sms_plans,
        "transactional_sms_plans_list":transactional_sms_plans,
        "addons_plans": addons_plans,
        'merchant':merchant,
        "SubscriptionNavclass": 'active',
        "SubscriptionCollapseShow": "show",
        "ManualSubscriptionNavclass": 'active',
        "transactional_merchant": transactional_merchant,
        'trans_plan':merchant_names,
        # "trans_merchant_name": transactional_merchant.merchant_name,
        "promotional_merchant": promotional_merchant,
    }
    return render(request, "super_admin/manual_subscription.html", context)

def get_merchants_by_promotional_plan_id(request):
    plan_id = request.POST['plan_id']

    promo_obj = promotional_subscription_plan_model.objects.get(id = plan_id)

    promo_obj_list = promo_obj.merchant_name.split(',')

    if promo_obj_list:
        m_names = []
        for l in promo_obj_list:
            if l:
                m_name = MerchantProfile.objects.get(id=l).m_business_name
                m_names.append({
                    'id':l,
                    'b_name':m_name,
                    })
            else:
                pass
    else:
        m_names = []

    return JsonResponse({"data":m_names})

def get_merchants_by_plan_id(request):
    plan_id = request.POST['plan_id']

    trans_obj = transactional_subscription_plan_model.objects.get(id = plan_id)

    trans_obj_list = trans_obj.merchant_name.split(',')

    if trans_obj_list:
        m_names = []
        for l in trans_obj_list:
            if l:
                m_name = MerchantProfile.objects.get(id=l).m_business_name
                m_names.append({
                    'id':l,
                    'b_name':m_name,
                    })
            else:
                pass
    else:
        m_names = []

    return JsonResponse({"data":m_names})

def Partner_recharge_manual_subscriptions(request):

    all_subscriptions_plans = subscription_plan_details.objects.all().filter(is_active=True, user_type="partner").order_by('-id')

    promotional_sms_plans = promotional_subscription_plan_model.objects.all().filter(is_active=True).order_by('-id')

    transactional_sms_plans = transactional_subscription_plan_model.objects.all().filter(is_active=True).order_by('-id')

    Partner = PartnerProfile.objects.filter(p_disabled_account = False)

    addons_plans = add_on_plan_model.objects.all().filter(is_active=True).order_by('-id')

    context = {
        "subscriptions_list" : all_subscriptions_plans,
        "promotional_sms_plans_list" : promotional_sms_plans,
        "transactional_sms_plans_list":transactional_sms_plans,
        "addons_plans": addons_plans,
        'Partner':Partner,
        "SubscriptionNavclass": 'active',
        "SubscriptionCollapseShow": "show",
        "ManualPartnerSubscriptionNavclass": 'active'
    }
    return render(request, "super_admin/partner-manual-subscription.html", context)


@csrf_exempt
def manual_subscription_purchased_success(request):
    if request.method == "POST":
        if request.POST.get('merchant_business1') != '':
            business_id = request.POST.get('merchant_business1')
        if request.POST.get('merchant_business2') != '':
            business_id = request.POST.get('merchant_business2')
        if request.POST.get('merchant_business3') != '':
            business_id = request.POST.get('merchant_business3')

        mode = request.POST.get('mode')

        print(mode)

        bank_transaction_id = request.POST.get('transaction_id')

        cheque_no = request.POST.get('cheque_no')

        total_amount = request.POST.get('amount')

        id = request.POST.get('subscription_id')

        per_users_cost = request.POST.get('per_users_cost')

        recharge_amount1 = request.POST.get('recharge_amount1')

        selected_users = request.POST.get('selected_users')

        merchant_gst = request.POST.get('merchant_gst')

        valid_for_month = request.POST.get('valid_for_month')

        amount1 = float(per_users_cost) * float(valid_for_month) * float(selected_users)

        # sub_amount = float(amount1) + float(recharge_amount1)
        sub_amount = float(recharge_amount1)
        
        if mode == 'cashwithoutbill':
            total_plan_amount = float(sub_amount) 
            gst_amount =0 
        else:
            gst_amount = (18 * float(sub_amount))/100

            total_plan_amount = float(sub_amount) + float(gst_amount)


        print("************************************************************")
        print("In form details ..................")
        print(per_users_cost,valid_for_month,selected_users)
        print(gst_amount,total_plan_amount,amount1,recharge_amount1,sub_amount,id)



        subscription_object = subscription_plan_details.objects.get(id=id)

        per_bill_cost = subscription_object.per_bill_cost
        per_digital_bill_cost = subscription_object.per_digital_bill_cost

        total_amount = float(subscription_object.recharge_amount)
        subscription_plan_cost = float(subscription_object.subscription_plan_cost)

        merchant = MerchantProfile.objects.get(id=business_id)

        merchant_object = GreenBillUser.objects.get(mobile_no = merchant.m_user)

        startswith = str(business_id) + ','
        endswith = ','+ str(business_id)
        contains = ','+ str(business_id) + ','
        exact = str(business_id)

        today = date.today()
        d1 = today.strftime("%d-%m-%Y")
        start_date = datetime.datetime.strptime(d1, "%d-%m-%Y")
        delta_period = int(valid_for_month)
        end_date = start_date + relativedelta(months=delta_period)
        expiry_date = end_date.strftime("%d-%m-%Y")
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

            # sweetify.success(request, title="Oops...", icon='error', text='You Already have .', timer=1500)

            business_ids_list_temp = list((check_subscription_available.business_ids).split(","))
            
            business_ids_list_temp.remove(business_id)

            business_ids_new = ""

            business_ids_new = ','.join(business_ids_list_temp)

            # sub_amount = float(sub_amount) + float(check_subscription_available.total_amount_avilable)
            
            update_result = merchant_subscriptions.objects.filter(id = check_subscription_available.id).update(business_ids = business_ids_new)

            get_updated_suscription = merchant_subscriptions.objects.get(id = check_subscription_available.id)

            if get_updated_suscription.business_ids == "":
                merchant_subscriptions.objects.filter(id = get_updated_suscription.id).update(is_active = False)

    subscription_active_status = True

    # if mode == "cashwithoutbill":
        # pass
        # gst_amount_cwb = 0
        # subscription =  merchant_subscriptions.objects.create(
        #     subscription_id = subscription_object.id,
        #     subscription_name = subscription_object.subscription_name,
        #     merchant_id = merchant_object,
        #     business_ids = business_id,

        #     valid_for_month = valid_for_month,

        #     per_bill_cost = per_bill_cost,

        #     per_digital_bill_cost = per_digital_bill_cost,

        #     recharge_amount = total_plan_amount,
        #     total_amount_avilable = sub_amount,
        #     is_active = subscription_active_status,

        #     gst_amount = gst_amount,
        #     no_of_users = selected_users,

        #     purchase_cost = subscription_plan_cost,
        #     expiry_date = expiry_date,
        # )
    # else:
    subscription =  merchant_subscriptions.objects.create(
            subscription_id = subscription_object.id,
            subscription_name = subscription_object.subscription_name,
            merchant_id = merchant_object,
            business_ids = business_id,

            valid_for_month = valid_for_month,

            per_bill_cost = per_bill_cost,

            per_digital_bill_cost = per_digital_bill_cost,

            recharge_amount = total_plan_amount,
            total_amount_avilable = sub_amount,
            is_active = subscription_active_status,

            gst_amount = gst_amount,
            no_of_users = selected_users,

            purchase_cost = subscription_plan_cost,
            expiry_date = expiry_date,
    )

    
    last_id = recharge_history.objects.filter().last()
    try:
        invoice_no = 'GB' + str(last_id.id+1)
    except:
        invoice_no = 'GB' + str(1+1)
    print(last_id)

    if 1==2:
        pass
    else:
        recharge_history.objects.create(
            subscription_plan_id = subscription_object.id,
            subscription_name = subscription_object.subscription_name,
            merchant_id = merchant_object,
            business_ids = business_id,

            valid_for_month = valid_for_month,

            per_bill_cost = per_bill_cost,

            per_digital_bill_cost = per_digital_bill_cost,

            cost = subscription_plan_cost,
            no_of_users = selected_users,
            gst_amount = merchant_gst,
            is_subscription_plan = True,
            expiry_date = expiry_date,
            mode = mode,
            cheque_no = cheque_no,
            bank_transaction_id = bank_transaction_id,
            # payu_transaction_id = mihpayid,
            invoice_no = invoice_no
                )
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    print(sub_amount,total_plan_amount)
    if subscription:
        sweetify.success(request, title="Success", icon='success', text='Subscription purchased Successfully.', timer=1500)
        return redirect(recharge_manual_subscriptions)

    else:
        sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

        return redirect(recharge_manual_subscriptions)

@csrf_exempt
def manual_promotional_sms_subscription_purchased_success(request):

    if request.method == "POST":
        business_id = request.POST.get('merchant_business')
        mode = request.POST.get('mode')
        bank_transaction_id = request.POST.get('transaction_id')
        cheque_no = request.POST.get('cheque_no')
        total_amount = request.POST.get('amount')
        id = request.POST.get('subscription_id1')
        print(id)
        # subscription_object = subscription_plan_details.objects.get(id=id)
        subscription_object = promotional_subscription_plan_model.objects.get(id=id)
        merchant = MerchantProfile.objects.get(id=business_id)
        merchant_object = GreenBillUser.objects.get(mobile_no = merchant.m_user)

        total_sms = subscription_object.total_sms
        per_sms_cost = subscription_object.per_sms_cost
        total_sms_cost = float(subscription_object.total_sms_cost)
        subscription_plan_cost = float(subscription_object.total_sms_cost)
        total_sms_avilable = total_sms

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
            # subscription_id = subscription_object.id,
            # subscription_name = subscription_object.subscription_name,
            # merchant_id = merchant_object,
            # business_ids = business_id,

            # total_sms = subscription_object.total_sms,
            # per_sms_cost = subscription_object.per_sms_cost,

            # total_sms_avilable = subscription_object.total_sms_avilable,

            is_active = subscription_active_status,
            # purchase_cost = subscription_object.subscription_plan_cost,

            subscription_id = subscription_object.id,
            subscription_name = subscription_object.subscription_name,
            merchant_id = merchant_object,
            business_ids = business_id,

            total_sms = total_sms,
            per_sms_cost = per_sms_cost,

            total_sms_avilable = total_sms_avilable,
            purchase_cost = subscription_plan_cost,
            
            # transaction_id = txnid,
            # payu_transaction_id = mihpayid,
        )

        last_id = recharge_history.objects.filter().last()
        try:
            invoice_no = 'GB' + str(last_id.id+1)
        except:
            invoice_no = 'GB' + str(1+1)
        if 1==2:
            pass
        else:
            recharge_history.objects.create(
                # subscription_plan_id = subscription_object.id,
                # subscription_name = subscription_object.subscription_name,
                # merchant_id = merchant_object,
                # business_ids = business_id,

                # total_sms = subscription_object.total_sms,
                # per_sms_cost = subscription_object.per_sms_cost,

                # cost = subscription_object.subscription_plan_cost,
                mode = mode,
                cheque_no = cheque_no,
           		bank_transaction_id = bank_transaction_id,
                # payu_transaction_id = mihpayid,
                invoice_no = invoice_no,

                subscription_plan_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                merchant_id = merchant_object,
                business_ids = business_id,

                total_sms = total_sms,
                per_sms_cost = per_sms_cost,

                cost = subscription_plan_cost,

                is_promotional_sms_plan = True,
            )

        if subscription:
            sweetify.success(request, title="Success", icon='success', text='Promotional plan purchased Successfully.', timer=1500)
            return redirect(recharge_manual_subscriptions)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

            return redirect(recharge_manual_subscriptions)

    else:
        sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

        return redirect(recharge_manual_subscriptions)


@csrf_exempt
def manual_transactional_sms_subscription_purchased_success(request):


	
    if request.method == "POST":
        business_id = request.POST.get('merchant_business')
        mode = request.POST.get('mode')
        bank_transaction_id = request.POST.get('transaction_id')
        cheque_no = request.POST.get('cheque_no')
        total_amount = request.POST.get('amount')

        id = request.POST.get('subscription_id2')

        subscription_object = transactional_subscription_plan_model.objects.get(id=id)
        merchant = MerchantProfile.objects.get(id=business_id)
        merchant_object = GreenBillUser.objects.get(mobile_no = merchant.m_user)

        total_sms = subscription_object.total_sms
        per_sms_cost = subscription_object.per_sms_cost
        total_sms_cost = float(subscription_object.total_sms_cost)
        subscription_plan_cost = float(subscription_object.total_sms_cost)
        total_sms_avilable = total_sms

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
            # subscription_id = subscription_object.id,
            # subscription_name = subscription_object.subscription_name,
            # merchant_id = merchant_object,
            # business_ids = business_id,
            # total_sms = subscription_object.total_sms,
            # per_sms_cost = subscription_object.per_sms_cost,
            #total_sms_avilable = subscription_object.total_sms_avilable,

            # is_active = subscription_active_status,
            # purchase_cost = subscription_object.subscription_plan_cost,
            
            # transaction_id = transaction_id,
            # payu_transaction_id = mihpayid,
            subscription_id = subscription_object.id,
            subscription_name = subscription_object.subscription_name,
            merchant_id = merchant_object,
            business_ids = business_id,

            total_sms = total_sms,
            per_sms_cost = per_sms_cost,

            total_sms_avilable = total_sms_avilable,

            is_active = subscription_active_status,
            purchase_cost = subscription_plan_cost,
        )
        last_id = recharge_history.objects.filter().last()
        try:
            invoice_no = 'GB' + str(last_id.id+1)
        except:
            invoice_no = 'GB' + str(1+1)
        if mode == 'cashwithoutbill':
            pass 
        else:
            recharge_history.objects.create(
                # subscription_plan_id = subscription_object.id,
                # subscription_name = subscription_object.subscription_name,
                # merchant_id = merchant_object,
                # business_ids = business_id,

                # total_sms = subscription_object.total_sms,
                # per_sms_cost = subscription_object.per_sms_cost,

                # cost = subscription_object.subscription_plan_cost,
                mode = mode,
                cheque_no = cheque_no,
           		bank_transaction_id = bank_transaction_id,
                # transaction_id = transaction_id,
                # payu_transaction_id = mihpayid,
                invoice_no = invoice_no,

                subscription_plan_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                merchant_id = merchant_object,
                business_ids = business_id,

                total_sms = total_sms,
                per_sms_cost = per_sms_cost,

                cost = subscription_plan_cost,

                is_transactional_sms_plan = True,
            )

        if subscription:
            sweetify.success(request, title="Success", icon='success', text='Transactional plan purchased Successfully.', timer=1500)
            return redirect(recharge_manual_subscriptions)

        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

            return redirect(recharge_manual_subscriptions)
    # else:

    #     sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)
    #     return redirect(recharge_manual_subscriptions)


@csrf_exempt
def manual_add_on_subscription_purchased_success(request):

    
    if request.method == "POST":
        business_id = request.POST.get('merchant_business')
        mode = request.POST.get('mode')
        bank_transaction_id = request.POST.get('transaction_id')
        cheque_no = request.POST.get('cheque_no')
        total_amount = request.POST.get('amount')
        adon_amounts_value = request.POST.get('adon_amounts_value')


        gst_amount = (18*float(adon_amounts_value))/100

        id = request.POST.get('subscription_id3')

        subscription_object = add_on_plan_model.objects.get(id=id)
        merchant = MerchantProfile.objects.get(id=business_id)
        merchant_object = GreenBillUser.objects.get(mobile_no = merchant.m_user)
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

        print(check_subscription_available)

        if check_subscription_available:

            total_amount = float(check_subscription_available.total_amount_avilable) + float(adon_amounts_value)

            subscription =  merchant_subscriptions.objects.filter(id = check_subscription_available.id).update(

                total_amount_avilable = total_amount,
                gst_amount = subscription_object.gst_amount,

            )
            last_id = recharge_history.objects.filter().last()
            try:
                invoice_no = 'GB' + str(last_id.id+1)
            except:
                invoice_no = 'GB' + str(1+1)

            if mode =='cashwithoutbill':
                pass 
            else:
                recharge_history.objects.create(

                    is_add_on_plan = True,
                    mode = mode,
                    cheque_no = cheque_no,
            		bank_transaction_id = bank_transaction_id,
                    # payu_transaction_id = mihpayid,
                    invoice_no = invoice_no,


                    subscription_plan_id = subscription_object.id,
                    subscription_name = subscription_object.add_on_name,
                    merchant_id = merchant_object,
                    business_ids = business_id,
                    cost = adon_amounts_value,
                    gst_amount = gst_amount,

                )

            if subscription:
                sweetify.success(request, title="Success", icon='success', text='Add On purchased Successfully.', timer=1500)
                return redirect(recharge_manual_subscriptions)

        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

            return redirect(recharge_manual_subscriptions)
    else:

        sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)
        return redirect(recharge_manual_subscriptions)


def GetMerchantAdressForGst(request):
    business_id = request.POST.get("merchant_business")
    merchant_business_object = MerchantProfile.objects.get(id = business_id)
    merchant_state = merchant_business_object.m_state

    if merchant_state == "Maharashtra":
        state_object = 1
    else:
        state_object = 2

    print(state_object)

    return JsonResponse({"data":state_object})


@csrf_exempt
def manual_partnerpromotional_sms_subscription_purchased_success(request):

    if request.method == "POST":
        partner_number = request.POST.get('partner_number')
        mode = request.POST.get('mode')
        bank_transaction_id = request.POST.get('transaction_id')
        cheque_no = request.POST.get('cheque_no')
        total_amount = request.POST.get('amount')
        id = request.POST.get('subscription_id1')
        subscription_object = promotional_subscription_plan_model.objects.get(id=id)
        partner_object = GreenBillUser.objects.get(mobile_no = partner_number)

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
        )

        try:
            last_id = partner_recharge_history.objects.filter().last()
            invoice_no = 'GB' + str(last_id.id+1)
        except:
            invoice_no = 'GB' + str(1)

        if mode =='cashwithoutbill':
            pass 
        else:
            partner_recharge_history.objects.create(

                subscription_plan_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name, 
                partner_id = partner_object,

                total_sms = total_sms,
                per_sms_cost = per_sms_cost,

                cost = subscription_plan_cost,

                is_promotional_sms_plan = True,

                mode = mode,
                cheque_no = cheque_no,
                bank_transaction_id = bank_transaction_id,
                invoice_no =invoice_no,
            )

        if subscription:
            sweetify.success(request, title="Success", icon='success', text='Promotional plan purchased Successfully.', timer=1500)
            return redirect(Partner_recharge_manual_subscriptions)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

            return redirect(Partner_recharge_manual_subscriptions)

    else:
        sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

        return redirect(Partner_recharge_manual_subscriptions)


@csrf_exempt
def manual_partner_Transactional_sms_subscription_purchased_success(request):

    if request.method == "POST":
        partner_number = request.POST.get('partner_number')
        mode = request.POST.get('mode')
        bank_transaction_id = request.POST.get('transaction_id')
        cheque_no = request.POST.get('cheque_no')
        total_amount = request.POST.get('amount')
        id = request.POST.get('subscription_id2')
        subscription_object = transactional_subscription_plan_model.objects.get(id=id)
        partner_object = GreenBillUser.objects.get(mobile_no = partner_number)

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
        )

        try:
            last_id = partner_recharge_history.objects.filter().last()
            invoice_no = 'GB' + str(last_id.id+1)
        except:
            invoice_no = 'GB' + str(1)

        if mode =='cashwithoutbill':
            pass 
        else:
            partner_recharge_history.objects.create(
                subscription_plan_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name, 
                partner_id = partner_object,

                total_sms = total_sms,
                per_sms_cost = per_sms_cost,

                cost = subscription_plan_cost,

                is_transactional_sms_plan = True,

                mode = mode,
                cheque_no = cheque_no,
                bank_transaction_id = bank_transaction_id,
                invoice_no = invoice_no,

            )


        if subscription:
            sweetify.success(request, title="Success", icon='success', text='Transactional plan purchased Successfully.', timer=1500)
            return redirect(Partner_recharge_manual_subscriptions)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

            return redirect(Partner_recharge_manual_subscriptions)

    else:
        sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

        return redirect(Partner_recharge_manual_subscriptions)


@csrf_exempt
def manual_partner_GreenBill_subscription_purchased_success(request):
    if request.method == "POST":
        partner_number = request.POST['partner_number']
        valid_for_month = request.POST['valid_for_month']
        plan_total_amount = request.POST['plan_total_amount']
        green_bill_gst_amount = request.POST['green_bill_gst_amount']
        # recharge_amountq = request.POST['plan_recharge_amount']
        subscription_id = request.POST['subscription_plan_id']
        green_bill_recharge_amount = request.POST['green_bill_recharge_amount']
        mode = request.POST.get('mode')
        bank_transaction_id = request.POST.get('transaction_id')
        cheque_no = request.POST.get('cheque_no')
        
        print("****************-----------------------------------------------*************************")
        # print(recharge_amountq)
        print(green_bill_recharge_amount)
        print(plan_total_amount)
        if mode =='cashwithoutbill':
            total_amount = float(green_bill_recharge_amount) 
            plan_total_amount = float(plan_total_amount) 
        else:

            total_amount = float(green_bill_recharge_amount) 

        partner_object = GreenBillUser.objects.get(mobile_no = partner_number)

        subscription_object = subscription_plan_details.objects.get(id=subscription_id)

        try:
            check_subscription_available = partner_subscriptions.objects.get(partner_id = partner_object, is_active = True)
        except:
            check_subscription_available = ""

        if check_subscription_available:
            partner_subscriptions.objects.update(partner_id = partner_object, is_active = False)
            
            # total_amount = float(total_amount) + float(check_subscription_available.total_amount_avilable)


        subscription_active_status = True

        today = date.today()
        d1 = today.strftime("%d-%m-%Y")
        start_date = datetime.datetime.strptime(d1, "%d-%m-%Y")
        delta_period = int(valid_for_month)
        end_date = start_date + relativedelta(months=delta_period)
        expiry_date = end_date.strftime("%d-%m-%Y")

        if mode =='cashwithoutbill':
            subscription =  partner_subscriptions.objects.create(
                        
                subscription_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                partner_id = partner_object, 

                valid_for_month = valid_for_month,

                per_bill_cost = subscription_object.per_bill_cost,
                per_url_cost = subscription_object.per_url_cost,
                per_digital_bill_cost = subscription_object.per_digital_bill_cost,

                total_amount_avilable = total_amount,
                is_active = subscription_active_status,
                recharge_amount = green_bill_recharge_amount,
                purchase_cost = plan_total_amount,
                expiry_date = expiry_date,

            ) 
        else:

            subscription =  partner_subscriptions.objects.create(
                        
                subscription_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name,
                partner_id = partner_object, 

                valid_for_month = valid_for_month,

                per_bill_cost = subscription_object.per_bill_cost,
                recharge_amount = green_bill_recharge_amount,
                per_url_cost = subscription_object.per_url_cost,
                per_digital_bill_cost = subscription_object.per_digital_bill_cost,

                total_amount_avilable = total_amount+ float(green_bill_gst_amount),
                is_active = subscription_active_status,

                purchase_cost = plan_total_amount,
                expiry_date = expiry_date,

            )

        try:
            last_id = partner_recharge_history.objects.filter().last()
            invoice_no = 'GB' + str(last_id.id+1)
        except:
            invoice_no = 'GB' + str(1)

        if 1==2:
            pass
        else:
            partner_recharge_history.objects.create(

                subscription_plan_id = subscription_object.id,
                subscription_name = subscription_object.subscription_name, 
                partner_id = partner_object,

                valid_for_month = valid_for_month,

                per_bill_cost = subscription_object.per_bill_cost,
                per_url_cost = subscription_object.per_url_cost,
                per_digital_bill_cost = subscription_object.per_digital_bill_cost,

                cost = plan_total_amount,

                is_subscription_plan = True,
                expiry_date = expiry_date,

                
                mode = mode,
                gst_amount = green_bill_gst_amount,
                cheque_no = cheque_no,
                bank_transaction_id = bank_transaction_id,
                invoice_no = invoice_no
            )

        

        if subscription:
            sweetify.success(request, title="Success", icon='success', text='Green Bill Subscription plan purchased Successfully.', timer=1500)
            return redirect(Partner_recharge_manual_subscriptions)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Purchase.', timer=1500)

            return redirect(Partner_recharge_manual_subscriptions)
    else:

        return redirect(Partner_recharge_manual_subscriptions)

@csrf_exempt
def manual_partner_Adon_purchased_success(request):
    if request.method == "POST":

        partner_number = request.POST['partner_number']

        partner_object = GreenBillUser.objects.get(mobile_no = partner_number)

        try:
            check_subscription_available = partner_subscriptions.objects.get(partner_id = partner_object, is_active = True)
        except:
            check_subscription_available = ""

        if check_subscription_available:

            plan_total_amount = request.POST['adon_amounts_value']

            green_bill_gst_amount = (float(plan_total_amount) * 0.18)

            subscription_id = request.POST['subscription_id3']

            mode = request.POST.get('mode')

            bank_transaction_id = request.POST.get('transaction_id')

            cheque_no = request.POST.get('cheque_no')

            # if mode == 'cashwithoutbill':
            if 1==2:
                pass

                # total_adon_plan_amount = float(plan_total_amount) + float(green_bill_gst_amount)

                # total_amount = float(check_subscription_available.total_amount_avilable) + float(plan_total_amount)

                # subscription_object = add_on_plan_model.objects.get(id=subscription_id)

                # subscription =  partner_subscriptions.objects.filter(id = check_subscription_available.id).update(

                #     per_bill_cost = subscription_object.per_bill_cost,
                #     per_digital_cash_memo_cost = subscription_object.per_digital_bill_cost,

                #     total_amount_avilable = total_amount,

                # )

                # try:
                #     last_id = partner_recharge_history.objects.filter().last()
                #     invoice_no = 'GB' + str(last_id.id+1)
                # except:
                #     invoice_no = 'GB' + str(1)

            
            else:
                total_adon_plan_amount = float(plan_total_amount) + float(green_bill_gst_amount)

                # total_amount = float(check_subscription_available.total_amount_avilable) + float(plan_total_amount)
                total_amount =  float(plan_total_amount)

                subscription_object = add_on_plan_model.objects.get(id=subscription_id)

                subscription =  partner_subscriptions.objects.filter(id = check_subscription_available.id).update(

                    per_bill_cost = subscription_object.per_bill_cost,
                    per_digital_cash_memo_cost = subscription_object.per_digital_bill_cost,

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

                per_bill_cost = subscription_object.per_bill_cost,
                
                per_digital_cash_memo_cost = subscription_object.per_digital_bill_cost,

                cost = total_adon_plan_amount,

                is_add_on_plan = True,

                mode = mode,
                gst_amount = green_bill_gst_amount,
                cheque_no = cheque_no,
                bank_transaction_id = bank_transaction_id,
                invoice_no = invoice_no

                )
            if subscription:
                sweetify.success(request, title="Success", icon='success', text='Add On purchased Successfully.', timer=1500)
            else:
                sweetify.success(request, title="Oops...", icon='error', text="Something went wrong .", timer=1500)
            return redirect(recharge_manual_subscriptions)

        else:
            sweetify.success(request, title="Oops...", icon='error', text="You don't have Green Bill Subscription Plan .", timer=1500)
            return redirect(recharge_manual_subscriptions)
    else:
        sweetify.success(request, title="Oops...", icon='error', text="You don't have Green Bill Subscription Plan .", timer=1500)
        return redirect(recharge_manual_subscriptions)