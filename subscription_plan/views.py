from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.http import HttpResponse, JsonResponse
from .models import *
import sweetify
from users.models import MerchantProfile
from category_and_tags.models import business_category
from users.models import GreenBillUser
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner


from my_subscription.models import *
from subscription_plan.models import *
from datetime import date
import time
import datetime
from datetime import date



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def view_subscription_status(request, subscription_name):
    check_plan = merchant_subscriptions.objects.filter(subscription_name=subscription_name, is_active=True)
    check_plan_count = merchant_subscriptions.objects.filter(subscription_name=subscription_name, is_active=True).count()
    today = date.today()
    current_day =  datetime.datetime.strptime(str(today), '%Y-%m-%d').strftime('%d-%m-%Y')
    check_with_current_day =  datetime.datetime.strptime(str(current_day), '%d-%m-%Y').strftime('%Y-%m-%d')
    count = 0
    for subscription in check_plan:
        expiry =  datetime.datetime.strptime(str(subscription.expiry_date), '%d-%m-%Y').strftime('%Y-%m-%d')
        if expiry <= check_with_current_day:
            count=count+1
    context = {
        "check_plan_count": check_plan_count,
        "count": count,
        "SubscriptionNavclass": 'active',
        "SimpleSubscriptionNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }
    return render(request, "super_admin/settings/subscription_plans/check-subscription-plans-status.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def view_subscription_status_Transitional(request, subscription_name):
    print()
    check_plan = transactional_sms_subscriptions.objects.filter(subscription_name=subscription_name, is_active=True)
    check_plan_count = transactional_sms_subscriptions.objects.filter(subscription_name=subscription_name, is_active=True).count()
    today = date.today()
    current_day =  datetime.datetime.strptime(str(today), '%Y-%m-%d').strftime('%d-%m-%Y')
    check_with_current_day =  datetime.datetime.strptime(str(current_day), '%d-%m-%Y').strftime('%Y-%m-%d')
    count = 0
    for subscription in check_plan:
        expiry =  datetime.datetime.strptime(str(subscription.expiry_date), '%d-%m-%Y').strftime('%Y-%m-%d')
        if expiry <= check_with_current_day:
            count=count+1
    context = {
        "check_plan_count": check_plan_count,
        "count": count,
        "SubscriptionNavclass": 'active',
        "TransactionalSubscriptionNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }
    return render(request, "super_admin/settings/subscription_plans/check-subscription-plans-status_transitional.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def view_subscription_status_promotional(request, subscription_name):
    print()
    check_plan = promotional_sms_subscriptions.objects.filter(subscription_name=subscription_name, is_active=True)
    check_plan_count = promotional_sms_subscriptions.objects.filter(subscription_name=subscription_name, is_active=True).count()
    today = date.today()
    current_day =  datetime.datetime.strptime(str(today), '%Y-%m-%d').strftime('%d-%m-%Y')
    check_with_current_day =  datetime.datetime.strptime(str(current_day), '%d-%m-%Y').strftime('%Y-%m-%d')
    count = 0
    for subscription in check_plan:
        expiry =  datetime.datetime.strptime(str(subscription.expiry_date), '%d-%m-%Y').strftime('%Y-%m-%d')
        if expiry <= check_with_current_day:
            count=count+1
    context = {
        "check_plan_count": check_plan_count,
        "count": count,
        "SubscriptionNavclass": 'active',
        "TransactionalSubscriptionNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }
    return render(request, "super_admin/settings/subscription_plans/check-subscription-plans-status_promotional.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def get_subscription_plans(request):

    sms_subscription_plans = subscription_plan_details.objects.all().order_by('-id')

    count = subscription_plan_details.objects.all().count()

    customized_subscription_plans = subscription_plan_details.objects.all().filter(customized_plan = True)

    # merchant_list = GreenBillUser.objects.all().filter(is_merchant = True)

    merchant_list = MerchantProfile.objects.all().filter(m_disabled_account = False)

    merchant_active = merchant_subscriptions.objects.filter(is_active = True ).count()

    total_merchant = GreenBillUser.objects.filter(is_merchant = True).count()

    merchant_inactive = total_merchant - merchant_active

   
    context = {
        "total_merchant": total_merchant,
        "merchant_inactive": merchant_inactive,
        "merchant_active": merchant_active,
        "count": count,
        "sms_subscription_plans": sms_subscription_plans,
        "customized_subscription_plans": customized_subscription_plans,
        "merchant_list" : merchant_list,
        "SubscriptionNavclass": 'active',
        "SimpleSubscriptionNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }

    return render(request, "super_admin/settings/subscription_plans/subscription-plans.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def get_customized_subscription_plans(request):

    subscription_plans = subscription_plan_details.objects.all().filter(customized_plan = False)

    customized_subscription_plans = subscription_plan_details.objects.all().filter(customized_plan = True).order_by('-id')

    merchant_list = GreenBillUser.objects.all().filter(is_merchant = True)

    context = {
        "sms_subscription_plans": subscription_plans,
        "customized_subscription_plans": customized_subscription_plans,
        "merchant_list" : merchant_list,
        "SubscriptionNavclass": 'active',
        "CustomizedSubscriptionNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }

    return render(request, "super_admin/settings/subscription_plans/customized-subscription-plans.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def get_subscription_plans_by_id(request, id):

    print("hiiiiiiii")

    subscription_plans = subscription_plan_details.objects.get(id=id)

    business_category1 = subscription_plans.business_category

    if business_category1:

        business_category_list = list(business_category1.split(",")) 
    
    else:

        business_category_list = ""


    business_name1 = subscription_plans.merchant_name

    if business_name1:

        business_name_list = list(business_name1.split(",")) 
    
    else:

        business_name_list = ""


    business_category_name2 = []
    
    if business_category1:

        for x in range(len(business_category_list)): 

            business_category_name1 = business_category.objects.get(id=business_category_list[x])

            business_category_name2.append(business_category_name1)

    business_category_name3 = ', '.join(map(str, business_category_name2))

    business_name3 = []
    
    if business_name1:

        for x in range(len(business_name_list)): 

            business_name2 = MerchantProfile.objects.get(id=business_name_list[x])

            business_name3.append(business_name2)

    business_name4 = ', '.join(map(str, business_name3))

    context = {
        'subscription_plans_id': subscription_plans.id,
        "subscription_name": subscription_plans.subscription_name,
        "valid_for_month": subscription_plans.valid_for_month,
        "per_bill_cost": subscription_plans.per_bill_cost,
        "per_url_cost": subscription_plans.per_url_cost,
        "per_receipt_cost": subscription_plans.per_receipt_cost,
        "per_cash_memo_cost": subscription_plans.per_cash_memo_cost,
        "per_digital_bill_cost": subscription_plans.per_digital_bill_cost,
        "per_digital_receipt_cost": subscription_plans.per_digital_receipt_cost,
        "per_digital_cash_memo_cost": subscription_plans.per_digital_cash_memo_cost,
        "software_maintainace_cost": subscription_plans.software_maintainace_cost,
        "recharge_amount":  subscription_plans.recharge_amount,
        "discount_in": subscription_plans.discount_in,
        "discount_percentage":  subscription_plans.discount_percentage,
        "discount_amount":  subscription_plans.discount_amount,
        "subscription_plan_cost":  subscription_plans.subscription_plan_cost,
        "user_type": subscription_plans.user_type,
        "number_of_users": subscription_plans.number_of_users,
        "cost_for_users": subscription_plans.cost_for_users,

        "business_category_list": business_category_list,
        "business_name_list": business_name_list,
        "customized_plan_for": subscription_plans.customized_plan_for,
        "business_category_name": business_category_name3,
        "merchant_name": business_name4,
        'suited_for': subscription_plans.suited_for,
    }

    return JsonResponse({'status':'success', 'subscription_plan': context})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def subscription_plans(request):
    subscriptionplan = request.POST['subscriptionplan']
    if subscriptionplan == "greenbillsubsplan":
        if request.method == "POST":
            subscription_name = request.POST["subscription_name"]
            # valid_for_month = request.POST["valid_for_month"]

            loyalty_point = request.POST['subscriptionplan']

            # if loyalty_point == "greenbillsubsplan":
            #     print(loyalty_point)
            #     loyaltypointsubsplan = ""
            #     bothsubsplan = ""
            # elif loyalty_point == "loyaltypointsubsplan":
            #     print(loyalty_point)
            #     greenbillsubsplan = ""
            #     bothsubsplan = ""
            # else:
            #     print(loyalty_point)
            #     greenbillsubsplan = ""
            #     loyaltypointsubsplan = ""

            number_of_users = request.POST["number_of_users"]
            cost_for_users = request.POST["cost_for_users"]

            per_bill_cost = request.POST["per_bill_cost"]
            # per_receipt_cost = request.POST["per_receipt_cost"]
            # per_cash_memo_cost = request.POST["per_cash_memo_cost"]

            per_digital_bill_cost = request.POST["per_digital_bill_cost"]


            per_url_cost = request.POST["per_url_cost"]
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(per_url_cost)
            # per_digital_receipt_cost = request.POST["per_digital_receipt_cost"]
            # per_digital_cash_memo_cost = request.POST["per_digital_cash_memo_cost"]

            # software_maintainace_cost = request.POST["software_maintainace_cost"]
            recharge_amount = request.POST["recharge_amount"]

            # suited_for = request.POST["suited_for"]

            discount_in = request.POST['discount_in']

            if discount_in == "none":
                discount_percentage = ""
                discount_amount = ""

            else:
                if discount_in == "percentage":
                    discount_percentage = request.POST["discount_percentage"]
                else:
                     discount_percentage = ""

                if discount_in == "amount":
                    discount_amount = request.POST["discount_amount"]
                else:
                    discount_amount = ""

            user_type = request.POST['user_type']

            if user_type == "category":
                customized_plan_for = "business_category"
                business_category_value = request.POST["business_category_value"]
                merchant_name_value = ""
                customized_plan = True

            elif user_type == "merchant":
                customized_plan_for = "merchant"
                merchant_name_value = request.POST["merchant_name_value"]
                business_category_value = ""
                customized_plan = True

            else:
                customized_plan_for = ""
                business_category_value = ""
                merchant_name_value = ""
                customized_plan = False

            subscription_plan_cost = request.POST['subscription_plan_cost']

            # gst_amount = (18*float(subscription_plan_cost_details))/100

            # subscription_plan_cost = float(subscription_plan_cost_details) + float(gst_amount)

            is_active = True
            status1 = ""
            status2 = ""

            if request.POST["plan_id"] != "":

                status1 = subscription_plan_details.objects.update_or_create(id=int(request.POST["plan_id"]), 
                    defaults={
                        "subscription_name": subscription_name,
                        # "valid_for_month": valid_for_month,
                        "loyalty_point" : loyalty_point,
                        "per_bill_cost": per_bill_cost,
                        "per_url_cost":per_url_cost,
                        "loyalty_point":loyalty_point,
                        "per_receipt_cost": per_bill_cost,
                        "per_cash_memo_cost": per_bill_cost,
                        "per_digital_bill_cost": per_digital_bill_cost,
                        "per_digital_receipt_cost": per_digital_bill_cost,
                        "per_digital_cash_memo_cost": per_digital_bill_cost,
                        # "software_maintainace_cost": software_maintainace_cost,
                        "recharge_amount": recharge_amount,
                        "discount_in": discount_in,
                        "discount_percentage": discount_percentage,
                        "discount_amount": discount_amount,
                        "user_type": user_type,
                        "subscription_plan_cost": subscription_plan_cost,
                        "business_category": business_category_value,
                        "merchant_name": merchant_name_value,
                        "customized_plan_for": customized_plan_for,
                        "customized_plan": customized_plan,
                        # "suited_for": suited_for,
                        "gst_amount": gst_amount,
                        "is_active": is_active
                    }
                )

            else:

                status2 = subscription_plan_details.objects.create(
                    subscription_name = subscription_name,
                    loyalty_point = loyalty_point,
                    # valid_for_month = valid_for_month,
                    per_bill_cost = per_bill_cost,
                    per_url_cost = per_url_cost,
                    per_receipt_cost = per_bill_cost,
                    per_cash_memo_cost = per_bill_cost,
                    per_digital_bill_cost = per_digital_bill_cost,
                    # per_digital_receipt_cost = per_digital_bill_cost,
                    # per_digital_cash_memo_cost = per_digital_bill_cost,
                    # software_maintainace_cost = software_maintainace_cost,
                    recharge_amount = recharge_amount,
                    discount_in = discount_in,
                    discount_percentage = discount_percentage,
                    discount_amount = discount_amount,
                    user_type = user_type,
                    subscription_plan_cost = subscription_plan_cost,
                    business_category = business_category_value,
                    merchant_name = merchant_name_value,
                    customized_plan_for = customized_plan_for,
                    customized_plan = customized_plan,
                    # suited_for = suited_for,
                    number_of_users = number_of_users,
                    cost_for_users = cost_for_users,
                    # gst_amount = gst_amount,
                    is_active = is_active
                )

            if status1:
                sweetify.success(request, title="Success", icon='success', text='Subscription updated Successfully.', timer=1500)
                return redirect(get_subscription_plans)

            elif status2:
                sweetify.success(request, title="Success", icon='success', text='Subscription created Successfully.', timer=1500)
                return redirect(get_subscription_plans)

            else:
                sweetify.success(request, title="Oops...", icon='error', text='Fail to create.', timer=1000)
                return redirect(get_subscription_plans)

        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Create !!!', timer=1000)
            return redirect(get_subscription_plans)

    elif subscriptionplan == "loyaltypointsubsplan":
        if request.method == "POST":
            subscription_name = request.POST["subscription_name"]
            # valid_for_month = request.POST["valid_for_month"]
            loyalty_point = request.POST['subscriptionplan']


            number_of_users = request.POST["number_of_users"]
            cost_for_users = request.POST["cost_for_users"]

            per_bill_cost = request.POST["per_bill_cost"]
            # per_receipt_cost = request.POST["per_receipt_cost"]
            # per_cash_memo_cost = request.POST["per_cash_memo_cost"]

            per_digital_bill_cost = request.POST["per_digital_bill_cost"]
            # per_digital_receipt_cost = request.POST["per_digital_receipt_cost"]
            # per_digital_cash_memo_cost = request.POST["per_digital_cash_memo_cost"]

            # software_maintainace_cost = request.POST["software_maintainace_cost"]
            recharge_amount = request.POST["recharge_amount"]

            per_url_cost = request.POST["per_url_cost"]

            # suited_for = request.POST["suited_for"]

            discount_in = request.POST['discount_in']

            if discount_in == "none":
                discount_percentage = ""
                discount_amount = ""

            else:
                if discount_in == "percentage":
                    discount_percentage = request.POST["discount_percentage"]
                else:
                     discount_percentage = ""

                if discount_in == "amount":
                    discount_amount = request.POST["discount_amount"]
                else:
                    discount_amount = ""

            user_type = request.POST['user_type']

            if user_type == "category":
                customized_plan_for = "business_category"
                business_category_value = request.POST["business_category_value"]
                merchant_name_value = ""
                customized_plan = True

            elif user_type == "merchant":
                customized_plan_for = "merchant"
                merchant_name_value = request.POST["merchant_name_value"]
                business_category_value = ""
                customized_plan = True

            else:
                customized_plan_for = ""
                business_category_value = ""
                merchant_name_value = ""
                customized_plan = False

            subscription_plan_cost = request.POST['subscription_plan_cost']

            # gst_amount = (18*float(subscription_plan_cost_details))/100

            # subscription_plan_cost = float(subscription_plan_cost_details) + float(gst_amount)

            is_active = True
            status1 = ""
            status2 = ""

            if request.POST["plan_id"] != "":

                status1 = subscription_plan_details.objects.update_or_create(id=int(request.POST["plan_id"]), 
                    defaults={
                        "subscription_name": subscription_name,
                        # "valid_for_month": valid_for_month,
                        "loyalty_point" : loyalty_point,
                        "per_bill_cost": per_bill_cost,
                        "per_receipt_cost": per_bill_cost,
                        "per_cash_memo_cost": per_bill_cost,
                        "per_url_cost":per_url_cost,
                        "per_digital_bill_cost": per_digital_bill_cost,
                        "per_digital_receipt_cost": per_digital_bill_cost,
                        "per_digital_cash_memo_cost": per_digital_bill_cost,
                        # "software_maintainace_cost": software_maintainace_cost,
                        "recharge_amount": recharge_amount,
                        "discount_in": discount_in,
                        "discount_percentage": discount_percentage,
                        "discount_amount": discount_amount,
                        "user_type": user_type,
                        "subscription_plan_cost": subscription_plan_cost,
                        "business_category": business_category_value,
                        "merchant_name": merchant_name_value,
                        "customized_plan_for": customized_plan_for,
                        "customized_plan": customized_plan,
                        # "suited_for": suited_for,
                        "gst_amount": gst_amount,
                        "is_active": is_active
                    }
                )

            else:

                status2 = subscription_plan_details.objects.create(
                    subscription_name = subscription_name,
                    # valid_for_month = valid_for_month,
                    loyalty_point = loyalty_point,
                    per_bill_cost = per_bill_cost,
                    per_receipt_cost = per_bill_cost,
                    per_cash_memo_cost = per_bill_cost,
                    per_url_cost=per_url_cost,
                    per_digital_bill_cost = per_digital_bill_cost,
                    # per_digital_receipt_cost = per_digital_bill_cost,
                    # per_digital_cash_memo_cost = per_digital_bill_cost,
                    # software_maintainace_cost = software_maintainace_cost,
                    recharge_amount = recharge_amount,
                    discount_in = discount_in,
                    discount_percentage = discount_percentage,
                    discount_amount = discount_amount,
                    user_type = user_type,
                    subscription_plan_cost = subscription_plan_cost,
                    business_category = business_category_value,
                    merchant_name = merchant_name_value,
                    customized_plan_for = customized_plan_for,
                    customized_plan = customized_plan,
                    # suited_for = suited_for,
                    number_of_users = number_of_users,
                    cost_for_users = cost_for_users,
                    # gst_amount = gst_amount,
                    is_active = is_active
                )

            if status1:
                sweetify.success(request, title="Success", icon='success', text='Subscription updated Successfully.', timer=1500)
                return redirect(get_subscription_plans)

            elif status2:
                sweetify.success(request, title="Success", icon='success', text='Subscription created Successfully.', timer=1500)
                return redirect(get_subscription_plans)

            else:
                sweetify.success(request, title="Oops...", icon='error', text='Fail to create.', timer=1000)
                return redirect(get_subscription_plans)

        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Create !!!', timer=1000)
            return redirect(get_subscription_plans)

    else:
        if request.method == "POST":
            subscription_name = request.POST["subscription_name"]
            # valid_for_month = request.POST["valid_for_month"]
            loyalty_point = request.POST['subscriptionplan']
            number_of_users = request.POST["number_of_users"]
            cost_for_users = request.POST["cost_for_users"]

            per_bill_cost = request.POST["per_bill_cost"]
            # per_receipt_cost = request.POST["per_receipt_cost"]
            # per_cash_memo_cost = request.POST["per_cash_memo_cost"]

            per_digital_bill_cost = request.POST["per_digital_bill_cost"]
            # per_digital_receipt_cost = request.POST["per_digital_receipt_cost"]
            # per_digital_cash_memo_cost = request.POST["per_digital_cash_memo_cost"]

            per_url_cost = request.POST["per_url_cost"]
            # software_maintainace_cost = request.POST["software_maintainace_cost"]
            recharge_amount = request.POST["recharge_amount"]

            # suited_for = request.POST["suited_for"]

            discount_in = request.POST['discount_in']

            if discount_in == "none":
                discount_percentage = ""
                discount_amount = ""

            else:
                if discount_in == "percentage":
                    discount_percentage = request.POST["discount_percentage"]
                else:
                     discount_percentage = ""

                if discount_in == "amount":
                    discount_amount = request.POST["discount_amount"]
                else:
                    discount_amount = ""

            user_type = request.POST['user_type']

            if user_type == "category":
                customized_plan_for = "business_category"
                business_category_value = request.POST["business_category_value"]
                merchant_name_value = ""
                customized_plan = True

            elif user_type == "merchant":
                customized_plan_for = "merchant"
                merchant_name_value = request.POST["merchant_name_value"]
                business_category_value = ""
                customized_plan = True

            else:
                customized_plan_for = ""
                business_category_value = ""
                merchant_name_value = ""
                customized_plan = False

            subscription_plan_cost = request.POST['subscription_plan_cost']

            # gst_amount = (18*float(subscription_plan_cost_details))/100

            # subscription_plan_cost = float(subscription_plan_cost_details) + float(gst_amount)

            is_active = True
            status1 = ""
            status2 = ""

            if request.POST["plan_id"] != "":

                status1 = subscription_plan_details.objects.update_or_create(id=int(request.POST["plan_id"]), 
                    defaults={
                        "subscription_name": subscription_name,
                        # "valid_for_month": valid_for_month,
                        "loyalty_point" : loyalty_point,
                        "per_bill_cost": per_bill_cost,
                        "per_receipt_cost": per_bill_cost,
                        "per_cash_memo_cost": per_bill_cost,
                        "per_url_cost":per_url_cost,
                        "per_digital_bill_cost": per_digital_bill_cost,
                        "per_digital_receipt_cost": per_digital_bill_cost,
                        "per_digital_cash_memo_cost": per_digital_bill_cost,
                        # "software_maintainace_cost": software_maintainace_cost,
                        "recharge_amount": recharge_amount,
                        "discount_in": discount_in,
                        "discount_percentage": discount_percentage,
                        "discount_amount": discount_amount,
                        "user_type": user_type,
                        "subscription_plan_cost": subscription_plan_cost,
                        "business_category": business_category_value,
                        "merchant_name": merchant_name_value,
                        "customized_plan_for": customized_plan_for,
                        "customized_plan": customized_plan,
                        # "suited_for": suited_for,
                        "gst_amount": gst_amount,
                        "is_active": is_active
                    }
                )

            else:

                status2 = subscription_plan_details.objects.create(
                    subscription_name = subscription_name,
                    # valid_for_month = valid_for_month,
                    loyalty_point = loyalty_point,
                    per_bill_cost = per_bill_cost,
                    per_receipt_cost = per_bill_cost,
                    per_cash_memo_cost = per_bill_cost,
                    per_url_cost=per_url_cost,
                    per_digital_bill_cost = per_digital_bill_cost,
                    # per_digital_receipt_cost = per_digital_bill_cost,
                    # per_digital_cash_memo_cost = per_digital_bill_cost,
                    # software_maintainace_cost = software_maintainace_cost,
                    recharge_amount = recharge_amount,
                    discount_in = discount_in,
                    discount_percentage = discount_percentage,
                    discount_amount = discount_amount,
                    user_type = user_type,
                    subscription_plan_cost = subscription_plan_cost,
                    business_category = business_category_value,
                    merchant_name = merchant_name_value,
                    customized_plan_for = customized_plan_for,
                    customized_plan = customized_plan,
                    # suited_for = suited_for,
                    number_of_users = number_of_users,
                    cost_for_users = cost_for_users,
                    # gst_amount = gst_amount,
                    is_active = is_active
                )

            if status1:
                sweetify.success(request, title="Success", icon='success', text='Subscription updated Successfully.', timer=1500)
                return redirect(get_subscription_plans)

            elif status2:
                sweetify.success(request, title="Success", icon='success', text='Subscription created Successfully.', timer=1500)
                return redirect(get_subscription_plans)

            else:
                sweetify.success(request, title="Oops...", icon='error', text='Fail to create.', timer=1000)
                return redirect(get_subscription_plans)

        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to Create !!!', timer=1000)
            return redirect(get_subscription_plans)





@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def enable_subscription_plans(request, id):

    status = subscription_plan_details.objects.filter(id=id).update(is_active = True)
    if status:
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'error'})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def disable_subscription_plans(request, id):

    status = subscription_plan_details.objects.filter(id=id).update(is_active = False)
    if status:
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'error'})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def delete_subscription_plans(request, id):

    subscription_object = subscription_plan_details.objects.get(id=id)
    status = subscription_object.delete()

    if status:
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'error'})


import json

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def customized_subscription_plans(request):

    if request.method == "POST":
        subscription_name = request.POST["subscription_name"]
        per_bill_cost = request.POST["per_bill_cost"]
        digital_bill = request.POST["digital_bill"]
        min_recharge = int(request.POST["min_recharge"])
        ideal_for = request.POST["ideal_for"]
        # business_category = request.POST["business_category"]
        business_category_value = request.POST["business_category_value"]
        # business_name = request.POST["business_name"]
        merchant_name_value = request.POST["merchant_name_value"]
        try:
            discount_in = request.POST['custome_amount_in']
        except:
            discount_in = ""
        if discount_in == "custome_percentage_amount":
            custom_percent_val = request.POST['custome_percent_value']
            discount = min_recharge - \
                (min_recharge*int(custom_percent_val)/100)

            customized_plan = True
            is_active = True
            customized_plan_for = request.POST["customized_plan_for"]
            status1 = ""
            status2 = ""
            if request.POST["plan_id"] != "":
                status1 = subscription_plan_details.objects.update_or_create(id=int(request.POST["plan_id"]), defaults={"subscription_name": subscription_name, "per_bill_cost": per_bill_cost, "digital_bill": digital_bill, "min_recharge": min_recharge,
                                                                                                                        "ideal_for": ideal_for, "customized_plan": customized_plan, "business_category": business_category_value, "merchant_name": merchant_name_value, "customized_plan_for": customized_plan_for, "is_active": is_active, "discount_amount": discount})

            else:
                status2 = subscription_plan_details.objects.create(subscription_name=subscription_name, per_bill_cost=per_bill_cost, digital_bill=digital_bill, min_recharge=min_recharge, ideal_for=ideal_for,
                                                                   customized_plan=customized_plan, business_category=business_category_value, merchant_name=merchant_name_value, customized_plan_for=customized_plan_for, is_active=is_active, discount_amount=discount)

            if status1:
                sweetify.success(request, title="Success", icon='success',
                                 text='Customized Subscription updated Successfully.', timer=1500)
                return redirect(get_customized_subscription_plans)
            elif status2:
                sweetify.success(request, title="Success", icon='success',
                                 text='Customized Subscription created Successfully.', timer=1500)
                return redirect(get_customized_subscription_plans)
            else:
                sweetify.success(request, title="Oops...",
                                 icon='error', text='Fail to create.', timer=1000)
                return redirect(get_customized_subscription_plans)
        elif discount_in == "custome_fix_amount":
            fix_amount = int(request.POST['custome_fix_value'])
            total_amount = min_recharge - fix_amount

            customized_plan = True
            is_active = True
            customized_plan_for = request.POST["customized_plan_for"]
            status1 = ""
            status2 = ""
            if request.POST["plan_id"] != "":
                status1 = subscription_plan_details.objects.update_or_create(id=int(request.POST["plan_id"]), defaults={"subscription_name": subscription_name, "per_bill_cost": per_bill_cost, "digital_bill": digital_bill, "min_recharge": min_recharge,
                                                                                                                        "ideal_for": ideal_for, "customized_plan": customized_plan, "business_category": business_category_value, "merchant_name": merchant_name_value, "customized_plan_for": customized_plan_for, "is_active": is_active,  "discount_amount": total_amount})

            else:
                status2 = subscription_plan_details.objects.create(subscription_name=subscription_name, per_bill_cost=per_bill_cost, digital_bill=digital_bill, min_recharge=min_recharge, ideal_for=ideal_for,
                                                                   customized_plan=customized_plan, business_category=business_category_value, merchant_name=merchant_name_value, customized_plan_for=customized_plan_for, is_active=is_active, discount_amount=total_amount)

            if status1:
                sweetify.success(request, title="Success", icon='success',
                                 text='Customized Subscription updated Successfully.', timer=1500)
                return redirect(get_customized_subscription_plans)
            elif status2:
                sweetify.success(request, title="Success", icon='success',
                                 text='Customized Subscription created Successfully.', timer=1500)
                return redirect(get_customized_subscription_plans)
            else:
                sweetify.success(request, title="Oops...",
                                 icon='error', text='Fail to create.', timer=1500)

                return redirect(get_customized_subscription_plans)
        else:
            customized_plan = True
            is_active = True
            customized_plan_for = request.POST["customized_plan_for"]
            status1 = ""
            status2 = ""
            is_discount = False
            if request.POST["plan_id"] != "":
                status1 = subscription_plan_details.objects.update_or_create(id=int(request.POST["plan_id"]), defaults={"subscription_name": subscription_name, "per_bill_cost": per_bill_cost, "digital_bill": digital_bill, "min_recharge": min_recharge,
                                                                                                                        "ideal_for": ideal_for, "customized_plan": customized_plan, "business_category": business_category_value, "merchant_name": merchant_name_value, "customized_plan_for": customized_plan_for, "is_active": is_active, "is_discount": is_discount})

            else:
                status2 = subscription_plan_details.objects.create(subscription_name=subscription_name, per_bill_cost=per_bill_cost, digital_bill=digital_bill, min_recharge=min_recharge, ideal_for=ideal_for,
                                                                   customized_plan=customized_plan, business_category=business_category_value, merchant_name=merchant_name_value, customized_plan_for=customized_plan_for, is_active=is_active, is_discount=is_discount)

            if status1:
                sweetify.success(request, title="Success", icon='success',
                                 text='Customized Subscription updated Successfully.', timer=1500)
                return redirect(get_customized_subscription_plans)
            elif status2:
                sweetify.success(request, title="Success", icon='success',
                                 text='Customized Subscription created Successfully.', timer=1500)
                return redirect(get_customized_subscription_plans)
            else:
                sweetify.success(request, title="Oops...",
                                 icon='error', text='Fail to create.', timer=1500)
                return redirect(get_customized_subscription_plans)

            

    else:
        sweetify.success(request, title="Oops...", icon='error',
                         text='Fail to create.', timer=1000)
        return redirect(get_customized_subscription_plans)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Promotions_Subscription_Plan(request):

    if request.method == "POST":
        subscription_name = request.POST['subscription_name']
        total_sms = request.POST['total_sms']
        per_sms_cost = request.POST['per_sms_cost']
        total_sms_cost = request.POST['total_cost']

        gst_amount = (18*float(total_sms_cost))/100

        total_amount_with_gst = float(total_sms_cost) + float(gst_amount)


        discount_in = request.POST['discount_in']
        merchant_name_value = request.POST["merchant_name_value"]

        # user_type = request.POST['user_type']

        # if user_type == "category":
        #     customized_plan_for = "business_category"
        #     business_category_value = request.POST["business_category_value"]
        #     merchant_name_value = ""
        #     customized_plan = True

        # elif user_type == "merchant":
        #     customized_plan_for = "merchant"
        #     merchant_name_value = request.POST["merchant_name_value"]
        #     business_category_value = ""
        #     customized_plan = True

        # else:
        #     customized_plan_for = ""
        #     business_category_value = ""
        #     merchant_name_value = ""
        #     customized_plan = False   

        
        if discount_in == "none":
            discount_percentage = ""
            discount_amount = ""

        else:
            if discount_in == "percentage":
                discount_percentage = request.POST["discount_percentage"]
            else:
                 discount_percentage = ""

            if discount_in == "amount":
                discount_amount = request.POST["discount_amount"]
            else:
                discount_amount = ""
    
        obj1 = ""
        obj2 = ""

        if request.POST['subscription_id'] != "":

            obj1 = promotional_subscription_plan_model.objects.update_or_create(
                id=int(request.POST['subscription_id']),
                defaults={
                    "subscription_name":subscription_name,
                    "total_sms": total_sms,
                    "per_sms_cost": per_sms_cost,
                    "total_sms_cost": total_amount_with_gst, 
                    "discount_in": discount_in,
                    "discount_amount": discount_amount,
                    "discount_percentage": discount_percentage,
                    # "user_type": user_type,
                    # "business_category": business_category_value,
                    "merchant_name": merchant_name_value,
                    # "customized_plan_for": customized_plan_for,
                    # "customized_plan": customized_plan,

                }
            )

        else:

            is_active = True

            obj2 = promotional_subscription_plan_model.objects.create(
                subscription_name = subscription_name,
                total_sms_cost = total_amount_with_gst,
                total_sms = total_sms,
                per_sms_cost = per_sms_cost,
                discount_in = discount_in, 
                discount_amount = discount_amount,
                gst_amount = gst_amount,
                discount_percentage = discount_percentage,
                actual_total_amount = total_sms_cost,
                is_active = is_active,
                # user_type = user_type,
                # business_category = business_category_value,
                merchant_name = merchant_name_value,
                # customized_plan_for = customized_plan_for,
                # customized_plan = customized_plan,
            )

        if obj1:
            sweetify.success(request, title="Success", icon='success', text='Promotional Subscription updated Successfully.', timer=1500)
        elif obj2:
            sweetify.success(request, title="Success", icon='success', text='Promotional Subscription created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to create.', timer=1500)

    all_promotions = promotional_subscription_plan_model.objects.all().order_by('-id')

    count = promotional_subscription_plan_model.objects.all().count()

    merchant_active = promotional_sms_subscriptions.objects.filter(is_active = True).count()

    total_merchant = GreenBillUser.objects.filter(is_merchant = True).count()

    merchant_inactive = total_merchant - merchant_active
    merchant_list = MerchantProfile.objects.all().filter(m_disabled_account = False)

    context = {
        "merchant_active": merchant_active,
        "total_merchant": total_merchant,
        "merchant_inactive": merchant_inactive,
        "count": count,
        "all_promotions": all_promotions,
        "merchant_list" : merchant_list,
        "SubscriptionNavclass": 'active',
        "PromotionalSubscriptionNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }

    return render(request, "super_admin/settings/subscription_plans/promotional-subscription-plans.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Get_Promotional_plan_by_id(request, id):
    promotional_plan = promotional_subscription_plan_model.objects.get(id=id)

    context = {
        "promotional_plan_id": promotional_plan.id,
        "total_sms": promotional_plan.total_sms,
        "per_cost_sms": promotional_plan.per_sms_cost,
        "total_sms_cost": promotional_plan.total_sms_cost,
        "subscription_name": promotional_plan.subscription_name,
        "discount_in": promotional_plan.discount_in,
        "discount_percentage":promotional_plan.discount_percentage,
        "discount_amount":promotional_plan.discount_amount,
    }
    return JsonResponse({'status': 'success', 'promotional_plan': context})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Delete_promotional_plan(request, id):
    status = promotional_subscription_plan_model.objects.get(
        id=id).delete()
    if status:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Disable_Promotional_Plan(request,id):
    status = promotional_subscription_plan_model.objects.filter(id=id).update(is_active = False)
    if status:
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'error'})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Enable_Promotional_Plan(request,id):
    status = promotional_subscription_plan_model.objects.filter(id=id).update(is_active = True)
    if status:
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'error'})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def transactional_subscription_plan(request):

    if request.method == "POST":
        subscription_name = request.POST['subscription_name']
        total_sms = request.POST['total_sms']
        per_sms_cost = request.POST['per_sms_cost']
        total_sms_cost = request.POST['total_cost']

        gst_amount = (18*float(total_sms_cost))/100

        total_amount_with_gst = float(total_sms_cost) + float(gst_amount)

        discount_in = request.POST['discount_in']
        merchant_name_value = request.POST["merchant_name_value"]

        # user_type = request.POST['user_type']

        # if user_type == "category":
        #     customized_plan_for = "business_category"
        #     business_category_value = request.POST["business_category_value"]
        #     merchant_name_value = ""
        #     customized_plan = True

        # elif user_type == "merchant":
        #     customized_plan_for = "merchant"
        #     merchant_name_value = request.POST["merchant_name_value"]
        #     business_category_value = ""
        #     customized_plan = True

        # else:
        #     customized_plan_for = ""
        #     business_category_value = ""
        #     merchant_name_value = ""
        #     customized_plan = False   

        
        if discount_in == "none":
            discount_percentage = ""
            discount_amount = ""

        else:
            if discount_in == "percentage":
                discount_percentage = request.POST["discount_percentage"]
            else:
                 discount_percentage = ""

            if discount_in == "amount":
                discount_amount = request.POST["discount_amount"]
            else:
                discount_amount = ""
    
        obj1 = ""
        obj2 = ""

        if request.POST['subscription_id'] != "":

            obj1 = transactional_subscription_plan_model.objects.update_or_create(
                id=int(request.POST['subscription_id']),
                defaults={
                    "subscription_name":subscription_name,
                    "total_sms": total_sms,
                    "per_sms_cost": per_sms_cost,
                    "total_sms_cost": total_amount_with_gst, 
                    "discount_in": discount_in,
                    "discount_amount": discount_amount,
                    "discount_percentage": discount_percentage,
                    # "user_type": user_type,
                    # "business_category": business_category_value,
                    "merchant_name": merchant_name_value,
                    # "customized_plan_for": customized_plan_for,
                    # "customized_plan": customized_plan,

                }
            )

        else:

            is_active = True

            obj2 = transactional_subscription_plan_model.objects.create(
                subscription_name = subscription_name,
                total_sms_cost = total_amount_with_gst,
                total_sms = total_sms,
                per_sms_cost = per_sms_cost,
                gst_amount = gst_amount,
                discount_in = discount_in, 
                discount_amount = discount_amount,
                discount_percentage = discount_percentage,
                actual_total_amount = total_sms_cost,
                is_active = is_active,
                # user_type = user_type,
                # business_category = business_category_value,
                merchant_name = merchant_name_value,
                # customized_plan_for = customized_plan_for,
                # customized_plan = customized_plan,
            )

        if obj1:
            sweetify.success(request, title="Success", icon='success', text='Transactional Subscription updated Successfully.', timer=1500)
        elif obj2:
            sweetify.success(request, title="Success", icon='success', text='Transactional Subscription created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to create.', timer=1500)

    all_transactional = transactional_subscription_plan_model.objects.all().order_by('-id')

    count = transactional_subscription_plan_model.objects.all().count()

    merchant_active = transactional_sms_subscriptions.objects.filter(is_active = True).count()

    total_merchant = GreenBillUser.objects.filter(is_merchant = True).count()

    merchant_inactive = total_merchant - merchant_active
    merchant_list = MerchantProfile.objects.all().filter(m_disabled_account = False)

    context = {
        "merchant_active": merchant_active,
        "total_merchant": total_merchant,
        "merchant_inactive": merchant_inactive,
        "count": count,
        "all_transactional":all_transactional,
        "merchant_list" : merchant_list,
        "SubscriptionNavclass": 'active',
        "TransactionalSubscriptionNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }

    return render(request, "super_admin/settings/subscription_plans/transactional-subscription-plans.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def get_transactional_plan_by_id(request, id):

    transactional_plan = transactional_subscription_plan_model.objects.get(id=id)

    context = {
        "transactional_plan_id": transactional_plan.id,
        "total_sms": transactional_plan.total_sms,
        "per_cost_sms": transactional_plan.per_sms_cost,
        "total_sms_cost": transactional_plan.total_sms_cost,
        "subscription_name": transactional_plan.subscription_name,
        "discount_in": transactional_plan.discount_in,
        "discount_percentage":transactional_plan.discount_percentage,
        "discount_amount":transactional_plan.discount_amount,
    }

    return JsonResponse({'status': 'success', 'promotional_plan': context})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def delete_transactional_plan(request, id):
    status = transactional_subscription_plan_model.objects.get(
        id=id).delete()
    if status:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def disable_transactional_plan(request,id):
    status = transactional_subscription_plan_model.objects.filter(id=id).update(is_active = False)
    if status:
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'error'})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def enable_transactional_plan(request,id):
    status = transactional_subscription_plan_model.objects.filter(id=id).update(is_active = True)
    if status:
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'error'})

