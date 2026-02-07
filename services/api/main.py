from fastapi import FastAPI
from services.api.routes import upload, jobs

app = FastAPI(title="CineScale")

app.include_router(upload.router)
app.include_router(jobs.router)

@app.get("/health")
def health():
    return {"status": "ok"}
