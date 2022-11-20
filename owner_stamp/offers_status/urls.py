from django.contrib import admin
from django.urls import path,include
from .import views 

urlpatterns = [
    path("offer-status/",views.Owner_offers, name="offer-status"),
    path("owner-offer/",views.owner_offers, name="owner-offer"),
    path("approve-offer-by-id/<int:id>", views.approve_offer_by_id, name="approve-offer-by-id"),
    path("disapprove-offer-by-id/", views.disapprove_offer_by_id, name="disapprove-offer-by-id"),
    path("Delete-owner-Offer/<int:id>",views.Delete_owner_Offer, name="Delete-owner-Offer"),
    path("add-offer-amount-by-id/", views.add_offer_Amount_by_id, name="add-offer-amount-by-id"),
    
]