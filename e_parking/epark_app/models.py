from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from cloudinary.models import CloudinaryField
from .manager import CustomUserManager
from django.contrib.auth.models import User, AbstractUser
# Create your models here.
from django.db import models



class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.CharField(max_length=255)
    image =  CloudinaryField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'location'

class CustomUser(AbstractUser, PermissionsMixin):
    VEHICLE_CHOICES = [
        ('2_wheeler', '2 Wheeler'),
        ('4_wheeler', '4 Wheeler'),
        ('Truck', 'Truck'),
        ('Bus', 'Bus'),
        ('Heavy Vehicle', 'Heavy Vehicle')

        # Add more choices as needed
    ]

    phone_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True, null=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    address = models.TextField(max_length=250, blank=False)
    otp = models.CharField(max_length=20, blank=True, null=True)
    is_logged_in = models.BooleanField(default=False)
    display_picture = CloudinaryField('Display Picture', null=True, blank=True)
    vehicle_type = models.CharField(max_length=20,choices=VEHICLE_CHOICES,default='2_wheeler')
    parking_lot_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    objects = CustomUserManager()

    # Use 'phone_number' as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        db_table = 'customuser'




class SlotDetail(models.Model):
    name = models.CharField(max_length=50, unique=True)
    opening_hours = models.CharField(max_length=100,default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    slot_variants = models.ManyToManyField('SlotDetailVariant', blank=True)

    def __str__(self):
            return self.name

    class Meta:
        db_table = 'slotdetail'


class SlotDetailVariant(models.Model):
    VEHICLE_CHOICES = [
        ('2_wheeler', '2 Wheeler'),
        ('4_wheeler', '4 Wheeler'),
        ('Truck', 'Truck'),
        ('Bus', 'Bus'),
        ('Heavy Vehicle', 'Heavy Vehicle')

        # Add more choices as needed
    ]
    slot = models.ForeignKey(SlotDetail, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(default=0)  # Total capacity of the parking slot
    available_slots = models.PositiveIntegerField(default=0)  # Number of available spots
    vehicle_type = models.CharField(max_length=20,choices=VEHICLE_CHOICES,default='2_wheeler')
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2,default=0.00)

    def __str__(self):
        return f"{self.slot.name}"

    class Meta:
        db_table = 'slotdetailvariant'
        verbose_name_plural = 'Slot Detail Variants'


class SlotBooking(models.Model):
    VEHICLE_CHOICES = [
        ('2_wheeler', '2 Wheeler'),
        ('4_wheeler', '4 Wheeler'),
        ('Truck', 'Truck'),
        ('Bus', 'Bus'),
        ('Heavy Vehicle', 'Heavy Vehicle')

        # Add more choices as needed
    ]
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    slot = models.ForeignKey(SlotDetail, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    vehicle_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES, default='2_wheeler')
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    def __str__(self):
        return f"{self.slot.name}"


    class Meta:
        db_table = 'slotbooking'

