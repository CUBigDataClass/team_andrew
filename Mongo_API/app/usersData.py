"""This module will serve the api request."""

# from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import json
import ast
from importlib.machinery import SourceFileLoader
import pymongo
from pymongo import MongoClient
from random import randint # to generate random number


randotp = randint(1000, 9999)   # Random 4 digit OTP Generator
otp = randotp
# Import the helpers module
helper_module = SourceFileLoader('*', './app/helpers.py').load_module()

# client = MongoClient("mongodb+srv://team_andrew:Green91%40%40@cluster1.jsqyd.mongodb.net/test")


client = pymongo.MongoClient("mongodb+srv://team_andrew:Green@cluster1.jsqyd.mongodb.net/ImageSearch")
db = client.ImageSearch

# Select the database
# db = client.ImageSearch
# DATABASE = client.ImageSearch #connect to "ImageSearch" Database
# Select the collection
collection = db.get_collection("ImageData")
# collection = DATABASE.get_collection("ImageData") #connect to "ImageData" Collection

@app.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Flask API'
    }
    # Making the message looks good
    resp = jsonify(message)
    # Returning the object
    return resp

# @app.route("/test")
# def get_test():
#     message = {
#         'message': 'it worked'
#     }
#      # Making the message looks good
#     resp = jsonify(message)
#     # Returning the object
#     return resp

# @app.route("/users", methods=['POST'])
# def add_user():
#     try:
#     # Create new users
#         try:
#             body = ast.literal_eval(json.dumps(request.get_json()))
#             # return str(body)
#         except:
#             # Bad request as request body is not available
#             # Add message for debugging purpose
#             return "", 400
#         # return collection.name
#         record_created = collection.insert_many(body)
#         # return str(record_created)
#         # Prepare the response
#         if isinstance(record_created, list):
#             # Return list of Id of the newly created item
#             return jsonify([str(v) for v in record_created]), 201
#         else:
#             # Return Id of the newly created item
#             return jsonify(str(record_created)), 201
#     except:
#         # Error while trying to create the resource
#         # Add message for debugging purpose
#         return "", 880

@app.route("/api/v1/users", methods=['POST'])
def create_user():
    """
       Function to create new users.
       """
    try:
        # Create new users
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400

        record_created = collection.insert_many(body)

        # Prepare the response
        if isinstance(record_created, list):
            # Return list of Id of the newly created item
            return jsonify([str(v) for v in record_created]), 201
        else:
            # Return Id of the newly created item
            return jsonify(str(record_created)), 201
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/v1/users", methods=['GET'])
def fetch_users():
    """
       Function to fetch the users.
       """
    users = []
    user = collection.find()
    for j in user:
        j.pop('_id')
        users.append(j)
    return jsonify(users)


# @app.route("/api/v1/users/<user_id>", methods=['POST'])
# def update_user(user_id):
#     """
#        Function to update the user.
#        """
#     try:
#         # Get the value which needs to be updated
#         try:
#             body = ast.literal_eval(json.dumps(request.get_json()))
#         except:
#             # Bad request as the request body is not available
#             # Add message for debugging purpose
#             return "", 400

#         # Updating the user
#         records_updated = collection.update_one({"id": int(user_id)}, body)

#         # Check if resource is updated
#         if records_updated.modified_count > 0:
#             # Prepare the response as resource is updated successfully
#             return "", 200
#         else:
#             # Bad request as the resource is not available to update
#             # Add message for debugging purpose
#             return "", 404
#     except:
#         # Error while trying to update the resource
#         # Add message for debugging purpose
#         return "", 500


@app.route("/api/v1/users/<user_id>", methods=['DELETE'])
def remove_user(user_id):
    """
       Function to remove the user.
       """
    try:
        # Delete the user
        delete_user = collection.delete_one({"id": int(user_id)})

        if delete_user.deleted_count > 0 :
            # Prepare the response
            return "", 204
        else:
            # Resource Not found
            return "", 404
    except:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp
