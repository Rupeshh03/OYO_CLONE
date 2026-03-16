from django.db import models
from django.contrib.auth.models import User
from .utils import generateSlug
# Create your models here.

class HotelUser(User):
    profile_picture=models.ImageField(upload_to='profile', null=True, blank=True)
    phone_number=models.CharField(max_length=10, null=True, blank=True)
    email_token=models.CharField(max_length=100, null=True, blank=True)
    otp=models.CharField(max_length=6, null=True, blank=True)
    is_email_verified=models.BooleanField(default=False)
    class Meta:
        db_table = 'hotel_user'
        verbose_name = 'Hotel User'

class HotelVendor(User):
    profile_picture=models.ImageField(upload_to='profile', null=True, blank=True)
    phone_number=models.CharField(max_length=10, null=True, blank=True)
    business_name=models.CharField(max_length=1000, null=True, blank=True)
    email_token=models.CharField(max_length=100, null=True, blank=True)
    otp=models.CharField(max_length=6, null=True, blank=True)
    is_email_verified=models.BooleanField(default=False)
    class Meta:
        db_table = 'hotel_vendor'
        verbose_name = 'Hotel Vendor'

class Ameneties(models.Model):
    amenetie_name=models.CharField(max_length=1000)
    icon=models.ImageField(upload_to='hotels/amenities/', null=True, blank=True)

    def __str__(self) -> str:
        return self.amenetie_name

class Hotel(models.Model):
    hotel_name=models.CharField(max_length=1000)
    hotel_image=models.ImageField(upload_to='hotels', null=True, blank=True)
    hotel_description=models.TextField()
    hotel_location=models.CharField(max_length=1000)
    hotel_price=models.FloatField()
    hotel_ameneties=models.ManyToManyField(Ameneties)
    hotel_slug=models.SlugField(max_length=1000, unique=True)
    hotel_owner=models.ForeignKey(HotelVendor, on_delete=models.CASCADE)
    hotel_offer_price=models.FloatField(null=True, blank=True)
    is_available=models.BooleanField(default=True)

    class Meta:
        db_table = 'hotel'
        verbose_name = 'Hotel'
    def __str__(self) -> str:
        return self.hotel_name

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
           self.hotel_slug=generateSlug(self.hotel_name)

        return super().save(*args, **kwargs)

class HotelImages(models.Model):
    hotel=models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image=models.ImageField(upload_to='hotels', null=True, blank=True)

class HotelManager(models.Model):
    hotel=models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='managers')
    manager_name=models.CharField(max_length=1000)
    manger_contact=models.CharField(max_length=10)

class HotelBooking(models.Model):
    hotel=models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    booking_user=models.ForeignKey(User, on_delete=models.CASCADE)
    booking_start_date=models.DateField()
    booking_end_date=models.DateField()
    price=models.FloatField()
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
]

    booking_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'hotel_booking'
        verbose_name = 'Hotel Booking'

    def __str__(self):
        return f"{self.hotel.hotel_name} - {self.booking_user.username}"