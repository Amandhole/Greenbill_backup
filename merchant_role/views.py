from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from .models import *
from .forms import *
from django.contrib import messages
import sweetify

from django.conf import settings
User = settings.AUTH_USER_MODEL

from users.models import GreenBillUser, Merchant_users
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_merchant_or_merchant_staff


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_role_detail_view(request):

    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_users_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    try:
        
        merchant_users_object = Merchant_users.objects.get(user_id = request.user)

        qs = merchant_role.objects.filter(merchant_id = merchant_users_object.merchant_user_id, merchant_business_id = merchant_business_id).order_by('-id')

        context = {
            "role_list": qs,
            'MyTeamNavclass': 'active',
            "MyTeamCollapsShow": "show",
            "RolesPermissionSettingsNavclass": "active"
        }

        return render(request, 'merchant/Roles & Permission/merchant-role.html', context)

    except merchant_role.DoesNotExist:
        return render(request, 'error-404.html')

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_create_role_view(request, *args, **kwargs):

    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_users_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    if request.method == "POST":
        post_data = request.POST or None
        if post_data != None:
            my_form = RoleForm(request.POST)
            if my_form.is_valid():
                role_name = my_form.cleaned_data.get("role_name")
                
                if merchant_business_id.m_business_category.id != 11 and merchant_business_id.m_business_category.id != 12:
                    if role_name != "Exe User":
                        merchant_users_object = Merchant_users.objects.get(user_id = request.user)
                        merchant_exists_role = merchant_role.objects.filter(merchant_business_id = merchant_business_id, merchant_id = merchant_users_object.merchant_user_id, role_name__iexact = role_name)
                        if merchant_exists_role:
                            return JsonResponse({'success':False, 'msg':'Role already exists...'})
                        else:
                            role_description = my_form.cleaned_data.get("role_description")
                            merchant_role.objects.create(merchant_business_id = merchant_business_id, merchant_id = merchant_users_object.merchant_user_id, role_name = role_name, role_description = role_description)
                            return JsonResponse({'success':True})
                    else:
                        return JsonResponse({'success':False})
                else:
                    if role_name != "Operator":
                        merchant_users_object = Merchant_users.objects.get(user_id = request.user)
                        merchant_exists_role_new =  merchant_role.objects.filter(merchant_business_id = merchant_business_id, merchant_id = merchant_users_object.merchant_user_id, role_name__iexact = role_name)
                        if merchant_exists_role_new:
                            return JsonResponse({'success':False,'msg':'Role already exists...'})
                        else:
                            role_description = my_form.cleaned_data.get("role_description")
                            merchant_role.objects.create(merchant_business_id = merchant_business_id, merchant_id = merchant_users_object.merchant_user_id, role_name = role_name, role_description = role_description)
                            return JsonResponse({'success':True})
                    else:
                        return JsonResponse({'success':False})
            return JsonResponse({'success':False})
        return JsonResponse({'success':False})
    return JsonResponse({'success':False})
        

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_delete_role_view(request, id, *args, **kwargs):
    instance = merchant_role.objects.get(id=id)
    instance.delete()
    return JsonResponse({'success':True})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_role_detail_by_id_view(request, id):
    try:
        instance = get_object_or_404(merchant_role, id=id)
        return JsonResponse({'role_id':id,'role_name':instance.role_name,'role_description':instance.role_description})
    except merchant_role.DoesNotExist:
        return render(request, 'error-404.html')

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/") 
def merchant_role_update_view(request, id):
    if request.method == "POST":
        post_data = request.POST or None
        if post_data != None:
            my_form = RoleForm_edit(request.POST)
            if my_form.is_valid():
                role_name = my_form.cleaned_data.get("edit_role_name")
                role_description = my_form.cleaned_data.get("edit_role_description")
                merchant_role.objects.filter(id=id).update(role_name = role_name, role_description = role_description)
                return JsonResponse({'success':True})

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_permission_view(request, id):

    instance = merchant_role.objects.get(id=id)

    qs = merchant_feature.objects.all().order_by('module_id__module_name')

    for object in qs:
        qs1 = merchant_permission.objects.filter(role_id = id).filter(feature_id=object.id)
        for oject1 in qs1:
            object.view_permission = oject1.view_permission
            object.add_permission = oject1.add_permission
            object.edit_permission = oject1.edit_permission
            object.delete_permission = oject1.delete_permission

    context  = {
        "feature_list": qs,
        "role_name": instance.id,
        'MyTeamNavclass': 'active',
        "MyTeamCollapsShow": "show",
        "RolesPermissionSettingsNavclass": "active"
    }

    return render(request, 'merchant/Roles & Permission/merchant-permission.html', context)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_permission_update_view(request):
    dict = request.POST
    if request.method == "POST":
        post_data = request.POST or None 
        if post_data != None:

            merchant_users_object = Merchant_users.objects.get(user_id = request.user)

            list_length = int(dict.get('list_length'))

            for x in range(1, list_length + 1):

                role_id_temp = 'role_id[' + str(x) + ']'
                try:
                    role_id = merchant_role.objects.get(id = dict.get(role_id_temp))
                except:
                    role_id = ""

                module_id_temp = 'module_id[' + str(x) + ']'
                try:
                    module_id = merchant_module.objects.get(module_name__iexact = dict.get(module_id_temp))
                except:
                    module_id = ""

                feature_id_temp = 'feature_id[' + str(x) + ']'
                try:
                    feature_id = merchant_feature.objects.get(feature_id__iexact = dict.get(feature_id_temp))
                except:
                    feature_id = ""

                if role_id and module_id_temp and feature_id_temp:

                    view_permission_temp = 'view_permission[' + str(x) + ']'
                    add_permission_temp = 'add_permission[' + str(x) + ']'
                    edit_permission_temp = 'edit_permission[' + str(x) + ']'
                    delete_permission_temp = 'delete_permission[' + str(x) + ']'
                    
                    merchant_permission.objects.update_or_create(merchant_user_id = merchant_users_object.merchant_user_id, role_id = role_id, module_id = module_id, feature_id = feature_id, 
                    defaults={'view_permission': dict.get(view_permission_temp), 'add_permission': dict.get(add_permission_temp),
                    'edit_permission': dict.get(edit_permission_temp), 'delete_permission': dict.get(delete_permission_temp)})

    sweetify.success(request, title="Success", icon='success', text='Permission Updated.')
    
    # return redirect(merchant_permission_view, id = dict.get(role_id_temp))
    return redirect(merchant_role_detail_view)

