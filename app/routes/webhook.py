from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/webhook/sendpulse")
async def sendpulse_webhook(request: Request):
    try:
        payload = await request.json()
    except:
        payload = {}

    phone = payload.get("phone", "")
    message = payload.get("message", "")

    reply = f"DEBUG OK | phone={phone} | message={message}"

    print("REPLY:", reply)

    return {
        "text": reply
    }