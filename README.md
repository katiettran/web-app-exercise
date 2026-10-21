# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

See instructions. Delete this line and place the Product Vision Statement here.

## User stories

See instructions. Delete this line and place a link to the user stories here.

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

## Task boards

See instructions. Delete this line and place a link to the task boards here.
