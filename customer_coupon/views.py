from django.shortcuts import render,redirect
from coupon.models import CouponModel,RedeemCouponModel
from green_points.models import GreenPointsModel
import sweetify
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_customer
from datetime import datetime, date
from users.models import Merchant_users, GreenBillUser, MerchantProfile
# Create your views here.
from owner_coupon.models import OwnerCouponModel, RedeemOwnerCouponModel
from app.models import generalSetting

def view_coupon_record(request, id):
    customer_data_object = GreenBillUser.objects.get(mobile_no=request.user)
    customer_state = customer_data_object.c_state
    customer_city = customer_data_object.c_city
    customer_area = customer_data_object.c_area
    print(customer_state)
    print(customer_city)
    print(customer_area)
    if request.method == "POST":
        # try:
        user_id = request.user.id
        coupon_id = request.POST['coupon_id']
        green_points = int(request.POST['green_points'])
        coupon_code = request.POST['promo_code']
        coupon_name = request.POST['coupon_name']
        merchant_id = request.POST['merchant_id']
        merchant_object = GreenBillUser.objects.get(id = merchant_id)
        coupon_user_count = CouponModel.objects.get(id=coupon_id)
        green_points_obj = GreenPointsModel.objects.get(mobile_no=request.user)
        total_points = int(green_points_obj.green_points_count)
        merchant_business_id = request.POST['merchant_business_id']
        
        if total_points >= green_points:
            new_green_points = total_points-green_points
            GreenPointsModel.objects.filter(mobile_no=request.user).update(
                green_points_count=new_green_points)
            CouponModel.objects.filter(id=coupon_id).update(coupon_redeem="1")
            RedeemCouponModel.objects.create(merchant_id=merchant_object, merchant_business_id = merchant_business_id, user_id = user_id, coupon_id = coupon_id, coupon_name=coupon_name,coupon_code=coupon_code,green_point=green_points)
            sweetify.success(request, title="Success", icon='success',
                             text='Coupon Redeemed Successfully', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error',
                           text="You don't have sufficient Green points to purchase", timer=2000)

    data = []

    base_url = "http://157.230.228.250/"
    all_coupons = CouponModel.objects.filter(id = id)
    all_coupons_new = []
    from datetime import date
    today = date.today()
    for coupon in all_coupons:
        redeem_status = RedeemCouponModel.objects.filter(user_id = request.user.id, coupon_id = coupon.id)
        merchant_object = MerchantProfile.objects.get(id = coupon.merchant_business_id)
        coupon.merchant_business_name = merchant_object.m_business_name
        coupon.merchant_business_id = merchant_object.id
        if redeem_status:
            coupon.redeem_status = True

        # if datetime.strptime(str(coupon.valid_through), "%Y-%m-%d").date() >= datetime.strptime(str(today_date), "%Y-%m-%d").date():
        if cust_offer_data.valid_through >= today:
            if coupon.customer_city:
                if customer_area in coupon.customer_city:
                    all_coupons_new.append(coupon)
    
    context = {
        "all_coupons" : all_coupons_new,
        'CustomerCouponNavclass': 'active',
        'CouponCollapseShow':'show',
        'CouponNavclass':'active',
    }
    return render(request, "customer/customer_coupon/view-coupon-record.html", context)
    

