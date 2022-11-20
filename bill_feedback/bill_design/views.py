from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff 
from .models import *
import sweetify
from users.models import *
from django.http import HttpResponse, JsonResponse

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def bill_design_view(request):

    if request.method == "POST":
        logo_check = request.POST.get("logo_check")
        address_check = request.POST.get("address_check")

        rating_check = request.POST.get("rating_check")
        if rating_check == "show_rating":
            rating_status = True
            rating_text = request.POST["rating_text"]
            rating_emoji =  request.POST["rating_emoji"]
        # elif rating_check == "hide_rating":
        #     rating_status = False
        #     rating_text = ""
        #     rating_emoji =  ""
        else:
            rating_status = False
            rating_text = ""
            rating_emoji =  ""

        social_media_check = request.POST.getlist("social_media_check")


        if "facebook" in social_media_check:
            facebook_status = True
            facebook_url = request.POST["facebook_url"]
        else:
            facebook_status = False
            facebook_url = ""

        if "youtube" in social_media_check:
            youtube_status = True
            youtube_url = request.POST["youtube_url"]
        else:
            youtube_status = False
            youtube_url = ""

        if "twitter" in social_media_check:
            twitter_status = True
            twitter_url = request.POST["twitter_url"]
        else:
            twitter_status = False
            twitter_url = ""

        if "instagram" in social_media_check:
            instagram_status = True
            instagram_url = request.POST["instagram_url"]
        else:
            instagram_status = False
            instagram_url = ""
        if "linkedin" in social_media_check:
            linkedin_status = True
            linkedin_url = request.POST["linkedin_url"]
        else:
            linkedin_status = False
            linkedin_url = ""

        if "skype" in social_media_check:
            skype_status = True
            skype_url = request.POST["skype_url"]
        else:
            skype_status = False
            skype_url = ""

        if "google" in social_media_check:
            google_status = True
            google_url = request.POST["google_url"]
        else:
            google_status = False
            google_url = ""

        if "pinterest" in social_media_check:
            pinterest_status = True
            pinterest_url = request.POST["pinterest_url"]
        else:
            pinterest_status = False
            pinterest_url = ""
        if "snapchat" in social_media_check:
            snapchat_status = True
            snapchat_url = request.POST["snapchat_url"]
        else:
            snapchat_status = False
            snapchat_url = ""

        if "android" in social_media_check:
            android_status = True
            android_url = request.POST["android_url"]
        else:
            android_status = False
            android_url = ""

        if "apple" in social_media_check:
            apple_status = True
            apple_url = request.POST["apple_url"]
        else:
            apple_status = False
            apple_url = ""

        if "zomato" in social_media_check:
            zomato_status = True
            zomato_url = request.POST["zomato_url"]
        else:
            zomato_status = False
            zomato_url = ""

        if "swiggy" in social_media_check:
            swiggy_status = True
            swiggy_url = request.POST["swiggy_url"]
        else:
            swiggy_status = False
            swiggy_url = ""
            
        # ads_check =  request.POST["ads_check"]

        # if ads_check == "show":
        #     ads_status = True
        # elif ads_check == "hide":
        #     ads_status = False
        # else:
        #     ads_status = False

        ads_status = True

        contact_check =  request.POST.getlist("contact_check")

        if "phone" in contact_check:
            phone_status = True
            phone_number = request.POST["phone"]
        else:
            phone_status = False
            phone_number = ""

        if "website" in contact_check:
            website_status = True
            website_url = request.POST["website"]
        else:
            website_status = False
            website_url = ""
        
        if "map" in contact_check:
            map_status = True
            map_link = request.POST["map_link"]
        else:
            map_status = False
            map_link = ""

        terms_check =  request.POST.get("terms_check")

        if terms_check == "show":
            terms_status = True
            terms_url = request.POST["terms_url"]
        else:
            terms_status = False
            terms_url = ""

        pay_link_check = request.POST.get('pay_link_check')
        if pay_link_check == "show":
            pay_link = True
        else:
            pay_link = False
        # footer_check = request.POST["footer_check"]

        # if "show" in footer_check:
        #     footer_logo_status = True
        # else:
        #     footer_logo_status = False
        footer_logo_status = False

        merchant_user_object = Merchant_users.objects.get(user_id = request.user)

        merchant_object = merchant_user_object.merchant_user_id

        merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
        result = ''
        if len(social_media_check) == 0 or len(social_media_check) >= 4:
            result = bill_designs.objects.update_or_create(merchant_business_id = merchant_business_id, defaults={ "logo" : logo_check, 
                "address" : address_check, "rating" : rating_status, "rating_text" : rating_text, "rating_emoji" : rating_emoji,
                 "facebook" : facebook_status, "facebook_url" : facebook_url, "youtube" : youtube_status, "youtube_url" : youtube_url,
                  "twitter" : twitter_status, "twitter_url" : twitter_url, "instagram" : instagram_status, "instagram_url" : instagram_url,
                   "ads_below_bill" : ads_status, "phone" : phone_status, "phone_number" : phone_number, "website" : website_status, 
                   "website_url" : website_url, "map" : map_status, "map_link" : map_link, "terms_conditions" : terms_status, "terms_url" : terms_url,
                    "footer_logo" : footer_logo_status,"linkedin":linkedin_status,"linkedin_url":linkedin_url,"skype":skype_status,"skype_url":skype_url,
                    "google":google_status,"google_url":google_url,"pinterest":pinterest_status,"pinterest_url":pinterest_url,"snapchat":snapchat_status,
                    "snapchat_url":snapchat_url,"android":android_status,"android_url":android_url, "apple":apple_status, "apple_url": apple_url,
                    "zomato":zomato_status, "zomato_url": zomato_url,"swiggy":swiggy_status, "swiggy_url": swiggy_url,'pay_link':pay_link})
        else:
            result = bill_designs.objects.update_or_create(merchant_business_id = merchant_business_id, defaults={ "logo" : logo_check, 
            "address" : address_check, "rating" : rating_status, "rating_text" : rating_text, "rating_emoji" : rating_emoji,
               "ads_below_bill" : ads_status, "phone" : phone_status, "phone_number" : phone_number, "website" : website_status, 
               "website_url" : website_url, "map" : map_status, "map_link" : map_link, "terms_conditions" : terms_status, "terms_url" : terms_url,
                'pay_link':pay_link})

        # result = bill_designs.objects.create()

        if result:
            sweetify.success(request, title="Success", icon='success', text='Bill Design Set Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Failed to Set !!!', timer=1500)

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

    try:
        business_address = merchant_business_id.m_address
    except:
        business_address = ""

    try:
        bill_design_data = bill_designs.objects.get(merchant_business_id = merchant_business_id)
    except:
        bill_design_data = ""



    context = {
        "bill_design_data" : bill_design_data,
        "business_logo":business_logo,
        "business_address":business_address,
        "merchant_business_id":merchant_business_id,
        "DesignNavclass": "active",
        "DesignCollapseShow": "show",
        "BillDesignNavClass": "active"
    }

    return render(request, "merchant/bill_design/bill-design.html", context)




