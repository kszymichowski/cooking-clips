import pytest
from jose import jwt
from . import auth

@pytest.mark.parametrize("data", [{"sub": "test", "id": 1}])
def test_jwt_token(data: dict):
	token = auth.generate_token(data)
	jwt_payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
	assert jwt_payload.get("sub") == data["sub"]
	assert jwt_payload.get("id") == data["id"]

def test_jwt_token_no_data():
	with pytest.raises(TypeError):
		token = auth.generate_token()

def test_secret_key():
	auth.set_secret_key()
	assert auth.SECRET_KEY != ""