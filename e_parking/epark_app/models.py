from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from cloudinary.models import CloudinaryField
from .manager import CustomUserManager
from django.contrib.auth.models import User, AbstractUser
# Create your models here.
from django.db import models


class CustomUser(AbstractUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True, null=True, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, blank=False)
    address = models.TextField(max_length=250, blank=False)
    otp = models.CharField(max_length=20, blank=True, null=True)
    is_logged_in = models.BooleanField(default=False)
    display_picture = CloudinaryField('Display Picture', null=True, blank=True)
    objects = CustomUserManager()

    # Use 'phone_number' as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone_number']

    class Meta:
        db_table = 'CustomUser'


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SlotDetail(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

