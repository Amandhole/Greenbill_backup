from django.conf.urls import url
from django.urls import path, include 
from .views import *

urlpatterns = [
    path("shared-words/", ShareWord_view, name="shared-words"),
]