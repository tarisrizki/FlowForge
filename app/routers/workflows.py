from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.db import get_db
from app.core.responses import BaseResponse
from app.models.workflow import Workflow, WorkflowRun
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate, WorkflowResponse, WorkflowRunResponse
from app.services.workflow_executor import WorkflowExecutorService

router = APIRouter(prefix="/workflows", tags=["Workflows"])

@router.get("/", response_model=BaseResponse[List[WorkflowResponse]])
async def get_workflows(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Workflow))
    workflows = result.scalars().all()
    return BaseResponse(data=workflows)

@router.post("/", response_model=BaseResponse[WorkflowResponse])
async def create_workflow(workflow_in: WorkflowCreate, db: AsyncSession = Depends(get_db)):
    workflow = Workflow(
        name=workflow_in.name,
        trigger_type=workflow_in.trigger_type,
        steps=[step.model_dump() for step in workflow_in.steps],
        is_active=workflow_in.is_active
    )
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)
    return BaseResponse(data=workflow)

@router.get("/{workflow_id}", response_model=BaseResponse[WorkflowResponse])
async def get_workflow(workflow_id: int, db: AsyncSession = Depends(get_db)):
    workflow = await db.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return BaseResponse(data=workflow)

@router.put("/{workflow_id}", response_model=BaseResponse[WorkflowResponse])
async def update_workflow(workflow_id: int, workflow_in: WorkflowUpdate, db: AsyncSession = Depends(get_db)):
    workflow = await db.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    update_data = workflow_in.model_dump(exclude_unset=True)
    if "steps" in update_data and update_data["steps"] is not None:
        update_data["steps"] = [step.model_dump() if hasattr(step, "model_dump") else step for step in update_data["steps"]]

    for key, value in update_data.items():
        setattr(workflow, key, value)
        
    await db.commit()
    await db.refresh(workflow)
    return BaseResponse(data=workflow)

@router.delete("/{workflow_id}", response_model=BaseResponse[dict])
async def delete_workflow(workflow_id: int, db: AsyncSession = Depends(get_db)):
    workflow = await db.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    await db.delete(workflow)
    await db.commit()
    return BaseResponse(message="Workflow deleted successfully", data={})

@router.post("/{workflow_id}/run", response_model=BaseResponse[WorkflowRunResponse])
async def run_workflow(workflow_id: int, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    workflow = await db.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if not workflow.is_active:
        raise HTTPException(status_code=400, detail="Workflow is not active")

    # Create a new run record
    run = WorkflowRun(workflow_id=workflow.id)
    db.add(run)
    await db.commit()
    await db.refresh(run)

    # Schedule the executor in the background
    background_tasks.add_task(WorkflowExecutorService.execute_workflow, workflow.id, run.id)

    return BaseResponse(message="Workflow execution started in background", data=run)
