from typing import List, Optional
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.user import user_crud
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from src.core.security import get_password_hash
from src.api.dependecies.user import get_current_user
from src.api.dependecies.database import get_db_session
from src.schemas.user import UserResponse, UserUpdate, AvatarResponse, UserUpdateInternal
from src.schemas.dict_table import DepartmentResponse, PositionResponse
from src.utils import save_avatar
from src.crud.dict_table import dict_crud

router = APIRouter(tags=["Dicts"])
@router.get("/departments", response_model=List[DepartmentResponse])
async def get_departments(session: AsyncSession = Depends(get_db_session)):
    """
    Получить список всех департаментов.
    """
    return await dict_crud.get_departments(db=session)
@router.get("/positions", response_model=List[PositionResponse])
async def get_positions(session: AsyncSession = Depends(get_db_session)):
    """
    Получить список всех должностей.
    """
    return await dict_crud.get_positions(db = session)

@router.get("/interests", response_model=List[PositionResponse])
async def get_interests(session: AsyncSession = Depends(get_db_session)):
    """
    Получить список всех интересов.
    """
    return await dict_crud.get_interests(db = session)

@router.get("/event_types", response_model=List[PositionResponse])
async def get_event_types(session: AsyncSession = Depends(get_db_session)):
    """
    Получить список видов мероприятий.
    """
    return await dict_crud.get_event_types(db = session)

@router.get("/priorities", response_model=List[PositionResponse])
async def get_priorities(session: AsyncSession = Depends(get_db_session)):
    """
    Получить список существующих приоритетов.
    """
    return await dict_crud.get_priorities(db = session)