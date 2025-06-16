"""Controller functions handling business logic for the notebook."""

from datetime import date
from sqlalchemy.orm import Session

from .models import User, Campaign, Note


def create_user(
    db: Session,
    username: str,
    hashed_password: str,
    profile_picture_url: str | None = None,
) -> User:
    """Create and persist a new user."""
    user = User(
        username=username,
        hashed_password=hashed_password,
        profile_picture_url=profile_picture_url,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, **fields) -> User:
    """Update an existing user by ID."""
    user = db.get(User, user_id)
    if user is None:
        raise ValueError("User not found")
    for key, value in fields.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def create_campaign(db: Session, name: str, description: str | None = None) -> Campaign:
    """Create and persist a new campaign."""
    campaign = Campaign(name=name, description=description)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def update_campaign(db: Session, campaign_id: int, **fields) -> Campaign:
    """Update an existing campaign."""
    campaign = db.get(Campaign, campaign_id)
    if campaign is None:
        raise ValueError("Campaign not found")
    for key, value in fields.items():
        setattr(campaign, key, value)
    db.commit()
    db.refresh(campaign)
    return campaign


def create_note(
    db: Session,
    campaign_id: int,
    author_id: int,
    title: str,
    body: str,
    image_url: str | None = None,
    is_private: bool = False,
    session_name: str | None = None,
    session_date: date | None = None,
    session_number: int | None = None,
    category: str | None = None,
) -> Note:
    """Create and persist a new note."""
    note = Note(
        campaign_id=campaign_id,
        author_id=author_id,
        title=title,
        body=body,
        image_url=image_url,
        is_private=is_private,
        session_name=session_name,
        session_date=session_date,
        session_number=session_number,
        category=category,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update_note(db: Session, note_id: int, **fields) -> Note:
    """Update an existing note."""
    note = db.get(Note, note_id)
    if note is None:
        raise ValueError("Note not found")
    for key, value in fields.items():
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note


def list_notes(db: Session, campaign_id: int | None = None) -> list[Note]:
    """Return all notes, optionally filtered by campaign."""
    query = db.query(Note)
    if campaign_id is not None:
        query = query.filter(Note.campaign_id == campaign_id)
    return query.all()
