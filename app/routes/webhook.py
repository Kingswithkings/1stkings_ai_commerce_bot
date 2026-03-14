from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/webhook/sendpulse")
async def sendpulse_webhook(request: Request):
    payload = await request.json()
    print("SENDPULSE PAYLOAD:", payload)

    return JSONResponse({
        "reply": "Webhook received successfully"
    })