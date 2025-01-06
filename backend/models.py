from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, BigInteger 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)  # Используйте BigInteger
    username = Column(String, unique=True, index=True)
    badges = Column(String, default="")
    points = Column(Integer, default=0)

    predictions = relationship("Prediction", back_populates="user")

class Competition(Base):
    __tablename__ = "competitions"
    id = Column(Integer, primary_key=True, index=True)
    sport_type = Column(String)  # Тип спорта (футбол, бои и т.д.)
    event_name = Column(String)  # Название события (матч, бой)
    is_finished = Column(Boolean, default=False)

    predictions = relationship("Prediction", back_populates="competition")

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    competition_id = Column(Integer, ForeignKey("competitions.id"))
    predicted_result = Column(String)  # Прогноз пользователя
    is_correct = Column(Boolean, default=False)

    user = relationship("User", back_populates="predictions")
    competition = relationship("Competition", back_populates="predictions")