from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .time import Timestamp

class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String)

    tasks = relationship("Task", back_populates="owner")