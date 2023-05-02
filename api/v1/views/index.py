#!/usr/bin/python3
"""
The index page for the flask application
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review


classes = {'states': State, 'cities': City, 'places': Place, 'users': User,
           'amenities': Amenity, 'reviews': Review}


@app_views.route('/status')
def index_page():
    """ returns status of api """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def data_stats():
    """returns number of each object type"""
    stat = {}
    for key, value in classes.items():
        count = storage.count(value)
        stat[key] = count

    return stat
