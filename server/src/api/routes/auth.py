from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.user import UserCreate, UserLogin, UserUpdate, UserPasswordReset
from src.schemas.auth import  Message, Token
from src.api.dependecies.database import get_db_session, get_redis_session
from src.crud.user import user_crud
from src.core.security import create_access_token, verify_password, get_password_hash
from src.redis_client.service import redis_service
from src.mail import mail
from src.mail import generate_reset_password_email

router = APIRouter(prefix="", tags=["auth"])

@router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session = Depends(get_db_session)):
    user = await user_crud.get_user_by_email(email=form_data.username, db=session)
    if user:
        if verify_password(form_data.password, user.hashed_password):
            return Token(access_token=create_access_token(user.email), token_type="bearer")
    raise HTTPException(status_code=400, detail="Incorrect email or password")

# @router.post('/login')
# async def login(user_login: UserLogin, session = Depends(get_db_session)):
#     user = await user_crud.get_user_by_email(email=user_login.email, db=session)
#     if user:
#         if verify_password(user_login.password, user.hashed_password):
#             return Token(access_token=create_access_token(user.email), token_type="bearer")
#     raise HTTPException(status_code=400, detail="Incorrect email or password")
@router.post('/register')
async def confirm_registration(user_create: UserCreate,
                               session=Depends(get_db_session)) -> Message:
    await user_crud.create_user(user_create=user_create, db=session)

    return Message(message="Registration successful")

@router.post("/password-reset")
async def reset_password(email: str,
                           session = Depends(get_db_session)) -> Message:
    user = await user_crud.get_user_by_email(email=email, db=session)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )

    reset_code = await redis_service.create_reset_code(email=user.email, ttl=240)

    message = generate_reset_password_email(
        recipients=[user.email], code=reset_code
    )
    await mail.send_message(message)
    return Message(message="Password recovery email sent")

@router.post("/password-reset/verify")
async def confirm_password_reset(user_reset: UserPasswordReset,
                                 session = Depends(get_db_session)) -> Message:
    user = await user_crud.get_user_by_email(email=user_reset.email, db=session)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    stored_code = await redis_service.get_reset_code(email=user_reset.email)
    if not stored_code or stored_code != user_reset.code:
        raise HTTPException(status_code=400, detail="Invalid reset code")
    if user_reset.new_password != user_reset.confirm_new_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    user_update = UserUpdate(password = get_password_hash(user_reset.new_password))
    await user_crud.update_user(user=user, user_update=user_update, db=session)
    await redis_service.delete_reset_code(email=user.email)
    return Message(message="Password reset successful")