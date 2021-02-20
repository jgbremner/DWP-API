from flask import Flask, jsonify
import requests
from geopy import distance, geocoders
from dwpapi_utils import getLondonUsers

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

#Main route for api call at localhost:5000, returns JSON array of users in London
@app.route('/',methods=['GET'])
def index():
    londonUsers = getLondonUsers()
    return jsonify(londonUsers), 200

#Error handler, returns json rather than HTML as is default.
@app.errorhandler(404)
def page_not_found(err):
    return jsonify(error="404: Page Not Found"), 404

if __name__ == '__main__':
    app.run()
