from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.task import TaskService
from app.schemas import TaskCreate, TaskUpdate, TaskOut
from app.auth.dependencies import get_current_active_user
from typing import List

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_active_user)]
)


@router.post("/", response_model=TaskOut, status_code=201)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    service = TaskService(db)
    try:
        task = service.create_task(task_in)
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get task by ID."""
    service = TaskService(db)
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=List[TaskOut])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all tasks."""
    service = TaskService(db)
    tasks = service.get_all_tasks(skip=skip, limit=limit)
    return tasks


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update task."""
    service = TaskService(db)
    task = service.update_task(task_id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete task."""
    service = TaskService(db)
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


@router.get("/project/{project_id}", response_model=List[TaskOut])
def get_tasks_by_project(
    project_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get tasks in a project."""
    service = TaskService(db)
    tasks = service.get_tasks_by_project(project_id, skip=skip, limit=limit)
    return tasks


@router.get("/status/{status}", response_model=List[TaskOut])
def get_tasks_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get tasks by status."""
    service = TaskService(db)
    tasks = service.get_tasks_by_status(status, skip=skip, limit=limit)
    return tasks


@router.get("/pending", response_model=List[TaskOut])
def get_pending_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all pending tasks."""
    service = TaskService(db)
    tasks = service.get_pending_tasks(skip=skip, limit=limit)
    return tasks
