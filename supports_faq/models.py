from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Add_Module_Name (models.Model):
    user_name = models.CharField(max_length=1000, null=True, default="")
    module_name = models.CharField(max_length=1000, null=True, default="")


class Video_Model(models.Model):
    user_name = models.CharField(max_length=1000, null=True, default="")
    module_name = models.CharField(max_length=1000, null=True, default="")
    video_url = models.CharField(max_length=500, null=True, default="")
    video_title = models.CharField(max_length=500,null=True,default="")


class FAQs_Model(models.Model):
    user_name = models.CharField(max_length=1000, null=True, default="")
    module_name = models.CharField(max_length=1000, null=True, default="")
    question = models.CharField(max_length=500, null=True, default="")
    answer = models.CharField(max_length=500, null=True, default="")


class Blogs_Model(models.Model):
    user_name = models.CharField(max_length=1000, null=True, default="")
    module_name = models.CharField(max_length=1000, null=True, default="")
    blog = RichTextUploadingField(blank=True, null=True)
    blog_title = models.CharField(max_length=1000, null=True, default="")
