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
    asset_id = models.IntegerField(unique=True)
    asset_name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    asset_category = models.CharField(max_length=50)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    
    def __str__(self):

        return self.asset_name
    
    
    
class Exit(models.Model):
    asset_id = models.IntegerField(unique=True)
    asset_name = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    time_log = models.DateTimeField(auto_now=True)
    
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
    
    def save(self, *args, **kwargs):
        if not self.pk: 
            last_instance = self.__class__.objects.last()
            if last_instance:
                self.sr = last_instance.sr + 1
            else:
                self.sr = 1
        super().save(*args, **kwargs)


class timeschedule(models.Model):
    group = models.CharField(max_length=100)
    active_time = models.CharField(max_length=50)
    inactive_time = models.CharField(max_length=50)

    def __str__(self):
        return self.group
    

class Upload_File(models.Model):
    #uploaded_file = models.FileField(upload_to='uploads/') # it takes all files 
    uploaded_file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpeg', 'jpg'])])


class Turnstile_S(models.Model):
    sr_no = models.AutoField(primary_key=True,unique=True)
    turnstile_id = models.IntegerField(unique=True)
    location = models.CharField(max_length=100)
    safety_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return str(self.turnstile_id)
    
    def save(self, *args, **kwargs):
        if not self.pk: 
            last_instance = self.__class__.objects.last()
            if last_instance:
                self.sr_no = last_instance.sr_no + 1
            else:
                self.sr_no = 1
        super().save(*args, **kwargs)
