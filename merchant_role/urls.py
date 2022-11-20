from django.urls import path
from .views import *
urlpatterns = [
    path('merchant-role/', merchant_role_detail_view, name="merchant role"),
    path('merchant-role/create/', merchant_create_role_view, name="merchant role create"),
    path('merchant-role/delete/<int:id>', merchant_delete_role_view, name="merchant role delete"),
    path('merchant-role/<int:id>/', merchant_role_detail_by_id_view, name="merchant role detail by id"),
    path('merchant-role/update/<int:id>/', merchant_role_update_view, name="merchant role update"),
    path('merchant-role/permission/<int:id>/', merchant_permission_view, name="merchant permission update"),
    path('merchant-role/permission/update/', merchant_permission_update_view, name="merchant permission update"),
    path('merchant-role/assign/', merchant_assign_role_details_view, name="merchant assign role details view"),
    path('merchant-role/assign/add/', merchant_assign_role_view, name="merchant assign role view"),
    # path('role/assign/get/', assign_role_view_details_by_id, name="assign role view details by id"),
]