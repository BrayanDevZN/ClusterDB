"model de keys"
from .users import Users
from src.database.base import Base 
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, UUID
from datetime import datetime
from typing import Literal
import uuid 

class keys(Base):

    __tablename__ = "keys"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    key: Mapped[uuid.UUID] = mapped_column(UUID, default=uuid.uuid4, unique=True)
    permission_db: Mapped[list[str]] = mapped_column(String, default=[])
    permission_actions: Mapped[str] = mapped_column(String, nullable=False)
    environment: Mapped[Literal["staging", "develop", "prod", "test"]] = mapped_column(String, default="test")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    