from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Conversation, Message


def get_or_create_conversation(
    db: Session,
    user_id: str,
    session_id: str
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id,
            Conversation.session_id == session_id
        )
        .first()
    )

    if conversation:
        return conversation

    conversation = Conversation(
        user_id=user_id,
        session_id=session_id
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def getConversationHistory(
    db: Session,
    user_id: str,
    session_id: str
):
    conversation = get_or_create_conversation(
        db,
        user_id,
        session_id
    )

    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation.id
        )
        .order_by(
            Message.created_at.asc(),
            Message.id.asc()
        )
        .all()
    )

    history = []

    for message in messages:

        item = {
            "role": message.role,
            "content": message.content
        }

        if message.image_url:
            item["image_url"] = message.image_url

        history.append(item)

    return history


def saveConversationHistory(
    db: Session,
    user_id: str,
    session_id: str,
    role: str,
    content: str,
    image_url: str = None
):
    conversation = get_or_create_conversation(
        db,
        user_id,
        session_id
    )

    message = Message(
        conversation_id=conversation.id,
        role=role,
        content=content,
        image_url=image_url
    )

    db.add(message)

    conversation.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(message)

    return message


def getAllConversationHistory(
    db: Session,
    user_id: str
):
    conversations = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id
        )
        .order_by(
            Conversation.updated_at.desc()
        )
        .all()
    )

    result = []

    for conversation in conversations:

        last_message = (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation.id
            )
            .order_by(
                Message.created_at.asc(),
                Message.id.desc()
            )
            .first()
        )

        result.append({
            "id": conversation.id,
            "user_id": conversation.user_id,
            "session_id": conversation.session_id,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
            "last_message": (
                {
                    "role": last_message.role,
                    "content": last_message.content,
                    "image_url": last_message.image_url
                }
                if last_message
                else None
            )
        })

    return result