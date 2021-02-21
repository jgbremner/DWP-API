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

#Accurate coordinates for both London and New York, pulled from google
OFFICIAL_LONDON_COORDS = (51.5074,-0.1277)
OFFICIAL_NEWYORK_COORDS = (40.7128,-74.0060)


#Tests various calls to the main API.
class TestAPICalls(unittest.TestCase):

    #Sets up API for testing
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    #Tests that the API returns a valid response (a JSON list) when a valid get request is made.
    def testValidURLRequest(self):
        # When
        response = self.app.get('/')

        # Then
        self.assertEqual(list, type(response.json))
        self.assertEqual(200, response.status_code)

    #Tests that the API returns a JSON 404 error when an invalid url request is made.
    def testInvalidURLRequest(self):
        # When
        response = self.app.get('/invalid')

        # Then
        self.assertEqual(str, type(response.json['error']))
        self.assertEqual(404, response.status_code)

#Tests the functions used for retrieving users listed in London , or located in a 50 mile range of London based on their coordinates.
class TestGetUsersInLondon(unittest.TestCase):
    
    #Tests that getUsersListedInLondon() returns a list of 5 users.
    def testGetUsersListedInLondon(self):
        london_users = dwpapi_utils.getUsersListedInLondon()
        self.assertEqual(len(london_users),6)
        
    #Tests that getUsersListedInLondon() returns a list of 4 users.
    def testGetUsersWithinLondonRadius(self):
        london_users = dwpapi_utils.getUsersWithinLondonRadius()
        self.assertEqual(len(london_users),3)
        
#Tests for the function filterUsersByDistanceFromLondon()
class TestDistanceFiltering(unittest.TestCase):

    #Tests that filterUsersByDistanceFromLondon(), when provided with a list containing a single user outside of a 50 mile radius
    #of London, returns a list with the same user.
    def testWithinLondonRadius(self):
        filteredList = dwpapi_utils.filterUsersByDistanceFromLondon([TEST_USER_IN_RADIUS],50)
        self.assertEqual(len(filteredList),1)

    #Tests that filterUsersByDistanceFromLondon(), when provided with a list containing a user outside of a 50 mile radius
    #of London, returns an empty list.
    def testOutsideLondonRadius(self):
        filteredList = dwpapi_utils.filterUsersByDistanceFromLondon([TEST_USER_OUT_RADIUS],50)
        self.assertEqual(len(filteredList),0)

    #Tests that filterUsersByDistanceFromLondon(), when provided with a list containing a user on the border of a 50 mile radius
    #of London, returns a list with the same user.
    def testOnLondonRadius(self):
        filteredList = dwpapi_utils.filterUsersByDistanceFromLondon([TEST_USER_ON_RADIUS],50)
        self.assertEqual(len(filteredList),1)

#Tests that the coordinates provided by the geoPy package are accurate to 2 decimal places by comparing them to coordinates provided by google.
class TestGetCityCoordinates(unittest.TestCase):
    def testGetLondonCoordinates(self):
        coords = dwpapi_utils.getCityCoordinates("London")
        roundedcoords = (round(coords[0],2),round(coords[1],2))
        roundedlondoncoords = (round(OFFICIAL_LONDON_COORDS[0],2),round(OFFICIAL_LONDON_COORDS[1],2))
        self.assertEqual(roundedcoords,roundedlondoncoords)
        
    def testGetNewYorkCoordinates(self):
        coords = dwpapi_utils.getCityCoordinates("New York")
        roundedcoords = (round(coords[0],2),round(coords[1],2))
        roundednewyorkcoords = (round(OFFICIAL_NEWYORK_COORDS[0],2),round(OFFICIAL_NEWYORK_COORDS[1],2))
        self.assertEqual(roundedcoords,roundednewyorkcoords)


if __name__ == '__main__':
    unittest.main()
