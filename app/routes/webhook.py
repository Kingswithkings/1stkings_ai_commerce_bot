from fastapi import APIRouter, Request
from app.services.business_service import handle_text

router = APIRouter()


@router.post("/webhook/sendpulse")
async def sendpulse_webhook(request: Request):
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    phone = payload.get("phone", "")
    message = payload.get("message", "")

    reply = handle_text(phone, message)

    print("REPLY:", reply)

    return {
        "text": reply
    }