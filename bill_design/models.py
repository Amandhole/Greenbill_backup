from inspect import trace
from statistics import mode
from django.db import models
from users.models import GreenBillUser, MerchantProfile
from django.utils import timezone

# Create your models here.
class bill_designs(models.Model):
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    logo = models.CharField(max_length=200, default='')
    address = models.CharField(max_length=200, default='')
    rating = models.BooleanField(default=False)
    rating_text = models.CharField(max_length=200, default='')
    rating_emoji = models.CharField(max_length=200, default='')
    facebook = models.BooleanField(default=False)
    facebook_url = models.CharField(max_length=1000, default='')
    youtube = models.BooleanField(default=False)
    youtube_url = models.CharField(max_length=1000, default='')
    twitter = models.BooleanField(default=False)
    twitter_url = models.CharField(max_length=1000, default='')
    instagram = models.BooleanField(default=False)
    instagram_url = models.CharField(max_length=1000, default='')
    ads_below_bill = models.BooleanField(default=False)
    phone = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=100, default='')
    website = models.BooleanField(default=False)
    website_url = models.CharField(max_length=1000, default='')
    map = models.BooleanField(default=False)
    map_link = models.CharField(max_length=1000, default='')
    terms_conditions = models.BooleanField(default=False)
    terms_url = models.CharField(max_length=1000, default='')
    footer_logo = models.BooleanField(default=False)
    linkedin = models.BooleanField(default=False)
    linkedin_url = models.CharField(max_length=1000, default='')
    skype = models.BooleanField(default=False)
    skype_url = models.CharField(max_length=1000, default='')
    google = models.BooleanField(default=False)
    google_url = models.CharField(max_length=1000, default='')
    pinterest = models.BooleanField(default=False)
    pinterest_url = models.CharField(max_length=1000, default='')
    snapchat = models.BooleanField(default=False)
    snapchat_url = models.CharField(max_length=1000, default='')
    android = models.BooleanField(default=False)
    android_url = models.CharField(max_length=1000, default='')
    apple = models.BooleanField(default=False)
    apple_url = models.CharField(max_length=1000, default='')
    zomato = models.BooleanField(default=False)
    zomato_url = models.CharField(max_length=1000, default='')
    swiggy = models.BooleanField(default=False)
    swiggy_url = models.CharField(max_length=1000, default='')
    justdail = models.BooleanField(default=False)
    justdail_url = models.CharField(max_length=1000, default='')
    indiamart = models.BooleanField(default=False)
    indiamart_url = models.CharField(max_length=1000, default='')

    pay_link = models.BooleanField(default=False)

    tripadvisor = models.BooleanField(default=False)
    tripadvisor_url = models.CharField(max_length=1000, default='')





class authorised_sign(models.Model):
    sign = models.FileField(null=True, blank=True, upload_to='authorised_sign')
    merchant_id = models.ForeignKey(GreenBillUser, null=True, on_delete= models.CASCADE)
    selection = models.CharField(max_length=5,null=True)

class temp_pdf_check(models.Model):
    pdf_image = models.FileField(null=True, blank=True, upload_to='temp1/')
    image_con = models.FileField(null=True, blank=True, upload_to='temp1/')

class contact_card(models.Model):
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    card_name = models.CharField(max_length=45,null=True)
    card_phone_no = models.CharField(max_length=45,null=True)
    card_email = models.CharField(max_length=45,null=True)
    card_country = models.CharField(max_length=45,null=True)
    card_city = models.CharField(max_length=45,null=True)
    card_photo = models.ImageField(null=True, blank=True, upload_to='card_pic/')
    cover_photo = models.ImageField(null=True, blank=True, upload_to='card_pic/')
    background_photo = models.ImageField(null=True, blank=True, upload_to='card_pic/')
    qrcode_photo = models.ImageField(null=True, blank=True, upload_to='card_pic/')
    card_desc = models.CharField(max_length=25,null=True)
    temp_choice = models.CharField(max_length=25,null=True)
    about_us = models.CharField(max_length=25,null=True)
    bussiness_time = models.CharField(max_length=25,null=True)
    alternate_mobile = models.CharField(max_length=25,null=True)

    
    facebook = models.BooleanField(default=False)
    facebook_url = models.CharField(max_length=1000, default='')
    youtube = models.BooleanField(default=False)
    youtube_url = models.CharField(max_length=1000, default='')
    email = models.BooleanField(default=False)
    email_url = models.CharField(max_length=1000, default='')

    phone = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=100, default='')
    website = models.BooleanField(default=False)
    website_url = models.CharField(max_length=1000, default='')
    map = models.BooleanField(default=False)
    map_link = models.CharField(max_length=1000, default='')
    msg = models.BooleanField(default=False)
    msg_number = models.CharField(max_length=100, default='')
    whatsapp = models.BooleanField(default=False)
    whatsapp_number = models.CharField(max_length=100, default='')
    address_book = models.BooleanField(default=False)
    address_book_number = models.CharField(max_length=100, default='')

    gallery1 = models.ImageField(null=True, blank=True, upload_to='card_pic/')
    gallery2 = models.ImageField(null=True, blank=True, upload_to='card_pic/')
    gallery3 = models.ImageField(null=True, blank=True, upload_to='card_pic/')
    

    # for client photo

    client1 = models.ImageField(null=True, blank=True, upload_to='card_pic/')
    client2 = models.ImageField(null=True, blank=True, upload_to='card_pic/')
    client3 = models.ImageField(null=True, blank=True, upload_to='card_pic/')
    client4 = models.ImageField(null=True, blank=True, upload_to='card_pic/')
    client5 = models.ImageField(null=True, blank=True, upload_to='card_pic/')
    client6 = models.ImageField(null=True, blank=True, upload_to='card_pic/')



    # bank detail
    
    acco_holder_name = models.CharField(max_length=100,default='')
    acc_no     =  models.CharField(max_length=20,default='')
    ifsc_code  = models.CharField(max_length=20,default='')
    bank_name  = models.CharField(max_length=100,default='')
    pan_card   = models.CharField(max_length=15 ,default='')
    gstin_no   = models.CharField(max_length=100,default='')

    # feedback

    share= models.IntegerField(null= True, default="0")
    view = models.IntegerField(null= True, default="0")



class Card_feedback(models.Model):
    merchant_business_id = models.ForeignKey(to = MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    comment = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(default=timezone.now, null=True,)
    rating  = models.CharField(max_length=5 ,default='')