@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def auth_sign(request):
    user_object = GreenBillUser.objects.get(id=request.user.id)
    if request.method  =="POST":
        sign = request.FILES.get('authorised_sign')
        auth = ''
        if sign != None:
            auth = authorised_sign.objects.create(
            merchant_id = user_object,
            sign = sign,
            )
        if auth:
            sweetify.success(request, title="Success", icon='success', text='Authorised Signature Added Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Failed to Add Authorised Signature !!!', timer=1500)

    
    signs = authorised_sign.objects.all().order_by('-id')

    
    context = {
        'DesignNavclass':'active',
        'DesignCollapseShow':'show',
        'AuthSignNavClass':'active',
        'signs':signs,
    } 

    return render(request, "merchant/auth_sign.html",context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def sign_select(request):
    if request.method == "POST":
        selection = request.POST.get('logo_check')
        print('selection')
        print(selection)

        authorised_sign.objects.update(selection=selection)
        print(authorised_sign)
        sign1 = authorised_sign.objects.get(id=selection)
        print(sign1.selection)
        print(sign1.sign)
        if selection:
            sweetify.success(request, title="Success", icon='success', text='Authorised Sign Set Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Failed to Set !!!', timer=1500)

    return redirect(auth_sign)
@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def Delete_auth_sign(request, id):
    instance = authorised_sign.objects.get(id=id)
    
    instance.delete()
    return JsonResponse({'success': True})