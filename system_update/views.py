from django.shortcuts import render
import sweetify
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff, is_owner, is_partner, is_customer
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *

from django.conf import settings
from django.core.mail import send_mail

from super_admin_settings.models import notification_settings

# SMS
import requests
import time
import pyshorteners

from users.models import Merchant_users, MerchantProfile, GreenBillUser, PartnerProfile

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def system_update_view(request):

    if request.method == "POST":
        title = request.POST["title"]
        message = request.POST["message"]
        group_check = request.POST.getlist("group_check[]")
        
        if "customer" in group_check:
            customer_check_status = True
        else:
            customer_check_status = False

        if "merchant" in group_check:
            merchant_check_status = True
        else:
            merchant_check_status = False

        if "partner" in group_check:
            partner_check_status = True
        else:
            partner_check_status = False

        if "parking" in group_check:
           parking_check_status = True
        else:
           parking_check_status = False 

        if "petrol" in group_check:
           petrol_check_status = True
        else:
           petrol_check_status = False    

        result = system_updates.objects.create(title = title, message = message, group_customer = customer_check_status, group_merchant = merchant_check_status, group_partner = partner_check_status, group_parking = parking_check_status, group_petrol = petrol_check_status)
        
        all_merchant = GreenBillUser.objects.filter(is_merchant=True)
        if merchant_check_status == True:
            for merchant in all_merchant:
                unread_system_updates.objects.create(user_id=merchant.id, group_merchant=True, notification_id=result.id)

        all_customer = GreenBillUser.objects.filter(is_customer=True)
        if customer_check_status == True:
            for cust in all_customer:
                unread_system_updates.objects.create(user_id=customer.id, group_customer=True, notification_id=result.id)

        all_partner = GreenBillUser.objects.filter(is_partner=True)
        if  partner_check_status == True:
            for partner in all_partner:
                unread_system_updates.objects.create(user_id=partner.id, group_partner=True,notification_id=result.id)

        all_parking_merchants = GreenBillUser.objects.filter(is_merchant=True)
        if parking_check_status == True:
            for parking_mer in all_parking_merchants:
                try:
                    merchant_object = GreenBillUser.objects.get(id=parking_mer.id)
                    all_business = MerchantProfile.objects.filter(m_user=merchant_object)
                except:
                    all_business = []
                for business in all_business:
                    if business.m_business_category:
                        if business.m_business_category.id == 12:
                            unread_system_updates.objects.create(user_id=parking_mer.id, group_parking=True,notification_id=result.id)
                            break

        all_petrol_merchants = GreenBillUser.objects.filter(is_merchant=True)
        if petrol_check_status == True:
            for petrol_mer in all_petrol_merchants:
                try:
                    merchant_object = GreenBillUser.objects.get(id=petrol_mer.id)
                    all_business = MerchantProfile.objects.filter(m_user=merchant_object)
                except:
                    all_business = []
                for business in all_business:
                    if business.m_business_category:
                        if business.m_business_category.id == 11:
                            unread_system_updates.objects.create(user_id=petrol_mer.id, group_petrol=True,notification_id=result.id)
                            break


        count = 0
        notification_object = notification_settings.objects.get(id = 8)

        merchants = GreenBillUser.objects.filter(is_merchant = True)

        excludes = ['11', '12']

        excludes1 = ['11'] #petrol

        excludes2 = ['12'] #parking

        mail_address = []

        filtered_mail_address = []

        if merchant_check_status == True:

            merchant_business_list = MerchantProfile.objects.filter(m_disabled_account = False).exclude(m_business_category__in = excludes)

            for mer in merchant_business_list:

                count = count + 1

                merchants = GreenBillUser.objects.get(mobile_no = mer.m_user)

                mail_address.append({
                    "mail": merchants.m_email
                })

                for x in mail_address:

                    if x['mail'] not in filtered_mail_address:



                        if notification_object.send_email:
                            subject = 'System Update'
                            message = f'Hey Green Bill Merchant, GreenBill system has been updated & some cool new feature has been added. Enjoy! - Team GreenBill'
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [x['mail'],]

                            try:
                                send_mail( subject, message, email_from, recipient_list)
                            except:
                                pass
                        filtered_mail_address.append(x['mail'])


        if parking_check_status == True:

            merchant_business_list = MerchantProfile.objects.filter(m_disabled_account = False,m_business_category__in =excludes1)

            for mer in merchant_business_list:

                count = count + 1

                merchants = GreenBillUser.objects.get(mobile_no = mer.m_user)
                
                mail_address.append({
                    "mail": merchants.m_email
                })

                for x in mail_address:

                    if x['mail'] not in filtered_mail_address:
                        if notification_object.send_email:
                            subject = 'System Update'
                            message = f'Hey Green Bill Merchant, GreenBill system has been updated & some cool new feature has been added. Enjoy! - Team GreenBill'
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [x['mail'],]

                            try:
                                send_mail( subject, message, email_from, recipient_list)
                            except:
                                pass
                        filtered_mail_address.append(x['mail'])


        if parking_check_status == True:

            merchant_business_list = MerchantProfile.objects.filter(m_disabled_account = False,m_business_category__in =excludes2)

            for mer in merchant_business_list:
                
                count = count + 1

                merchants = GreenBillUser.objects.get(mobile_no = mer.m_user)
                
                mail_address.append({
                    "mail": merchants.m_email
                })

                for x in mail_address:

                    if x['mail'] not in filtered_mail_address:
                        if notification_object.send_email:
                            subject = 'System Update'
                            message = f'Hey Green Bill Merchant, GreenBill system has been updated & some cool new feature has been added. Enjoy! - Team GreenBill'
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [x['mail'],]

                            try:
                                send_mail( subject, message, email_from, recipient_list)
                            except:
                                pass
                        filtered_mail_address.append(x['mail'])


        if partner_check_status == True:

            partner_list = PartnerProfile.objects.filter(p_disabled_account = False)

            for par in partner_list:
                
                count = count + 1

                if par.p_user:

                    partners = GreenBillUser.objects.get(mobile_no = par.p_user)
                    
                    mail_address.append({
                        "mail": partners.p_email
                    })

                    for x in mail_address:

                        if x['mail'] not in filtered_mail_address:

                            if notification_object.send_email:
                                subject = 'System Update'
                                message = f'Hey Green Bill Merchant, GreenBill system has been updated & some cool new feature has been added. Enjoy! - Team GreenBill'
                                email_from = settings.EMAIL_HOST_USER
                                recipient_list = [x['mail'],]

                                try:
                                    send_mail( subject, message, email_from, recipient_list)
                                except:
                                    pass

                            filtered_mail_address.append(x['mail'])



                # for merchant_mail in filtered_mail_address:
                #     print(merchant_mail['mail'])
                # if notification_object.send_email:
                #     subject = 'System Update'
                #     message = f'Hey Green Bill Merchant, GreenBill system has been updated & some cool new feature has been added. Enjoy! - Team GreenBill'
                #     email_from = settings.EMAIL_HOST_USER
                #     recipient_list = [merchants.m_email,]

                #     try:
                #         send_mail( subject, message, email_from, recipient_list)
                #     except:
                #         pass


        # if merchant_check_status == True:

        #     for merchant in merchants:
        #         count = count + 1

                # if notification_object.send_sms:

                #     ts = int(time.time())

                #     data_temp = {
                #             "keyword":"System Update",
                #             "timeStamp":ts,
                #             "dataSet":
                #                 [
                #                     {
                #                         "UNIQUE_ID":"GB-" + str(ts),
                #                         "MESSAGE":"Hey Green Bill Merchant, GreenBill system has been updated & some cool new feature has been added. Enjoy! - Team GreenBill",
                #                         "OA":"GBBILL",
                #                         "MSISDN":str(merchant.mobile_no), # Recipient's Mobile Number
                #                         "CHANNEL":"SMS",
                #                         "CAMPAIGN_NAME":"hind_user",
                #                         "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                #                         "USER_NAME":"hind_hsi",
                #                         "DLT_TM_ID":"1001096933494158", # TM ID
                #                         "DLT_CT_ID":"1007162098326474514", # Template Id
                #                         "DLT_PE_ID":"1001659120000037015" # PE ID 
                #                     }
                #                 ]
                #             }

                #     url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                #     response = requests.post(url, json = data_temp)

                # if notification_object.send_email:
                #     subject = 'System Update'
                #     message = f'Hey Green Bill Merchant, GreenBill system has been updated & some cool new feature has been added. Enjoy! - Team GreenBill'
                #     email_from = settings.EMAIL_HOST_USER
                #     recipient_list = [merchant.m_email,]

                #     try:
                #         send_mail( subject, message, email_from, recipient_list)
                #     except:
                #         pass
        # print('count',count)
        if result:
            sweetify.success(request, title="Success", icon='success', text='System Update Send Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Failed to Send !!!', timer=1500)
    
    SystemUpdate_Form = SystemUpdateForm()

    all_system_update = system_updates.objects.all().order_by("-id")

    context = {
        'all_system_update': all_system_update,
        'SystemUpdateForm' : SystemUpdate_Form,
        'SystemUpdateNavclass': 'active',
    }

    return render(request, "super_admin/system_update/system-update-add.html", context)


