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
    running_packages = TravelPackage.objects.filter(status='Running')

    return render(request, 'index.html',{'running_packages': running_packages})

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
        # username = request.POST['username']
        username = request.POST['email']
        password = request.POST['password']

        # Check if an active user with the same username exists
        if User.objects.filter(email=username, is_active=True,is_driver=True).exists():
            messages.error(request, " Email is already taken.")
            return redirect('/dregister')
        cache.clear()
        # Create a user with is_active=False initially
        user = User(username=username,email=username, is_driver=True ,is_traveller=False, is_active=False)
        user.set_password(password)

        try:
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
        messages.success(request, "A link has been sent to your registered email. Please click on it to continue.")
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
                request.session["user_type"] = "traveller" 
                print("hello") # Set session variable for user type
                messages.success(request, "welcome To NIWI TRAVELS. Explore the Unexplored!")
                return redirect('/thome')
            elif user.is_driver==True:
                request.session["user_type"] = "driver"  # Set session variable for user type
                return redirect('/dhome')
            elif user.is_staff:
                request.session["user_type"] = "admin"  # Set session variable for user type
                return redirect('/admins')
        else:
            messages.error(request, "Username or Password is Incorrect.")
    
    cache.clear()
    return render(request, 'login.html')

@csrf_protect
@sensitive_post_parameters()
@never_cache
@csrf_exempt
def tregister(request):
    if request.user.is_authenticated:
        return redirect('/thome')

    if request.method == 'POST':
        # username = request.POST['username']
        username = request.POST['email']
        password = request.POST['password']
        cache.clear()
        # Check if an active user with the same email exists
        if User.objects.filter(email=username, is_active=True,is_traveller=True).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('tregister')
        cache.clear()

        # Create a user with is_active=False initially
        user = User(username=username, email=username, is_traveller=True, is_driver=False,is_active=False)
        user.set_password(password)

        try:
            user.full_clean()  # Validate the user data
            user.save()
            traveller = Traveller(user=user)
            traveller.save()
        except ValidationError as e:
            # Handle validation errors, e.g., unique constraint violations
            messages.error(request, e.messages[0])  # Display the first error message
            return redirect('tregister')

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
        messages.success(request, "A link has been sent to your registered email. Please click on it to continue.")

        return render(request, 'index.html', {'email': user.email})

    cache.clear()
    return render(request, 'tregister.html')


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
            return redirect('log')
        else:
            messages.error(request, "Invalid activation link.")
            return redirect('log')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        messages.error(request, "Invalid activation link.")
        return redirect('log')

@never_cache
@login_required(login_url='log')
def traveller_home(request):
    running_packages = TravelPackage.objects.filter(status='Running')
    if request.user.is_authenticated and hasattr(request.user, 'traveller'):
        profile = request.user.traveller  # Get or create the Traveller model instance
        return render(request, 'loginview.html', {'profile': profile, 'running_packages': running_packages})
    if request.user.is_traveller:
        profile = request.user.is_traveller  # Corrected from 'is_traveller' to 'traveller'
        return render(request, 'loginview.html', {'profile': profile, 'running_packages': running_packages})
    # If the user is not a traveler or not logged in, redirect to login
    return render(request, 'login.html')

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
        traveller = Traveller(user=user, first_name=first_name, last_name=last_name, phone_number=phone_number, country=country, gender=gender, profile_photo=profile_photo)
        traveller.save()
        traveler.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('/profile_updated')
    
    # Moved user_details definition out of the conditional block
    user_details = {
        'username': request.user.username,
        'email': request.user.email,
    }
    if request.user.is_authenticated and hasattr(request.user, 'traveller'):
        user = request.user
        profile = request.user.traveller # Get or create the Traveller model instance

        return render(request, 'update_traveler.html', {'profile': profile, 'user_details': user_details})
    if request.user.is_traveller:
        profile = request.user.is_traveller  # Corrected from 'is_traveller' to 'traveller'

        return render(request, 'update_traveler.html', {'profile': profile, 'user_details': user_details})
    return render(request, 'login.html')  # Handle the case when the user is not authenticated or not a traveler

    

@login_required(login_url='log')
def profile_updated(request):
    return render(request, 'tprofile_updated.html')

