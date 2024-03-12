import pytest
import os
from pathlib import Path
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
    
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    test_db_name = os.getenv('TEST_DB_NAME')
    print(f"postgresql://{username}:{password}@localhost/{test_db_name}")
    SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@localhost/{test_db_name}"

    engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=StaticPool)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()


    app.dependency_overrides[get_db] = override_get_db

    folder_path = Path(__file__).parent.parent / "local_storage/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    
    yield TestingSessionLocal()  # this is where the testing happens

    # teardown
    TestingSessionLocal().close()
    Base.metadata.drop_all(bind=engine)
    clear_mappers()

@pytest.fixture(scope='session')
def auth_token(db_session):
    response = client.post("/users/", 
                           json={"username": "set_up_user",
                                "password": "set_up_user",
                                "email": "set_up_user@gmail.com"
                            }
                        )
    response = client.post("/login/", 
                           data={"username": "set_up_user",
                                "password": "set_up_user"
                            }
                        )
    token = response.json().get('access_token')
    yield token

client = TestClient(app)


