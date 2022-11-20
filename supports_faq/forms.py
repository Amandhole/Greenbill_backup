from django import forms
from .models import Blogs_Model
from ckeditor_uploader.fields import RichTextUploadingField


class BlogsForm(forms.ModelForm):
    class Meta:
        model = Blogs_Model
        fields = ('blog',)

class CkEditBlogsForm(forms.ModelForm):
    class Meta:
        model = Blogs_Model
        fields = ('blog',)

    def __init__(self, *args, **kwargs):
	    super(CkEditBlogsForm, self).__init__(*args, **kwargs)
	    self.fields['blog'].widget.attrs\
	        .update({
	          'id':'blog_edit'
	        })

class EditBlogForm(forms.ModelForm):
    class Meta:
        model = Blogs_Model
        fields = ('blog',)
        widgets = {
            'blog': forms.TextInput(attrs={'id': 'blog_faq_id', 'name': 'blog'})

        }
