from django.shortcuts import render
from .models import *
from .forms import *
from app.views import is_merchant_or_merchant_staff, is_owner
from django.contrib.auth.decorators import login_required, user_passes_test
import sweetify
from django.shortcuts import render, get_object_or_404, redirect
from role.models import role, userrole
# Create your views here.

@login_required(login_url="/login/")
@user_passes_test(is_owner)
def Get_Referral_points(request):
    if request.method == "POST":
        form = referralForm(request.POST, request.FILES)

        if form.is_valid():
            referrer_merchant_amount = form.cleaned_data.get("recharge_amount_per_refferal")
            referent_merchan_amount = form.cleaned_data.get("recharge_amount_per_referent")
            temp = ReferralModel.objects.update_or_create(id=1, defaults={'recharge_amount_per_refferal': referrer_merchant_amount, 'recharge_amount_per_referent': referent_merchan_amount})

            sweetify.success(request, title="Success", icon='success',
                             text='Referral Points Stored Successfully !!!')
            return redirect('/referral-points/')
        else:
            sweetify.error(request, title="error",
                           icon='error', text='Failed !!!')
    else:
        user = request.user
        if ReferralModel.objects.all():
            data = ReferralModel.objects.latest('id')
        else:
            data = None
            
        form = referralForm()

        context = {
            'form' : form,
            'data': data,
            "SettingsNavclass": "active",
            "settingsCollapseShow":"show",
            "ReferralProgramActiveClass":"active"
        }
        
        return render(request, "super_admin/referral_points/owner-referral-points.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_owner)
def add_promotions_amount(request):
    if request.method == "POST":
        offers_amount = request.POST['offers_amount']
        coupon_amount = request.POST['coupon_amount']
        third_party_ads_amount = request.POST['third_party_ads_amount']
        green_bill_ads_amount = request.POST['green_bill_ads_amount']

        temp = PromotionsAmount.objects.update_or_create(id=1, defaults={'offer_amount': offers_amount, 'coupon_amount' : coupon_amount, 'third_party_ads_belowbill_amount': third_party_ads_amount, 'green_bill_ads_belowbill_amount': green_bill_ads_amount})

        sweetify.success(request, title="Success", icon='success',
                         text='Promotions Amount Stored Successfully !!!')
        return redirect('/add-promotions-amount/')
    try:
        if ReferralModel.objects.all():
            data = PromotionsAmount.objects.latest('id')
    except:
        data = ''
    

    context = {
        'data': data,
        "SettingsNavclass": "active",
        "settingsCollapseShow":"show",
        "PromotionsAmountActiveClass":"active"
    }

    return render(request, "super_admin/promotions_amount/add-promotions-amount.html", context)