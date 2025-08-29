from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from models import JobApplication, JobPost
from database import get_session
from lib import get_current_user
from typing import List, Optional


router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=JobApplication, status_code=201)
def add_application(
    data: JobPost,
    session=Depends(get_session),
    user: int = Depends(get_current_user)
):
    post_data = data.model_dump()
    post_data.update({"user_id": user['id']})
    job = JobApplication(**post_data)
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


@router.get("/", response_model=List[JobApplication])
def list_applications(
    session=Depends(get_session),
    user: int = Depends(get_current_user)
):
    apps = session.exec(select(JobApplication).where(
        JobApplication.user_id == user['id'])).all()
    return apps


@router.get("/search", response_model=List[JobApplication])
def search_applications(
    status: Optional[str] = Query(None),
    session=Depends(get_session),
    user: int = Depends(get_current_user)
):
    query = select(JobApplication).where(JobApplication.user_id == user['id'])
    if status:
        query = query.where(JobApplication.status == status)
    apps = session.exec(query).all()
    if not apps:
        raise HTTPException(
            status_code=404, detail="No applications found for given query.")
    return apps
