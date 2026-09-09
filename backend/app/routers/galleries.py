import secrets

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
    Photo,
    Event
)
from ..schemas import (
    GalleryCreate,
    GalleryResponse,
    GalleryPinVerify
)
from ..auth import require_admin


router = APIRouter(
    prefix="/galleries",
    tags=["Galleries"]
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
@router.patch("/photos/{photo_id}/select")
def select_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):

    photo = db.query(Photo).filter(
        Photo.id == photo_id
    ).first()

    if not photo:
        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    event = db.query(Event).filter(
        Event.id == photo.event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this event"
        )

    photo.is_selected = True

    db.commit()
    db.refresh(photo)

    return {
        "message": "Photo selected",
        "photo_id": photo.id,
        "is_selected": photo.is_selected
    }

@router.patch("/photos/{photo_id}/unselect")
def unselect_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):

    photo = db.query(Photo).filter(
        Photo.id == photo_id
    ).first()

    if not photo:
        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    event = db.query(Event).filter(
        Event.id == photo.event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this event"
        )

    photo.is_selected = False

    db.commit()
    db.refresh(photo)

    return {
        "message": "Photo unselected",
        "photo_id": photo.id,
        "is_selected": photo.is_selected
    }
@router.post(
    "/",
    response_model=GalleryResponse
)
def create_gallery(
    gallery: GalleryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):

    event = db.query(Event).filter(
        Event.id == gallery.event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not own this event"
        )

    if len(gallery.pin) < 4:
        raise HTTPException(
            status_code=400,
            detail="PIN must contain at least 4 digits"
        )

    selected_photos = db.query(Photo).filter(
        Photo.event_id == gallery.event_id,
        Photo.is_selected == True
    ).all()

    if not selected_photos:
        raise HTTPException(
            status_code=400,
            detail="Select at least one photo"
        )

    gallery_token = secrets.token_urlsafe(16)

    pin_hash = pwd_context.hash(
        gallery.pin
    )

    new_gallery = Gallery(
        event_id=gallery.event_id,
        gallery_token=gallery_token,
        pin_hash=pin_hash,
        is_published=False
    )

    db.add(new_gallery)
    db.flush()

    for photo in selected_photos:

        gallery_photo = GalleryPhoto(
            gallery_id=new_gallery.id,
            photo_id=photo.id
        )

        db.add(gallery_photo)

    db.commit()
    db.refresh(new_gallery)

    return new_gallery

@router.patch("/{gallery_id}/publish")
def publish_gallery(
    gallery_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):

    gallery = db.query(Gallery).filter(
        Gallery.id == gallery_id
    ).first()

    if not gallery:
        raise HTTPException(
            status_code=404,
            detail="Gallery not found"
        )

    event = db.query(Event).filter(
        Event.id == gallery.event_id
    ).first()

    if event.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not own this gallery"
        )

    gallery.is_published = True

    db.commit()
    db.refresh(gallery)

    return {
        "message": "Gallery published successfully",
        "gallery_id": gallery.id,
        "gallery_token": gallery.gallery_token,
        "is_published": gallery.is_published
    }