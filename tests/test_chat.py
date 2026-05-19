
from unittest.mock import MagicMock, patch

from app.schemas.chat import ChatMessageCreate


def test_create_chat_success(test_client, registered_user):
    user =  registered_user["user"]

    response = test_client.post(
        "/chats",
        headers={"Authorization": f"Bearer {registered_user["access_token"]}"}
    )

    assert response.status_code == 201

def test_create_message_success(test_client, books_created, chat_created):
    chat = chat_created["chat"]
    msg = ChatMessageCreate(content="Recommend a history book")

    with patch("app.api.v1.chat.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_content = MagicMock()
        mock_content.text = "A history book about ancient civilizations"

        mock_response = MagicMock()
        mock_response.content = [mock_content]
        mock_client.messages.create.return_value = mock_response
                
        response = test_client.post(
            f"/chats/{chat["id"]}",
            json=msg.model_dump(mode="json", exclude_unset=True),
            headers={"Authorization": f"Bearer {chat_created["access_token"]}"}
        )

        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_create_message_chat_not_found(test_client, chat_created):
    chat = chat_created["chat"]
    msg = ChatMessageCreate(content="Recommend a history book")

    response = test_client.post(
        f"/chats/{chat["id"]+1}",
        json=msg.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {chat_created["access_token"]}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Chat with id {chat["id"]+1} not found"

def test_create_message_forbidden(test_client, chat_created, register_regular_user):
    chat = chat_created["chat"]
    msg = ChatMessageCreate(content="Recommend a history book")

    response = test_client.post(
        f"/chats/{chat["id"]}",
        json=msg.model_dump(mode="json", exclude_unset=True),
        headers={"Authorization": f"Bearer {register_regular_user["access_token"]}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to perform this action"
