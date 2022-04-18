"""This module will serve the api request."""

# from config import client
from collections import UserList
from pyexpat import features
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import json
import ast
from importlib.machinery import SourceFileLoader
import pymongo
from pymongo import MongoClient
from random import randint # to generate random number
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.applications.imagenet_utils import preprocess_input
import os
from keras.preprocessing import image
import urllib
# from tensorflow.keras.applications import resnet50
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import math
from math import sqrt
from sanic import Sanic
from sanic.response import html



from numpy.linalg import norm
# model = resnet50.ResNet50(weights='imagenet', include_top=False,
#                  input_shape=(256, 256, 3))
def loadImage(URL):
    with urllib.request.urlopen(URL) as url:
        with open('temp.jpg', 'wb') as f:
            f.write(url.read())

    img_path = 'temp.jpg'
    img = image.load_img(img_path, target_size=(256, 256,3))
    os.remove(img_path)
    x = image.img_to_array(img)
    return x

def extract_features(img_path, model):
    img_array = loadImage(img_path)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    features = model.predict(preprocessed_img)
    flattened_features = features.flatten()
    normalized_features = flattened_features / norm(flattened_features)
    return normalized_features

def cosineSim(a1,a2):
    sum = 0
    suma1 = 0
    sumb1 = 0
    for i,j in zip(a1, a2):
        suma1 += i * i
        sumb1 += j*j
        sum += i*j
    cosine_sim = sum / ((sqrt(suma1))*(sqrt(sumb1)))
    return cosine_sim

model = keras.models.load_model('mpg_model.h5')
path1 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAA8FBMVEVjhZYAAACFb1Y1JBDKThGTNwlqVj9mipsmMzn/ySZff49LZXI3JRAcEwipjGt/alKLdFquQw8sGwBzYEowHgguHw5lVEG4Rg5Vc4GEcll/LwiVOAm9ViaQRSPQUBE0Rk9qKQlWSDgZFRBNHQUiFwpAVmEQAA4hEQ5GOi0zKiH/0ifHnB8XBQ6wQw2gPAsmIRBKOSauhxz1wSVMOBITGRyScRlyVxaGaRTfryIfKi9sJQAeMzv/1igrR1GIPSFXU1dOFABvMBd9LwiuUCWnTiSaSSNNMiwEDggaFwAqKidLPzFbRw8uJx4AAAu8kx6dehqm1YzpAAAD9ElEQVR4nO3daVfaQBSA4VYQxKWgLFqxWCwV3Ki22rp1U7uL/f//pp7D3Bt0ME2MknF839NP0xDyNFqGSdAnT4iIiIiIiIiIiIiIiIiIiIiIiIiI3GwycWkL/lP+adKW82kbwkOIEGH6IUTorjAvJRZ+1F2lbbrSwsFEv6P52WRtfToyuzpwijilp6CRTVajq7vyVVhHmE4IESJMvby3woUp0+fDl6akwuys7OlQdj6V3sJG/kD+uQ8bUlLg5VmU9GROpSeckGNIfuqGSBEiRIgQ4YMW6jrDUSC8hwLhqBc2JvWpF7v1+uWfy8bvobrZefeLPN+oFjYGhPcis6Sv5PkmECJEiBAhQpeF3XlJj2tWRrZ0SDfq6sHbQ/aunBDOyry0EXBkKEDrjFPRdX2cCu1duSHM2sLsjcJsqNDaFUKECBH6Luw3+F+8DMmrRSOrQ1kZ2pKhAaGM2LtKQai3JXxd7HcyviU3GryQTpdMpzokI0tn9tA3GTnToROz98XvcvPCyO5Esddpfrwx/Xx+d+mXysjXaQKprrXNTGf6zZXG7qpSIBw1DCFChAgRIrwrYTlnFeaxNy97JrS3znkmHLI5QoQIEXot1Dek3gpfS79apqotrHVMzZIUAiw1ZfOabp6eMFiJqk5LmevCUkc26jyTwoTnsnlTN3dCmLnerYVrCBEiRIjwMQp/r5giCmXzByMcK0WZygwQra3dmNOECBOHECFChAh9Ed78DtgTocxDVlp+XZkJhJpn154QIkSIECHCCMJladcSVvQKS9E+5ppUtofszdO8FyPk2lOmYpqzrzQFh9yUM13UoXLI5k5dP9QqQ4QrCBEiRIgQ4VVh2Vqnj/h66MCdCpGEmcqcaTvsUoY9kmvJA10Xatvxpqq5inncNEKECBEifARCeSscVzgnb6JdFzZlOcOej4VW1Mc5Lqzkkq5JuT5rGzLzRogQIUKECE1VSYXFcqyKjguDyWRNjjSYm0SqU0KIECFChAgRPkDhWDFeD29Oc9sQIkSIEKFvwpVWu18rEMb6+OGgzMk7Ff7smC568oMkOk1TzJNZlsc19YdTLDgg/LBe6He8Kp+imZG/O493Fmt66hz4latDhOur8g2pwrVbC9OTIUSIEGG6wp5Z1M/cUlhyVVh4268w/c5UVWG8N/m1XZNbwt6mqXe83u94Tz5Cq9RoLTvwQq8NmXmv6pfrXkuuRsUVps0aCCFChOmH0E9h8HrYMwsbm34Jq++li33ThR78QpTS+zXjQwq722Rzw3y9ru+r0KmDj1TYHUPtDfMNWUDocggRut9jF/r+atH6u2Ha8VSYkatR7bavQq2K0OEQInQ/hAhH1z9GBYG+R+1fSgAAAABJRU5ErkJggg=='
path2 = 'data:image/png;base64,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'
features0 = extract_features(path1, model)
features1 = extract_features(path2, model)
print(cosineSim(features0, features1))


randotp = randint(1000, 9999)   # Random 4 digit OTP Generator
otp = randotp
# Import the helpers module
helper_module = SourceFileLoader('*', './app/helpers.py').load_module()

# client = MongoClient("mongodb+srv://team_andrew:Green91%40%40@cluster1.jsqyd.mongodb.net/test")


client = pymongo.MongoClient("mongodb+srv://team_andrew:Green@cluster1.jsqyd.mongodb.net/ImageSearch")
db = client.ImageSearch



# Select the collection
collection = db.get_collection("ImageData")
# collection = DATABASE.get_collection("ImageData") #connect to "ImageData" Collection

@app.route("/")
async def get_initial_response(request):
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
async def create_user(request):
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
        # return str(body)
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
async def fetch_users(request):
    """
       Function to fetch the users.
       """
    users = []
    user = collection.find()
    for j in user:
        j.pop('_id')
        users.append(j)
    return jsonify(users)

@app.route("/api/v1/users/<obj_id>", methods=['GET'])
async def fetch_user(obj_id):
    users = []
    user = collection.find()
    for j in user:
        if str(j['_id']) == obj_id:
            # return "here"
            j.pop('_id')
            users.append(j)
    return jsonify(users)


@app.route("/image_id", methods=['GET'])
async def fetch_image_id(request):
    user = collection.find()

    features = []
    URL = 'https://static01.nyt.com/images/2021/03/12/arts/11nft-auction-cryptopunks-print/11nft-auction-cryptopunks-print-articleLarge.jpg?quality=75&auto=webp&disable=upscale'
    features.append(extract_features(path1, model))

    newList = []
    for j in user:
        newList.append(str(j['previewImageURL:']))
    for i in range(5):
        features.append(extract_features(newList[i], model))
    userURL = extract_features(URL, model)   
    similary_score = []
    for i in range(5):
        similary_score.append(cosineSim(userURL, features[i]) * 100)
    return jsonify(similary_score)





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
async def remove_user(user_id):
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
async def page_not_found(e):
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
