from typing import List, Optional

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.security import get_password_hash
from src.database import User, UserInterest, Interest, Event
from src.schemas.user import UserCreate, UserUpdateInternal
from src.crud.dict_table import dict_crud
class UserCRUDRepository():
    async def create_user(self, user_create: UserCreate, db: AsyncSession) -> User:
        depart = await dict_crud.get_departments(db=db)
        pos = await dict_crud.get_positions(db=db)
        depar_type = {value[1]: key[1] for key, value in dict(depart).items()}
        pos_type = {value[1]: key[1] for key, value in dict(pos).items()}
        user = User(    email=user_create.email,
                        telephone=user_create.telephone,
                        hashed_password=get_password_hash(user_create.password),
                        username=user_create.username,
                        department_id=depar_type[user_create.department],
                        position_id=pos_type[user_create.position],
                        birth_date=user_create.birth_date,
                        skills=user_create.skills)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_user_by_email(self, email: str , db: AsyncSession) -> User:
        stmt = (
            sqlalchemy.select(User)
            .where(User.email == email)
            .options(selectinload(
                User.interests).joinedload(UserInterest.interest),  # Подтягиваем интересы
                selectinload(User.department),  # Подтягиваем департамент
                selectinload(User.position)  # Подтягиваем должность
        )
        )
        query = await db.execute(statement=stmt)
        return query.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int, db: AsyncSession):
        stmt = (
            sqlalchemy.select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.interests).joinedload(UserInterest.interest),  # Подтягиваем интересы
                selectinload(User.department),  # Подтягиваем департамент
                selectinload(User.position)  # Подтягиваем должность
            )
        )
        query = await db.execute(statement=stmt)
        return query.scalar_one_or_none()

    async def get_users(self, db: AsyncSession, skip: int, limit: int,
                        department_id: Optional[int] = None,
                        position_id: Optional[int] = None,
                        username: Optional[str] = None
                        ):
        stmt = sqlalchemy.select(User).offset(skip).limit(limit)\
                .options(
                    selectinload(User.interests).joinedload(UserInterest.interest),  # Подтягиваем интересы
                    selectinload(User.department),  # Подтягиваем департамент
                    selectinload(User.position)  # Подтягиваем должность
        )
        if department_id is not None:
            stmt = stmt.where(User.department_id == department_id)
        if position_id is not None:
            stmt = stmt.where(User.position_id == position_id)
        if username is not None:
            stmt = stmt.where(User.username.ilike(f"%{username}%"))  # Поиск по части имени (некейс-чувствительный)

        query = await db.execute(statement=stmt)
        return query.scalars().all()
    async def update_user(self, user: User, user_update: UserUpdateInternal, db: AsyncSession) -> User:
        user_data = user_update.model_dump(exclude_unset=True)
        depart = await dict_crud.get_departments(db=db)
        pos = await dict_crud.get_positions(db=db)
        depar_type = {value[1]: key[1] for key, value in dict(depart).items()}
        pos_type = {value[1]: key[1] for key, value in dict(pos).items()}

        # Если передан новый пароль – хэшируем его
        if user_update.password:
            user_data['hashed_password'] = get_password_hash(user_data.pop("password"))

        # Обновляем атрибуты пользователя
        for k, v in user_data.items():
            if k == "department":
                setattr(user, "department_id", depar_type[v])
                continue
            if k == "position":
                setattr(user, "position_id", pos_type[v])
                continue
            if k != "interests":
                setattr(user, k, v)


        # Обновляем интересы пользователя, если они переданы
        if user_update.interests is not None:
            # Получаем все интересы из БД по их названиям
            stmt = sqlalchemy.select(Interest).where(Interest.name.in_(user_update.interests))
            result = await db.execute(stmt)
            existing_interests = result.scalars().all()

            # Очищаем старые интересы
            await db.execute(
                sqlalchemy.delete(UserInterest).where(UserInterest.user_id == user.id)
            )

            # Создаем новые связи пользователя с интересами
            user.interests = [UserInterest(user_id=user.id, interest_id=i.id) for i in existing_interests]

        await db.commit()
        await db.refresh(user, ["department", "position", "interests"])  # Загружаем связи перед возвратом
        return user

    async def delete_user(self, user_id: int, db: AsyncSession ):
        result = await db.execute(select(User).filter(User.id == user_id))
        db_event = result.scalars().first()
        if db_event:
            await db.delete(db_event)
            await db.commit()
            return db_event

user_crud = UserCRUDRepository()
