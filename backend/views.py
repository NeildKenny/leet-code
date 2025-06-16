"""HTTP API endpoints for the DnD Notebook backend."""

from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date
import logging

from .db import SessionLocal, create_tables
from .controllers import (
    create_user,
    update_user,
    create_campaign,
    update_campaign,
    add_user_to_campaign,
    list_campaigns,
    create_note,
    update_note,
    list_notes,
    authenticate_user,
)
from .models import User, Campaign, Note

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DnD Notebook API")

# Allow cross-origin requests so the browser-based frontend can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Creating database tables")
    create_tables()


@app.post("/users", response_model=dict)
def api_create_user(
    username: str = Form(...),
    password: str = Form(...),
    profile_picture_url: str | None = Form(None),
    db: Session = Depends(get_db),
):
    logger.info("POST /users user=%s", username)
    user = create_user(
        db,
        username=username,
        password=password,
        profile_picture_url=profile_picture_url,
    )
    return {"id": user.id, "username": user.username}


@app.post("/register", response_model=dict)
def api_register(
    username: str = Form(...),
    password: str = Form(...),
    profile_picture_url: str | None = Form(None),
    db: Session = Depends(get_db),
):
    """Alias endpoint for user registration."""
    logger.info("POST /register user=%s", username)
    user = create_user(
        db,
        username=username,
        password=password,
        profile_picture_url=profile_picture_url,
    )
    return {"id": user.id, "username": user.username}


@app.post("/login", response_model=dict)
def api_login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    logger.info("POST /login user=%s", username)
    user = authenticate_user(db, username=username, password=password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": user.id, "username": user.username}


@app.put("/users/{user_id}", response_model=dict)
def api_update_user(
    user_id: int,
    username: str | None = Form(None),
    password: str | None = Form(None),
    profile_picture_url: str | None = Form(None),
    db: Session = Depends(get_db),
):
    logger.info("PUT /users/%s", user_id)
    fields = {}
    if username is not None:
        fields["username"] = username
    if password is not None:
        fields["hashed_password"] = password
    if profile_picture_url is not None:
        fields["profile_picture_url"] = profile_picture_url
    try:
        user = update_user(db, user_id, **fields)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"id": user.id, "username": user.username}


@app.post("/campaigns", response_model=dict)
def api_create_campaign(
    name: str = Form(...),
    description: str | None = Form(None),
    dm_id: int | None = Form(None),
    db: Session = Depends(get_db),
):
    logger.info("POST /campaigns name=%s", name)
    campaign = create_campaign(db, name=name, description=description, dm_id=dm_id)
    return {
        "id": campaign.id,
        "name": campaign.name,
        "description": campaign.description,
        "dm_id": campaign.dm_id,
    }


@app.put("/campaigns/{campaign_id}", response_model=dict)
def api_update_campaign(
    campaign_id: int,
    name: str | None = Form(None),
    description: str | None = Form(None),
    dm_id: int | None = Form(None),
    db: Session = Depends(get_db),
):
    logger.info("PUT /campaigns/%s", campaign_id)
    fields = {}
    if name is not None:
        fields["name"] = name
    if description is not None:
        fields["description"] = description
    if dm_id is not None:
        fields["dm_id"] = dm_id
    try:
        campaign = update_campaign(db, campaign_id, **fields)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {
        "id": campaign.id,
        "name": campaign.name,
        "description": campaign.description,
        "dm_id": campaign.dm_id,
    }


@app.post("/campaigns/{campaign_id}/join", response_model=dict)
def api_join_campaign(
    campaign_id: int,
    user_id: int = Form(...),
    db: Session = Depends(get_db),
):
    logger.info("POST /campaigns/%s/join user=%s", campaign_id, user_id)
    try:
        add_user_to_campaign(db, campaign_id, user_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"status": "joined"}


@app.get("/campaigns", response_model=list[dict])
def api_list_campaigns(user_id: int | None = None, db: Session = Depends(get_db)):
    logger.info("GET /campaigns user_id=%s", user_id)
    campaigns = list_campaigns(db, user_id=user_id)
    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "dm_id": c.dm_id,
        }
        for c in campaigns
    ]


@app.post("/notes", response_model=dict)
def api_create_note(
    campaign_id: int = Form(...),
    author_id: int = Form(...),
    title: str = Form(...),
    body: str = Form(...),
    image_url: str | None = Form(None),
    is_private: bool = Form(False),
    session_name: str | None = Form(None),
    session_date: str | None = Form(None),
    session_number: int | None = Form(None),
    category: str | None = Form(None),
    db: Session = Depends(get_db),
):
    logger.info("POST /notes campaign=%s author=%s", campaign_id, author_id)
    note = create_note(
        db,
        campaign_id=campaign_id,
        author_id=author_id,
        title=title,
        body=body,
        image_url=image_url,
        is_private=is_private,
        session_name=session_name,
        session_date=date.fromisoformat(session_date) if session_date else None,
        session_number=session_number,
        category=category,
    )
    return {"id": note.id, "title": note.title, "is_private": note.is_private}


@app.put("/notes/{note_id}", response_model=dict)
def api_update_note(
    note_id: int,
    title: str | None = Form(None),
    body: str | None = Form(None),
    image_url: str | None = Form(None),
    is_private: bool | None = Form(None),
    session_name: str | None = Form(None),
    session_date: str | None = Form(None),
    session_number: int | None = Form(None),
    category: str | None = Form(None),
    db: Session = Depends(get_db),
):
    logger.info("PUT /notes/%s", note_id)
    fields = {}
    if title is not None:
        fields["title"] = title
    if body is not None:
        fields["body"] = body
    if is_private is not None:
        fields["is_private"] = is_private
    if image_url is not None:
        fields["image_url"] = image_url
    if session_name is not None:
        fields["session_name"] = session_name
    if session_date is not None:
        fields["session_date"] = date.fromisoformat(session_date)
    if session_number is not None:
        fields["session_number"] = session_number
    if category is not None:
        fields["category"] = category
    try:
        note = update_note(db, note_id, **fields)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"id": note.id, "title": note.title, "is_private": note.is_private}


@app.get("/notes", response_model=list[dict])
def api_list_notes(campaign_id: int | None = None, db: Session = Depends(get_db)):
    """Return all notes, optionally filtered by campaign ID."""
    logger.info("GET /notes campaign=%s", campaign_id)
    notes = list_notes(db, campaign_id=campaign_id)
    return [
        {
            "id": n.id,
            "campaign_id": n.campaign_id,
            "author_id": n.author_id,
            "title": n.title,
            "body": n.body,
            "image_url": n.image_url,
            "is_private": n.is_private,
            "session_name": n.session_name,
            "session_date": n.session_date.isoformat() if n.session_date else None,
            "session_number": n.session_number,
            "category": n.category,
        }
        for n in notes
    ]
