from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpResponse, Http404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone

from travelwebsite.forms import LoginForm, RegisterForm, TripForm, EditForm, ActivityForm

from travelwebsite.MyMemoryList import MyMemoryList
from travelwebsite.models import Trip, Profile, Itinerary, Activity

import json
from datetime import datetime, date

from serpapi import GoogleSearch

ENTRY_LIST = MyMemoryList()

def get_flight(request):
    params = {
        "engine": "google_flights",
        "departure_id": request.POST['origin_airport'],
        "arrival_id": request.POST['destination_airport'],
        "outbound_date": request.POST['start_date'],
        "return_date": request.POST['end_date'],
        "currency": "USD",
        "stops": 1,
        "type": 1,
        "hl": "en",
        "api_key": google_api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    flight = ""
    flight_url = "https://www.google.com/travel/flights"
    print("results", results)
    if 'error' in results.keys():
        flight = results['error']
        #flight_url = ""
    else:
        flight=results['other_flights'][0]['flights'][0]['flight_number']
        flight_url = results['search_metadata']['google_flights_url']
    print("get_flight", flight, flight_url)
    return flight, flight_url


google_api_key = "5d654e352963466af5f6f701442a732f94debbbff33f1d95326d8cde4976c9b0"

def login_action(request):
    if request.user.is_authenticated:
        return my_profile(request)
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'travelwebsite/calendar-19/calendar-19/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'travelwebsite/calendar-19/calendar-19/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('my_profile'))

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'travelwebsite/calendar-19/calendar-19/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'travelwebsite/calendar-19/calendar-19/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_profile = Profile.objects.create(
        user=new_user
    )
    new_profile.save()
    print(Profile.objects.all())

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('my_profile'))


@login_required
def my_profile(request):
    profile = get_object_or_404(Profile, user=request.user.id)
    #print("profile", profile)
    assert(profile.user.id == profile.id == request.user.id)
    #print(profile.user)
    
    #form = TripForm(initial={})
    
    if request.method == "GET":
        context = {'trip_form': TripForm(), 
                   'profile': profile}
        print("get context", context)
        return render(request, 'travelwebsite/calendar-19/calendar-19/myprofile.html', context)
    
    #return render(request, 'travelwebsite/myprofile.html', context)
    form = TripForm(request.POST)
    print("request.POST", request.POST)
    if not request.user.is_authenticated:
        print("not user")
        return render(request, 'travelwebsite/calendar-19/calendar-19/myprofile.html', {'error': "You must be logged in to add a trip!", 'trip_form': TripForm(), 'profile': profile})
    
    start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()
    current_date = date.today()

    if request.POST['start_date'] > request.POST['end_date']:
        return render(request, 'travelwebsite/calendar-19/calendar-19/myprofile.html', {'error': "Start date must be before end date!", 'trip_form': TripForm(), 'profile': profile})
    
    if start_date < current_date:
        return render(request, 'travelwebsite/calendar-19/calendar-19/myprofile.html', {'error': "Start date must be on or after the current date!", 'trip_form': TripForm(), 'profile': profile})

    if end_date < current_date:
        return render(request, 'travelwebsite/calendar-19/calendar-19/myprofile.html', {'error': "End date must be after the current date!", 'trip_form': TripForm(), 'profile': profile})
    
    # params = {
    #     "engine": "google_flights",
    #     "departure_id": request.POST['origin_airport'],
    #     "arrival_id": request.POST['destination_airport'],
    #     "outbound_date": request.POST['start_date'],
    #     "return_date": request.POST['end_date'],
    #     "currency": "USD",
    #     "stops": 1,
    #     "type": 1,
    #     "hl": "en",
    #     "api_key": google_api_key
    # }

    # search = GoogleSearch(params)
    # results = search.get_dict()
    # flight = ""
    # print("results my_profile", results)
    # if 'error' in results.keys():
    #     flight = results['error']
    # else:
    #     flight=results.other_flights[0].flights[0]['flight_number'] ## TODO: get the flight from t
    flight, flight_url = get_flight(request)
    print("?????????????????????? request.POST", request.POST)
    new_trip = Trip(person = request.user, 
                    start_date=request.POST['start_date'], 
                    end_date=request.POST['end_date'],
                    location=request.POST['location'],
                    cost=request.POST['cost'], 
                    origin_airport=request.POST['origin_airport'], 
                    destination_airport=request.POST['destination_airport'],
                    flights=flight,
                    flights_url = flight_url)
    new_trip.save()
    print("new trip, username", request.user.id)
    new_trip.people_followers.add(request.user.id)
    new_trip.save()
    print(new_trip.people_followers)
    profile.trips.add(new_trip)
    profile.save()

    context = {'trip_form': TripForm(), 
               'profile': profile}
    # return render(request, 'travelwebsite/myprofile.html', context)
    return redirect(f'trip/{new_trip.id}') # rhea change

