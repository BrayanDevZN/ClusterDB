"models de users"
from src.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, UUID
from typing import Literal
from datetime import datetime
import uuid

class Users(Base): 

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    public_id: Mapped[uuid.UUID] = mapped_column(UUID, default=uuid.uuid4, index=True)
    user_name: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Literal["admin","dev", "user"]] = mapped_column(String, default="user")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
