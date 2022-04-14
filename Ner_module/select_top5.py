from ner_module import multi_run_ner
import multiprocessing
from pymongo import MongoClient
from multiprocessing import Pool
from itertools import product
import time
from flask import Flask
from flask_restful import Resource, Api, reqparse


my_client = MongoClient("mongodb+srv://team_andrew:Green91%40%40@cluster1.jsqyd.mongodb.net/test")
db = my_client.ImageSearch
collection = db["Test"]
x = collection.find()

if __name__ == '__main__':
    start_time = time.time()
    p = Pool()
    data = p.map(multi_run_ner, [(i['description'],i['_id']) for i in x])
    p.close()
    print("--- %s seconds ---" % (time.time() - start_time))
    print(data)