# DnD Notebook Backend

This project provides a backend for a collaborative Dungeons & Dragons note taking application. It uses a simple SQLite database via SQLAlchemy and exposes an HTTP API with FastAPI. Notes can include optional images and session details while users may have profile pictures.

Run the server with::

    uvicorn backend.views:app --reload

Create the database tables using::

    from backend import create_tables
    create_tables()

## Frontend

Open `frontend/login.html` in your browser after starting the backend. The login page will authenticate a user and redirect to `notes.html` where you can create campaigns and notes. Both pages include a theme toggle for light or dark mode.
