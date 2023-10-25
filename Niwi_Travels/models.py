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

    def _str_(self):
        return self.user.username