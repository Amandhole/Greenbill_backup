import random
import os
import base64
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token  # To generate the token
from rest_framework import viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from users.models import GreenBillUser, UserProfileImage
from .serializers import *
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from django.utils import formats
from authentication.models import otp_validation
from django.conf import settings
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from green_points.models import GreenPointsModel
from merchant_software_apis.models import CustomerBill
from category_and_tags.models import bill_category, bill_tags
from users.models import MerchantProfile
from .models import *
from parking_lot_apis.models import ParkingLotPass, SaveParkingLotBill
from petrol_pump_apis.models import SavePetrolPumpBill

# Create your views here.


@csrf_exempt
def customerLogin(request):
    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        password = request.POST['password']

        try:

            if GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_customer')[0]['is_customer']:

                user = authenticate(mobile_no=mobile_no, password=password)

                if user:
                    is_customer = GreenBillUser.objects.filter(
                        mobile_no=mobile_no).values('is_customer')[0]['is_customer']
                    serializer = customerSerializer(user)

                    try:
                        token = Token.objects.create(user=user)
                    except:
                        token = Token.objects.get(user_id=user.id)

                    if user is not None and is_customer:
                        return JsonResponse({'status': 'success', 'token': token.key, 'data': serializer.data}, status=200)
                    else:
                        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)
                else:
                    return JsonResponse({'status': 'error', 'message': "Invalid credentials !!!"}, status=400)
            else:
                return JsonResponse({'status': 'error', 'message': "User not register !!!"}, status=400)
        except:
            return JsonResponse({'status': 'error', 'message': "User not register !!!"}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


class customerChangePassword(generics.GenericAPIView):
    serializer_class = customerSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.POST['user_id']

        user = GreenBillUser.objects.get(id=user_id)

        old_password = request.POST['old_password']

        success = GreenBillUser.check_password(user, old_password)

        if success == True:
            new_password = request.POST['new_password']

            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)  # Important!

            return JsonResponse({'status': 'success', 'message': "Password changed successfully !!!"}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed, old password not matched !!!"}, status=400)


# def base64_file(data, name=None):
#     _format, _img_str = data.split(';base64,')
#     _name, ext = _format.split('/')
#     if not name:
#         name = _name.split(":")[-1]
#     return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))

class setCustomerProfileData(generics.GenericAPIView):
    serializer_class = customerSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            user_id = request.POST['user_id']
            email = request.POST["email"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            c_gender = request.POST["c_gender"]
            c_dob = request.POST["c_dob"]
            formatted_c_dob = datetime.strptime(
                c_dob, '%d-%m-%Y').strftime('%Y-%m-%d')
            c_address_1 = request.POST["c_address_1"]
            c_address_2 = request.POST["c_address_2"]
            c_area = request.POST["c_area"]
            c_state = request.POST["c_state"]
            c_pincode = request.POST["c_pincode"]
            c_city = request.POST["c_city"]
            # c_profile_image = request.FILES["c_profile_image"]

            profile = GreenBillUser.objects.filter(id=user_id).update(email=email, first_name=first_name, last_name=last_name, c_gender=c_gender,c_dob=formatted_c_dob, c_address_1=c_address_1, c_address_2=c_address_2, c_area=c_area, c_state=c_state, c_pincode=c_pincode, c_city=c_city)

            # if c_profile_image:

            #     #random_no = random.randint(9999999, 999999999)

            #     #c_profile_image = base64_file(data=c_profile_image_temp, name="profile_image"+str(random_no))

            #     image = UserProfileImage.objects.update_or_create(user_id = request.user.id, defaults={ "c_profile_image" : c_profile_image })

            # if profile and image :
            if profile:
                return JsonResponse({'status': 'success', 'message': "Profile edited successfully !!!"}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)

        else:
            return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


class getCustomerProfileImage(generics.GenericAPIView):

    serializer_class = customerSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            user_id = request.POST['user_id']

            if user_id:
                user = GreenBillUser.objects.get(id=user_id)

                userDetails = UserProfileImage.objects.filter(user=user_id)
                base_url = "http://157.230.228.250/"

                if user:
                    if userDetails:
                        try:
                            new_dic = {
                                'mobile_no': user.mobile_no,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'c_unique_id': user.c_unique_id,
                                'profile_image': str(base_url) + str(userDetails[0].c_profile_image.url)
                            }
                        except:
                            new_dic = {
                                'mobile_no': user.mobile_no,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'c_unique_id': user.c_unique_id,
                                'profile_image': str(base_url) + str("/media/user-profile-pic.png")
                            }
                    else:

                        new_dic = {
                            'mobile_no': user.mobile_no,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'c_unique_id': user.c_unique_id,
                            'profile_image': str(base_url) + str("/media/user-profile-pic.png")
                        }
                    return JsonResponse({'status': "success", 'data': new_dic}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "User not found"}, status=400)
            else:
                return JsonResponse({'status': "error", 'message': "User id is mandatory."}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "Something went wrong."}, status=400)


class setCustomerProfileImage(generics.GenericAPIView):

    serializer_class = customerSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            user_id = request.POST['user_id']
            c_profile_image = request.FILES["c_profile_image"]

            if user_id and c_profile_image:

                #random_no = random.randint(9999999, 999999999)
                #m_profile_image = base64_file(data=m_profile_image_temp, name="profile_image"+str(random_no))

                image = UserProfileImage.objects.update_or_create(user_id=user_id, defaults={
                    "c_profile_image": c_profile_image})

                if image:
                    return JsonResponse({'status': "success", 'message': "Profile image uploaded successfully."}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "Failed to upload profile image."}, status=400)
            else:
                return JsonResponse({'status': "error", 'message': "user_id and c_profile_image are mandatory fields."}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "Something went wrong."}, status=400)


