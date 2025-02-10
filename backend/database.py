from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Numeric, Date, LargeBinary, DateTime, text

engine = create_async_engine("sqlite+aiosqlite:///./data.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()



class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    number = Column(String, nullable=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    role = Column(String, nullable=False)



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)