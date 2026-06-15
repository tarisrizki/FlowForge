from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base

class WebhookLog(Base):
    __tablename__ = "webhook_logs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    headers = Column(JSONB, nullable=False, default=dict)
    payload = Column(JSONB, nullable=False, default=dict)
    status = Column(String, nullable=False, default="accepted") # accepted, rejected, failed
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
