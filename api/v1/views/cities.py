#!/usr/bin/python3
'''Contains the cities view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State."""
    if state_id:
        state = storage.get(State, state_id)
        # If no State object was found, return a 404 error
        if not state:
            abort(404)
        return jsonify([city.to_dict() for city in state.cities])
    return None


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object."""
    if city_id:
        # Retrieving the City object from the storage class by ID
        city = storage.get(City, city_id)
        # If the City object does not exist, return a 404 error
        if not city:
            abort(404)
        return jsonify(city.to_dict())
    return None


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object."""
    if city_id:
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        city.delete()
        storage.save()
        # Return an empty JSON response with 200 status code
        return make_response(jsonify({}), 200)
    return None


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    '''Creates a City.'''
    if state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        # Get the json data from the request
        new_city = request.get_json()
        if not new_city:
            abort(400, "Not a JSON")
        if 'name' not in new_city:
            abort(400, "Missing name")
        # Add the state_id to the new city data
        new_city['state_id'] = state_id
        # Create a new City object with the new city_id
        city = City(**new_city)
        # Add the new city object to storage
        storage.new(city)
        storage.save()
        # Return a 201 status code with the new city data as a json response
        return make_response(jsonify(city.to_dict()), 201)
    return None


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''Updates a City object.'''
    if city_id:
        # Retrieve the City object from the storage using the city_id
        city = storage.get(City, city_id)
        # If the City object does not exist, return a 404 error
        if not city:
            abort(404)
        # Retrieve the JSON request data
        update_info = request.get_json()
        # If the request data is not in JSON format, return a 400 error
        if not update_info:
            abort(400, "Not a JSON")
        # Iterate through each key-value pair in the request data
        for key, value in update_info.items():
            if key not in ['id', 'created_at', 'updated_at', 'state_id']:
                setattr(city, key, value)
        # Save the changes made to the City object
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
