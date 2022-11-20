from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.views import is_merchant_or_merchant_staff, is_partner
from django.contrib.auth.decorators import login_required, user_passes_test
from offers.models import OfferModel
from .models import ShareOfferModel
from .forms import OfferImageForm
import sweetify
import random
import string
from users.models import *
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def share_image(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_user_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    if request.method == "POST":
        form = OfferImageForm(request.POST, request.FILES)
        letters = string.ascii_letters
        digit = string.digits
        web_offer_id = request.user
        obj1 = ""
        obj2 = ""
        random_string = str(obj2) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
        if request.POST['offer_id'] != "":
            share_offer_image = request.POST['share_offer_image']
            obj1 = ShareOfferModel.objects.update_or_create(
                id=int(request.POST["offer_id"]), defaults={"share_offer_image": share_offer_image})
        else:
            share_offer_image = request.FILES['share_offer_image']
            obj2 = ShareOfferModel.objects.create(merchant_business_id = merchant_business_id, merchant=request.user, share_offer_image=share_offer_image, offer_url=random_string)
        if obj1:
            sweetify.success(request, title="Success", icon='success',
                             text='Offers updated Successfully.', timer=1500)

        elif obj2:
            sweetify.success(request, title="Success", icon='success',
                             text='Offers created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...",
                             icon='error', text='Fail to create.', timer=1000)
    
    data = ShareOfferModel.objects.filter(merchant=request.user, merchant_business_id = merchant_business_id).order_by('-id')
    context = {
    'data': data, 
    'OfferforWebNavclass': 'active', 
     'PromotionsNavclass': "active", 
        'ShowPromotionsNavclass': "show", 
    }
    return render(request, "merchant/share_web_offer/share-web-offer.html", context)


def web_offer_by_id(request, id):
    data = []

    base_url = "http://157.230.228.250/"
    offer_details = ShareOfferModel.objects.filter(offer_url=id)
    print(offer_details)
    context = {
    'offer_details': offer_details,   
    }
    return render(request, "merchant/share_web_offer/view-web-offer.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def Delete_web_offer(request, id):
    instance = ShareOfferModel.objects.get(id=id)
    
    instance.delete()
    return JsonResponse({'success': True})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff)
def set_active_web_offer(request):
    if request.method == "POST":

        id = request.POST["web_offer_id"]
        

        mer_user_id = Merchant_users.objects.get(user_id=request.user)

        merchant_object = mer_user_id.merchant_user_id

        merchant_user_object = Merchant_users.objects.get(user_id = request.user)

        merchant_object = merchant_user_object.merchant_user_id

        merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

        
        sweetify.success(request, title="success", icon='success', text='Ads Set Successfully !!!', timer=1500)
        result1 = ShareOfferModel.objects.filter(merchant = request.user, merchant_business_id = merchant_business_id).update(active_web_offer = False)

        result2 = ShareOfferModel.objects.filter(id = id).update(active_web_offer = True)

        if result1 and result2:
            sweetify.success(request, title="success", icon='success', text='Web Offer Active Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="error", icon='error', text='Failed to Active Web Offer!!!', timer=1500)
            

        return redirect(share_image)
    else: 
        sweetify.error(request, title="error", icon='error', text='Failed to Active Web Offer!!!', timer=1500)
        return redirect(share_image)
