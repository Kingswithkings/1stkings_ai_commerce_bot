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

    # Case 1: simple JSON sent from SendPulse API Request block
    if isinstance(payload, dict):
        phone = str(payload.get("phone", "")).strip()
        message = str(payload.get("message", "")).strip()

    # Case 2: full SendPulse event payload
    elif isinstance(payload, list) and payload:
        event = payload[0] if payload else {}
        contact = event.get("contact", {}) if isinstance(event, dict) else {}
        last_message_data = contact.get("last_message_data", {}) or {}
        message_obj = last_message_data.get("message", {}) or {}
        text_obj = message_obj.get("text", {}) or {}

        phone = str(contact.get("phone", "")).strip()
        message = str(
            text_obj.get("body") or contact.get("last_message") or ""
        ).strip()

    print("PHONE:", phone)
    print("MESSAGE:", message)

    # Temporary debug reply
    reply = f"DEBUG OK | phone={phone} | message={message}"

    # IMPORTANT: return only one field for SendPulse
    return JSONResponse({
        "text": reply
    })