def update_system_update_read_status_merchant(request):
    unread_updates = unread_system_updates.objects.filter(read_status=False, user_id=request.user.id).update(read_status=True)
    return JsonResponse({'status': 'success'})


def update_system_update_read_status_partner(request):
    unread_updates= unread_system_updates.objects.filter(read_status=False, user_id=request.user.id).update(read_status=True)
    return JsonResponse({'status': 'success'})

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def delete_system_update_by_id(request, id):
    if request.method == "POST":
        data = system_updates.objects.get(id = id).delete()
        sweetify.success(request, title="success", icon='success', text='System Update deleted Successfully !!!', timer=1500)
        return redirect(system_update_view)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete System Update!!!', timer=1500)
        return redirect(system_update_view)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def get_system_update_by_id(request):
    if request.method == "POST":

        id = request.POST['id']

        update_object = system_updates.objects.get(id= id)

        data = {
            'id': update_object.id,
            'title': update_object.title,
            'message' : update_object.message
        }

        return JsonResponse({'status': "success", 'data' : data})
    else:
        return JsonResponse({'status': "error", 'msg': "Something went wrong !!!"})


@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def customer_system_updates(request):

    all_system_update = system_updates.objects.filter(group_customer=True).order_by("-id")

    context = {
        'all_system_update': all_system_update,
        'SystemUpdateNavclass': 'active'
    }

    return render(request, "customer/system_update/system-update-view.html", context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_system_updates(request):

    
    
    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    all_business = MerchantProfile.objects.filter(m_user=merchant_id)

    business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account=1)

    all_system_update = []
    

    # Petrol Pump
    if business_object.m_business_category.id == 11:
        petrol_system_update = system_updates.objects.filter(group_petrol=True).order_by("-id")
        for system_update in petrol_system_update:
            all_system_update.append(system_update)

    # Parking Lot
    if business_object.m_business_category.id == 12:
        parking_system_update = system_updates.objects.filter(group_parking=True).order_by("-id")
        for system_update in parking_system_update:
            all_system_update.append(system_update)

    other_system_update = system_updates.objects.filter(group_merchant=True).order_by("-id")
    for system_update in other_system_update:
        all_system_update.append(system_update)

    system_update_ids = []
    for system_update in all_system_update:
        if system_update.id in system_update_ids:
            pass
        else:
            system_update_ids.append(system_update.id)

    system_update_ids.sort(reverse = True)

    main_system_updates_data = []
    for system_update in system_update_ids:
        system_update_object = system_updates.objects.get(id = system_update)
        main_system_updates_data.append(system_update_object)
    
    context = {
        'all_system_update': main_system_updates_data,
        'SystemUpdateNavclass': 'active'
    }

    return render(request, "merchant/system_update/system-update-view.html", context)

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_system_updates(request):

    all_system_update = system_updates.objects.filter(group_partner=True).order_by("-id")

    context = {
        'all_system_update': all_system_update,
        'SystemUpdateNavclass': 'active'
    }

    return render(request, "partner/system_update/system-update-view.html", context)