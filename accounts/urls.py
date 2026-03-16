from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('send-otp/<email>/', views.send_otp, name='send_otp'),
    path('verify-otp/<email>/', views.verify_otp, name='verify_otp'),
    path('verify-account/<str:token>/', views.verify_email, name='verify_email'),

    path('vendor-login/', views.login_vendor, name='vendor_login'),
    path('vendor-register/', views.register_vendor, name='vendor_register'),
    path('vendor-verify-otp/<email>/', views.verify_vendor_otp, name='vendor_verify_otp'),
    path('vendor-send-otp/<email>/', views.send_vendor_otp, name='vendor_send_otp'),
    path('vendor-verify-account/<str:token>/', views.verify_vendor_email, name='vendor_verify_email'),
    path('vendor-logout/', views.logout_vendor, name='vendor_logout'),

    path('add-hotel/', views.add_hotel, name='add_hotel'),   
    path('dashboard/', views.dashboard, name='vendor_dashboard'),    

    path('edit-hotel/<int:id>/', views.edit_hotel, name='edit_hotel'),
    path('delete-hotel/<int:id>/', views.delete_hotel, name='delete_hotel'),

    path('book-hotel/<int:hotel_id>/', views.book_hotel, name='book_hotel'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('hotel-bookings/', views.hotel_bookings, name='hotel_bookings'),

]  