# @login_required
def get_photo(request, id):
    item = get_object_or_404(Profile, user=id)
    if not item.picture:
        raise Http404

#     return HttpResponse(item.picture, content_type=item.content_type)

def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)

@login_required
def show_trips(request, id, errors=[]):
    print("show trips")
    if not request.user.is_authenticated:
        return render(request, 'travelwebsite/calendar-19/calendar-19/myprofile.html', {'error': "You must be logged in to add an activity!", 'link': 'login'})
    
    tripObj = get_object_or_404(Trip, id=id)
    if request.user not in tripObj.people_followers.all():
        return render(request, 'travelwebsite/calendar-19/calendar-19/error.html', {'error': "You can't access this trip. Please return to your profile page", 'link': 'my_profile'})

    print("-------------- tripObj", tripObj)
    print("show trips flights", tripObj.flights)
    activities = []
    for iti in Itinerary.objects.all():
        # print(iti.trip.id)
        if id == iti.trip.id:
            # print('here')
            activities.append(iti)

    return render(request, 'travelwebsite/calendar-19/calendar-19/trip.html', {'trip_id': id, 'trip_form': EditForm(initial={'id': tripObj.id,
            'person': tripObj.person,
            'flights': tripObj.flights,
            'start_date': tripObj.start_date,
            'end_date': tripObj.end_date,
            'origin_airport': tripObj.origin_airport,
            'destination_airport': tripObj.destination_airport,
            'location': tripObj.location,
            'itinerary': activities,
            'errors': errors,
            'cost': tripObj.cost}), 'activity_form': ActivityForm(initial={}), 'errors': errors})


