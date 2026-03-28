from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Column, DateTime, ForeignKey, Text
from typing import Optional
from ..core.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), ondelete="CASCADE", nullable=False)
    assignee_id: Mapped[Optional[int]]= mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False)

    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    assignee: Mapped[Optional["User"]] = relationship(
        "User", back_populates="assigned_tasks", foreign_keys=[assignee_id]
    )