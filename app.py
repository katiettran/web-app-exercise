import os
import pymongo
from dotenv import load_dotenv
from flask import Flask, render_template
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from bson import ObjectId
from bson.errors import InvalidId

load_dotenv()

app = Flask(__name__)

connection = pymongo.MongoClient(os.environ["MONGO_URI"])
db = connection[os.environ["MONGO_DBNAME"]]

@app.route("/reports/<report_id>")
def report_detail(report_id):
    try:
        object_id = ObjectId(report_id)

    except InvalidId:
        return render_template(
            "report_detail.html",
            report={},
            error="The report you requested could not be found."
        ), 404

    try:
        report = db.reports.find_one({"_id": object_id})

    except PyMongoError:
        return render_template(
            "report_detail.html",
            report={},
            error="The report could not be loaded. Please try again."
        ), 503

    if report is None:
        return render_template(
            "report_detail.html",
            report={},
            error="The report you requested could not be found."
        ), 404

    report["id"] = str(report["_id"])

    return render_template(
        "report_detail.html",
        report=report,
        error=""
    )
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
@app.route("/reports")
def browse_reports():
    reports = []
    error = ""

    try:
        documents = db.reports.find({}).sort("created_at", -1)

        for report in documents:
            report["id"] = str(report["_id"])
            report["created_at"] = report["created_at"].strftime("%Y-%m-%d %H:%M UTC")
            reports.append(report)

    except PyMongoError:
        reports = []
        error = "Reports could not be loaded. Please try again."

    return render_template("browse.html", reports=reports, error=error)
