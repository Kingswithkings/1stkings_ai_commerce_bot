from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import json

router = APIRouter()


@router.post("/webhook/sendpulse")
async def sendpulse_webhook(request: Request):
    content_type = (request.headers.get("content-type") or "").lower()

    raw_body = await request.body()
    payload = None
    form_data = None

    try:
        if "application/json" in content_type:
            payload = await request.json()
        elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
            form = await request.form()
            form_data = dict(form)
        else:
            try:
                payload = json.loads(raw_body.decode("utf-8"))
            except Exception:
                payload = None
    except Exception as e:
        print("WEBHOOK PARSE ERROR:", repr(e))

    print("\n=== SENDPULSE WEBHOOK START ===")
    print("Content-Type:", content_type)
    print("Headers:", dict(request.headers))

    if payload is not None:
        print("JSON PAYLOAD:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    elif form_data is not None:
        print("FORM PAYLOAD:")
        print(form_data)
    else:
        print("RAW BODY:")
        print(raw_body.decode("utf-8", errors="replace"))

    print("=== SENDPULSE WEBHOOK END ===\n")

    return JSONResponse(
        status_code=200,
        content={"status": "ok"}
    )