def add_activity(request, trip_id):
    print("---------------------------------add activity called", request.POST)
    tripObj = get_object_or_404(Trip, id=trip_id)
    flights = tripObj.flights
    """ if (request.method != 'POST'):
        trip_form = TripForm(instance=tripObj)
        activity_form = ActivityForm()
        
    else:
        trip_form = TripForm(request.POST, instance = tripObj)
        activity_form = ActivityForm(request.POST) """
    
    trip_form = TripForm(initial={'start_date': tripObj.start_date, 
                                  'end_date': tripObj.end_date,
                                  'origin_airport': tripObj.origin_airport,
                                  'destination_airport': tripObj.destination_airport,
                                  'location': tripObj.location,
                                  'cost': tripObj.cost})
    
        
    activity_form = ActivityForm(initial={'date': request.POST['date'],
                                          'start_time': request.POST['start_time'],
                                          'end_time': request.POST['end_time'],
                                          'activity_type': request.POST['activity_type'],
                                          'location': request.POST['location'],
                                          'cost': request.POST['cost']})

    if not request.user.is_authenticated:
        return render(request, 'travelwebsite/calendar-19/calendar-19/error.html', {'error': "You must be logged in to add an activity!", 'link': 'login'})
        #return render(request, 'travelwebsite/calendar-19/calendar-19/trip.html', {'trip_id': tripObj.id, 'trip_form': trip_form, 'activity_form': activity_form, 'error': "You must be logged in to add an activity!"})
    
    """ if "date" not in request.POST or not request.POST['date']:
        return render(request, f'travelwebsite/trip/{trip_id}', {'trip_id': tripObj.id, 'trip_form': trip_form, 'activity_form': activity_form, 'error': "You must enter a date!"})
    
    if "start_time" not in request.POST or not request.POST['start_time']:
        return render(request, f'travelwebsite/trip/{trip_id}', {'trip_id': tripObj.id, 'trip_form': trip_form, 'activity_form': activity_form, 'error': "You must enter a start time!"})
    
    if "end_time" not in request.POST or not request.POST['end_time']:
        return render(request, f'travelwebsite/trip/{trip_id}', {'trip_id': tripObj.id, 'trip_form': trip_form, 'activity_form': activity_form, 'error': "You must enter a end time!"})
    
    if "cost" not in request.POST or not request.POST['cost']:
        return render(request, f'travelwebsite/trip/{trip_id}', {'trip_id': tripObj.id, 'trip_form': trip_form, 'activity_form': activity_form, 'error': "You must enter a cost!"})
    
    if "activity_type" not in request.POST or not request.POST['activity_type']:
        return render(request, f'travelwebsite/trip/{trip_id}', {'trip_id': tripObj.id, 'trip_form': trip_form, 'activity_form': activity_form, 'error': "You must enter an activity!"})
     """
    if request.POST['start_time'] > request.POST['end_time']:
        return render(request, 'travelwebsite/calendar-19/calendar-19/error.html', {'error': "Start time must be before end time!", 'link': 'show_trip', 'trip_id': trip_id})
        #return render(request, 'travelwebsite/calendar-19/calendar-19/trip.html', {'trip_id': tripObj.id, 'trip_form': trip_form, 'activity_form': activity_form, 'error': "Start time must be before end time!!"})

    activity_date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
    if activity_date < tripObj.start_date or activity_date > tripObj.end_date:
        print("---------------------------------- here")
        #return _my_json_error_response("Youactivitytion", status=401)
        return render(request, 'travelwebsite/calendar-19/calendar-19/error.html', {'error': "Activity date not in trip range!", 'link': 'show_trip', 'trip_id': trip_id})
        #return render(request, 'travelwebsite/calendar-19/calendar-19/trip.html', {'trip_id': tripObj.id, 'trip_form': trip_form, 'activity_form': activity_form, 'error': "Activity date not in trip range!"})
    
    new_activity = Itinerary(activity_type=request.POST["activity_type"], start_time=request.POST['start_time'], end_time=request.POST['end_time'],
                            date=request.POST['date'], cost=request.POST['cost'], trip = tripObj)
    
    """ activity_date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
    if activity_date < tripObj.start_date or activity_date > tripObj.end_date:
        return render(request, f'travelwebsite/trip/{trip_id}', {'trip_id': tripObj.id, 'trip_form': trip_form, 'activity_form': activity_form, 'error': "Activity date not in trip range!"}) """

    
    new_activity.save()
    print("new activity", new_activity)
    return redirect(f'/trip/{trip_id}')

