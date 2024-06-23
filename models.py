from sqlalchemy import Column, Integer, String
from database import Base


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    preparation_time = Column(Integer)
    ingredients = Column(String)
    description = Column(String)
    views = Column(Integer, default=0)