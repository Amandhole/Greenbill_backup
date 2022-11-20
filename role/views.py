import sweetify
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from .models import role, module, feature, permission, userrole
from .forms import RoleForm, RoleForm_edit, RoleAssign_form
from django.contrib import messages
from django.conf import settings
User = settings.AUTH_USER_MODEL
from users.models import GreenBillUser
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner


# Create your views here.

# @login_required(login_url="/login/")

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def role_detail_view(request):
    try:
        qs = role.objects.all().order_by('-id') # pk-> primary key
        context = {"role_list": qs, "myteamNavActiveClass": "active", "myteamInfoCollapseShow": "show", "RoleNavclass": 'active'}
        return render(request, 'role/role.html', context)
    except role.DoesNotExist:
        return render(request, 'error-404.html')

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def create_role_view(request, *args, **kwargs):
   
    if request.method == "POST":
        post_data = request.POST or None
        if post_data != None:
            my_form = RoleForm(request.POST)
            if my_form.is_valid():
                role_name = my_form.cleaned_data.get("role_name")
                result = role.objects.filter(role_name__iexact = role_name)

                if result:
                    return JsonResponse({'success':False,'msg':'Role name already available.!!!'})
                else:
                    role_description = my_form.cleaned_data.get("role_description")
                    role.objects.create(role_name = role_name, role_description = role_description)
                    return JsonResponse({'success':True})
                

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def delete_role_view(request, id, *args, **kwargs):
    instance = role.objects.get(id=id)
    instance.delete()
    return JsonResponse({'success':True})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/") 
def role_detail_by_id_view(request, id):
    try:
        instance = get_object_or_404(role, id=id)
        return JsonResponse({'role_id':id,'role_name':instance.role_name,'role_description':instance.role_description})
    except role.DoesNotExist:
        return render(request, 'error-404.html')

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")  
def role_update_view(request, id):
    if request.method == "POST":
        post_data = request.POST or None
        if post_data != None:
            my_form = RoleForm_edit(request.POST)
            if my_form.is_valid():
                role_name = my_form.cleaned_data.get("edit_role_name")
                role_description = my_form.cleaned_data.get("edit_role_description")
                role.objects.filter(id=id).update(role_name = role_name, role_description = role_description)
                return JsonResponse({'success':True})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def permission_view(request, id):
    try: 
        instance = role.objects.get(id=id)

        qs = feature.objects.all()

        # qs1 = permission.objects.filter(role_id = id).select_related('feature_id')

        for object in qs:
            qs1 = permission.objects.filter(role_id = id).filter(feature_id=object.id)
            for oject1 in qs1:
                object.view_permission = oject1.view_permission
                object.add_permission = oject1.add_permission
                object.edit_permission = oject1.edit_permission
                object.delete_permission = oject1.delete_permission

        # instance1 = permission.objects.filter(role_id=id)

        context  = {"feature_list": qs, "role_name": instance.id, "myteamNavActiveClass": "active", "myteamInfoCollapseShow": "show", "RoleNavclass": 'active'}

        return render(request, 'role/permission.html', context )

    except feature.DoesNotExist:
        return render(request, 'error-404.html')

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def permission_update_view(request):
    dict = request.POST
    if request.method == "POST":
        post_data = request.POST or None 
        if post_data != None:
            list_length = int(dict.get('list_length'))
            for x in range(1, list_length + 1):

                role_id_temp = 'role_id[' + str(x) + ']'
                role_id = role.objects.get(id = dict.get(role_id_temp))

                module_id_temp = 'module_id[' + str(x) + ']'
                module_id = module.objects.get(module_name__iexact = dict.get(module_id_temp))

                feature_id_temp = 'feature_id[' + str(x) + ']'
                feature_id = feature.objects.get(feature_id__iexact = dict.get(feature_id_temp))

                view_permission_temp = 'view_permission[' + str(x) + ']'
                add_permission_temp = 'add_permission[' + str(x) + ']'
                edit_permission_temp = 'edit_permission[' + str(x) + ']'
                delete_permission_temp = 'delete_permission[' + str(x) + ']'
                
                permission.objects.update_or_create(role_id = role_id, module_id = module_id, feature_id = feature_id, 
                defaults={'view_permission': dict.get(view_permission_temp), 'add_permission': dict.get(add_permission_temp),
                'edit_permission': dict.get(edit_permission_temp), 'delete_permission': dict.get(delete_permission_temp)})

                # permission.objects.create(role_id = role_id, module_id = module_id, feature_id = feature_id, view_permission = dict.get(view_permission_temp), add_permission = dict.get(add_permission_temp), 
                # edit_permission = dict.get(edit_permission_temp), delete_permission = dict.get(delete_permission_temp))

    sweetify.success(request, title="Success", icon='success', text='Permission Updated.')
    
    return redirect(permission_view, id = dict.get(role_id_temp))

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def assign_role_details_view(request):

    # qs1 = User.objects.filter().select_related('userrole')

    qs1 = GreenBillUser.objects.all().filter(is_staff = "1")

    for object in qs1:
        temp = GreenBillUser.objects.get(id=object.id)
        qs3 = userrole.objects.filter(user = temp)
    
        for oject1 in qs3:
            object.role = oject1.id
            object.role_name = oject1.role
            qs4 = role.objects.filter(role_name= oject1.role)
            for oject2 in qs4:
                object.role_id = oject2.id

    
    
    qs2 = role.objects.all()

    context  = {"user_list": qs1, "role_list": qs2, "myteamNavActiveClass": "active", "myteamInfoCollapseShow": "show", "RoleNavclass": 'active'}

    return render(request, 'role/role_assign.html', context)


# def assign_role_view_details_by_id(request, id):

#     instance = User.objects.filter(id=id).select_related('userrole')

#     return JsonResponse({'user_id':id,'role_name':instance.role_name})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def assign_role_view(request):
    
    if request.method == "POST":
        post_data = request.POST or None
        if post_data != None:
            my_form = RoleAssign_form(request.POST)

            if my_form.is_valid():

                auth_id_temp = my_form.cleaned_data.get("auth_id")
                # auth_id = User.objects.get(id = auth_id_temp)

                role_id_temp = my_form.cleaned_data.get("role_name")
                # role_id = role.objects.get(id = role_id_temp)

                user_role_id = my_form.cleaned_data.get("user_role_id")

                
                if user_role_id is not None:
                    # userrole.objects.update_or_create(user=auth_id, defaults={'role': role_id})
                    userrole.objects.filter(id = user_role_id).update(user_id = auth_id_temp, role_id = role_id_temp)
                else:
                    
                    userrole.objects.create(user_id = auth_id_temp, role_id = role_id_temp)

                # userrole.objects.update_or_create(user_id=auth_id, defaults={'role_id': role_id})

                return JsonResponse({'success':True})
    else:
        return False
