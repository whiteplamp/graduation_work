from fastapi import APIRouter, Depends, HTTPException, status

from src.core.db import database
from src.core.security import get_current_user, get_password_hash, verify_password
from src.models import User
from src.schemas import ChangePasswordRequest, ProfileUpdate, UserOut

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)


@router.put("", response_model=UserOut)
def update_profile(data: ProfileUpdate, current_user: User = Depends(get_current_user)):
    with database.atomic():
        current_user.name = data.name
        current_user.email = data.email
        current_user.save()
        return UserOut.model_validate(current_user)


@router.post("/change-password", status_code=204)
def change_password(body: ChangePasswordRequest, current_user: User = Depends(get_current_user)):
    if body.newPassword != body.newPasswordConfirmation:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    with database.atomic():
        if not verify_password(body.currentPassword, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )
        current_user.hashed_password = get_password_hash(body.newPassword)
        current_user.save()
    return


