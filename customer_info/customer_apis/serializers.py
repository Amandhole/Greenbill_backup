from rest_framework import serializers, fields
from users.models import GreenBillUser
from category_and_tags.models import bill_category, bill_tags
from users.models import MerchantProfile
from merchant_software_apis.models import CustomerBill
from .models import *

class customerSerializer(serializers.ModelSerializer):
	c_dob = fields.DateField(input_formats=['%d-%m-%Y'], format='%d-%m-%Y')
	class Meta:
		model = GreenBillUser
		fields = ('id', 'mobile_no', 'password', 'email', 'is_customer', 'is_merchant','is_active', 'date_joined', 'c_area', 'c_dob', 'c_state', 'first_name', 'last_name', 'c_address_1', 'c_address_2', 'c_gender', 'c_pincode', 'c_city', 'c_unique_id')
        # fields = "__all__"

class billCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = bill_category
		fields = "__all__"

class billTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = bill_tags
		fields = "__all__"

class merchantBusinessSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantProfile
		fields = "__all__"

class customerBillListSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerBill
		fields = "__all__"

class customerQRSerializer(serializers.ModelSerializer):
	class Meta:
		model = customerQR
		fields = "__all__"


class LogSerializer(serializers.ModelSerializer):                          
   class Meta:
        model = bill_category
        fields = ('id','bill_category_name')


class PostSerializer(serializers.ModelSerializer):
    customer_bill_category = LogSerializer()
    class Meta:
        model = CustomerBill
        fields = ('id','customer_bill_category')