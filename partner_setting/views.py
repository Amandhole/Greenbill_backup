import os
import random
import sweetify
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import get_connection, send_mail, BadHeaderError
from users.models import GreenBillUser, UserProfileImage, PartnerProfile, Partner_users
from .forms import *
from category_and_tags.models import business_category
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_partner
from merchant_promotion.models import bulkMailSmsMerchantCustomerModel, smsHeaderModel, templateContentModel


import json
import os
from io import BytesIO
from django.shortcuts import render
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse

from .models import *
from authentication.models import *

# @login_required(login_url="/partner-login/")
# @user_passes_test(is_partner, login_url="/partner-login/")
# def partner_general_setting(request):

#     if request.method == "POST":

#         form = PartnergeneralSettingForm(request.POST, request.FILES)

#         if form.is_valid():
#             partner_setting_id = request.POST["partner_setting_id"]
#             business_name = form.cleaned_data.get("business_name")
#             # business_category_temp = request.POST["merchant_business_category"]
#             pin_code = form.cleaned_data.get("pin_code")
#             city = form.cleaned_data.get("city")
#             district = form.cleaned_data.get("district")
#             state = form.cleaned_data.get("state")
#             address = form.cleaned_data.get("address")
#             landline_number = form.cleaned_data.get("landline_number")
#             alternate_mobile_number = form.cleaned_data.get("alternate_mobile_number")
#             company_email = form.cleaned_data.get("company_email")
#             alternate_email = form.cleaned_data.get("alternate_email")
#             pan_number = form.cleaned_data.get("pan_number")
#             gstin = form.cleaned_data.get("gstin")
#             GSTIN_certificate = form.cleaned_data.get("GSTIN_certificate")
#             cin = form.cleaned_data.get("cin")
#             CIN_certificate = form.cleaned_data.get("CIN_certificate")
#             profile_image = form.cleaned_data.get("profile_image")
#             business_logo = form.cleaned_data.get("business_logo")
#             business_stamp = form.cleaned_data.get("business_stamp")
#             digital_signature = form.cleaned_data.get("digital_signature")
#             bank_account_number = form.cleaned_data.get("bank_account_number")
#             bank_IFSC_code = form.cleaned_data.get("bank_IFSC_code")
#             bank_name = form.cleaned_data.get("bank_name")
#             bank_branch = form.cleaned_data.get("bank_branch")

#             # business_category_object = business_category.objects.get(id=business_category_temp)

#             PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={'p_business_name': business_name, 'p_business_category': "", 'p_pin_code': pin_code, 'p_city': city, 'p_district': district, 'p_state': state, 'p_address': address, 'p_landline_number': landline_number, 'p_alternate_mobile_number': alternate_mobile_number, 'p_company_email': company_email, 'p_alternate_email' : alternate_email, 'p_pan_number': pan_number, 'p_gstin': gstin, 'p_cin': cin, 'p_bank_account_number': bank_account_number, 'p_bank_IFSC_code': bank_IFSC_code, 'p_bank_name' : bank_name, 'p_bank_branch' : bank_branch})

#             if profile_image:
#                 UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "p_profile_image" : profile_image })
            
#             if GSTIN_certificate:
#                 PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_GSTIN_certificate" : GSTIN_certificate })

#             if CIN_certificate:
#                 PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_CIN_certificate" : CIN_certificate })
            
#             if business_logo:
#                 PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_business_logo" : business_logo })

#             if business_stamp:
#                 PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_business_stamp" : business_stamp })

#             if digital_signature:
#                 PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_digital_signature" : digital_signature })
            
#             sweetify.success(request, title="Success", icon='success',
#                              text='Business Settings Stored Successfully !!!', timer=1000)

#             return redirect('/partner-general-setting/')
#         else:
#             sweetify.error(request, title="error",
#                            icon='error', text='Failed !!!', timer=1000)
#             return redirect('/partner-general-setting/')
#     else:

#         partner_general_setting = PartnerProfile.objects.get(p_user = request.user)

#         partner_business_category = business_category.objects.all()
        
#         form = PartnergeneralSettingForm()

#         context = {
#             'form' : form,
#             'partner_general_setting': partner_general_setting,
#             'partner_business_category': partner_business_category,
#             "SettingNavclass": 'active',
#             "settingsCollapseShow": "show",
#             "GeneralSettingsNavclass": 'active'
#         }
            
