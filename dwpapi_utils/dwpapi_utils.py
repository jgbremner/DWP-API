from flask import Flask, jsonify
import requests
from geopy import distance, geocoders

REQUEST_API_URL = 'https://bpdts-test-app.herokuapp.com'

#Returns a combined list of users who are listed as either living in London, or whose current coordinates are within 50 miles of London,
#removing duplicates
def getLondonUsers():
    listedLondonUsers = getUsersListedInLondon()
    londonRadiusUsers = getUsersWithinLondonRadius()
    combinedLondonUsers = listedLondonUsers + [i for i in londonRadiusUsers if i not in listedLondonUsers]
    
    return combinedLondonUsers

#Returns list of users listed as being in London according to the 'city' property
#in their personal details.
def getUsersListedInLondon():
    response = requests.get(REQUEST_API_URL + '/city/London/users')
    london_users = response.json()
    return london_users

#Returns list of users within an x mile radius of London according to their listed
#coordinates.
def getUsersWithinLondonRadius(radius=50):
    response = requests.get(REQUEST_API_URL + '/users')
    all_users = response.json()
    
    users_within_mile_range_of_london = filterUsersByDistanceFromLondon(all_users, radius)
    
    return users_within_mile_range_of_london

#Returns, when given a list of users. a list of users filtered to those within a certain mile radius of London.
def filterUsersByDistanceFromLondon(all_users, miledistance):
    filtered_users=[]
    city = "London"
    london_coords = getCityCoordinates("London")
        
    for user in all_users:
        userlat = float(user['latitude'])
        userlong = float(user['longitude'])
        user_coords = (userlat, userlong)

        distance_from_london = distance.distance(user_coords, london_coords).miles

        if distance_from_london <= miledistance:
            filtered_users.append(user)

    return filtered_users

#Returns the coordinates of a particular city when given its name as a string, using the Nominatim geocoder provided by geoPy.
def getCityCoordinates(city):
    geolocator = geocoders.Nominatim(user_agent="Geocode Test API")
    location = geolocator.geocode(city)
    city_coords = (location.latitude, location.longitude)
    return city_coords

