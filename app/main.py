from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from .core import ChaparinoHub
from .templates import ChaparinoTemplates
from .utils import process_bulk_dispatch
import json

app = FastAPI(title="Chaparino API")
hub = ChaparinoHub()

@app.post("/send/single")
async def single_send(
    provider: str = Form(...), # 'sms' or 'bale'
    template: str = Form(...),
    phone: str = Form(...),
    params: str = Form("{}") # JSON string of variables like {"name": "Amir"}
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

@app.post("/send/bulk")
async def bulk_send(
    provider: str = Form(...),
    template: str = Form(...),
    file: UploadFile = File(...)
):
    provider_func = hub.send_bale if provider == "bale" else hub.send_sms
    try:
        results = process_bulk_dispatch(file.file, provider_func, template)
        return {"total": len(results), "details": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))