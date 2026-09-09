from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str="TEAM_MEMBER"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    name: str
    description: str | None = None


class EventResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_by: int

    class Config:
        from_attributes = True


class AddMember(BaseModel):
    user_id: int

class GalleryCreate(BaseModel):
    event_id: int
    pin: str


class GalleryResponse(BaseModel):
    id: int
    event_id: int
    gallery_token: str
    is_published: bool

    class Config:
        from_attributes = True


class GalleryPinVerify(BaseModel):
    pin: str

class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8,max_length=100) 

class GalleryCreate(BaseModel):
    event_id: int
    pin: str = Field(min_length=4, max_length=10,pattern="^\\d+$")  # PIN must be numeric and between 4 to 10 digits

class GalleryPhoto(Base):
    __tablename__ = "gallery_photos"

    id = Column(Integer, primary_key=True)

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

    __table_args__ = (
        UniqueConstraint(
            "gallery_id",
            "photo_id",
            name="unique_gallery_photo"
        ),
    )