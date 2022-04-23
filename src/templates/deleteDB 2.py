from pymongo import MongoClient

def deleteAll():
    my_client = MongoClient("mongodb+srv://team_andrew:Green91%40%40@cluster1.jsqyd.mongodb.net/test")
    db = my_client.ImageSearch #connect to "ImageSearch" Database
    collection = db.get_collection("ImageData") #connect to "ImageData" Collection
    x = collection.delete_many({})

    print(x.deleted_count, "documents deleted")