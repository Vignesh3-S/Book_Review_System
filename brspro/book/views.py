from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from book.form import registerform,signinform,additionalprofile,bookform,Queryform
from django.contrib.auth import login,logout
from django.core.mail import send_mail
from book.backend import EmailAuthBackend
from .models import user,book
from django.utils import timezone
import phonenumbers
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.hashers import make_password
import os

def home(request):
    if request.method =='GET':
        form = Queryform
        return render(request,'registration/index.html',{'form':form})
    elif request.method == 'POST':
        form = Queryform(request.POST)
        if form.is_valid():
            name = request.POST['Name']
            email = request.POST['Email']
            sub = request.POST['Subject']
            query = request.POST['Query']
            message = 'Hai admin, this is '+ name +' with an email '+ email +'. My query or feedback  is ' + query + '.'
            send_mail(sub,message,'brsapp33@gmail.com',[email],fail_silently=False)
            return redirect('/home',messages.success(request,'Message sent Successfully.'))


@login_required
def mhome(request,userid):
    if request.method == "GET":
        form = Queryform
        uname  = user.objects.get(id = userid)
        uname.last_login = timezone.now()
        uname.save
        name = uname.username
        id = uname.id
        return render(request,'registration/mainhome.html',{'name':name,'userid':id,'form':form})
    elif request.method == 'POST':
        form = Queryform(request.POST)
        if form.is_valid():
            name = request.POST['Name']
            email = request.POST['Email']
            sub = request.POST['Subject']
            query = request.POST['Query']
            message = 'Hai admin, this is '+ name +'with an email '+ email +'. My query or feedback  is ' + query + '.'
            send_mail(sub,message,email,['brsapp33@gmail.com'],fail_silently=False)
            urlparam = '/mhome/'+userid
            return redirect(urlparam,messages.success(request,'Message sent Successfully.'))


def mhomecheck(request):
    if request.user.is_authenticated:
        return redirect('mhome',request.user.id)
    else:
        return redirect('login')

@login_required
def mypage(request,user_id):
    if request.user.usertype == 'reader':
        url = '/mhome/'+user_id
        return redirect(url,messages.error(request,'Sorry This is for Publishers.'))
    else:
        user_obj = user.objects.get(id = user_id)
        name = user_obj.username
        bookinfo = book.objects.filter(user_id = user_obj)
        return render(request,'registration/mypage.html',{'name':bookinfo,'username':name})
        
@login_required
def createbook(request,number):
    if request.method == 'GET':
        id = user.objects.get(username = number)
        number = id.id
        return render(request,'registration/bookadd.html',{'form':bookform,'id':number})
    if request.method == "POST":
        form = bookform(request.POST,request.FILES)
        if form.is_valid():
            bname = request.POST['bookname']
            bauthor = request.POST['bookauthor']
            rauthor = request.POST['reviewauthor']
            btype = request.POST['booktype']
            bimg = request.FILES['bookimg']
            bfile = request.FILES['bookfile']
            book.objects.create(user_id = number, bookname = bname, bookauthor = bauthor, reviewauthor = rauthor, booktype = btype, bookimg = bimg, bookfile = bfile)
            return redirect('myreview',number)
        else:
            return redirect('bookadd',messages.error(request,'Please fill the form correctly'),)

@login_required
def updatebook(request,name,number):
    if request.method == "GET":
        data = book.objects.get(user_id = number,bookname = name)
        if data:
            bookauthor = data.bookauthor
            reviewauthor = data.reviewauthor
            btype = data.booktype
            return render(request,'registration/update.html',{'id':number,'bname':name,'bauthor':bookauthor,'rauthor':reviewauthor,'type':btype})
    if request.method == "POST":
        data = book.objects.get(user_id = number, bookname = name)
        if data:
            data.bookname = request.POST['bookname']
            data.bookauthor = request.POST['bookauthor']
            data.reviewauthor = request.POST['reviewauthor']
            data.booktype = request.POST['booktype']
            data.save()
            return redirect('myreview',number)     
    else:
        return redirect('bookupdate',messages.error(request,'Please fill the form correctly'),)

@login_required
def bookreview(request):
    books = book.objects.all()
    return render(request,'registration/bookreview.html',{'book':books}) 

