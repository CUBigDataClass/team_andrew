from pymongo import MongoClient
import keras
from numpy.linalg import norm
from keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing import image
import numpy as np
from math import sqrt
import urllib
from numpy.linalg import norm
import pyimgur
import os

global model_sim
model_sim = keras.models.load_model('mpg_model.h5', compile=False)

#MongoDB with PyMongo to insert Database directly
def get_mongo():
    my_client = MongoClient("mongodb+srv://team_andrew:Green@cluster1.jsqyd.mongodb.net/ImageSearch")
    db = my_client.ImageSearch #connect to "ImageSearch" Database
    collect_mongo = db.get_collection("ImageData") #connect to "ImageData" Collection
    return collect_mongo

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

def extract_features1(img_path, model):
    img_array = loadImage1(img_path)
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

def loadImage1(URL):
    # image1 = Image.open(URL)
    # newsize = (256, 256)
    # im1 = image1.resize(newsize)
    # x = image.img_to_array(im1)
    CLIENT_ID = "593e9ceece15bc4"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(URL)
    original_url = uploaded_image.link

    with urllib.request.urlopen(original_url) as new_url:
        with open('temp.jpg', 'wb') as f: #this could be problem - need to change from temp?
            f.write(new_url.read())

    img_path = 'temp.jpg'
    img = image.load_img(img_path, target_size=(256, 256,3))
    os.remove(img_path)
    x = image.img_to_array(img)
    return x