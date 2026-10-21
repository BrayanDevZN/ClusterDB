"model de clusters"
from src.database.base import Base 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, UUID, Integer, DateTime
from datetime import datetime
from typing import Literal
from .keys import keys
import uuid
class Clusters(Base):

    __tablename__ = "clusters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    public_id: Mapped[uuid.UUID] = mapped_column(UUID, default=uuid.uuid4, index=True)
    cluster_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    instance_limit: Mapped[int] = mapped_column(Integer)
    created_key: Mapped[uuid.UUID] = mapped_column(ForeignKey("keys.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    instances: Mapped[list["Instances"]] = relationship(
        "Instances",
        back_populates="cluster"
    )