@never_cache
@login_required(login_url='log')
def viewprofile(request):
    if request.user.is_authenticated and hasattr(request.user, 'traveller'):
        profile = request.user.traveller # Get or create the Traveller model instance

        # Get user details from the Traveller model
        user_details = {
            'username': request.user.username,
            'email': request.user.email,
            }
        

        return render(request, 'viewprofileT.html', {'profile': profile, 'user_details': user_details})
    if request.user.is_traveller:
                profile = request.user.is_traveller  # Retrieve the traveler's profil # Replace 'update_traveller' with the actual URL name for your update page
                user_details = {
                    'username': request.user.username,
                    'email': request.user.email,
                    # 'first_name': request.user.first_name,
                    # 'last_name': request.user.last_name,
                    # 'phone_number': request.user.phone_number,
                    # 'country': request.user.country,
                    # 'gender': request.user.gender,
                    # 'profile_photo': Traveller.profile_photo if Traveller.profile_photo else None,
                }
                return render(request, 'viewprofileT.html', {'profile': profile, 'user_details': user_details})
    return render(request, 'login.html')  # Handle the case when the user is not authenticated or not a traveler



@login_required(login_url='log')
def update_driver(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        contact_email = request.POST['contact_email']
        contact_phone_number = request.POST['contact_phone_number']
        date_of_birth = request.POST['date_of_birth']
        location = request.POST['location']
        profile_photo = request.FILES.get('profile_photo')
        license = request.FILES.get('license')

        driver, created = Driver.objects.get_or_create(user=user)
        driver.first_name = first_name
        driver.last_name = last_name
        driver.contact_email = contact_email
        driver.contact_phone_number = contact_phone_number
        driver.date_of_birth = date_of_birth
        driver.location = location

        if profile_photo:
            driver.profile_photo = profile_photo
        
        if license:
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
    return redirect('/')


@never_cache
@login_required(login_url='log')
def admin(request):
    if request.user.is_staff:
        return render(request, 'adminreg.html')
    cache.clear()
    return redirect('/log')


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
        
        approved_users = User.objects.filter(driver__verification='approved')
        rejected_users = User.objects.filter(driver__verification='rejected')
        approved_drivers = Driver.objects.filter(verification='approved')
        rejected_drivers = Driver.objects.filter(verification='rejected')

        context = {
            'user_profiles': page,
            'user_count': user_count,
            'approved_users': approved_users,
            'rejected_users': rejected_users,
            'approved_drivers': approved_drivers,
            'rejected_drivers': rejected_drivers,
        }

        return render(request, 'drivers.html', context)
    return redirect('/log')



from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@never_cache
@login_required(login_url='log')
def update_verification_status(request, user_profile_id):
    if request.method == 'POST':
        user_profile = User.objects.get(pk=user_profile_id)
        new_status = request.POST.get('verification_status')

        if new_status in ('approved', 'rejected'):
            old_status = user_profile.driver.verification

            user_profile.driver.verification = new_status
            user_profile.driver.save()

            # Check if the verification status has changed
            if old_status != new_status:
                # Send an email notification
                subject = 'Verification Status Changed'
                message = f'Your verification status has been changed to "{new_status}".'
                from_email = 'godwinbmenachery2024a@mca.ajce.in'
                recipient_list = [user_profile.email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
    return redirect('/drivers')  # Redirect back to the user profile list view



@never_cache
@login_required(login_url='log')
def list_approved_users(request):
    # Query the User and Driver models to get approved users
    approved_users = User.objects.filter(driver__verification='approved')
    approved_drivers = Driver.objects.filter(verification='approved')

    context = {'approved_users': approved_users, 'approved_drivers': approved_drivers}

    return render(request, 'drivers.html', context)


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




# views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
# from .models import TravelPackage  # Import your TravelPackage model
from django.utils.datastructures import MultiValueDictKeyError




from .models import TravelPackage
from .models import PackageImage  # Import the PackageImage model

@never_cache
@login_required(login_url='log')
def upload_package(request):
    if request.method == "POST":
        # This block handles form submission and package creation when the form is submitted.

        # Retrieve form data from the request
        package_name = request.POST.get("package_name")
        description = request.POST.get("description")
        destination = request.POST.get("destination")
        duration = request.POST.get("duration")
        price = request.POST.get("price")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        accommodation = request.POST.get("accommodation")
        # meals = request.POST.get("meals")
        transportation = request.POST.get("transportation")
        activities = request.POST.get("activities")

        selected_inclusions = [request.POST.get(key) for key in request.POST if key.startswith("inclusions")]
        inclusions = ', '.join(selected_inclusions)

        # Process and build a comma-separated string for exclusions
        selected_exclusions = [request.POST.get(key) for key in request.POST if key.startswith("exclusions")]
        exclusions = ', '.join(selected_exclusions)

        images = request.FILES.getlist("images")  # Handle multiple uploaded images
        # ratings = request.POST.get("ratings")
        availability = request.POST.get("availability")
        booking_deadline = request.POST.get("booking_deadline")
        category = request.POST.get("category")
        tags = request.POST.get("tags")
        cancellation_policy = request.POST.get("cancellation_policy")
        # booking_link = request.POST.get("booking_link")
        status = request.POST.get("status")

        # Create a new TravelPackage object with the form data
        package = TravelPackage(
            package_name=package_name,
            description=description,
            destination=destination,
            duration=duration,
            price=price,
            start_date=start_date,
            end_date=end_date,
            accommodation=accommodation,
            # meals=meals,
            transportation=transportation,
            activities=activities,
            inclusions=inclusions,
            exclusions=exclusions,
            # ratings=ratings,
            availability=availability,
            booking_deadline=booking_deadline,
            category=category,
            tags=tags,
            cancellation_policy=cancellation_policy,
            # booking_link=booking_link,
            status=status
        )

        # Save the package to the database
        package.save()

        # Handle image uploads and save them
        for image in images:
            # Create and save an Image object for each uploaded image
            package_image = PackageImage(package=package, image=image)
            package_image.save()

        # Redirect or perform further actions as needed
        return redirect("/upload_package")  # Redirect to a package list page or any other page

    # This block handles the GET request, rendering the template for uploading a package
    return render(request, "add_package.html")



from datetime import date, timezone

@never_cache
@login_required(login_url='log')
def view_travel_packages(request):
    # Query the database to get a list of TravelPackage instances
    packages = TravelPackage.objects.all()
    search_date = request.GET.get('search_date')
    if search_date:
        try:
            search_date = date.fromisoformat(search_date)
            packages = packages.filter(start_date=search_date)
        except ValueError:
            # Handle the case when an invalid date is entered
            pass
    # Add pagination
    paginator = Paginator(packages, 10)  # Show 10 items per page
    page = request.GET.get('page')
    packages = paginator.get_page(page)

    # Render the template with the queried data and pagination context
    return render(request, 'view_package.html', {'packages': packages})


from django.shortcuts import render, redirect, get_object_or_404
@never_cache
@login_required(login_url='log')
def edit_package(request, package_id):
    # Get the TravelPackage object based on the package_id
    package = get_object_or_404(TravelPackage, pk=package_id)

    if request.method == "POST":
        # Update the TravelPackage attributes based on the form data
        package.package_name = request.POST.get('package_name')
        package.description = request.POST.get('description')
        package.destination = request.POST.get('destination')
        package.duration = int(request.POST.get('duration'))
        package.price = float(request.POST.get('price'))
        package.start_date = request.POST.get('start_date')
        package.end_date = request.POST.get('end_date')
        package.accommodation = request.POST.get('accommodation')
        package.transportation = request.POST.get('transportation')
        package.activities = request.POST.get('activities')
        package.category = request.POST.get('category')
        package.tags = request.POST.get('tags')
        package.availability = int(request.POST.get('availability'))
        package.booking_deadline = request.POST.get('booking_deadline')
        package.cancellation_policy = request.POST.get('cancellation_policy')
        package.status = request.POST.get('status')
        
        selected_inclusions = [request.POST.get(key) for key in request.POST if key.startswith("inclusions")]
        inclusions = ', '.join(selected_inclusions)
        package.inclusions = inclusions

        # Process and build a comma-separated string for exclusions
        selected_exclusions = [request.POST.get(key) for key in request.POST if key.startswith("exclusions")]
        exclusions = ', '.join(selected_exclusions)
        package.exclusions = exclusions
        # Save the updated TravelPackage
        package.save()

        return redirect('view_packages')  # Redirect to the view_packages page after editing

    # Render the edit_package template with the package data
    return render(request, 'edit_package.html', {'package': package})


def package_detail(request, package_id):
    package = get_object_or_404(TravelPackage, pk=package_id)
    from_upcoming_journeys = request.GET.get('from_upcoming_journeys')
    user= request.user
    passenger = Passenger.objects.filter(package=package, user=user).first()

    if from_upcoming_journeys:
        # If the 'from_upcoming_journeys' query parameter is present, hide the book button
        return render(request, 'package_detail.html', {'package': package, 'from_upcoming_journeys': from_upcoming_journeys})

    if request.user.is_authenticated:
        if hasattr(request.user, 'traveller'):
            profile = request.user.traveller  # Get or create the Traveller model instance
            return render(request, 'package_detail.html', {'profile': profile,'package': package,'from_upcoming_journeys': from_upcoming_journeys,'passenger':passenger})
        if request.user.is_traveller:
            profile = request.user.is_traveller  # Corrected from 'is_traveller' to 'traveller'
            return render(request, 'package_detail.html', {'profile': profile,'package': package,'from_upcoming_journeys': from_upcoming_journeys,'passenger':passenger})
    else:
        return render(request, 'package_detail.html', {'package': package,'from_upcoming_journeys': from_upcoming_journeys,'passenger':passenger})


from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Passenger

def add_passenger(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)
    if request.method == 'POST':
        user_id = request.user.id
        package_id = package_id
        passenger_name_list = request.POST.getlist('passenger_name')
        passenger_age_list = request.POST.getlist('passenger_age')
        proof_of_id_list = request.FILES.getlist('proof_of_id')
        print(passenger_name_list)

        # Check if the number of entries in all lists match
        if len(passenger_name_list) == len(passenger_age_list) == len(proof_of_id_list):
            flag = 0
            for i in range(len(passenger_name_list)):
                passenger_name = passenger_name_list[i]
                passenger_age = passenger_age_list[i]
                proof_of_id = proof_of_id_list[i]

                passenger = Passenger(
                    user_id=user_id,
                    package_id=package_id,
                    passenger_name=passenger_name,
                    passenger_age=passenger_age,
                    proof_of_id=proof_of_id
                )
                passenger.save()
                flag = 1

            if flag == 0:
                return render(request, 'passenger_info.html', {'package':package,'package_id': package_id})
            else:
                return redirect('/thome')
        else:
            # Handle the case where the number of entries in lists don't match
            messages.success(request, "Upload ID Proof of all the Passengers for Booking.")
    return render(request, 'passenger_info.html', {'package':package,'package_id': package_id})
      

from django.shortcuts import render
from .models import TravelPackage
from django.utils import timezone

def upcoming_journeys(request):
    current_date = timezone.now().date()
    user = request.user

    # Retrieve upcoming journeys for the user
    upcoming_journeys = TravelPackage.objects.filter(start_date__gt=current_date, passenger__user=user).distinct()

    # Create a dictionary to store the travel packages along with their images
    packages_with_images = []

    for journey in upcoming_journeys:
        # Retrieve images related to the travel package
        package_images = PackageImage.objects.filter(package=journey)

        # Append the travel package and its images to the dictionary
        packages_with_images.append({
            'package': journey,
            'images': package_images
        })

    return render(request, 'upcoming_journeys.html', {'packages_with_images': packages_with_images})


def history_journeys(request):
    current_date = timezone.now().date()
    user = request.user  # Assuming you are using authentication

    # Retrieve historical journeys for the user
    history_journeys = TravelPackage.objects.filter(end_date__lt=current_date, passenger__user=user).distinct()
    packages_with_images = []

    for journey in history_journeys:
        # Retrieve images related to the travel package
        package_images = PackageImage.objects.filter(package=journey)

        # Append the travel package and its images to the dictionary
        packages_with_images.append({
            'package': journey,
            'images': package_images
        })

    return render(request, 'history_journeys.html', {'packages_with_images': packages_with_images})


def ongoing_journeys(request):
    current_date = timezone.now().date()
    user = request.user  # Assuming you are using authentication

    # Retrieve historical journeys for the user
    ongoing_journeys = TravelPackage.objects.filter(start_date__lt=current_date ,end_date__gt=current_date, passenger__user=user).distinct()

    packages_with_images = []

    for journey in ongoing_journeys:
        # Retrieve images related to the travel package
        package_images = PackageImage.objects.filter(package=journey)

        # Append the travel package and its images to the dictionary
        packages_with_images.append({
            'package': journey,
            'images': package_images
        })

    return render(request, 'ongoing_journeys.html', {'packages_with_images': packages_with_images})



from django.urls import reverse

def cancel_booking(request, package_id):
    # Retrieve all passengers associated with the package and the logged-in user
    passengers = Passenger.objects.filter(package=package_id, user=request.user)

    # Check if there are passengers to cancel
    if passengers:
        # Delete all passenger records
        passengers.delete()
        messages.success(request, "Your bookings have been canceled successfully")
        return redirect(reverse('thome'))  # Redirect to 'thome' using the named URL pattern
    else:
        # Handle the case where no bookings were found
        messages.error(request, "No bookings found for cancellation")
        return redirect(reverse('error_url_name'))  # Redirect to an error page using the named URL pattern



