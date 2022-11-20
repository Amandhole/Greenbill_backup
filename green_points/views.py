from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import GreenPointsModel
from users.models import GreenBillUser
from parking_lot_apis.models import ParkingLotPass, SaveParkingLotBill
from merchant_software_apis.models import CustomerBill
from petrol_pump_apis.models import SavePetrolPumpBill
from coupon.models import *
from django.db.models import Q
from super_admin_settings.models import *
# @login_required(login_url="/customer-login/")
# def get_green_points(request):

# 	# import PyPDF2 as pypdf
# 	# import os
# 	# print(os.path.dirname(__file__))
# 	# pdfobject=open("/myprojects/green_bill/media/customer_bill/InvoiceSimple-PDF-Template_1.pdf",'rb')
# 	# pdf=pypdf.PdfFileReader(pdfobject)
# 	# print(pdf.getFormTextFields())

# 	try:
# 		GreenPoints = GreenPointsModel.objects.filter(mobile_no=request.user.mobile_no).values('green_points_count')[0]['green_points_count']

# 	except:
# 		GreenPoints = 0

# 	context = {
#         "GreenPoints" : GreenPoints
# 	}
# 	return render(request, "customer/green-points.html", context)


@login_required(login_url="/customer-login/")
def get_green_points(request):

    try:
        GreenPoints = GreenPointsModel.objects.filter(mobile_no=request.user.mobile_no).values('green_points_count')[0]['green_points_count']
    except:
        GreenPoints = 0

    total_earned_green_points =  GetEarnedGreenPoints(request.user.mobile_no)
    total_green_points_used = GetUsedGreenPoints(request.user.id)
    earned_points = GreenPointsEarnedHistoryfun(request.user.mobile_no)
    redeem_history =  RedeemCouponHistory(request.user.id)

    # print(earned_points)

    # print(GreenPoints)
    total_available_points = int(total_earned_green_points - total_green_points_used)
    print("JJ",total_available_points)
    if total_green_points_used != 0:
        total_green_points_used_percentage = int((total_green_points_used / total_earned_green_points) * 100)
    else:
        total_green_points_used_percentage = 0

    if int(GreenPoints) != 0:
        total_green_points_available_percentage = int((int(GreenPoints) / total_earned_green_points) * 100)
    else:
        total_green_points_available_percentage = 0

    context = {
        "total_green_points_available" : total_available_points,
        "total_earned_green_points": total_earned_green_points,
        "total_green_points_used": total_green_points_used,
        "total_green_points_used_percentage": total_green_points_used_percentage,
        "total_green_points_available_percentage": total_green_points_available_percentage,
        "earned_points": earned_points,
        "redeem_history": redeem_history,
	}

    return render(request, "customer/green-points.html", context)


def GetEarnedGreenPoints(mobile_no):

    data = []

    customer_object = GreenBillUser.objects.get(mobile_no=mobile_no)
    
    customer_bill_list = CustomerBill.objects.filter(mobile_no=customer_object.mobile_no, green_points_earned__isnull=False).order_by('-id')

    for bill in customer_bill_list:

        try:
            business_name = bill.business_name.m_business_name
        except:
            business_name = ""

        try:
            bill_category_temp = bill.customer_bill_category.bill_category_name
        except:
            bill_category_temp = ""

        base_url = "http://157.230.228.250/"

        try:
            business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
        except:
            business_logo = ""

        data.append({
                    "id": bill.id,
                    "business_name": business_name,
                    "bill_category_name": bill_category_temp,
                    "bill_amount": bill.bill_amount,
                    "comments": bill.remarks,
                    "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y') if bill.bill_date else '',
                    "business_logo": business_logo,
                    "customer_added": bill.customer_added,
                    'db_table': "CustomerBill",
                    'green_points_earned': bill.green_points_earned,
                })

    parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = mobile_no, green_points_earned__isnull=False, is_pass = False).order_by('-id')

    for bill in parking_bill_list:

        try:
            business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
        except:
            business_name = ""

        try:
            bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
        except:
            bill_category_temp = ""

        base_url = "http://157.230.228.250/"

        try:
            business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
            business_logo = str(base_url) + str(business_logo_temp.url)

        except:
            business_logo = ""


        data.append({
                    "id": bill.id,
                    "business_name": business_name,
                    "bill_category_name": bill_category_temp,
                    "bill_amount": bill.amount,
                    "comments": bill.remarks,
                    "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                    "business_logo": business_logo,
                    "customer_added": False,
                    'db_table': "SaveParkingLotBill",
                    'green_points_earned': bill.green_points_earned,
                })


    petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = mobile_no, green_points_earned__isnull=False).order_by('-id')

    for bill in petrol_bill_list:

        try:
            business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
        except:
            business_name = ""

        try:
            bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
        except:
            bill_category_temp = ""

        base_url = "http://157.230.228.250/"

        try:
            business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
            business_logo = str(base_url) + str(business_logo_temp.url)

        except:
            business_logo = ""


        data.append({
                    "id": bill.id,
                    "business_name": business_name,
                    "bill_category_name": bill_category_temp,
                    "bill_amount": bill.total_amount,
                    "comments": bill.remarks,
                    "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                    "business_logo": business_logo,
                    "customer_added": False,
                    'db_table': "SavePetrolPumpBill",
                    'green_points_earned': bill.green_points_earned,
                })

    total_earned_ponits = 0

    referral_history = GreenPointsEarnedHistory.objects.filter(mobile_no = mobile_no)

    for referral in referral_history:
        data.append({
            "id": referral.id,
            "green_points_earned":referral.earned_green_points 
        })


    for bill in data:
        if bill['green_points_earned']:
            total_earned_ponits = total_earned_ponits + int(bill['green_points_earned'])

    return total_earned_ponits


