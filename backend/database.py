from datetime import datetime
import enum
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Float, Date, DateTime, event, Enum
from sqlalchemy.engine import Engine


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

engine = create_async_engine("sqlite+aiosqlite:///./data/data.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


class RoleEnum(enum.Enum):
    user = "Пользователь"
    legal_entity = "Юр.лицо"
    ip = "ИП"
    admin = "Админ"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    number = Column(String, nullable=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    role = Column(Enum(RoleEnum, values_callable=lambda x: [e.value for e in x]), nullable=False)
    organization_name = Column(String, nullable=True)
    INN = Column(Integer, nullable=True)

    orders = relationship("Order", cascade="all, delete", passive_deletes=True)
    wishlist = relationship("Wishlist", cascade="all, delete", passive_deletes=True)


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True)

    products = relationship("Product", back_populates="article", cascade="all, delete", passive_deletes=True)


class Color(Base):
    __tablename__ = "color"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class MeasurementEnum(enum.Enum):
    meter = "м"
    package = "упак"
    piece = "шт"


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("category.id",  ondelete="CASCADE"), nullable=False)
    article_id = Column(Integer, ForeignKey("article.id",  ondelete="CASCADE"), nullable=False)
    color_id = Column(Integer, ForeignKey("color.id", ondelete="SET NULL"), nullable=True)
    name = Column(String, nullable=False)
    image_path = Column(String, nullable=True)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    measured_in = Column(Enum(MeasurementEnum, values_callable=lambda x: [e.value for e in x]), nullable=False)
    price = Column(Integer, nullable=False)
    new = Column(Boolean, nullable=False, default=True)
    new_until = Column(DateTime, nullable=True)
    hit = Column(Boolean, nullable=False, default=False)
    promotion = Column(Boolean, nullable=False, default=False)
    percent_promotion = Column(Float, nullable=True)
    new_price = Column(Float, nullable=True)
    purchase_count = Column(Integer, default=0)
    last_hit_date = Column(DateTime, nullable=True)

    category = relationship("Category", back_populates="products")
    article = relationship("Article", back_populates="products")
    characteristics = relationship("Characteristic", cascade="all, delete", passive_deletes=True)
    color = relationship("Color")


class Property(Base):
    __tablename__ = "property"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Characteristic(Base):
    __tablename__ = "characteristic"
    product_id = Column(Integer, ForeignKey("product.id",  ondelete="CASCADE"), primary_key=True, nullable=False)
    property_id = Column(Integer, ForeignKey("property.id",  ondelete="CASCADE"), primary_key=True, nullable=False)
    property_value = Column(String, nullable=False)

    property = relationship("Property")


class Wishlist(Base):
    __tablename__ = "wishlist"
    user_id = Column(Integer, ForeignKey("user.id",  ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id",  ondelete="CASCADE"), primary_key=True)

    product = relationship("Product")


class Cart(Base):
    __tablename__ = "cart"
    user_id = Column(Integer, ForeignKey("user.id",  ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id",  ondelete="CASCADE"), primary_key=True)
    amount = Column(Float, nullable=False)

    product = relationship("Product")


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id",  ondelete="CASCADE"))
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    payment_status = Column(String, nullable=False, default="pending")  # "pending", "paid", "failed"
    items = Column(String, nullable=True)  # JSON строка списка товаров
    delivery_service_id = Column(Integer, ForeignKey("delivery_service.id", ondelete="CASCADE"), nullable=True)
    delivery_service = relationship("DeliveryService", back_populates="orders")


class DeliveryService(Base):
    __tablename__ = "delivery_service"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    orders = relationship("Order", back_populates="delivery_service")


# КатегорииТоваров
class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("category.id",  ondelete="CASCADE"), nullable=True)

    parent = relationship("Category", remote_side=[id], backref="children", cascade="all, delete", passive_deletes=True)
    products = relationship("Product", back_populates="category", cascade="all, delete", passive_deletes=True)


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    comment = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_processed = Column(Boolean, default=False)


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    requirements = Column(String)
    responsibilities = Column(String)
    salary = Column(String, nullable=True)


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    name = Column(String, nullable=False)
    vacancy = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    comment = Column(String, nullable=True)
    file_name = Column(String, default="default_resume.pdf")


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    office_phone = Column(String, nullable=True)
    office_email = Column(String, nullable=True)
    office_workhours = Column(String, nullable=True)
    sales_phone = Column(String, nullable=True)
    sales_email = Column(String, nullable=True)
    purchase_phone = Column(String, nullable=True)
    purchase_email = Column(String, nullable=True)
    purchase_extension = Column(String, nullable=True)
    purchase_addition = Column(String, nullable=True)
    commercial_email = Column(String, nullable=True)
    general_email = Column(String, nullable=True)
    legal_address = Column(String, nullable=True)
    ogrn = Column(String, nullable=True)
    inn = Column(String, nullable=True)
    kpp = Column(String, nullable=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
