 
from audioop import reverse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff 
from .models import *
import sweetify
from users.models import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from pdf2image import convert_from_path
# SMS
import requests
import time
import pyshorteners

@csrf_exempt
def padfchecker(request):
    if request.method == "POST":
        bill = request.FILES['bill']
        customer_mobile_number = request.POST['cust_no']
        bill_amount = request.POST['bill_amt']
        invoice_no  = request.POST['invoice_no']
        bussiness_name = request.POST['business_name']
        date = request.POST['date']
        merchant_id = request.POST['merchant_no']
        print(bill)


        list_data = []

        list_data.append(customer_mobile_number)
        list_data.append(bill_amount)
        list_data.append(invoice_no)
        list_data.append(bussiness_name)
        list_data.append(date)
        list_data.append(merchant_id)

        d = temp_pdf_check.objects.all()
        print(list(d))
        obj = temp_pdf_check.objects.update(pdf_image = bill)
        if len(list(d)) ==0:
            obj = temp_pdf_check.objects.create(pdf_image = bill)
        else:
            list(d)[0].pdf_image = bill
            list(d)[0].save()

        f = temp_pdf_check.objects.all()

        print(f)
       
        g = list(f)
        print(g)
        bill_url = g[0].pdf_image
        print(bill_url)
        d = "http://157.230.228.250/media/temp1/" + str(bill_url) + "/"
        s = pyshorteners.Shortener()
        print(s)
        short_url = s.tinyurl.short(d)
        ts = int(time.time())

        data_temp = {
                "keyword":"Bill Delivery SMS",
                "timeStamp":ts,
                "dataSet":
                    [
                        {
                            "UNIQUE_ID":"GB-" + str(ts),
                            "MESSAGE":"Hey Green Bill user to view or download your bill click on link " + short_url + " to view all your bills download Green Bill App",
                            "OA":"GBBILL",
                            "MSISDN": str(customer_mobile_number), # Recipient's Mobile Number
                            "CHANNEL":"SMS",
                            "CAMPAIGN_NAME":"hind_user",
                            "CIRCLE_NAME":"DLT_SERVICE_IMPLICT",
                            "USER_NAME":"hind_hsi",
                            "DLT_TM_ID":"1001096933494158", # TM ID
                            "DLT_CT_ID":"1007161814187973948", # Template Id
                            "DLT_PE_ID":"1001659120000037015" # PE ID 
                        }
                    ]
                }
        url = "http://digimate.airtel.in:15181/BULK_API/InstantJsonPush"

        response = requests.post(url, json = data_temp)
        print(response)
        if response.status_code == 200:
            # total_amount_avilable_new = 0
            # total_amount_avilable_new = float(subscription_object.total_amount_avilable) - float(subscription_object.per_bill_cost)
            # subscription_object.total_amount_avilable = total_amount_avilable_new
            # subscription_object.save()
            print("msg sent ")
            return JsonResponse({'status':'success', 'message': 'SMS sent successfully','data':list_data}, status=200)
        else:
            print("Message not sent")
            return JsonResponse({'status' : 'error', 'message': "Failed to send SMS"}, status=400)
                                
        
        # try:
        #     s = list(d)
        #     print(s)
        #     print(s[0].pdf_image)
        #     sr = "http://157.230.228.250/media/"
        #     sr = sr+str(s[0].pdf_image)
        #     print(sr)
        #     images = convert_from_path(str(s[0].pdf_image))
        #     print(images)
        #     for img in images:
        #         img.save('output.jpg', 'JPEG')
        # except  :
        #     Result = "No pdf found"

        # else:
        #     Result = "success"
        print(Result)
        s[0].delete()
        return JsonResponse({"msg":Result})
    return JsonResponse({"msg":"No"})
           

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def bill_design_view(request):
    print("in funcr")
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

        print("************************************")

        print(social_media_check)
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

        if "tripadvisor" in social_media_check:
            tripadvisor_status = True
            tripadvisor_url = request.POST["tripadvisor_url"]
        else:
            tripadvisor_status = False 
            tripadvisor_url = ""

        if "indiamart" in social_media_check:
            indiamart_status = True
            indiamart_url = request.POST["indiamart_url"]
        else:
            indiamart_status = False
            indiamart_url = ""

        if "justdial" in social_media_check:
            justdial_status = True
            justdial_url = request.POST["justdial_url"]
        else:
            justdial_status = False
            justdial_url = ""
            
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
        # "indiamart":indiamart_status,"indiamart_url":indiamart_url,"justdial":justdial_status,"justdial_url":justdial_url
        merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
        result = ''
        if len(social_media_check) == 0 or len(social_media_check) <= 4:
            result = bill_designs.objects.update_or_create(merchant_business_id = merchant_business_id, defaults={ "logo" : logo_check, 
                "address" : address_check, "rating" : rating_status, "rating_text" : rating_text, "rating_emoji" : rating_emoji,
                 "facebook" : facebook_status, "facebook_url" : facebook_url, "youtube" : youtube_status, "youtube_url" : youtube_url,
                  "twitter" : twitter_status, "twitter_url" : twitter_url, "instagram" : instagram_status, "instagram_url" : instagram_url,
                   "ads_below_bill" : ads_status, "phone" : phone_status, "phone_number" : phone_number, "website" : website_status, 
                   "website_url" : website_url, "map" : map_status, "map_link" : map_link, "terms_conditions" : terms_status, "terms_url" : terms_url,
                    "footer_logo" : footer_logo_status,"linkedin":linkedin_status,"linkedin_url":linkedin_url,"skype":skype_status,"skype_url":skype_url,
                    "google":google_status,"google_url":google_url,"pinterest":pinterest_status,"pinterest_url":pinterest_url,"snapchat":snapchat_status,
                    "snapchat_url":snapchat_url,"android":android_status,"android_url":android_url, "apple":apple_status, "apple_url": apple_url,
                    "zomato":zomato_status, "zomato_url": zomato_url,"swiggy":swiggy_status, "swiggy_url": swiggy_url,'pay_link':pay_link,"tripadvisor":tripadvisor_status,"tripadvisor_url":tripadvisor_url,
                    })
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



