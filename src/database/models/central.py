"Controla Central"
from src.database.base import Base 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey,  JSON
from .instances import Instances
import uuid

class Central(Base):

    __tablename__ = "central"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    instance_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("instances.id"), nullable=False, index=True, unique=True)
    mean: Mapped[list[float]] = mapped_column(JSON, nullable=False)
