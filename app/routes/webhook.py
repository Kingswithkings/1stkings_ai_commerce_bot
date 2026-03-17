from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


def extract_sendpulse_event(payload):
    """
    Supports SendPulse event webhook payloads shaped like a list.
    """
    event = payload[0] if isinstance(payload, list) and payload else payload

    contact = event.get("contact", {}) if isinstance(event, dict) else {}
    last_message_data = contact.get("last_message_data", {}) or {}
    message_obj = last_message_data.get("message", {}) or {}
    text_obj = message_obj.get("text", {}) or {}

    phone = str(contact.get("phone", "")).strip()
    message = str(text_obj.get("body") or contact.get("last_message") or "").strip()

    return {
        "phone": phone,
        "message": message,
        "raw_event": event,
    }


@router.post("/webhook/sendpulse")
async def sendpulse_webhook(request: Request):
    payload = await request.json()
    data = extract_sendpulse_event(payload)

    phone = data["phone"]
    message = data["message"]

    print("SENDPULSE PHONE:", phone)
    print("SENDPULSE MESSAGE:", message)

    # Temporary reply logic
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

    # This returns data to SendPulse, but it will only appear in chat
    # if you use an API Request block in the flow builder.
    return JSONResponse({
        "reply": reply,
        "phone": phone,
        "message": message,
    })