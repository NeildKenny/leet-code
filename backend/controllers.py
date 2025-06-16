
"""Controller functions handling business logic for the notebook."""

from datetime import date
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import logging

from .models import User, Campaign, Note

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return a bcrypt hash for the given password."""
    logger.debug("Hashing password")
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against an existing hash."""
    logger.debug("Verifying password for hash")
    return pwd_context.verify(password, hashed)


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """Return a user if the credentials match."""
    logger.debug("Authenticating user %s", username)
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def create_user(
    db: Session,
    username: str,
    password: str,
    profile_picture_url: str | None = None,
) -> User:
    """Create and persist a new user."""
    logger.debug("Creating user %s", username)
    user = User(
        username=username,
        hashed_password=hash_password(password),
        profile_picture_url=profile_picture_url,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, **fields) -> User:
    """Update an existing user by ID."""
    logger.debug("Updating user %s with %s", user_id, fields)
    user = db.get(User, user_id)
    if user is None:
        raise ValueError("User not found")
    for key, value in fields.items():
        if key == "hashed_password":
            value = hash_password(value)
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def create_campaign(db: Session, name: str, description: str | None = None) -> Campaign:
    """Create and persist a new campaign."""
    logger.debug("Creating campaign %s", name)
    campaign = Campaign(name=name, description=description)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def update_campaign(db: Session, campaign_id: int, **fields) -> Campaign:
    """Update an existing campaign."""
    logger.debug("Updating campaign %s with %s", campaign_id, fields)
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
    logger.debug(
        "Creating note for campaign %s by author %s", campaign_id, author_id
    )
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
    logger.debug("Updating note %s with %s", note_id, fields)
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
    logger.debug("Listing notes for campaign %s", campaign_id)
    query = db.query(Note)
    if campaign_id is not None:
        query = query.filter(Note.campaign_id == campaign_id)
    return query.all()
