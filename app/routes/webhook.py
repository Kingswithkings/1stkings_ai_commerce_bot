from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/webhook/sendpulse")
async def sendpulse_webhook(request: Request):
    payload = await request.json()

    # Support both:
    # 1. Simple API Request body from SendPulse flow
    # 2. Full SendPulse event webhook payload
    phone = ""
    message = ""

    if isinstance(payload, dict):
        # Simple JSON sent from API Request block
        phone = str(payload.get("phone", "")).strip()
        message = str(payload.get("message", "")).strip()

    elif isinstance(payload, list) and payload:
        # Full SendPulse event webhook payload
        event = payload[0]
        contact = event.get("contact", {}) if isinstance(event, dict) else {}
        last_message_data = contact.get("last_message_data", {}) or {}
        message_obj = last_message_data.get("message", {}) or {}
        text_obj = message_obj.get("text", {}) or {}

        phone = str(contact.get("phone", "")).strip()
        message = str(
            text_obj.get("body") or contact.get("last_message") or ""
        ).strip()

    print("SENDPULSE PHONE:", phone)
    print("SENDPULSE MESSAGE:", message)

    if message.lower() in ["hi", "hello", "hey", "start"]:
        reply = (
            "Welcome to Najeebullah Store 👋\n\n"
            "Try:\n"
            "- categories\n"
            "- search charger\n"
            "- cart\n"
            "- checkout\n"
            "- or send your order naturally"
        )
    else:
        reply = f"You said: {message}"

    return JSONResponse({
        "reply": reply,
        "phone": phone,
        "message": message,
    })