@login_required
def edit_trip(request, trip_id):
    print("edit trip called")
    print(request.POST)
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)
    
    tripObj = get_object_or_404(Trip, id=trip_id)
    print("tripObj", tripObj)

    tripObj.person = request.user
    if ("origin_airport" in request.POST or not request.POST['origin_airport']) and ("destination_airport" in request.POST or not request.POST['destination_airport']):
        if tripObj.origin_airport != request.POST['origin_airport'] or tripObj.destination_airport != request.POST['destination_airport'] or tripObj.start_date != request.POST['start_date'] or tripObj.end_date != request.POST['end_date']:
            # params = {
            #     "engine": "google_flights",
            #     "departure_id": request.POST['origin_airport'],
            #     "arrival_id": request.POST['destination_airport'],
            #     "outbound_date": request.POST['start_date'],
            #     "return_date": request.POST['end_date'],
            #     "currency": "USD",
            #     "stops": 1,
            #     "type": 1,
            #     "hl": "en",
            #     "api_key": google_api_key
            # }
            # search = GoogleSearch(params)
            # results = search.get_dict()
            # print("results", results)
            # flight = ""
            # if 'error' in results.keys():
            #     flight = results['error']
            # else:
            #     flight =results.other_flights[0].flights[0]['flight_number'] ## TODO: get the flight from t
            a,b = get_flight(request)
            # tripObj.flight, tripObj.flights_url
            tripObj.flights = a
            tripObj.flights_url = b
            print("in edit trip flight", tripObj.flights, tripObj.flights_url)
    if "start_date" in request.POST or not request.POST['start_date']:
        tripObj.start_date = request.POST['start_date']
    if "end_date" in request.POST or not request.POST['end_date']:
        tripObj.end_date = request.POST['end_date']
    if "cost" in request.POST or not request.POST['cost']:
        tripObj.cost = request.POST['cost']
    if "location" in request.POST or not request.POST['location']:
        tripObj.location = request.POST['location']
    if "origin_airport" in request.POST or not request.POST['origin_airport']:
        tripObj.origin_airport = request.POST['origin_airport']
    if "destination_airport" in request.POST or not request.POST['destination_airport']:
        tripObj.destination_airport = request.POST['destination_airport']
    # print("flights in edit_trip", tripObj.flights, tripObj.flights_url)
    tripObj.save()
    print("in edit trip flight after save", tripObj.flights, tripObj.flights_url)
    tripObj = get_object_or_404(Trip, id=trip_id)
    print("in edit trip flight after reload", tripObj.flights, tripObj.flights_url)
    # user = Profile.objects.get(id = request.user.id)
    # print(user.trips)
    
    # request.user.profile.trips.add(new_trip)
    
    # return render(request, 'travelwebsite/trip.html', {'id': trip_id})
    # return show_trips(request, trip_id)
    # return get_trip(request)
    # return render(request, 'travelwebsite/trip.html', {'trip_id': trip_id})
    # return render(request, f'trip/{trip_id}')
    # return redirect(f'/trip/{trip_id}')
    return show_trips(request, trip_id, [])
    # print("edit trip called")
    # tripObj = get_object_or_404(Trip, id=trip_id)

    # params = {
    #     "engine": "google_flights",
    #     "departure_id": "PEK", #request.POST['origin_airport'],
    #     "arrival_id": "AUS", #request.POST['destination_airport'],
    #     "outbound_date": "2024-04-01", #request.POST['start_date'],
    #     "return_date": "2024-04-04", #request.POST['end_date'],
    #     "currency": "USD",
    #     "stops": 1,
    #     "type": 1,
    #     "hl": "en",
    #     "api_key": google_api_key
    # }

    # search = GoogleSearch(params)
    # results = search.get_dict()
    # flight = ""

    # if 'error' in results.keys():
    #     flight = results['error']
    # else:
    #     flight=results.other_flights[0].flights[0]['flight_number'] ## TODO: get the flight from t
    
    # tripObj.flights = flight
    # print("tripObj.flight", tripObj.flights)
    # curr_id = tripObj.id
    # curr_person = tripObj.person
    # curr_flights = tripObj.flights
    # curr_start_date = tripObj.start_date
    # curr_end_date = tripObj.end_date
    # curr_origin_airport = tripObj.origin_airport
    # curr_destination_airport = tripObj.destination_airport
    # curr_location = tripObj.location
    # curr_itinerary = []
    # curr_errors = []
    # curr_cost = tripObj.cost
    # print("curr_id", curr_id)
    # print("curr_person", curr_person)
    # print("curr_flights", curr_flights)
    # print("curr_start_date", curr_start_date)
    # print("curr_end_date", curr_end_date)
    # print("curr_origin_airport", curr_origin_airport)
    # print("curr_destination_airport", curr_destination_airport)
    # print("curr_location", curr_location)
    # print("curr_cost", curr_cost)


    # if not request.user.is_authenticated:        
    #     return render(request, f'/trip/{trip_id}', {'error': "You must be logged in to edit the trip or add an activity!"})

    
    # print("OOOOOOOOO request.POST", request.POST)
    # tripObj.person = request.user
    # if "start_date" in request.POST or not curr_start_date:
    #     print("----------here")
    #     tripObj.start_date = curr_start_date
    # if "end_date" in request.POST or not curr_end_date:
    #     tripObj.end_date = curr_end_date
    # if "cost" in request.POST or not curr_cost:
    #     tripObj.cost = curr_cost
    # if "location" in request.POST or not curr_location:
    #     tripObj.location = curr_location
    # if "origin_airport" in request.POST or not curr_origin_airport:
    #     tripObj.origin_airport = curr_origin_airport
    # if "destination_airport" in request.POST or not curr_destination_airport:
    #     tripObj.destination_airport = curr_destination_airport
    # if ("origin_airport" in request.POST or not curr_origin_airport) and ("destination_airport" in request.POST or not curr_destination_airport):
    #     params = {
    #         "engine": "google_flights",
    #         "departure_id": "PEK", #request.POST['origin_airport'],
    #         "arrival_id": "AUS", #request.POST['destination_airport'],
    #         "outbound_date": "2024-04-01", #request.POST['start_date'],
    #         "return_date": "2024-04-04", #request.POST['end_date'],
    #         "currency": "USD",
    #         "stops": 1,
    #         "type": 1,
    #         "hl": "en",
    #         "api_key": google_api_key
    #     }
    #     search = GoogleSearch(params)
    #     results = search.get_dict()
    #     flight = ""
    #     if 'error' in results.keys():
    #         flight = results['error']
    #     else:
    #         flight =results.other_flights[0].flights[0]['flight_number'] 
    #     tripObj.flight = flight
    # tripObj.save()

    # # user = Profile.objects.get(id = request.user.id)
    # # print(user.trips)
    
    # # request.user.profile.trips.add(new_trip)
    
    # # return render(request, 'travelwebsite/trip.html', {'id': trip_id})
    # # return show_trips(request, trip_id)
    # # return get_trip(request)
    # # return render(request, 'travelwebsite/trip.html', {'trip_id': trip_id})
    # # return render(request, f'trip/{trip_id}')
    # # return redirect(f'/trip/{trip_id}')
    # return show_trips(request, trip_id, [])
    # # print("edit trip called")
    # # tripObj = get_object_or_404(Trip, id=trip_id)

    # # params = {
    # #     "engine": "google_flights",
    # #     "departure_id": "PEK", #request.POST['origin_airport'],
    # #     "arrival_id": "AUS", #request.POST['destination_airport'],
    # #     "outbound_date": "2024-04-01", #request.POST['start_date'],
    # #     "return_date": "2024-04-04", #request.POST['end_date'],
    # #     "currency": "USD",
    # #     "stops": 1,
    # #     "type": 1,
    # #     "hl": "en",
    # #     "api_key": google_api_key
    # # }

    # # search = GoogleSearch(params)
    # # results = search.get_dict()
    # # flight = ""

    # # if 'error' in results.keys():
    # #     flight = results['error']
    # # else:
    # #     flight=results.other_flights[0].flights[0]['flight_number'] ## TODO: get the flight from t
    
    # # tripObj.flight = flight
    # # print("tripObj.flight", tripObj.flight)
    # # curr_id = tripObj.id
    # # curr_person = tripObj.person
    # # curr_flights = tripObj.flights
    # # curr_start_date = tripObj.start_date
    # # curr_end_date = tripObj.end_date
    # # curr_origin_airport = tripObj.origin_airport
    # # curr_destination_airport = tripObj.destination_airport
    # # curr_location = tripObj.location
    # # curr_itinerary = []
    # # curr_errors = []
    # # curr_cost = tripObj.cost
    # # print("curr_id", curr_id)
    # # print("curr_person", curr_person)
    # # print("curr_flights", curr_flights)
    # # print("curr_start_date", curr_start_date)
    # # print("curr_end_date", curr_end_date)
    # # print("curr_origin_airport", curr_origin_airport)
    # # print("curr_destination_airport", curr_destination_airport)
    # # print("curr_location", curr_location)
    # # print("curr_cost", curr_cost)

    # # context = {}
    # # print("----------GET")
    # # context['trip_form'] = EditForm(initial={'start_date': curr_start_date, 
    # #                                          'end_date': curr_end_date,
    # #                                          'origin_airport': curr_origin_airport,
    # #                                          'destination_airport': curr_destination_airport,
    # #                                          'location': curr_location,
    # #                                          'cost': curr_cost})
    
    # # curr_trip = Trip(person = curr_person, 
    # #                  start_date=curr_start_date, 
    # #                  end_date=curr_end_date,
    # #                  location=curr_location,
    # #                  cost=curr_cost, 
    # #                  origin_airport=curr_origin_airport, 
    # #                  destination_airport=curr_destination_airport,
    # #                  flights=flight)
    # # curr_trip.save()
    # # print("curr_trip.id", curr_trip.id)

    # # context['curr_trip'] = curr_trip

    # # if not request.user.is_authenticated:        
    # #     return render(request, f'/travelwebsite/trip/{trip_id}', {'error': "You must be logged in to edit the trip or add an activity!"})

    
    # # print("OOOOOOOOO request.POST", request.POST)
    # # tripObj.person = request.user
    # # if "start_date" in request.POST or not curr_start_date:
    # #     tripObj.start_date = curr_start_date
    # # if "end_date" in request.POST or not curr_end_date:
    # #     tripObj.end_date = curr_end_date
    # # if "cost" in request.POST or not curr_cost:
    # #     tripObj.cost = curr_cost
    # # if "location" in request.POST or not curr_location:
    # #     tripObj.location = curr_location
    # # if "origin_airport" in request.POST or not curr_origin_airport:
    # #     tripObj.origin_airport = curr_origin_airport
    # # if "destination_airport" in request.POST or not curr_destination_airport:
    # #     tripObj.destination_airport = curr_destination_airport
    # # if ("origin_airport" in request.POST or not curr_origin_airport) and ("destination_airport" in request.POST or not curr_destination_airport):
    # #     params = {
    # #         "engine": "google_flights",
    # #         "departure_id": "PEK", #request.POST['origin_airport'],
    # #         "arrival_id": "AUS", #request.POST['destination_airport'],
    # #         "outbound_date": "2024-04-01", #request.POST['start_date'],
    # #         "return_date": "2024-04-04", #request.POST['end_date'],
    # #         "currency": "USD",
    # #         "stops": 1,
    # #         "type": 1,
    # #         "hl": "en",
    # #         "api_key": google_api_key
    # #     }
    # #     search = GoogleSearch(params)
    # #     results = search.get_dict()
    # #     flight = ""
    # #     if 'error' in results.keys():
    # #         flight = results['error']
    # #     else:
    # #         flight =results.other_flights[0].flights[0]['flight_number'] 
    # #     tripObj.flight = flight
    # # tripObj.save()

    # # context['new_trip'] = tripObj
    # # # return render(request, f'/trip/{trip_id}', context)
    # # # return redirect(f'trip/{trip_id}')
    # # return show_trips(request, trip_id, [])


