import uuid
from sqlalchemy import UUID, Column, Integer, String
from app.db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String)
    description = Column(String)
    filename = Column(String)
    demo_link = Column(String)
    video_link = Column(String)
    journal_link = Column(String)
    author = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)


class Hero(Base):
    __tablename__ = "heros"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    main_text = Column(String)
    alt_text = Column(String, nullable=True)


class AboutUs(Base):
    __tablename__ = "about_us"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    filename = Column(String)
    text = Column(String)
    description = Column(String)


class ContactUs(Base):
    __tablename__ = "contact_us"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String)
    filename = Column(String)
    link = Column(String)
