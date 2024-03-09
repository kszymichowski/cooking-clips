from cooking_clips.main import app
from .test_setup import db_session, client

 
def test_login_user(db_session):
    # GIVEN a user is created
    response = client.post("/users/", 
                           json={"username": "loginTest",
                                "password": "loginTest",
                                "email": "loginTest@gmail.com"
                            }
                        )
    assert response.status_code == 201
    # WHEN the user tries to login
    response = client.post("/login/", 
                           data={"username": "loginTest",
                                "password": "loginTest"
                            }
                        )
    # THEN the user is logged in
    assert response.status_code == 200
    # AND the user is given a token
    assert "access_token" in response.json()

