from django.urls import path
from .views import *

urlpatterns = [
    path("bill-design/", bill_design_view, name="bill-design"),
    path("authorised-sign/",auth_sign,name="authorised-sign"),
    path('sign-select/', sign_select, name="sign-select"),
    path("delete-auth-sign/<int:id>", Delete_auth_sign , name="delete-auth-sign"),
    path("api-for-pdf/",padfchecker ,name = "api-for-pdf"),
    path("card-design/", card_design_view, name="card-design"),
    path("card-design-view/<int:id>",card_design_preview,name="card-design-preview"),

    path("feedback-card/" , feedback ,name = "feedback-card"),
    path("card-analysis/" , analysis ,name = "card-analysis")
]