import unittest
import dwpapi_utils
from dwpapi import app
import json

#Extract JSON user test cases from file
with open('test_cases.json') as json_file:
    data = json.load(json_file)

TEST_USER_IN_RADIUS = data[0]
TEST_USER_OUT_RADIUS = data[1]
TEST_USER_ON_RADIUS = data[2]

#Accurate coordinates for both London and New York, pulled from google maps
ACCURATE_LONDON_COORDS = (51.5074,-0.1277)
ACCURATE_NEWYORK_COORDS = (40.7128,-74.0060)


class TestAPICalls(unittest.TestCase):
    '''Tests various calls to the main API.'''

    def setUp(self):
        '''Sets up API for testing using a Flask test client.'''
        app.testing = True
        self.app = app.test_client()

    def test_valid_url_request(self):
        '''Tests that the API returns a valid response (a JSON list) when a valid get request is made.'''
        response = self.app.get('/')

        self.assertEqual(list, type(response.json))
        self.assertEqual(200, response.status_code)

    def test_invalid_url_request(self):
        '''Tests that the API returns a JSON 404 error when an invalid url request is made.'''
        response = self.app.get('/invalid')

        self.assertEqual(str, type(response.json['error']))
        self.assertEqual(404, response.status_code)

    def test_non_get_request(self):
        '''Tests that the API returns a JSON 405 error when a non-get request is made.'''
        response = self.app.post('/')

        self.assertEqual(str, type(response.json['error']))
        self.assertEqual(405, response.status_code)


class TestGetUsersInLondon(unittest.TestCase):
    '''Tests the functions used for retrieving users listed in London,
    or located in a 50 mile range of London based on their coordinates.'''
    
    def test_get_users_listed_in_london(self):
        '''Tests that get_users_listed_in_london() returns a list of 5.'''
        listed_london_users = dwpapi_utils.get_users_listed_in_london()
        self.assertEqual(len(listed_london_users),6)
        
    def test_get_users_within_london_radius(self):
        '''Tests that get_users_within_london_radius() returns a list of 4.'''
        radius_london_users = dwpapi_utils.get_users_within_london_radius()
        self.assertEqual(len(radius_london_users),3)

    def test_get_all_london_users(self):
        '''Tests that get_all_london_users() returns a list of 9 where each member
        of listed_london_users or radius_london_users is featured in the list.'''
        london_users = dwpapi_utils.get_all_london_users()
        concatenated_users = dwpapi_utils.get_users_listed_in_london() + dwpapi_utils.get_users_within_london_radius()
        
        for user in concatenated_users:
            self.assertIn(user, london_users)
            
        self.assertEqual(len(london_users),9)

        
class TestDistanceFiltering(unittest.TestCase):
    '''Tests for the function filter_users_by_distance_from_london()'''

    def test_within_london_radius(self):
        '''Tests that filter_users_by_distance_from_london(), when provided with a list containing a single user outside of a 50 mile radius
        of London, returns a list with the same user.'''
        filtered_list = dwpapi_utils.filter_users_by_distance_from_london([TEST_USER_IN_RADIUS],50)
        self.assertEqual(len(filtered_list),1)
    
    def test_outside_london_radius(self):
        '''Tests that filter_users_by_distance_from_london(), when provided with a list containing a user outside of a 50 mile radius
        of London, returns an empty list.'''
        filtered_list = dwpapi_utils.filter_users_by_distance_from_london([TEST_USER_OUT_RADIUS],50)
        self.assertEqual(len(filtered_list),0)

    def test_on_london_radius(self):
        '''Tests that filter_users_by_distance_from_london(), when provided with a list containing a user on the border of a 50 mile radius
        of London, returns a list with the same user.'''
        filtered_list = dwpapi_utils.filter_users_by_distance_from_london([TEST_USER_ON_RADIUS],50)
        self.assertEqual(len(filtered_list),1)


class TestGetCityCoordinates(unittest.TestCase):
    '''Tests that the coordinates provided by the geoPy package are accurate to 2 decimal places by comparing
    them to coordinates provided by google.'''
    
    def test_get_london_coordinates(self):
        coords = dwpapi_utils.get_city_coordinates("London")
        rounded_coords = (round(coords[0],2),round(coords[1],2))
        rounded_london_coords = (round(ACCURATE_LONDON_COORDS[0],2),round(ACCURATE_LONDON_COORDS[1],2))
        self.assertEqual(rounded_coords,rounded_london_coords)
        
    def test_get_newyork_coordinates(self):
        coords = dwpapi_utils.get_city_coordinates("New York")
        rounded_coords = (round(coords[0],2),round(coords[1],2))
        rounded_newyork_coords = (round(ACCURATE_NEWYORK_COORDS[0],2),round(ACCURATE_NEWYORK_COORDS[1],2))
        self.assertEqual(rounded_coords,rounded_newyork_coords)


if __name__ == '__main__':
    unittest.main()
