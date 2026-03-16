from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(HotelUser)
admin.site.register(HotelVendor)
admin.site.register(Ameneties)
admin.site.register(Hotel)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'booking_user', 'booking_start_date', 'booking_end_date', 'price', 'booking_status']
    list_filter = ['booking_status', 'booking_start_date']
    search_fields = ['hotel__hotel_name', 'booking_user__username']

admin.site.register(HotelBooking, HotelBookingAdmin)
