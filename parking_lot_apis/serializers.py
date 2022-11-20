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

class parkingLotVehicleTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantParkingAddVehicle
		fields = "__all__"

class parkingLotSpaceSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantParkingLotSpace
		fields = "__all__"

class parkingLotSpaceChargesSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantParkingSpaceCharges
		fields = "__all__"

class parkingLotBillSerializer(serializers.ModelSerializer):
	class Meta:
		model = SaveParkingLotBill
		fields = "__all__"

class parkingpasschargesSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantParkingLotPassCharges
		fields = "__all__"

class parkingpasscompaniesSerializer(serializers.ModelSerializer):
	class Meta:
		model = CompniesName
		fields = "__all__"

class ManageVehicleTypeListSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantParkingAddVehicle
		fields = ('id','vehicle_type')

class ManageChargesListSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantParkingSpaceCharges
		fields = "__all__"
		