from fastapi import APIRouter, HTTPException, Path, status
from typing import List

from models import User, UserCreate
from storage import storage


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):

    for existing_user in storage.user.values():
        if existing_user['email'] == user.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already resgistered")
    new_user = storage.create_user(user.dict())
    return new_user
    
@router.get("/", response_model=List[User])
def read_user():
    return list(storage.user.values())

@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int = Path(..., gt=0, description="The ID the user to retriev")
):
    user = storage.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user: UserCreate
):
    existing_user = storage.get_user(user_id)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="User not found")
    updated_user = storage.update_user(user_id, user.dict())
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if not storage.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None

@router.put("/{user_id}/deactivate", response_model=User)
def deactivate_user(user_id: int):
    user = storage.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    updated_user = storage.update_user(user_id, {"is_active": False})
    return updated_user