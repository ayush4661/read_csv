from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from db import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)


class User(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=100)
    age: int