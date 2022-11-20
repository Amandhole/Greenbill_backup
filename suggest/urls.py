from django.urls import path, re_path, include
from .views import *

urlpatterns = [
    path("suggest-petrol-pump/", suggestPetrolPump, name="suggest-petrol-pump"),
    path("suggest-parking/", suggestParking, name="suggest-parking"),
    path("suggested-business-list/", suggestBusinessList, name="suggested-business-list"),
    path("suggest-new-business/", suggestNewBusiness, name="suggest-new-business"),
]