from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_db
from app.routes.webhook import router as webhook_router

app = FastAPI(title="1stkings AI Commerce Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
app.include_router(webhook_router)


@app.get("/")
def root():
    return {
        "name": "1stkings AI Commerce Bot",
        "status": "running",
        "store": "Najeebullah Store",
        "provider": "SendPulse",
        "webhook": "/webhook/sendpulse",
    }


@app.get("/health")
def health():
    return {"ok": True}