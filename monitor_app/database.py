from datetime import datetime
import pytz
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from monitor_app.settings import settings


class Base(DeclarativeBase):     
    pass


class SystemRecord(Base):
    __tablename__ = 'system_records'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now(pytz.utc))
    cpu_load = Column(Float)
    ram_load = Column(Float)
    storage_load = Column(Float)


engine = create_engine(settings.db_uri)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

