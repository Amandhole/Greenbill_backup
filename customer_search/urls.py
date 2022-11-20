from django.urls import path
from customer_search import views

urlpatterns = [

    path("search-by-customer/", views.Search_By_Customer,
         name="search-by-customer"),
    
    
]
