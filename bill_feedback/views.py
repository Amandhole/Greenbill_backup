from django.shortcuts import render, redirect
from .models import *
import sweetify
from django.http import JsonResponse
from users.models import MerchantProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff, is_customer
from users.models import *
from merchant_software_apis.models import CustomerBill
from users.models import Merchant_users, GreenBillUser, MerchantProfile
from datetime import datetime
from bill_design.models import *
from django.db.models import Q

from merchant_software_apis.models import *
from pyfcm import FCMNotification
from django.conf import settings
import socket



@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def bill_feedback(request):

	merchant_user_object = Merchant_users.objects.get(user_id = request.user)
	merchant_object = merchant_user_object.merchant_user_id
	merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)




	try:
		for_rating_1_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_id.id, for_rating = "1")
	except:
		for_rating_1_object = ""

	try:
		for_rating_2_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_id.id, for_rating = "2")
	except:
		for_rating_2_object = ""

	try:
		for_rating_3_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_id.id, for_rating = "3")
	except:
		for_rating_3_object = ""

	try:
		for_rating_4_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_id.id, for_rating = "4")
	except:
		for_rating_4_object = ""

	try:
		for_rating_5_object = bill_feedback_question.objects.get(merchant_business_id = merchant_business_id.id, for_rating = "5")
	except:
		for_rating_5_object = ""

	context = {
		"for_rating_1_object": for_rating_1_object,
		"for_rating_2_object": for_rating_2_object,
		"for_rating_3_object": for_rating_3_object,
		"for_rating_4_object": for_rating_4_object,
		"for_rating_5_object": for_rating_5_object,
		"FeedbackNavclass":"active"
	}

	return render(request, "merchant/bill_feedback/create-bill-feedback.html", context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def update_bill_feedback_rating(request, id):

	rating = id

	merchant_user_object = Merchant_users.objects.get(user_id = request.user)
	merchant_object = merchant_user_object.merchant_user_id
	merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

	if request.method == "POST":
		question = request.POST["question"]
		option_1 = request.POST["option_1"]
		option_2 = request.POST["option_2"]
		option_3 = request.POST["option_3"]

		result = bill_feedback_question.objects.update_or_create(merchant_business_id = merchant_business_id.id, for_rating = rating,
			defaults={
				"for_rating" : rating,
				"question" : question,
				"option_1" : option_1,
				"option_2" : option_2,
				"option_3" : option_3,
			}
		)

		if result:
			sweetify.success(request, title="Success", icon='success', text='Question updated Successfully !!!', timer=1500)
		else:
			sweetify.error(request, title="Error", icon='error', text='Failed to update !!!', timer=1500)
	else:
		sweetify.error(request, title="Error", icon='error', text='Something went wrong !!!', timer=1500)

	return redirect(bill_feedback)



@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def customer_reply(request):
	cust_id = request.user
	customer_object1 = GreenBillUser.objects.get(mobile_no = cust_id)
	rating = ''
	if request.method == 'POST':
		rating = request.POST.get('rating_filter')
		if rating:
			data_reply = CustomerBill.objects.filter(mobile_no = customer_object1,customer_added=False, rating = rating).order_by('-id')
			rating = int(rating)
		else:
			data_reply = CustomerBill.objects.filter(Q(mobile_no = customer_object1) & Q(customer_added=False) & (Q(rating=1) | Q(rating=2) | Q(rating=3) | Q(rating=4) | Q(rating=5))).order_by('-id')
	else:
		data_reply = CustomerBill.objects.filter(Q(mobile_no = customer_object1) & Q(customer_added=False) & (Q(rating=1) | Q(rating=2) | Q(rating=3) | Q(rating=4) | Q(rating=5))).order_by('-id')
		# data_reply = CustomerBill.objects.filter(mobile_no = customer_object1,customer_added=False).order_by('-id')

	data1 = []
	feedback_emoji = '😊'
	# feedback_emoji = "❤️"

	feedback_count = 0
	data = []
	rating1 = 0
	rating2 = 0
	rating3 = 0
	rating4 = 0
	rating5 = 0
	for reply in data_reply:
		if reply.business_name:
			try:
				reply.feedback_emoji = bill_designs.objects.get(merchant_business_id = reply.business_name.id).rating_emoji
			except:
				reply.feedback_emoji = '😊'
		else:
			reply.feedback_emoji = '😊'
		if not reply.feedback_emoji:
			reply.feedback_emoji = '😊'

		# if reply.feedback_reply:
		if reply.rating == '1':
			rating1 = rating1 + 1
		if reply.rating == '2':
			rating2 = rating2 + 1
		if reply.rating == '3':
			rating3 = rating3 + 1
		if reply.rating == '4':
			rating4 = rating4 + 1
		if reply.rating == '5':
			rating5 = rating5 + 1
		feedback_count = feedback_count + 1

		data.append({
            'id': reply.id,
            'rating': reply.rating,
            'invoice_no': reply.invoice_no,
            'bill_date': reply.bill_date,
            'feedback_reply': reply.feedback_reply,
            'feedback_emoji': reply.feedback_emoji,
        })
	
	# data1.append(rating1)
	# data1.append(rating2)
	# data1.append(rating3)
	# data1.append(rating4)
	# data1.append(rating5)
	star1percentage = 0
	star2percentage = 0
	star3percentage = 0
	star4percentage = 0
	star5percentage = 0
	if feedback_count:

		if rating1:
			star1percentage = (rating1/feedback_count)*100
		if rating2:
			star2percentage = (rating2/feedback_count)*100
		if rating3:
			star3percentage = (rating3/feedback_count)*100
		if rating4:
			star4percentage = (rating4/feedback_count)*100
		if rating5:
			star5percentage = (rating5/feedback_count)*100
    	
	context = {
		'data_reply' : data,
		# 'data1': data1,
		'rating1': rating1,
		'rating2': rating2,
		'rating3': rating3,
		'rating4': rating4,
		'rating5': rating5,
		'rating': rating,
		'star1percentage': star1percentage,
		'star2percentage': star2percentage,
		'star3percentage': star3percentage,
		'star4percentage': star4percentage,
		'star5percentage': star5percentage,
		'feedback_count': feedback_count,
		"feedback_emoji": feedback_emoji,
		'RatingNavclass' : 'active',

	}
	return render(request, 'customer/customer_feedReply/merchant_reply.html', context)
	# context = {
	# 	'data_reply' : data,
	# 	'RatingNavclass':'active',
 #    }
 #    return render(request, 'customer/customer_feedReply/merchant_reply.html', context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def feedback_reply(request):
	merchant_user_object = Merchant_users.objects.get(user_id = request.user)
	merchant_object = merchant_user_object.merchant_user_id
	merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

	try:
		feedback_emoji = bill_designs.objects.get(merchant_business_id = merchant_business_id).rating_emoji
	except:
		feedback_emoji = ""

	if not feedback_emoji:
		feedback_emoji = '😊'

	rating = ''

	if request.method == 'POST':

		rating = request.POST.get('rating_filter')

		if rating:
			reply = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = rating).order_by('-id')
			feedback_count = 0
			rating = int(rating)
			for obj in reply:
				if obj.rating:
					feedback_count = feedback_count + 1
		else:
			reply = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id).order_by('-id')
			feedback_count = 0
			for obj in reply:
				if obj.rating:
					feedback_count = feedback_count + 1
	else:
		reply = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id).order_by('-id')
		feedback_count = 0
		for obj in reply:
			if obj.rating:
				feedback_count = feedback_count + 1
	ratings = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id).order_by('-id')
	star1 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 1).count()
	star2 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 2).count()
	star3 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 3).count()
	star4 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 4).count()
	star5 = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id, rating = 5).count()
	total_rating = CustomerBill.objects.filter(customer_added = False, business_name = merchant_business_id)

	total_feedback_count = 0

	for obj in total_rating:
		if obj.rating:
			total_feedback_count = total_feedback_count + 1

	if total_feedback_count == 0:
		average_rating = 0
	else:	
		average_rating = ((star5 * 5) + (star4 * 4) + (star3 * 3) + (star2 * 2) + (star1 * 1))/(total_feedback_count)

	rating_in_percentage = (average_rating/5) * 100
	rating1 = 0
	rating2 = 0
	rating3 = 0
	rating4 = 0
	rating5 = 0
	data1 = []
	for obj1 in ratings:
		if obj1.rating:
			if obj1.rating == '1':
				rating1 = rating1 + 1
			if obj1.rating == '2':
				rating2 = rating2 + 1
			if obj1.rating == '3':
				rating3 = rating3 + 1
			if obj1.rating == '4':
				rating4 = rating4 + 1
			if obj1.rating == '5':
				rating5 = rating5 + 1

	# data1.append(rating1)
	# data1.append(rating2)
	# data1.append(rating3)
	# data1.append(rating4)
	# data1.append(rating5)
	star1percentage = 0
	star2percentage = 0
	star3percentage = 0
	star4percentage = 0
	star5percentage = 0
	if feedback_count:
		if rating1:
			star1percentage = (rating1/feedback_count)*100
		if rating2:
			star2percentage = (rating2/feedback_count)*100
		if rating3:
			star3percentage = (rating3/feedback_count)*100
		if rating4:
			star4percentage = (rating4/feedback_count)*100
		if rating5:
			star5percentage = (rating5/feedback_count)*100

	print(rating)
	context = {
		'feedback_emoji': feedback_emoji,
	    'reply' : reply,
	    'rating1': rating1,
		'rating2': rating2,
		'rating3': rating3,
		'rating4': rating4,
		'rating5': rating5,
		'rating': rating,
		'star1percentage': star1percentage,
		'star2percentage': star2percentage,
		'star3percentage': star3percentage,
		'star4percentage': star4percentage,
		'star5percentage': star5percentage,
	    'feedback_count' : feedback_count,
	    'average_rating': average_rating,
	    'rating_in_percentage': rating_in_percentage,
	    'RatingNavClass':'active',
	    'BillInfoNavClass':'active',
	    'BillInfoCollapseShow':'show',
	}
	
	return render(request, 'merchant/merchant_feedreply/reply.html', context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def reply_by_id(request):
    if request.method == "POST":
        id = request.POST["bill_id"]
        feedback_reply = request.POST["feedback_reply"] 
        bill_object = CustomerBill.objects.get(id = id)
        data_status = CustomerBill.objects.filter(id = id).update(feedback_reply = feedback_reply)
        device = DeviceId.objects.filter(mobile_no = bill_object.mobile_no, user_type = 'customer').first()

        if bill_object.business_name:
	        if device:

	        	push_service = FCMNotification(api_key=settings.API_KEY)

	        	registration_id = device.device_id

	        	message_title = "Rating"

	        	message_body = "Your feedback got a reply from shop. " + str(bill_object.business_name.m_business_name)

	        	result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)


        return JsonResponse({'status':'success'}, status=200)
    else:
    	return JsonResponse({'status':'error'}, status=200)
        