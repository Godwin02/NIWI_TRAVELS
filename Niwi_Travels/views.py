from django.shortcuts import render
from django.db import IntegrityError
from django.urls import reverse
from .forms import RegistrationForm
from .models import CustomUser,UserProfile
from django.contrib.auth.decorators import login_required
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
                    return redirect('log')
      
    else:
            form = RegistrationForm()        
    return render(request, 'registration.html',{'form':form})
def login(request):
    
    if 'username' in request.session:
         return redirect('/loginview')
    if 'username' in request.session:
         return redirect('/driver')
    if 'username' in request.session:
         return redirect('http://127.0.0.1:8000/admin/')
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
                print(request.user.user_type,"1")
                if request.user.user_type == 'Traveller':
                    request.session["username"] = user.username
                    # print(request.session["username"])
                    # if request.session["username"]:
                    return redirect('/loginview', {'username': username})
                    #return render(request,'loginview.html', {'user':user})
            
                elif request.user.user_type == 'Driver':
                    request.session["username"] = user.username
                    return redirect('/driver',{'username': username})
                #     return redirect(reverse('therapist'))
                elif request.user.user_type == '1':
                    print("user is admin")
                    request.session["username"] = user.username                   
                    return redirect('http://127.0.0.1:8000/admin/')
                # else:
                #     print("user is normal")
                #     return redirect('')

            else:
                messages.success(request,("Invalid Username or Password."))
                return redirect('log')
    return render(request, 'login.html')


@login_required(login_url='log')
def loginview(request):
    if request.user.user_type == 'Traveller':
    # if request.user.is_authenticated:
        return render(request,'loginview.html')
    return redirect('/driver')
    # return redirect('log')
@login_required(login_url='log')
def dri(request):
    if request.user.user_type == 'Driver':
    # if request.user.is_authenticated:
        return render(request,'driver.html')
    return redirect('/loginview')
    # return redirect('log')
def logo(request):
    if request.user.is_authenticated:
        # request.session["username"] =""
        # print(request.session["username"],"2")
        logout(request)
    return render(request,'login.html')
    #  return render(request,'login.html')
    
# Create your views here.

