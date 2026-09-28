
from datetime import datetime,timezone
from sqlalchemy import (
    Column,Integer,String, DateTime
    )
from app.db.database import Base

class User(Base):
    __tablename__="users"
    
    id=Column(Integer,primary_key=True)
    name=Column(
        String,
        nullable=False
        )
    email=Column(
        String,
        nullable=False,
        unique=True
        )
    password=Column(
        String,
        nullable=False
        )
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )