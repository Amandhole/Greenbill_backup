from role.models import role, module, feature, permission, userrole
from users.models import UserProfileImage, MerchantProfile, Merchant_users, Partner_users, PartnerProfile
from merchant_role.models import *
from merchant_enquiry.models import MerchantEnquiryModel
from app.forms import ChangeMerchnatBusinessForm
from merchant_cashmemo_design.models import Cash_Memo_Design_Model

from system_update.models import unread_system_updates
from category_and_tags.models import business_category

from django.conf import settings
User = settings.AUTH_USER_MODEL

from merchant_notice.models import merchant_notice_sent
from owner_notice_board.models import OwnerSentNotice
from merchant_software_apis.models import *
from django.db.models import Q
from itertools import chain

from parking_lot_apis.models import SaveParkingLotBill
from petrol_pump_apis.models import SavePetrolPumpBill
from merchant_setting.models import MerchantPaymentSetting

def userProfilePic(request):
    try:
        userDetails = MerchantProfile.objects.get(m_user=request.user, m_active_account=True)
    except:
        userDetails = ""
    
    profile_pic = UserProfileImage.objects.filter(user_id = request.user.id)

    m_profile_pic = ""

    try:
        if userDetails.m_business_logo:
            m_profile_pic = userDetails.m_business_logo.url
    except:
        pass


    context = {
                'ProfileImages': profile_pic,
                'm_profile_pic':m_profile_pic,
            }

    return context


# def show_search_suggestions(request):
#     tag1 = CustomerBill.objects.filter(mobile_no = request.user.id).values_list('customer_bill_category__bill_category_name', flat=True).distinct()
#     tag2 = CustomerBill.objects.filter(mobile_no = request.user.id).values_list('business_name__m_business_name', flat=True).distinct()
#     result_list = list(chain(tag1, tag2))

#     context = {
#         'search_suggestions':result_list,
#     }
#     return context

def module_permissions(request):
    
    # Actions Permissions Start

    user_roles = userrole.objects.filter(user = request.user.id)

    action_permissions_list = ''

    user_role = None

    if user_roles.exists():

        for x in user_roles:
            user_role = x.role

        action_permissions =  permission.objects.filter(role_id = user_role)

        action_permissions_list = action_permissions

    # Actions Permissions End

    # Module Permissions Start

    module_names = module.objects.all()

    if module_names.exists() and user_role is not None:

        for module1 in module_names:

            module_permission_temp = permission.objects.filter(role_id = user_role, module_id = module1.id)

            if module_permission_temp.exists():

                for module_permission in module_permission_temp:

                    if module_permission.view_permission != None or module_permission.add_permission != None or module_permission.edit_permission != None or module_permission.delete_permission != None:

                        module1.permission = True

    module_permissions_list = module_names
    
    context = {
                'action_permissions_list': action_permissions_list,
                'module_permissions_list': module_permissions_list,
            }

    # Module Permissions End

    return context


def super_admin(request):

    context = {
                'is_superuser': request.user.is_superuser,
            }

    return context

def merchant_admin(request):
    
    try:
        context = {
            'is_merchant' : request.user.is_merchant,
            'is_merchant_staff': request.user.is_merchant_staff
        }
    except:
        context = {}

    return context

def ChangeMerchnatBusinessForm_context(request):

    try:

        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        ChangeMerchnatBusinessForm1 = ChangeMerchnatBusinessForm(user = merchant_users_object.merchant_user_id)

        get_merchant_active_id = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = True)

        business_category_name = get_merchant_active_id.m_business_category.business_category_name

        merchant = get_merchant_active_id

        business_category = MerchantProfile.objects.filter(m_user = merchant_users_object.merchant_user_id, m_business_category=merchant.m_business_category)


        context = {
                'm_business_previous_id' : get_merchant_active_id.id,
                'm_business_category_name' : business_category_name,
                
                'ChangeMerchnatBusinessForm': ChangeMerchnatBusinessForm1,
                'merchant' : merchant,
                'business_category' : business_category,
          
            }
    except:
        context = {}

    return context


def merchant_user_module_permissions(request):

    try:

        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        get_merchant_active_id = MerchantProfile.objects.get(m_user = merchant_users_object.merchant_user_id, m_active_account = True)

        business_category_id = get_merchant_active_id.m_business_category.id
        
        # Actions Permissions Start

        user_roles = merchant_userrole.objects.filter(user = request.user.id)

        action_permissions_list = ''

        user_role = None

        if user_roles.exists():

            for x in user_roles:
                user_role = x.role

            action_permissions =  merchant_permission.objects.filter(role_id = user_role)

            action_permissions_list = action_permissions

        # Actions Permissions End

        # Module Permissions Start

        module_names = merchant_module.objects.all()

        if module_names.exists() and user_role is not None:

            for module1 in module_names:

                module_permission_temp = merchant_permission.objects.filter(role_id = user_role, module_id = module1.id)

                if module_permission_temp.exists():

                    for module_permission in module_permission_temp:

                        # parking
                        exclude_parking_feature_list = ['Cash Memos', 'Receipts', 'Stamps', 'Bill Design Request']

                        # petrol
                        exclude_petrol_feature_list = ['Cash Memos', 'Receipts', 'Stamps', 'Bill Design Request']
                        
                        if business_category_id == 11:
                            if str(module_permission.feature_id) not in exclude_parking_feature_list:
                                if module_permission.view_permission == '1'or module_permission.add_permission == '1' or module_permission.edit_permission == '1' or module_permission.delete_permission == '1':
                                    module1.permission = True
                
                        elif business_category_id == 12:
                            if str(module_permission.feature_id) not in exclude_petrol_feature_list:
                                if module_permission.view_permission == '1'or module_permission.add_permission == '1' or module_permission.edit_permission == '1' or module_permission.delete_permission == '1':
                                    module1.permission = True
                        else:
                            if module_permission.view_permission == '1'or module_permission.add_permission == '1' or module_permission.edit_permission == '1' or module_permission.delete_permission == '1':
                                module1.permission = True

        module_permissions_list = module_names
        
        context = {
                    'merchnat_action_permissions_list': action_permissions_list,
                    'merchnat_module_permissions_list': module_permissions_list,
                    'merchant_action_permissions_list': action_permissions_list,
                    'merchant_module_permissions_list': module_permissions_list,
                }

        # Module Permissions End

        # print(module_permissions_list)

        return context

    except:
        context = {
                    'merchnat_action_permissions_list': '',
                    'merchnat_module_permissions_list': '',
                    'merchant_action_permissions_list': '',
                    'merchant_module_permissions_list': '',
                }

        return context


def getMerchnatBusinesscategory_context(request):

    try:

        get_merchnat_business_category = business_category.objects.order_by("business_category_name")

        context = {
                'merchnat_business_category' : get_merchnat_business_category,
            }

    except:
        context = {}

    return context



def get_unread_merchant_inquiry_count(request):
    unread_count = MerchantEnquiryModel.objects.filter(
        read_status=False).count()

    context = {
        'dm_inquiry_unread_count': unread_count,
    }
    return context

def display_notification_merchant_notice(request):
    # print(request.user.id)
    if request.user.is_authenticated:
        unread_status = merchant_notice_sent.objects.filter(
            read_status="0", notification=True, user_id=request.user)
        context = {
            'unread_notification_status_merchant': unread_status,
        }

        return context
    else:
        context = {
            
        }
        return context


def display_notification_owner_notice(request):
    # print(request.user.id)
    if request.user.is_authenticated:
        unread_status = OwnerSentNotice.objects.filter(
            read_status="0", notification=True, user_id=request.user)
        context = {
            'unread_notification_status': unread_status,
        }

        return context
    else:
        context = {
            
        }
        return context

def getUserRole(request):

    try:
        user_roles = userrole.objects.filter(user = request.user.id)
        # print(user_roles[0].role)
        context = {
            'user_role': user_roles[0].role
        }
    except:
        context = {}
    # print(context)
    return context


def get_unread_merchant_cashMemoDesign_count(request):
    unread_count = Cash_Memo_Design_Model.objects.filter(
        read_status=False).count()

    context = {
        'memo_design_unread_count': unread_count,
    }
    return context

def partner_category(request):
    try:
        partner_users_object = Partner_users.objects.get(user_id = request.user)

        get_partner_active_id = PartnerProfile.objects.get(p_user = partner_users_object.partner_user_id, p_active_account = True)

        business_category_name = get_partner_active_id.p_category
        
        context = {
        'partnercategory' : business_category_name,
        }
    except:
        context = {}

    return context

def payment_settings(request):
    try:
        merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']
        business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)
        try:
            data = MerchantPaymentSetting.objects.get(m_business_id = business_object.id)
            
            
        except:
            data = ""
        print(data)
        context = {
        'data' : data,
        }
    except:
        context = {}

    return context


def show_search_suggestions(request):
    updated_search_list=[]
    bill_category_temp = ''
    bill_categories = bill_category.objects.order_by('bill_category_name')
    for bill_cat in bill_categories:

        customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user,customer_bill_category = bill_cat).values('customer_bill_category__bill_category_name').distinct()
        for bill in customer_bill_list:

            updated_search_list.append({
                'bill_category' : bill['customer_bill_category__bill_category_name'],
            })


        parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no=request.user,bill_category_id = bill_cat.id, is_pass = False).order_by('-id')
        for bill in parking_bill_list:

            try:
                bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
            except:
                bill_category_temp = ""

    updated_search_list.append({
        'bill_category' : bill_category_temp,
    })


    for bill_cat in bill_categories:                                                      
        petrol_pump_bill_list = SavePetrolPumpBill.objects.filter(mobile_no=request.user,bill_category_id = bill_cat.id).order_by('-id')
        for bill in petrol_pump_bill_list:

            try:
                bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)

            except:
                bill_category_temp = ""

    updated_search_list.append({
        'bill_category' : bill_category_temp,
    })


    context = {
        'search_suggestions':updated_search_list,
    }
    return context


def get_unread_system_update_count_partner(request):
    unread_updates = unread_system_updates.objects.filter(
        group_partner=True, read_status=False, user_id=request.user.id).count()

    context = {
        'unread_updates' : unread_updates
    }
    return context

# def get_unread_system_update_count(request):
#     try:
        

#         if request.user.is_authenticated:

#             merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']

#             merchant_object = GreenBillUser.objects.get(id=merchant_id)

#             all_business = MerchantProfile.objects.filter(m_user=merchant_id)

#             business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account=1)

#             all_system_update = []


#             # Petrol Pump
#             if business_object.m_business_category.id == 11:
#                 petrol_system_update = unread_system_updates.objects.filter(group_petrol=True, read_status=False, user_id=request.user.id).order_by("-id")
#                 for system_update in petrol_system_update:
#                     all_system_update.append(system_update)

#             # Parking Lot
#             if business_object.m_business_category.id == 12:
#                 parking_system_update = unread_system_updates.objects.filter(group_parking=True, read_status=False, user_id=request.user.id).order_by("-id")
#                 for system_update in parking_system_update:
#                     all_system_update.append(system_update)

#             other_system_update = unread_system_updates.objects.filter(group_merchant=True, read_status=False, user_id=request.user.id).order_by("-id")
#             for system_update in other_system_update:
#                 all_system_update.append(system_update)
#             len_count=len(all_system_update)
#             system_update_ids = []
#             if system_update != '[]':
#                 print(all_system_update)
#                 for system_update in all_system_update:
                    
#                     if system_update.id in system_update_ids:
#                         pass
#                     else:
#                         system_update_ids.append(system_update.id)
                        
#                     context = {
#                         'unread_updates_mer' : len(system_update_ids),
#                     }
#                     return context
#             else:
#                 context = {
#                     'unread_updates_mer' : len_count,

#                 }
#                 return context
#     except:
        
#         context = {

#         }
#         return context





# def show_search_suggestions(request):
#     updated_search_list=[]

#     bill_categories = bill_category.objects.order_by('bill_category_name').distinct()
#     for bill_cat in bill_categories:

#         customer_bill_list = CustomerBill.objects.filter(mobile_no = request.user,customer_bill_category = bill_cat).order_by('-id').distinct()
#         for bill in customer_bill_list:
#             updated_search_list.append({
#                 'bill_category' : bill.customer_bill_category,
#                 # 'business_name' : bill.business_name
#             })


#         parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no=request.user,bill_category_id = bill_cat.id, is_pass = False).order_by('-id').distinct()
#         for bill in parking_bill_list:
            
#             try:
#                 business_name = MerchantProfile.objects.get(id = bill.m_business_id)
#             except:
#                 business_name = ""

#             try:
#                 bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)
#             except:
#                 bill_category_temp = ""

#             updated_search_list.append({
#                     'bill_category' : bill_category_temp,
#                     # 'business_name' : business_name
#             })

                                                                
#         petrol_pump_bill_list = SavePetrolPumpBill.objects.filter(mobile_no=request.user,bill_category_id = bill_cat.id).order_by('-id').distinct()
#         for bill in petrol_pump_bill_list:
#             try:
#                 business_name = MerchantProfile.objects.get(id = bill.m_business_id)
#             except:
#                 business_name = ""
#             try:
#                 bill_category_temp = bill_category.objects.get(id = bill.bill_category_id)

#             except:
#                 bill_category_temp = ""

#             updated_search_list.append({
#                 'bill_category' : bill_category_temp,
#                 # 'business_name' : business_name
#             })


#     context = {
#         'search_suggestions':updated_search_list,
#     }
#     return context


