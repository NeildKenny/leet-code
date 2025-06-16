# DnD Notebook Backend

This project provides a backend for a collaborative Dungeons & Dragons note taking application. It uses a simple SQLite database via SQLAlchemy and exposes an HTTP API with FastAPI. Notes can include optional images and session details while users may have profile pictures.

Run the server with::

    ./start.sh

Create the database tables using::

    from backend import create_tables
    create_tables()

## Setup

Use `setup.sh` to prepare a Python virtual environment and install
all dependencies on Linux Mint::

    ./setup.sh

Once the environment is created, you can start the service using
`start.sh` as shown above.

## Frontend

Open `frontend/login.html` in your browser after starting the backend. The login page will authenticate a user and redirect to `notes.html` where you can create campaigns and notes. Both pages include a theme toggle for light or dark mode.
