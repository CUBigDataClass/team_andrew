import pyimgur
from keras.preprocessing import image
import os
from PIL import Image
import bs4
from flask import jsonify
import requests
import selenium
from selenium import webdriver
from pymongo import MongoClient
import pymongo
import traceback
import os
import time
from selenium.webdriver.common.by import By
import keras
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing import image
import numpy as np
from math import sqrt
import json
import urllib
from numpy.linalg import norm
from model import model
from PIL import Image
# im = pyimgur.Imgur(CLIENT_ID)
# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# PATH = os.path.join(APP_ROOT, 'images/' + 'Randy' + ".jpg")
# print(PATH)
# print("app root:", APP_ROOT)
# uploaded_img = im.upload_image(PATH)
# original_url = uploaded_img.link
# print(original_url)


client = pymongo.MongoClient("mongodb+srv://team_andrew:Green@cluster1.jsqyd.mongodb.net/ImageSearch")
db = client.ImageSearch

# Select the collection
collection = db.get_collection("ImageData")

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
        with open('temp.jpg', 'wb') as f: 
            f.write(new_url.read())

    img_path = 'temp.jpg'
    img = image.load_img(img_path, target_size=(256, 256,3))
    os.remove(img_path)
    x = image.img_to_array(img)
    return x

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

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(APP_ROOT, '../images/drewbdoobiedoo.jpg')
userSim = collection.find({'user_id': "drewbdoobiedoo"}).limit(5)
# print(userSim)
features = []
for item in userSim:
    print(item['description'])
    features.append(extract_features(item['previewImageURL:'], model))
userExtract = extract_features1(PATH, model)
similarity_score = []
for i in range(5):
    # print(cosineSim(userExtract, features[i]) * 100)
    similarity_score.append(cosineSim(userExtract, features[i]) * 100)
    
print("RIGHT HERE HHHHHHHHHHAHAHHAHHAHHAHAHHAHHAHHAHHAHHAHAHHAHHAHHHHHHHHHHHHHHHHHHHHHHHHHHH:",similarity_score)