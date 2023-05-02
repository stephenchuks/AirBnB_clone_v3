#!/usr/bin/python3
"""
This module contains the views for Review objects
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews_by_place(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews
               if review.place_id == place_id]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a new Review object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')

    user_id = data.get('user_id')
    if user_id is None:
        abort(400, 'Missing user_id')

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    text = data.get('text')
    if text is None:
        abort(400, 'Missing text')

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')

    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
