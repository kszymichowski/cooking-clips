from cooking_clips.main import app
from .test_setup import db_session, client

def test_create_user(db_session):
    response = client.post("/users/", json={"username": "test3", "password": "test1", "email": "test3@gmail.com"})
    assert response.status_code == 201