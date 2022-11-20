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

from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def Feedback_view(request):

    if request.method == "POST":
        status_id = request.POST.get('object_status_id')
        status = request.POST.get('status')
        feed = Feedback.objects.filter(id=int(status_id)).update(status = status)
        if feed:
            sweetify.success(request, title="Success", icon='success',
                             text='Feedback Status Updated Successfully !!!', timer=1000)
        else:
            sweetify.success(request, title="Error", icon='error',
                             text='Something Went Wrong!!!', timer=1000)

    Feedbacks = Feedback.objects.all().order_by('-id')

    total_bugs = Feedback.objects.filter(bug = True).count()
    total_suggestions = Feedback.objects.filter(suggestion = True).count()
    total_closed = Feedback.objects.filter(status = "Closed").count()
    total_open = Feedback.objects.filter(status = "Open").count()
    total_assigned = Feedback.objects.filter(status = "Assigned").count()
    
    context = {
        "FeedbackNavclass": "active",
        "Feedbacks": Feedbacks,
        "total_bugs":total_bugs,
        "total_suggestions":total_suggestions,
        "total_closed": total_closed,
        "total_open": total_open,
        "total_assigned": total_assigned,
    }

    return render(request, "super_admin/feedback/feedback.html", context)