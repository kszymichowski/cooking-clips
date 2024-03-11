import os
from cooking_clips.main import app
from .test_setup import db_session, client, auth_token
from pathlib import Path

#@pytest.mark.skip(reason="test not implemented")
def test_create_recipe(db_session, auth_token):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }

    create_book_data = {"title": "book test title"}

    response = client.post("/books/", json=create_book_data, headers=headers)
    assert response.status_code == 201

    form_data = {
        "name": "Recipe Name",
        "ingredients": "Ingredient details",
        "instructions": "Instructions details",
        "book_id": response.json().get('id')
    }

    data = {}
    for key, value in form_data.items():
        data[key] = (None, str(value))

    file_path = Path(__file__).parent / "test_data" / "test_video.mp4"
    file_name = file_path.name
    file_content = open(file_path, "rb")
    file_data = {"file": (file_name, file_content, "multipart/form-data")}
    data.update(file_data)


    response = client.post("/recipes/", headers=headers, files=data)
    assert response.status_code == 201

    video_path = Path(__file__).parent.parent / "local_storage" / "test_video.mp4"
    assert os.path.exists(video_path)

    os.remove(video_path)
