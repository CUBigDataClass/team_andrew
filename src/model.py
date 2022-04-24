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
from tensorflow.keras.applications import resnet50

global model
model = keras.models.load_model('mpg_model.h5')