@login_required
def get_trip(request, trip_id=None, errors=[]):
    print("get_trip")
    # To make quiz11 easier, we permit reading the list without logging in. :-)
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    response_data = []
    if trip_id is None:
        trip_id = request.POST["trip_id"]
    print("trip id" , trip_id)
    tripObj = get_object_or_404(Trip, id=trip_id)
    print("get trip flight", tripObj.flights,tripObj.flights_url)
    listfollowers = []
    for user in tripObj.people_followers.all():
        listfollowers.append(user.username)
    my_item = {
            'id': tripObj.id,
            'person': tripObj.person,
            'flights': tripObj.flights,
            'flights_url': tripObj.flights_url,
            'start_date': tripObj.start_date,
            'end_date': tripObj.end_date,
            'origin_airport': tripObj.origin_airport,
            'destination_airport': tripObj.destination_airport,
            'location': tripObj.location,
            'itinerary': [],
            'people_followers': listfollowers,
            'cost': tripObj.cost,
            'errors': errors
        }
    # print("my_item", my_item)
    for iti in Itinerary.objects.all():
        # print(iti.trip.id)
        if tripObj.id == iti.trip.id:
            # print('here')
            my_item['itinerary'].append({
                'id': iti.id,
                'start_time': iti.start_time,
                'end_time': iti.end_time,
                'date': iti.date,
                'cost': iti.cost,
                'activity_type': iti.activity_type
            })
    # print(my_item)
    response_data.append(my_item)
    response_json = json.dumps(response_data, default=str)
    # print(response_json)
    print(response_json)
    return HttpResponse(response_json, content_type='application/json')


