import os
import random
import sweetify
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from django.conf import settings
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import get_connection, send_mail, BadHeaderError

from django.contrib.auth.forms import SetPasswordForm
from users.models import GreenBillUser, UserProfileImage
from authentication.models import otp_validation
from category_and_tags.models import business_category

 
import random
import json
import os
from io import BytesIO
from django.shortcuts import render
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse


import datetime

from django.utils import timezone
from datetime import datetime
from django.utils import formats
from datetime import date
import filetype
from django.db.models import Q

import random
import string

from .models import *
from suggest.models import SuggestBusiness
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner
from suggest_a_brand.models import *

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def SuggestedBrands(request):
    #SuggestedBrand = SuggestBrand.objects.all().order_by('-id')
    suggestedbrand = SuggestBrand.objects.all().order_by('-id')
    context = {
        "SuggestBrandsNavclass": "active",
        "SuggestedBrand": suggestedbrand,  
    }

    return render(request, "super_admin/suggest-a-brand/suggested-brand.html", context)


def deleteSuggestedBrand(request,id):
    SuggestBrand.objects.filter(id=id).delete()
    # print("TT",instance)
    # instance.delete()

    return JsonResponse({'status':'success'})