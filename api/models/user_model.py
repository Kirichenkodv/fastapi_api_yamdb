from sqlalchemy import Column, Boolean, String, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum as PyEnum
import uuid

Base = declarative_base()


class UserRole(PyEnum):
    user = "user"
    admin = "admin"
    moderator = "moderator"


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)

    role = Column(Enum(UserRole), default=UserRole.user)

    confirmation_code = Column(String)
