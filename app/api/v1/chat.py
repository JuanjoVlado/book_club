import anthropic
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from app.core.security import get_current_user
from app.db.session import SessionDep
from app.models.book import Book
from app.models.chat import Chat, ChatMessage, ChatRole
from app.models.user import User
from app.schemas.book import BookResponse
from app.schemas.chat import ChatMessageCreate
from app.core.config import settings
from app.tasks import create_embedding, get_model

chat_router = APIRouter()

_anthropic_client = None

def get_client():
    global _anthropic_client
    if _anthropic_client is None:
        _anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _anthropic_client

@chat_router.post(
        "/chats",
        tags=["recommendations"],
        status_code=status.HTTP_201_CREATED,
        response_model=Chat
    )
def create_chat(session: SessionDep, user: User = Depends(get_current_user)):
    chat = Chat(user_id=user.id)
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return chat

@chat_router.post(
        "/chats/{chat_id}",
        tags=["recommendations"],
        status_code=status.HTTP_201_CREATED,
        response_model=List[BookResponse]
    )
def create_message(
    session: SessionDep,
    chat_id: int,
    message: ChatMessageCreate,
    user: User = Depends(get_current_user)
):
    db_chat = session.get(Chat, chat_id)
    if not db_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found"
        )
    
    if db_chat.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
    
    chat_message = ChatMessage(
        role=ChatRole.USER,
        content=message.content,
        chat_id=chat_id
    )

    session.add(chat_message)
    session.commit()
    session.refresh(chat_message)

    statement = select(ChatMessage).where(ChatMessage.chat_id == chat_id)
    db_chat_messages = session.exec(statement).all()

    client = get_client()
    api_message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system="Eres un bibliotecario experto. Basándote en los requerimientos del usuario, genera una descripción concisa del tipo de libro que busca, optimizada para búsqueda semántica. Devuelve ÚNICAMENTE la descripción, sin texto adicional.",
        messages=[{"role": chat_message.role, "content": chat_message.content} for chat_message in db_chat_messages]
    )

    re_prompt = api_message.content[0].text
    print("ANTHROPIC PROMPT: ", re_prompt)

    assistant_msg = ChatMessage(
        chat_id=chat_id,
        role=ChatRole.ASSISTANT,
        content=re_prompt
    )
    session.add(assistant_msg)
    session.commit()
    session.refresh(assistant_msg)

    embedding = create_embedding(re_prompt)
    statement = select(Book).order_by(Book.embedding.cosine_distance(embedding)).limit(5)
    db_books = session.exec(statement).all()
    
    return [BookResponse.model_validate(db_book) for db_book in db_books]
    
