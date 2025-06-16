# DnD Notebook Backend

This project provides a backend for a collaborative Dungeons & Dragons note taking application.
It uses a simple SQLite database via SQLAlchemy for storage and defines models for campaigns,
users and notes. Notes may include an image URL and users can have profile
pictures associated with their accounts. Notes also track session information
(`session_name`, `session_date`, `session_number`) and a `category` field.

An HTTP API is provided using FastAPI. Run the server with::

    uvicorn backend.views:app --reload

To create the database tables run the following in a Python shell:

```python
from backend import create_tables
create_tables()
```

## Frontend

A minimal JavaScript frontend lives in the `frontend` directory. Start the
backend server and then open `frontend/index.html` in your browser. The page
offers simple forms for creating users, campaigns and notes through the HTTP
API. A "Load Notes" button retrieves stored notes and displays them on the page.
