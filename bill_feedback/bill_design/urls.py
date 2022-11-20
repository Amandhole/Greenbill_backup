from django.urls import path
from .views import *

urlpatterns = [
    path("bill-design/", bill_design_view, name="bill-design"),
     path("authorised-sign/",auth_sign,name="authorised-sign"),
    path('sign-select/', sign_select, name="sign-select"),
    path("delete-auth-sign/<int:id>", Delete_auth_sign , name="delete-auth-sign"),
]