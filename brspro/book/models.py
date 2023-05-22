from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from book.manager import customusermanager
from django.utils.translation import gettext_lazy as _

class user(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(verbose_name= "FullName" , max_length= 35)
    email = models.EmailField(verbose_name='Email', unique = True)
    mobilenumber = PhoneNumberField(verbose_name="Mobile")
    password = models.CharField(verbose_name="Password",max_length=255)
    typechoices = [('publisher','Publisher'),('reader','Reader')]
    usertype = models.CharField(verbose_name= "UserType" , max_length = 20 , choices=typechoices)
    date_joined = models.DateTimeField(auto_now_add=True,verbose_name='Date_Joined')
    date_modified = models.DateTimeField(auto_now=True,verbose_name='Modified_Date')
    last_login = models.DateTimeField(default=timezone.now,verbose_name='last_login')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = customusermanager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password','mobilenumber']
    
    def __str__(self):
        return self.username
    

class book(models.Model):
    user = models.ForeignKey("user",on_delete=models.CASCADE,verbose_name="user_id")
    bookname = models.CharField(verbose_name="Book Name",max_length=50)
    bookauthor = models.CharField(verbose_name='Book Author',max_length=50)
    reviewauthor = models.CharField(verbose_name='Review Author',max_length=50)
    booktypechoices= [('fantasy','fantasy'),('romance novel','romance novel'),('autobiography','autobiography'),('biography','biography'),
                      ('mystery','mystery'),('memoir','memoir'),('horror','horror'),('philosophy','philosophy'),
                      ('cookbook','cookbook'),("children's literature","children's literature"),('anthology','anthology'),('nonfiction','nonfiction'),
                      ('short story','short story'),('drime','drime'),('dncyclopedia','dncyclopedia'),('dairy','dairy'),
                      ('politics','politics'),('biblophile','biblophile'),('fable','fable'),('fiction','fiction'),]
    booktype = models.CharField(verbose_name= "BookType" , max_length = 30 , choices=booktypechoices)
    bookimg = models.ImageField(verbose_name='Book Image', upload_to="fileimages")
    bookfile = models.FileField(verbose_name = 'Review File',upload_to="audio")
    createdatetime = models.DateTimeField(auto_now_add=True,verbose_name='Create DateTime')
    modifieddatetime =  models.DateTimeField(auto_now=True,verbose_name='Modified DateTime')

    def __str__(self):
         return self.bookname