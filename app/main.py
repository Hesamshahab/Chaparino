from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from .core import ChaparinoHub
from .templates import ChaparinoTemplates
from .utils import process_bulk_dispatch
import json
import os

app = FastAPI(title="Chaparino API")
hub = ChaparinoHub()

# ۱. تعریف هدر مورد نظر برای احراز هویت در کلاینت‌ها و مستندات اسمارت سواگر
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_allowed_clients():
    clients_raw = os.getenv("CHAPARINO_CLIENTS", "{}")
    try:
        return json.loads(clients_raw)
    except Exception:
        return {}

async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="API Key is missing.")
        
    allowed_clients = get_allowed_clients()
    
    # جستجوی کلید در میان کلاینت‌های مجاز
    for client_name, client_key in allowed_clients.items():
        if api_key == client_key:
            return client_name  # نام سرویس درخواست‌کننده را برمی‌گرداند تا در لاگ‌ها ثبت شود
            
    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key.")

# ۲. اعمال وابستگی (Dependency) به روت تک‌ارسال
@app.post("/send/single")
async def single_send(
    provider: str = Form(...), # 'sms' or 'bale'
    template: str = Form(...),
    phone: str = Form(...),
    params: str = Form("{}"), # JSON string of variables like {"name": "Amir"}
    api_key: str = Depends(verify_api_key) # 👈 قفل شدن روت
):
    try:
        extra_params = json.loads(params)
        message_text = ChaparinoTemplates.render(template, **extra_params)
        
        if provider == "bale":
            res = hub.send_bale(phone, message_text)
        else:
            res = hub.send_sms(phone, message_text)
        return {"status": "success", "response": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ۳. اعمال وابستگی (Dependency) به روت ارسال انبوه
@app.post("/send/bulk")
async def bulk_send(
    provider: str = Form(...),
    template: str = Form(...),
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key) # 👈 قفل شدن روت
):
    provider_func = hub.send_bale if provider == "bale" else hub.send_sms
    try:
        results = process_bulk_dispatch(file.file, provider_func, template)
        return {"total": len(results), "details": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))