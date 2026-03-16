from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),    
    path('logout/', views.logout_page, name='logout'),
    path('hotel/<int:id>/', views.hotel_detail, name='hotel_detail'),
    path('search/', views.search_hotels, name='search_hotels'),
]