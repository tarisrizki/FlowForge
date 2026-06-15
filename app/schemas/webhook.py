from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class WebhookEventPayload(BaseModel):
    """
    Generic webhook event payload parser.
    """
    event_type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    
    # Allow arbitrary extra fields
    model_config = {"extra": "allow"}

class WebhookLogResponse(BaseModel):
    id: int
    workflow_id: int
    status: str
    error_message: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
