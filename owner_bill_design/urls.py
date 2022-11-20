from django.urls import path
from .views import *


urlpatterns = [
    path("owner-bill-design/", owner_bill_design_view, name="owner-bill-design")
]