#         return render(request, "partner/partner_general_setting.html", context)

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_general_setting(request):

    partner_users_object = Partner_users.objects.get(user_id = request.user)

    partner_general_setting = PartnerProfile.objects.get(p_user = partner_users_object.partner_user_id, p_active_account = 1)

    partner_objects_id = GreenBillUser.objects.get(mobile_no = request.user)

    if request.method == "POST":

        form = PartnergeneralSettingForm(request.POST, request.FILES)

        if form.is_valid():
            partner_setting_id = request.POST["partner_setting_id"]
            business_name = form.cleaned_data.get("business_name")
            business_category_temp = request.POST.get("partner_business_category")
            pin_code = form.cleaned_data.get("pin_code")
            city = form.cleaned_data.get("city")
            area = form.cleaned_data.get('area')
            district = form.cleaned_data.get("district")
            state = form.cleaned_data.get("state")
            address = form.cleaned_data.get("address")
            landline_number = form.cleaned_data.get("landline_number")
            alternate_mobile_number = form.cleaned_data.get("alternate_mobile_number")
            p_website_url = form.cleaned_data.get("p_website_url")
            company_email = form.cleaned_data.get("company_email")
            alternate_email = form.cleaned_data.get("alternate_email")
            pan_number = form.cleaned_data.get("pan_number")
            aadhaar_number = form.cleaned_data.get('aadhaar_number')
            tin_vat_number = form.cleaned_data.get('tin_vat_number')
            gstin = form.cleaned_data.get("gstin")
            GSTIN_certificate = form.cleaned_data.get("GSTIN_certificate")
            cin = form.cleaned_data.get("cin")
            CIN_certificate = form.cleaned_data.get("CIN_certificate")
            profile_image = form.cleaned_data.get("profile_image")
            business_logo = form.cleaned_data.get("business_logo")
            business_stamp = form.cleaned_data.get("business_stamp")
            digital_signature = form.cleaned_data.get("digital_signature")
            bank_account_number = form.cleaned_data.get("bank_account_number")
            bank_IFSC_code = form.cleaned_data.get("bank_IFSC_code")
            bank_name = form.cleaned_data.get("bank_name")
            bank_branch = form.cleaned_data.get("bank_branch")
            cancel_bank_cheque_photo = form.cleaned_data.get("cancelled_cheque_certificate")
            udyog_adhar_certificate_file = form.cleaned_data.get("udyog_adhar_certificate")
            address_proof_file = form.cleaned_data.get("address_proof")
            p_business_name_for_billing = form.cleaned_data.get("p_business_name_for_billing")
            p_billing_phone = form.cleaned_data.get("p_billing_phone")
            p_billing_address = form.cleaned_data.get("p_billing_address")
            p_billing_email = form.cleaned_data.get("p_billing_email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            p_bank_account_entity = form.cleaned_data.get("p_bank_account_entity")
            p_adress_account_entity = form.cleaned_data.get("p_adress_account_entity")

            p_pan_legal_entity = form.cleaned_data.get("p_pan_legal_entity")
            p_signature_proof = form.cleaned_data.get("p_signature_proof")
            p_company_registration_certificate = form.cleaned_data.get("p_company_registration_certificate")
            p_payu_schedule_upload = form.cleaned_data.get("p_payu_schedule_upload")
            
            print("************")
            print(business_category_temp)

            business_category_object = business_category.objects.get(id=partner_setting_id)
            # business_category_object = business_category.objects.get(id=business_category_temp)

            GreenBillUser.objects.filter(mobile_no = partner_general_setting.p_user).update(first_name = first_name, last_name = last_name)

            PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={'p_business_name_for_billing': p_business_name_for_billing, 
            'p_business_name': business_name, 'p_business_category': business_category_object, 'p_pin_code': pin_code, 'p_city': city, 'p_area':area,
            'p_district': district, 'p_state': state, 'p_address': address, 'p_landline_number': landline_number, 'p_alternate_mobile_number': alternate_mobile_number,
            'p_company_email': company_email, 'p_alternate_email' : alternate_email, 'p_pan_number': pan_number, 'p_gstin': gstin, 'p_cin': cin, 'p_website_url': p_website_url,
            'p_bank_account_number': bank_account_number, 'p_bank_IFSC_code': bank_IFSC_code, 'p_bank_name' : bank_name, 'p_bank_branch' : bank_branch, 'p_aadhaar_number':aadhaar_number,
            'p_vat_tin_number':tin_vat_number, 'p_billing_phone':p_billing_phone, 'p_billing_address':p_billing_address, 'p_billing_email':p_billing_email,
            'p_bank_account_entity':p_bank_account_entity, 'p_adress_account_entity':p_adress_account_entity})

            for all in PartnerProfile.objects.filter(p_user=request.user,p_business_name=business_name):

                if profile_image:
                    UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "p_profile_image" : profile_image })
                
                if GSTIN_certificate:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_GSTIN_certificate" : GSTIN_certificate })

                if CIN_certificate:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_CIN_certificate" : CIN_certificate })
                
                if business_logo:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_business_logo" : business_logo })

                if business_stamp:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_business_stamp" : business_stamp })

                if digital_signature:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_digital_signature" : digital_signature })

                if cancel_bank_cheque_photo:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_cancelled_cheque_certificate" : cancel_bank_cheque_photo })


                if udyog_adhar_certificate_file:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_udyog_adhar_certificate" : udyog_adhar_certificate_file })
                
                if address_proof_file:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "address_proof" : address_proof_file })

                if p_pan_legal_entity:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_pan_legal_entity" : p_pan_legal_entity })

                if p_signature_proof:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_signature_proof" : p_signature_proof })

                if p_company_registration_certificate:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_company_registration_certificate" : p_company_registration_certificate })

                if p_payu_schedule_upload:
                    PartnerProfile.objects.update_or_create(id = partner_setting_id, defaults={ "p_payu_schedule_upload" : p_payu_schedule_upload })



                sweetify.success(request, title="Success", icon='success',
                                 text='Business Settings Stored Successfully !!!', timer=1000)

            return redirect('/partner-general-setting/')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!', timer=1000)
            return redirect('/partner-general-setting/')
    else:

        partner_general_setting = PartnerProfile.objects.get(p_user = request.user)

        partner_business_category = business_category.objects.all()
        States = StateCityData.objects.values('state').distinct().order_by('state')
        form = PartnergeneralSettingForm()

        context = {
            'form' : form,
            'States': States,
            'partner_general_setting': partner_general_setting,
            'partner_business_category': partner_business_category,
            'partner_objects_id': partner_objects_id,
            "SettingNavclass": 'active',
            "settingsCollapseShow": "show",
            "GeneralSettingsNavclass": 'active'
        }
            
        return render(request, "partner/partner_general_setting.html", context)
        
