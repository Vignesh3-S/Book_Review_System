from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import user,book
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
class registerform(forms.ModelForm):
    username = forms.CharField(label='',widget= forms.TextInput(attrs={'placeholder':'Full Name','class':'form-control'}))
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder':'Email','class':'form-control'}))
    mobilenumber = PhoneNumberField(label = '',widget=PhoneNumberPrefixWidget(attrs={'placeholder': 'Mobile', 'class': "form-control"}),)
    password = forms.CharField(label='',max_length=8,min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':"form-control"}),)
    
    class Meta:
        model = user
        fields = ('username','email','mobilenumber','password','usertype',)

class signinform(forms.ModelForm):
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder':'Email','class':'form-control'}))
    password = forms.CharField(label='',max_length=8,min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'password','class':"form-control"}),)
    class Meta:
        model = user
        fields = ('email','password','usertype',)

class additionalprofile(forms.ModelForm):
    mobilenumber = PhoneNumberField(label = '',widget=PhoneNumberPrefixWidget(attrs={'placeholder': 'Mobile', 'class': "form-control"}),)
    class Meta:
        model = user
        fields = ('usertype','mobilenumber')

class bookform(forms.ModelForm):
    class Meta:
        model = book
        fields = ('bookname','bookauthor','reviewauthor','booktype','bookimg','bookfile',)

class Queryform(forms.Form):
    Name = forms.CharField(label='',widget= forms.TextInput(attrs={'placeholder':'Full Name','class':'form-control'}))
    Email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder':'Email','class':'form-control'}))
    Subject = forms.CharField(label = '',widget=forms.TextInput(attrs={'placeholder': 'Subject', 'class': "form-control"}),)
    Query = forms.CharField(label = '',widget=forms.Textarea(attrs={'placeholder':'your feedback/query', 'class':"form-control"}),)
    
# Create your models here.