@login_required
def delete_trip(request, trip_id):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    # context = { 'items': Trip.objects.all() }

    # if request.method != 'POST':
    #     context['error'] = 'Deletes must be done using the POST method'
    #     return render(request, 'travelwebsite/trip.html', context)

    # # Deletes the item if present in the todo-list database.
    # try:
    #     item_to_delete = Trip.objects.get(id=trip_id)
    #     if request.user.id != item_to_delete.user.id:
    #         context['error'] = 'You can only delete items you have created.'
    #         return render(request, 'travelwebsite/myprofile.html', context)

    #     item_to_delete.delete()
    #     return redirect(reverse('my_profile'))
    # except ObjectDoesNotExist:
    #     context['error'] = 'The item did not exist in the To Do List.'
    #     return render(request, 'travelwebsite/myprofile.html', context)
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    try:
        item = Trip.objects.get(id=trip_id)
    except ObjectDoesNotExist:
        return _my_json_error_response(f"Item with id={trip_id} does not exist.", status=404)

    if request.user.id != item.person.id:
        if request.user not in item.people_followers.all():
            return _my_json_error_response("You cannot delete other user's entries", status=403)
        else:
            print(item.people_followers.all())
            item.people_followers.remove(request.user)
            request.user.profile.trips.remove(item)
            print(item.people_followers.all())
            print("shouldve removed")
            return redirect(reverse('my_profile'))
    for iti in Itinerary.objects.all():
        if item.id == iti.trip.id:
            iti.delete()
    item.delete()

    # return get_trip(request)
    return redirect(reverse('my_profile'))
    

