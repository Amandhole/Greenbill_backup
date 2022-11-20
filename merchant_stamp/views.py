from django.shortcuts import render, redirect
from django import forms
from .models import StampModel
from .forms import *
from owner_stamp.models import wstampmodels
from merchant_stamp.models import *
from users.models import *
import sweetify
from django.http import HttpResponse, JsonResponse
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import json
import os
def stamp_cropped_image_upload(request):
    img_data = dict(request.POST.items())
    stamp_name = request.POST.get('own_stamp_name')

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

    im = Image.open(
        request.FILES['merchantlogofile']).convert('RGBA')

    tempfile = im.rotate(-rotate, expand=True)
    tempfile = tempfile.crop((int(x), int(y), int(w+x), int(h+y)))
    tempfile_io = BytesIO()
    tempfile_io.seek(0, os.SEEK_END)
    tempfile.save(tempfile_io, format='PNG')
    image_file = InMemoryUploadedFile(
        tempfile_io, None, 'rotate.png', 'image/png', tempfile_io.tell(), None)

    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
       
    merchantstampupload.objects.create(merchant_user = request.user, merchant_business_id = merchant_business_id, m_business_stamp = image_file, stamp_name=stamp_name)

    data = {
        'result': True,
        'state': 200,
        'message': 'Success',
    }

    # redirect("/general-setting/")

    return JsonResponse({'data': data})


def stampview(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    # print('merchant_business_id',merchant_business_id)
    if request.method == "POST":

        stamp_one_id = request.POST.getlist('chk[]')

        result = merchantusagestamp.objects.create(merchant_user_id = request.user, merchant_business_id = merchant_business_id, merchant_stamp_id_one = stamp_one_id)
        
        if result:
            sweetify.success(request, title="Saved", icon='success', text='Stamp Saved Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to save.', timer=1000)
    status = wstampmodels.objects.all().order_by('-id')
    
    try:
        saved_stamp = merchantusagestamp.objects.filter(merchant_user_id = request.user, merchant_business_id = merchant_business_id).last()

        stamp_checked_ids = saved_stamp.merchant_stamp_id_one
    except:
        stamp_checked_ids = ''

    if stamp_checked_ids:
        temp_stamp = ""
        temp_stamp = stamp_checked_ids.replace("[", "")
        temp_stamp = temp_stamp.replace("]", "")
        temp_stamp = temp_stamp.replace("'", "")
        stamp_checked_ids = temp_stamp


    new_stamp_id = stamp_checked_ids.split(", ")
    id1 = 0
    id2 = 0
    id3 = 0
    id4 = 0
    id5 = 0
    for stamp in new_stamp_id:
        if stamp:
            if id1 == 0:
                id1 = int(stamp)
            elif id2 == 0:
                id2 = int(stamp)
            elif id3 == 0:
                id3 = int(stamp)
            elif id4 == 0:
                id4 = int(stamp)
            elif id5 == 0:
                id5 = int(stamp)

    for stamp1 in status:
        if stamp1:
            s_id = int(stamp1.id)
            if s_id == id1 or s_id == id2 or s_id == id3 or s_id == id4 or s_id == id5:
                stamp1.is_check = 0
            else:
                stamp1.is_check = 1

    try:
        selected = selectstampimage.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id).last()
        checked_stamp_image = int(selected.m_select_image)
    except:
        checked_stamp_image = ''
  
    stamp_uploaded_image = merchantstampupload.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)

    if stamp_uploaded_image:
        for object1 in stamp_uploaded_image:
            img_id = int(object1.id)
    else:
        img_id = ''

    return render(request, "merchant/merchant_mystamp/mystamp.html", {'img_id': img_id, 'checked_stamp_image': checked_stamp_image, 'stamp_uploaded_image': stamp_uploaded_image, 'status': status, "DesignNavclass": "active", "DesignCollapseShow": "show", 'StampNavclass':'active'})


def save_merchant_stampImage(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    # check_status = merchantstampupload.objects.filter(merchant_user = merchant_object, merchant_business_id = merchant_business_id)

    if request.method == 'POST':
        form = stampuploadForms(request.POST, request.FILES)
        stamp_image = request.FILES['stamp_image']
        
        # if check_status:
        #     image1 = merchantstampupload.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id).update(m_business_stamp = stamp_image)
        # else:
        merchantstampupload.objects.create(merchant_user = request.user, merchant_business_id = merchant_business_id, m_business_stamp = stamp_image)

        sweetify.success(request, title="Success", icon='success', text='Stamp uploaded Successfully.', timer=1500)
    return redirect(stampview)

def DeleteMerchantOwnStamp(request, id):
    result = merchantstampupload.objects.filter(id = id).delete()
    if result:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": False})


def save_image_select(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    selected = selectstampimage.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id)

    if request.method == "POST":

        select_img = request.POST["select_img"]

        if selected:
            selectstampimage.objects.filter(merchant_user = request.user, merchant_business_id = merchant_business_id).update(m_select_image = select_img)
        else:

            selectstampimage.objects.create(merchant_user = request.user, merchant_business_id = merchant_business_id, m_select_image = select_img)
        sweetify.success(request, title="Success", icon='success', text='Stamp saved Successfully.', timer=1500)



    return redirect(stampview)



    
           