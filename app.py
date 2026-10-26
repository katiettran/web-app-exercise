import os
import pymongo
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from pymongo.errors import PyMongoError
import datetime
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)

connection = pymongo.MongoClient(os.environ["MONGO_URI"])
db = connection[os.environ["MONGO_DBNAME"]]

@app.route("/reports/<report_id>")
def report_detail(report_id):
    report = {}
    error = ""
    status_code = 200

    if not ObjectId.is_valid(report_id):
        error = "Report not found."
        status_code = 404

    else:
        try:
            document = db.reports.find_one({"_id": ObjectId(report_id)})

            if document is None:
                error = "Report not found."
                status_code = 404

            else:
                report = document
                report["id"] = str(report["_id"])
                report["created_at"] = report["created_at"].strftime("%Y-%m-%d %H:%M UTC")

        except PyMongoError:
            report = {}
            error = "Report could not be loaded. Please try again."
            status_code = 503

    return render_template(
        "report_detail.html",
        report=report,
        error=error
    ), status_code
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
@app.route("/reports/new", methods=["GET", "POST"])
def create_report():
    fields = [
        "status",
        "item_name",
        "category",
        "date",
        "location",
        "description",
        "contact_info"
    ]

    form = {}

    for field in fields:
        form[field] = ""

    form["status"] = "lost"
    errors = {}
    error = ""
    status_code = 200

    if request.method == "POST":
        for field in fields:
            form[field] = request.form.get(field, "").strip()

            if not form[field]:
                errors[field] = field.replace("_", " ").capitalize() + " is required."

        if form["status"] and form["status"] not in ["lost", "found"]:
            errors["status"] = "Choose lost or found."

        if form["date"]:
            try:
                datetime.datetime.strptime(form["date"], "%Y-%m-%d")

                if len(form["date"]) != 10:
                    errors["date"] = "Use YYYY-MM-DD for the date."

            except ValueError:
                errors["date"] = "Enter a valid date as YYYY-MM-DD."

        if errors:
            status_code = 400

        else:
            document = {}

            for field in fields:
                document[field] = form[field]

            document["created_at"] = datetime.datetime.utcnow()

            try:
                result = db.reports.insert_one(document)
    
            except PyMongoError:
                error = "Submission could not be confirmed. Check the listings before trying again."
                status_code = 503
    
            else:
                return redirect(url_for(
                    "report_confirmation",
                    report_id=str(result.inserted_id)
                ))

    return render_template(
        "report_form.html",
        form=form,
        errors=errors,
        error=error
    ), status_code
@app.route("/reports/<report_id>/confirmation")
def report_confirmation(report_id):
    if not ObjectId.is_valid(report_id):
        return render_template(
            "home.html",
            reports=[],
            error="Report not found."
        ), 404

    try:
        report = db.reports.find_one({"_id": ObjectId(report_id)})

    except PyMongoError:
        return render_template(
            "home.html",
            reports=[],
            error="Confirmation could not be loaded. Check the listings before submitting again."
        ), 503

    if report is None:
        return render_template(
            "home.html",
            reports=[],
            error="Report not found."
        ), 404

    report["id"] = str(report["_id"])
    report["created_at"] = report["created_at"].strftime("%Y-%m-%d %H:%M UTC")

    return render_template(
        "report_confirmation.html",
        report=report,
        error=""
    )
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
