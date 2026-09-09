from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..database import get_db
from ..models import (
    Gallery,
    GalleryPhoto,
    Photo
)
from ..schemas import GalleryPinVerify
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import HTTPBearer
from fastapi import Security
from ..config import settings
import os


router = APIRouter(
    prefix="/gallery",
    tags=["Customer Gallery"]
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

security = HTTPBearer()
GALLERY_SECRET_KEY = settings.GALLERY_SECRET_KEY
GALLERY_ALGORITHM = "HS256"

def verify_gallery_access(
    credentials=Security(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            GALLERY_SECRET_KEY,
            algorithms=[GALLERY_ALGORITHM]
        )

        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired gallery access token"
        )

@router.get("/{gallery_token}")
def get_gallery(
    gallery_token: str,
    db: Session = Depends(get_db)
):

    gallery = db.query(Gallery).filter(
        Gallery.gallery_token == gallery_token
    ).first()

    if not gallery:
        raise HTTPException(
            status_code=404,
            detail="Gallery not found"
        )

    if not gallery.is_published:
        raise HTTPException(
            status_code=403,
            detail="Gallery is not published"
        )

    return {
        "gallery_id": gallery.id,
        "event_id": gallery.event_id,
        "message": "Gallery found. PIN required."
    }
@router.post("/{gallery_token}/verify")
def verify_gallery_pin(
    gallery_token: str,
    data: GalleryPinVerify,
    db: Session = Depends(get_db)
):

    gallery = db.query(Gallery).filter(
        Gallery.gallery_token == gallery_token
    ).first()

    if not gallery:
        raise HTTPException(
            status_code=404,
            detail="Gallery not found"
        )

    if not gallery.is_published:
        raise HTTPException(
            status_code=403,
            detail="Gallery is not published"
        )

    valid_pin = pwd_context.verify(
        data.pin,
        gallery.pin_hash
    )

    if not valid_pin:
        raise HTTPException(
            status_code=401,
            detail="Incorrect PIN"
        )

    return {
        "message": "PIN verified successfully",
        "gallery_token": gallery.gallery_token
    }
@router.get("/{gallery_token}/photos")
def get_gallery_photos(
    gallery_token: str,
    db: Session = Depends(get_db),
    gallery_access= Depends(verify_gallery_access)
):
    if gallery_access.get("gallery_token") != gallery_token:
        raise HTTPException(
            status_code=403,
            detail="Gallery access denied"
        )

    gallery = db.query(Gallery).filter(
        Gallery.gallery_token == gallery_token
    ).first()

    if not gallery:
        raise HTTPException(
            status_code=404,
            detail="Gallery not found"
        )

    if not gallery.is_published:
        raise HTTPException(
            status_code=403,
            detail="Gallery is not published"
        )

    gallery_photos = (
        db.query(
            GalleryPhoto,
            Photo
        )
        .join(
            Photo,
            GalleryPhoto.photo_id == Photo.id
        )
        .filter(
            GalleryPhoto.gallery_id == gallery.id
        )
        .all()
    )

    return [
        {
            "photo_id": photo.id,
            "filename": photo.filename,
            "storage_location": photo.storage_location
        }
        for gallery_photo, photo in gallery_photos
    ]
@router.post("/{gallery_token}/verify")
def verify_gallery_pin(
    gallery_token: str,
    data: GalleryPinVerify,
    db: Session = Depends(get_db)
):

    gallery = db.query(Gallery).filter(
        Gallery.gallery_token == gallery_token
    ).first()

    if not gallery:
        raise HTTPException(
            status_code=404,
            detail="Gallery not found"
        )

    if not gallery.is_published:
        raise HTTPException(
            status_code=403,
            detail="Gallery is not published"
        )

    valid_pin = pwd_context.verify(
        data.pin,
        gallery.pin_hash
    )

    if not valid_pin:
        raise HTTPException(
            status_code=401,
            detail="Incorrect PIN"
        )

    expire = datetime.utcnow() + timedelta(
        minutes=30
    )

    access_token = jwt.encode(
        {
            "gallery_id": gallery.id,
            "gallery_token": gallery.gallery_token,
            "exp": expire
        },
        GALLERY_SECRET_KEY,
        algorithm=GALLERY_ALGORITHM
    )

    return {
        "message": "PIN verified successfully",
        "access_token": access_token
    }
