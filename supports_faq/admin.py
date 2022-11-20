from django.contrib import admin
from .models import *

class FAQsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'module_name', 'question','answer')
admin.site.register(FAQs_Model, FAQsAdmin)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'module_name', 'video_url','video_title')
admin.site.register(Video_Model, VideoAdmin)

class BlogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'module_name', 'blog_title', 'blog')
admin.site.register(Blogs_Model, BlogsAdmin)

class Add_Module_NameAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'module_name')
admin.site.register(Add_Module_Name, Add_Module_NameAdmin)