@login_required
def delete_activity(request, activity_id):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    context = { 'items': Itinerary.objects.all() }

    if request.method != 'POST':
        context['error'] = 'Deletes must be done using the POST method'
        return render(request, 'travelwebsite/calendar-19/calendar-19/trip.html', context)

    # Deletes the item if present in the todo-list database.
    try:
        item_to_delete = Itinerary.objects.get(id=activity_id)
        if request.user.id != item_to_delete.trip.person.id:
            context['error'] = 'You can only delete items you have created.'
            return render(request, 'travelwebsite/calendar-19/calendar-19/trip.html', context)

        item_to_delete.delete()
        return redirect(f'/trip/{item_to_delete.trip.id}')
    except ObjectDoesNotExist:
        context['error'] = 'The item did not exist in the To Do List.'
        return render(request, 'travelwebsite/calendar-19/calendar-19/trip.html', context)

def add_collaborator(request, trip_id):
    print("adding colab")
    email = request.POST.get('collaborator_email')
    print(email)
    # user = get_object_or_404(User, email=email)
    user = User.objects.filter(email=email).first()

    print(user)
    if user == None:
        return show_trips(request, trip_id, [])

    profile = user.profile

    tripObj = get_object_or_404(Trip, id=trip_id)
    profile.trips.add(tripObj)
    tripObj.people_followers.add(user)
    print("here")
    print(tripObj.people_followers.all())
    return show_trips(request, trip_id, [])