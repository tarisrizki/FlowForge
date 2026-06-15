from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.workflow import WorkflowRunStatus

class WorkflowStep(BaseModel):
    name: str
    action: str
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)

class WorkflowBase(BaseModel):
    name: str
    trigger_type: str
    steps: List[WorkflowStep] = Field(default_factory=list)
    is_active: bool = True

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    trigger_type: Optional[str] = None
    steps: Optional[List[WorkflowStep]] = None
    is_active: Optional[bool] = None

class WorkflowResponse(WorkflowBase):
    id: int

    model_config = {"from_attributes": True}

class WorkflowRunResponse(BaseModel):
    id: int
    workflow_id: int
    status: WorkflowRunStatus
    started_at: datetime
    finished_at: Optional[datetime] = None
    logs: str
    total_tokens: int

    model_config = {"from_attributes": True}
