from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.urls import reverse
from django.core.validators import FileExtensionValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username field must be set")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50,unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.username

class UserEnrolled(models.Model):
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100, choices=[
        ('role1', 'Role 1'),
        ('role2', 'Role 2'),
    ])
    mycompany_id = models.IntegerField(unique=True)
    tag_id = models.IntegerField(unique=True)
    job_location = models.CharField(max_length=100)
    orientation = models.FileField(upload_to='attachments/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpeg', 'jpg'])])
    status = models.CharField(max_length=10, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ])
    
    def __str__(self):
        return self.name
    

class Notification(models.Model):
    subject = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.subject


class Upload_data(models.Model):
    #uploaded_file = models.FileField(upload_to='uploads/') # it takes all files 
    uploaded_file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpeg', 'jpg'])])
  
    def __str__(self):
        return str(self.uploaded_file)
    

class Site_management(models.Model):
    link_field = models.URLField(max_length=200) 


class Asset(models.Model):
    asset_name = models.CharField(max_length=255)
    asset_id = models.IntegerField(unique=True)
    description = models.CharField(max_length=500)
    asset_category = models.CharField(max_length=250)
    
    def __str__(self):
        return self.asset_name
    
class Exit(models.Model):
    asset_id = models.IntegerField(unique=True)
    asset_name = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    time_log = models.CharField(max_length=10)
    
    def __str__(self):
        return self.asset_name
    

class check_changes(models.Model):
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now=True) 
   

class Site(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class company(models.Model):
    sr = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=100)
    works = models.CharField(max_length=100)
    safety_insurance = models.FileField(upload_to='attachments/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpeg', 'jpg'])])
    insurance_expiry = models.DateField()

    def __str__(self):
        return self.name


class timeschedule(models.Model):
    group = models.CharField(max_length=100)
    active_time = models.CharField(max_length=50)
    inactive_time = models.CharField(max_length=50)

    def __str__(self):
        return self.group
    

class Upload_File(models.Model):
    #uploaded_file = models.FileField(upload_to='uploads/') # it takes all files 
    uploaded_file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpeg', 'jpg'])])


import matplotlib.pyplot as plt
import os
from django.conf import settings
from django.shortcuts import render
from .models import UserEnrolled  # Import the UserEnrolled model

def report_view(request):
    try:
        # Retrieve counts of active and inactive users
        active_users = UserEnrolled.objects.filter(status='active').count()
        inactive_users = UserEnrolled.objects.filter(status='inactive').count()

        # Prepare data for the pie chart
        labels = ['Active', 'Inactive']
        sizes = [active_users, inactive_users]
        colors = ['lightgreen', 'lightcoral']

        # Plot the pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title('User Status')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save the pie chart as an image file
        chart_path = os.path.join(settings.MEDIA_ROOT, 'pie_chart.png')
        plt.savefig(chart_path)

        # Render the template with the chart path
        return render(request, 'app1/report.html', {'chart_path': chart_path})
    except Exception as e:
        # Log any exceptions that occur
        print(f"An error occurred: {e}")
        # Render a generic error page or handle the error as needed
        return render(request, 'app1/error.html', {'error_message': str(e)})
