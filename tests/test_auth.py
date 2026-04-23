from datetime import date
from app.schemas.user import UserRegister

def test_user_register_success(test_client):
    user = UserRegister(
        email="test_email2@email.com",
        password="TeSt_P@ssWorD",
        name= "Test User",
        date_of_birth=date(1991, 5, 12)
    )

    response = test_client.post("/auth/register", json=user.model_dump(mode="json"))
    assert response.status_code == 201
    assert response.json()["message"] == "User created"

def test_user_register_duplicated_email(test_client, registered_user):
    db_user = registered_user["user"]
    print(db_user.model_dump_json())
    user = UserRegister(
        email=db_user.email,
        password="TeSt_P@ssWorD",
        name= "Test User",
        date_of_birth=date(1991, 5, 12)
    )

    response = test_client.post("/auth/register", json=user.model_dump(mode="json"))
    assert response.status_code == 409
    assert response.json()["detail"] == "An user with this email already exists"
