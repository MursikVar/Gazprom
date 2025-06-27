from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.api.dependecies.database import get_db_session
from src.core.security import verify_access_token
from src.crud.user import user_crud
from src.database import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
async def get_current_user(session = Depends(get_db_session), token = Depends(oauth2_scheme)) -> User:
    email = verify_access_token(token)
    user = await user_crud.get_user_by_email(email, db=session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_active_superuser(user= Depends(get_current_user)) -> User:
    if not user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return user

