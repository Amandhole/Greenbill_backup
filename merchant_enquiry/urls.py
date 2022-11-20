from django.urls import path

from merchant_enquiry import views

urlpatterns = [

    path("merchant-enquiry/", views.Merchant_Enquiry, name="merchant-enquiry"),

    path("get-all-merchant-enquiry/", views.Get_Merchant_Enquiry_Details, name="get-all-merchant-enquiry"),

    path("delete-dm-enquiry/<int:id>", views.Delete_DM_Enquiry, name="delete-dm-enquiry"),

    path("owner-delete-dm-enquiry/<int:id>",views.Owner_Delete_Inquiry,name="owner-delete-dm-enquiry"),

    path("delete-multiple-enquiry/", views.Delete_Meltiple_Inquiry, name="delete-multiple-enquiry"),

    path("assign-company-for-merchant-enquiry/", views.assign_company_for_merchant_enq, name="assign-company-for-merchant-enquiry"),
]
