import os
from base64 import b64encode
# from flask import Flask, flash, redirect, render_template, send_from_directory, url_for, request
import templates.test_scraper as test_scraper
from templates.test_scraper import * #to import all variables from test_scraper.py
import templates.deleteDB as deleteDB
from sanic import Sanic,Blueprint
from sanic.response import html,redirect,file
from jinja2 import Template,PackageLoader,Environment
import aiofiles
import requests
import urllib
import json
import pymongo
import numpy as np
from math import sqrt
import keras
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing import image


app = Sanic(__name__)
env = Environment(loader=PackageLoader('main', 'templates/'))

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.static('/static', './static')
app.static('/templates', './templates')
app.static('/images', './images')


#Open Default homepage: upload.html
@app.route("/",methods=['POST','GET'])
async def index(request):
    if request.method == "POST":
        email = request.form.get("email")
        global username
        username = email
        template = env.get_template('upload.html')
        content = template.render(email=email)
        return html(content)
    template = open(os.getcwd() + "/templates/base.html")
    return html(template.read())
    #delete all data in database in homepage
    # deleteDB.deleteAll()




#Connect hompage with complete.html, and create upload and submit features


@app.route("/upload/<username>", methods=['POST','GET'])

async def upload(request,username):
    target = os.path.join(APP_ROOT, 'images/')
    if not os.path.isdir(target):
        os.mkdir(target)  # creat new folder if folder doesn't exist
    else:
        print("Folder already exists: {}".format(target))
    upload_file = request.files.get('file')
    if not upload_file:
        return redirect("/?error=no_file")
    file_parameters = {
        'body': upload_file.body,
        'name': upload_file.name,
        'type': upload_file.type,
    }

    file_path = "/".join([target, f"{username}.jpg"])
    with open(file_path, 'wb') as f:
        f.write(file_parameters['body'])
    f.close()

    #calling test_scraper.py for image scraping after the user clicks on Submit button.
    var = test_scraper.imgurl(username)
    var2 = test_scraper.imgweb(username)
    # word_count, entites = ner_function()
    template = env.get_template('complete.html')
    content = template.render(image_name=f"/images/{username}.jpg", variable=var, variable2=var2)# word_count=word_count, entites = entites)
    return html(content)

# image_name = tuple(*[files for (_, _, files) in os.walk('./images/')])

#Display uploaded image from user
# @app.route('/upload/<image_name>')
# async def send_image(image_name):
#     return image_name
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

client = pymongo.MongoClient("mongodb+srv://team_andrew:Green@cluster1.jsqyd.mongodb.net/ImageSearch")
db = client.ImageSearch

# Select the collection
collection = db.get_collection("ImageData")

@app.route("/imageSearch/<username>", methods=['GET'])
async def fetch_users(request):
    """
       Function to fetch the users.
       """
    users = []
    user = collection.find()
    for j in user:
        j.pop('_id')
        users.append(j)
    print("REturning users:", users)
    return json(users)


    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True,workers=4)