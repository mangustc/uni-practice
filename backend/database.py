from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Float, Date, DateTime, event
from sqlalchemy.engine import Engine


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

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

    orders = relationship("Order", back_populates="user", cascade="all, delete", passive_deletes=True)
    wishlist = relationship("Wishlist", back_populates="user", cascade="all, delete", passive_deletes=True)


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("category.id",  ondelete="CASCADE"))
    description = Column(String, nullable=True)
    country = Column(String, nullable=True)
    characteristic_width = Column(String, nullable=True)
    characteristic_density = Column(String, nullable=True)
    characteristic_consist = Column(String, nullable=True)
    measured_in = Column(String, nullable=False)  # "м", "упак", "шт"
    price = Column(Integer, nullable=False)

    category = relationship("Category", back_populates="articles")
    products = relationship("Product", back_populates="article", cascade="all, delete", passive_deletes=True)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("article.id",  ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    image_path = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    characteristic_color = Column(String, nullable=True)
    new = Column(Boolean, nullable=False, default=True)
    new_until = Column(DateTime, nullable=True)
    hit = Column(Boolean, nullable=False, default=False)
    promotion = Column(Boolean, nullable=False, default=False)
    percent_promotion = Column(Float, nullable=True)
    new_price = Column(Float, nullable=True)
    purchase_count = Column(Integer, default=0)
    last_hit_date = Column(DateTime, nullable=True)

    article = relationship("Article", back_populates="products")
    wishlists = relationship("Wishlist", back_populates="product", cascade="all, delete", passive_deletes=True)
    carts = relationship("Cart", back_populates="product", cascade="all, delete", passive_deletes=True)


class Wishlist(Base):
    __tablename__ = "wishlist"
    user_id = Column(Integer, ForeignKey("user.id",  ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id",  ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="wishlist")
    product = relationship("Product", back_populates="wishlists")


class Cart(Base):
    __tablename__ = "cart"
    user_id = Column(Integer, ForeignKey("user.id",  ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id",  ondelete="CASCADE"), primary_key=True)
    amount = Column(Float, nullable=False)

    product = relationship("Product", back_populates="carts")


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id",  ondelete="CASCADE"))
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    payment_status = Column(String, nullable=False, default="pending")  # "pending", "paid", "failed"
    items = Column(String, nullable=True)  # JSON строка списка товаров

    user = relationship("User", back_populates="orders")


# КатегорииТоваров
class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("category.id",  ondelete="CASCADE"), nullable=True)

    parent = relationship("Category", remote_side=[id], backref="children", cascade="all, delete", passive_deletes=True)
    articles = relationship("Article", back_populates="category", cascade="all, delete", passive_deletes=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
