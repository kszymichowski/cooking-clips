import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, clear_mappers
from cooking_clips import models  # replace with your actual models module
from cooking_clips.main import app
from sqlalchemy.orm import sessionmaker, declarative_base
from cooking_clips.database import get_db, Base
from fastapi.testclient import TestClient

@pytest.fixture(scope='session')
def db_session():
    # setup
    SQLALCHEMY_DATABASE_URL = "sqlite://"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


    Base.metadata.create_all(bind=engine)


    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()


    app.dependency_overrides[get_db] = override_get_db

    
    yield TestingSessionLocal()  # this is where the testing happens

    # teardown
    TestingSessionLocal().close()
    clear_mappers()

client = TestClient(app)

