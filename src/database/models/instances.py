"model de instances"
from src.database.base import Base 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, UUID, Integer, DateTime
from datetime import datetime
from typing import Literal
import uuid

class Instances(Base):

    __tablename__ = "instances"

    id: Mapped[uuid.UUID] = mapped_column(UUID,primary_key=True, default=uuid.uuid4, nullable=False, index=True)
    cluster_id: Mapped[int] = mapped_column(ForeignKey("clusters.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    cluster: Mapped["Clusters"] = relationship(
        "Clusters",
        back_populates="instances"
    )