from django.urls import path
from .views import *
from core import settings

urlpatterns = [
    path("shopping-analysis-category/", customer_shopping_analysis_by_category, name="shopping-analysis-category"),
    path("shopping-analysis-merchant/", customer_shopping_analysis_by_merchant, name="shopping-analysis-merchant"),
]