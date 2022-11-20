import sys
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail, EmailMessage, BadHeaderError, EmailMultiAlternatives
from owner_notice_board.sendsms import *
from email.mime.image import MIMEImage
from django.conf import settings
from django.shortcuts import get_object_or_404
import sweetify
from role.models import role, userrole
from merchant_role.models import merchant_role, merchant_userrole
from users.models import *
from .forms import *
from .models import *

from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff, is_owner, is_partner, is_owner, is_customer
# Create your views here.
from merchant_notice.models import merchant_notice_sent,Merchant_Notice_Model
from datetime import datetime
from operator import itemgetter, attrgetter

def get_individual_by_category(request):
    category = request.POST['categories']

    print(category)
    # individuals = individual_category_value.split(",")

    list1 = []

    # filtered_city_list = []
    objs = ''

    if category == 'customers':
    	objs = GreenBillUser.objects.filter(is_customer=True)
    elif category == 'merchants':
    	objs = GreenBillUser.objects.filter(is_merchant=True)
    elif category == 'ownerstaffs':
    	objs = GreenBillUser.objects.filter(is_staff=True)
    elif category == 'partners':
    	objs = GreenBillUser.objects.filter(is_partner=True)

    for ind in objs:
    	list1.append({
    		'id':ind.id,
    		'mobile':ind.mobile_no,
    		})

        # for ind in objs:
        # 	pass
            # list1.append({
            # 	'id':ind.id,
            #     "mobile": ind.mobile_no,
            # })
        
    # for x in list1:
    #     if x['m_city'] not in filtered_city_list:
    #         filtered_city_list.append(x['m_city'])

    return JsonResponse({"data":list1})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def ownerNoticeBoard(request):

    staff = GreenBillUser.objects.all()
    role_list = merchant_role.objects.all()
    category = business_category.objects.all()
    
   
    for object in staff:
        role_name = merchant_userrole.objects.filter(user_id=object.id)
        # print(role_name)
        for object1 in role_name:
            object.role = object1.id
            object.role_name = object1.role
            newRole = role.objects.filter(role_name = object1.role)
            for oject2 in newRole:
                object.role_id = oject2.id
    staff1 = MerchantProfile.objects.all()
    for object in staff1:
       
        category_name = object.m_business_category
        business_name = MerchantProfile.objects.filter(m_business_category=category_name)
        
    notice_data = OnwerNoticeBoard.objects.filter(owner_id= request.user.id).order_by("-id")

    notice_form = ownerNoticeBoardForm()

    selected_messages = DefinedNoticeBoardMessages.objects.all().order_by('-id')
    context = {
        'all_user': staff,
        'selected_messages': selected_messages,
        'role_list': role_list,
        'role_name': role_name,
        'notice_data': notice_data,
        'category' : category,
        'OwnerNotificationNavclass': 'active',
        "OwnerNotificationCollapseShow": "show",
        "OwnerSendNotificationNavclass": "active"
    }


    if request.method == "POST":
        notice_form = ownerNoticeBoardForm(request.POST, request.FILES)
        if notice_form.is_valid():
            notice_title = notice_form.cleaned_data['notice_title']
            notice_file = notice_form.cleaned_data['notice_file']
            message = notice_form.cleaned_data['message']
            user_group = request.POST.getlist('checks')
            owner = request.POST.get('checkso')
            merchant = request.POST.get('checksm')
            customer = request.POST.get('checksc')
            partner = request.POST.get('checksp')
            # print(owner)
            
            individual_user = request.POST.get('individual_value')
           
            category1 = request.POST.getlist('categorychecks')
          
            sent_notice = request.POST.getlist('sentnotice')

            if owner:
                receiver_name = 'Owner Staff'
            if merchant:
                receiver_name = 'Merchant'
            if customer:
                receiver_name = 'Customer'
            if partner:
                receiver_name = 'Partner'
            if owner and merchant:
                receiver_name = 'Qwner Staff, Merchant'
            if owner and customer:
                receiver_name = 'Owner Staff, Mustomer'
            if owner and partner:
                receiver_name = 'Owner Staff, Partner'
            if owner and merchant and customer:
                receiver_name = 'Owner Staff, Merchant, Customer'
            if owner and merchant and customer and partner:
                receiver_name = 'Owner Staff, Merchant, Customer, Partner'
            if individual_user:
                receiver_name = 'Individual User'
            if category1:
                receiver_name = 'Category'
            print('received by')
            print(receiver_name)
            # sys.exit()
            if user_group and category and owner and individual_user and merchant and partner and customer :
                sweetify.error(request,text="Please select either from group or individual  list !!!", timer=5500)
            elif user_group or category or owner or merchant or partner or customer :
                for notice in sent_notice:
                    # if notice == "sms":
                    #     notice_id = OnwerNoticeBoard.objects.create(
                    #         owner_id=request.user, notice_title=notice_title, notice_file=notice_file, message=message, o_sent_sms=True)

                    # elif notice == "sent_mail":
                    #     notice_id = OnwerNoticeBoard.objects.create(
                    #         owner_id=request.user, notice_title=notice_title, notice_file=notice_file, message=message, o_sent_mail=True)

                    # else:
                    #     notice_id = OnwerNoticeBoard.objects.create(
                    #         owner_id=request.user, notice_title=notice_title, notice_file=notice_file, message=message, o_notification=True)

                    if notice == "sms":
                        notice_id = OnwerNoticeBoard.objects.update_or_create(owner_id=request.user, notice_title=notice_title, message=message, defaults= { 'notice_title':notice_title, 'notice_file': notice_file, 'message':message, 'o_sent_sms':True })

                    elif notice == "sent_mail":
                        notice_id = OnwerNoticeBoard.objects.update_or_create(owner_id=request.user, notice_title=notice_title, message=message, defaults= { 'notice_title':notice_title, 'notice_file': notice_file, 'message':message, 'o_sent_mail':True })

                    else:
                        notice_id = OnwerNoticeBoard.objects.update_or_create(owner_id=request.user, notice_title=notice_title, message=message, receiver_name=receiver_name, defaults= { 'notice_title':notice_title, 'notice_file': notice_file, 'message':message, 'o_notification':True })

                    print(notice_id[0].id)

                    notice_object = OnwerNoticeBoard.objects.get(id= notice_id[0].id)

                if user_group:
                    for roleid in user_group:
                        user_list = userrole.objects.filter(role=roleid)
                        
                        for user_data in user_list:
                           
                            for notice in sent_notice:
                                if notice == "sms":
                                    contact = user_data.user
                                    sms_response = sendSMS(str(contact), message)
                                    try:
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user_data.user, defaults = {'sent_sms':True})
                                    except:
                                        owner_notice_sent_save = ""

                                elif notice == "sent_mail":
                                    try:
                                        email_id = user_data.user.email
                                        email_from = settings.EMAIL_HOST_USER
                                        recipient_list = [email_id, ]
                                        sendmail = EmailMessage(
                                            notice_title, message, email_from, recipient_list)

                                        sendmail.attach(notice_file.name,
                                                        notice_file.read(), notice_file.content_type)
                                        response = sendmail.send()
                                        # print(response)
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                            notice_id=notice_object, user_id=user_data.user, defaults = {'sent_mail':True})

                                    except:
                                        owner_notice_sent_save = ""

                                else:
                                    # print(user_data.user)
                                    try:
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user_data.user, defaults = {'notification':True})
                                    except:
                                        owner_notice_sent_save = ""
                if individual_user:
                    # pass
                    print(individual_user)
                    for notice in sent_notice:
                        single_individual = individual_user.split(",")
                        for user in single_individual:
                            user_object = GreenBillUser.objects.get(id=user)
                            if notice == 'sms':
                                contact = user_object.mobile_no
                                sms_response = sendSMS(str(contact), message)
                                owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(notice_id=notice_object, user_id=user_object, defaults = {'sent_sms':True})
                            elif notice == "sent_mail":
                                try:
                                    email_id = user_object.email
                                    email_from = settings.EMAIL_HOST_USER
                                    recipient_list = [email_id, ]
                                    sendmail = EmailMessage(
                                        notice_title, message, email_from, recipient_list)

                                    sendmail.attach(notice_file.name,
                                                    notice_file.read(), notice_file.content_type)

                                    response = sendmail.send()
                                    
                                    owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user_object, defaults = {'sent_mail':True})

                                except:
                                    
                                    owner_notice_sent_save = ""

                            else:
                                try:
                                    owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                    notice_id=notice_object, user_id=user_object, defaults = {'notification':True})
                                except:
                                    owner_notice_sent_save = ""
                if owner:
                    for notice in sent_notice:
                        
                            # print(user)
                            user_object = GreenBillUser.objects.filter(is_staff=True)
                            # print(user_object)
                            for user in user_object:
                                print('users')
                                print(owner)
                                print(user,"+", user.id)
                                if notice == "sms":
                                    contact = user.mobile_no
                                    sms_response = sendSMS(str(contact), message)
                                    owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user, defaults = {'sent_sms':True})

                                elif notice == "sent_mail":
                                    try:
                                        email_id = user.email
                                        email_from = settings.EMAIL_HOST_USER
                                        recipient_list = [email_id, ]
                                        sendmail = EmailMessage(
                                            notice_title, message, email_from, recipient_list)

                                        sendmail.attach(notice_file.name,
                                                        notice_file.read(), notice_file.content_type)

                                        response = sendmail.send()
                                        
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                            notice_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                    except:
                                        
                                        owner_notice_sent_save = ""

                                else:
                                    
                                    try:
                                        print('notice')
                                        print(user)
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user, defaults = {'notification':True})
                                        print(owner_notice_sent_save)
                                    except:
                                        owner_notice_sent_save = ""
                
                if merchant:
                    for notice in sent_notice:
                        
                            # print(user)
                            user_object = GreenBillUser.objects.filter(is_merchant=True)
                            # print(user_object)
                            for user in user_object:
                                print('users')
                                print(user,"+", user.id,"+", user.first_name)
                                if notice == "sms":
                                    contact = user.mobile_no
                                    sms_response = sendSMS(str(contact), message)
                                    owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user, defaults = {'sent_sms':True})

                                elif notice == "sent_mail":
                                    try:
                                        email_id = user.email
                                        email_from = settings.EMAIL_HOST_USER
                                        recipient_list = [email_id, ]
                                        sendmail = EmailMessage(
                                            notice_title, message, email_from, recipient_list)

                                        sendmail.attach(notice_file.name,
                                                        notice_file.read(), notice_file.content_type)

                                        response = sendmail.send()
                                        
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                            notice_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                    except:
                                        
                                        owner_notice_sent_save = ""

                                else:
                                    
                                    try:
                                        print('notice')
                                        print(user)
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user, defaults = {'notification':True})
                                        print(owner_notice_sent_save)
                                    except:
                                        owner_notice_sent_save = ""
                
                if customer:
                    for notice in sent_notice:
                        
                            # print(user)
                            user_object = GreenBillUser.objects.filter(is_customer=True)
                            # print(user_object)
                            for user in user_object:
                                print('users')
                                print(user,"+", user.id,"+", user.first_name)
                                if notice == "sms":
                                    contact = user.mobile_no
                                    sms_response = sendSMS(str(contact), message)
                                    owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user, defaults = {'sent_sms':True})

                                elif notice == "sent_mail":
                                    try:
                                        email_id = user.email
                                        email_from = settings.EMAIL_HOST_USER
                                        recipient_list = [email_id, ]
                                        sendmail = EmailMessage(
                                            notice_title, message, email_from, recipient_list)

                                        sendmail.attach(notice_file.name,
                                                        notice_file.read(), notice_file.content_type)

                                        response = sendmail.send()
                                        
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                            notice_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                    except:
                                        
                                        owner_notice_sent_save = ""

                                else:
                                    
                                    try:
                                        print('notice')
                                        print(user)
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user, defaults = {'notification':True})
                                        print(owner_notice_sent_save)
                                    except:
                                        owner_notice_sent_save = ""
                
                if partner:
                    for notice in sent_notice:
                        
                            # print(user)
                            user_object = GreenBillUser.objects.filter(is_partner=True)
                            # print(user_object)
                            for user in user_object:
                                print('users')
                                print(user,"+", user.id,"+", user.first_name)
                                if notice == "sms":
                                    contact = user.mobile_no
                                    sms_response = sendSMS(str(contact), message)
                                    owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user, defaults = {'sent_sms':True})

                                elif notice == "sent_mail":
                                    try:
                                        email_id = user.email
                                        email_from = settings.EMAIL_HOST_USER
                                        recipient_list = [email_id, ]
                                        sendmail = EmailMessage(
                                            notice_title, message, email_from, recipient_list)

                                        sendmail.attach(notice_file.name,
                                                        notice_file.read(), notice_file.content_type)

                                        response = sendmail.send()
                                        
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                            notice_id=notice_object, user_id=user, defaults = {'sent_mail':True})

                                    except:
                                        
                                        owner_notice_sent_save = ""

                                else:
                                    
                                    try:
                                        print('notice')
                                        print(user)
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user, defaults = {'notification':True})
                                        print(owner_notice_sent_save)
                                    except:
                                        owner_notice_sent_save = ""
                


                if category:
                    for roleid in category1:
                        print('cca')
                        print(roleid)
                        user_list = business_category.objects.filter(id=roleid)
                        for u in user_list:
                            print(u.business_category_name)
                        bb = MerchantProfile.objects.filter(m_business_category = u)
                        print(bb)
                        for user_data in bb:
                           
                            for notice in sent_notice:
                                if notice == "sms":
                                    print(user_data.m_user)
                                    contact = user_data.m_user
                                    print(contact)
                                    sms_response = sendSMS(str(contact), message)
                                    try:
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user_data.m_user, defaults = {'sent_sms':True})
                                    except:
                                        owner_notice_sent_save = ""

                                elif notice == "sent_mail":
                                    try:
                                        email_id = user_data.user.email
                                        email_from = settings.EMAIL_HOST_USER
                                        recipient_list = [email_id, ]
                                        sendmail = EmailMessage(
                                            notice_title, message, email_from, recipient_list)

                                        sendmail.attach(notice_file.name,
                                                        notice_file.read(), notice_file.content_type)
                                        response = sendmail.send()
                                        # print(response)
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                            notice_id=notice_object, user_id=user_data.m_user, defaults = {'sent_mail':True})

                                    except:
                                        owner_notice_sent_save = ""

                                else:
                                    # print('notice')
                                    # print(user_data.m_user)
                                    try:
                                        owner_notice_sent_save = OwnerSentNotice.objects.update_or_create(
                                        notice_id=notice_object, user_id=user_data.m_user, defaults = {'notification':True})
                                    except:
                                        owner_notice_sent_save = ""

            
                sweetify.success(request, title="Success", icon='success',
                                text='Notice Send', timer=5500)
                # return redirect("/owner_notice_board/")
            else:
                sweetify.error(request, title="Error", icon='error',
                                text="Please select either from group or individual list !!!", timer=5500)
        else:
            sweetify.error(request, "Please Provide Valid Data")
            # return JsonResponse({"status": 'error'})

    return render(request, "super_admin/owner_notice_board/owner_notice_board.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def saveOwnerMessages(request):
    notice_message = request.POST['notice_message']
    print(notice_message)
    result = DefinedNoticeBoardMessages.objects.create(message = notice_message)
    if result:
        sweetify.success(request, title="Success", icon='success', text='Message Added Successfully.', timer=1500)
    else:
        sweetify.success(request, title="Oops...", icon='error', text='Fail to Add.', timer=1000)

    return redirect(ownerNoticeBoard)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def DeleteOwnerNoticeBoardMessages(request, id):
    result = DefinedNoticeBoardMessages.objects.filter(id = id).delete()
    if result:
        return JsonResponse({'status': 'success', 'msg': 'Meassage deleted successfully'})
    else:
        return JsonResponse({"status": "error", 'msg': "Something went wrong"})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def ownerNoticeBoardList(request):
    notice_data = OwnerSentNotice.objects.filter(user_id=request.user.id).order_by('-id')
    notice_var = []
    for notice in notice_data:
        # print(notice.notice_id_id)
        
        notification_list = OnwerNoticeBoard.objects.filter(id=notice.notice_id_id).order_by('-id')
        for notification in notification_list:
            notice_var.append(notification)
            # print(notification_list)

    context = {
        'notice_data' : notice_var,
        'OwnerNotificationNavclass': 'active',
        "OwnerNotificationCollapseShow": "show",
        "OwnerNotificationListNavclass": "active"
    }
    return render(request, "super_admin/owner_notice_board/owner_notice_list.html", context)




def readOwnerNotification(request):
    OwnerSentNotice.objects.filter(user_id=request.user.id).update(read_status=1)
    return JsonResponse({'status': "success"})


def deleteownernotice(request,id):
    if request.method == "POST":
        eel = OnwerNoticeBoard.objects.get(id=id)
        
        eel.delete()
        
        return JsonResponse({'success':True})

    return HttpResponse('done!!')



def deletemerchantownernotice(request,id):
    if request.method == 'POST':
        # rel = ownerNoticeBoard.objects.get(id=id)
        # rel.delete()

        rel2 = Merchant_Notice_Model.objects.get(id=id)
        rel2.delete()
        return JsonResponse({"success": True})





@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def ownerMerchantNoticeBoardList(request):    
    
    notice_var = []
    notice_data = OwnerSentNotice.objects.filter(user_id=request.user.id).order_by('-id')
    # notice_var_owner = []
    # print('notice data')
    # print(notice_data)
    # print(request.user.id)
    for notice in notice_data:
        # print(notice.notice_id_id)
        
        notification_list = OnwerNoticeBoard.objects.filter(id=notice.notice_id_id).order_by('-id')
        for notification in notification_list:
            notice_var.append({
                'id': notification.id,
                'owner_id' : notification.owner_id,
                'notice_title': notification.notice_title,
                'notice_file': notification.notice_file,
                'message':notification.message,
                'created_at' : notification.created_at,
                 })
                # datetime.strptime(str(notification.created_at), '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S.%f'),
               
            print(notice_var)

            

    notice_data = merchant_notice_sent.objects.filter(user_id=request.user.id).order_by('-id')
    # notice_var_mer = []
    for notice in notice_data:
        # print(notice.notice_id_id)
        
        notification_list = Merchant_Notice_Model.objects.filter(id=notice.notice_id_id)
        for notification in notification_list:
            notice_var.append({
                'id': notification.id,
                'owner_id' : notification.owner_id,
                'notice_title': notification.notice_title,
                'notice_file': notification.notice_file,
                'message':notification.message,
                'created_at' :  notification.created_at,
                # datetime.strptime(str(notification.created_at), '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S.%f'),
                })
            
            print(notice_var)
    sorted(notice_var,key = itemgetter('created_at'), reverse = True) 
    # notice_var.sort(key = lambda x: datetime.strptime(x['created_at'], '%Y-%m-%d %H:%M:%S.%f'), reverse = True) 
    print(notice_var)
        # print('notice list owner')
        # print(notice_var_owner)
        # print('notice list merchant')
        # print(notice_var_mer)
        # print()
        # notice_var = notice_var_owner + notice_var_mer
       
    context = {
        'notice_data' : notice_var,
        'OwnerNotificationNavclass': 'active',
        "OwnerNotificationCollapseShow": "show",
        "OwnerNotificationListNavclass": "active"
    }
    return render(request, "super_admin/owner_notice_board/owner_merchant_notice_list.html", context)



@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def ownerPartnerNoticeBoardList(request):    
    
    notice_data = OwnerSentNotice.objects.filter(user_id=request.user.id).order_by('-id')
    notice_var = []
    for notice in notice_data:
        # print(notice.notice_id_id)
        
        notification_list = OnwerNoticeBoard.objects.filter(id=notice.notice_id_id).order_by('-id')
        for notification in notification_list:
            notice_var.append(notification)
            # print(notification_list)

    context = {
        'notice_data' : notice_var,
        'OwnerNotificationNavclass': 'active',
        "OwnerNotificationCollapseShow": "show",
        "OwnerNotificationListNavclass": "active"
    }
    return render(request, "super_admin/owner_notice_board/owner_partner_notice_list.html", context)




@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def ownerCustomerNoticeBoardList(request):
    notice_data = OwnerSentNotice.objects.filter(user_id=request.user.id).order_by('-id')
    notice_var = []
    for notice in notice_data:
        # print(notice.notice_id_id)
        
        notification_list = OnwerNoticeBoard.objects.filter(id=notice.notice_id_id).order_by('-id')
        for notification in notification_list:
            notice_var.append(notification)
            # print(notification_list)

    context = {
        'notice_data' : notice_var,
        'OwnerNotificationNavclass': 'active',
        "OwnerNotificationCollapseShow": "show",
        "OwnerNotificationListNavclass": "active"
    }
    return render(request, "super_admin/owner_notice_board/owner_customer_notice_list.html", context)
    
        
        