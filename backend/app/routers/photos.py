import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import (
    Photo,
    Event,
    EventMember,
    User
)

from ..auth import get_current_user
from fastapi.responses import FileResponse
from ..storage import upload_photo




router = APIRouter(
    prefix="/photos",
    tags=["Photos"]
)


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}
@router.post("/upload/{event_id}")
async def upload_photo(
    event_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Only Team Members can upload
    if current_user.role != "TEAM_MEMBER":
        raise HTTPException(
            status_code=403,
            detail="Only team members can upload photos"
        )

    # Check event
    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    # Check assignment
    membership = db.query(EventMember).filter(
        EventMember.event_id == event_id,
        EventMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this event"
        )

    # Check extension
    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, PNG and WEBP files are allowed"
        )

    # Generate unique filename
    unique_filename = (
        f"{uuid.uuid4()}{extension}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    # Save file
    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # Save metadata
    photo = Photo(
        event_id=event_id,
        uploaded_by=current_user.id,
        filename=file.filename,
        storage_location=file_path,
        file_size=len(contents),
        is_selected=False
    )

    db.add(photo)
    db.commit()
    db.refresh(photo)

    return {
        "message": "Photo uploaded successfully",
        "photo_id": photo.id,
        "filename": photo.filename,
        "size": photo.file_size
    }
@router.post("/upload-multiple/{event_id}")
async def upload_multiple_photos(
    event_id: int,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "TEAM_MEMBER":
        raise HTTPException(
            status_code=403,
            detail="Only team members can upload photos"
        )

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    membership = db.query(EventMember).filter(
        EventMember.event_id == event_id,
        EventMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this event"
        )

    uploaded_photos = []

    for file in files:

        extension = os.path.splitext(
            file.filename
        )[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            continue

        unique_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            unique_filename
        )

        contents = await file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        photo = Photo(
            event_id=event_id,
            uploaded_by=current_user.id,
            filename=file.filename,
            storage_location=file_path,
            file_size=len(contents),
            is_selected=False
        )

        db.add(photo)

        uploaded_photos.append({
            "filename": file.filename,
            "size": len(contents)
        })

    db.commit()

    return {
        "message": "Photos uploaded successfully",
        "count": len(uploaded_photos),
        "photos": uploaded_photos
    }
@router.get("/my-photos/{event_id}")
def get_my_photos(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "TEAM_MEMBER":
        raise HTTPException(
            status_code=403,
            detail="Only team members can use this endpoint"
        )

    membership = db.query(EventMember).filter(
        EventMember.event_id == event_id,
        EventMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this event"
        )

    photos = db.query(Photo).filter(
        Photo.event_id == event_id,
        Photo.uploaded_by == current_user.id
    ).all()

    return photos

@router.get("/event/{event_id}")
def get_event_photos(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if current_user.role == "ADMIN":

        if event.created_by != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You do not have access to this event"
            )

        photos = db.query(Photo).filter(
            Photo.event_id == event_id
        ).all()

        return photos

    # Team Member
    membership = db.query(EventMember).filter(
        EventMember.event_id == event_id,
        EventMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this event"
        )

    photos = db.query(Photo).filter(
        Photo.event_id == event_id,
        Photo.uploaded_by == current_user.id
    ).all()

    return photos

@router.get("/file/{photo_id}")
def get_photo_file(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    photo = db.query(Photo).filter(
        Photo.id == photo_id
    ).first()

    if not photo:
        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )


    # Admin can access photos belonging
    # to their own events
    if current_user.role == "ADMIN":

        event = db.query(Event).filter(
            Event.id == photo.event_id
        ).first()

        if not event or event.created_by != current_user.id:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )


    # Team Member can access only
    # their own uploaded photo
    elif current_user.role == "TEAM_MEMBER":

        if photo.uploaded_by != current_user.id:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )


    if not os.path.exists(
        photo.storage_location
    ):

        raise HTTPException(
            status_code=404,
            detail="Photo file not found"
        )


    return FileResponse(
        photo.storage_location
    )
