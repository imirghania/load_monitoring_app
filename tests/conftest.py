import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from monitor_app.database import Base
from monitor_app.main import SystemMonitorApp, tk
from monitor_app.settings import settings

load_dotenv()


# Setup test database
@pytest.fixture(scope="module")
def test_db():
    engine = create_engine(settings.test_db_uri)
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    return TestSession()


# Setup monitor_app test instance
@pytest.fixture
def app_instance(test_db):
    root = tk.Tk()
    app = SystemMonitorApp(root, test_db)
    return app