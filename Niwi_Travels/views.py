from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Traveller, Driver
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Traveller, Driver
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache

# Import User model dynamically to ensure compatibility
User = get_user_model()

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'register.html')

def index(request):
    return render(request, 'index.html')

# Define a view to activate the user's email
def activate_email(request, uidb64, token):
    try:
        # Decode the uid and get the user
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        
        # Verify the token
        if default_token_generator.check_token(user, token):
            # Activate the user's account
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated. You can now log in.")
            return redirect('/log')
        else:
            messages.error(request, "Invalid activation link.")
            return redirect('/log')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        messages.error(request, "Invalid activation link.")
        return redirect('/log')
    
@csrf_protect
@sensitive_post_parameters()
@never_cache
@csrf_exempt
def drireg(request):
    if request.user.is_authenticated:
        return redirect('/dhome')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if an active user with the same username exists
        if User.objects.filter(username=username, is_active=True).exists() or User.objects.filter(email=email, is_active=True).exists():
            messages.error(request, "Username or email is already taken.")
            return redirect('/dregister')
        cache.clear()
        # Create a user with is_active=False initially
        user = User(username=username, email=email, is_driver=True, is_active=False)
        user.set_password(password)

        try:
            user.full_clean()  # Validate the user data
            user.save()
            driver = Driver(user=user)
            driver.save()
        except ValidationError as e:
            # Handle validation errors, e.g., unique constraint violations
            messages.error(request, e.messages[0])  # Display the first error message
            return redirect('dregister')

        # Generate an activation token for the user
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Create an activation link with the token
        activation_link = reverse('activate_email', args=[uid, token])

        # Construct the activation email
        subject = 'Activate Your Account'
        message = render_to_string('activation_email.html', {
            'user': user,
            'domain': get_current_site(request).domain,
            'activation_link': activation_link,
        })
        from_email = 'godwinbmenachery2024a@mca.ajce.in'  # Change this to your email
        to_email = user.email

        # Send the activation email
        send_mail(subject, message, from_email, [to_email])

        return render(request, 'index.html', {'email': user.email})

    cache.clear()
    return render(request, 'dregister.html')

def login(request):
    if request.user.is_authenticated and request.user.is_traveller:
        return redirect('/thome')
    if request.user.is_authenticated and request.user.is_driver:
        return redirect('/dhome')
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/admins')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            
            if user.is_traveller==True:
                request.session["user_type"] = "traveller"  # Set session variable for user type
                return redirect('/thome')
            elif user.is_driver:
                request.session["user_type"] = "driver"  # Set session variable for user type
                return redirect('/dhome')
            elif user.is_staff:
                request.session["user_type"] = "admin"  # Set session variable for user type
                return redirect('/admins')
        else:
            messages.error(request, "Username or Password is Incorrect.")
    
    cache.clear()
    return render(request, 'login.html')

@never_cache
@login_required(login_url='log')
def traveller_home(request):
    user_type = request.session.get("user_type")  # Get user type from session
    
    if user_type == "traveller":
        profile = request.user.traveller
        return render(request, 'loginview.html', {'profile': profile})
    
    # If user is not a traveller or not logged in, redirect to login
    return render(request, 'loginview.html')