@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def views_customer_coupon(request):
    logo = generalSetting.objects.get(id=1) 
    c_logo = logo.o_business_logo
    print('c_logo',c_logo)
    customer_data_object = GreenBillUser.objects.get(mobile_no=request.user)
    customer_state = customer_data_object.c_state
    customer_city = customer_data_object.c_city
    customer_area = customer_data_object.c_area
    if request.method == "POST":
        # try:
        user_id = request.user.id
        
        expiry = request.POST['expiry']
        print(expiry)
        coupon_id = request.POST['coupon_id']
        green_points = int(request.POST['green_points'])
        coupon_code = request.POST['promo_code']
        coupon_name = request.POST['coupon_name']
        merchant_id = request.POST['merchant_id']
        merchant_object = GreenBillUser.objects.get(id = merchant_id)
        coupon_user_count = CouponModel.objects.get(id=coupon_id)
        total_user_validity = coupon_user_count.coupon_valid_for_user
        green_points_obj = GreenPointsModel.objects.get(mobile_no=request.user)
        total_points = int(green_points_obj.green_points_count)
        merchant_business_id = request.POST['merchant_business_id']
        redeem_coupon = RedeemCouponModel.objects.filter(coupon_id=coupon_id).count()
        print('redeem_coupon',redeem_coupon)
        print('total_user_validity', total_user_validity)
        if total_points >= green_points:
            new_green_points = total_points-green_points
            GreenPointsModel.objects.filter(mobile_no=request.user).update(
                green_points_count=new_green_points)
            CouponModel.objects.filter(id=coupon_id).update(coupon_redeem="1")
            RedeemCouponModel.objects.create(merchant_id=merchant_object, merchant_business_id = merchant_business_id, user_id = user_id, coupon_id = coupon_id, coupon_name=coupon_name,coupon_code=coupon_code,green_point=green_points)
            sweetify.success(request, title="Success", icon='success',
                            text='Coupon Redeemed Successfully', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error',
                        text="You don't have sufficient Green points to purchase", timer=2000)

    all_coupons = CouponModel.objects.all().order_by('-id')

    all_coupons_new = []

    # from datetime import fieldName = models.DateField(auto_now=False, auto_now_add=False)
    
    today = date.today()

    for coupon in all_coupons:
        try:
            redeem_status = RedeemCouponModel.objects.filter(user_id = request.user.id, coupon_id = coupon.id)
            merchant_object = MerchantProfile.objects.get(id = coupon.merchant_business_id)
            coupon.merchant_business_name = merchant_object.m_business_name
            coupon.merchant_business_id = merchant_object.id
        except:
            ""
        # print('print',coupon.coupon_valid_for_user)
        redeem_coupon = RedeemCouponModel.objects.filter(coupon_id=coupon.id).count()
        print('redeem_coupon',redeem_coupon)

        if redeem_status:
            coupon.redeem_status = True
        if coupon.valid_through >= today:
            if redeem_coupon < int(coupon.coupon_valid_for_user):
                if coupon.customer_state:
                    if customer_state in coupon.customer_state:
                        if coupon.customer_city:
                            if customer_city in coupon.customer_city:
                                if coupon.customer_area:
                                    if customer_area in coupon.customer_area:
                                        all_coupons_new.append(coupon)
                                else:
                                    all_coupons_new.append(coupon)
                        else:
                            all_coupons_new.append(coupon)

    coupon_history = RedeemCouponModel.objects.filter(user_id=request.user.id).order_by('-id')
   

    for coupon in coupon_history:
        try:
            merchant_object = MerchantProfile.objects.get(id = coupon.merchant_business_id)
            coupon.merchant_business_name = merchant_object.m_business_name
            print('abc',coupon.merchant_business_name)

            
        except:
            coupon.merchant_business_name = 'Green Bill'
            
        try:
            coupon_object = CouponModel.objects.get(id=coupon.coupon_id)
            coupon.valid_through = coupon_object.valid_through
        except:
            ""

    context = {
        'c_logo': c_logo,
        "coupon_history": coupon_history,
        "all_coupons": all_coupons_new,
        'CustomerCouponNavclass': 'active',
        'CouponCollapseShow':'show',
        'CouponNavclass':'active',
    }
    return render(request, "customer/customer_coupon/view_customer_coupon.html", context)


def Coupon_History(request):
    coupon_history = RedeemCouponModel.objects.filter(merchant_id=request.user)
    context = {
        "coupon_history": coupon_history,
        'CustomerCouponHistoryNavclass': 'active',
        'CouponCollapseShow':'show',
        'CouponNavclass':'active',
    }

    return render(request, "customer/customer_coupon/customer_coupon_history.html", context)






