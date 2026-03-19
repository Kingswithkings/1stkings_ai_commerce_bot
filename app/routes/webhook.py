from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/webhook/sendpulse")
async def sendpulse_webhook(request: Request):
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    print("RAW PAYLOAD:", payload)

    phone = ""
    message = ""

    if isinstance(payload, dict):
        phone = str(payload.get("phone", "")).strip()
        message = str(payload.get("message", "")).strip()

    elif isinstance(payload, list) and payload:
        event = payload[0]
        contact = event.get("contact", {})
        last_message_data = contact.get("last_message_data", {}) or {}
        message_obj = last_message_data.get("message", {}) or {}
        text_obj = message_obj.get("text", {}) or {}

        phone = str(contact.get("phone", "")).strip()
        message = str(text_obj.get("body") or contact.get("last_message") or "").strip()

    reply = f"DEBUG OK | phone={phone} | message={message}"

    return JSONResponse({
        "text": reply
    })