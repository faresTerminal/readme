from django import forms
from django.db import models
from tinymce.widgets import TinyMCE

from blogArabic.models import articles, author, comment_put
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

# add multy fields to register page
class MyRegistrationForm(UserCreationForm):
   
   email = forms.EmailField(required = True)
  
  


   class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

   def save(self, commit = True):
        user = super(MyRegistrationForm, self).save(commit = False)
       
        user.email = self.cleaned_data['email']
       

        if commit:
                user.save()
        return user 

   def clean_email(self):
      email = self.cleaned_data['email']
      qs = User.objects.filter(email = email)
      if qs.exists():
          raise ValidationError ('Email is already registed')
      return email


   def check_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no user registered with the specified email address!")

        return email 



class createForm(forms.ModelForm):
    body = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = articles
        fields = [
            'category',
            'title',
            'image',
            'taker_image',
            'body',
            'source',
          
        ]
class createAuthor(forms.ModelForm):
    class Meta:
        model = author
        fields = [
            'profile_picture',
            'job',
            'pays',
            'firstname',
            'age',
            'gender',
            'level',
            'facebook_account',
            'instagram_account', 
            'youtube_channel',  
            'twitter_account', 
        ]

class CommentForm(forms.ModelForm):

        class Meta:
                model = comment_put
                fields =[
                 'comment',
                 
                ]


