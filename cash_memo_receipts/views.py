from django.shortcuts import render, redirect
from .models import Cash_Memos, Receipts_Model
from .forms import Cash_Memo_Form, ReceiptsForm
import sweetify
from django.http import JsonResponse
from merchant_cashmemo_design.models import Cash_Memo_Design_Model
from users.models import MerchantProfile
from merchant_promotion.models import smsHeaderModel, templateContentModel
# Create your views here.


def Cash_memos(request):
    all_cash_memo = Cash_Memos.objects.all().order_by('-id')
    context = {
        "cash_memo": all_cash_memo,
        'CashMemosNavClass': 'active',
        'CashNavClass': 'active',
        'CashMemosCollapseShow': 'show',

    }
    if request.method == "POST":
        memo_form = Cash_Memo_Form(request.POST, request.FILES)
        if memo_form.is_valid():
            Cash_Memos.objects.create(

                memo_name=memo_form.cleaned_data['memo_name'],
                header_text=memo_form.cleaned_data['header_text'],
                footer_text=memo_form.cleaned_data['footer_text'],
                stamp_image=memo_form.cleaned_data['stamp_image'],
                fav_color=memo_form.cleaned_data['favcolor']

            ).save()
            sweetify.success(request, title="Success", icon='success',
                             text='Cash Memo Saved', timer=1500)

    return render(request, "super_admin/cash_memo_owner/cash-memo-template.html", context)


def Delete_Cash_Memo(request, id):
    instance = Cash_Memos.objects.get(id=id)
    status = instance.delete()
    if status:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def Edit_Cash_Memo(request):
    if request.method == "POST":
        c_id = request.POST['mid']
        print(c_id)
        edit_memo_name = request.POST['edit_memo_name']
        edit_header_name = request.POST['edit_header_text']
        edit_footer_name = request.POST['edit_footer_text']
        try:
            edit_stamp_logo = request.FILES['edit_stamp']
        except:
            edit_stamp_logo = ""
        edit_color = request.POST['favcolor']
        if edit_stamp_logo:
            cash_memo_obj = Cash_Memos.objects.get(id=c_id)
            Cash_Memos.objects.filter(id=c_id).update(
                memo_name=edit_memo_name, header_text=edit_header_name, footer_text=edit_footer_name, fav_color=edit_color)
            cash_memo_obj.stamp_image = edit_stamp_logo
            cash_memo_obj.save()
        else:
            Cash_Memos.objects.filter(id=c_id).update(
                memo_name=edit_memo_name, header_text=edit_header_name, footer_text=edit_footer_name, fav_color=edit_color)

        sweetify.success(request, title="Success", icon='success',
                         text='Cash Memo Updated', timer=1500)
        return redirect("/cash-memo/")


def All_Cash_Memo_Design(request):
    """ This code for Display all data for super user"""
    qs = Cash_Memo_Design_Model.objects.all().order_by('-id')
    unread_count = Cash_Memo_Design_Model.objects.filter(
        read_status=False).count()
    update_read_status = Cash_Memo_Design_Model.objects.filter(
        read_status=False)
    update_read_status.update(read_status=True)
    for all in qs:
        design_object = MerchantProfile.objects.filter(m_user = all.merchant_user)
        for object in design_object:
            all.m_business_name = object.m_business_name
            print('aaa')
    if request.method == "POST":
        # if 'statusSubmit' in request.POST:
        status = request.POST.get('status')
        notes = request.POST.get('notes')
        print('status',status)
        status_id = request.POST.get('status_id')
        obj = request.POST.get('object_status_id')
        print('obj',obj)
        print('id',status_id)
        upate_status = Cash_Memo_Design_Model.objects.filter(id=int(obj)).update(status = status,notes = notes)
        if upate_status:
            sweetify.success(request, title="Success", icon='success',
                                text='Status and notes Updated Successfully !!!')
            return redirect(All_Cash_Memo_Design)
        else:
            sweetify.error(request, title="error",
                            icon='error', text='Failed !!!')

    
    context = {
        "memo_list": qs,
        "MerchantRequestNavclass": "active",
        "MerchantRequestCollapseShow": "show",
        "MerchantBillDesignRequestNavclass": "active"
    }
    return render(request, "super_admin/cash_memo_owner/owner_cash_memo_design.html", context)