@csrf_exempt
def validateCustomerMobileNumber(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']

        try:
            is_customer = GreenBillUser.objects.filter(
                mobile_no=mobile_no).values('is_customer')[0]['is_customer']
        except:
            is_customer = ""

        if is_customer:
            return JsonResponse({'status': 'error', 'message': "Mobile number already registered."}, status=400)
        else:
            return JsonResponse({'status': 'success', 'message': "Mobile number not registered."}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': "Something went wrong."}, status=400)


@csrf_exempt
def generateOtpCustomer(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        signature = request.POST['signature']
        # email = request.POST['email']

        try:
            is_customer = GreenBillUser.objects.filter(
                mobile_no=mobile_no).values('is_customer')[0]['is_customer']
        except:
            is_customer = ""

        # if not mobile_exists:
        if is_customer:
            return JsonResponse({'status': 'error', 'message': "Mobile number exists as customer"}, status=400)
        else:
            if mobile_no:
                otp = random.randint(99999, 999999)
                otp_validation.objects.update_or_create(
                    mobile_no=mobile_no, defaults={'otp': otp})

                # subject = 'welcome to Green Bill'
                # message = f'Please use this OTP: {otp}'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [email,]
                # mail_res = send_mail( subject, message, email_from, recipient_list)

                import urllib
                username = "sanjog1"
                Password = "123456"
                sender = "HINDAG"
                temp_message = "<#> Hey Green Bill User, Please use OTP " + \
                    str(otp) + " to log in to your account." + \
                    "\n" + str(signature)
                temp_dict = {"text": temp_message}
                message = urllib.parse.urlencode(temp_dict)
                priority = 'ndnd'
                stype = 'normal'

                var = "user=" + str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(
                    mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                import requests

                url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                res = requests.get(url)

                if res.status_code == 200:
                    return JsonResponse({'status': 'success'}, status=200)
                else:
                    return JsonResponse({'status': 'error'}, status=403)
            else:
                return JsonResponse({'status': 'error'}, status=403)
        # elif mobile_exists[0].is_customer:
        #     return JsonResponse({'status':'error', 'message': "Mobile Number is registered as Customer. So please Use Customer Web Panel OR Customer App!!!"}, status=400)
        # elif mobile_exists[0].is_merchant or mobile_exists[0].is_merchant_staff:
        #     return JsonResponse({'status':'error', 'message': "Mobile Number is registered as Merchant or Merchant user. So please Use Merchant Web Panel OR Merchant App!!!"}, status=400)
        # elif mobile_exists[0].is_partner:
        #     return JsonResponse({'status':'error', 'message': "Mobile Number is registered as Partner. So please Use Partner Web Panel.!!!"}, status=400)
        # elif mobile_exists[0].is_staff:
        #     return JsonResponse({'status':'error', 'message': "Mobile Number is registered as Owner or Owner Staff. So please Use Owner Web Panel.!!!"}, status=400)
        # else:
        #     return JsonResponse({'status':'error', 'message': "Customer Exists, Please use different Mobile Number !!!"}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


@csrf_exempt
def generateOtpCustomerForgotPassword(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        signature = request.POST['signature']

        try:
            if mobile_no:
                mobile_exists = GreenBillUser.objects.get(mobile_no=mobile_no)
                is_customer = GreenBillUser.objects.filter(
                    mobile_no=mobile_no).values('is_customer')[0]['is_customer']
                email = GreenBillUser.objects.filter(
                    mobile_no=mobile_no).values('email')[0]['email']
                if mobile_exists and is_customer:
                    otp = random.randint(99999, 999999)
                    otp_validation.objects.update_or_create(
                        mobile_no=mobile_no, defaults={'otp': otp})

                    # subject = 'welcome to Green Bill'
                    # message = f'Please use this OTP: {otp}'
                    # email_from = settings.EMAIL_HOST_USER
                    # recipient_list = [email,]
                    # mail_res = send_mail( subject, message, email_from, recipient_list )
                    # print(mail_res)

                    import urllib
                    username = "sanjog1"
                    Password = "123456"
                    sender = "HINDAG"
                    temp_message = "<#> Hey Green Bill User, Please use OTP " + \
                        str(otp) + " to log in to your account." + \
                        "\n" + str(signature)
                    temp_dict = {"text": temp_message}
                    message = urllib.parse.urlencode(temp_dict)
                    priority = 'ndnd'
                    stype = 'normal'

                    var = "user=" + str(username) + "&pass=" + str(Password) + "&sender=" + str(sender) + "&phone=" + str(
                        mobile_no) + "&" + str(message) + "&priority=" + str(priority) + "&stype=" + str(stype) + ""

                    import requests

                    url = "http://trans.smsfresh.co/api/sendmsg.php?" + var

                    res = requests.get(url)

                    if res.status_code == 200:
                        return JsonResponse({'status': 'success'}, status=200)
                    else:
                        return JsonResponse({'status': 'error', 'message': "Failed to send otp !!!"}, status=400)
                else:
                    return JsonResponse({'status': 'error', 'message': 'User not registered'}, status=400)
            else:
                return JsonResponse({'status': 'error'}, status=403)
        except:
            return JsonResponse({'status': 'error', 'message': 'User not registered'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


@csrf_exempt
def otpValidateCustomer(request):
    if request.method == "POST":
        temo_otp = request.POST['otp']
        mobile_no = request.POST['mobile_no']
        otp = otp_validation.objects.filter(
            mobile_no=mobile_no).values('otp')[0]['otp']

        if otp == temo_otp:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=406)

    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


@csrf_exempt
def customerRegister(request):
    if request.method == "POST":

        mobile_no = request.POST['mobile_no']
        password = request.POST['password']

        exists = GreenBillUser.objects.filter(mobile_no=mobile_no)

        if exists:
            is_merchant = GreenBillUser.objects.filter(
                mobile_no=mobile_no).values('is_merchant')[0]['is_merchant']
        else:
            is_merchant = False

        if is_merchant == True:

            user = GreenBillUser.objects.get(mobile_no=mobile_no)

            email = request.POST['email']
            c_area = request.POST['c_area']
            c_dob = request.POST['c_dob']
            formatted_c_dob = datetime.strptime(
                c_dob, '%d-%m-%Y').strftime('%Y-%m-%d')
            c_state = request.POST["c_state"]
            c_pincode = request.POST["c_pincode"]
            c_city = request.POST['c_city']
            is_customer = 1
            is_active = 1
            unique_id = uuid.uuid4().hex[:6].upper()

            GreenBillUser.objects.filter(id=user.id).update(email=email, c_dob=formatted_c_dob, c_area=c_area, c_state=c_state,
                                                            c_pincode=c_pincode, c_city=c_city, is_customer=is_customer, is_active=is_active, c_unique_id=unique_id)

            newUser = GreenBillUser.objects.get(id=user.id)

            temp = newUser.set_password(password)
            temp2 = newUser.save()

            update_session_auth_hash(request, user)

            return JsonResponse({'status': 'success', 'message': 'User created successfully !!!'}, status=200)

        elif is_merchant == False:
            serializer = customerSerializer(data=request.POST)
            if serializer.is_valid():
                result = serializer.save()

                unique_id = uuid.uuid4().hex[:6].upper()

                user = authenticate(mobile_no=mobile_no, password=password)

                result.set_password(password)
                result.save()

                update_session_auth_hash(request, user)

                GreenBillUser.objects.filter(
                    id=result.id).update(c_unique_id=unique_id)

                return JsonResponse({'status': 'success', 'message': 'User created successfully !!!'}, status=200)

            else:
                return JsonResponse({'status': 'success', 'message': serializer.errors}, status=200)

        else:
            return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': "Something Went Wrong !!!"}, status=400)


@csrf_exempt
def forgotPasswordCustomer(request):
    if request.method == "POST":
        mobile_no = request.POST['mobile_no']
        new_password = request.POST['new_password']

        result = GreenBillUser.objects.filter(
            mobile_no=mobile_no).values('id')[0]['id']
        user = GreenBillUser.objects.get(id=result)
        success = GreenBillUser.check_password(user, new_password)
        if success == True:
            return JsonResponse({'status': 'error', 'message': 'New Password cannot be same as Old Password !!!'}, status=400)

        else:
            if result:

                user.set_password(new_password)
                user.save()

                update_session_auth_hash(request, user)  # Important!

                return JsonResponse({'status': 'success', 'message': 'Password changed successfully !!!'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'User not found !!!'}, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': 'Something went wrong, Please try again later !!!'}, status=400)


class getCustomerDetails(generics.GenericAPIView):
    serializer_class = customerSerializer
    queryset = GreenBillUser.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":

            mobile_no = request.POST['mobile_no']
            user_temp = GreenBillUser.objects.get(mobile_no=mobile_no)

            try:
                token = Token.objects.get(user_id=user_temp)
            except:
                token = ""

            if request.META['HTTP_AUTHORIZATION'] == str("Token " + token.key):

                if GreenBillUser.objects.filter(mobile_no=mobile_no).values('is_customer')[0]['is_customer']:
                    user = GreenBillUser.objects.get(mobile_no=mobile_no)
                    serializer = customerSerializer(user)

                    base_url = "http://157.230.228.250"

                    try:
                        profile_image = UserProfileImage.objects.get(
                            user_id=user.id)
                        if profile_image.c_profile_image:
                            image_url = str(
                                base_url) + str(profile_image.c_profile_image.url)
                        else:
                            image_url = str(base_url) + \
                                str("/media/user-profile-pic.png")
                    except:
                        image_url = str(base_url) + \
                            str("/media/user-profile-pic.png")

                    return JsonResponse({'status': "success", 'profile_data': serializer.data, 'image_data': image_url}, status=200)
                else:
                    return JsonResponse({'status': "error", 'message': "User not exists"}, status=400)
            else:
                return JsonResponse({'status': "error", 'message': "Token not valid !!!"}, status=400)
        else:
            return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)


@csrf_exempt
def removeCustomerProfileImage(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        result = UserProfileImage.objects.update_or_create(
            user_id=user_id, defaults={"c_profile_image": ""})

        if result:
            return JsonResponse({'status': "success", 'message': "Profile image removed successfully."}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to remove profile image"}, status=400)
    else:
        return JsonResponse({'status': "error", 'message': "Something went wrong"}, status=400)


class getCustomerGreenPoints(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        mobile_no = request.POST['user_id']

        try:
            GreenPoints = GreenPointsModel.objects.filter(mobile_no=mobile_no).values(
                'green_points_count')[0]['green_points_count']
        except:
            GreenPoints = 0

        if GreenPoints:
            return JsonResponse({'status' : "success", 'message': str(GreenPoints)}, status=200)
        else:
            return JsonResponse({'status': "success", 'message': str(GreenPoints)}, status=200)

class getShoppingAnalysisByCategory(generics.GenericAPIView):

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        queryset = CustomerBill.objects.filter(mobile_no=user_id)

        if from_date and to_date:
            labels = []
            data = []

            from_date = datetime.strptime(request.POST["from_date"], '%d-%m-%Y').strftime('%Y-%m-%d')
            to_date = datetime.strptime(request.POST["to_date"], '%d-%m-%Y').strftime('%Y-%m-%d')
            from_date_new = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_new = datetime.strptime(to_date, '%Y-%m-%d').date()
            
            for bills in queryset:
                
                if bills.bill_date >= from_date_new and bills.bill_date <= to_date_new:
                    if bills.customer_bill_category:
                        if bills.customer_bill_category.bill_category_name in labels:
                            print("available")
                        else:
                            labels.append(bills.customer_bill_category.bill_category_name)

            spend_by_bill_category = {new_list: 0 for new_list in labels}

            customer_bills = CustomerBill.objects.filter(mobile_no=user_id)

            for oject in customer_bills:
                for x in labels:
                    if oject.customer_bill_category:
                        if oject.customer_bill_category.bill_category_name == x:
                            spend_by_bill_category[x] =  spend_by_bill_category[x] + oject.bill_amount

            for object in spend_by_bill_category:
                data.append(spend_by_bill_category[object])

            
        else:
            labels = []
            data = []

            # date in yyyy/mm/dd format 
            # d1 = datetime.date(2020, 1, 3)
            # d2 = datetime.date(2021, 1, 30) 

            for bills in queryset:
                if bills.customer_bill_category:
                    if bills.customer_bill_category.bill_category_name in labels:
                        print("available")
                    else:
                        labels.append(bills.customer_bill_category.bill_category_name)

            spend_by_bill_category = {new_list: 0 for new_list in labels} 

            customer_bills = CustomerBill.objects.filter(mobile_no=user_id)

            for oject in customer_bills:
                for x in labels:
                    if oject.customer_bill_category:
                        if oject.customer_bill_category.bill_category_name == x:
                            spend_by_bill_category[x] =  spend_by_bill_category[x] + oject.bill_amount

            for object in spend_by_bill_category:
                data.append(spend_by_bill_category[object])


        # context['data'] = data
        # context['labels'] = labels

        if data and labels:
            return JsonResponse({'status': 'success', 'data': data, 'labels': labels}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)


class getShoppingAnalysisByMerchant(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        queryset = CustomerBill.objects.filter(mobile_no=user_id)

        if from_date and to_date:
            labels = []
            data = []

            from_date = datetime.strptime(request.POST["from_date"], '%d-%m-%Y').strftime('%Y-%m-%d')
            to_date = datetime.strptime(request.POST["to_date"], '%d-%m-%Y').strftime('%Y-%m-%d')
            from_date_new = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_new = datetime.strptime(to_date, '%Y-%m-%d').date()
            
            for bills in queryset:
                if bills.bill_date >= from_date_new and bills.bill_date <= to_date_new:
                    if bills.business_name:
                        if bills.business_name.m_business_name in labels:
                            print("available")
                        else:
                            labels.append(bills.business_name.m_business_name)

            spend_by_bill_business = {new_list: 0 for new_list in labels} 

            customer_bills = CustomerBill.objects.filter(mobile_no=request.user)

            for oject in customer_bills:
                for x in labels:
                    if oject.business_name:
                        if oject.business_name.m_business_name == x:
                            spend_by_bill_business[x] =  spend_by_bill_business[x] + oject.bill_amount

            for object in spend_by_bill_business:
                data.append(spend_by_bill_business[object])
                
        else:
            labels = []
            data = []

            for bills in queryset:
                if bills.business_name:
                    if bills.business_name.m_business_name in labels:
                        print("available")
                    else:
                        labels.append(bills.business_name.m_business_name)

            spend_by_bill_business = {new_list: 0 for new_list in labels} 

            customer_bills = CustomerBill.objects.filter(mobile_no=request.user)

            for oject in customer_bills:
                for x in labels:
                    if oject.business_name:
                        if oject.business_name.m_business_name == x:
                            spend_by_bill_business[x] =  spend_by_bill_business[x] + oject.bill_amount

            for object in spend_by_bill_business:
                data.append(spend_by_bill_business[object])


        if data and labels:
            return JsonResponse({'status': 'success', 'data': data, 'labels': labels}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data"}, status=400)

class getBillCategoriesList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        bill_categories = bill_category.objects.all()
        

        if bill_categories:
            serializer = billCategorySerializer(bill_categories, many=True)
            return JsonResponse({'status': "success", 'data': serializer.data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)

class getBillTagsList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        bill_tags_list = bill_tags.objects.all()
        
        if bill_tags_list:
            serializer = billTagSerializer(bill_tags_list, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)

class getMerchantBusinessList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        business_list = MerchantProfile.objects.all()

        if business_list:
            serializer = merchantBusinessSerializer(business_list, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)

class getCustomerBillList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST['user_id']

        data = []

        customer_bill_list = CustomerBill.objects.filter(mobile_no=user_id)

        customer_object = GreenBillUser.objects.get(id = user_id)

        for bill in customer_bill_list:

            try:
                business_name = bill.business_name.m_business_name
            except:
                business_name = bill.custom_business_name

            try:
                bill_category_temp = bill.customer_bill_category.bill_category_name
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
            except:
                business_logo = ""


            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": bill.bill_amount,
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": bill.customer_added,
                        'db_table': "CustomerBill",
                    })


        parking_bill_list = SaveParkingLotBill.objects.filter(mobile_no = customer_object.mobile_no)

        for bill in parking_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""


            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": bill.amount,
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": False,
                        'db_table': "SaveParkingLotBill",
                    })


        petrol_bill_list = SavePetrolPumpBill.objects.filter(mobile_no = customer_object.mobile_no)

        for bill in petrol_bill_list:

            try:
                business_name = MerchantProfile.objects.filter(id = bill.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            try:
                bill_category_temp = bill_category.objects.filter(id = bill.bill_category_id).values('bill_category_name')[0]['bill_category_name']
            except:
                bill_category_temp = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo_temp = MerchantProfile.objects.get(id = bill.m_business_id).values('m_business_logo')[0]['m_business_logo']
                business_logo = str(base_url) + str(business_logo_temp.url)

            except:
                business_logo = ""


            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category_temp,
                        "bill_amount": bill.total_amount,
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.date), '%d-%m-%Y').strftime('%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": False,
                        'db_table': "SavePetrolPumpBill",
                    })

            data.sort(key = lambda x: datetime.strptime(x['bill_date'], '%d-%m-%Y'), reverse = True)


        if customer_bill_list:
            # serializer = customerBillListSerializer(customer_bill_list, many=True)
            return JsonResponse({"status":"success","data":data}, status=200, safe=False)
            # return JsonResponse({"status":"success","data":serializer.data}, status=200)

        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data !!!"}, status=400)

class addCustomerBill(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        bill_file = request.FILES['cust_bill']
        business_id = request.POST['business_id']
        customer_bill_category = request.POST['customer_bill_category_id']
        bill_amount = request.POST['bill_amount']
        bill_date = datetime.strptime(request.POST["bill_date"], '%d-%m-%Y').strftime('%Y-%m-%d')
        bill_tags_values = request.POST['bill_tags_values']
        remarks = request.POST['remarks']
        custom_business = request.POST['custom_business']
        user_object = GreenBillUser.objects.get(id = user_id)

        # print(custom_business)

        try:
            business_object = MerchantProfile.objects.get(id = business_id)
        except:
            pass

        try:
            bill_category_object = bill_category.objects.get(id = customer_bill_category)
        except:
            pass

        if business_id and customer_bill_category:
            result = CustomerBill.objects.create(mobile_no= user_object, bill= bill_file, business_name= business_object, customer_bill_category= bill_category_object, bill_amount= bill_amount, bill_date= bill_date, customer_added = True, bill_tags = bill_tags_values, remarks = remarks, custom_business_name = custom_business)

        elif business_id:
            result = CustomerBill.objects.create(mobile_no= user_object, bill= bill_file, business_name= business_object, bill_amount= bill_amount, bill_date= bill_date, customer_added = True, bill_tags = bill_tags_values, remarks = remarks, custom_business_name = custom_business)

        elif customer_bill_category:
            result = CustomerBill.objects.create(mobile_no= user_object, bill= bill_file, customer_bill_category= bill_category_object, bill_amount= bill_amount, bill_date= bill_date, customer_added = True, bill_tags = bill_tags_values, remarks = remarks, custom_business_name = custom_business)

        else:
            result = CustomerBill.objects.create(mobile_no= user_object, bill=bill_file, bill_amount= bill_amount, bill_date= bill_date, customer_added = True, bill_tags = bill_tags_values, remarks = remarks, custom_business_name = custom_business)

        if result:
            return JsonResponse({'status' : 'success', 'message' : 'Bill added successfully !'}, status=200)
        else:
            return JsonResponse({'status' : 'error', 'message' : 'Failed to add bill !!!'}, status=400)

class editCustomerBill(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        bill_id = request.POST['id']
        business_id = request.POST['business_id']
        bill_file = request.FILES['cust_bill']
        customer_bill_category = request.POST['customer_bill_category_id']
        bill_amount = request.POST['bill_amount']
        bill_date = datetime.strptime(request.POST["bill_date"], '%d-%m-%Y').strftime('%Y-%m-%d')
        bill_tags_values = request.POST['bill_tags_values']
        remarks = request.POST['remarks']
        custom_business = request.POST['custom_business']

        db_table = request.POST['db_table']

        try:
            business_object = MerchantProfile.objects.get(id= business_id)
        except:
            pass

        try:
            bill_category_object = bill_category.objects.get(id= customer_bill_category)
        except:
            pass

        if db_table == "CustomerBill":

            if business_id and customer_bill_category:
                result = CustomerBill.objects.filter(id=bill_id).update(business_name= business_object, bill= bill_file, customer_bill_category= bill_category_object, bill_amount= bill_amount, bill_date= bill_date, bill_tags= bill_tags_values, remarks = remarks, custom_business_name = custom_business)
                bill_id_object = CustomerBill.objects.get(id=bill_id)
                bill_id_object.bill = bill_file
                bill_id_object.save()
                
            elif business_id:
                result = CustomerBill.objects.filter(id=bill_id).update(business_name= business_object, bill= bill_file, bill_amount= bill_amount, bill_date= bill_date, bill_tags= bill_tags_values, remarks = remarks, custom_business_name = custom_business)
                bill_id_object = CustomerBill.objects.get(id=bill_id)
                bill_id_object.bill = bill_file
                bill_id_object.save()

            elif customer_bill_category:
                result = CustomerBill.objects.filter(id=bill_id).update(customer_bill_category= bill_category_object, bill= bill_file, bill_amount= bill_amount, bill_date= bill_date, bill_tags= bill_tags_values, remarks = remarks, custom_business_name = custom_business)
                bill_id_object = CustomerBill.objects.get(id=bill_id)
                bill_id_object.bill = bill_file
                bill_id_object.save()
                
            else:
                result = CustomerBill.objects.filter(id=bill_id).update(bill_amount= bill_amount, bill_date= bill_date, bill_tags= bill_tags_values, remarks= remarks, custom_business_name= custom_business)
                bill_id_object = CustomerBill.objects.get(id=bill_id)
                bill_id_object.bill = bill_file
                bill_id_object.save()

        elif db_table == "SaveParkingLotBill":
            result = SaveParkingLotBill.objects.filter(id=bill_id).update(bill_category_id=customer_bill_category, bill_tags = bill_tags_values, remarks = remarks)

        elif db_table == "SavePetrolPumpBill":
            result = SavePetrolPumpBill.objects.filter(id=bill_id).update(bill_category_id=customer_bill_category, bill_tags = bill_tags_values, remarks = remarks)

        if result:
            return JsonResponse({'status' : 'success', 'message' : 'Bill edited successfully !'}, status=200)
        else:
            return JsonResponse({'status' : 'error', 'message' : 'Failed to edit bill !!!'}, status=400)

class deleteCustomerBill(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        bill_id = request.POST['id']

        db_table = request.POST['db_table']

        if db_table == "CustomerBill":
            result = CustomerBill.objects.filter(id = bill_id).delete()

        elif db_table == "SaveParkingLotBill":
            result = SaveParkingLotBill.objects.filter(id = bill_id).delete()

        elif db_table == "SavePetrolPumpBill":
            result = SavePetrolPumpBill.objects.filter(id = bill_id).delete()

        if result:
            return JsonResponse({'status' : 'success', 'message' : 'Bill deleted successfully !'}, status=200)
        else:
            return JsonResponse({'status' : 'error', 'message' : 'Failed to delete bill !!!'}, status=400)

class downloadCustomerBill(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        bill_id = request.POST['id']

        result = CustomerBill.objects.filter(id = bill_id)

        if result:
            base_url = "http://157.230.228.250"
            
            if result[0].bill:
                file = str(base_url) + str(result[0].bill.url)

            return JsonResponse({'status': 'success', 'message': file }, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)

class getBillByMerchantStore(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        business_id = request.POST['business_id']

        user_id = request.POST['user_id']

        customer_object = GreenBillUser.objects.get(id=user_id)
        
        customer_bill_list = CustomerBill.objects.filter(business_name = business_id, mobile_no=customer_object)

        data = []

        for bill in customer_bill_list:

            try:
                business_name = bill.business_name.m_business_name
            except:
                business_name = ""

            try:
                bill_category = bill.customer_bill_category.bill_category_name
            except:
                bill_category = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
            except:
                business_logo = ""


            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category,
                        "bill_amount": bill.bill_amount,
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": bill.customer_added,
                    })

        if customer_bill_list:
            # serializer = customerBillListSerializer(customer_bill_list, many=True)
            return JsonResponse({'status': 'success', 'data': data }, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)


class getBillByBillCategory(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        bill_category_id = request.POST['bill_category_id']
        user_id = request.POST['user_id']

        customer_object = GreenBillUser.objects.get(id=user_id)
        
        customer_bill_list = CustomerBill.objects.filter(customer_bill_category = bill_category_id, mobile_no=customer_object)

        data = []

        for bill in customer_bill_list:

            try:
                business_name = bill.business_name.m_business_name
            except:
                business_name = ""

            try:
                bill_category = bill.customer_bill_category.bill_category_name
            except:
                bill_category = ""

            base_url = "http://157.230.228.250/"

            try:
                business_logo = str(base_url) + str(bill.business_name.m_business_logo.url)
            except:
                business_logo = ""


            data.append({
                        "id": bill.id,
                        "business_name": business_name,
                        "bill_category_name": bill_category,
                        "bill_amount": bill.bill_amount,
                        "comments": bill.remarks,
                        "bill_date": datetime.strptime(str(bill.bill_date), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        "business_logo": business_logo,
                        "customer_added": bill.customer_added,
                    })

        if customer_bill_list:
            # serializer = customerBillListSerializer(customer_bill_list, many=True)
            return JsonResponse({'status': 'success', 'data': data }, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': "Failed to retrieve data !!!"}, status=400)


# QR CODE GENERATION 
class generateQRCustomer(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']
        mobile_no = request.POST['mobile_no']
        vehicle_no = request.POST['vehicle_no']
        vehicle_type = request.POST['vehicle_type']
        description = request.POST['description']
        
        result = customerQR.objects.create(user_id= user_id, mobile_no= mobile_no, vehicle_no= vehicle_no, vehicle_type= vehicle_type, description= description)

        if result:
            return JsonResponse({'status': "success", 'message': "Data added successfully !"}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to store data !!!"}, status=400)

class listQRCustomer(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.POST['user_id']

        result = customerQR.objects.filter(user_id= user_id)
        
        if result:
            serializer = customerQRSerializer(result, many=True)
            return JsonResponse({'status': "success", 'data': serializer.data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "No Data Found !!!"}, status=400)

class editQRCustomer(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        id = request.POST['id']

        mobile_no = request.POST['mobile_no']
        vehicle_no = request.POST['vehicle_no']
        vehicle_type = request.POST['vehicle_type']
        description = request.POST['description']


        result = customerQR.objects.filter(id= id).update(mobile_no= mobile_no, vehicle_no= vehicle_no, vehicle_type= vehicle_type, description= description)

        if result:
            return JsonResponse({'status': "success", 'message': "Data updated successfully !"}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to update data !!!"}, status=400)

# QR CODE GENERATION END

class parkingPassList(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        mobile_no = request.POST['mobile_no']

        result = ParkingLotPass.objects.filter(mobile_no = mobile_no)

        data = []

        for parkingPass in result:

            try:
                business_name = MerchantProfile.objects.filter(id = parkingPass.m_business_id).values('m_business_name')[0]['m_business_name']
            except:
                business_name = ""

            base_url = "http://157.230.228.250/"

            try:
                m_business = MerchantProfile.objects.filter(id = parkingPass.m_business_id)
                
                if m_business[0].m_business_logo:
                    business_logo = str(base_url) + str(m_business[0].m_business_logo.url)
                else:
                    business_logo = ""
            except:
                business_logo = ""

            data.append({
                        "id": parkingPass.id,
                        "business_name": business_name,
                        "business_logo": business_logo,
                        "mobile_no": parkingPass.mobile_no,
                        "amount": parkingPass.amount,
                        "vehical_no": parkingPass.vehical_no,
                        "valid_from": datetime.strptime(str(parkingPass.valid_from,), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        "valid_to": datetime.strptime(str(parkingPass.valid_to), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        "comments": parkingPass.comments,
                    })

        if result:
            return JsonResponse({'status': "success", 'data': data}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Data not available !!!"}, status=400)


class getBillByBillId(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        bill_id = request.POST['bill_id']

        db_table = request.POST['db_table']

        if db_table == "CustomerBill":
            result = CustomerBill.objects.filter(id=bill_id)

        elif db_table == "SaveParkingLotBill":
            result = SaveParkingLotBill.objects.filter(id=bill_id)

        elif db_table == "SavePetrolPumpBill":
            result = SavePetrolPumpBill.objects.filter(id=bill_id)

        base_url = "http://157.230.228.250/"

        bill_tags_name1 = []

        try:

            if result[0].bill_tags:
                bill_tags_list = list(result[0].bill_tags.split(","))
                for bill_tags1 in bill_tags_list:
                    bill_tags_name_temp = bill_tags.objects.filter(id = int(bill_tags1)).values('bill_tags_name')[0]['bill_tags_name']
                    bill_tags_name1.append(bill_tags_name_temp)

            bill_tags_name2 = ', '.join(map(str, bill_tags_name1))

            bill_tags_id = result[0].bill_tags

        except:
            bill_tags_name2 = ""

        try:
            if db_table == "CustomerBill":
                business = MerchantProfile.objects.filter(id = result[0].business_name.id)
            else:
                business = MerchantProfile.objects.filter(id = result[0].m_business_id)

            business_id = business[0].id
            business_name = business[0].m_business_name
        except:
            business_id = ""
            business_name = ""

        try:
            if db_table == "CustomerBill":
                bill_category_temp = bill_category.objects.filter(id = result[0].customer_bill_category.id)
            else:
                bill_category_temp = bill_category.objects.filter(id = result[0].bill_category_id)

            customer_bill_category_id = bill_category_temp[0].id
            bill_category_name = bill_category_temp[0].bill_category_name

        except:
            customer_bill_category_id = ""
            bill_category_name = ""


        if db_table == "CustomerBill":
            amount = result[0].bill_amount

            bill_file_temp = str(base_url) + str(result[0].bill.url)

            try:
                bill_file_temp = str(base_url) + str(result[0].bill.url)
            except:
                bill_file_temp = ""

            bill_date = datetime.strptime(str(result[0].bill_date), '%Y-%m-%d').strftime('%d-%m-%Y')
            customer_added_temp = result[0].customer_added
            custom_business_name_temp = result[0].custom_business_name

        elif db_table == "SaveParkingLotBill":
            amount = result[0].amount

            try:
                bill_file_temp = str(base_url) + str(result[0].bill_file.url)
            except:
                bill_file_temp = ""

            bill_date = datetime.strptime(str(result[0].date), '%d-%m-%Y').strftime('%d-%m-%Y')
            customer_added_temp = False
            custom_business_name_temp = ""

        elif db_table == "SavePetrolPumpBill":
            amount = result[0].total_amount

            try:
                bill_file_temp = str(base_url) + str(result[0].bill_file.url)
            except:
                bill_file_temp = ""

            bill_date = datetime.strptime(str(result[0].date), '%d-%m-%Y').strftime('%d-%m-%Y')
            customer_added_temp = False
            custom_business_name_temp = ""

        # try:
        #     business_id = result[0].business_name.id
        #     business_name =  result[0].business_name.m_business_name

        # except:
        #     business_id = ""
        #     business_name = ""

        # try:
        #     customer_bill_category_id = result[0].customer_bill_category.id
        #     bill_category_name =  result[0].customer_bill_category.bill_category_name

        # except:
        #     customer_bill_category_id = ""
        #     bill_category_name = ""
        
        context = {
            "bill_id":result[0].id,
            "bill": bill_file_temp,
            "bill_amount": str(amount),
            "bill_date": bill_date,
            "customer_added": customer_added_temp,
            "bill_tags_id": bill_tags_id,
            "bill_tags_name": bill_tags_name2,
            "remarks": result[0].remarks,
            "custom_business_name": custom_business_name_temp,
            "business_name": business_name,
            "business_id": str(business_id),
            "customer_bill_category_id" : customer_bill_category_id,
            "customer_bill_category_name": bill_category_name,
        }

        if result:
            # serializer = customerBillListSerializer(result, many=True)
            return JsonResponse({'status': "success","data":context}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)

class getBillCategoriesListByCustomerId(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST["user_id"]

        user_object = GreenBillUser.objects.get(id = user_id)
        bill_categories = bill_category.objects.all()

        allocated_bill_categories = []

        for category in bill_categories:
            customer_bill_count = CustomerBill.objects.filter(mobile_no = user_object, customer_bill_category = category).count()
            if customer_bill_count > 0:
                if category in allocated_bill_categories:
                    continue
                else:
                    allocated_bill_categories.append({
                        "id": category.id,
                        "bill_category_name": category.bill_category_name,
                        "bill_category_description": category.bill_category_description,
                        "bill_count": customer_bill_count
                    })
                    # allocated_bill_categories.append(category)

            parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = user_object.mobile_no).count()
            if parking_bill_count > 0:
                if category in allocated_bill_categories:
                    continue
                elif category.id == 27:
                    allocated_bill_categories.append({
                        "id": category.id,
                        "bill_category_name": category.bill_category_name,
                        "bill_category_description": category.bill_category_description,
                        "bill_count": parking_bill_count
                    })
                    # allocated_bill_categories.append(category)

            petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = user_object.mobile_no).count()
            if petrol_bill_count > 0:
                if category in allocated_bill_categories:
                    continue
                elif category.id == 26:
                    allocated_bill_categories.append({
                        "id": category.id,
                        "bill_category_name": category.bill_category_name,
                        "bill_category_description": category.bill_category_description,
                        "bill_count": petrol_bill_count
                    })
                    # allocated_bill_categories.append(category)

        # print(allocated_bill_categories)
        
        if bill_categories:
            serializer = billCategorySerializer(allocated_bill_categories, many=True)
            return JsonResponse({'status': "success", 'data': allocated_bill_categories}, status=200)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)

class getMerchantBusinessListByCustomerId(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.POST["user_id"]

        user_object = GreenBillUser.objects.get(id = user_id)
        
        business_list = MerchantProfile.objects.all()

        allocated_business_list = []

        base_url = "http://157.230.228.250/"

        for business in business_list:
            customer_bill_count = CustomerBill.objects.filter(mobile_no = user_object, business_name = business).count()
            if customer_bill_count > 0:
                if business in allocated_business_list:
                    continue
                else:
                    if business.m_business_logo:
                        m_business_logo = str(base_url) + str(business.m_business_logo.url)
                    else:
                        m_business_logo = ""

                    allocated_business_list.append({
                        "id": business.id,
                        "m_business_name": business.m_business_name,
                        "m_business_logo": m_business_logo,
                        "bill_count": customer_bill_count
                    })

                    # allocated_business_list.append(business)

            parking_bill_count = SaveParkingLotBill.objects.filter(mobile_no = user_object.mobile_no, m_business_id = business.id).count()
            if parking_bill_count > 0:
                if business in allocated_business_list:
                    continue
                else:
                    if business.m_business_logo:
                        m_business_logo = str(base_url) + str(business.m_business_logo.url)
                    else:
                        m_business_logo = ""

                    allocated_business_list.append({
                        "id": business.id,
                        "m_business_name": business.m_business_name,
                        "m_business_logo": m_business_logo,
                        "bill_count": parking_bill_count
                    })
                    # allocated_business_list.append(business)

            petrol_bill_count = SavePetrolPumpBill.objects.filter(mobile_no = user_object.mobile_no, m_business_id = business.id).count()
            if petrol_bill_count > 0:
                if business in allocated_business_list:
                    continue
                else:
                    if business.m_business_logo:
                        m_business_logo = str(base_url) + str(business.m_business_logo.url)
                    else:
                        m_business_logo = ""

                    allocated_business_list.append({
                        "id": business.id,
                        "m_business_name": business.m_business_name,
                        "m_business_logo": m_business_logo,
                        "bill_count": petrol_bill_count
                    })
                    # allocated_business_list.append(business)

            # print(allocated_business_list)

        if business_list:
            serializer = merchantBusinessSerializer(allocated_business_list, many=True)
            return JsonResponse(allocated_business_list, status=200, safe=False)
        else:
            return JsonResponse({'status': "error", 'message': "Failed to retrieve the data"}, status=400)
