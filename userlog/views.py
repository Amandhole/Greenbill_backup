from django.shortcuts import render
from user_visit.models import UserVisit
from users.models import GreenBillUser
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner
from users.models import GreenBillUser, UserProfileImage, Merchant_users, MerchantProfile
from merchant_role.models import merchant_role, merchant_userrole


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def owner_logs(request, mobile_no):
    UserVisit_details = UserVisit.objects.all().order_by('-id')

    new_data = []

    for data in UserVisit_details:
        if str(data.user) == mobile_no:
            new_data.append({
                'id': data.id,
                'timestamp': data.timestamp,
                'user': data.user,
                'remote_addr': data.remote_addr
                })

    context = {
        'userlogs': new_data,
        'myteamNavActiveClass': 'active',
        'myteamInfoCollapseShow': 'show',
        'userlogsActiveClass': 'active',
    }

    return render(request, 'owner_log.html', context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def userlogs(request):
    # print(request.user.first_name, '---------------',request.user.last_name)

    owner_users = GreenBillUser.objects.all().filter(is_staff = "1", is_active=True)
    merchant_users = GreenBillUser.objects.all().filter(is_merchant = "1", is_active=True)
    partner_users = GreenBillUser.objects.all().filter(is_partner = "1", is_active=True)
    customer_users = GreenBillUser.objects.all().filter(is_customer = "1", is_active=True)

    data = []
    merchant_data = []
    partner_data = []
    customer_data = []

    data.append({
        'role': 'owner_user',
        'first_name': request.user.first_name,
        'last_name' : request.user.last_name,
        'mo_number':request.user
    })

    for temp in owner_users:
        data.append({
            'role': 'owner_user',
            'first_name' : temp.first_name,
            "last_name" : temp.last_name,
            'mo_number': temp.mobile_no
        })

    for temp in merchant_users:
        merchant_data.append({
            'role': 'merchant_user',
            'first_name' : temp.first_name,
            "last_name" : temp.last_name,
            'mo_number': temp.mobile_no
        })

    for temp in partner_users:
        partner_data.append({
            'role': 'partner_user',
            'first_name' : temp.first_name,
            "last_name" : temp.last_name,
            'mo_number': temp.mobile_no
        })

    for temp in customer_users:
        customer_data.append({
            'role': 'customer_user',
            'first_name' : temp.first_name,
            "last_name" : temp.last_name,
            'mo_number': temp.mobile_no
        })

    

    # data = UserVisit.objects.all().order_by('-id')
    context = {
    	'userlogs': data,
        'merchant_data': merchant_data,
        'partner_data': partner_data,
        'customer_data': customer_data,
    	'myteamNavActiveClass': 'active',
    	'myteamInfoCollapseShow': 'show',
    	'userlogsActiveClass': 'active',
    }
    template = 'user-log.html'
    return render(request, template, context) 

def merchant_list_for_userlogs(request):
    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_users_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    qs = merchant_role.objects.filter(merchant_id = merchant_users_object.merchant_user_id, merchant_business_id = merchant_business_id)

    qs1 = GreenBillUser.objects.all().filter(is_merchant_staff = "1")

    try:
        merchant_user_id = Merchant_users.objects.filter(user_id = request.user).values('merchant_user_id')[0]['merchant_user_id']

        merchant_user_id_object = GreenBillUser.objects.get(id=merchant_user_id)
        
        qs_temp = Merchant_users.objects.filter(merchant_user_id = merchant_user_id_object, m_business_id = merchant_business_id.id).order_by('-id')
    
    except:
        qs_temp = ""

    data = []

    data.append({
        'name': merchant_user_id_object.first_name + " " + merchant_user_id_object.last_name,
        'mo_number':merchant_user_id_object.mobile_no
        })

    for temp in qs_temp:
        data.append({
            'name' : temp.user_id.first_name + " " + temp.user_id.last_name,
            'mo_number': temp.user_id.mobile_no
        })



    context  = {
        "role_list": qs,
        "user_list": data,
        'MyTeamNavclass': 'active',
        "MyTeamCollapsShow": "show",
        "userlogsActiveClass": "active"
    }

    return render(request, 'merchant/merchant_list_for_user_log.html', context)


    # startswith = str(merchant_business_id.id) + ','
    # endswith = ','+ str(merchant_business_id.id)
    # contains = ','+ str(merchant_business_id.id) + ','
    # exact = str(merchant_business_id.id)

    # try:
    #     check_subscription_available = merchant_subscriptions.objects.get(
    #         Q(merchant_id = merchant_object),
    #         Q(is_active = True),
    #         Q(business_ids__startswith = startswith) | 
    #         Q(business_ids__endswith = endswith) | 
    #         Q(business_ids__contains = contains) | 
    #         Q(business_ids__exact = exact)
    #     )
    # except:
    #     check_subscription_available = ""

    # # if check_subscription_available:
    # #     for object1 in qs_temp:
    # #         temp1 = GreenBillUser.objects.get(mobile_no=object.user_id)
    # #         qs31 = merchant_userrole.objects.filter(user = temp1)
    # #         for oject2 in qs31:
    # #             qs4 = merchant_role.objects.filter(role_name= oject2.role, merchant_business_id = merchant_business_id)
    # #             for oject3 in qs4:
    # #                 role_name = oject3.role_name

    # # else:


    # # number_of_users = ''
    # # if check_subscription_available:
    #     # if check_subscription_available.no_of_users:
    #     #     number_of_users = check_subscription_available.no_of_users

    # user_data = []

    # for object in qs_temp:
    #     temp = GreenBillUser.objects.get(mobile_no=object.user_id)
        
    #     qs3 = merchant_userrole.objects.filter(user = temp)
    
    #     for oject1 in qs3:
    #         object.user_id.role = oject1.id
    #         object.user_id.role_name = oject1.role
            
    #         qs4 = merchant_role.objects.filter(role_name= oject1.role, merchant_business_id = merchant_business_id)
    #         for oject2 in qs4:
    #             object.user_id.role_id = oject2.id

    #             assign_role_name = oject2.role_name

    #             if assign_role_name == 'Exe User':
    #                 user_data.append(temp)

    # # print(user_data)
    # if check_subscription_available:

    #     planforuser = 0

    #     if check_subscription_available.no_of_users:

    #         planforuser = check_subscription_available.no_of_users 

    #     avialable_exe_user = len(user_data)

    #     if int(planforuser) < int(avialable_exe_user + 1):

    #         for mobile_no in user_data:

    #             not_exist_user = GreenBillUser.objects.get(mobile_no=mobile_no).delete()

    # else:
    #     for mobile_no in user_data:
    #         print(mobile_no)
    #         not_exist_user = GreenBillUser.objects.get(mobile_no=mobile_no).delete()

    

def merchant_userlogs(request, mobile_no):

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']
    merchant_object = GreenBillUser.objects.get(id=merchant_id)

    merchant_profile = MerchantProfile.objects.get(m_user = merchant_object.id, m_active_account = 1)

    merchant_business_id = merchant_profile.id

    merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = merchant_business_id)

    UserVisit_details = UserVisit.objects.all().order_by('-id')

    new_data = []

    for data in UserVisit_details:
        if str(data.user) == mobile_no:
            new_data.append({
                'id': data.id,
                'timestamp': data.timestamp,
                'user': data.user,
                'remote_addr': data.remote_addr
                })


    # print(UserVisit_details,'----------------------')

    # merchant_user = []

    # merchant_user.append({
    #     'user_id': merchant_object,
    #     'mobile_no': merchant_object.mobile_no
    # })

    # merchant_user_temp = Merchant_users.objects.filter(merchant_user_id = merchant_object, m_business_id = merchant_business_id)

    # for user in merchant_user_temp:
    #     merchant_user.append({
    #         'user_id': user.user_id,
    #         'mobile_no': user.user_id.mobile_no
    #         })

    # new_data = []

    # for data in UserVisit_details:
    # 	for user in merchant_user:
	   #  	if data.user.mobile_no == user['mobile_no']:
		  #   	new_data.append({
		  #   		'id': data.id,
		  #   		'timestamp': data.timestamp,
		  #   		'user': data.user,
		  #   		'remote_addr': data.remote_addr
		  #   		})

    new_data.sort(reverse=True, key = lambda e: e['id'])
    
    context = {
    	'userlogs': new_data,
    	'MyTeamNavclass': 'active',
        "MyTeamCollapsShow": "show",
        "userlogsActiveClass": "active"
    }
    template = 'merchant/merchant-user-log.html'
    return render(request, template, context) 

def MerchantUserlogsDetails(request):
    print("ok")
