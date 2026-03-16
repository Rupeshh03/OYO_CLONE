import random
from random import choice
from faker import Faker

from django.contrib.auth.models import User
from accounts.models import Hotel, HotelVendor, Ameneties

fake = Faker()


def createUser():

    for i in range(10):

        User.objects.create_user(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            username=fake.user_name(),
            email=fake.email(),
            password="password123"
        )


def createHotel():

    vendors = HotelVendor.objects.all()

    if not vendors.exists():
        print("No vendors found. Create vendor first.")
        return

    for i in range(20):

        vendor = choice(vendors)

        hotel = Hotel.objects.create(
            hotel_name=fake.company(),
            hotel_description=fake.text(),
            hotel_slug=fake.slug() + str(random.randint(1000,9999)),
            hotel_offer_price=random.randint(800,1500),
            hotel_price=random.randint(2000,5000),
            hotel_location=fake.city(),
            hotel_owner=vendor,
            is_available=fake.boolean()
        )

        hotel.hotel_ameneties.set(Ameneties.objects.all())

    print("Fake hotels created successfully")