# Add On's Plans
@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def add_on_plan(request):

    if request.method == "POST":
        add_on_name = request.POST['add_on_name']

        # per_bill_cost = request.POST['per_bill_cost']
        # per_receipt_cost = request.POST['per_receipt_cost']
        # per_cash_memo_cost = request.POST['per_cash_memo_cost']

        # per_digital_bill_cost = request.POST['per_digital_bill_cost']
        # per_digital_receipt_cost = request.POST['per_digital_receipt_cost']
        # per_digital_cash_memo_cost = request.POST['per_digital_cash_memo_cost']

        recharge_amount = request.POST['recharge_amount1']
        recharge_amount1 = request.POST.get('recharge_amount1')
        recharge_amount2 = request.POST.get('recharge_amount2')
        recharge_amount3 = request.POST.get('recharge_amount3')
        recharge_amount4 = request.POST.get('recharge_amount4')
        recharge_amount5 = request.POST.get('recharge_amount5')
        recharge_amount6 = request.POST.get('recharge_amount6')
        recharge_amount7 = request.POST.get('recharge_amount7')
        recharge_amount8 = request.POST.get('recharge_amount8')
        recharge_amount9 = request.POST.get('recharge_amount9')
        recharge_amount10 = request.POST.get('recharge_amount10')
        recharge_amount11 = request.POST.get('recharge_amount11')
        recharge_amount12 = request.POST.get('recharge_amount12')
        recharge_amount13 = request.POST.get('recharge_amount13')
        recharge_amount14 = request.POST.get('recharge_amount14')
        recharge_amount15 = request.POST.get('recharge_amount15')
        recharge_amount16 = request.POST.get('recharge_amount16')
        recharge_amount17 = request.POST.get('recharge_amount17')
        recharge_amount18 = request.POST.get('recharge_amount18')
        recharge_amount19 = request.POST.get('recharge_amount19')
        recharge_amount20 = request.POST.get('recharge_amount20')

        #print(recharge_amount1,recharge_amount2,recharge_amount3,recharge_amount4,recharge_amount5,recharge_amount6,recharge_amount7,recharge_amount8,recharge_amount9,recharge_amount10,recharge_amount11,recharge_amount12,recharge_amount13,recharge_amount14,recharge_amount15,recharge_amount16,recharge_amount17,recharge_amount18,recharge_amount19,recharge_amount20)

        gst_amount = (18*float(recharge_amount))/100

        total_amount_with_gst = float(recharge_amount) + float(gst_amount)
    
        obj1 = ""
        obj2 = ""

        if request.POST['add_on_id'] != "":

            obj1 = add_on_plan_model.objects.update_or_create(
                id=int(request.POST['add_on_id']),
                defaults={
                    "add_on_name":add_on_name,
                    # "per_bill_cost": per_bill_cost,
                    # "per_receipt_cost": per_receipt_cost,
                    # "per_cash_memo_cost": per_cash_memo_cost,
                    # "per_digital_bill_cost": per_digital_bill_cost,
                    # "per_digital_receipt_cost": per_digital_receipt_cost,
                    # "per_digital_cash_memo_cost": per_digital_cash_memo_cost,
                    "recharge_amount": total_amount_with_gst
                }
            )

        else:

            is_active = True

            obj2 = add_on_plan_model.objects.create(
                add_on_name = add_on_name,
                # per_bill_cost = per_bill_cost,
                # per_receipt_cost = per_receipt_cost,
                # per_cash_memo_cost = per_cash_memo_cost,
                # per_digital_bill_cost = per_digital_bill_cost,
                # per_digital_receipt_cost = per_digital_receipt_cost,
                # per_digital_cash_memo_cost = per_digital_cash_memo_cost,
                gst_amount = gst_amount,
                recharge_amount = total_amount_with_gst,
                actual_total_amount = recharge_amount,
                recharge_amount_one = recharge_amount1,
                recharge_amount_two = recharge_amount2,
                recharge_amount_three = recharge_amount3,
                recharge_amount_four = recharge_amount4,
                recharge_amount_five = recharge_amount5,
                recharge_amount_six = recharge_amount6,
                recharge_amount_seven = recharge_amount7,
                recharge_amount_eight = recharge_amount8,
                recharge_amount_nine = recharge_amount9,
                recharge_amount_ten = recharge_amount10,
                recharge_amount_eleven = recharge_amount11,
                recharge_amount_twelve = recharge_amount12,
                recharge_amount_thirteen = recharge_amount13,
                recharge_amount_fourteen = recharge_amount14,
                recharge_amount_fifteen = recharge_amount15,
                recharge_amount_sixteen = recharge_amount16,
                recharge_amount_seventeen = recharge_amount17,
                recharge_amount_eighteen = recharge_amount18,
                recharge_amount_nineteen = recharge_amount19,
                recharge_amount_twenty = recharge_amount20,
                is_active = is_active,
            )

        if obj1:
            sweetify.success(request, title="Success", icon='success', text='Add On updated Successfully.', timer=1500)
        elif obj2:
            sweetify.success(request, title="Success", icon='success', text='Add On created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to create.', timer=1500)

    all_add_on = add_on_plan_model.objects.all().order_by('-id')

    count = add_on_plan_model.objects.all().count()

    context = {
        "count": count,
        "all_add_on":all_add_on,
        "SubscriptionNavclass": 'active',
        "AddOnNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }

    return render(request, "super_admin/settings/subscription_plans/add-on-plans.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def get_add_on_plan_by_id(request, id):

    plan = add_on_plan_model.objects.get(id=id)

    context = {
        "plan_id": plan.id,
        "add_on_name": plan.add_on_name,
        "per_bill_cost": plan.per_bill_cost,
        "per_receipt_cost": plan.per_receipt_cost,
        "per_cash_memo_cost": plan.per_cash_memo_cost,
        "per_digital_bill_cost": plan.per_digital_bill_cost,
        "per_digital_receipt_cost":plan.per_digital_receipt_cost,
        "per_digital_cash_memo_cost":plan.per_digital_cash_memo_cost,
        "recharge_amount": plan.recharge_amount,
        "recharge_amount_one": plan.recharge_amount_one,
        "recharge_amount_two": plan.recharge_amount_two,
        "recharge_amount_three": plan.recharge_amount_three,
        "recharge_amount_four": plan.recharge_amount_four,
        "recharge_amount_five": plan.recharge_amount_five,
        "recharge_amount_six": plan.recharge_amount_six,
        "recharge_amount_seven": plan.recharge_amount_seven,
        "recharge_amount_eight": plan.recharge_amount_eight,
        "recharge_amount_nine": plan.recharge_amount_nine,
        "recharge_amount_ten": plan.recharge_amount_ten,
        "recharge_amount_eleven": plan.recharge_amount_eleven,
        "recharge_amount_twelve": plan.recharge_amount_twelve,
        "recharge_amount_thirteen": plan.recharge_amount_thirteen,
        "recharge_amount_fourteen": plan.recharge_amount_fourteen,
        "recharge_amount_fifteen": plan.recharge_amount_fifteen,
    }

    return JsonResponse({'status': 'success', 'plan': context})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def delete_add_on_plan(request, id):
    status = add_on_plan_model.objects.get(id=id).delete()
    if status:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def disable_add_on_plan(request,id):
    status = add_on_plan_model.objects.filter(id=id).update(is_active = False)
    if status:
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'error'})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def enable_add_on_plan(request,id):
    status = add_on_plan_model.objects.filter(id=id).update(is_active = True)
    if status:
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'error'})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def get_offers_subscription_plans(request):

    if request.method == "POST":

        plan_id = request.POST["plan_id"]

        plan_object = subscription_plan_details.objects.get(id = plan_id)

        subscription_name = request.POST["subscription_name"]

        # valid_for_month = plan_object.valid_for_month

        per_bill_cost = plan_object.per_bill_cost
        # per_receipt_cost = plan_object.per_receipt_cost
        # per_cash_memo_cost = plan_object.per_cash_memo_cost

        per_digital_bill_cost = plan_object.per_digital_bill_cost
        # per_digital_receipt_cost = plan_object.per_digital_receipt_cost
        # per_digital_cash_memo_cost = plan_object.per_digital_cash_memo_cost

        # software_maintainace_cost = plan_object.software_maintainace_cost

        number_of_users = plan_object.number_of_users

        cost_for_users = plan_object.cost_for_users

        recharge_amount = plan_object.recharge_amount

        discount_in = request.POST['discount_in']

        if discount_in == "none":
            discount_percentage = ""
            discount_amount = ""

        else:
            if discount_in == "percentage":
                discount_percentage = request.POST["discount_percentage"]
            else:
                 discount_percentage = ""

            if discount_in == "amount":
                discount_amount = request.POST["discount_amount"]
            else:
                discount_amount = ""

        user_type = request.POST['user_type']

        if user_type == "category":
            customized_plan_for = "business_category"
            business_category_value = request.POST["business_category_value"]
            merchant_name_value = ""
            customized_plan = True

        elif user_type == "merchant":
            customized_plan_for = "merchant"
            merchant_name_value = request.POST["merchant_name_value"]
            business_category_value = ""
            customized_plan = True

        else:
            customized_plan_for = ""
            business_category_value = ""
            merchant_name_value = ""
            customized_plan = False

        subscription_plan_cost = request.POST['subscription_plan_cost']

        is_active = True
        status1 = ""
        status2 = ""

        status2 = subscription_plan_details.objects.create(
            subscription_name = subscription_name,
            # valid_for_month = valid_for_month,
            per_bill_cost = per_bill_cost,
            # per_receipt_cost = per_receipt_cost,
            # per_cash_memo_cost = per_cash_memo_cost,
            per_digital_bill_cost = per_digital_bill_cost,
            # per_digital_receipt_cost = per_digital_receipt_cost,
            # per_digital_cash_memo_cost = per_digital_cash_memo_cost,
            number_of_users = number_of_users,
            cost_for_users = cost_for_users,
            recharge_amount = recharge_amount,
            discount_in = discount_in,
            discount_percentage = discount_percentage,
            discount_amount = discount_amount,
            user_type = user_type,
            subscription_plan_cost = subscription_plan_cost,
            business_category = business_category_value,
            merchant_name = merchant_name_value,
            customized_plan_for = customized_plan_for,
            customized_plan = customized_plan,
            is_active = is_active,
            is_offer = True
        )

        if status1:
            sweetify.success(request, title="Success", icon='success', text='Subscription updated Successfully.', timer=1500)

        elif status2:
            sweetify.success(request, title="Success", icon='success', text='Subscription created Successfully.', timer=1500)

        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to create.', timer=1000)

    subscription_plans = subscription_plan_details.objects.all().order_by('-id')

    # merchant_list = GreenBillUser.objects.all().filter(is_merchant = True

    merchant_list = MerchantProfile.objects.all().filter(m_disabled_account = False)
    
    count = subscription_plan_details.objects.all().count()

    context = {
        "count": count,
        "subscription_plans": subscription_plans,
        "merchant_list" : merchant_list,
        "SubscriptionNavclass": 'active',
        "OffersSubscriptionNavclass": "active",
        "SubscriptionCollapseShow": "show"
    }

    return render(request, "super_admin/settings/subscription_plans/offers-subscription-plans.html", context)


# @login_required(login_url="/login/")
# @user_passes_test(is_owner, login_url="/login/")
# def get_add_on_by_id(request, id):

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")  
def merchant_contact_for_subscriptions(request):
    merchant_detail = contact_for_subscriptions_requirements.objects.all()

    context = {
        "merchant_detail" :merchant_detail,
        "MerchantRequestNavclass": "active",
        "MerchantRequestCollapseShow": "show",
        "SubscriptionRequestNavClass": "active"
    }

    return render(request, "super_admin/request-contact-subscription-plans.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")  
def Delete_Enquiry(request, id):
    dm_enquiry = contact_for_subscriptions_requirements.objects.get(id=id)
    dm_enquiry.delete()
    return JsonResponse({'success': True})