from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import DateTime, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from python_api.database import Base

class TodoDB(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True), 
      default=lambda: datetime.now(timezone.utc)
    )