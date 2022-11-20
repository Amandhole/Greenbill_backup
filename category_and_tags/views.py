from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.forms.utils import ErrorList
from .forms import *
from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner
import sweetify

# Business Category module Start

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def business_category_view(request):

    qs = business_category.objects.all().order_by('-id')
    business_category_count = business_category.objects.all().count()
    context = {
        "business_category_list" : qs,
        'business_category_count':business_category_count,
        "SettingsNavclass": "active",
        "settingsCollapseShow": "show",
        "CategoryandTagsExpanded": "true",
        "CategoryandTagShow":"show",
        "BusinessCategoryNavclass":"active",
    }

    if request.method == "POST":
    	business_category_name_temp = request.POST.get('business_category_name')
    	business_category_present = business_category.objects.filter(business_category_name__iexact=business_category_name_temp)
    	print(business_category_present)
    	if business_category_present:
    		print(business_category_present)
    		return JsonResponse({'status':'error', 'message': 'Category Already Availble'})
    	else:
    		post_data = request.POST or None
    		if post_data != None:
    			my_form = BusinessCategoryForm(request.POST)
    			if my_form.is_valid():
    				business_category_name = my_form.cleaned_data.get("business_category_name")
    				business_category_description = my_form.cleaned_data.get("business_category_description")
    				business_category.objects.create(business_category_name = business_category_name, business_category_description = business_category_description)
    				return JsonResponse({'status':'success'})
    			else:
    				return JsonResponse({'status':'error'})
    		else:
    				return JsonResponse({'status':'error'})
    else:
        return render(request, "category_and_tags/business_category.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def delete_business_category_view(request, id):
    instance = business_category.objects.get(id=id)
    instance.delete()
    return JsonResponse({'success':True})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def business_category_by_id_view(request, id):
    try:
        instance = get_object_or_404(business_category, id=id)
        return JsonResponse({'business_category_id':id,'business_category_name':instance.business_category_name,'business_category_description':instance.business_category_description})
    except business_category.DoesNotExist:
        return render(request, 'error-404.html')

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def business_category_update_view(request, id):
    if request.method == "POST":
        post_data = request.POST or None
        if post_data != None:
            my_form = BusinessCategoryEditForm(request.POST)
            if my_form.is_valid():
                edit_business_category_name = my_form.cleaned_data.get("edit_business_category_name")
                edit_business_category_description = my_form.cleaned_data.get("edit_business_category_description")
                business_category.objects.filter(id=id).update(business_category_name = edit_business_category_name, business_category_description = edit_business_category_description)
                return JsonResponse({'status':'success'})
            else:
                return JsonResponse({'status':'error'})
        else:
                return JsonResponse({'status':'error'})
    else:
                return JsonResponse({'status':'error'})

# Business Category module End

# Bill Category module Start

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def bill_category_view(request):
    qs = bill_category.objects.all().order_by('-id')
    bill_category_count = bill_category.objects.all().count()
    context = {
        "bill_category_list" : qs,
        'bill_category_count':bill_category_count,
        "SettingsNavclass": "active",
        "settingsCollapseShow": "show",
        "CategoryandTagsExpanded": "true",
        "CategoryandTagShow":"show",
        "BillCategoryNavclass": "active",
    }

    if request.method == "POST":
        bill_category_name_temp = request.POST.get('bill_category_name')
        print('bill_category_name_temp',bill_category_name_temp)
        bill_category_present = bill_category.objects.filter(bill_category_name__iexact=bill_category_name_temp)
        print('XX',bill_category_present)
        if bill_category_present:
            print('QQ',bill_category_present)
            # return JsonResponse({'status':'success'}, status=200)
            sweetify.success(request, title="Error", icon='error', text='Bill Category Already Exists!!.', timer=1000)
            return redirect(bill_category_view)
        else:
            print('WW')
            post_data = request.POST or None
            if post_data != None:
                print('EE')
                try:
                    bill_category_id = request.POST['edit_bill_category_id']
                except:
                    bill_category_id = ""

            if bill_category_id:
                print('RR')
                my_form = BillCategoryEditForm(request.POST, request.FILES)
                if my_form.is_valid():
                    edit_bill_category_name = my_form.cleaned_data.get("edit_bill_category_name")
                    edit_bill_category_description = my_form.cleaned_data.get("edit_bill_category_description")
                    edit_bill_category_icon = my_form.cleaned_data.get("edit_bill_category_icon")
                    if edit_bill_category_icon:
                        print('TT')
                        bill_category_object = bill_category.objects.get(id = bill_category_id)
                        bill_category_object.icon = edit_bill_category_icon
                        bill_category_object.save()
                        print('hii')
                        result = bill_category.objects.filter(id=bill_category_id).update(bill_category_name = edit_bill_category_name, bill_category_description = edit_bill_category_description)
                        return JsonResponse({'status':'success'}, status=200)
                    else:
                        print('hiii12')
                        result = bill_category.objects.filter(id=bill_category_id).update(bill_category_name = edit_bill_category_name, bill_category_description = edit_bill_category_description)
                        return JsonResponse({'status':'success'}, status=200)
                    if result:
                        print('hiii112')
                        return JsonResponse({'status':'success'}, status=200)
                        # sweetify.success(request, title="Success", icon='success', text='Bill Category Updated.', timer=1000)
                        # return redirect(bill_category_view)

                else:
                    return JsonResponse({'status':'error'})
            else:
                print('DD')
                my_form = BillCategoryForm(request.POST, request.FILES)
                if my_form.is_valid():
                    bill_category_name = my_form.cleaned_data.get("bill_category_name")
                    bill_category_description = my_form.cleaned_data.get("bill_category_description")
                    bill_category_icon = my_form.cleaned_data.get("bill_category_icon")
                    bill_category.objects.create(bill_category_name = bill_category_name, bill_category_description = bill_category_description, icon = bill_category_icon)
                    # return JsonResponse({'status':'success'}, status=200)
                    sweetify.success(request, title="Success", icon='success', text='Bill Category addded.', timer=1000)
                    return redirect(bill_category_view)

                else:

                    return JsonResponse({'status':'error'})

    else:
        return render(request, "category_and_tags/bill_category.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def delete_bill_category_view(request, id):
    instance = bill_category.objects.get(id=id)
    instance.delete()
    return JsonResponse({'success':True})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def bill_category_by_id_view(request, id):
    try:
        instance = get_object_or_404(bill_category, id=id)
        try:
            bill_icon = instance.icon.url
        except:
            bill_icon = ""

        return JsonResponse({'bill_category_id':id,'bill_category_name':instance.bill_category_name,'bill_category_description':instance.bill_category_description, 'bill_icon':bill_icon})
    except bill_category.DoesNotExist:
        return render(request, 'error-404.html')

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/") 
def bill_category_update_view(request, id):
    if request.method == "POST":
        post_data = request.POST or None
        if post_data != None:
        	my_form = BillCategoryEditForm(request.POST, request.FILES)
        	if my_form.is_valid():
        		edit_bill_category_name = my_form.cleaned_data.get("edit_bill_category_name")
        		edit_bill_category_description = my_form.cleaned_data.get("edit_bill_category_description")
        		edit_bill_category_icon = my_form.cleaned_data.get("edit_bill_category_icon")
        		if edit_bill_category_icon:
        			bill_category.objects.filter(id=id).update(bill_category_name = edit_bill_category_name, bill_category_description = edit_bill_category_description, icon = edit_bill_category_icon)
        		else:
        			bill_category.objects.filter(id=id).update(bill_category_name = edit_bill_category_name, bill_category_description = edit_bill_category_description)
        			# return JsonResponse({'status':'success'}, status=200)
        			print("hii")
        			sweetify.success(request, title="Success", icon='success', text='Bill Category Updated.', timer=1000)
        		return redirect(bill_category_view)
        	else:
        		return JsonResponse({'status':'error'})
        else:
        	return JsonResponse({'status':'error'})
    else:
    	return JsonResponse({'status':'error'})

# Bill Category module End


# Bill Tags module Start

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def bill_tags_view(request):
    qs = bill_tags.objects.all().order_by('-id')
    bill_tags_count = bill_tags.objects.all().count()
    context = {
        "bill_tags_list" : qs,
        "SettingsNavclass": "active",
        'bill_tags_count':bill_tags_count,
        "settingsCollapseShow": "show",
        "CategoryandTagsExpanded": "true",
        "CategoryandTagShow":"show",
        "BillTagsNavclass": "active",
    }
    if request.method == "POST":
        bill_tags_name_temp = request.POST.get('bill_tags_name')
        bill_tags_present = bill_tags.objects.filter(bill_tags_name__iexact=bill_tags_name_temp)
        print(bill_tags_present)
        if bill_tags_present:
            print(bill_tags_present)
            return JsonResponse({'status':'error', 'message': 'Category Already Availble'})
        else:
            print('DD')
            post_data = request.POST or None
            if post_data != None:
                print('XX')
                my_form = BillTagsForm(request.POST)
                if my_form.is_valid():
                    bill_tags_name = my_form.cleaned_data.get("bill_tags_name")
                    bill_tags_description = my_form.cleaned_data.get("bill_tags_description")
                    bill_tags.objects.create(bill_tags_name = bill_tags_name, bill_tags_description = bill_tags_description)
                    return JsonResponse({'status':'success'})
                else:
                    return JsonResponse({'status':'error'})
            else:
                    return JsonResponse({'status':'error'})
    else:
        return render(request, "category_and_tags/bill_tags.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def delete_bill_tags_view(request, id):
    instance = bill_tags.objects.get(id=id)
    instance.delete()
    return JsonResponse({'success':True})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/") 
def bill_tags_by_id_view(request, id):
    try:
        instance = get_object_or_404(bill_tags, id=id)
        return JsonResponse({'bill_tags_id':id,'bill_tags_name':instance.bill_tags_name,'bill_tags_description':instance.bill_tags_description})
    except bill_tags.DoesNotExist:
        return render(request, 'error-404.html')

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")  
def bill_tags_update_view(request, id):
    if request.method == "POST":
        post_data = request.POST or None
        if post_data != None:
            my_form = BillTagsEditForm(request.POST)
            if my_form.is_valid():
                edit_bill_tags_name = my_form.cleaned_data.get("edit_bill_tags_name")
                edit_bill_tags_description = my_form.cleaned_data.get("edit_bill_tags_description")
                bill_tags.objects.filter(id=id).update(bill_tags_name = edit_bill_tags_name, bill_tags_description = edit_bill_tags_description)
                return JsonResponse({'status':'success'})
            else:
                return JsonResponse({'status':'error'})
        else:
                return JsonResponse({'status':'error'})
    else:
                return JsonResponse({'status':'error'})

# Bill Tags module End