def Create_Receipts(request):

    if request.method == "POST":
        receipts_form = ReceiptsForm(request.POST, request.FILES)
        if receipts_form.is_valid():
            Receipts_Model.objects.create(

                receipts_name=receipts_form.cleaned_data['receipts_name'],
                header_text=receipts_form.cleaned_data['header_text'],
                footer_text=receipts_form.cleaned_data['footer_text'],
                stamp_image=receipts_form.cleaned_data['stamp_image'],
                fav_color=receipts_form.cleaned_data['favcolor']

            ).save()
            sweetify.success(request, title="Success", icon='success',
                             text='Receipts Saved Successfully', timer=1500)
    all_receipts = Receipts_Model.objects.all()
    context = {
        "receipts": all_receipts,
        'ReceiptNavClass': 'active',
        'CashMemosNavClass': 'active',
        'CashMemosCollapseShow': 'show',

    }
    # return render(request, "super_admin/cash_memo_owner/owner_receipts.html", context)
    return render(request, "super_admin/cash_memo_owner/receipt-template.html", context)



def Edit_Receipts(request):
    if request.method == "POST":
        c_id = request.POST['mid']
        print(c_id)
        edit_receipts_name = request.POST['edit_receipts_name']
        edit_header_name = request.POST['edit_header_text']
        edit_footer_name = request.POST['edit_footer_text']
        try:
            edit_stamp_logo = request.FILES['edit_stamp']
        except:
            edit_stamp_logo = ""
        edit_color = request.POST['favcolor']
        if edit_stamp_logo:
            cash_memo_obj = Receipts_Model.objects.get(id=c_id)
            Receipts_Model.objects.filter(id=c_id).update(
                receipts_name=edit_receipts_name, header_text=edit_header_name, footer_text=edit_footer_name, fav_color=edit_color)
            cash_memo_obj.stamp_image = edit_stamp_logo
            cash_memo_obj.save()
        else:
            Receipts_Model.objects.filter(id=c_id).update(
                receipts_name=edit_receipts_name, header_text=edit_header_name, footer_text=edit_footer_name, fav_color=edit_color)

        sweetify.success(request, title="Success", icon='success',
                         text='Receipts Updated', timer=1500)
        return redirect("/create-receipts/")


def Delete_Receipts(request, id):
    instance = Receipts_Model.objects.get(id=id)
    status = instance.delete()
    if status:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def smsHeaderrequest(request):
    qs = smsHeaderModel.objects.all().order_by('-id')
    # print('sms header',qs)
    if request.method == "POST":
        update_status = request.POST.get('status')
        # print('status',status)
        status_id = request.POST.get('status_id')
        obj = request.POST.get('object_status_id')
        print('obj',obj)
        print('id',status_id)
        upate_status = smsHeaderModel.objects.filter(id=int(obj)).update(status = update_status)
        if upate_status:
            sweetify.success(request, title="Success", icon='success',
                                text='Status Updated Successfully !!!')
            return redirect(smsHeaderrequest)
        else:
            sweetify.error(request, title="error",
                            icon='error', text='Failed !!!')
      
    context ={
    'all':qs,
    'MerchantRequestNavclass':'active',
    'MerchantRequestCollapseShow':'show',
    'SmsHeaderRequestNavClass':'active',
    }
    return render(request,'super_admin/cash_memo_owner/sms-header-request.html', context)
def smsTemplaterequest(request):
    qs = templateContentModel.objects.all().order_by('-id')
    # print('sms template',qs)
    if request.method == "POST":
        update_status = request.POST.get('status')
        # print('status',status)
        status_id = request.POST.get('status_id')
        obj = request.POST.get('object_status_id')
        print('obj',obj)
        print('id',status_id)
        upate_status = templateContentModel.objects.filter(id=int(obj)).update(status = update_status)
        if upate_status:
            sweetify.success(request, title="Success", icon='success',
                                text='Status Updated Successfully !!!')
            return redirect(smsTemplaterequest)
        else:
            sweetify.error(request, title="error",
                            icon='error', text='Failed !!!')
      
    context ={
    'all':qs,
    'MerchantRequestNavclass':'active',
    'MerchantRequestCollapseShow':'show',
    'SmsTemplateRequestNavClass':'active',
    }
    return render(request, 'super_admin/cash_memo_owner/sms-template-request.html',context)