def GetUsedGreenPoints(user_id):

    coupon_history = RedeemCouponModel.objects.filter(user_id=user_id).order_by('-id')

    total_green_points_used = 0

    for coupon in coupon_history:
        if coupon.green_point:
            total_green_points_used = total_green_points_used + int(coupon.green_point)

    return total_green_points_used


def GreenPointsEarnedHistoryfun(mobile_no):

    data = []

    customer_object = GreenBillUser.objects.get(mobile_no=mobile_no)
    
    customer_bill_list = CustomerBill.objects.filter(mobile_no=customer_object.mobile_no, green_points_earned__isnull=False).order_by('-id')

    for bill in customer_bill_list:

        try:
            business_name = bill.business_name.m_business_name
        except:
            business_name = ""

        try:
            bill_category_temp = bill.customer_bill_category.bill_category_name
        except:
            bill_category_temp = ""

        base_url = "http://157.230.228.250/"

        try:
            business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
        except:
            business_logo = ""


        data.append({
                    "id": bill.id,
                    "business_name": business_name,
                    "bill_category_name": bill_category_temp,
                    "bill_amount": bill.bill_amount,
                    "comments": bill.remarks,
                    "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                    "business_logo": business_logo,
                    "customer_added": bill.customer_added,
                    'db_table': "CustomerBill",
                    'green_points_earned': bill.green_points_earned,
                    "invoice_no": ""
                })

    parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = mobile_no, green_points_earned__isnull=False, is_pass = False).order_by('-id')

    for bill in parking_bill_list:

        try:
            business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
        except:
            business_name = ""

        try:
            bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
        except:
            bill_category_temp = ""

        base_url = "http://157.230.228.250/"

        try:
            business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
            business_logo = str(base_url) + str(business_logo_temp.url)

        except:
            business_logo = ""


        data.append({
                    "id": bill.id,
                    "business_name": business_name,
                    "bill_category_name": bill_category_temp,
                    "bill_amount": bill.amount,
                    "comments": bill.remarks,
                    "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                    "business_logo": business_logo,
                    "customer_added": False,
                    'db_table': "SaveParkingLotBill",
                    'green_points_earned': bill.green_points_earned,
                    "invoice_no": bill.invoice_no,
                })


    petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = mobile_no, green_points_earned__isnull=False).order_by('-id')

    for bill in petrol_bill_list:

        try:
            business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
        except:
            business_name = ""

        try:
            bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
        except:
            bill_category_temp = ""

        base_url = "http://157.230.228.250/"

        try:
            business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
            business_logo = str(base_url) + str(business_logo_temp.url)

        except:
            business_logo = ""


        data.append({
                    "id": bill.id,
                    "business_name": business_name,
                    "bill_category_name": bill_category_temp,
                    "bill_amount": bill.total_amount,
                    "comments": bill.remarks,
                    "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                    "business_logo": business_logo,
                    "customer_added": False,
                    'db_table': "SavePetrolPumpBill",
                    'green_points_earned': bill.green_points_earned,
                    "invoice_no": bill.invoice_no,
                })

    referral_history = GreenPointsEarnedHistory.objects.filter(mobile_no = mobile_no).order_by('-id')

    for referral in referral_history:
        data.append({
            "id": referral.id,
            "green_points_earned":referral.earned_green_points ,
            "db_table":'GreenPointsEarnedHistory',
            "bill_date": datetime.strptime(str((referral.created_at).date()), '%Y-%m-%d').strftime('%d-%m-%Y')
        })

    # print(data)

    data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)

    return data

def RedeemCouponHistory(user_id):

	coupon_history = RedeemCouponModel.objects.filter(user_id=user_id).order_by('-id')

	coupon_history_new = []

	for coupon in coupon_history:

		try:
			merchant_object = MerchantProfile.objects.get(id = coupon.merchant_business_id)
			coupon.merchant_business_name = merchant_object.m_business_name
		except:
			coupon.merchant_business_name = ""

		coupon_history_new.append({
                'id': coupon.id,
                'merchant_id': coupon.merchant_id.id,
                'merchant_business_id': coupon.merchant_business_id,
                'user_id': coupon.user_id,
                'coupon_id': coupon.coupon_id,
                'coupon_name': coupon.coupon_name,
                'coupon_code': coupon.coupon_code,
                'green_point': coupon.green_point,
                'coupon_redeem_date': datetime.strptime(str((coupon.coupon_redeem_date).date()), '%Y-%m-%d').strftime('%d-%m-%Y'),
                'merchant_business_name': coupon.merchant_business_name
            })

	return coupon_history_new