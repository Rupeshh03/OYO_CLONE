from datetime import datetime

from django.shortcuts import get_object_or_404, render, redirect

from home import models
from .models import HotelBooking, HotelUser, HotelVendor, Hotel, Ameneties
from django.db.models import Q
from django.contrib import messages
from .utils import generateRandomToken, sendEmailToken, sendOtpEmail, sendVendorEmailToken, sendVendorOtpEmail
from django.contrib.auth import authenticate, login, logout
import random
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_page(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        hotel_user=HotelUser.objects.filter(
            Q(email=email) | Q(username=email)
        )
        if not hotel_user.exists():
            messages.error(request, "Invalid email or username.")
            return redirect('/account/login/')
        
        if not hotel_user[0].is_email_verified:
            messages.error(request, "Email not verified. Please check your email for the verification link.")
            return redirect('/account/login/')
        
        hotel_user=authenticate(request, username=hotel_user[0].username, password=password)
       
        if hotel_user:
            messages.success(request, "Login successful.")
            login(request, hotel_user)
            return redirect('/')
        
        messages.error(request, "Invalid password.")
        return redirect('/account/login/')
    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        # Handle form submission and user registration logic here
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        hotel_user = HotelUser.objects.filter(
            Q(email=email) | Q(username=email)
        )
        
        if hotel_user.exists():
            messages.error(request, "A user with this email or username already exists.")
            return redirect('/account/register/')
        
        hotel_user = HotelUser.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            email_token=generateRandomToken(),
        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email, hotel_user.email_token)
        messages.success(request, "Registration successful. Please check your email to verify your account.")
        return redirect('/account/register/')
        
    return render(request, 'register.html')

def verify_email(request, token):
    try:
        hotel_user = HotelUser.objects.get(email_token=token)
        hotel_user.is_email_verified = True
        hotel_user.email_token = ''
        hotel_user.save()

        messages.success(request, "Email verified successfully. You can now log in.")
        return redirect('/account/login/')
   
    except HotelUser.DoesNotExist:
        messages.error(request, "Invalid verification token.")
        return redirect('/account/login/')
    
def send_otp(request, email):
    hotel_user=HotelUser.objects.filter(
        email=email)
    if not hotel_user.exists():
        messages.warning(request, "Invalid email or username.")
        return redirect('/account/vendor-login/')
    
    otp=(random.randint(1000, 9999))
    hotel_user.update(otp=otp)
    
    sendOtpEmail(email, otp)
    return redirect(f'/account/verify-otp/{email}/')

def verify_otp(request, email):
    if request.method =='POST':
        otp=request.POST.get('otp')
        hotel_user=HotelUser.objects.get(
            email=email)

        if otp == hotel_user.otp:
            messages.success(request, "login Success")
            login(request, hotel_user)
            return redirect('/account/login/')
        if len(otp) != 4:
            messages.warning(request, "OTP must be 4 digits")
            return redirect(f'/account/verify-otp/{email}/')
            
        
        messages.warning(request, "Invalid OTP")
        return redirect(f'/account/verify-otp/{email}/')
    return render(request, 'verify_otp.html')
 
# -------------------Vendor Views------------------#

