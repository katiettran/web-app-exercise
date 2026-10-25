import os
import pymongo
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from pymongo.errors import PyMongoError
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
@app.route("/reports/new", methods=["GET", "POST"])
def new_report():
    if request.method == "GET":
        return render_template(
            "report_form.html",
            form={},
            errors={},
            error=""
        )

    fields = [
        "status",
        "item_name",
        "category",
        "date",
        "location",
        "description",
        "contact_info"
    ]

    form = {
        field: request.form.get(field, "").strip()
        for field in fields
    }

    errors = {}

    for field in fields:
        if not form[field]:
            errors[field] = f"{field.replace('_', ' ').title()} is required."

    if form["status"] not in ("lost", "found"):
        errors["status"] = "Please select Lost or Found."

    try:
        datetime.strptime(form["date"], "%Y-%m-%d")
    except ValueError:
        errors["date"] = "Please enter a valid date."

    if errors:
        return render_template(
            "report_form.html",
            form=form,
            errors=errors,
            error=""
        ), 400

    document = {
        **form,
        "created_at": datetime.now(timezone.utc)
    }

    try:
        result = db.reports.insert_one(document)
    except PyMongoError:
        return render_template(
            "report_form.html",
            form=form,
            errors={},
            error="Report could not be saved. Please try again."
        ), 503

    return redirect(url_for("report_detail", report_id=str(result.inserted_id)))