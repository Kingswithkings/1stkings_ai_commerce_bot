import os
from typing import Any

import requests


SENDPULSE_API_KEY = os.getenv("SENDPULSE_API_KEY", "")
SENDPULSE_API_BASE = os.getenv("SENDPULSE_API_BASE", "https://api.sendpulse.com/whatsapp")


class SendPulseError(Exception):
    pass


def _headers() -> dict[str, str]:
    if not SENDPULSE_API_KEY:
        raise SendPulseError("SENDPULSE_API_KEY is missing")
    return {
        "Authorization": f"Bearer {SENDPULSE_API_KEY}",
        "Content-Type": "application/json",
    }


def send_whatsapp_text(contact_id: str | int, text: str) -> dict[str, Any]:
    url = f"{SENDPULSE_API_BASE}/contacts/send"
    payload = {
        "contact_id": str(contact_id),
        "message": {
            "type": "text",
            "text": {
                "body": text
            }
        }
    }

    response = requests.post(url, headers=_headers(), json=payload, timeout=20)
    if not response.ok:
        raise SendPulseError(f"SendPulse send failed: {response.status_code} {response.text}")

    try:
        return response.json()
    except Exception:
        return {"ok": True, "raw": response.text}