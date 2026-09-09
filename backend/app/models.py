from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(100),
        nullable=False,
        default="TEAM_MEMBER"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(200),
        nullable=False
    )

    description = Column(
        String(1000),
        nullable=True
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class EventMember(Base):
    __tablename__ = "event_members"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


class Photo(Base):
    __tablename__ = "photos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    filename = Column(
        String(255),
        nullable=False
    )

    storage_location = Column(
        String(500),
        nullable=False
    )

    file_size = Column(
        Integer,
        nullable=False
    )

    is_selected = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
class Gallery(Base):
    __tablename__ = "galleries"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )

    gallery_token = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    pin_hash = Column(
        String(255),
        nullable=False
    )

    is_published = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class GalleryPhoto(Base):
    __tablename__ = "gallery_photos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    gallery_id = Column(
        Integer,
        ForeignKey("galleries.id"),
        nullable=False
    )

    photo_id = Column(
        Integer,
        ForeignKey("photos.id"),
        nullable=False
    )

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    filename = Column(
        String(255),
        nullable=False
    )

    storage_location = Column(
        String(500),
        nullable=False
    )

    cloudinary_public_id = Column(
        String(255),
        nullable=True
    )

    file_size = Column(
        Integer,
        nullable=False
    )

    is_selected = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )