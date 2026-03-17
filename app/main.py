from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router
from app.routes.products import router as products_router
from app.routes.webhook import router as sendpulse_router   # ✅ ADD THIS

app = FastAPI(title="Conversational Ordering API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)
app.include_router(chat_router)
app.include_router(sendpulse_router)   # ✅ ADD THIS