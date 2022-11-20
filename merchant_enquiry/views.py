from django.shortcuts import render, redirect
from .models import MerchantEnquiryModel
from .forms import MerchantEnquiryForm
from django.http import HttpResponse, JsonResponse
import sweetify
from users.models import MerchantProfile, Merchant_users
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff, is_owner
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, BadHeaderError, EmailMultiAlternatives
from super_admin_settings.models import ManageCompaniesDMR
# Create your views here.


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def Merchant_Enquiry(request):
    enquiry_form = MerchantEnquiryForm()
    enquiry_data = MerchantEnquiryModel.objects.filter(mer_id=request.user)
    m_business = MerchantProfile.objects.filter(m_user=request.user)

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

    all_business = MerchantProfile.objects.filter(m_user=merchant_id, m_active_account = True)

    context = {
        'enq_form': enquiry_form,
        'enq_data': enquiry_data,
        'm_business': m_business,
        'merchant_data': all_business[0],
        'PromotionsNavclass': "active", 
        'ShowPromotionsNavclass': "show",
        'MerchantEnquiryNavClass': 'active',
        
    }
    if request.method == 'POST':
        enquiry_form = MerchantEnquiryForm(request.POST)
        customer_name = request.POST.get('customer_name')
        bissiness_name = request.POST.get('bissiness_name')
        contact_no = request.POST.get('contact_no')
        email_id = request.POST.get('email_id')
        intrested_in = request.POST.getlist('intrested_in[]')
        comments = request.POST.get('comments')
        print('intrested_in',intrested_in)
        user  = MerchantEnquiryModel.objects.create(
                mer_id=request.user,
                customer_name=customer_name,          
                 bissiness_name=bissiness_name,
                contact_no=contact_no,
                email_id=email_id,
                intrested_in=intrested_in,
                comments=comments,
                enquary_status="Active",
            )
        # if enquiry_form.is_valid():
        #     #  Merchant Digital Enquirty

        #     customer_name = enquiry_form.cleaned_data['customer_name']
        #     bissiness_name = enquiry_form.cleaned_data['bissiness_name']
        #     contact_no = enquiry_form.cleaned_data['contact_no']
        #     email_id = enquiry_form.cleaned_data['email_id']
        #     intrested_in = enquiry_form.cleaned_data['intrested_in']
        #     comments = enquiry_form.cleaned_data['comments']
        #     user = MerchantEnquiryModel.objects.create(
        #         mer_id=request.user,
        #         customer_name=enquiry_form.cleaned_data['customer_name'],
        #         bissiness_name=enquiry_form.cleaned_data['bissiness_name'],
        #         contact_no=enquiry_form.cleaned_data['contact_no'],
        #         email_id=enquiry_form.cleaned_data['email_id'],
        #         intrested_in=enquiry_form.cleaned_data['intrested_in'],
        #         comments=enquiry_form.cleaned_data['comments'],
        #         enquary_status="Active",
        #     )
        #     user.save()
            # mer_data = merchant_data[0]
            # subject = 'Merchant DM Inquiry'
            # message = f'Dear Green Bill Team,\n Please find the Digital Marketing Inquiries raised by merchant. \n Merchant Name:{mer_data.m_user.first_name} \n Merchant Category: {bissiness_name} \n Name:{customer_name} \n Email Id:{email_id} \n Mobile Number:{contact_no} \n Interested In:{intrested_in} \n Notes:{comments}'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = ['lrahangdale6@gmail.com', ]
            # sendmail = EmailMessage(
            #     subject, message, email_from, recipient_list)
            # response = sendmail.send()
        if user:
            sweetify.success(request, title="Success", icon='success',
                             text='Enquiry Submitted SuccessFully', timer=1500)
            return render(request, 'merchant/merchant-enquiry/merchant-enquiry-form.html', context)
        else:
            sweetify.error(request, title="Error", icon='Error',
                           text='Something Went To Wrong', timer=1500)
            return redirect("/merchant-enquiry/")
    else:
        return render(request, 'merchant/merchant-enquiry/merchant-enquiry-form.html', context)


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Get_Merchant_Enquiry_Details(request):
    qs = MerchantEnquiryModel.objects.all().order_by('-id')

    for enquiry in qs:
        temp_intrested_in = ""
        temp_intrested_in = enquiry.intrested_in.replace("[", "")
        temp_intrested_in = temp_intrested_in.replace("]", "")
        temp_intrested_in = temp_intrested_in.replace("'", "")
        enquiry.intrested_in = temp_intrested_in

    qs_count = MerchantEnquiryModel.objects.all().count()
    unread_count = MerchantEnquiryModel.objects.filter(
        read_status=False).count()
    update_read_status = MerchantEnquiryModel.objects.filter(read_status=False)
    
    update_read_status.update(read_status=True)

    if request.method == "POST":
        status = request.POST.get('status')
        notes = request.POST.get('notes')

        notes_id = request.POST.get('notes_id')
        obj1 = request.POST.get('object_notes_id')
        status_id = request.POST.get('status_id')
        obj = request.POST.get('object_status_id')
        
        update_status = MerchantEnquiryModel.objects.filter(id=int(obj)).update(status = status)
        update_notes = MerchantEnquiryModel.objects.filter(id=int(obj)).update(notes = notes)
        print("NOTES",update_notes)
       
        if update_status:
            
            sweetify.success(request, title="Success", icon='success',
                                text='Status Updated Successfully !!!')
            return redirect(Get_Merchant_Enquiry_Details)
        else:
            sweetify.error(request, title="error",
                            icon='error', text='Failed !!!')

        #if update_notes:
            # sweetify.success(request, title="Status"='success')
    data = ManageCompaniesDMR.objects.all()
    print("AA",data)                            
    context = {
        "enquiry_list": qs,
        "status_count": qs_count,
        "assign_company" : data,
        "MerchantRequestNavclass": "active",
        "MerchantRequestCollapseShow": "show",
        "MerchantDigitalMarketingRequestNavClass": "active"
    }

    return render(request, 'merchant/merchant-enquiry/merchant-enquiry_details.html', context)



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def Delete_DM_Enquiry(request, id):
    dm_enquiry = MerchantEnquiryModel.objects.get(id=id)
    dm_enquiry.delete()
    return JsonResponse({'success': True})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Owner_Delete_Inquiry(request,id):
    dm_enquiry = MerchantEnquiryModel.objects.get(id=id)
    dm_enquiry.delete()
    return JsonResponse({'success': True})


    
@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Delete_Meltiple_Inquiry(request):
    dm_enquiry = MerchantEnquiryModel.objects.all()
    dm_enquiry.delete()
    return JsonResponse({'success': True})

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def assign_company_for_merchant_enq(request):
    if request.method == "POST":
        id = request.POST["disapprove_offer_id"]
        print("id",id)
        company_name = request.POST["company_name"] 
        data_status = MerchantEnquiryModel.objects.filter(id = id).update(assign_company = company_name)

        sweetify.success(request, title="success", icon='success', text='Assigned Company Successfully !!!', timer=1500)
        return redirect(Get_Merchant_Enquiry_Details)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to assign company!!!', timer=1500)
        return redirect(Get_Merchant_Enquiry_Details)