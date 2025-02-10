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
    role = Column(String, nullable=False)  # "Пользователь", "Админ", "Юр.лицо", "ИП"
    organization_name = Column(String, nullable=True)
    INN = Column(Integer, nullable=True)


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True)
    subcategory_id = Column(Integer, ForeignKey("subcategory.id"))
    description = Column(String, nullable=True)
    characteristics = Column(String, nullable=True)
    price = Column(Integer, nullable=True)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("article.id"))
    name = Column(String, nullable=False)
    image_path = Column(String, nullable=True)
    amount = Column(Integer, nullable=False)
    article = relationship("Article")


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


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)