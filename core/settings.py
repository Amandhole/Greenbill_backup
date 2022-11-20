# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020- present Hind Softwares
"""

import os
from unipath import Path
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = Path(__file__).parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'S#perS3crEt_1122'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# load production server from .env
ALLOWED_HOSTS = ['134.122.113.139']
# ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'authentication',
    'app',  # Enable the inner app
    'role',
    'sweetify',
    'dashboard_user',
    'software_partner_user',
    'category_and_tags',
    'crispy_forms',  # Enable Crispy  Forms
    'merchant_setting',  # merchant settings app
    'merchant_role',  # merchant role permission
    'partner_setting',  # partner setting app
    'super_admin_settings',  # super admin setting app
    'ckeditor',  # ckeditor
    'ckeditor_uploader',
    'rest_framework',  # Rest API
    'rest_framework.authtoken',  # REST APIS AUTH TOKEN
    'customer_apis',
    'merchant_apis',
    'merchant_info',
    'partner_info',
    'merchant_software_apis',
    'dbbackup',  # django-dbbackup
    'petrol_pump_apis',
    'customer_bill',
    'merchant_enquiry',
    'shopping_analysis',
    'green_points',
    'customer_info',
    'parking_lot_apis',
    'subscription_plan',
    'my_subscription',
    'merchant_notice',
    'owner_notice_board',
    'customer_search',
    'coupon',
    'customer_coupon',
    'cash_memo_receipts',
    'offers',
    'merchant_cash_memo',
    'bill_info',
    'promotions',
    'supports_faq',
    'system_update',
    'bill_design',
    'merchant_cashmemo_design',
    'user_visit',
    'userlog',
    'suggest',
    'payments',
    'qr_code',
    'share_a_word',
    'suggest_a_brand',
    'feedback',
    'owner_customer_info',
    'partner_merchant_info',
    'offer_cusavailable',
    'offers_status',
    'merchant_stamp',
    'owner_stamp',
    'merchant_payment',
    'partner_my_subscription',
    'partner_payment',
    'merchant_promotion',
    'owner_bill_info',
    'owner_coupon',
    'referral_points',
    'share_web_offer',
    'bill_feedback',
    'django_crontab',
    'manual_subscription',
    'owner_bill_design',
    'django_truncate',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user_visit.middleware.UserVisitMiddleware',
]




ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"   # Route defined in app/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in app/urls.py
TEMPLATE_DIR = os.path.join(BASE_DIR, "core/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.module_permissions',
                'app.context_processors.super_admin',
                'app.context_processors.userProfilePic',
                'app.context_processors.ChangeMerchnatBusinessForm_context',
                'app.context_processors.merchant_admin',
                'app.context_processors.merchant_user_module_permissions',
                'app.context_processors.getMerchnatBusinesscategory_context',
                'app.context_processors.get_unread_merchant_inquiry_count',
                'app.context_processors.display_notification_merchant_notice',
                'app.context_processors.display_notification_owner_notice',
                'app.context_processors.getUserRole',
                'app.context_processors.get_unread_merchant_cashMemoDesign_count',
                'app.context_processors.show_search_suggestions',
                'app.context_processors.partner_category',
                #'app.context_processors.get_unread_system_update_count',
                'app.context_processors.get_unread_system_update_count_partner',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# DATABASES = {
# 'default': {
#    'ENGINE': 'django.db.backends.mysql',
#    'NAME': 'green_bill_27_11_20',
#    'HOST': '127.0.0.1',
#    'PORT': '3306',
#    'USER': 'root',
#   'PASSWORD': '',
# 'OPTIONS': {
#         'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         'charset': 'utf8mb4',
#     }
# }}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'core/static'),
)
#############################################################
#############################################################

SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'


# Email Configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.greenbill.in'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "support@greenbill.in"
EMAIL_HOST_PASSWORD = "SupportGB@2510"

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = "zappkodesolutions@gmail.com"
# EMAIL_HOST_PASSWORD = "ZSrashmi@12345"

AUTH_USER_MODEL = 'users.GreenBillUser'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {"location": os.path.join(MEDIA_ROOT, "backup/")}


CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_RESTRICT_BY_USER = True

CKEDITOR_CONFIGS = {
    'default': {
        'width': 'auto',
    },
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated'
    ),

}

DATA_UPLOAD_MAX_MEMORY_SIZE = 200000


REST_FRAMEWORK = {
    "DATE_INPUT_FORMATS": ["%d-%m-%Y"],
}

API_KEY = "AAAAT0x_FXs:APA91bEqvJatQkrynFXV252aQgPF7W_1V1oNoUwLAEcTww2pwOTwwdxCyurFQ5-YKYpBJbf-PaFhiRU82H-gy7kXg37jbKXOLVnz0g2pgxQWdbET1w20BnLfHfgAAPpNm78r7BOMb05A"

# X_FRAME_OPTIONS = 'SAMEORIGIN'

X_FRAME_OPTIONS = 'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']


# Cron Jobs
# CRONJOBS = [
#     ('1 10 * * *', 'app.cron.subscription_expiration_cron_job_notification'),
#     ('1 10 * * *', 'app.cron.subscription_expired_cron_job_notification')
# ]
