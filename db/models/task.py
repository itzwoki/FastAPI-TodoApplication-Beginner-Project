from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .time import Timestamp

class Task(Timestamp, Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), index=True)
    description = Column(Text, nullable=True)
    done = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")