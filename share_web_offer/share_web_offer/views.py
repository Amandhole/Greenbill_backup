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

# Create your views here.

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def share_image(request):
    if request.method == "POST":
        form = OfferImageForm(request.POST, request.FILES)
        letters = string.ascii_letters
        digit = string.digits
        obj1 = ""
        obj2 = ""
        random_string = str(obj2) + ''.join(random.choice(letters) for i in range(4)) + ''.join(random.choice(digit) for i in range(3)) + ''.join(random.choice(letters) for i in range(2))
        if request.POST['offer_id'] != "":
            share_offer_image = request.POST['share_offer_image']
            obj1 = ShareOfferModel.objects.update_or_create(
                id=int(request.POST["offer_id"]), defaults={"share_offer_image": share_offer_image})
        else:
            share_offer_image = request.FILES['share_offer_image']
            obj2 = ShareOfferModel.objects.create(share_offer_image=share_offer_image, offer_url=random_string)
        if obj1:
            sweetify.success(request, title="Success", icon='success',
                             text='Offers updated Successfully.', timer=1500)

        elif obj2:
            sweetify.success(request, title="Success", icon='success',
                             text='Offers created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...",
                             icon='error', text='Fail to create.', timer=1000)
    
    data = ShareOfferModel.objects.all()
    context = {
    'data': data, 
    'WebOffersNavclass': 'active',  
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