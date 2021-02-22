from flask import Flask, jsonify
import requests
from geopy import distance, geocoders
from dwpapi_utils import get_all_london_users

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/',methods=['GET'])
def index():
    '''Main route for api call at localhost:5000,
    returns JSON array of users in London'''
    try:
        london_users = get_all_london_users()
        return jsonify(london_users), 200
    except requests.exceptions.RequestException as e:
        return jsonify(error="500 Internal Server Error - Failed to make connection to DWP Test API: "+repr(e)), 500
    except Exception as e:
        return jsonify(error="500 Internal Server Error: "+repr(e)), 500

#
#JSON Error handling for expected invalid requests
#
@app.errorhandler(404)
def page_not_found(err):
    '''Error handler, returns json rather than HTML as is default.'''
    return jsonify(error="404 Error: Page Not Found"), 404

@app.errorhandler(405)
def non_get_request(err):
    '''Error handler, returns json rather than HTML as is default.'''
    return jsonify(error="405 Error: Only GET requests are allowed on this URL"), 405

if __name__ == '__main__':
    app.run()
