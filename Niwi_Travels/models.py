from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_traveller = models.BooleanField(default=True)
    is_driver = models.BooleanField(default=False)
    
    def _str_(self):
         return f"{self.username} ({'Traveller' if self.is_traveller else 'Driver'})"

class Traveller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='traveller')
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    phone_number = models.CharField(max_length=15, null=True)
    country = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=10, null=True)
    profile_photo = models.ImageField(blank=True, null=True, upload_to='traveller_profile_photos/')

    def _str_(self):
        return self.user.username
    
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='driver')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact_email = models.EmailField(max_length=254)
    contact_phone_number = models.CharField(max_length=15)
    profile_photo = models.ImageField(blank=True, null=True, upload_to='driver_profile_photos/')
    verification = models.CharField(max_length=20, default='Pending')
    admin_notes = models.TextField(blank=True, null=True)
    license = models.FileField(blank=True, null=True, upload_to='college_pdf_copies/')
    date_of_birth = models.DateField(null=True, blank=True)  # Add date_of_birth field
    location = models.CharField(max_length=100, null=True, blank=True)  # Add location field

    def _str_(self):
        return self.user.username
    




class TravelPackage(models.Model):
    STATUS_CHOICES = (
        ('Running', 'Running'),
        ('Paused', 'Paused'),
    )
    ACCOMMODATION_CHOICES = (
        ('Included', 'Included'),
        ('Excluded', 'Excluded'),
    )
    FEED_CHOICES = (
        ('Save', 'Save'),
        ('Post', 'Post'),
    )

    package_name = models.CharField(max_length=100)
    description = models.TextField()
    destination = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    accommodation = models.CharField(max_length=100, choices=ACCOMMODATION_CHOICES,default='Included')
    # meals = models.CharField(max_length=100)
    transportation = models.CharField(max_length=100)
    activities = models.TextField()
    inclusions = models.TextField()
    exclusions = models.TextField()
    images = models.ImageField(upload_to='package_images/')
    # ratings = models.FloatField()
    availability = models.PositiveIntegerField()
    booking_deadline = models.DateField()
    category = models.CharField(max_length=50)
    tags = models.CharField(max_length=100)
    cancellation_policy = models.TextField()
    # booking_link = models.URLField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    feed = models.CharField(max_length=10, choices=FEED_CHOICES, default='Save')


    def __str__(self):
        return self.package_name

class PackageImage(models.Model):
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE)  # Assuming TravelPackage is your package model
    image = models.ImageField(upload_to='package_images/')

    def __str__(self):
        return f"Image for {self.package.package_name}"
    

class Passenger(models.Model):
    passenger_name = models.CharField(max_length=100)
    passenger_age = models.PositiveIntegerField()
    proof_of_id = models.FileField(upload_to='passenger_ids/')
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE)  # Assuming TravelPackage is your package model
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate each passenger with a user

    def __str__(self):
        return self.passenger_name
    


from django.utils import timezone
class Booking(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    passenger_limit = models.IntegerField(default=1)  # Adjust default value as needed
    
    # Fields related to payment
    # total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # payment_method = models.CharField(max_length=50)
    # payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    # payment_date = models.DateTimeField(blank=True, null=True)
    
    # Add other common fields for your Booking model

    def __str__(self):
        return f'Booking ID: {self.id}, User: {self.user}, Package: {self.package}, Status: {self.status}'
    
class Payment(models.Model):
    booking=models.ForeignKey(Booking, on_delete=models.CASCADE, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id=models.CharField(max_length=100, blank=True, null=True)
    razor_pay_payment_id=models.CharField(max_length=100, blank=True, null=True)
    razor_pay_payment_signature=models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the payment to a customer
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Store the payment amount
    payment_date = models.DateTimeField(auto_now_add=True)  # Date and time of the payment
    # Add other fields as per your requirements, like payment status, transaction ID, etc.
    
    def __str__(self):
        return f"Payment of {self.amount} by {self.customer.username} on {self.payment_date}"