@login_required()
def search(request):
    if request.method == 'GET':
        data = request.GET.get('search')
        if book.objects.filter(reviewauthor__contains = data):
            reviewar = book.objects.filter(reviewauthor__contains = data)
            return render(request,'registration/bookreview.html',{'results':reviewar}) 
        elif book.objects.filter(bookauthor__contains = data):
            bookar = book.objects.filter(bookauthor__contains = data)
            return render(request,'registration/bookreview.html',{'results':bookar})
        elif book.objects.filter(booktype__contains = data):
            booktp = book.objects.filter(booktype__contains = data)
            return render(request,'registration/bookreview.html',{'results':booktp}) 
        elif book.objects.filter(reviewauthor__contains = data):
            bookne = book.objects.filter(bookname__contains = data)
            return render(request,'registration/bookreview.html',{'results':bookne})  
        else:
            return redirect("/bookreviews",messages.error(request,'Search a valid object.'))
    else:
        return HttpResponse('Bad request')

@login_required
def delete(request,name,number):
    data = book.objects.get(user_id = number,bookname = name)
    os.remove(data.bookimg.path)
    os.remove(data.bookfile.path)
    data.delete()
    return redirect('myreview',number) 

def tdptypro(request):
    if request.method == 'GET':
        try:
            check = user.objects.get(username = request.user)
            if check.usertype:
                return redirect('mhome',check.username)
            else:
                return render(request,'registration/thirdptprof.html',{'profm':additionalprofile})
        except:
            return redirect('home')
    if request.method == 'POST':
        form = additionalprofile(request.POST)
        if form.is_valid():
            rtype = request.POST['usertype']
            phone_1 = "+"+ str(phonenumbers.country_code_for_region(request.POST['mobilenumber_0']))
            phone_2= request.POST['mobilenumber_1']
            phone = phone_1+phone_2
            userobj = user.objects.get(username = request.user)
            nameobj = SocialAccount.objects.get(user = userobj) 
            print(nameobj.id)
            a = nameobj.extra_data
            uname = a['name']
            userobj.username = uname
            userobj.usertype = rtype
            userobj.mobilenumber = phone
            userobj.save()
            return redirect('mhome',userobj.id)
        else:
            phone_1 = "+"+ str(phonenumbers.country_code_for_region(request.POST['mobilenumber_0']))
            phone_2= request.POST['mobilenumber_1']
            phone = phone_1+phone_2
            mob = phonenumbers.parse(phone)
            mobile = phonenumbers.is_valid_number(mob)
            if mobile == False:
                return redirect("/register",messages.error(request,'Enter a valid phone number.'))
            

def register(request):
    if request.method == 'POST':
        form = registerform(request.POST)
        if form.is_valid():
            fname = request.POST['username']
            email = request.POST['email']
            rtype = request.POST['usertype']
            password = request.POST['password']
            message = 'Hai '+ fname + ',this is from book review application. Thanks for your registration as ' + rtype + '. Please use your registered email and password to login using the below link.\nhttp://127.0.0.1:8000/login/'"\nDon't reply to this email."
            userform = form.save(commit=False)
            userform.password = make_password(password)
            userform.save()
            send_mail('register indication',message,'brsapp33@gmail.com',[email],fail_silently=False)
            return redirect('/register',messages.success(request,'Successfully registered'))
        else:
            email = request.POST['email']
            dbemail = user.objects.filter(email = email)
            print(dbemail)
            if dbemail:
                return redirect('/register',messages.error(request,"Email already exists"))
            
            phone_1 = "+"+ str(phonenumbers.country_code_for_region(request.POST['mobilenumber_0']))
            phone_2= request.POST['mobilenumber_1']
            phone = phone_1+phone_2
            mob = phonenumbers.parse(phone)
            mobile = phonenumbers.is_valid_number(mob)
            if mobile == False:
                return redirect("/register",messages.error(request,'Enter a valid phone number.'))
           
    return render(request,'registration/signuptemplate.html',{"pbfm":registerform})

def lo(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        usertype = request.POST['usertype']
        try:
            usern = user.objects.get(email = email)
        except:
            return redirect('/login',messages.error(request,'No such user.'))
        userid = usern.id
        if usertype == 'publisher':
            Userobj = EmailAuthBackend()
            User = Userobj.authenticate(email = email , password = password, usertype = usertype)
            if User is not None:
                login(request,User,backend='book.backend.EmailAuthBackend')
                return redirect('mhome',userid)
            else:
                return redirect('/login',messages.error(request,'Enter valid credentials.'))
        else:
            Userobj = EmailAuthBackend()
            User = Userobj.authenticate(email = email , password = password,usertype = usertype)
            if User is not None:
                login(request,User,backend='book.backend.EmailAuthBackend')
                return redirect('mhome',userid)
            else:
                return redirect('/login',messages.error(request,'Enter valid credentials.'))
    return render(request,'registration/login.html',{'logo':signinform})

def signout(request):
    logout(request)
    return redirect('home')
    
# Create your views here.
