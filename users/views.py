import os
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib.auth.models import User
from django.contrib import messages
import sweetify
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import get_connection, send_mail, BadHeaderError
from .forms import *
from users.models import GreenBillUser, UserProfileImage, MerchantProfile
from datetime import datetime
from django.utils import formats
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner, is_merchant_or_merchant_staff, is_partner, is_customer

# for crop image import statement
from io import BytesIO
from django.shortcuts import render
import json
import os
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from authentication.models import *


from users.models import *
from .models import *

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def profile(request):
    
    if request.method == 'POST':
        user = request.user
        
        user_form = ProfileForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES, instance=user)
        
        if user_form.is_valid() and image_form.is_valid():
            first_name = user_form.cleaned_data.get("first_name")
            last_name = user_form.cleaned_data.get("last_name")
            email = user_form.cleaned_data.get("email")
            profile_image = image_form.cleaned_data.get("profile_image")
            
            GreenBillUser.objects.filter(id=request.user.id).update(first_name = first_name, last_name = last_name, email = email)
            
            if profile_image:
                if image_form.is_valid():
                    UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "profile_image" : profile_image })
            sweetify.success(request, title="Success", icon='success', text='Profile Updated.')
            return redirect('/profile/')
        else:
            sweetify.error(request, title="error", icon='danger', text='Failed To Update')
    else:
        user = request.user

        user_form = ProfileForm()
        image_form = ImageForm(instance=user)
        userDetails = UserProfileImage.objects.filter(id= request.user.id)
            
    return render(request, 'profile/profile.html', {
        'user_form': user_form,
        'image_form': image_form,
        'userDetails': userDetails,
    })

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def profile_image_remove(request):
    UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "profile_image" : "" })
    return redirect(profile)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_profile(request):
    
    if request.method == 'POST':
        user = request.user
        
        user_form = MerchantProfileForm(request.POST)
        # image_form = ImageForm(request.POST, request.FILES, instance=user)
        
        
        if user_form.is_valid():

            first_name = user_form.cleaned_data.get("first_name")
            last_name = user_form.cleaned_data.get("last_name")
            m_email = user_form.cleaned_data.get("m_email")
            m_designation = user_form.cleaned_data.get("m_designation")
            m_adhaar_number = user_form.cleaned_data.get("m_adhaar_number")
            m_pan_number = user_form.cleaned_data.get("m_pan_number")
            m_dob = user_form.cleaned_data.get("m_dob")

            # m_profile_image = image_form.cleaned_data.get("m_profile_image")

            # m_digital_signature = image_form.cleaned_data.get("m_digital_signature")
            
            GreenBillUser.objects.filter(id=request.user.id).update(first_name = first_name, last_name = last_name, m_email = m_email, m_designation = m_designation, m_adhaar_number = m_adhaar_number, m_pan_number = m_pan_number, m_dob = m_dob)
            
            # user_object = GreenBillUser.objects.get(id=request.user.id)

            # try:
            #     user_object.m_digital_signature = request.FILES['m_digital_signature']
            # except KeyError:
            #     user_object.m_digital_signature = ''

            # user_object.save()

            # if m_profile_image:
            #     if image_form.is_valid():
            #         UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "m_profile_image" : m_profile_image })

            sweetify.success(request, title="Success", icon='success', text='Profile Updated.')
            
            return redirect('/merchant-profile/')
        else:

            
            sweetify.error(request, title="error", icon='danger', text='Failed To Update')
    else:

        # user = request.user
        # image_form = ImageForm(instance=user)
        # merchant_profile = MerchantProfile.objects.get(m_user = request.user.id, m_active_account = 1)
        # m_digital_signature = GreenBillUser.objects.filter(id = request.user.id)

        user_form = MerchantProfileForm()
        merchant_user_object = Merchant_users.objects.get(user_id = request.user)

        merchant_object = merchant_user_object.merchant_user_id

        try:
            merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
        except:
            pass

        try:
            if merchant_business_id.m_business_logo:
                business_logo = merchant_business_id.m_business_logo
            else:
                business_logo = ""
        except:
            business_logo = ""

        

    return render(request, 'profile/merchant-profile.html', {
        'user_form': user_form,"business_logo":business_logo
    })

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchnat_profile_image_remove(request):
    UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "m_profile_image" : ""})
    return redirect(merchant_profile)

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_profile(request):
    
    if request.method == 'POST':
        user = request.user
        
        user_form = PartnerProfileForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES, instance=user)

        print('-----------------------',user_form.is_valid(),'-------------------',image_form.is_valid())
        
        if user_form.is_valid() and image_form.is_valid():

            first_name = user_form.cleaned_data.get("first_name")
            last_name = user_form.cleaned_data.get("last_name")
            p_email = user_form.cleaned_data.get("p_email")
            p_designation = user_form.cleaned_data.get("p_designation")
            p_adhaar_number = user_form.cleaned_data.get("p_adhaar_number")
            p_pan_number = user_form.cleaned_data.get("p_pan_number")
            p_dob = user_form.cleaned_data.get("p_dob")

            p_profile_image = image_form.cleaned_data.get("m_profile_image")
            
            GreenBillUser.objects.filter(id=request.user.id).update(first_name = first_name, last_name = last_name, p_email = p_email, p_designation = p_designation, p_adhaar_number = p_adhaar_number, p_pan_number = p_pan_number, p_dob = p_dob)

            if p_profile_image:
                if image_form.is_valid():
                    UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "p_profile_image" : p_profile_image })

            sweetify.success(request, title="Success", icon='success', text='Profile Updated.')
            
            return redirect('/partner-profile/')
        else:
            sweetify.error(request, title="error", icon='danger', text='Failed To Update')
    else:

        user = request.user
        image_form = ImageForm(instance=user)

    return render(request, 'profile/partner-profile.html', {
        'image_form': image_form,
    })

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_profile_image_remove(request):
    UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "p_profile_image" : "" })
    return redirect(partner_profile)

