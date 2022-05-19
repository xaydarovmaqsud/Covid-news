from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.http.response import JsonResponse,HttpResponse
from .models import *
import json
from .forms import LoginForm,RegistrationForm
from .decorators import not_logged,no_logged
# Create your views here.


@not_logged
def home(request):
    context={
        'new_list':New.objects.all(),
        'category':Category.objects.all()
    }
    return render(request,'index.html',context=context)

def bycategory(request,id):
    context={
        'new_list':New.objects.filter(category=id),
        'category':Category.objects.all()
    }
    return render(request,'index.html',context=context)

@not_logged
def new_details(request,id):
    new=New.objects.get(id=id)
    new.view_add
    new.likes
    new.dislikes
    context={
        'new':new,
        'category':Category.objects.all(),
    }
    return render(request,'new_details.html',context=context)

def comment(request,id):
    if request.method=='POST':
        data=json.loads(request.body)
        print(data)
        comment=data.get('comment',None)
        person=Person.objects.get(user=request.user)
        new=New.objects.get(id=id)
        if comment:
            new.setcomment(person=person,comment=comment)
            return HttpResponse(status=201)

def reaction(request,id,react):
    if request.user.username:
        person=Person.objects.get(user=request.user)
        new=New.objects.get(id=id)
        new.setreaction(person=person,react=react)
        response={
            'likes':new.likes,
            'dislikes':new.dislikes
        },
        status=200
    else:
        response={
            'error':'Undefined user'
        },
        status=401
    return JsonResponse(
        data={
            'res':response
        },
        status=status
        )
@no_logged
def login_view(request):
    loginform=LoginForm()
    if request.method=='POST': 
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            username=login_form.data.get('username')
            password = login_form.data.get('password')
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect('new')
            print(username,password)
    return render(request=request,template_name='login.html',context={'login_form':loginform})

def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
@no_logged
def registration(request):
    error_user=None
    error_confirm=None
    if request.method=='POST':
        reg_form=RegistrationForm(request.POST)
        if reg_form.is_valid():
            first_name=reg_form.data.get('first_name')
            last_name=reg_form.data.get('last_name')
            username=reg_form.data.get('username')
            email=reg_form.data.get('email')
            password = reg_form.data.get('password')
            password1 = reg_form.data.get('password1')
            res=User.objects.filter(username=username)
            if password1==password and len(res)==0:
                user=User.objects.create(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
                person=Person.objects.create(user=user)
                login(request,user)
                return redirect('new')
            else:
                error_user='Bu foydalanuvchi nomi band!' if len(res)!=0 else None
                error_confirm='Parolni tugri kirilitganiga ishonch hosil qiling!' if password1!=password else None

    return render(request,template_name='registration.html',context={
        'error_user':error_user,
        'error_confirm':error_confirm
    })