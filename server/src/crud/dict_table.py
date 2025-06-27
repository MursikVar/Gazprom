from typing import List, Optional

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.core.security import get_password_hash
from src.database import User, UserInterest, Interest
from src.schemas.user import UserCreate, UserUpdateInternal
from src.schemas.dict_table import PositionResponse, DepartmentResponse, InterestResponse
from src.database import Department, Position, Interest, EventType, Priority, StatusEvent

class DictTablesCRUD():
    async def get_departments(self, db: AsyncSession):
        """
        Получить список всех департаментов.
        """
        stmt = sqlalchemy.select(Department)
        query = await db.execute(stmt)
        departments = query.scalars().all()

        return [DepartmentResponse(id=dept.id, name=dept.name) for dept in departments]

    async def get_positions(self, db: AsyncSession):
        """
        Получить список всех должностей.
        """
        stmt = sqlalchemy.select(Position)
        query = await db.execute(stmt)
        positions = query.scalars().all()

        return [PositionResponse(id=pos.id, name=pos.name) for pos in positions]
    async def get_interests(self, db: AsyncSession):
        """
        Получить список всех интересов.
        """
        stmt = sqlalchemy.select(Interest)
        query = await db.execute(stmt)
        positions = query.scalars().all()

        return [InterestResponse(id=pos.id, name=pos.name) for pos in positions]

    async def get_event_types(self, db: AsyncSession):
        """
        Получить список всех типов событий.
        """
        stmt = sqlalchemy.select(EventType)
        query = await db.execute(stmt)
        positions = query.scalars().all()

        return [InterestResponse(id=pos.id, name=pos.name) for pos in positions]
    async def get_priorities(self, db: AsyncSession):
        """
        Получить список всех типов событий.
        """
        stmt = sqlalchemy.select(Priority)
        query = await db.execute(stmt)
        positions = query.scalars().all()
        return [InterestResponse(id=pos.id, name=pos.level) for pos in positions]

    async def get_status_types(self, db: AsyncSession):
        """
        Получить список всех состояний.
        """
        stmt = sqlalchemy.select(StatusEvent)
        query = await db.execute(stmt)
        positions = query.scalars().all()
        return [InterestResponse(id=pos.id, name=pos.name) for pos in positions]

    async def get_event_type_by_id(db: AsyncSession, event_type_id: int):
        """
        Получить тип события по ID.
        """
        stmt = sqlalchemy.select(EventType).where(EventType.id == event_type_id)
        result = await db.execute(stmt)
        return result.scalars().first()

dict_crud = DictTablesCRUD()
