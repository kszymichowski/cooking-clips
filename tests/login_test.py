from cooking_clips.main import app
from .test_setup import db_session, client

 
def test_login_user(db_session):
    # GIVEN a user is created
    response = client.post("/users/", 
                           json={"username": "login_test",
                                "password": "login_test",
                                "email": "login_test@gmail.com"
                            }
                        )
    assert response.status_code == 201
    # WHEN the user tries to login
    response = client.post("/login/", 
                           data={"username": "login_test",
                                "password": "login_test"
                            }
                        )
    # THEN the user is logged in
    assert response.status_code == 200
    # AND the user is given a token
    assert "access_token" in response.json()