@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_assign_role_details_view(request):

    merchant_users_object = Merchant_users.objects.get(user_id = request.user)

    merchant_object = merchant_users_object.merchant_user_id

    merchant_business_id = MerchantProfile.objects.get(m_user = merchant_object, m_active_account = True)

    qs1 = Merchant_users.objects.filter(merchant_user_id = merchant_users_object.merchant_user_id, m_business_id = merchant_business_id.id)

    for object in qs1:

        temp = GreenBillUser.objects.get(mobile_no = object.user_id)

        qs3 = merchant_userrole.objects.filter(user = temp)
    
        for oject1 in qs3:
            object.role = oject1.id
            object.role_name = oject1.role
            qs4 = merchant_role.objects.filter(role_name = oject1.role)
            for oject2 in qs4:
                object.role_id = oject2.id
    
    qs2 = merchant_role.objects.filter(merchant_id = merchant_users_object.merchant_user_id, merchant_business_id = merchant_business_id)

    context  = {
        "user_list": qs1,
        "role_list": qs2,
        'MyTeamNavclass': 'active',
        "MyTeamCollapsShow": "show",
        "RolesPermissionSettingsNavclass": "active"
    }

    return render(request, 'merchant/Roles & Permission/merchant-role-assign.html', context)


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def merchant_assign_role_view(request):
    
    if request.method == "POST":
        post_data = request.POST or None
        if post_data != None:
            my_form = RoleAssign_form(request.POST)

            if my_form.is_valid():

                auth_id_temp = my_form.cleaned_data.get("auth_id")
            
                role_id_temp = my_form.cleaned_data.get("role_name")
                
                user_role_id = my_form.cleaned_data.get("user_role_id")
                
                if user_role_id is not None:
                    merchant_userrole.objects.filter(id = user_role_id).update(user_id = auth_id_temp, role_id = role_id_temp)
                else:                    
                    merchant_userrole.objects.create(user_id = auth_id_temp, role_id = role_id_temp)

                return JsonResponse({'success':True})
    else:
        return False
