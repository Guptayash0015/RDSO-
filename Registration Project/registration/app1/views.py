from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .helpers import send_forget_password_mail
from django.urls import reverse



def HomePage(request):
    return render(request, 'home.html')

def SignupPage(request):
    password_error_message = None

    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('signup')

        if password1!=password2:
          messages.error(request,"Your password and confirm password are not Same!!")
          return redirect('signup')
        my_user = User.objects.create_user(username, email, password1)
        my_user.save()
        return redirect('login')
    
    
    return render (request,'signup.html')


def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password1=request.POST.get('password')
        user=authenticate(request,username=username,password=password1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            error_message = "Username or password is incorrect!"
            return render (request,'login.html',{'error_message': error_message})

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def Home(request):
    return render(request,'home.html')



def ChangePassword(request , token=None):
    context = {}
    
    
    try:
        profile_obj = app1.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(reverse('change_password', args=[token]))
                
            if new_password != confirm_password:
                messages.success(request, 'Passwords do not match.')
                return redirect(reverse('change_password', args=[token]))
            
            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            
            # Redirect to the login page
            return redirect('login')
               
    except Exception as e:
        print(e)
    return render(request , 'change-password.html' , context)

import uuid
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            app1_obj= app1.objects.get(user = user_obj)
            app1_obj.forget_password_token = token
            app1_obj.save()
            
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')
                
    
    
    except Exception as e:
        print(e)
    return render(request , 'forget-password.html')




    
    