from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?async_fallback=True"
Base: DeclarativeMeta = declarative_base()


# class Link(Base):
#     __tablename__ = 'link'

#     id = Column('id', Integer, primary_key=True)
#     url = Column('url', String, nullable=False)
#     created = Column('created', TIMESTAMP, default=datetime.utcnow)


# class Counter(Base):
#     __tablename__ = 'counter'

#     id = Column('id', Integer, primary_key=True)
#     count = Column('count', Integer)
#     created = Column('created', TIMESTAMP, default=datetime.utcnow)


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
