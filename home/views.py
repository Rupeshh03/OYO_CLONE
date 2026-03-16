from pyexpat.errors import messages
from django.shortcuts import redirect, render
from accounts.models import *
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views.decorators.cache import cache_page

# Create your views here.
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator

@cache_page(60 * 5)
def home(request):

    hotel_list = Hotel.objects.prefetch_related('hotel_ameneties').all()

    paginator = Paginator(hotel_list, 8)   # 1 page me 8 hotels

    page_number = request.GET.get('page')

    hotels = paginator.get_page(page_number)

    context = {
        'hotels': hotels
    }

    return render(request, 'utils/home.html', context)

def login_page(request):
    return render(request, 'utils/login.html')

def register_page(request):
    return render(request, 'utils/register.html')

def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('/')

def hotel_detail(request, id):
    hotel=Hotel.objects.get(id=id)
    context={'hotel':hotel}
    return render(request, 'utils/hotel_detail.html', context)

def search_hotels(request):
    hotels=Hotel.objects.filter(name__icontains=request.GET.get('query'))
    context={'hotels':hotels}
    return render(request, 'utils/home.html', context)

