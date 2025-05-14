from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    population = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    subregion = Column(String)