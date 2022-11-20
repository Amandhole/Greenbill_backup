from django.contrib import admin
from django.urls import path,include
from .import views 

urlpatterns = [
    path("share-web-offer/",views.share_image, name="share-web-offer"),
    path('view-web-offer-url/<str:id>/', views.web_offer_by_id, name="view-web-offer-url/"),

    
]