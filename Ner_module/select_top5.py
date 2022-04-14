from pymongo import MongoClient
from ner_module import get_ner_data

my_client = MongoClient("mongodb+srv://team_andrew:Green@cluster1.jsqyd.mongodb.net/test")
db = my_client.ImageSearch
collection = db["Test"]
x = collection.find()

for i in x:
    print(get_ner_data(i['description'],i['_id']))
