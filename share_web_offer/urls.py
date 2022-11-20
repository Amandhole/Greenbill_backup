from django.contrib import admin
from django.urls import path,include
from .import views 

urlpatterns = [
    path("share-web-offer/",views.share_image, name="share-web-offer"),
    path('view-web-offer-url/<str:id>/', views.web_offer_by_id, name="view-web-offer-url/"),
    path('delete-web-offer/<int:id>', views.Delete_web_offer, name="delete-web-offer"),
    # path('Promotions/Web-Offer/<str:id>/', views.web_offer_by_id, name="view-web-offer-url/"),
    path("set-web-offer/", views.set_active_web_offer, name="set-web-offer"),
    
]