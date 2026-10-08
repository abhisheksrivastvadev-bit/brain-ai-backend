from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime

from app.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id : Mapped[int]= mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    conversation_id : Mapped[int]= mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    role : Mapped[str]= mapped_column(
        nullable=False
    )

    content : Mapped[str]= mapped_column(
        nullable=False
    )

    image_url : Mapped[str]= mapped_column(
        nullable=True
    )

    created_at : Mapped[datetime]= mapped_column(
        server_default=func.now(),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    image_url = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )