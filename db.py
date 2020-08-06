from pymongo import MongoClient
from flask import g

client = MongoClient("localhost", 27017)
db = client["scheduler_db"]

def get_db():

    client = g._database = MongoClient("localhost", 27017)
    db = client["scheduler_db"]

    return db