@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def views_customer_owner_coupon(request):
    customer_data_object = GreenBillUser.objects.get(mobile_no=request.user)
    customer_state = customer_data_object.c_state
    customer_city = customer_data_object.c_city
    customer_area = customer_data_object.c_area
    if request.method == "POST":
        # try:
        user_id = request.user.id
        coupon_id = request.POST['coupon_id']
        green_points = int(request.POST['green_points'])
        coupon_code = request.POST['promo_code']
        coupon_name = request.POST['coupon_name']
        owner_id = request.POST['owner_id']
        merchant_object = GreenBillUser.objects.get(id = owner_id)
        coupon_user_count = CouponModel.objects.get(id=coupon_id)
        green_points_obj = GreenPointsModel.objects.get(mobile_no=request.user)
        total_points = int(green_points_obj.green_points_count)
        merchant_business_id = request.POST['merchant_business_id']

        if total_points >= green_points:
            new_green_points = total_points-green_points
            GreenPointsModel.objects.filter(mobile_no=request.user).update(
                green_points_count=new_green_points)
            OwnerCouponModel.objects.filter(id=coupon_id).update(coupon_redeem="1")
            RedeemOwnerCouponModel.objects.create(merchant_id=merchant_object, merchant_business_id = merchant_business_id, user_id = user_id, coupon_id = coupon_id, coupon_name=coupon_name,coupon_code=coupon_code,green_point=green_points)
            sweetify.success(request, title="Success", icon='success',
                             text='Coupon Redeemed Successfully', timer=1500)
        else:
            sweetify.error(request, title="Error", icon='error',
                           text="You don't have sufficient Green points to purchase", timer=2000)
        # except:
        #     pass
    all_coupons_new = []
    from datetime import date

    # today = date.today()
    # today_date = today.strftime("%Y-%m-%d")
    today = date.today()
    all_coupons = OwnerCouponModel.objects.all().order_by('-id')

    for coupon in all_coupons:
        redeem_status = RedeemOwnerCouponModel.objects.filter(user_id = request.user.id, coupon_id = coupon.id)
        if coupon.valid_through >= today:
            if coupon.customer_state:
                if customer_state in coupon.customer_state:
                    if coupon.customer_city:
                        if customer_city in coupon.customer_city:
                            if coupon.customer_area:
                                if customer_area in coupon.customer_area:
                                    all_coupons_new.append(coupon)
                            else:
                                all_coupons_new.append(coupon)
                    else:
                        all_coupons_new.append(coupon)
       
       
      
        if redeem_status:
            coupon.redeem_status = True

    # for coupon in all_coupons:
    #     if coupon.valid_through:
    #         coupon.valid_through = datetime.strptime(coupon.valid_through, '%Y-%m-%d').strftime('%d-%m-%Y')

    coupon_history = RedeemOwnerCouponModel.objects.filter(user_id=request.user.id)

    # for coupon in coupon_history:
    #     merchant_object = MerchantProfile.objects.get(id = coupon.merchant_business_id)
    #     coupon.merchant_business_name = merchant_object.m_business_name
    
    context = {
        "coupon_history": coupon_history,
        "all_coupons": all_coupons_new,
        'OwnerCustomerCouponNavclass': 'active',
        
    }
    return render(request, "customer/customer_coupon/view_customer_owner_coupon.html", context)




def Owner_Coupon_History(request):
    coupon_history = RedeemOwnerCouponModel.objects.filter(owner_id=request.user)
    context = {
        "coupon_history": coupon_history,
        
        'OwnerCouponNavclass':'active',
    }
    return render(request, "customer/customer_coupon/customer_coupon_history.html", context)


def Number_of_views(request):
    if request.method == "POST":
        id = request.POST.get("coupon_id_clicks")
        object = CouponModel.objects.get(id=id)
        object.cout = object.cout + 1
        object.save()
    return redirect('customer-coupons-redeem')