
from django.urls import path, include
from . import views

urlpatterns = [
    path("add-module/", views.Add_Module_Names, name="add-module"),
    path("delete-module/<int:id>", views.delete_module, name="delete-module"),
    path("add-video/", views.Add_Video, name="add-video"),
    path("delete-video/<int:id>", views.Delete_Video, name="delete-video"),
    path("add-faqs/", views.Add_FAQs, name="add-faqs"),
    path("delete-faqs/<int:id>", views.Delete_FAQ, name="delete-faqs"),
    path("add-blog/", views.Add_Blog, name="add-blog"),
    path("delete-blog/<int:id>", views.Delete_Blog, name="delete-blog"),
    path("get-all-module-name/<str:id>/",views.All_Module_name, name="get-all-module-name"),
    path("get-blog-data/<int:id>/", views.GetBlogData, name="get-blog-data"),


    # merchant supports and faqs
    path("merchant-supports-faqs/", views.Merchant_Support_FAQ,
         name="merchant-supports-faqs"),
    path("customer-supports-faqs/", views.Customer_Support_FAQ,
         name="customer-supports-faqs"),
    path("partner-supports-faqs/", views.Partner_Support_FAQ,
         name="partner-supports-faqs")
]
