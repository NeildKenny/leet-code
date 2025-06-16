"""HTTP API endpoints for the DnD Notebook backend."""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import date

from .db import SessionLocal, create_tables
from .controllers import (
    create_user,
    update_user,
    create_campaign,
    update_campaign,
    create_note,
    update_note,
    list_notes,
)
from .models import User, Campaign, Note

app = FastAPI(title="DnD Notebook API")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    create_tables()


@app.post("/users", response_model=dict)
def api_create_user(
    username: str,
    password: str,
    profile_picture_url: str | None = None,
    db: Session = Depends(get_db),
):
    user = create_user(
        db,
        username=username,
        hashed_password=password,
        profile_picture_url=profile_picture_url,
    )
    return {"id": user.id, "username": user.username}


@app.put("/users/{user_id}", response_model=dict)
def api_update_user(
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    profile_picture_url: str | None = None,
    db: Session = Depends(get_db),
):
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
def api_create_campaign(name: str, description: str | None = None, db: Session = Depends(get_db)):
    campaign = create_campaign(db, name=name, description=description)
    return {"id": campaign.id, "name": campaign.name, "description": campaign.description}


@app.put("/campaigns/{campaign_id}", response_model=dict)
def api_update_campaign(campaign_id: int, name: str | None = None, description: str | None = None, db: Session = Depends(get_db)):
    fields = {}
    if name is not None:
        fields["name"] = name
    if description is not None:
        fields["description"] = description
    try:
        campaign = update_campaign(db, campaign_id, **fields)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"id": campaign.id, "name": campaign.name, "description": campaign.description}


@app.post("/notes", response_model=dict)
def api_create_note(
    campaign_id: int,
    author_id: int,
    title: str,
    body: str,
    image_url: str | None = None,
    is_private: bool = False,
    session_name: str | None = None,
    session_date: str | None = None,
    session_number: int | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
):
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
    title: str | None = None,
    body: str | None = None,
    image_url: str | None = None,
    is_private: bool | None = None,
    session_name: str | None = None,
    session_date: str | None = None,
    session_number: int | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
):
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
