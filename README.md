# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

To create a mobile-friendly platform that helps NYU students reconnect with their lost items by allowing users to report lost or found items, browse listings, and search for missing items across campus.

## User stories

Our user stories are tracked as GitHub Issues.

[View User Stories](https://github.com/katiettran/web-app-exercise/issues)


## Steps necessary to run the software

These steps to run the local server assuming you are using a Mac with Python3 and Git installed.

1. Clone the shared repository:

```bash
git clone https://github.com/katiettran/web-app-exercise.git
cd web-app-exercise
```

2. Run the instructor's setup once per clone:

```bash
python3 .automations/setup.py
```

Follow the setup script's hook-approval instructions.

3. Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

4. Create the local settings file:

```bash
cp env.example .env
```

Get the real database settings from Brian through Discord or our group chat.
Replace the placeholders in `.env`.
Ask Brian to add your current IP address to Atlas's IP access list, so you can run the local server on your computer.
Make sure to keep `.env` out of Git.

5. Start Flask:

```bash
python -m flask --app app run --port 5001
```

Open http://127.0.0.1:5001 in a browser.

6. Viewing the Report Detail

The `report_detail` route serves `/reports/<report_id>`.

It passes `report` and `error` to `templates/report_detail.html`. The report includes all seven form fields, a string `id`, and a readable UTC `created_at`.

Malformed IDs and missing reports return 404. Database failures return 503 with a clear error message.

The starter template displays the item name or error. Yash will build the full details page in task #19.

## Task boards

See instructions. Delete this line and place a link to the task boards here.
