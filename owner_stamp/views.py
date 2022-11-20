from django import forms
from django.shortcuts import render
from .models import wstampmodels, stampdmodels
from .forms import wstampforms, stampdforms
import sweetify

def wstampview(request):
    if request.method == "POST":
        stamp_name = request.POST['stamp_name']
        stamp_content = request.POST['stamp_content'] 
        selection_design = request.POST['selection_design'] 
        option_color = request.POST['option_color'] 

        obj1 = ""
        obj2 = ""
        if request.POST['stamp_id'] != "":
            obj1 = wstampmodels.objects.update_or_create(
                id=int(request.POST["stamp_id"]),
                defaults={"stamp_name": stamp_name, "stamp_content": stamp_content, "selection_design": selection_design, "option_color":option_color})
        else:
            selection_design = request.POST['selection_design']  
            obj2 = wstampmodels.objects.create(
                stamp_name=stamp_name, stamp_content=stamp_content, selection_design=selection_design, option_color=option_color)
        if obj1:
            sweetify.success(request, title="Success", icon='success',
                             text='Stamp updated Successfully.', timer=1500)

        elif obj2:
            sweetify.success(request, title="Success", icon='success',
                             text='Stamp created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...",
                             icon='error', text='Failed to create.', timer=1000)
            
    data = wstampmodels.objects.all().order_by('-id')

    context = {
        'title' : "this is title",
        'data': data,
        'DesignNavClass':'active',
        'DesignNavClasscollapsShows':'show',
        'StampNavClass':'active',
    }

    return render(request, "super_admin/owner_stamp/stamp.html", context)

def stampdview(request):
    data_status = stampdmodels.objects.all()
    print(data_status)
    return render(request, "super_admin/owner_stamp/stampdesign.html", {'data_status': data_status})

def Delete_Offer(request, id):
    offer_obj = wstampmodels.objects.get(id=id).delete()
    if offer_obj:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})






