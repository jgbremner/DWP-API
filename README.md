# DWP-API

This is an API created for the technical test at https://bpdts-test-app.herokuapp.com/, which returns users listed by that API that have the property city="London" or have coordinates that fall within a 50-mile radius of London.

## Installing/running the API

The API is written in Python 3.6 using the Flask API library as well as various other dependencies which can be installed using the following command:

```
pip install -r requirements.txt
```

Then start the api by running the following command, which creates a server at http://127.0.0.1:5000/:

```
python3 dwpapi.py
```

Run tests for the API using:

```
python3 dwpapi_tests.py
```

## Endpoints/Calling the API

The API has a single endpoint at the root URL http://127.0.0.1:5000/, which should return a JSON list fullflling the test requirements.
