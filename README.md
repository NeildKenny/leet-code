# DnD Notebook Backend

This project provides a backend for a collaborative Dungeons & Dragons note taking application. It uses a simple SQLite database via SQLAlchemy and exposes an HTTP API with FastAPI. Notes can include optional images and session details while users may have profile pictures.

Run the server with::

    ./start.sh

The backend starts on http://localhost:8001 by default.

Logs are printed to the console at INFO level to aid debugging.

Cross-origin requests are allowed so the JavaScript frontend can call the API
from another origin (for example when opening the HTML files directly from
disk).

Create the database tables using::

    from backend import create_tables
    create_tables()

## Setup

Use `setup.sh` to prepare a Python virtual environment and install
all dependencies on Linux Mint::

    ./setup.sh

Once the environment is created, you can start the service using
`start.sh` as shown above.

## API Testing

Run `test_api.sh` to exercise the HTTP endpoints using `curl`. The script
registers a demo user, creates a campaign, posts a note and finally lists
all notes. Sample payloads are included directly in the curl commands so
you can see exactly what data is sent. It requires `jq` for parsing JSON
output::

    sudo apt-get install -y jq
    ./test_api.sh

## Registration

Create a new account by sending a POST request to `/register` (or `/users`) with
`username` and `password` parameters. Passwords are stored using bcrypt hashes.

## Frontend

Open `frontend/login.html` in your browser after starting the backend. From there you can navigate to the registration page to create an account. After either logging in or completing registration you are taken to `notes.html` where you can create campaigns and notes. All pages include a theme toggle for light or dark mode.
