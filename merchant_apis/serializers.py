from rest_framework import serializers, fields
from users.models import GreenBillUser, UserProfileImage, MerchantProfile
from category_and_tags.models import business_category
from merchant_role.models import *
from suggest.models import *
from supports_faq.models import *
from coupon.models import *
from offers.models import *
from merchant_payment.models import *
from my_subscription.models import *

from subscription_plan.models import *

from merchant_software_apis.models import *

from bill_design.models import *

class merchantSerializer_register(serializers.ModelSerializer):
	class Meta:
		model = GreenBillUser
		fields = ('id', 'mobile_no', 'password', 'm_email', 'is_merchant', 'is_customer', 'first_name', 'last_name', 'm_adhaar_number', 'm_designation', 'm_dob', 'm_email', 'm_pan_number', 'is_active', 'date_joined', 'is_merchant_staff')


class merchantSerializer(serializers.ModelSerializer):
	# m_dob = fields.DateField(input_formats=['%d-%m-%Y'], format='%d-%m-%Y')
	class Meta:
		model = GreenBillUser
		fields = ('id', 'mobile_no', 'password', 'm_email', 'is_merchant', 'is_customer', 'first_name', 'last_name', 'm_adhaar_number', 'm_designation', 'm_dob', 'm_email', 'm_pan_number', 'is_active', 'date_joined', 'is_merchant_staff')

class BusinessCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = business_category
		fields = "__all__"

class merchantBusinessSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantProfile
		fields = ('id', 'm_business_name', 'm_address', 'm_area', 'm_city', 'm_user_id', 'm_business_logo', 'm_business_category')


class MerchantUserRoleSerializer(serializers.ModelSerializer):
	class Meta:
		model = merchant_role
		fields = "__all__"

class SuggestBusinessSerializer(serializers.ModelSerializer):
	class Meta:
		model = SuggestBusiness
		fields = ('id', 'm_business_id', 'user_id', 'suggested_business_name', 'contact_no', 'address')

class MerchantFaqsSerializer(serializers.ModelSerializer):
	class Meta:
		model = FAQs_Model
		fields = "__all__"

class MerchantCouponListSerializer(serializers.ModelSerializer):
	class Meta:
		model = CouponModel
		fields = "__all__"

class MerchantOffersListSerializer(serializers.ModelSerializer):
	class Meta:
		model = OfferModel
		fields = "__all__"

class PaymentLinkListSerializer(serializers.ModelSerializer):
	class Meta:
		model = PaymentLinks
		fields = "__all__"

class RechargeHistorySerializer(serializers.ModelSerializer):
	class Meta:
		model = recharge_history
		fields = "__all__"

class SubscriptionPlanSerializer(serializers.ModelSerializer):
	class Meta:
		model = subscription_plan_details
		fields = "__all__"


class PromotionalSMSSubscriptionPlanSerializer(serializers.ModelSerializer):
	class Meta:
		model = promotional_subscription_plan_model
		fields = "__all__"

class TransactionalSMSSubscriptionPlanSerializer(serializers.ModelSerializer):
	class Meta:
		model = transactional_subscription_plan_model
		fields = "__all__"


class AddOnRechargePlanSerializer(serializers.ModelSerializer):
	class Meta:
		model = add_on_plan_model
		fields = "__all__"

class PaymentHistorySerializer(serializers.ModelSerializer):
	class Meta:
		model = recharge_history
		fields = "__all__"

class BillRatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerBill
		fields = "__all__"


class MerchantBillPaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = MerchantBill
		fields = "__all__"

class MerchantContactCardSerializer(serializers.ModelSerializer):
	class Meta:
		model = contact_card
		fields = "__all__"


