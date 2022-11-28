from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from engine_session_middle import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    # email = Column(String(100), nullable=False, unique=True)
    # advertisement = relationship("AdvModel", backref="user")


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(UUID, server_default=func.uuid_generate_v4(), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")
    created = Column(DateTime, server_default=func.now())


class AdvModel(Base):
    __tablename__ = 'adv'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, unique=True)
    description = Column(String(2000), nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
