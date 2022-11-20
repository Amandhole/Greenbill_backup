import sweetify
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.http import HttpResponse, JsonResponse
from .models import *
from users.models import GreenBillUser, PartnerProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner
from users.models import GreenBillUser

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def email_templates(request):
    email_templates_form = EmailTemplatesForm()

    context = {
        'form' : email_templates_form
    }

    return render(request, "super_admin/settings/email_templates.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def notification_settings_view(request):



    if request.method == 'POST':
        dict = request.POST

        row_count = notification_settings.objects.latest('id')

        for i in range(1, row_count.id + 1):

            send_email_temp = 'email[' + str(i) + ']'
            send_email = dict.get(send_email_temp)

            send_sms_temp = 'sms[' + str(i) + ']'
            send_sms = dict.get(send_sms_temp)
           
            send_app_notification_temp = 'app_notification[' + str(i) + ']'
            send_app_notification = dict.get(send_app_notification_temp)
            
            notification_settings.objects.filter(id = i).update(send_email = send_email, send_sms = send_sms, send_app_notification = send_app_notification)

        sweetify.success(request, title="Success", icon='success', text='Notification Settings Updated.', timer=1500)

        return redirect(notification_settings_view)

    else:
        super_admin_notification_settings = notification_settings.objects.filter(is_super_admin_setting = 1)

        merchant_notification_settings = notification_settings.objects.filter(is_merchant_setting = 1)

        partner_notification_settings = notification_settings.objects.filter(is_partner_setting = 1)

        customer_notification_settings = notification_settings.objects.filter(is_customer_setting = 1)

        notification_settings_form = NotificationSettingsForm()

    context = {
        'NotificationSettingsForm' : notification_settings_form,
        "SuperAdminNotificationSettings" : super_admin_notification_settings, 
        "MerchantNotificationSettings": merchant_notification_settings, 
        "PartnerNotificationSettings" : partner_notification_settings, 
        "CustomerNotificationSettings" : customer_notification_settings,
        "SettingsNavclass": "active",
        "settingsCollapseShow": "show",
        "NotificationSettingsNavclass": "active"
    }
    return render(request, "super_admin/settings/notification_settings.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def get_notification_settings_by_id(request, id):
    instance = notification_settings.objects.get(id=id)
    return JsonResponse({'notification_settings_id':id, 'notification_message': instance.message})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def notification_message_update_view(request, id):
    if request.method == "POST":
        notification_settings.objects.filter(id = id).update(message = request.POST["message"])
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def smsSetting(request):
    if request.method == "POST":
        form = smsSettingForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            sender_id = form.cleaned_data.get("sender_id")
            status = form.cleaned_data.get("status")

            result = sms_setting.objects.update_or_create(username=username, defaults={
                'username': username, 'password':password, 'sender_id': sender_id, 'status': status
            })

            if result:
               sweetify.success(request, title="Success", icon='success', text='SMS Settings Stored Successfully!.', timer=1500)
               return redirect("/sms-setting/")
            else:
                sweetify.error(request, title="error", icon='error', text='Failed to Stored Setting!')
                return redirect("/sms-setting/")
        else:
            sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
            return redirect("/sms-setting/") 
    else:
        form = smsSettingForm()

        try:
            data = sms_setting.objects.latest('id')
            context = {
                'form': form, 
                'data': data, 
                "SettingsNavclass": "active",
                "settingsCollapseShow": "show",
                'smsSettingActiveClass': "active"
            }
            return render(request, "super_admin/settings/sms_setting.html", context)
        except sms_setting.DoesNotExist:
            data = None
            context = {
                'form': form, 
                'data': data, 
                "SettingsNavclass": "active",
                "settingsCollapseShow": "show",
                'smsSettingActiveClass': "active"
            }
            return render(request, "super_admin/settings/sms_setting.html", context)
@login_required(login_url="/login/")
@user_passes_test(is_owner)
def manage_comapanies_dmr(request):
    if request.method == "POST":
        max_length = 30
        company_name = request.POST["comp_name"]
        
        if company_name:
            if len(company_name) <= max_length:
                result = ManageCompaniesDMR.objects.create(comp_name = company_name)
                if result:
                    return JsonResponse({'status': 'success', 'msg': "Company added successfully !!!"})
                else:
                    return JsonResponse({'status': 'error', 'msg': "Failed to add Company !!!"})
            else:
                msg = "Please add company name with 12 characters."
    data = ManageCompaniesDMR.objects.all().order_by('-id')
    context ={
        'companies_list' : data,
        "MerchantRequestNavclass": "active",
        "MerchantRequestCollapseShow": "show",
        "ManageCompaniesDMR":"active",
    }
    return render(request, "super_admin/add-companies-dmr.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def deletecompaniesdmr(request, id):
    if request.method == "POST":
        data = ManageCompaniesDMR.objects.filter(id= id).delete()
        sweetify.success(request, title="Success", icon='success', text='Company deleted Successfully !!!', timer=1000)
        return redirect(manage_comapanies_dmr)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to delete Company !!!', timer=1000)
        return redirect(manage_comapanies_dmr)

        
@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def payment_setting(request):
    
    if request.method == "POST":
        form = PaymentSettingForm(request.POST)
        
        if form.is_valid():
            payu_key = form.cleaned_data.get("payu_key")
            payu_salt = form.cleaned_data.get("payu_salt")
            
            if request.user.is_staff == True :
                PaymentSetting.objects.update_or_create(payu_key=payu_key, defaults={
                    'payu_key': payu_key, 'payu_salt': payu_salt })

                sweetify.success(request, title="Success", icon='success',
                                text='Payment Setting Stored Successfully !!!')
                return redirect('/payment-setting/')
            else:
                sweetify.error(request, title="error",
                            icon='error', text='You do not have sufficient priviledge to change these settings')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!')
            return redirect('/payment-setting/')
    else:

        if PaymentSetting.objects.all():
            data = PaymentSetting.objects.latest('id')
        else:
            data = None

        form = PaymentSettingForm()
        context = {
            'form' : form, 
            'data' : data,
            "SettingsNavclass": "active",
            "settingsCollapseShow": "show",
            'paymentSettingActiveClass': "active"
        }
        return render(request, "super_admin/settings/payment_setting.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner)
def green_point_settings(request):

    if request.method == "POST":

        form = GreenPointsForm(request.POST, request.FILES)

        if form.is_valid():
            bill_points = form.cleaned_data.get("bill_points")
            referral_points = form.cleaned_data.get("referral_points")
            temp = GreenPointsSettings.objects.update_or_create(id=1, defaults={'bill_points': bill_points , 'referral_points' : referral_points})

            sweetify.success(request, title="Success", icon='success', text='Green Points Stored Successfully !!!')
            return redirect('/green-point-settings/')
            
        else:
            sweetify.error(request, title="error", icon='error', text='Failed to Store !!!')
    else:

       
        data = GreenPointsSettings.objects.latest('id')
        
        form = GreenPointsForm()

        print(data)
    
        context = {
            'form' : form,
            'green_point_settings_data': data,
            "SettingsNavclass": "active",
            "settingsCollapseShow":"show",
            "GreenPointSettingsActiveClass":"active"
        }

        return render(request, "super_admin/settings/green-points-setting.html", context)