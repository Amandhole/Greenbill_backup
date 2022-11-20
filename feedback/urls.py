from django.conf.urls import url
from django.urls import path, include 
from .views import *

urlpatterns = [
    path("get-feedback/", Feedback_view, name="get-feedback"),
]