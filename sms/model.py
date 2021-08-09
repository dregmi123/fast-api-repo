from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class sahayatri(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    firstname = Column(VARCHAR(255))
    lastname = Column(VARCHAR(255))
    email= Column(VARCHAR(255))
    password = Column(VARCHAR(255))
