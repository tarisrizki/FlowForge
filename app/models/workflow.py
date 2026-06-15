import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base

class WorkflowRunStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    trigger_type = Column(String, nullable=False)
    steps = Column(JSONB, nullable=False, default=list)
    is_active = Column(Boolean, default=True)

    runs = relationship("WorkflowRun", back_populates="workflow", cascade="all, delete-orphan")

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    status = Column(Enum(WorkflowRunStatus), default=WorkflowRunStatus.PENDING, nullable=False)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    logs = Column(String, default="")
    total_tokens = Column(Integer, default=0)

    workflow = relationship("Workflow", back_populates="runs")
