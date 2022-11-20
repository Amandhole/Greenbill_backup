from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .forms import CreateSoftwarePartnerForm, UpdateSoftwarePartnerForm

from django.conf import settings
User = settings.AUTH_USER_MODEL

from django.core.mail import send_mail 
from users.models import GreenBillUser
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner


# Create your views here.

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def register_software_partner_view(request):

    qs = GreenBillUser.objects.all().filter(is_partner = "1")
    
    context  = {"software_partner_list": qs, 'SoftwarePartnerUserNavclass':'active'}
    
    if request.method == 'POST': 
       
        form = CreateSoftwarePartnerForm(request.POST)

        if form.is_valid():
            # To check mobile no.already used
            if GreenBillUser.objects.filter(mobile_no = form.cleaned_data['mobile_no']).exists():
                return JsonResponse({'status':'invalid'})
            else:

                temp_password = GreenBillUser.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
                
                user = GreenBillUser.objects.create_user(
                    mobile_no = form.cleaned_data['mobile_no'],
                    email = form.cleaned_data['email'],
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'],
                    password = temp_password,
                    is_partner = 1
                )

                user.save()

                name = form.cleaned_data['first_name']
                email = form.cleaned_data['email']
                mobile_no = form.cleaned_data['mobile_no']

                # subject = 'welcome to Green Bill'
                # message = f'Hi {name}, thank you for registering in Green Bill.\n Please use below credentials to login:\n Mobile Number: {mobile_no} \n Password: {temp_password}'
                # email_from = settings.EMAIL_HOST_USER 
                # recipient_list = [email,] 
                # send_mail( subject, message, email_from, recipient_list ) 
            
                import urllib
                username = "sanjog1"
                Password = "123456"
                sender = "HINDAG"
                temp_message = f'Hi {name}, thank you for registering in Green Bill.\n Please use below credentials to login:\n Mobile Number: {mobile_no} \n Password: {temp_password}'
                temp_dict = {"text": temp_message}
                message= urllib.parse.urlencode(temp_dict)
                priority='ndnd'
                stype='normal'

                var= "user="+ str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                import requests

                url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                res = requests.get(url)

                if res.status_code == 200:
                    return JsonResponse({'status':'success'})
                else:
                    return JsonResponse({'status' : 'error', 'msg': "Failed to send message"}) 
        else: 
            return JsonResponse({'status':'error'})
    else:
        return render(request, 'accounts/software-partner-users.html', context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def update_software_partner_view(request):

    if request.method == "POST":
        post_data = request.POST or None
        if post_data != None:

            my_form = UpdateSoftwarePartnerForm(request.POST)

            if my_form.is_valid():

                user_id = my_form.cleaned_data.get("user_id")

                mobile_no = my_form.cleaned_data.get("edit_mobile_no")
                
                email = my_form.cleaned_data.get("edit_email")

                first_name = my_form.cleaned_data.get("edit_first_name")

                last_name = my_form.cleaned_data.get("edit_last_name")

                if user_id is not None:

                    GreenBillUser.objects.filter(id = user_id).update(mobile_no = mobile_no, email = email, first_name = first_name, last_name = last_name)

                return JsonResponse({'success':True})
    else:
        return False

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def delete_software_partner_view(request, id):

    instance = GreenBillUser.objects.get(id=id)
    instance.delete()
    return JsonResponse({'success':True})