def card_design_preview(request,id):
    # print(id)
    try:
        user_object = GreenBillUser.objects.get(mobile_no = id)
        print(user_object)
        merchant_user = Merchant_users.objects.get(user_id = user_object)
        print(merchant_user)

        merchant_object = merchant_user.merchant_user_id
        print(merchant_object)
        merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
        print(merchant_business_id)

        contact_object  = contact_card.objects.get(merchant_business_id = merchant_business_id)
        print(contact_object)


        view_url = contact_card.objects.get(merchant_business_id=merchant_business_id)
        view_count = view_url.view
        view_count =view_count + 1
        
        view_url.view = view_count
        print("&*@**#*#")
        print(view_count)
        view_url.save()

        context = {
            "data":contact_object
        }
        print(context)
        return render(request, "merchant/bill_design/card-design-2.html", context)
    except:
        # print("in expect")
        return HttpResponse("I am error")



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def card_design_view(request):
    print("***********")
    if request.method == "POST" :
        email = request.POST["email"]
        first_name =  request.POST["first_name"]
        city = request.POST["city"]
        country =  request.POST["country"]
        description = request.POST["description"]

        about = request.POST["about_us"]
        alternate_mobile = request.POST["alternate_mobile"]
        bussiness_time = request.POST["buss_time"]
        
        file_pic = request.FILES.get("profile_pic")
        background = request.FILES.get("background_pic",False)
        cover = request.FILES.get("cover_pic",False)
        gallery1 = request.FILES.get("Gallery1",False)
        gallery2 = request.FILES.get("Gallery2",False)
        gallery3 = request.FILES.get("Gallery3",False)
        temp_choice = request.POST.get("template_check",False)
        #  bank detail
        account_holder_name = request.POST['account_holder_name']
        account_no = request.POST['account_no']
        ifsc_Code = request.POST['ifsc_Code']
        bank_name = request.POST['bank_name']
        pan_card = request.POST['pan_card']
        gstin_number = request.POST['gstin_number']




        client1 = request.FILES.get("client1",False)
        client2 = request.FILES.get("client2",False)
        client3 = request.FILES.get("client3",False)
        client4 = request.FILES.get("client4",False)
        client5 = request.FILES.get("client5",False)
        client6 = request.FILES.get("client6",False)
        



        print(gallery3,gallery2,gallery3)
        video_url = request.POST["youtube_video_url"]

        print(temp_choice)
        if temp_choice:
            sweetify.success(request, title="Success", icon='success', text='Template Set Successfully !!!', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error', text='Failed to Set Template !!!', timer=1500)

        print(file_pic,video_url,background)
        print(gallery3,gallery2,gallery1,about,description)


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

        if "email" in social_media_check:
            email_status = True
            email_url = request.POST["email_url"]
        else:
            email_status = False
            email_url = ""

        print(facebook_url,youtube_url)


        contact_check =  request.POST.getlist("contact_check")

        print("************************************")

        print(contact_check)

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

        if "whatsapp" in contact_check:
            whatsapp_status = True
            whatsapp_number = request.POST["whatsapp_url"]
        else:
            whatsapp_status = False
            whatsapp_number = ""

        if "addtobook" in contact_check:
            addtobook_status = True
            addtobook_url = request.POST["address_book_number"]
        else:
            addtobook_status = False
            addtobook_url = ""
        
        if "msg" in contact_check:
            msg_status = True
            msg_link = request.POST["msg_url"]
        else:
            msg_status = False
            msg_link = ""


        print(msg_status,addtobook_status,map_status,whatsapp_status,website_status)
       
        merchant_user_object = Merchant_users.objects.get(user_id = request.user)

        merchant_object = merchant_user_object.merchant_user_id

        mobile_no =  request.user.mobile_no
        

        merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

        try:
            avai = contact_card.objects.get(merchant_business_id=merchant_business_id)
        except:
            avai = ""

        
        if avai and file_pic:
            print("in g")
            avai.card_photo = file_pic
            avai.save()
        else:
            pass

        result = ''

        if len(social_media_check) == 0 or len(social_media_check) <= 4:
            result = contact_card.objects.update_or_create(merchant_business_id = merchant_business_id, defaults={ 
                "card_desc":description,"card_city":city,"card_country":country,"card_email":email,"card_phone_no":mobile_no,"card_name":first_name,
                 "facebook" : facebook_status, "facebook_url" : facebook_url, "youtube" : youtube_status, "youtube_url" : youtube_url,
                  "phone" : phone_status, "phone_number" : phone_number, "website" : website_status, 
                   "website_url" : website_url, "map" : map_status, "map_link" : map_link,"cover_photo":cover,"gallery1":gallery1,"gallery2":gallery2,"gallery3":gallery3,  'client1':client1,'client2':client2,'client3':client3,'client4':client4,'client5':client5,'client6':client6,"msg":msg_status,
                   "msg_number":msg_link,"whatsapp":whatsapp_status,"whatsapp_number":whatsapp_number,"address_book":addtobook_status,"address_book_number":addtobook_url,"email":email_status,"email_url":email_url,
                   "alternate_mobile":alternate_mobile,
                   "bussiness_time":bussiness_time,"about_us":about,"temp_choice":temp_choice,"card_desc":description,"background_photo":background,"cover_photo":cover, 'acco_holder_name':account_holder_name, 'acc_no':account_no, 'ifsc_Code':ifsc_Code, 'bank_name':bank_name, 'pan_card':pan_card , 'gstin_no':gstin_number })
        else:
            result = contact_card.objects.update_or_create(merchant_business_id = merchant_business_id, defaults={  "phone" : phone_status, "phone_number" : phone_number, "website" : website_status, 
               "website_url" : website_url, "map" : map_status, "map_link" : map_link, })

        

        # print(result)

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
        card_design_data = contact_card.objects.get(merchant_business_id = merchant_business_id)
    except:
        card_design_data = ""



    context = {
        "card_design_data" : card_design_data,
        "business_logo":business_logo,
        "business_address":business_address,
        "merchant_business_id":merchant_business_id,
        "DesignNavclass": "active",
        "DesignCollapseShow": "show",
        "CashMemoNavClass": "active"
    }


    return render(request, "merchant/bill_design/card-design.html", context)




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



  
@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def feedback(request):
    if request.method == 'POST':
        coment = request.POST['feedback']
        rating_check = request.POST.getlist("rating_check")
        merchant_user_object = Merchant_users.objects.get(user_id = request.user)

        merchant_object = merchant_user_object.merchant_user_id

        mobile_no =  request.user.mobile_no
        

        merchant_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
        print(merchant_id)

        print("*****************dgeyyeheeueuueue*******************")

        print(rating_check)

        print(len(rating_check))
        data=Card_feedback(merchant_business_id = merchant_id,comment=coment,rating=(len(rating_check)))
        data.save()
        obj  = Card_feedback.objects.filter(merchant_business_id=merchant_id)


        print(obj)
        total_rating_given = len(obj)
        print(total_rating_given)
        sum_rating  = 0 
        for rating_obj in obj :
            sum_rating = sum_rating+ int(rating_obj.rating)
        total_rating_recived = ''
        try:

            total_rating_recived  = float(sum_rating/total_rating_given)
        except:
            total_rating_given = 0


        print("*************************************sghdhdh")
        print(total_rating_recived)
        print(coment)
        print('22222222222')
      
        print('data saved')
        return HttpResponse('succes')
    return render(request,'card-design-2.html')



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def analysis(request):
    merchant_user_object = Merchant_users.objects.get(user_id = request.user)
    merchant_object = merchant_user_object.merchant_user_id
    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)
    print('in try')
    data =  Card_feedback.objects.filter(merchant_business_id=merchant_business_id).reverse()
    var = contact_card.objects.filter(merchant_business_id=merchant_business_id)
    print(data)
    context ={"data":data,"var":var}

    return render(request,"merchant/bill_design/analysis.html",context)
 



        
    

