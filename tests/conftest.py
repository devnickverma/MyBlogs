import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base
from app.dependencies import get_db
# Import models to ensure they are registered with Base.metadata
from app.models import models

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """
    Create tables for each test.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(setup_database):
    """
    Yield a database session for each test function.
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db):
    """
    Override the get_db dependency to use the test database session.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass # Session closed in db fixture

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}
