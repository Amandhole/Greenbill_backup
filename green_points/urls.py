from django.urls import path
from .views import *
from core import settings

urlpatterns = [
	path("green-points/", get_green_points, name="green-points"),
]