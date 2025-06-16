"""SQLAlchemy data models for the DnD Notebook project."""

from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from .db import Base

# Association table linking campaigns and users
campaign_members = Table(
    "campaign_members",
    Base.metadata,
    Column("campaign_id", ForeignKey("campaigns.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    """Represents a player using the notebook."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    profile_picture_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    campaigns = relationship(
        "Campaign", secondary=campaign_members, back_populates="members"
    )
    dm_campaigns = relationship(
        "Campaign", back_populates="dm", foreign_keys="Campaign.dm_id"
    )
    notes = relationship("Note", back_populates="author")


class Campaign(Base):
    """A DnD campaign that groups notes and players."""

    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    dm_id = Column(Integer, ForeignKey("users.id"))

    dm = relationship("User", back_populates="dm_campaigns", foreign_keys=[dm_id])
    members = relationship(
        "User", secondary=campaign_members, back_populates="campaigns"
    )
    notes = relationship("Note", back_populates="campaign")


class Note(Base):
    """A note belonging to a campaign."""

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    image_url = Column(String)
    is_private = Column(Boolean, default=False)
    session_name = Column(String)
    session_date = Column(Date)
    session_number = Column(Integer)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    campaign = relationship("Campaign", back_populates="notes")
    author = relationship("User", back_populates="notes")
