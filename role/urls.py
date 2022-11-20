from django.urls import path
from .views import role_detail_view, role_detail_by_id_view, create_role_view, delete_role_view, role_update_view, permission_view, permission_update_view, assign_role_details_view, assign_role_view

urlpatterns = [
    path('role/', role_detail_view, name="role"),
    path('role/create/', create_role_view, name="role create"),
    path('role/delete/<int:id>', delete_role_view, name="role delete"),
    path('role/<int:id>/', role_detail_by_id_view, name="role detail by id"),
    path('role/update/<int:id>/', role_update_view, name="role update"),
    path('role/permission/<int:id>/', permission_view, name="permission update"),
    path('role/permission/update/', permission_update_view, name="permission update"),
    path('role/assign/', assign_role_details_view, name="assign role details view"),
    path('role/assign/add/', assign_role_view, name="assign role view"),
    # path('role/assign/get/', assign_role_view_details_by_id, name="assign role view details by id"),
]