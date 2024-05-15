from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.forms.widgets import DateInput
from decimal import Decimal
import csv


class Activity(models.TextChoices):
    SKIING_SNOWBOARDING = 'Skiing/Snowboarding', 'Skiing/Snowboarding'
    HIKING = 'Hiking', 'Hiking'
    ALL_INCLUSIVE_RESORTS = 'All-inclusive resorts', 'All-inclusive resorts'
    EXCURSIONS = 'Excursions', 'Excursions'
    BOAT_TOURS = 'Boat tours', 'Boat tours'
    WINE_TASTING_BREWERY_TOURS = 'Wine-tasting/Brewery tours', 'Wine-tasting/Brewery tours'
    
    POOL = 'Pool', 'Pool'
    HIKES = 'Hikes', 'Hikes'
    BOARD_GAMES = 'Board games', 'Board games'
    BEACH = 'Beach', 'Beach'
    TRIVIA_NIGHTS = 'Trivia nights', 'Trivia nights'
    BOWLING = 'Bowling', 'Bowling'
    
    CAMPING = 'Camping', 'Camping'
    SPA = 'Spa', 'Spa'
    MUSEUM_VISITS = 'Museum visits', 'Museum visits'
    MINIGOLF = 'Minigolf', 'Minigolf'

csv_file_path = 'travelwebsite/airports.csv'
data = dict() #(code:name)

# Read the CSV file and extract data from the desired columns
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        airport_name = row['Goroka Airport']  # Replace 'airport_name' with the actual column name for airport names
        airport_code = row['GKA']  # Replace 'airport_code' with the actual column name for airport codes
        data[airport_code] = airport_name


class Trip(models.Model):
    person          = models.ForeignKey(User, on_delete=models.PROTECT, related_name="entry_creator")
    # itinerary       = models.ForeignKey(Itinerary, on_delete=models.PROTECT, related_name="itinerary")
    flights         = models.CharField(max_length=200)
    flights_url     = models.TextField(default='https://www.google.com/travel/flights')
    start_date      = models.DateField()
    end_date        = models.DateField()
    origin_airport = models.CharField(max_length=3, choices=data.items(), default='EWR')
    destination_airport = models.CharField(max_length=3, choices=data.items(), default='EWR')

    location       = models.CharField(max_length=200)
    people_followers = models.ManyToManyField(User, related_name="people_followers")
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    # updated_by    = models.ForeignKey(User, on_delete=models.PROTECT, related_name="trip_updators")
    # update_time   = models.DateTimeField()

class Itinerary(models.Model):
    activity_type = models.CharField(max_length=50, choices=Activity.choices, default=Activity.SKIING_SNOWBOARDING)
    start_time = models.TimeField()
    end_time = models.TimeField()
    cost = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    date = models.DateField()
    trip        = models.ForeignKey(Trip, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return f"Entry(id={self.id})"

class Profile(models.Model):
    user          = models.OneToOneField(User, on_delete=models.PROTECT)
    trips     = models.ManyToManyField(Trip, related_name="followers")
    # picture       = models.FileField(blank=True)
    # content_type  = models.CharField(blank=True, max_length=50)

    def __str__(self):
        try:
            first_name = self.user.first_name
            last_name = self.user.last_name
        except ObjectDoesNotExist:
            print("Either the blog or entry doesn't exist.")

        return f"profile {first_name}, {last_name}"
