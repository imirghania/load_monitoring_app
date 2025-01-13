import os
from datetime import datetime
import pytz
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
load_dotenv()


__all__ = ("SystemRecord", "session")


class Base(DeclarativeBase):     
    pass


class SystemRecord(Base):
    __tablename__ = 'system_records'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now(pytz.utc))
    cpu_load = Column(Float)
    ram_load = Column(Float)
    storage_load = Column(Float)


engine = create_engine(os.getenv("DB_URI", "sqlite:///system_data.db"))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

