import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify


def generateRandomToken():
    return str(uuid.uuid4())

def sendEmailToken(email, token):
    # Implement your email sending logic here
    subject = 'Email Verification'
    message = f'''Please use the following token to verify your email: 
    http://127.0.0.1:8000/account/verify-account/{token}'''
    
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False,)

def sendOtpEmail(email, otp):
    # Implement your email sending logic here
    subject = 'OTP for Login'
    message = f'''Hi use this OTP to login: {otp} '''
    
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False,)

# -------------------Vendor Utils------------------#

def sendVendorEmailToken(email, token):
    # Implement your email sending logic here
    subject = 'Email Verification'
    message = f'''Please use the following token to verify your email: 
    http://127.0.0.1:8000/account/vendor-verify-account/{token}'''
    
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False,)

def sendVendorOtpEmail(email, otp):
    # Implement your email sending logic here
    subject = 'OTP for Login'
    message = f'''Hi use this OTP to login: {otp} '''
    
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False,)

def generateSlug(hotel_name):
    from .models import Hotel
    slug=slugify(hotel_name)+'-'+str(uuid.uuid4())[:8]
    if Hotel.objects.filter(hotel_slug=slug).exists():
        return generateSlug(hotel_name)
    return slug