from typing import List, Optional

from fastapi.params import Query

from src.crud.user import user_crud
from src.crud.dict_table import dict_crud
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from src.core.security import get_password_hash
from src.api.dependecies.user import get_current_user
from src.api.dependecies.database import get_db_session
from src.schemas.user import UserResponse, UserUpdate, AvatarResponse, UserUpdateInternal
from src.utils import save_avatar
from src.schemas.event import Event
from src.crud.event import get_events_by_user_id

router = APIRouter(tags=["users"])

@router.get("/users", response_model=List[UserResponse])
async def read_users(session = Depends(get_db_session), skip: int = 0, limit: int = 100,
                     department_id: Optional[int] = Query(None),
                     position_id: Optional[int] = Query(None),
                     username: Optional[str] = Query(None)
                     ):
    """
    Retrieve users.
    """
    users = await user_crud.get_users(
        db=session,
        skip=skip,
        limit=limit,
        department_id=department_id,
        position_id=position_id,
        username=username
    )
    users_data = []
    for user in users:
        user_data = UserResponse(
            id=user.id,
            email=user.email,
            telephone=user.telephone,
            username=user.username,
            is_superuser=user.is_superuser,
            department=user.department.name,
            position=user.position.name,
            birth_date=user.birth_date,
            skills=user.skills,
            profile_image_url=user.profile_image_url,
            interests = [user_interest.interest.name for user_interest in user.interests])
        users_data.append(user_data)
    return users_data

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user_by_id(user_id: int, session = Depends(get_db_session)):
    """
    Retrieve user by id.
    """
    user = await user_crud.get_user_by_id(db=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=user.id,
        email=user.email,
        telephone=user.telephone,
        username=user.username,
        is_superuser=user.is_superuser,
        department=user.department.name,
        position=user.position.name,
        birth_date=user.birth_date,
        skills=user.skills,
        profile_image_url=user.profile_image_url,
        interests=[user_interest.interest.name for user_interest in user.interests]
    )


@router.get("/user/me", response_model=UserResponse)
async def read_user_me(user = Depends(get_current_user)):
    """
    Get current user.
    """
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        telephone=user.telephone,
        is_superuser=user.is_superuser,
        department=user.department.name,
        position=user.position.name,
        birth_date=user.birth_date,
        skills=user.skills,
        profile_image_url=user.profile_image_url,
        interests=[user_interest.interest.name for user_interest in user.interests]
    )
@router.patch("/user/me", response_model=UserResponse)
async def update_user_me(
    user_update: UserUpdate, session = Depends(get_db_session),  user = Depends(get_current_user)
):
    """
    Update own user.
    """
    if user_update.email:
        existing_user = await user_crud.get_user_by_email(db=session, email=user_update.email)
        if existing_user and existing_user.id != user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
    if user_update.password:
        user_update.password = get_password_hash(user_update.password)
    await user_crud.update_user(user=user, user_update=user_update, db=session)
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        telephone=user.telephone,
        is_superuser=user.is_superuser,
        department=user.department.name,
        position=user.position.name,
        birth_date=user.birth_date,
        skills=user.skills,
        profile_image_url=user.profile_image_url,
        interests=[user_interest.interest.name for user_interest in user.interests]
    )
@router.post("/user/me/avatar", response_model=AvatarResponse)
async def update_avatar(
        file: UploadFile = File(...),
        current_user = Depends(get_current_user),
        session = Depends(get_db_session)
):
    """
    Update user's avatar.
    """
    try:
        avatar_url = await save_avatar(file, current_user.id, current_user.profile_image_url)
        user_update = UserUpdateInternal(profile_image_url=avatar_url)
        updated_user = await user_crud.update_user(db=session, user=current_user, user_update=user_update)
        return AvatarResponse(profile_image_url=updated_user.profile_image_url)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during avatar upload: {str(e)}"
        )

@router.get("/user/me/events", response_model=List[Event])
async def get_user_events(
    session = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    """
    Get all events that the current user is registered for.
    """
    events = await get_events_by_user_id(db=session, user_id=current_user.id)
    events_data = []
    if not events:
        return []
    event_type = await dict_crud.get_event_types(db=session)
    event_type = {key[1]: value[1] for key,value in dict(event_type).items()}
    status_type = await dict_crud.get_status_types(db=session)
    status_type = {key[1]: value[1] for key, value in dict(status_type).items()}
    for event in events:
        # breakpoint()
        # event.interests[0].interest.name
        event_data = Event(
            id=event.id,
            name=event.name,
            description=event.description,
            event_type=event_type[event.event_type_id],
            start_time=event.start_time,
            end_time=event.end_time,
            status_event=status_type[event.status_id],
            place=event.place,
            organizator=event.organizator,
            interests=[interest.interest.name for event in events for interest in event.interests])
        events_data.append(event_data)
    return events_data

@router.delete("/user/{user_id}")
async def delete_user(
    user_id: int,
    session = Depends(get_db_session)
):
    """
    Get all events that the current user is registered for.
    """
    await user_crud.delete_user(db=session, user_id = user_id)
    return {"message": "User deleted"}

