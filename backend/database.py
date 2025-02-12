from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Float, Date, DateTime

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
    country = Column(String, nullable=True)
    characteristic_color = Column(String, nullable=True)
    characteristic_width = Column(String, nullable=True)
    characteristic_density = Column(String, nullable=True)
    characteristic_consist = Column(String, nullable=True)
    measured_in = Column(String, nullable=False)  # "м", "упак", "шт"
    price = Column(Integer, nullable=False)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("article.id"))
    name = Column(String, nullable=False)
    image_path = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    hit = Column(Boolean, nullable=False, default=False)
    promotion = Column(Boolean, nullable=False, default=False)
    procent_promotion = Column(Float, nullable=True)
    new = Column(Boolean, nullable=False, default=True)
    new_until = Column(DateTime, nullable=True)
    old_price = Column(Float, nullable=True)
    new_price = Column(Float, nullable=True)
    purchase_count = Column(Integer, default=0)
    last_hit_date = Column(DateTime, nullable=True)
    article = relationship("Article")


class Wishlist(Base):
    __tablename__ = "wishlist"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True)


class Cart(Base):
    __tablename__ = "cart"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True)
    amount = Column(Float, nullable=False)


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    payment_status = Column(String, nullable=False, default="pending")  # "pending", "paid", "failed"
    items = Column(String, nullable=True)  # JSON строка списка товаров


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