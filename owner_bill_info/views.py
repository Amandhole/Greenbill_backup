from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
import csv
import io
from django.contrib.auth.decorators import login_required, user_passes_test
import sweetify
from users.models import Merchant_users, MerchantProfile, GreenBillUser
from merchant_software_apis.models import CustomerBill, MerchantBill
from petrol_pump_apis.models import SavePetrolPumpBill
from parking_lot_apis.models import SaveParkingLotBill
from datetime import datetime
from django.utils import formats

from app.views import is_owner

from bill_design.models import *
from my_subscription.models import*

# SMS
import requests
import time
import pyshorteners

from django.db.models import Q


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def owner_sent_bills_view(request):

	# merchant_bill_list = MerchantBill.objects.all().order_by('-id')

	# all_merchants = MerchantProfile.objects.filter(m_disabled_account = False)

	# base_url = "http://157.230.228.250/"

	# data = []

	# for bill in merchant_bill_list:
	# 	try:
	# 		bill_file = str(base_url) + str(bill.bill.url)
	# 	except:
	# 		bill_file = ""
	# 	try:
	# 		user_object = GreenBillUser.objects.get(id = bill.user_id)
	# 		created_by_id = user_object.id
	# 		created_by = user_object.first_name + ' ' + user_object.last_name
	# 	except:
	# 		created_by = ""
	# 		created_by_id = ""


	# 	data.append({
	# 		'bill_id': bill.id,
 #            'invoice_no': bill.invoice_no,
 #            'mobile_no': bill.mobile_no,
 #            'amount': str(bill.bill_amount),
 #            'business': bill.business_name,
 #            'date': datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
 #            'bill_file': bill.bill,
 #            'db_table': "MerchantBill",
 #            'customer_added': False,
 #            'created_by': created_by,
 #            'created_by_id': created_by_id,
 #            'bill_flag': False,
 #            'bill_url': bill.bill_url,			
 #        })

    
	# data.sort(key = lambda x: datetime.strptime(x['date'], '%d-%m-%Y'), reverse = True)

	# for merchant in all_merchants:
	# 	startswith = str(merchant.id) + ','
	# 	endswith = ','+ str(merchant.id)
	# 	contains = ','+ str(merchant.id) + ','
	# 	exact = str(merchant.id)

	# 	recharge_his = recharge_history.objects.filter(
	#         Q(merchant_id = merchant.m_user),
	#         Q(business_ids__startswith = startswith) | 
	#         Q(business_ids__endswith = endswith) | 
	#         Q(business_ids__contains = contains) | 
	#         Q(business_ids__exact = exact)
	#     ).order_by('-id')

	    # for recharge in recharge_his:
	    # 	if recharge.is_subscription_plan == True:
	    # 		subscription_plan = subscription_plan_details.objects.filter(id=recharge.subscription_plan_id)
	    # 		for subscription in subscription_plan:
	    # 			try:
	    # 				users_cost = float(recharge.no_of_users) * float(recharge.valid_for_month) * float(subscription.cost_for_users)
	    # 				final_amount = float(users_cost) + float(recharge.cost) + float(recharge.gst_amount)
	    # 			except:
	    # 				final_amount = 0
	    # 	else:
	    # 		final_amount = recharge.cost


	    #     purchase_date = timezone.localtime(recharge.purchase_date).strftime("%Y-%m-%d")

	    #     data.append({
	    #         'bill_id': recharge.id,
	    #         'invoice_no': recharge.invoice_no,
	    #         'mobile_no': '',
	    #         'amount': str(final_amount),
	    #         'business': 'Green Bill',
	    #         'date': datetime.strptime(str(purchase_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
	    #         'bill_file': '',
	    #         'db_table': "recharge_history",
	    #         'customer_added': '',
	    #         'created_by': '',
	    #         'created_by_id': '',
	    #         'bill_flag': '',
	    #         'bill_url': '',
	    #     })
	
	context = {
		# "bills":data,
		'BillInfoNavClass':'active',
		'SentBillsNavClass': 'active',
		"BillInfoCollapseShow": "show",
	}

	return render(request, "super_admin/bill_info/sent-bills.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def owner_received_bills_view(request):

	context = {
		'BillInfoNavClass':'active',
		'ReceivedBillsNavClass': 'active',
		"BillInfoCollapseShow": "show",
	}

	return render(request, "super_admin/bill_info/received-bills.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def owner_rejected_bills_view(request):

	context = {
		'BillInfoNavClass':'active',
		'RejectedBillsNavClass': 'active',
		"BillInfoCollapseShow": "show",
	}

	return render(request, "super_admin/bill_info/rejected-bills.html", context)