from datetime import date
from app.schemas.user import UserRegister, UserLogin

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
    
    user = UserRegister(
        email=db_user.email,
        password="TeSt_P@ssWorD",
        name= "Test User",
        date_of_birth=date(1991, 5, 12)
    )

    response = test_client.post("/auth/register", json=user.model_dump(mode="json"))
    assert response.status_code == 409
    assert response.json()["detail"] == "An user with this email already exists"

def test_user_login_success(test_client, registered_user):
    db_user = registered_user["user"]
    login_user = UserLogin(
        email=db_user.email,
        password=db_user.password
    )
    response = test_client.post(
        "/auth/login",
        data={"username": login_user.email, "password": login_user.password}
    )

    assert response.status_code == 200


def test_user_login_invalid_email(test_client):
    login_user = UserLogin(
        email="NotExists@email.com",
        password="anyPassword"
    )
    response = test_client.post(
        "/auth/login",
        data={"username": login_user.email, "password": login_user.password}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "incorrect credentials"

def test_user_login_invalid_password(test_client, registered_user):
    db_user = registered_user["user"]
    login_user = UserLogin(
        email=db_user.email,
        password=db_user.password+"x"
    )
    response = test_client.post(
        "/auth/login",
        data={"username": login_user.email, "password": login_user.password}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "incorrect credentials"

def test_user_logout_success(test_client, registered_user):
    access_token = registered_user["access_token"]
    response = test_client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "logout"}

def test_user_logout_unsuccess(test_client):
    response = test_client.post("/auth/logout")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