@never_cache
@login_required(login_url='log')
def update_traveler(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        gender = request.POST['gender']
        country = request.POST['country']
        profile_photo = request.FILES.get('profile_photo')

        traveler, created = Traveller.objects.get_or_create(user=user)
        traveler.first_name = first_name
        traveler.last_name = last_name
        traveler.phone_number = phone_number
        traveler.gender = gender
        traveler.country = country
        if profile_photo:
            traveler.profile_photo = profile_photo
        traveler.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('/profile_updated')
    cache.clear()
    return render(request, 'update_traveler.html')

@login_required(login_url='log')
def profile_updated(request):
    return render(request, 'tprofile_updated.html')

@never_cache
@login_required(login_url='log')
def viewprofile(request):
    if request.user.is_traveller:
        profile = request.user.is_traveller
        user_details = {
            'username': request.user.username,
            'email': request.user.email,
        }
        return render(request, 'viewprofileT.html', {'profile': profile, 'user_details': user_details})
    cache.clear()
    return redirect('/log')

@login_required(login_url='log')
def update_driver(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        contact_email = request.POST['contact_email']
        contact_phone_number = request.POST['contact_phone_number']
        profile_photo = request.FILES.get('profile_photo')
        license = request.FILES.get('license')

        driver, created = Driver.objects.get_or_create(user=user)
        driver.first_name = first_name
        driver.last_name = last_name
        driver.contact_email = contact_email
        driver.contact_phone_number = contact_phone_number

        if profile_photo:
            driver.profile_photo = profile_photo
        
        driver.license = license

        driver.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('/dpro_updated')
    cache.clear()
    if request.user.is_driver:
        profile = request.user.driver
        user_details = {
            'username': request.user.username,
            'email': request.user.email,
        }
    return render(request, 'update_driver.html', {'profile': profile, 'user_details': user_details})

@login_required(login_url='log')
def dprofile_updated(request):
    return render(request, 'dprofile_updated.html')

@never_cache
@login_required(login_url='log')
def driver_home(request):
    user_type = request.session.get("user_type")  # Get user type from session
    
    if user_type == "driver":
        profile = request.user.driver
        return render(request, 'driver.html', {'profile': profile})
    
    # If user is not a driver or not logged in, redirect to login
    return redirect('/log')

@login_required(login_url='log')
def viewprofileD(request):
    user_type = request.session.get("user_type")  # Get user type from session
    
    if user_type == "driver":
        profile = request.user.driver
        user_details = {
            'username': request.user.username,
            'email': request.user.email,
        }
        return render(request, 'viewprofileD.html', {'profile': profile, 'user_details': user_details})
    
    # If user is not a driver or not logged in, redirect to login
    return redirect('/log')

def logo(request):
    logout(request)
    cache.clear()
    return render(request, 'index.html')


@never_cache
@login_required(login_url='log')
def admin(request):
    if request.user.is_staff:
        return render(request, 'adminreg.html')
    cache.clear()
    return redirect('login')


@never_cache
@login_required(login_url='log')
def user_list(request):
    if request.user.is_staff:
        user_profiles = User.objects.all()
        user_count = user_profiles.count()
        paginator = Paginator(user_profiles, 10)
    
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {'user_profiles': page, 'user_count': user_count}
        return render(request, 'user_list.html', context)
    cache.clear()
    return redirect('/log')

@never_cache
@login_required(login_url='log')
def travellers(request):
    if request.user.is_staff:
        user_profiles = User.objects.filter(is_traveller=True)
        user_count = user_profiles.count()
        paginator = Paginator(user_profiles, 10)
    
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {'user_profiles': page, 'user_count': user_count}
        return render(request, 'travellers.html', context)
    return redirect('/log')


@never_cache
@login_required(login_url='log')
def drivers(request):
    if request.user.is_staff:
        user_profiles = User.objects.filter(is_driver=True)
        user_count = user_profiles.count()
        paginator = Paginator(user_profiles, 10)
    
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {'user_profiles': page, 'user_count': user_count}
        return render(request, 'drivers.html', context)
    return redirect('/log')

@never_cache
@login_required(login_url='log')
def update_user_status(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        # Perform your logic to update the user's status here
        user.is_active = not user.is_active  # Toggle the user's status
        user.save()
    except User.DoesNotExist:
        pass  # Handle the case where the user is not found (optional)

    # Redirect back to the user list page
    return redirect('drivers')



from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

# Use the built-in views provided by Django's auth app
class MyPasswordResetView(auth_views.PasswordResetView):
    template_name = 'password_reset_form.html'  # Your template for the password reset form
    email_template_name = 'password_reset_email.html'  # Your email template for the password reset email
    success_url = reverse_lazy('password_reset_done')  # URL to redirect after successful form submission

class MyPasswordResetDoneView(auth_views.PasswordResetDoneView):
        template_name = 'password_reset_done.html'  # Your template for password reset done page


class MyPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'  # Your template for password reset confirmation form
    success_url = reverse_lazy('password_reset_complete')  # URL to redirect after successful password reset

class MyPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'  # Your template for password reset complete page

    def get(self, request, *args, **kwargs):
        return redirect('/log')  # Replace 'home' with the desired URL name






from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

def deactivate_user(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        is_active = not user.is_active  # Toggle user's active status
        user.is_active = is_active
        user.save()

        if not is_active:
            # Send the deactivation email
            subject = 'Account Deactivation Notification'
            from_email = 'godwinbmenacehry2024a@mca.ajce.in'  # Replace with your email address
            to_email = user.email
            context = {
                'user': user,  # Pass the user instance to the email template
                # You can add more context data here as needed
            }
            # Load the HTML email template
            html_message = render_to_string('deactivation_email.html', context)

            # Create a plain text version of the email
            plain_message = strip_tags(html_message)

            # Send the email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

        return JsonResponse({'is_active': user.is_active})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)