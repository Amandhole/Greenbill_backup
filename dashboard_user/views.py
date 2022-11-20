from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .forms import CreateUserForm, UpdateUserForm

from django.conf import settings
User = settings.AUTH_USER_MODEL

from django.core.mail import send_mail 
from role.models import role, userrole
from users.models import GreenBillUser
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner
from super_admin_settings.models import notification_settings

# SMS
import requests
import time
import pyshorteners

from django.utils import timezone

import sweetify

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def register_user_view(request):

    qs = role.objects.all()

    qs1 = GreenBillUser.objects.all().filter(is_staff = "1").order_by('-id')

    for object in qs1:
        temp = GreenBillUser.objects.get(id=object.id)
        qs3 = userrole.objects.filter(user = temp)
    
        for oject1 in qs3:
            object.role = oject1.id
            object.role_name = oject1.role
            qs4 = role.objects.filter(role_name= oject1.role)
            for oject2 in qs4:
                object.role_id = oject2.id
    
    context  = {"role_list": qs, "user_list": qs1, 'myteamNavActiveClass': "active",
            'myteamInfoCollapseShow': "show",
            'myteamByUserNavClass': "active",}
    
    if request.method == 'POST': 
       
        form = CreateUserForm(request.POST)

        if form.is_valid():

            user_object = GreenBillUser.objects.filter(mobile_no = form.cleaned_data['mobile_no'])

            # To check mobile no.already used
            if GreenBillUser.objects.filter(mobile_no = form.cleaned_data['mobile_no']).exists():
                if user_object[0].is_customer and not user_object[0].is_staff and not user_object[0].is_merchant and not user_object[0].is_partner and not user_object[0].is_merchant_staff:

                    temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

                    GreenBilluser = GreenBillUser.objects.filter(
                        mobile_no = form.cleaned_data['mobile_no']).update(
                        email = form.cleaned_data['email'],
                        first_name = form.cleaned_data['first_name'],
                        last_name = form.cleaned_data['last_name'],
                        is_staff = 1
                    )


                    user = GreenBillUser.objects.get(mobile_no = form.cleaned_data['mobile_no'])

                    role_id = form.cleaned_data.get("role_name")

                    userrole.objects.create(user_id = user.id, role_id = role_id)

                    name = form.cleaned_data['first_name']
                    email = form.cleaned_data['email']
                    mobile_no = form.cleaned_data['mobile_no']

                    try:
                        super_user = GreenBillUser.objects.filter(is_superuser = True)
                        super_user_email = super_user[0].email
                        super_user_mobile_no = super_user[0].mobile_no
                    except:
                        super_user_email = ""
                        super_user_mobile_no = ""

                    notification_object = notification_settings.objects.get(id = 1)

                    mobile_no_str = str(super_user_mobile_no) + ',' + str(mobile_no)

                    if notification_object.send_sms:
                        ts = int(time.time())
                        data_temp = {
                                "keyword":"Team Login Credentials",
                                "timeStamp":ts,
                                "dataSet":
                                    [
                                        {
                                            "UNIQUE_ID":"GB-" + str(ts),
                                            "MESSAGE":"Dear Green Bill user, here is the login credentials for your team. Username: " + mobile_no + " Password is same as their Customer Account ",
                                            "OA":"GRBILL", 
                                            "MSISDN": str(mobile_no_str), # Recipient's Mobile Number
                                            "CHANNEL":"SMS",
                                            "CAMPAIGN_NAME":"hind_user",
                                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                            "USER_NAME":"hind_hsi",
                                            "DLT_TM_ID":"1001096933494158", # TM ID
                                            "DLT_CT_ID":"1007162098336084141", # Template Id
                                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                                        }
                                    ]
                                }

                        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                    response = requests.post(url, json = data_temp)

                    if notification_object.send_email:
                        subject = 'Team Login Credentials'
                        message = f'Dear Green Bill user, here is the login credentials for your team.\n Username: {mobile_no} \n Password is same as their Customer Account '
                        email_from = settings.EMAIL_HOST_USER 
                        recipient_list = [email,super_user_email] 
                        send_mail( subject, message, email_from, recipient_list)

                    return JsonResponse({'status':'success'})
                else:
                    return JsonResponse({'status':'invalid'})
            else:

                temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
                
                user = GreenBillUser.objects.create_user(
                    mobile_no = form.cleaned_data['mobile_no'],
                    email = form.cleaned_data['email'],
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'],
                    password = temp_password,
                    is_staff = 1
                )

                user.save()

                role_id = form.cleaned_data.get("role_name")

                userrole.objects.create(user_id = user.id, role_id = role_id)

                name = form.cleaned_data['first_name']
                email = form.cleaned_data['email']
                mobile_no = form.cleaned_data['mobile_no']

                try:
                    super_user = GreenBillUser.objects.filter(is_superuser = True)
                    super_user_email = super_user[0].email
                    super_user_mobile_no = super_user[0].mobile_no
                except:
                    super_user_email = ""
                    super_user_mobile_no = ""

                notification_object = notification_settings.objects.get(id = 1)

                mobile_no_str = str(super_user_mobile_no) + ',' + str(mobile_no)

                if notification_object.send_sms:
                    ts = int(time.time())
                    data_temp = {
                            "keyword":"Team Login Credentials",
                            "timeStamp":ts,
                            "dataSet":
                                [
                                    {
                                        "UNIQUE_ID":"GB-" + str(ts),
                                        "MESSAGE":"Dear Green Bill user, here is the login credentials for your team. Username: " + mobile_no + " Password: "+ temp_password,
                                        "OA":"GRBILL", 
                                        "MSISDN": str(mobile_no_str), # Recipient's Mobile Number
                                        "CHANNEL":"SMS",
                                        "CAMPAIGN_NAME":"hind_user",
                                        "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                                        "USER_NAME":"hind_hsi",
                                        "DLT_TM_ID":"1001096933494158", # TM ID
                                        "DLT_CT_ID":"1007162098336084141", # Template Id
                                        "DLT_PE_ID":"1001659120000037015" # PE ID 
                                    }
                                ]
                            }

                    url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

                response = requests.post(url, json = data_temp)

                if notification_object.send_email:
                    subject = 'Team Login Credentials'
                    message = f'Dear Green Bill user, here is the login credentials for your team.\n Username: {mobile_no} \n Password: {temp_password}'
                    email_from = settings.EMAIL_HOST_USER 
                    recipient_list = [email,super_user_email] 
                    send_mail( subject, message, email_from, recipient_list)

                return JsonResponse({'status':'success'})
        else: 
            return JsonResponse({'status':'error'})
    else:
        return render(request, 'accounts/admin-panel-users.html', context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def update_user_view(request):

    # if request.method == "POST":
    #     post_data = request.POST or None
    #     if post_data != None:

    #         my_form = UpdateUserForm(request.POST)

    #         if my_form.is_valid():

    #             user_id = my_form.cleaned_data.get("user_id")

    #             mobile_no = my_form.cleaned_data.get("edit_mobile_no")
                
    #             role_name = my_form.cleaned_data.get("edit_role_name")
                
    #             email = my_form.cleaned_data.get("edit_email")

    #             first_name = my_form.cleaned_data.get("edit_first_name")

    #             last_name = my_form.cleaned_data.get("edit_last_name")

    #             if user_id is not None:

    #                 GreenBillUser.objects.filter(id = user_id).update(mobile_no = mobile_no, email = email, first_name = first_name, last_name = last_name)

    #                 userrole.objects.filter(user_id = user_id).update(role_id = role_name)

    #             return JsonResponse({'success':True})
    # else:
    #     return False

    if request.method == "POST":

        post_data = request.POST or None

        my_form = UpdateUserForm(request.POST)
        
        if my_form.is_valid():

            user_id = my_form.cleaned_data.get("user_id")

            mobile_no = my_form.cleaned_data.get("edit_mobile_no")
            
            role_name = my_form.cleaned_data.get("edit_role_name")
            print('role_name',role_name)
            email1 = my_form.cleaned_data.get("edit_email")
            print('email12',email1)

            first_name = my_form.cleaned_data.get("edit_first_name")

            last_name = my_form.cleaned_data.get("edit_last_name")

            if user_id is not None:

                GreenBillUser.objects.filter(id = user_id).update(mobile_no = mobile_no, email = email1, first_name = first_name, last_name = last_name)

                userrole.objects.filter(user = user_id).update(role = role_name)

            return JsonResponse({'success':True})
        else:
            return JsonResponse({'success':False})
    else:
        return JsonResponse({'success':False})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def delete_user_view(request, id):

    instance = GreenBillUser.objects.get(id=id)
    instance.delete()

    userrole.objects.filter(user_id = id).delete()

    return JsonResponse({'success':True})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def disable_user_view(request, id):
    GreenBillUser.objects.filter(id=id).update(is_active = False, disable_date = timezone.now())
    return JsonResponse({'success':True})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def enable_user_view(request, id):
    GreenBillUser.objects.filter(id=id).update(is_active = True)
    return JsonResponse({'success':True})

    
@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def all_disable_user(request):
    disable_user = GreenBillUser.objects.all().filter(is_staff="1", is_active= False).order_by('-disable_date')
    context = {	
                "disable_user_list": disable_user,
    			'myteamNavActiveClass': "active",
                'myteamInfoCollapseShow': "show",
                'myteamByDisableNavClass': "active",
    }
    return render(request, 'accounts/admin-panel-disable-user.html', context)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def ownerchangeuserpassword(request):

    if request.method == "POST":
        user_id = request.POST['uid']
        new_password = request.POST['edit_password']

        # print(new_password)
        # print(user_id)

        if user_id is not None:
            user_object = GreenBillUser.objects.get(id=user_id)
            user_object.set_password(new_password)
            user_object.save()
            sweetify.success(request, title="Success", icon='success', text='Password Changed Successfully', timer=1500)

    all_user = GreenBillUser.objects.all().filter(is_staff = "1")

    context = {
        "user_list": all_user,
        'myteamNavActiveClass': "active",
        'myteamInfoCollapseShow': "show",
        'myteamByUserNavClass': "active"
    }

    return render(request, 'accounts/owner-change-user-password.html', context)

