from django.shortcuts import render
from .models import Add_Module_Name, Video_Model, FAQs_Model, Blogs_Model
import sweetify
from django.http import JsonResponse
from .forms import BlogsForm, EditBlogForm, CkEditBlogsForm
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner,is_customer,is_merchant_or_merchant_staff,is_partner
from users.models import GreenBillUser, UserProfileImage, Merchant_users, MerchantProfile

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Add_Module_Names(request):
    if request.method == "POST":
        user_name = request.POST['user']
        module_name = request.POST['module_name']
        obj1 = ""
        obj2 = ""
        if request.POST['module_id'] != "":
            obj1 = Add_Module_Name.objects.update_or_create(
                id=int(request.POST["module_id"]), defaults={"user_name": user_name, "module_name": module_name})
        else:
            obj2 = Add_Module_Name.objects.create(
                user_name=user_name, module_name=module_name)
        if obj1:
            sweetify.success(request, title="Success", icon='success',
                             text='Module Name updated Successfully.', timer=1500)

        elif obj2:
            sweetify.success(request, title="Success", icon='success',
                             text='Module Name created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...",
                             icon='error', text='Fail to create.', timer=1000)
    all_module = Add_Module_Name.objects.all()
    context = {
        "all_module": all_module,
        "SupportFAQNavclass": 'active',
        "SupportFAQCollapseShow": "show",
        "AddModuleNavClass": 'active'
    }
    return render(request, "supports_faq/add_module.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def delete_module(request, id):
    status = Add_Module_Name.objects.get(id=id).delete()
    if status:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Add_Video(request):
    if request.method == "POST":
        user_name = request.POST['user']
        module_name = request.POST['module_name']
        video_url = request.POST['video_url']
        video_title = request.POST['video_title']
        obj1 = ""
        obj2 = ""
        if request.POST['module_id'] != "":
            obj1 = Video_Model.objects.update_or_create(
                id=int(request.POST["module_id"]), defaults={"user_name": user_name, "module_name": module_name, "video_url": video_url,"video_title":video_title})
        else:
            obj2 = Video_Model.objects.create(
                user_name=user_name, module_name=module_name, video_url=video_url,video_title=video_title)
        if obj1:
            sweetify.success(request, title="Success", icon='success',
                             text='Video updated Successfully.', timer=1500)

        elif obj2:
            sweetify.success(request, title="Success", icon='success',
                             text='Video created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...",
                             icon='error', text='Fail to create.', timer=1000)
    all_module = Add_Module_Name.objects.all()
    all_video = Video_Model.objects.all().order_by('-id')

    for video in all_video:
        try:
            module_name_temp = Add_Module_Name.objects.get(id = video.module_name)
            module_name = module_name_temp.module_name
        except:
            module_name = ""

        video.module_name_new = module_name

    context = {
        "all_module": all_module,
        "all_video": all_video,
        "SupportFAQNavclass": 'active',
        "SupportFAQCollapseShow": "show",
        "AddVideoNavClass": 'active'
    }
    return render(request, "supports_faq/add_video.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Delete_Video(request, id):
    status = Video_Model.objects.get(id=id).delete()
    if status:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Add_FAQs(request):
    if request.method == "POST":
        user_name = request.POST['user']
        module_name = request.POST['module_name']
        question = request.POST['question']
        answer = request.POST['answer']
        obj1 = ""
        obj2 = ""
        if request.POST['module_id'] != "":
            obj1 = FAQs_Model.objects.update_or_create(id=int(request.POST["module_id"]), defaults={"user_name": user_name, "module_name": module_name, "question": question, "answer": answer})
        else:
            obj2 = FAQs_Model.objects.create(user_name=user_name, module_name=module_name, question=question, answer=answer)
        if obj1:
            sweetify.success(request, title="Success", icon='success',text='FAQs updated Successfully.', timer=1500)

        elif obj2:
            sweetify.success(request, title="Success", icon='success',text='FAQs created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...", icon='error', text='Fail to create.', timer=1000)

    all_module = Add_Module_Name.objects.all()
    all_faqs = FAQs_Model.objects.all().order_by('-id')

    for faq in all_faqs:
        try:
            module_name_temp = Add_Module_Name.objects.get(id = faq.module_name)
            module_name = module_name_temp.module_name
        except:
            module_name = ""

        faq.module_name_new = module_name

    context = {
        "all_module": all_module,
        "all_faqs": all_faqs,
        "SupportFAQNavclass": 'active',
        "SupportFAQCollapseShow": "show",
        "AddFAQsNavClass": 'active'
    }
    return render(request, "supports_faq/add_FAQs.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Delete_FAQ(request, id):
    status = FAQs_Model.objects.get(id=id).delete()
    if status:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Add_Blog(request):
    if request.method == "POST":
        user_name = request.POST['user']
        module_name = request.POST.get('module_name')
        blog = request.POST['blog']
        blog_title = request.POST['blog_title']
        obj1 = ""
        obj2 = ""
        if request.POST['module_id'] != "":
            obj1 = Blogs_Model.objects.update_or_create(
                id=int(request.POST["module_id"]), defaults={"user_name": user_name, "module_name": module_name, "blog": blog, "blog_title": blog_title})
        else:
            obj2 = Blogs_Model.objects.create(
                user_name=user_name, module_name=module_name, blog=blog, blog_title=blog_title)
        if obj1:
            sweetify.success(request, title="Success", icon='success',
                             text='Blog updated Successfully.', timer=1500)

        elif obj2:
            sweetify.success(request, title="Success", icon='success',
                             text='Blog created Successfully.', timer=1500)
        else:
            sweetify.success(request, title="Oops...",
                             icon='error', text='Fail to create.', timer=1000)
    all_module = Add_Module_Name.objects.all()
    all_blog = Blogs_Model.objects.all().order_by('-id')

    for blog in all_blog:
        try:
            module_name_temp = Add_Module_Name.objects.get(id = blog.module_name)
            module_name = module_name_temp.module_name
        except:
            module_name = ""

        blog.module_name_new = module_name

    context = {
        "all_module": all_module,
        "all_blogs": all_blog,
        "BlogsForm": BlogsForm,
        "CkEditBlogsForm": CkEditBlogsForm,
        "SupportFAQNavclass": 'active',
        "SupportFAQCollapseShow": "show",
        "AddBlogNavClass": 'active'
    }
    return render(request, "supports_faq/add_blogs.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Delete_Blog(request, id):
    status = Blogs_Model.objects.get(id=id).delete()
    if status:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def GetBlogData(request, id):
    blog = Blogs_Model.objects.get(id=id)

    data = {
        'blog_messages':blog.blog,
        'id': blog.id,
        'user_name': blog.user_name,
        'module_name': blog.module_name,
        'blog_title': blog.blog_title,
    }
    
    if blog:
        return JsonResponse({"data":data})
    else:
        return JsonResponse({"success": False})


@login_required(login_url="/merchant-login/")
@user_passes_test(is_merchant_or_merchant_staff, login_url="/merchant-login/")
def Merchant_Support_FAQ(request):

    merchant_id = Merchant_users.objects.filter(user_id=request.user).values('merchant_user_id')[0]['merchant_user_id']
    business_object = MerchantProfile.objects.get(m_user=merchant_id, m_active_account = 1)

    if business_object.m_business_category.id == 11:
        user_name = "petrol_pump"
    elif business_object.m_business_category.id == 12:
        user_name = "parking_lot"
    else:
        user_name = "other_business"

    merchant_module = Add_Module_Name.objects.filter(user_name=user_name)
    blog_details = []
    video_details = []
    faq_details = []
    for objects in merchant_module:
        objects.blog_details = []
        objects.video_details = []
        objects.faq_details = []
              
        merchant_faq = FAQs_Model.objects.filter(user_name=user_name, module_name=objects.id).order_by('-id')
        
        merchant_video = Video_Model.objects.filter(user_name=user_name, module_name=objects.id).order_by('-id')


        # for blogs in merchant_blog:
        #     if blogs in objects.blog_details:
        #         continue
        #     else:
        #         objects.blog_details.append(blogs)

        for video in merchant_video:
            if video in objects.video_details:
                continue
            else:
                # objects.video_details.append(video)
                video_details.append(video)

        for faq in merchant_faq:
            if faq in objects.faq_details:
                continue
            else:
                objects.faq_details.append(faq)
                # faq_details.append(faq)

    merchant_blog = Blogs_Model.objects.filter(user_name=user_name).order_by('-id')
    # merchant_video = Video_Model.objects.filter(user_name=user_name)
    print('merchant_faq',faq_details)
    context = {
        "merchant_blog": merchant_blog,
        "merchant_video": video_details,
        "merchant_faq": faq_details,
        "merchant_module": merchant_module,
        "merchantSupportFAQNavclass": 'active',
    }

    return render(request, "supports_faq/merchant_support_faq.html", context)

@login_required(login_url="/customer-login/")
@user_passes_test(is_customer, login_url="/customer-login/")
def Customer_Support_FAQ(request):
    customer_module = Add_Module_Name.objects.filter(user_name="customer").order_by('-id')
    faq_details = []
    video_details = []

    for module in customer_module:
        module.faq_details = []
        module.video_details = []
        customer_faq = FAQs_Model.objects.filter(user_name="customer", module_name=module.id).order_by('-id')
        customer_video = Video_Model.objects.filter(user_name="customer",module_name=module.id).order_by('-id')
  
        for faq in customer_faq:
            if faq in module.faq_details:
                continue
            else:
                module.faq_details.append(faq)


        for video in customer_video:
            if video in module.video_details:
                continue
            else:
                module.video_details.append(video)
    

    customer_blog = Blogs_Model.objects.filter(user_name="customer").order_by('-id')
    # customer_video = Video_Model.objects.filter(user_name="customer").order_by('-video_url')
 
    context = {
        "customer_faq": faq_details,
        "customer_module": customer_module,
        "customerSupportFAQNavclass": 'active',
        'customer_blog':customer_blog,
        'customer_video':video_details,
    }

    return render(request, "supports_faq/customer_support_faq.html", context)



@login_required(login_url="/partner-login/")
@user_passes_test(is_partner, login_url="/partner-login/")
def Partner_Support_FAQ(request):
    partner_module = Add_Module_Name.objects.filter(user_name="partner").order_by('-id')
    blog_details = []
    video_details = []
    faq_details = []

    for objects in partner_module:
        objects.blog_details = []
        objects.video_details = []
        objects.faq_details = []

        partner_faq = FAQs_Model.objects.filter(user_name="partner", module_name=objects.id).order_by('-id')
        partner_video = Video_Model.objects.filter(user_name="partner", module_name=objects.id).order_by('-id')

        # for blogs in partner_blog:
        #     if blogs in objects.blog_details:
        #         continue
        #     else:
        #         objects.blog_details.append(blogs)
        for video in partner_video:
            if video in objects.video_details:
                continue
            else:
                objects.video_details.append(video)


        for faq in partner_faq:
            if faq in objects.faq_details:
                continue
            else:
                objects.faq_details.append(faq)
    partner_blog = Blogs_Model.objects.filter(user_name="partner").order_by('-id')
    # partner_video = Video_Model.objects.filter(user_name="partner")

    print("***********************************************")
    print(faq_details,video_details)

    video_present=0
    faq_present=0
    if len(faq_details)==0 :
        faq_present = 0
    else:
        faq_present = 1

    if len(video_details)==0:
        video_present = 0
    else:
        video_present = 1

    print(faq_present,video_present)

    context = {
        "partner_blog": partner_blog,
        "partner_video": video_details,
        "partner_faq": faq_details,
        "partner_module": partner_module,
        "merchantSupportFAQNavclass": 'active',
        "faq_present":faq_present,
        "video_present":video_present,
    }

    return render(request, "supports_faq/partner_support_faq.html", context)


# @login_required(login_url="/partner-login/")
# @user_passes_test(is_partner, login_url="/partner-login/")
# def Partner_Support_FAQ(request):
#     partner_module = Add_Module_Name.objects.filter(user_name="partner")
#     blog_details = []
#     video_details = []
#     faq_details = []

#     for objects in partner_module:
#         objects.blog_details = []
#         objects.video_details = []
#         objects.faq_details = []
#         partner_blog = Blogs_Model.objects.filter(user_name="partner", module_name=objects.id)

#         partner_video = Video_Model.objects.filter(user_name="partner", module_name=objects.id)

#         partner_faq = FAQs_Model.objects.filter(user_name="partner", module_name=objects.id)

#         for blogs in partner_blog:
#             if blogs in objects.blog_details:
#                 continue
#             else:
#                 objects.blog_details.append(blogs)
#         for video in partner_video:
#             if video in objects.video_details:
#                 continue
#             else:
#                 objects.video_details.append(video)
#         for faq in partner_faq:
#             if faq in objects.faq_details:
#                 continue
#             else:
#                 objects.faq_details.append(faq)

#     context = {
#         "partner_blog": blog_details,
#         "partner_video": video_details,
#         "partner_faq": faq_details,
#         "partner_module": partner_module,
#         "customerSupportFAQNavclass": 'active',
#     }

#     return render(request, "supports_faq/partner_support_faq.html", context)

def All_Module_name(request, id):

    module_names = Add_Module_Name.objects.filter(user_name=id)

    list1 = []

    for module in module_names:
        list1.append({
            "id": module.id,
            "module_name": module.module_name
        })

    sorted_list = sorted(list1, key=lambda item: item.get("module_name"))

    return JsonResponse({"data": sorted_list})
