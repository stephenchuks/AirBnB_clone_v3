#!/usr/bin/python3
'''Contains the places view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.state import State
from models.city import City
from models.user import User


@app_views.route('/cities/<cities_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(cities_id):
    """ method to get list of all places in a city"""

    city = storage.get(City, cities_id)
    if not city:
        abort(404)

    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ get a place based on its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete a place """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ create a place in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user_id = data.get('user_id')
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")

    place = Place(**data)
    setattr(place, 'city_id', city_id)
    storage.new()
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ update an atrribute of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:

            setattr(place, key, value)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
