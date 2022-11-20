from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff, is_owner
from .models import *
from users.models import GreenBillUser, Merchant_users, MerchantProfile
from django.http import HttpResponse, JsonResponse

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def suggestPetrolPump(request):

    user_id =  request.user.id

    mer_user_id = Merchant_users.objects.get(user_id=request.user)

    merchant_object = mer_user_id.merchant_user_id

    business_object = MerchantProfile.objects.filter(m_user = merchant_object, m_active_account = True)

    m_business_id = business_object[0].id

    business_list = SuggestBusiness.objects.filter(m_business_id = m_business_id, user_id = user_id).order_by('-id')

    context = {
        "m_business_id" : m_business_id,
        "user_id" : user_id,
        "business_list" : business_list,
		"SuggestPetrolPumpNavclass": "active"
	}

    return render(request, "merchant/suggest/suggest-petrol-pump.html",context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def suggestParking(request):
    user_id =  request.user.id

    mer_user_id = Merchant_users.objects.get(user_id=request.user)

    merchant_object = mer_user_id.merchant_user_id

    business_object = MerchantProfile.objects.filter(m_user = merchant_object, m_active_account = True)

    m_business_id = business_object[0].id

    business_list = SuggestBusiness.objects.filter(m_business_id = m_business_id, user_id = user_id).order_by('-id')

    context = {
        "m_business_id" : m_business_id,
        "user_id" : user_id,
        "business_list" : business_list,
        "SuggestParkingNavclass": "active"
    }

    return render(request, "merchant/suggest/suggest-parking.html",context)


@login_required(login_url="/login/")
@user_passes_test(is_owner)
def suggestBusinessList(request):

    business_list = SuggestBusiness.objects.all().order_by('-id')

    for business in business_list:
        try:
            user_oject = GreenBillUser.objects.filter(id = business.user_id)
            suggested_by = user_oject[0].first_name + " " + user_oject[0].last_name
            mobile_no =  user_oject[0].mobile_no
        except:
            suggested_by = ""
            mobile_no = ""

        business.suggested_by = suggested_by
        business.suggested_by_mobile_no = mobile_no

    context = {
        "business_list" : business_list,
        "SuggestedBusinessNavclass": "active",
    }

    return render(request, "super_admin/suggest/suggest-business.html", context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def suggestNewBusiness(request):

    m_business_id = request.POST['m_business_id']
    user_id = request.POST['user_id']

    suggested_business_name = request.POST['suggested_business_name']
    contact_no = request.POST['contact_no']
    address = request.POST['address']

    result = SuggestBusiness.objects.create(m_business_id = m_business_id, user_id = user_id, suggested_business_name = suggested_business_name, contact_no = contact_no, address = address)

    if result:
        return JsonResponse({'status': 'success', 'message': 'Business suggested Successfully !!!'}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Failed to suggest !!!'}, status=400)
