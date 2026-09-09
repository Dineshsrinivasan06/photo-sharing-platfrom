from fastapi import APIRouter, Depends

from ..auth import (
    get_current_user,
    require_admin,
    require_team_member
)
from ..models import User


router = APIRouter(
    prefix="/protected",
    tags=["Protected"]
)


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }


@router.get("/admin")
def admin_only(
    current_user: User = Depends(require_admin)
):

    return {
        "message": "Welcome Admin!",
        "user": current_user.name
    }


@router.get("/team")
def team_only(
    current_user: User = Depends(require_team_member)
):

    return {
        "message": "Welcome Team Member!",
        "user": current_user.name
    }