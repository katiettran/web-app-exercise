import os
import pymongo
from dotenv import load_dotenv
from flask import Flask, render_template
from pymongo.errors import PyMongoError

load_dotenv()

app = Flask(__name__)

connection = pymongo.MongoClient(os.environ["MONGO_URI"])
db = connection[os.environ["MONGO_DBNAME"]]

@app.route("/")
def home():
    reports = []
    error = ""
    try:
        documents = db.reports.find({}).sort("created_at", -1).limit(6)
        for report in documents:
            report["id"] = str(report["_id"])
            report["created_at"] = report["created_at"].strftime("%Y-%m-%d %H:%M UTC")
            reports.append(report)
    except PyMongoError:
        reports = []
        error = "Reports could not be loaded. Please try again."

    return render_template("home.html", reports=reports, error=error)
