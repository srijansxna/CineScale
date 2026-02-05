from fastapi import FastAPI

app = FastAPI(title="Mini Netflix Video Pipeline")

@app.get("/health")
def health_check():
    return {"status": "ok"}
