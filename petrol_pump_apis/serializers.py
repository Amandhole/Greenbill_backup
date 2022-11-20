from rest_framework import serializers, fields
from users.models import GreenBillUser, UserProfileImage, MerchantProfile
from category_and_tags.models import business_category
from merchant_setting.models import *
from .models import *

class merchantSerializer_register(serializers.ModelSerializer):
	class Meta:
		model = GreenBillUser
		fields = ('id', 'mobile_no', 'password', 'm_email', 'is_merchant', 'is_customer', 'first_name', 'last_name', 'm_adhaar_number', 'm_designation', 'm_dob', 'm_email', 'm_pan_number', 'is_active', 'date_joined', 'is_merchant_staff')


class merchantSerializer(serializers.ModelSerializer):
	m_dob = fields.DateField(input_formats=['%d-%m-%Y'], format='%d-%m-%Y')
	class Meta:
		model = GreenBillUser
		fields = ('id', 'mobile_no', 'password', 'm_email', 'is_merchant', 'is_customer', 'first_name', 'last_name', 'm_adhaar_number', 'm_designation', 'm_dob', 'm_email', 'm_pan_number', 'is_active', 'date_joined', 'is_merchant_staff')
        # fields = "__all__"

class BusinessCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = business_category
		fields = "__all__"

class merchantBusinessSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantProfile
		fields = ('id', 'm_business_name', 'm_address', 'm_area', 'm_city', 'm_user_id', 'm_business_logo')

class merchantPetrolPumpProductsSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantPetrolPump
		fields = "__all__"

class merchantPetrolPumpBillSerializer(serializers.ModelSerializer):
	class Meta:
		model = SavePetrolPumpBill
		fields = "__all__"

class AddonsProductListSerializer(serializers.ModelSerializer):
	class Meta:
		model = AddonPetrolPump
		fields = "__all__"

class MerchantPetrolNozzleListSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantPetrolNozzle
		fields = ('id','nozzle')

class FlagBillReasontSerializer(serializers.ModelSerializer):
	class Meta:
		model = flagbillreason
		fields = "__all__"

class ManageProductListSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantPetrolPump
		fields = ('id', 'm_business_id','product_name', 'product_cost', 'product_availability')

class AdOnProductListSerializer(serializers.ModelSerializer):
	class Meta:
		model = AddonPetrolPump
		fields = ('id', 'm_business_id','product_name', 'product_cost', 'product_availability')