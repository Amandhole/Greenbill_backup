from django.shortcuts import render, redirect
from .forms import Notice_Form
from .models import *
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail, EmailMessage, BadHeaderError, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from merchant_notice.sendsms import *
from email.mime.image import MIMEImage
from django.conf import settings
from django.shortcuts import get_object_or_404
import sweetify
from merchant_role.models import merchant_role, merchant_userrole
from users.models import *
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff

# Create your views here.

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def Merchant_Notice_Board(request):

    mer_user_id = Merchant_users.objects.get(user_id=request.user)

    merchant_object = mer_user_id.merchant_user_id      # added for bug of multiple displaying on notice

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True) # added for bug of multiple displaying on notice
    
    merchant_all_user = Merchant_users.objects.filter(merchant_user_id=mer_user_id.merchant_user_id)

    for object in merchant_all_user:
        role_name = merchant_role.objects.filter(merchant_id=object.merchant_user_id, merchant_business_id = merchant_business_id)
        # role_name = merchant_role.objects.filter(merchant_id=object.merchant_user_id)     # old query which generates multiple records

    notice_data = Merchant_Notice_Model.objects.filter(owner_id = request.user.id).order_by("-id")

    notice_form = Notice_Form()
    context = {
        'all_user': merchant_all_user,
        'role_name': role_name,
        'notice_data': notice_data,
        'MerchantNotificationNavclass': 'active',
        "MerchantNotificationCollapseShow": "show",
        "MerchantSendNotificationNavclass": "active"
    }
    if request.method == "POST":

        notice_form = Notice_Form(request.POST, request.FILES)
        if notice_form.is_valid():
            notice_title = notice_form.cleaned_data['notice_title']
            notice_file = notice_form.cleaned_data['notice_file']
            message = notice_form.cleaned_data['message']
            user_group = request.POST.getlist('checks')
            individual_user = request.POST.getlist('individual')
            # print(user_group)
            
            sent_notice = request.POST.getlist('sentnotice')
            receiver_name = ''
            receiver_name = []
            for u in user_group:
                merchant_role_name =  merchant_role.objects.get(id=u)
                
                receiver_name = merchant_role_name.role_name
            
            if user_group:
                receiver_name = 'Group'
            if individual_user:
                receiver_name = 'Individual User'

            if user_group and individual_user:
                sweetify.error(request, title="Error", icon='error',
                                text="Please select either from group or individual list !!!", timer=5500)
                                
            elif user_group or individual_user :
                for notice in sent_notice:
                    # if notice == "sms":
                    #     notice_id = Merchant_Notice_Model.objects.create(owner_id=request.user, notice_title=notice_title, notice_file=notice_file, message=message, m_sent_sms=True)

                    # elif notice == "sent_mail":
                    #     notice_id = Merchant_Notice_Model.objects.create(owner_id=request.user, notice_title=notice_title, notice_file=notice_file, message=message, m_sent_mail=True)

                    # else:
                    #     notice_id = Merchant_Notice_Model.objects.create(owner_id=request.user, notice_title=notice_title, notice_file=notice_file, message=message, m_notification=True)

                    if notice == "sms":
                        notice_id = Merchant_Notice_Model.objects.update_or_create(owner_id=request.user, notice_title=notice_title, message=message, defaults= { 'notice_title':notice_title, 'notice_file': notice_file, 'message':message, 'm_sent_sms':True })

                    elif notice == "sent_mail":
                        notice_id = Merchant_Notice_Model.objects.update_or_create(owner_id=request.user, notice_title=notice_title, message=message, defaults= { 'notice_title':notice_title, 'notice_file': notice_file, 'message':message, 'm_sent_mail':True })

                    else:
                        notice_id = Merchant_Notice_Model.objects.update_or_create(owner_id=request.user, notice_title=notice_title, message=message, receiver_name=receiver_name, defaults= { 'notice_title':notice_title, 'notice_file': notice_file, 'message':message, 'm_notification':True })
                    
                    # print(notice_id[0].id)

                    notice_object = Merchant_Notice_Model.objects.get(id= notice_id[0].id)

                if user_group:
                    for roleid in user_group:
                        user_list = merchant_role.objects.filter(id=roleid)
                        # print(user_list)
                        for u in user_list:
                            print(u.merchant_id)
                            merchant = MerchantProfile.objects.filter(m_user = u.merchant_id)
                            # print('merchant',merchant)
                        
                        for user_data in merchant:
                           
                            for notice in sent_notice:
                                if notice == "sms":
                                    contact = user_data.user
                                    sms_response = sendSMS(str(contact), message)
                                    try:
                                        merchant_notice_sent_save = merchant_notice_sent.objects.update_or_create(notice_id=notice_object, user_id=user_data.user, defaults = {'sent_sms':True})
                                    except:
                                        merchant_notice_sent_save = ""

                                elif notice == "sent_mail":
                                    try:
                                        email_id = user_data.user.m_email
                                        email_from = settings.EMAIL_HOST_USER
                                        recipient_list = [email_id, ]
                                        sendmail = EmailMessage(
                                            notice_title, message, email_from, recipient_list)

                                        sendmail.attach(notice_file.name,
                                                        notice_file.read(), notice_file.content_type)
                                        response = sendmail.send()
                                        # print(response)
                                        merchant_notice_sent_save = merchant_notice_sent.objects.update_or_create(
                                            notice_id=notice_object, user_id=user_data.user, defaults = {'sent_mail':True})

                                    except:
                                        merchant_notice_sent_save = ""

                                else:
                                    try:
                                        print('hi',merchant)
                                        merchant_notice_sent_save = merchant_notice_sent.objects.update_or_create(notice_id=notice_object, user_id=user_data.user, defaults = {'notification':True})
                                    except:
                                        merchant_notice_sent_save = ""

            
                if individual_user:
                    for notice in sent_notice:
                        for user in individual_user:
                            user_object = Merchant_users.objects.get(id = user)
                            # print(user_object)
                            if notice == "sms":
                                contact = user_object.user_id.mobile_no
                                sms_response = sendSMS(str(contact), message)
                                try:
                                    merchant_notice_sent_save = merchant_notice_sent.objects.update_or_create(
                                    notice_id=notice_object, user_id=user_object.user_id, defaults = {'sent_sms':True})
                                except:
                                    merchant_notice_sent_save = ""

                            elif notice == "sent_mail":
                                try:
                                    email_id = user_object.user_id.m_email
                                    email_from = settings.EMAIL_HOST_USER
                                    recipient_list = [email_id, ]
                                    sendmail = EmailMessage(
                                        notice_title, message, email_from, recipient_list)

                                    sendmail.attach(notice_file.name,
                                                    notice_file.read(), notice_file.content_type)

                                    response = sendmail.send()
                                    
                                    merchant_notice_sent_save = merchant_notice_sent.objects.update_or_create(
                                        notice_id=notice_object, user_id=user_object.user_id, defaults = {'sent_mail':True})

                                except:
                                    merchant_notice_sent_save = ""

                            else:
                                try:
                                    merchant_notice_sent_save = merchant_notice_sent.objects.update_or_create(
                                    notice_id=notice_object, user_id=user_object.user_id, defaults = {'notification':True})
                                except:
                                    merchant_notice_sent_save = ""


                sweetify.success(request, title="Success", icon='success',
                                text='Notice Sent', timer=5500)
                # return redirect("/merchant_notice_board/")
            else:
                sweetify.error(request, title="Error", icon='error',
                                text="Please select either from group or individual list !!!", timer=5500)
        else:
            sweetify.error(request, "Please Provide Valid Data")
            # return JsonResponse({"status": 'error'})
    return render(request, "merchant/merchant_notice_board/merchant_notice_board.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchantNoticeBoardList(request):
    notice_data = merchant_notice_sent.objects.filter(user_id=request.user.id).order_by('-id')
    notice_var = []
    for notice in notice_data:
        # print(notice.notice_id_id)
        
        notification_list = Merchant_Notice_Model.objects.filter(id=notice.notice_id_id).order_by("-id")
        for notification in notification_list:
            notice_var.append(notification)
            # print(notification_list)

    context = {
        'notice_data' : notice_var,
        'MerchantNotificationNavclass': 'active',
        "MerchantNotificationCollapseShow": "show",
        "MerchantNotificationListNavclass": "active"
    }
    return render(request, "merchant/merchant_notice_board/merchant_notice_list.html", context)

def readMerchantNotification(request):
    merchant_notice_sent.objects.filter(user_id=request.user.id).update(read_status=1)
    return JsonResponse({'status': "success"})



  
def deletemerchantnotice(request,id):
    if request.method == "POST":
        eel = Merchant_Notice_Model.objects.get(id=id)
        
        eel.delete()
        
        return JsonResponse({'success':True})

    return HttpResponse('done!!')

