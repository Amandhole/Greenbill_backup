from django.conf.urls import url
from django.urls import path, include 
from .views import *

urlpatterns = [
    path("suggested-brands/", SuggestedBrands, name="suggested-brands"),
    path("delete-suggested-brand/<int:id>",deleteSuggestedBrand, name="delete-suggested-brand"),
]