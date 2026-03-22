from fastapi import APIRouter, Request
from app.services.business_service import handle_text
from app.services.sendpulse_api import send_whatsapp_text, SendPulseError

router = APIRouter()


def extract_sendpulse_payload(payload):
    """
    Supports:
    1. Full SendPulse incoming webhook event payload
    2. Simpler dict payload for manual testing
    """
    event = payload[0] if isinstance(payload, list) and payload else payload
    if not isinstance(event, dict):
        return {
            "contact_id": "",
            "phone": "",
            "message": "",
            "raw_event": payload,
        }

    contact = event.get("contact", {}) or {}
    last_message_data = contact.get("last_message_data", {}) or {}
    message_obj = last_message_data.get("message", {}) or {}
    text_obj = message_obj.get("text", {}) or {}

    contact_id = (
        contact.get("id")
        or contact.get("contact_id")
        or event.get("contact_id")
        or event.get("id")
        or ""
    )

    phone = str(
        contact.get("phone")
        or event.get("phone")
        or ""
    ).strip()

    message = str(
        text_obj.get("body")
        or contact.get("last_message")
        or event.get("message")
        or ""
    ).strip()

    return {
        "contact_id": contact_id,
        "phone": phone,
        "message": message,
        "raw_event": event,
    }


@router.post("/webhook/sendpulse")
async def sendpulse_webhook(request: Request):
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    data = extract_sendpulse_payload(payload)
    contact_id = data["contact_id"]
    phone = data["phone"]
    message = data["message"]

    print("RAW PAYLOAD:", payload)
    print("CONTACT ID:", contact_id)
    print("PHONE:", phone)
    print("MESSAGE:", message)

    reply = handle_text(phone, message)
    print("REPLY:", reply)

    # Direct-send architecture:
    # Send reply back to WhatsApp through SendPulse API,
    # instead of relying on the SendPulse flow Message block.
    if contact_id:
        try:
            api_result = send_whatsapp_text(contact_id=contact_id, text=reply)
            print("SENDPULSE SEND RESULT:", api_result)
            return {"ok": True, "sent": True}
        except SendPulseError as e:
            print("SENDPULSE ERROR:", str(e))
            return {"ok": False, "sent": False, "error": str(e)}

    # Fallback for manual tests when contact_id is not present
    return {"ok": True, "sent": False, "text": reply, "warning": "contact_id missing"}