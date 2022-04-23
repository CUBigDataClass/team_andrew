from pymongo import MongoClient
from ner_module import get_ner_data
from preprocess import text_preprocessing,get_top_words,check_top_ents

my_client = MongoClient("mongodb+srv://team_andrew:Green@cluster1.jsqyd.mongodb.net/ImageSearch")
db = my_client.ImageSearch
collection = db["ImageData"]
x = collection.find()
list_dest = []
list_ent = []
for i in x[:]:
    print(i)
    cleaned_text = text_preprocessing(i['description'].lower())
    list_ent.append(get_ner_data(cleaned_text))
    list_dest.append(cleaned_text.split())

top_words = get_top_words(list_dest)
top_ents = get_top_words(list_ent,3)
top_ents = check_top_ents(top_ents)
print(top_words,top_ents)