@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_business_logo_remove(request):
    PartnerProfile.objects.update_or_create(p_user = request.user.id, defaults={ "p_business_logo" : ""})
    return redirect(partner_general_setting)

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_business_stamp_remove(request):
    PartnerProfile.objects.update_or_create(p_user = request.user.id, defaults={ "p_business_stamp" : ""})
    return redirect(partner_general_setting)

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_digital_signature_remove(request):
    PartnerProfile.objects.update_or_create(p_user = request.user.id, defaults={ "p_digital_signature" : ""})
    return redirect(partner_general_setting)




@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_cropped_logo_upload(request):

    if request.method == 'POST':

        form = partneruploadlogoForm(data=request.POST, files=request.FILES)
        if form.is_valid():

            setting_id = request.POST['partner_setting_logo_modal_id']
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
                    # print(str_value)
                    x = str_value.get('x')
                    y = str_value.get('y')
                    w = str_value.get('width')
                    h = str_value.get('height')
                    rotate = str_value.get('rotate')

            # print('x: {}, y: {}, w: {}, h: {}, rotate: {}'.format(
            #     x, y, w, h, rotate))

            im = Image.open(
                request.FILES['partnerlogofile']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            newdoc = PartnerProfile.objects.get(id=setting_id)
            newdoc.p_business_logo.save('partner_logo.png', image_file)
            newdoc.save()
            # data = {
            #     'result': True,
            #     'state': 200,
            #     'message': 'Success',
            # }

            # # redirect("/general-setting/")

            # return JsonResponse({'data': data})
            sweetify.success(request, title="Success...", icon='success', text='Logo updated successfully...', timer=1500)
            return redirect(partner_general_setting)

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_cropped_stamp_upload(request):
    if request.method == 'POST':

        form = partneruploadstampForm(data=request.POST, files=request.FILES)
        print(form)
        if form.is_valid():

            setting_id = request.POST['partner_setting_stamp_modal_id']

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
                request.FILES['partnerstampfile']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            newdoc = PartnerProfile.objects.get(id=setting_id)
            newdoc.p_business_stamp.save('partner_stamp_image.png', image_file)
            newdoc.save()
            # data = {
            #     'result': True,
            #     'state': 200,
            #     'message': 'Success',
            # }

            # # redirect("/general-setting/")

            # return JsonResponse({'data': data})
            sweetify.success(request, title="Success...", icon='success', text='Stamp updated successfully...', timer=1500)
            return redirect(partner_general_setting)


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_cropped_signature_upload(request):
    if request.method == 'POST':
        form = partneruploadsignatureForm(
            data=request.POST, files=request.FILES)
        if form.is_valid():
            img_data = dict(request.POST.items())
            setting_id = request.POST['partner_setting_signature_modal_id']
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
                request.FILES['partnersignaturefile']).convert('RGBA')

            tempfile = im.rotate(-rotate, expand=True)
            tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
            tempfile_io = BytesIO()
            tempfile_io.seek(0, os.SEEK_END)
            tempfile.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(
                tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

            newdoc = PartnerProfile.objects.get(id=setting_id)
            newdoc.p_digital_signature.save(
                'p_digital_signature.png', image_file)
            newdoc.save()
            # data = {
            #     'result': True,
            #     'state': 200,
            #     'message': 'Success',
            # }

            # # redirect("/general-setting/")

            # return JsonResponse({'data': data})
            sweetify.success(request, title="Success...", icon='success', text='Signature updated successfully...', timer=1500)
            return redirect(partner_general_setting)



@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partnerSmsSetting(request):
    if request.method == "POST":

        template_header_id = request.POST.get('template_header_id')

        if template_header_id == '0':
            type_header = request.POST.get('transactional')

            if type_header == 'transactional':
                request_header = request.POST.get('request_header_trans')
            elif type_header == 'promotional':
                request_header = request.POST.get('request_header_promo')

            sms_header = smsHeaderModel.objects.filter(request_user = request.user, header_content = request_header)

            if sms_header:
                sweetify.error(request, title="error", icon='error', text='Sms Header is already exists !!!', timer=1000)
                return redirect('/partner-sms-setting/')
            else:
                header = smsHeaderModel.objects.create(header_content= request_header, request_user = request.user, status = 'Approved', Active_status = True, header_type=type_header)
                if header:
                    sweetify.success(request, title="Success", icon='success', text='SMS Header Stored Successfully !!!')
                    return redirect('/partner-sms-setting/')
                else:
                    sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
                    return redirect('/partner-sms-setting/')

        else:
            template_content = request.POST.get('template_content')
            sms_template = templateContentModel.objects.filter(request_user = request.user, template_content = template_content, status = 'Approved')
            if sms_template:
                sweetify.error(request, title="error", icon='error', text='Sms Template is already exists !!!', timer=1000)
                return redirect('/partner-sms-setting/')
            else:
                sms_header = request.POST['sms_header_value']
                sms_header_new = sms_header.split(",")
                template_id = request.POST['template_id']
                template = templateContentModel.objects.create(template_content= template_content, request_user = request.user, status = 'Approved', sms_header = sms_header_new, template_id=template_id)

                if template:
                    sweetify.success(request, title="Success", icon='success', text='SMS Template Stored Successfully !!!')
                    return redirect('/partner-sms-setting/')
                else:
                    sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
                    return redirect('/partner-sms-setting/')
    data = smsHeaderModel.objects.filter(request_user = request.user).order_by('-id')
    Template = templateContentModel.objects.filter(request_user = request.user).order_by('-id')
    for obj in Template:
        if obj.sms_header:
            temp_sms_header = ""
            temp_sms_header = obj.sms_header.replace("[", "")
            temp_sms_header = temp_sms_header.replace("]", "")
            temp_sms_header = temp_sms_header.replace("'", "")
            obj.sms_header = temp_sms_header
    context = {
        'data': data,
        'Template': Template,
        'SettingNavclass': "active",
        'settingsCollapseShow': "show",
        'PartnerSmsSettingsNavclass': "active"
    }
    return render(request, "partner/partner_sms_setting.html", context)

    #     form = PartnerSmsSettingForm(request.POST)

    #     if form.is_valid():
    #         user_id = form.cleaned_data.get("user_id")
    #         sms_header = form.cleaned_data.get("sms_header")
    #         status = form.cleaned_data.get("status")

    #         result = PartnerSmsSetting.objects.update_or_create(sms_header=sms_header, defaults={'user_id': user_id, 'sms_header': sms_header, 'status': status})

    #         if result:
    #             sweetify.success(request, title="Success", icon='success', text='SMS Settings Stored Successfully !!!')
    #             return redirect('/partner-sms-setting/')
    #         else:
    #             sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
    #             return redirect('/partner-sms-setting/')
    #     else:
    #         sweetify.error(request, title="error", icon='error', text='Failed !!!', timer=1000)
    #         return redirect('/partner-sms-setting/')
    # else:
    #     form = PartnerSmsSettingForm()
    #     data = PartnerSmsSetting.objects.filter(user_id = request.user.id).order_by('-id')
        
    #     if data:
    #         context = {
    #             'form': form, 
    #             'data': data,
    #             'SettingNavclass': "active",
    #             'settingsCollapseShow': "show",
    #             'ParntnerSmsSettingsNavclass': "active"
    #         }
    #         return render(request, "partner/partner_sms_setting.html", context)
    #     else:
    #         data = ""
            # context = {
            #     'form': form, 
            #     'data': data,
            #     'SettingNavclass': "active",
            #     'settingsCollapseShow': "show",
            #     'PartnerSmsSettingsNavclass': "active"
            # }
            # return render(request, "partner/partner_sms_setting.html", context)


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def deletepartnerSmsHeader(request, id):
    if request.method == "POST":
        instance = smsHeaderModel.objects.get(id=id)
        user = instance.request_user
        header = instance.header_content
        template = templateContentModel.objects.filter(request_user = user)

        for header_template in template:
            if header in header_template.sms_header:
                templates = templateContentModel.objects.get(id = header_template.id)
                templates.delete()
        instance.delete()
        return JsonResponse({'status': 'success', 'msg': 'Header deleted successfully'})
    else:
        return JsonResponse({"status": "error", 'msg': "Something went wrong"})

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def activepartnersmsheader(request, id):
    if request.method == "POST":
        result1 = smsHeaderModel.objects.filter(request_user = request.user).update(Active_status = False)
        result2 = smsHeaderModel.objects.filter(id = id).update(Active_status = True)
        return JsonResponse({'status': 'success', 'msg': 'Status change successfully'})
    else:
        return JsonResponse({'status': 'error', 'msg': 'Something went wrong'})

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def deleteSmstemplatebypartner(request, id):
    if request.method == "POST":
        instance = templateContentModel.objects.get(id=id)
        instance.delete()
        return JsonResponse({'status': 'success', 'msg': 'Template deleted successfully'})
    else:
        return JsonResponse({"status": "error", 'msg': "Something went wrong"})


@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def changeSmsHeaderStatusDisable(request, id):
    if request.method == "POST":
        result = PartnerSmsSetting.objects.filter(
            id=id, user_id=request.user.id).update(status=0)
        return JsonResponse({'status': 'success', 'msg': 'Status change successfully'})
    else:
        return JsonResponse({'status': 'error', 'msg': 'Something went wrong'})

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def changeSmsHeaderStatusEnable(request, id):
    if request.method == "POST":
        result = PartnerSmsSetting.objects.filter(
            id=id, user_id=request.user.id).update(status=1)
        return JsonResponse({'status': 'success', 'msg': 'Status change successfully'})
    else:
        return JsonResponse({'status': 'error', 'msg': 'Something went wrong'})

@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def deleteSmsHeader(request, id):
    if request.method == "POST":
        instance = PartnerSmsSetting.objects.get(id=id)
        instance.delete()
        return JsonResponse({'status': 'success', 'msg': 'Header deleted successfully'})
    else:
        return JsonResponse({"status": "error", 'msg': "Something went wrong"})




@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def partner_payment_setting(request):

    partner_id = Partner_users.objects.filter(user_id=request.user).values('partner_user_id')[0]['partner_user_id']

    # partner_business_object = PartnerProfile.objects.get(p_user=partner_id)
    
    if request.method == "POST":

        form = PaymentSettingForm(request.POST)
        
        if form.is_valid():
            payu_key = form.cleaned_data.get("payu_key")
            payu_salt = form.cleaned_data.get("payu_salt")

            PartnerPaymentSetting.objects.update_or_create(partner_id = partner_id, defaults={'payu_key': payu_key, 'payu_salt': payu_salt })

            sweetify.success(request, title="Success", icon='success', text='Payment Setting Stored Successfully !!!')
            return redirect('/partner-payment-settings/')

        else:
            sweetify.error(request, title="error", icon='error', text='Failed !!!')
            return redirect('/partner-payment-settings/')
    else:

        try:
            data = PartnerPaymentSetting.objects.get(partner_id = partner_id)
        except:
            data = ""

        form = PaymentSettingForm()

        context = {
            'form' : form, 
            'data' : data,
            "SettingNavclass": "active",
            "settingsCollapseShow": "show",
            'paymentSettingActiveClass': "active"
        }

        return render(request, "partner/payment_setting.html", context)
