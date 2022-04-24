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
import pyimgur
from PIL import Image


client = pymongo.MongoClient("mongodb+srv://team_andrew:Green@cluster1.jsqyd.mongodb.net/ImageSearch")
db = client.ImageSearch

# Select the collection
collection = db.get_collection("ImageData")

print("in test scraper")

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

def imageScrapping(username):
    '''
    Install selenium and chromedriver (make sure chromedriver matches your version of chrome)
    '''
    # download chromedriver and place it somewhere
    option = webdriver.ChromeOptions()
    # Prevent some useless logs
    # option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    option.add_argument('--no-sandbox')
    option.add_argument('--headless')
    option.add_argument("start-maximized")
    option.add_argument("--window-size=1920,1080")
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--disable-gpu')
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1920x1080")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=option)
    try:
        # Open the website
        driver.get('https://images.google.com/')
        # Find cam button
        cam_button = driver.find_elements(by=By.XPATH, value="//div[@aria-label=\"Search by image\" and @role=\"button\"]")[0]
        cam_button.click()

        # Find upload tab
        upload_tab = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Upload an image')]")[0]
        upload_tab.click()
        # Find image input
        upload_btn = driver.find_elements(by=By.NAME, value='encoded_image')[0]
        #Using the image that user uploaded which saved in "temp.jpg" from app.py
        upload_btn.send_keys(os.getcwd()+f"/images/{username}.jpg")
        # Click on "visually similar images"
        driver.find_elements(by=By.XPATH, value="""//*[@id="rso"]/div[2]/div/div[2]/g-section-with-header/div[1]/title-with-lhs-icon/a/div[2]/h3""")[0].click()
        time.sleep(2)
    except Exception as e:
        print(e)
    # If we want to search by term
    # search_URL = "https://www.google.com/search?q=cute+puppies&source=lnms&tbm=isch"
    # driver.get(search_URL)
    num_images = 5
    # scroll down until we have enough images
    while True:
        page_html = driver.page_source
        pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
        # containers = pageSoup.findAll('div', {'class': "isv-r PNCib MSM1fd BUooTd"})
        containers = pageSoup.findAll('div', {'class': "c7cjWc"}) #had to change class to get docker to work
        driver.execute_script("window.scrollBy(0,1000);")
        len_containers = len(containers)
        # once we have enough containers to scrape the # of images we want
        if len_containers > num_images:
            break
    # scrolling all the way up
    driver.execute_script("window.scrollTo(0,0);")
    print("found %s image containers"%(len(containers)))

    #create list of imageurl to use in app.py and html
    image_list = []
    image_web = []

    for i in range(1,num_images + 1):
        # in google images every 25th images is 'related images', this will break if we click this
        if i % 25 == 0:
            continue
        xpath = """//*[@id="islrg"]/div[1]/div[%s]"""%(i)
        image_website_xpath = """//*[@id="islrg"]/div[1]/div[%s]/a[2]"""%(i)
        preview_image_xpath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img"""%(i)
        image_website_element = driver.find_elements(by=By.XPATH, value=image_website_xpath)[0]
        preview_image_element = driver.find_elements(by=By.XPATH, value=preview_image_xpath)[0]
        preview_image_url = preview_image_element.get_attribute("src")
        driver.find_elements(by=By.XPATH, value=xpath)[0].click()
        timeStarted = time.time()
        while True:
            image_element1 = driver.find_elements(by=By.XPATH, value="""//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img""")[0]
            # gather image URL
            imageURL = image_element1.get_attribute("src")
            image_description = image_element1.get_attribute("alt")
            image_website = image_website_element.get_attribute("href")
            i= i+1
            # if the new high-res image has loaded
            if imageURL != preview_image_url:
                break
            # if we have not loaded the high res images in x seconds, break
            if time.time() - timeStarted > 3:
                break
        #MongoDB with PyMongo to insert Database directly
        my_client = MongoClient("mongodb+srv://team_andrew:Green@cluster1.jsqyd.mongodb.net/ImageSearch")
        db = my_client.ImageSearch #connect to "ImageSearch" Database
        collection = db.get_collection("ImageData") #connect to "ImageData" Collection
        image_element = {"imageLink": imageURL,"description": image_description,"websiteLink":image_website, "previewImageURL:":preview_image_url,"user_id":username} #Create Element
        data = [image_element]
        result = collection.insert_many(data) #insert the saved data into the collection



        #append each imageURL
        image_list.append(imageURL)
        image_web.append(image_website)
        # print("image description:", image_description)
        # print("image URL", imageURL)
        # print("image website:", image_website)

        
    print("made through loop")
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    PATH = os.path.join(APP_ROOT, '../images/' + username + ".jpg")
    userSim = collection.find({'user_id': username}).limit(5)
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

    driver.close()
    driver.quit()
    return image_list,image_web, similarity_score

# def imgurl(username):
#     val, __, __ =imageScrapping(username)
#     return val
# def imgweb(username):
#     __, val, __ = imageScrapping(username)
#     return val
# def imgSim(username):
#     __, __, val = imageScrapping(username)
#     return val
def img(username):
    return imageScrapping(username)


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


