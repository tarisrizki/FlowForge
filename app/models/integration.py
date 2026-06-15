from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base

class Integration(Base):
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    integration_type = Column(String, nullable=False, index=True) # e.g., "slack", "sendgrid", "http"
    config = Column(JSONB, nullable=False, default=dict)