def login_vendor(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        hotel_user=HotelVendor.objects.filter(
            Q(email=email) | Q(username=email)
        )
        if not hotel_user.exists():
            messages.error(request, "Invalid email or username.")
            return redirect('/account/vendor-login/')
        
        if not hotel_user[0].is_email_verified:
            messages.error(request, "Email not verified. Please check your email for the verification link.")
            return redirect('/account/vendor-login/')
        
        hotel_user=authenticate(request, username=hotel_user[0].username, password=password)
       
        if hotel_user:
            messages.success(request, "Login successful.")
            login(request, hotel_user)
            return redirect('/account/dashboard/')
        
        messages.error(request, "Invalid password.")
        return redirect('/account/vendor-login/')
    return render(request, 'vendor/login_vendor.html')

def register_vendor(request):
    if request.method == 'POST':
        # Handle form submission and user registration logic here
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        hotel_user = HotelVendor.objects.filter(
            Q(email=email) | Q(username=email)
        )
        
        if hotel_user.exists():
            messages.error(request, "A user with this email or username already exists.")
            return redirect('/account/vendor-register/')
        
        hotel_user = HotelVendor.objects.create(
            username=email,
            business_name=business_name,
            email=email,
            first_name=first_name,
            last_name=last_name,
            email_token=generateRandomToken(),
        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendVendorEmailToken(email, hotel_user.email_token)
        messages.success(request, "Registration successful. Please check your email to verify your account.")
        return redirect('/account/vendor-register/')
        
    return render(request, 'vendor/register_vendor.html')

def verify_vendor_email(request, token):
    try:
        hotel_user = HotelVendor.objects.get(email_token=token)
        hotel_user.is_email_verified = True
        hotel_user.email_token = ''
        hotel_user.save()

        messages.success(request, "Email verified successfully. You can now log in.")
        return redirect('/account/vendor-login/')
   
    except HotelVendor.DoesNotExist:
        messages.error(request, "Invalid verification token.")
        return redirect('/account/vendor-login/')

   
def send_vendor_otp(request, email):
    hotel_user=HotelVendor.objects.filter(
        email=email)
    if not hotel_user.exists():
        messages.warning(request, "Invalid email or username.")
        return redirect('/account/vendor-login/')
    
    otp=(random.randint(1000, 9999))
    hotel_user.update(otp=otp)
    
    sendVendorOtpEmail(email, otp)
    return redirect(f'/account/vendor-verify-otp/{email}/')


def verify_vendor_otp(request, email):
    if request.method =='POST':
        otp=request.POST.get('otp')
        hotel_user=HotelVendor.objects.get(
            email=email)

        if otp == hotel_user.otp:
            messages.success(request, "login Success")
            login(request, hotel_user)
            return redirect('/account/dashboard/')
        if len(otp) != 4:
            messages.warning(request, "OTP must be 4 digits")
            return redirect(f'/account/verify-otp/{email}/')
            
        
        messages.warning(request, "Invalid OTP")
        return redirect(f'/account/vendor-verify-otp/{email}/')
    return render(request, 'vendor/verify_Vendor_otp.html')

@login_required(login_url='vendor_login')
def dashboard(request):
    context={'hotels':Hotel.objects.filter(hotel_owner__username=request.user.username)}
    return render(request, 'vendor/vendor_dashboard.html', context)

@login_required(login_url='vendor_login')
def add_hotel(request):
    if request.method == 'POST':
        hotel_name=request.POST.get('hotel_name')
        hotel_image=request.FILES.get('hotel_image')
        hotel_description=request.POST.get('hotel_description')
        hotel_location= request.POST.get('hotel_location')
        hotel_price=request.POST.get('hotel_price')
        hotel_ameneties= request.POST.getlist('hotel_ameneties')
        hotel_offer_price=request.POST.get('hotel_offer_price')
        is_available=request.POST.get('is_available') == 'on'
        
        try:
            hotel_vendor = HotelVendor.objects.get(username=request.user.username)
        except HotelVendor.DoesNotExist:
            messages.error(request, "You are not registered as a vendor.")
            return redirect('/account/vendor-login/')
        
        hotel=Hotel.objects.create(
            hotel_name=hotel_name,
            hotel_image=hotel_image,
            hotel_description=hotel_description,
            hotel_location=hotel_location,
            hotel_price=hotel_price,
            hotel_owner=hotel_vendor,
            hotel_offer_price=hotel_offer_price,
            is_available=is_available,
        )
        for ameneti in hotel_ameneties:
            ameneti_obj=Ameneties.objects.get(id=ameneti)
            hotel.hotel_ameneties.add(ameneti_obj)
            

        messages.success(request, "Hotel added successfully.")
        return redirect('/account/add-hotel/')
    
    ameneties=Ameneties.objects.all()
    return render(request, 'vendor/add_hotel.html', context={'ameneties': ameneties})

@login_required(login_url='vendor_login')
def edit_hotel(request, id):

    hotel = Hotel.objects.get(id=id)

    if request.method == 'POST':

        hotel.hotel_name = request.POST.get('hotel_name')
        hotel.hotel_description = request.POST.get('hotel_description')
        hotel.hotel_location = request.POST.get('hotel_location')
        hotel.hotel_price = request.POST.get('hotel_price')
        hotel.hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel.is_available = request.POST.get('is_available') == 'on'

        # Image update only if uploaded
        if request.FILES.get('hotel_image'):
            hotel.hotel_image = request.FILES.get('hotel_image')

        hotel.save()

        # Update amenities
        hotel_ameneties = request.POST.getlist('hotel_ameneties')
        hotel.hotel_ameneties.clear()

        for ameneti in hotel_ameneties:
            ameneti_obj = Ameneties.objects.get(id=ameneti)
            hotel.hotel_ameneties.add(ameneti_obj)

        messages.success(request, "Hotel updated successfully.")
        return redirect('/account/dashboard/')

    ameneties = Ameneties.objects.all()

    return render(request, 'vendor/edit_hotel.html',
                  {'ameneties': ameneties, 'hotel': hotel})

@login_required(login_url='vendor_login')
def delete_hotel(request, id):

    hotel = Hotel.objects.get(id=id)
    hotel.delete()

    messages.success(request, "Hotel deleted successfully")
    return redirect('/account/dashboard/')

def logout_vendor(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('/account/vendor-login/')


@login_required(login_url='login')
def book_hotel(request, hotel_id):

    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == "POST":

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Date validation
        if start_date >= end_date:
            messages.warning(request, "Check-out date must be after check-in date.")
            return redirect('book_hotel', hotel_id=hotel.id)

        # Check booking conflict
        already_booked = HotelBooking.objects.filter(
            hotel=hotel,
            booking_start_date__lte=end_date,
            booking_end_date__gte=start_date,
            booking_status = 'confirmed'
        
        ).exists()

        if already_booked:
            messages.warning(request, "Hotel already booked for these dates.")
            return redirect('book_hotel', hotel_id=hotel.id)

        # Price calculation
        price_per_day = hotel.hotel_offer_price if hotel.hotel_offer_price else hotel.hotel_price
        days = (end_date - start_date).days
        total_price = price_per_day * days

        HotelBooking.objects.create(
            hotel=hotel,
            booking_user=request.user,
            booking_start_date=start_date,
            booking_end_date=end_date,
            price=total_price,
            booking_status='confirmed'
        )

        messages.success(request, "Hotel booked successfully.")
        return redirect('my_bookings')

    return render(request, 'book_hotel.html', {'hotel': hotel})

@login_required(login_url='login')
def my_bookings(request): 
    bookings = HotelBooking.objects.filter(booking_user=request.user)

    return render(request, 'my_bookings.html', {
        'bookings': bookings
    })



@login_required(login_url='login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(HotelBooking, id=booking_id, booking_user=request.user)
    booking.booking_status = 'cancelled'
    booking.save()

    messages.success(request, "Booking cancelled successfully.")
    return redirect('my_bookings')

@login_required(login_url='vendor_login')
def hotel_bookings(request):

    bookings = HotelBooking.objects.filter(hotel__hotel_owner=request.user)
    return render(request, 'vendor/hotel_bookings.html', {'bookings': bookings})