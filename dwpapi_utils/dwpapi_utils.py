from flask import Flask, jsonify
import requests
from geopy import distance, geocoders

REQUEST_API_URL = 'https://bpdts-test-app.herokuapp.com'

def get_all_london_users():
    '''Returns a combined list of users who are listed as either living in London, or whose current coordinates are within 50 miles of London,
    removing duplicates'''
    try:
        listed_london_users = get_users_listed_in_london()
        radius_london_users = get_users_within_london_radius()
        
        #Combines both lists removing duplicates
        combined_london_users = listed_london_users + [i for i in radius_london_users if i not in listed_london_users]

        return combined_london_users

    except requests.exceptions.RequestException as e: #Error handling to deal with any unexpected connection errors when connecting to external dwp api.
        raise requests.exceptions.RequestException(e)
    except Exception as e: #Error handling to deal with any unexpected generic internal errors
        raise Exception(e)
        

def get_users_listed_in_london():
    '''Returns list of users listed as being in London according to the 'city' property
    in their personal details.'''
    response = requests.get(REQUEST_API_URL + '/city/London/users')
    london_users = response.json()
    return london_users
        

def get_users_within_london_radius(radius=50):
    '''Returns list of users within an x mile radius of London according to their listed
    coordinates.'''
    response = requests.get(REQUEST_API_URL + '/users')
    all_users = response.json()
    users_within_radius = filter_users_by_distance_from_london(all_users, radius)
    return users_within_radius

def filter_users_by_distance_from_london(users, radius):
    '''Returns, when given a list of users. a list of users filtered to those within a certain mile radius of London.'''
    filtered_users=[]
    city = "London"
    london_coords = get_city_coordinates("London")

    #Iterates through list of all users, only adding it to filteredUsers
    #if its coordinates are within a 50 mile range of London.
    for user in users:
        user_lat = float(user['latitude'])
        user_long = float(user['longitude'])
        user_coords = (user_lat, user_long)

        #Determines distance in miles from user coordinates to central London coords
        distance_from_london = distance.distance(user_coords, london_coords).miles

        if distance_from_london <= radius:
            filtered_users.append(user)

    return filtered_users

def get_city_coordinates(city):
    '''Returns the coordinates of a particular city when given its name as a string, using the Nominatim geocoder provided by geoPy.'''
    geolocator = geocoders.Nominatim(user_agent="Geocode Test API")
    location = geolocator.geocode(city)
    city_coords = (location.latitude, location.longitude)
    return city_coords

