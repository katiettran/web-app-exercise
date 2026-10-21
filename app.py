import os
import pymongo
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)

connection = pymongo.MongoClient(os.environ["MONGO_URI"])
db = connection[os.environ["MONGO_DBNAME"]]

@app.route("/")
def home():
    return "NYU Lost & Found"
