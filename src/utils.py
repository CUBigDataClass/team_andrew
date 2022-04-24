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
import spacy
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import nltk
import unidecode
from collections import Counter



global model_sim
global nlp
model_sim = keras.models.load_model('mpg_model.h5', compile=False)
nlp = spacy.load('en_core_web_sm')
lemmatizer = nltk.stem.WordNetLemmatizer()
w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
stop = set(stopwords.words('english'))


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

def get_ner_data(text):
    entities = []
    doc = nlp(text)
    for ent in doc.ents:
        entities.append(ent.label_)
    return entities

def get_ner_values(list_dest,list_ent):
    top_words = get_top_words(list_dest)
    top_ents = get_top_words(list_ent,3)
    top_ents = check_top_ents(top_ents)
    return top_words,top_ents

def text_preprocessing(text):
    # Replacing all the occurrences of \n,\\n,\t,\\ with a space.
    text = text.replace('\\n', ' ').replace('\n', ' ').replace('\t', ' ').replace('\\', ' ').replace('. com', '.com')
    # strip html tags
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text(separator=" ")
    # remove links
    stripped_text = re.sub(r'http\S+', '', stripped_text)
    stripped_text = re.sub(r"\ [A-Za-z]*\.com", " ", stripped_text)
    # remove whitespace
    pattern = re.compile(r'\s+')
    no_whitespace = re.sub(pattern, ' ', stripped_text)
    stripped_text = no_whitespace.replace('?', ' ? ').replace(')', ') ')
    # Removing unicode characters
    stripped_text = unidecode.unidecode(stripped_text)
    # Changing words like cherrrrrrrry to cherry
    pattern_alpha = re.compile(r"([A-Za-z])\1{1,}", re.DOTALL)
    stripped_text = pattern_alpha.sub(r"\1\1", stripped_text)
    pattern_punct = re.compile(r'([.,/#!$%^&*?;:{}=_`~()+-])\1{1,}')
    stripped_text = pattern_punct.sub(r'\1', stripped_text)
    stripped_text = re.sub(' {2,}', ' ', stripped_text)
    
    # removing special characters and numbers
    text = re.sub('[^A-Za-z0-9]+', ' ', stripped_text)
    text = re.sub(r"[^a-zA-Z:$-,%.?!]+", ' ', text)
    # lemmatization swimming , swim
    text = [lemmatizer.lemmatize(w, 'v') for w in w_tokenizer.tokenize(text)]
    # removing stopwords
    text = ' '.join([word for word in text if word not in stop])
    return text


def get_top_words(text,top_words=5):
    stop = set(stopwords.words('english'))
    corpus = [word for i in text for word in i]
    corpus = [word for word in corpus if word not in stop]
    counter = Counter(corpus)
    most = counter.most_common()
    x = []
    for word, count in most[:top_words]:
        if (word not in stop):
            x.append(word)
    return x

def check_top_ents(top_ents):
    if len(top_ents) < 1:
        top_ents.extend(['NFT','NFT','NFT']) 
    elif len(top_ents)<2:
        top_ents.extend(['NFT','NFT'])
    else:
        top_ents.append('NFT')
    return top_ents