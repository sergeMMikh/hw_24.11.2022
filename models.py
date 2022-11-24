from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    advertisement = relationship("AdvModel", backref="user")


class AdvModel(Base):
    __tablename__ = 'adv'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, unique=True)
    description = Column(String(2000), nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
