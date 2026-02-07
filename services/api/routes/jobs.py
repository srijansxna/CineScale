from fastapi import APIRouter, HTTPException
from services.api.core.jobs import jobs

router = APIRouter()

@router.get("/job/{job_id}")
def status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    return {"job_id": job_id, "status": jobs[job_id]["status"]}
