from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Event, EventMember, User
from ..schemas import EventCreate, EventResponse, AddMember
from ..auth import get_current_user, require_admin


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.post(
    "/",
    response_model=EventResponse
)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    new_event = Event(
        name=event.name,
        description=event.description,
        created_by=current_user.id
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

@router.get(
    "/{event_id}",
    response_model=EventResponse
)
def get_event(
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

    # Admin who created the event can access it
    if current_user.role == "ADMIN":

        if event.created_by != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You do not have access to this event"
            )

        return event

    # Check Team Member assignment
    membership = db.query(EventMember).filter(
        EventMember.event_id == event_id,
        EventMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this event"
        )

    return event

@router.post(
    "/{event_id}/members"
)
def add_team_member(
    event_id: int,
    member: AddMember,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    event = db.query(Event).filter(
        Event.id == event_id
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

    user = db.query(User).filter(
        User.id == member.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role != "TEAM_MEMBER":
        raise HTTPException(
            status_code=400,
            detail="Only team members can be assigned"
        )

    existing = db.query(EventMember).filter(
        EventMember.event_id == event_id,
        EventMember.user_id == member.user_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already assigned to this event"
        )

    assignment = EventMember(
        event_id=event_id,
        user_id=member.user_id
    )

    db.add(assignment)
    db.commit()

    return {
        "message": "Team member added successfully"
    }

@router.get("/")
def get_my_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role == "ADMIN":

        events = db.query(Event).filter(
            Event.created_by == current_user.id
        ).all()

    else:

        events = (
            db.query(Event)
            .join(
                EventMember,
                Event.id == EventMember.event_id
            )
            .filter(
                EventMember.user_id == current_user.id
            )
            .all()
        )

    return events