@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def customer_profile(request):
    
    if request.method == 'POST':
        user = request.user
        user_details = GreenBillUser.objects.filter(mobile_no=user)
        user_form = CustomerProfileForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES, instance=user)
        
        if user_form.is_valid() and image_form.is_valid():
            email = user_form.cleaned_data.get("email")
            first_name = user_form.cleaned_data.get("first_name")
            last_name = user_form.cleaned_data.get("last_name")
            c_gender = user_form.cleaned_data.get("c_gender")
            c_dob = user_form.cleaned_data.get("c_dob")
            # formatted_c_dob = datetime.strptime(c_dob, '%d-%m-%Y').strftime('%Y-%m-%d')
            c_address_1 = user_form.cleaned_data.get("c_address_1")
            c_address_2 = user_form.cleaned_data.get("c_address_2")

            cust_area = user_form.cleaned_data.get("c_area")
            c_area = cust_area.capitalize()

            cust_state = user_form.cleaned_data.get("c_state")
            c_state = cust_state.capitalize()

            c_pincode = user_form.cleaned_data.get("c_pincode")
            
            cust_city = user_form.cleaned_data.get("c_city")
            c_city = cust_city.capitalize()
            
            GreenBillUser.objects.filter(id=request.user.id).update(email = email, first_name = first_name, last_name = last_name, c_gender = c_gender, c_dob = c_dob, c_address_1 = c_address_1, c_address_2 = c_address_2, c_area = c_area, c_state = c_state, c_pincode= c_pincode, c_city = c_city)
            
            c_profile_image = image_form.cleaned_data.get("c_profile_image")
            if c_profile_image:
                if image_form.is_valid():
                    UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "c_profile_image" : c_profile_image })
            
            sweetify.success(request, title="Success", icon='success', text='Profile Updated Successfully!!')
            return redirect('/customer-profile/')
        else:
            sweetify.error(request, title="error", icon='error', text='Failed To Update')
    else:
        user = request.user
        user_form = CustomerProfileForm()
        image_form = ImageForm(instance=user)
        user_details = GreenBillUser.objects.filter(mobile_no=user)
        States = StateCityData.objects.values('state').distinct().order_by('state')
        
    return render(request, 'profile/customer-profile.html', {
        'user_form': user_form,
        'image_form': image_form,
        'States': States,
        'user_details': user_details
    })

@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def customer_profile_image_remove(request):
    UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "c_profile_image" : "" })
    return redirect(customer_profile)



@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def upload_crop_profile_image(request):
    if request.method == 'POST':
        form = UploadCropImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            img_data = dict(request.POST.items())
            # print(img_data)

            x = None  # Coordinate x
            y = None  # Coordinate y
            w = None  # Width
            h = None  # Height
            rotate = None  # Rotate
            for key, value in img_data.items():
                if key == "avatar_data":
                    str_value = json.loads(value)
                    print(str_value)
                    x = str_value.get('x')
                    y = str_value.get('y')
                    w = str_value.get('width')
                    h = str_value.get('height')
                    rotate = str_value.get('rotate')

            # print('x: {}, y: {}, w: {}, h: {}, rotate: {}'.format(
            #     x, y, w, h, rotate))

            im = Image.open(request.FILES['profileimage']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            # newdoc = UserProfileImage.objects.get(user_id=request.user.id)

            try:
                newdoc = UserProfileImage.objects.get(user_id=request.user.id)
            except:
                UserProfileImage.objects.create(user_id=request.user.id)
                newdoc = UserProfileImage.objects.get(user_id=request.user.id)
                
            newdoc.profile_image.save('profile_image.png', image_file)
            newdoc.save()
            data = {
                'result': True,
                'state': 200,
                'message': 'Success',
            }

            # redirect("/general-setting/")

            return JsonResponse({'data': data})


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def upload_crop_merchant_profile_image(request):
    if request.method == 'POST':
        form = merchantCropImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            img_data = dict(request.POST.items())
            # print(img_data)

            x = None  # Coordinate x
            y = None  # Coordinate y
            w = None  # Width
            h = None  # Height
            rotate = None  # Rotate
            for key, value in img_data.items():
                if key == "avatar_data":
                    str_value = json.loads(value)
                    print(str_value)
                    x = str_value.get('x')
                    y = str_value.get('y')
                    w = str_value.get('width')
                    h = str_value.get('height')
                    rotate = str_value.get('rotate')

            # print('x: {}, y: {}, w: {}, h: {}, rotate: {}'.format(
            #     x, y, w, h, rotate))

            im = Image.open(
                request.FILES['merchantprofileimage']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            # newdoc = UserProfileImage.objects.get(user_id=request.user.id)
            
            try:
                newdoc = UserProfileImage.objects.get(user_id=request.user.id)
            except:
                UserProfileImage.objects.create(user_id=request.user.id)
                newdoc = UserProfileImage.objects.get(user_id=request.user.id)

            newdoc.m_profile_image.save('profile_image.png', image_file)
            newdoc.save()
            data = {
                'result': True,
                'state': 200,
                'message': 'Success',
            }

            # redirect("/general-setting/")

            return JsonResponse({'data': data})


@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def upload_croped_customer_profile_image(request):
    if request.method == 'POST':
        form = customerCropImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            img_data = dict(request.POST.items())
            # print(img_data)

            x = None  # Coordinate x
            y = None  # Coordinate y
            w = None  # Width
            h = None  # Height
            rotate = None  # Rotate
            for key, value in img_data.items():
                if key == "avatar_data":
                    str_value = json.loads(value)
                    print(str_value)
                    x = str_value.get('x')
                    y = str_value.get('y')
                    w = str_value.get('width')
                    h = str_value.get('height')
                    rotate = str_value.get('rotate')

            # print('x: {}, y: {}, w: {}, h: {}, rotate: {}'.format(
            #     x, y, w, h, rotate))

            im = Image.open(
                request.FILES['customerprofileimage']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            try:
                newdoc = UserProfileImage.objects.get(user_id=request.user.id)
            except:
                UserProfileImage.objects.create(user_id=request.user.id)
                newdoc = UserProfileImage.objects.get(user_id=request.user.id)

            newdoc.c_profile_image.save('profile_image.png', image_file)
            newdoc.save()
            data = {
                'result': True,
                'state': 200,
                'message': 'Success',
            }

            # redirect("/general-setting/")

            return JsonResponse({'data': data})


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def upload_crop_partner_profile_image(request):
    if request.method == 'POST':
        form = partnerCropImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            img_data = dict(request.POST.items())
            # print(img_data)

            x = None  # Coordinate x
            y = None  # Coordinate y
            w = None  # Width
            h = None  # Height
            rotate = None  # Rotate
            for key, value in img_data.items():
                if key == "avatar_data":
                    str_value = json.loads(value)
                    print(str_value)
                    x = str_value.get('x')
                    y = str_value.get('y')
                    w = str_value.get('width')
                    h = str_value.get('height')
                    rotate = str_value.get('rotate')

            # print('x: {}, y: {}, w: {}, h: {}, rotate: {}'.format(
            #     x, y, w, h, rotate))

            im = Image.open(
                request.FILES['partnerprofileimage']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            try:
                newdoc = UserProfileImage.objects.get(user_id=request.user.id)
            except:
                UserProfileImage.objects.create(user_id=request.user.id)
                newdoc = UserProfileImage.objects.get(user_id=request.user.id)

            newdoc.p_profile_image.save('profile_image.png', image_file)
            newdoc.save()
            data = {
                'result': True,
                'state': 200,
                'message': 'Success',
            }

            # redirect("/general-setting/")

            return JsonResponse({'data': data})
