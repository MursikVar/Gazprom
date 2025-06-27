from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from src.database import Department, StatusEvent, Position, User, Interest, EventType, Priority, Event, EventParticipantWithPriority, UserInterest, SessionLocal, EventInterest
from src.core.security import get_password_hash

# Асинхронная функция для добавления данных в базу данных
async def create_initial_data():
    async with SessionLocal() as session:
        # Добавляем записи в таблицу Department
        department1 = Department(name="Отдел продаж")
        department2 = Department(name="Отдел маркетинга")
        session.add(department1)
        session.add(department2)

        # Добавляем записи в таблицу Position
        position1 = Position(name="Менеджер по продажам")
        position2 = Position(name="Маркетолог")
        session.add(position1)
        session.add(position2)

        await session.commit()

        # Добавляем записи в таблицу User
        user1 = User(
            username="oleg123",
            email="user@example.com",
            hashed_password=get_password_hash("123"),
            telephone="+7634634326",
            birth_date=datetime(1990, 5, 24),
            is_superuser=True,
            skills="Python, SQL",
            department_id=department1.id,  # Привязка к отделу
            position_id=position1.id  # Привязка к позиции
        )
        user2 = User(
            username="irina123",
            email="irina@example.com",
            telephone="+613613513",
            hashed_password="hashed_password_2",
            birth_date=datetime(1992, 3, 16),
            is_superuser=False,
            skills="SEO, Marketing",
            department_id=department2.id,
            position_id=position2.id
        )
        session.add(user1)
        session.add(user2)

        # Фиксируем изменения, чтобы получить id пользователей
        await session.commit()

        status1=StatusEvent(name="Активно   ")
        status2=StatusEvent(name="Завершено")
        session.add(status1)
        session.add(status2)

        await session.commit()

        # Добавляем записи в таблицу Interest
        interest1 = Interest(name="Программирование")
        interest2 = Interest(name="Маркетинг")
        session.add(interest1)
        session.add(interest2)

        # Фиксируем изменения, чтобы получить id интересов
        await session.commit()

        # Добавляем записи в таблицу UserInterest
        user_interest1 = UserInterest(user_id=user1.id, interest_id=interest1.id)
        user_interest2 = UserInterest(user_id=user2.id, interest_id=interest2.id)
        session.add(user_interest1)
        session.add(user_interest2)

        # Фиксируем изменения, чтобы получить id интересов для пользователей
        await session.commit()

        # Добавляем записи в таблицу EventType
        event_type1 = EventType(name="Конференция")
        event_type2 = EventType(name="Вебинар")
        session.add(event_type1)
        session.add(event_type2)

        # Фиксируем изменения, чтобы получить id типов событий
        await session.commit()

        # Добавляем записи в таблицу Priority
        priority1 = Priority(level="Высокий")
        priority2 = Priority(level="Средний")
        session.add(priority1)
        session.add(priority2)

        # Фиксируем изменения, чтобы получить id приоритетов
        await session.commit()

        # Добавляем записи в таблицу Event
        event1 = Event(
            name="Конференция по Python",
            description="Конференция для разработчиков, посвященная Python",
            event_type_id=event_type1.id,
            start_time=datetime(2025, 5, 10, 10, 0),
            end_time=datetime(2025, 5, 10, 18, 0),
            status_id=status1.id,
            place="Москва, ул. Тверская, д. 123",
            organizator="Томск"
        )
        event2 = Event(
            name="Вебинар по SEO",
            description="Вебинар о поисковой оптимизации",
            event_type_id=event_type2.id,
            start_time=datetime(2025, 6, 5, 12, 0),
            end_time=datetime(2025, 6, 5, 14, 0),
            status_id = status2.id,
            place="Москва, ул. Тверская, д. 123",
            organizator="Томск"
        )
        session.add(event1)
        session.add(event2)

        # Фиксируем изменения, чтобы получить id событий
        await session.commit()

        event_interest1 = EventInterest(event_id=event1.id, interest_id=interest1.id)
        event_interest2 = EventInterest(event_id=event2.id, interest_id=interest2.id)
        session.add(event_interest1)
        session.add(event_interest2)

        # Commit changes to the database
        await session.commit()

        # Добавляем записи в таблицу EventParticipantWithPriority
        event_participant1 = EventParticipantWithPriority(
            event_id=event1.id,  # Привязываем к событию
            user_id=user1.id,    # Привязываем к пользователю
            priority_id=priority1.id,
            is_present=True
        )
        event_participant2 = EventParticipantWithPriority(
            event_id=event2.id,  # Привязываем к событию
            user_id=user2.id,    # Привязываем к пользователю
            priority_id=priority2.id,
            is_present=False
        )
        session.add(event_participant1)
        session.add(event_participant2)

        # Фиксируем изменения в базе данных
        await session.commit()
