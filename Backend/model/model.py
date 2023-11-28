from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from pydantic import BaseModel

Base = declarative_base()

class ImageData(BaseModel):
    image: str


class Log(Base):
    __tablename__ = "log"
    seq = Column(Integer, primary_key=True, autoincrement=True)
    administrator = Column(String)
    phone = Column(String)
    logtime = Column(DateTime, default=datetime.now)
    logpath = Column(String)
    smsflag = Column(Boolean)
