# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

from django.urls import path
from .views import *

urlpatterns = [
    path('business-category/', business_category_view, name="business category"),
    path('business-category/delete/<int:id>', delete_business_category_view, name="business category delete"),
    path('business-category/<int:id>/', business_category_by_id_view, name="business category detail by id"),
    path('business-category/update/<int:id>/', business_category_update_view, name="rbusiness categoryole update"),

    path('bill-category/', bill_category_view, name="bill category"),
    path('bill-category/delete/<int:id>', delete_bill_category_view, name="bill category delete"),
    path('bill-category/<int:id>/', bill_category_by_id_view, name="bill category detail by id"),
    path('bill-category/update/<int:id>/', bill_category_update_view, name="bill category update"),

    path('bill-tags/', bill_tags_view, name="bill tags"),
    path('bill-tags/delete/<int:id>', delete_bill_tags_view, name="bill tags delete"),
    path('bill-tags/<int:id>/', bill_tags_by_id_view, name="bill tags detail by id"),
    path('bill-tags/update/<int:id>/', bill_tags_update_view, name="bill tags update"),

]