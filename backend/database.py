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


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    сharacteristics = Column(String, nullable=False)
    article = Column(String, nullable=False)
    subcategory_id = Column(Integer, ForeignKey("subcategory.id"))
    subcategory = relationship("Subcategory", back_populates="products")


# КатегорииТоваров
class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    subcategories = relationship("Subcategory", back_populates="category")


# Подкатегории товаров
class Subcategory(Base):
    __tablename__ = "subcategory"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="subcategories")
    products = relationship("Product", back_populates="subcategory")



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)