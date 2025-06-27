from sqlalchemy import String, Boolean, Date, ForeignKey, Text, TIMESTAMP, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import relationship, sessionmaker, DeclarativeBase, mapped_column
from datetime import datetime
from src.core.config import settings
import asyncpg

# Создание асинхронного движка
engine = create_async_engine(str(settings.DATABASE_URL), echo=False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Department(Base):
    __tablename__ = "department"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)  # ID будет инкрементироваться автоматически
    name = mapped_column(String(255), unique=True, nullable=False)

    # Пример каскадных удалений
    users = relationship("User", back_populates="department", cascade="all, delete-orphan")

class Position(Base):
    __tablename__ = "position"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), unique=True, nullable=False)

    # Пример каскадных удалений
    users = relationship("User", back_populates="position", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    telephone = mapped_column(String(255), unique=True)
    username = mapped_column(String(255), nullable=True, default="Unknown")  # Значение по умолчанию
    email = mapped_column(String(255), unique=True, nullable=True)
    hashed_password = mapped_column(Text, nullable=True)
    birth_date = mapped_column(Date, nullable=True)
    is_superuser = mapped_column(Boolean, default=False)  # Значение по умолчанию
    skills = mapped_column(Text, nullable=True, default="")  # Пустая строка по умолчанию
    department_id = mapped_column(Integer, ForeignKey("department.id", ondelete="SET NULL"), nullable=True)
    position_id = mapped_column(Integer, ForeignKey("position.id", ondelete="SET NULL"), nullable=True)
    profile_image_url = mapped_column(String, default="changethattoimage")  # Значение по умолчанию

    # Связь с department и position
    department = relationship("Department", back_populates="users")
    position = relationship("Position", back_populates="users")

    # Связь с интересами (UserInterest)
    interests = relationship("UserInterest", back_populates="user", cascade="all, delete-orphan")
    event_participants = relationship("EventParticipantWithPriority", back_populates="user", cascade="all, delete-orphan")

class Interest(Base):
    __tablename__ = "interest"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), unique=True, nullable=False)

class UserInterest(Base):
    __tablename__ = "user_interest"

    user_id = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    interest_id = mapped_column(Integer, ForeignKey("interest.id", ondelete="CASCADE"), primary_key=True)

    # Связи с пользователем и интересом
    user = relationship("User", back_populates="interests")
    interest = relationship("Interest")

class EventType(Base):
    __tablename__ = "event_type"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), unique=True, nullable=False)

class Priority(Base):
    __tablename__ = "priority"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    level = mapped_column(String(50), unique=True, nullable=False)  # Например: "Низкий", "Средний", "Высокий"

class Event(Base):
    __tablename__ = "event"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), nullable=False)
    description = mapped_column(Text, nullable=True)
    event_type_id = mapped_column(Integer, ForeignKey("event_type.id", ondelete="SET NULL"))
    start_time = mapped_column(TIMESTAMP, nullable=False)
    end_time = mapped_column(TIMESTAMP, nullable=True)
    status_id = mapped_column(Integer, ForeignKey("status_event.id"), default=1)
    organizator = mapped_column(String(255), nullable=False)
    place = mapped_column(String(255), nullable=False)

    # Связь с участниками
    participants = relationship("EventParticipantWithPriority", back_populates="event", cascade="all, delete-orphan")
    interests = relationship("EventInterest", back_populates="event", cascade="all, delete-orphan")

class StatusEvent(Base):
    __tablename__ = "status_event"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), unique=True, nullable=False)
class EventInterest(Base):
    __tablename__ = "event_interest"

    event_id = mapped_column(Integer, ForeignKey("event.id", ondelete="CASCADE"), primary_key=True)
    interest_id = mapped_column(Integer, ForeignKey("interest.id", ondelete="CASCADE"), primary_key=True)

    event = relationship("Event", back_populates="interests")
    interest = relationship("Interest")
class EventParticipantWithPriority(Base):
    __tablename__ = "event_participant_with_priority"

    event_id = mapped_column(Integer, ForeignKey("event.id", ondelete="CASCADE"), primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    priority_id = mapped_column(Integer, ForeignKey("priority.id", ondelete="SET NULL"), nullable=True)
    is_present = mapped_column(Boolean, default=False)  # Будет ли участник на мероприятии

    user = relationship("User", back_populates="event_participants")
    event = relationship("Event", back_populates="participants")

async def init_database():
    try:
        conn = await asyncpg.connect(str(settings.DATABASE_URL))
        await conn.execute("CREATE DATABASE gazprom;")
        await conn.close()
        print("База данных 'gazprom' успешно создана!")
    except Exception:
        print("База данных gazprom уже существует!")

async def init_models():
    async with engine.begin() as conn:
        print("Удаление всех таблиц...")
        # Используем raw SQL для удаления и создания схемы
        from sqlalchemy import text
        await conn.execute(text("DROP SCHEMA public CASCADE;"))
        await conn.execute(text("CREATE SCHEMA public;"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO postgres;"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))

        print("Создание всех таблиц...")
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы успешно созданы!")
