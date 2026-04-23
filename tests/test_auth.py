from datetime import date
from app.schemas.user import UserRegister

def test_user_register(test_client):
    user = UserRegister(
        email="test_email2@email.com",
        password="TeSt_P@ssWorD",
        name= "Test User",
        date_of_birth=date(1991, 5, 12)
    )
    response = test_client.post("/auth/register", json=user.model_dump(mode="json"))
    print("### ", response.json())
    print("### ", user.model_dump_json())
    assert response.status_code == 201
    assert response.json()["message"] == "User created"
