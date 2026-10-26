# NYU Lost & Found

## Product vision statement

To create a mobile-friendly platform that helps NYU students reconnect with their lost items by allowing users to report lost or found items, browse listings, and search for missing items across campus.

## User stories

[View user stories and tasks](https://github.com/katiettran/web-app-exercise/issues)

## Task boards

[View the Sprint 1 and Sprint 2 boards](https://github.com/katiettran/web-app-exercise/projects)

## Steps necessary to run the software

Follow the setup steps below in order, then check that the app works.

### Before you start

You need the following:

- An internet connection and a web browser.
- Python 3. Local development checks used Python 3.12.
- Git.
- Visual Studio Code (VS Code), as required by the [course conventions](https://knowledge.kitchen/content/courses/software-engineering/conventions/).

You also need the team's MongoDB settings from Brian through the team messenger. Ask Brian to add your current public IP address to the cluster's IP access list. Brian must keep the cluster available while you use the app. You do not need to create a separate database server on your computer.

Complete the steps in order. Use only the commands for your operating system. Enter each command in the command window and press Enter. Copy the command text, without the surrounding code fences or language labels such as `bash`.

If a command reports an error, resolve it before continuing.

### 1. Open VS Code's terminal and check Python and Git

Install [Visual Studio Code](https://code.visualstudio.com/) if it is not already installed, then open it.

Use VS Code's integrated terminal for the following commands:

- On a Mac, choose **Terminal > New Terminal** and use the default `zsh` shell.
- On Linux, choose **Terminal > New Terminal** and use `bash` or another UNIX-compatible shell.
- On Windows, install [Git for Windows](https://gitforwindows.org/), which includes Git Bash. In VS Code, choose **Terminal > Select Default Profile > Git Bash**, then **Terminal > New Terminal**.

If Git Bash does not appear, restart VS Code after installing Git for Windows. The Windows instructions below use Git Bash, as required by the course.

On Mac or Linux:

```bash
python3 --version
git --version
```

On Windows in Git Bash:

```bash
py --version
git --version
```

You should see a Python 3 version and a Git version.

If Python is missing, install it from [Python's official download page](https://www.python.org/downloads/) for your operating system. Complete the installer, restart VS Code, and repeat the version checks.

If Git is missing, follow [Git's installation instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). On a Mac, running `git --version` may open Apple's installation prompt. Complete that installation and repeat the check.

On Linux, use your distribution's instructions to install Python 3, Git, pip, and Python's `venv` support before continuing.

### 2. Download the project and enter its folder

For a first download, run the following commands in VS Code's terminal. They work in Mac/Linux shells and Windows Git Bash.

```bash
cd ~
git clone https://github.com/katiettran/web-app-exercise.git
cd web-app-exercise
ls
pwd
```

The listing should include these project files and folders:

- `app.py`
- `requirements.txt`
- `env.example`
- `templates/`
- `static/`

The `pwd` command prints the project's location. Choose **File > Open Folder** in VS Code and open that folder. Open a new integrated terminal in the project. On Windows, keep using Git Bash. Run the remaining setup commands from this folder.

If you already have this repository on your computer, use its existing folder instead. Its name may differ from `web-app-exercise`. Open that folder in VS Code, then open its integrated terminal and confirm the same files are present. Keep any existing `.env` file.

If Git says the destination folder already exists, open that folder and check its contents. Do not delete an existing project to repeat these steps.

### 3. Run the instructor's setup

Run this once in each new clone.

On Mac or Linux:

```bash
python3 .automations/setup.py
```

On Windows in Git Bash:

```bash
py .automations/setup.py
```

Resolve the problems the script reports. If it requests a Git identity, use your GitHub username and the email address you use for the course. Follow its hook-approval instructions for each AI coding tool in your environment, then rerun setup if required.

Keep the instructor's automation files unchanged.

### 4. Create the project's Python environment and install packages

The `.venv` folder keeps this project's Python packages separate from other projects.

On Mac or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows in Git Bash:

```bash
py -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

Wait for installation to finish. Confirm that the project's Python and packages are available:

```bash
python -c "import sys, flask, pymongo, dotenv; print(sys.executable); print('Packages installed')"
```

The printed Python path should contain this project's `.venv` folder. You should also see `Packages installed`.

### 5. Create and fill in the private database settings

If `.env` already exists, keep it and check its values. Otherwise, copy `env.example` using the following command on Mac, Linux, or Windows Git Bash:

```bash
cp env.example .env
```

In VS Code's Explorer panel, open `.env`. Replace its example values using the next instructions and save the file.

Replace the example values with the complete settings Brian provides. The file must contain both variable names:

```dotenv
MONGO_DBNAME=nyu_lost_found
MONGO_URI="mongodb+srv://<db_username>:<db_password>@<cluster_address>/"
```

The connection string above is a placeholder. Use the team's complete connection string, including its database username and password. Keep those credentials private.

Save the file as `.env` in the same folder as `app.py`. Confirm that the name is not `.env.txt`.

Check that Git ignores the private file:

```bash
git check-ignore .env
```

The expected output is `.env`. Commit only `env.example` with dummy values.

### 6. Check the database connection

With the project's environment still active, run:

```bash
python -c "from app import connection; connection.admin.command('ping'); print('MongoDB connected')"
```

Continue when `MongoDB connected` appears. If the command reports an error or keeps waiting for over a minute, press Control+C and use the troubleshooting table below.

### 7. Start the app and open it

Run:

```bash
python -m flask --app app run --port 5001
```

Wait for `Running on http://127.0.0.1:5001` to appear.

Keep the VS Code terminal running, then [open NYU Lost & Found in your browser](http://127.0.0.1:5001/).

Flask serves the HTML pages and handles their database operations. No separate frontend command is required.

The homepage shows the six newest reports. An empty database should show `No reports yet.` Use **Browse Items**, **Search Items**, and **Report Item** in the navigation.

### 8. Stop the app and start it again later

To stop the app, click its VS Code terminal and press Control+C. The command prompt should return.

For a later session, return to the same project folder, activate its environment, and start Flask.

For the default folder from step 2, on Mac or Linux:

```bash
cd ~/web-app-exercise
source .venv/bin/activate
python -m flask --app app run --port 5001
```

On Windows in Git Bash:

```bash
cd ~/web-app-exercise
source .venv/Scripts/activate
python -m flask --app app run --port 5001
```

If your project has a different location, use that folder instead. Your installed packages and `.env` remain available, so you do not need to repeat the first-time setup.

## Check the app

1. Submit a temporary report through **Report Item**. Complete every required field.
2. Check its confirmation and details. Confirm that the report also appears in Browse Items and Search Items.
3. Edit your temporary report and check the saved changes. Test the All, Lost, and Found filters.
4. Open Delete Report and select Cancel. Confirm that your report remains. Then delete that same temporary report through its confirmation page.

Each report requires the following fields:

- Status, either `lost` or `found`.
- Item name.
- Category.
- Item date in `YYYY-MM-DD` format.
- Location.
- Description.
- Contact information.

The server records the report's creation time. Editing preserves the report's ID and creation time.

No account is required. Any visitor can edit or delete a report, so use only your own temporary report when testing.

## Troubleshooting

| What you see | What to do |
|---|---|
| `python3`, `py`, or `git` is not recognized | Complete step 1, restart VS Code, and repeat the version checks. |
| `app.py`, `requirements.txt`, or `.automations/setup.py` cannot be found | Return to the project folder from step 2. Confirm the files with `ls`. |
| `No module named flask`, `pymongo`, or `dotenv` | Activate this project's `.venv` using step 4, then run `python -m pip install -r requirements.txt`. |
| `externally-managed-environment` during installation | Activate `.venv` first. Run installation through `python -m pip` as shown in step 4. |
| `MONGO_URI` or `MONGO_DBNAME` is missing | Check both names in the saved `.env` file beside `app.py`. Check that the file is not named `.env.txt`. |
| Authentication, SSL, connection, or timeout errors | Ask Brian to check the supplied credentials, active cluster, and your current IP address in Atlas. Recheck step 6. Do not disable TLS checks. |
| `Reports could not be loaded` | Flask is running, but the database request failed. Check the same Atlas settings and connection test. |
| Address already in use on port 5001 | Stop your earlier Flask server with Control+C. If the port belongs to another app, use `python -m flask --app app run --port 5002` and [open the app on port 5002](http://127.0.0.1:5002/). |
| The browser cannot connect | Keep Flask running and use the exact address and port printed in its command window. |
| The browser shows template text such as `{% extends ... %}` | Open the running app's HTTP address instead of opening an HTML file from the templates folder. |

## Team workflow

Work in a feature branch in this shared repository. Push the branch and open a pull request into the team's `main` branch. Another teammate must review, approve, and merge it.

Update the sprint boards as work starts, awaits review, and finishes. Keep `.env` private and share it with teammates and course admins through the required team messenger.

The app runs locally. Deployment is not required.

## Environment note

The setup uses `requirements.txt`. Its package versions are currently unpinned, so future installations may select different versions. The instructions define the setup order and checks, so make sure to check that you have identical package versions on every computer.
