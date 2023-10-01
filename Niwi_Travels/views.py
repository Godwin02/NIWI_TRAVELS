from django.shortcuts import render
from django.db import IntegrityError
from django.urls import reverse
from .forms import RegistrationForm
from .models import CustomUser,UserProfile

from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate ,login as auth_login,logout
def index(request):
    return render(request, 'index.html')
def register(request):
    # if request.method == 'POST':
    #     form = SignupForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('login')
    #     else:
    #          error_message = 'This email address is already registered.'
    #          return render(request, 'registration.html', {'error_message': error_message})

    # return render(request, 'registration.html')

    #     username = request.POST.get('username')
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')
    #     try:
    #         new_user = CustomUser(username=username, email=email, password=password)
    #         new_user.save()
    #         return render(request,'login.html')
    #     except IntegrityError:
    #     #     # Handle the case where the email already exists
    #          error_message = 'This email address is already registered.'
    #          return render(request, 'registration.html', {'error_message': error_message})

    # return render(request, 'registration.html')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm_password', None)
        user_type= request.POST.get('user_type',None)
        # role = CustomUser.CUSTOMER
        if username and email and  password:
            if CustomUser.objects.filter(email=email).exists():
                    messages.success(request,("Email is already registered."))
            elif CustomUser.objects.filter(username=username).exists():
                   messages.success(request,("Username is already registered."))
            
            elif password!=confirm_password:
                    messages.success(request,("Password's Don't Match, Enter correct Password"))
            else:
                    user = CustomUser(username=username, email=email,user_type=user_type)
                    user.set_password(password)  # Set the password securely
                    user.is_active=True
                    user.save()
                    user_profile = UserProfile(user=user)
                    user_profile.save()
                # activateEmail(request, user, email)
                    return redirect('login')
      
    else:
            form = RegistrationForm()        
    return render(request, 'registration.html',{'form':form})
def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        # user=authenticate(request, username=username,password=password)
        # user=CustomUser.objects.filter(username=username,password=password).first()
        #if user is not None:
            # auth_login(request,user)
            # request.session['user_type']=user.user_type
            # request.session['username']=user.username
            # request.session['password']=user.password
            # if user.user_type==CustomUser.ADMIN:
            #     return redirect('http://127.0.0.1:8000/admin/')
            # elif user.user_type==2:
            #     return render(request,'loginview.html', {'user':user})
            
        if username and password:
            user = authenticate(request, username =username , password=password)
            #user=CustomUser.objects.filter(username=username,password=password).first()
        
            if user is not None:
                auth_login(request,user)
                if request.user.user_type == 'Traveller':
                    return redirect('loginview')
                    #return render(request,'loginview.html', {'user':user})
            
                elif request.user.user_type == 'Driver':
                    print("user is Driver")
                #     return redirect(reverse('therapist'))
                elif request.user.user_type == 'Admin':
                    print("user is admin")                   
                    return redirect('http://127.0.0.1:8000/admin/')
                # else:
                #     print("user is normal")
                #     return redirect('')

            else:
                messages.success(request,("Invalid Username or Password."))
                return redirect('login')
    return render(request, 'login.html')
def loginview(request):
    return render(request,'loginview.html')
def log(request):
     logout(request)
     return redirect('loginview')
# Create your views here.

