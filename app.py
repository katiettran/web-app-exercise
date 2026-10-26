import os
import re
import datetime
import pymongo
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)

connection = pymongo.MongoClient(os.environ["MONGO_URI"])
db = connection[os.environ["MONGO_DBNAME"]]


def validate_report_form():
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
    errors = {}

    for field in fields:
        form[field] = request.form.get(field, "").strip()
        if not form[field]:
            errors[field] = field.replace("_", " ").capitalize() + " is required."

    if form["status"] and form["status"] not in ["lost", "found"]:
        errors["status"] = "Choose lost or found."

    if form["date"]:
        try:
            parsed_date = datetime.datetime.strptime(form["date"], "%Y-%m-%d")
            if parsed_date.date().isoformat() != form["date"]:
                errors["date"] = "Use YYYY-MM-DD for the date."
        except ValueError:
            errors["date"] = "Enter a valid date as YYYY-MM-DD."

    return form, errors


def get_report(report_id):
    if not ObjectId.is_valid(report_id):
        return {}, "Report not found.", 404

    try:
        report = db.reports.find_one({"_id": ObjectId(report_id)})
    except PyMongoError:
        return {}, "Report could not be loaded. Please try again.", 503

    if report is None:
        return {}, "Report not found.", 404

    report["id"] = str(report["_id"])
    report["created_at"] = report["created_at"].strftime("%Y-%m-%d %H:%M UTC")
    return report, "", 200


def get_matching_reports(q, status):
    if status not in ["all", "lost", "found"]:
        return [], "Choose all, lost, or found.", 400

    query = {}
    if q:
        search_text = re.escape(q)
        query["$or"] = [
            {"item_name": {"$regex": search_text, "$options": "i"}},
            {"location": {"$regex": search_text, "$options": "i"}}
        ]
    if status != "all":
        query["status"] = status

    reports = []
    try:
        documents = db.reports.find(query).sort("created_at", -1)
        for report in documents:
            report["id"] = str(report["_id"])
            report["created_at"] = report["created_at"].strftime("%Y-%m-%d %H:%M UTC")
            reports.append(report)
    except PyMongoError:
        return [], "Reports could not be loaded. Please try again.", 503

    return reports, "", 200


@app.route("/")
def home():
    reports = []
    error = ""
    status_code = 200
    try:
        documents = db.reports.find({}).sort("created_at", -1).limit(6)
        for report in documents:
            report["id"] = str(report["_id"])
            report["created_at"] = report["created_at"].strftime("%Y-%m-%d %H:%M UTC")
            reports.append(report)
    except PyMongoError:
        reports = []
        error = "Reports could not be loaded. Please try again."
        status_code = 503

    return render_template("home.html", reports=reports, error=error), status_code


@app.route("/reports")
def browse_reports():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "all").strip()
    reports, error, status_code = get_matching_reports(q, status)
    return render_template(
        "browse.html", reports=reports, q=q, status=status, error=error
    ), status_code


@app.route("/reports/search")
def search_reports():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "all").strip()
    reports, error, status_code = get_matching_reports(q, status)
    return render_template(
        "search.html", reports=reports, q=q, status=status, error=error
    ), status_code


@app.route("/reports/new", methods=["GET", "POST"])
def create_report():
    form = {"status": "lost"}
    errors = {}
    error = ""
    status_code = 200

    if request.method == "POST":
        form, errors = validate_report_form()
        if errors:
            status_code = 400
        else:
            document = {}
            for field in form:
                document[field] = form[field]
            document["created_at"] = datetime.datetime.utcnow()

            try:
                result = db.reports.insert_one(document)
            except PyMongoError:
                error = "Submission could not be confirmed. Check the listings before trying again."
                status_code = 503
            else:
                return redirect(url_for(
                    "report_confirmation", report_id=str(result.inserted_id)
                ))

    return render_template(
        "report_form.html", form=form, errors=errors, error=error
    ), status_code


@app.route("/reports/<report_id>")
def report_detail(report_id):
    report, error, status_code = get_report(report_id)
    return render_template(
        "report_detail.html", report=report, error=error
    ), status_code


@app.route("/reports/<report_id>/confirmation")
def report_confirmation(report_id):
    report, error, status_code = get_report(report_id)
    if error:
        if status_code == 503:
            error = "Confirmation could not be loaded. Check the listings before submitting again."
        return render_template(
            "report_detail.html", report={}, error=error
        ), status_code

    return render_template(
        "report_confirmation.html", report=report, error=""
    )


@app.route("/reports/<report_id>/edit", methods=["GET", "POST"])
def edit_report(report_id):
    report, error, status_code = get_report(report_id)
    form = {}
    errors = {}

    if report and request.method == "POST":
        form, errors = validate_report_form()
        if errors:
            status_code = 400
        else:
            try:
                result = db.reports.update_one(
                    {"_id": ObjectId(report_id)}, {"$set": form}
                )
            except PyMongoError:
                error = "Changes could not be confirmed. Check the report before trying again."
                status_code = 503
            else:
                if result.matched_count == 0:
                    report = {}
                    error = "Report not found."
                    status_code = 404
                else:
                    return redirect(url_for("report_detail", report_id=report_id))

    return render_template(
        "edit_report.html", report=report, form=form, errors=errors, error=error
    ), status_code


@app.route("/reports/<report_id>/delete", methods=["GET", "POST"])
def delete_report(report_id):
    report, error, status_code = get_report(report_id)

    if report and request.method == "POST":
        try:
            result = db.reports.delete_one({"_id": ObjectId(report_id)})
        except PyMongoError:
            error = "Deletion could not be confirmed. Check the listings before trying again."
            status_code = 503
        else:
            if result.deleted_count == 0:
                report = {}
                error = "Report not found."
                status_code = 404
            else:
                return redirect(url_for("browse_reports"))

    return render_template(
        "delete_report.html", report=report, error=error
    ), status_code
