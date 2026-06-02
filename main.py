from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
import os
import uuid
from stt import get_stt_engine
from agent import agent
from storage import save_transaction, get_history

app = FastAPI(title="Agent Jalebi")

@app.on_event("startup")
async def startup_event():
    # Pre-load Whisper model
    get_stt_engine()

# Ensure uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class TextProcessRequest(BaseModel):
    text: str

@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    # Save audio file
    file_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.{ext}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 1. Transcribe
        stt = get_stt_engine()
        text = stt.transcribe(file_path)
        
        if not text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")
        
        # 2. Extract
        data = agent.extract_transaction(text)
        
        # 3. Validate
        if not data.get("item") or not data.get("price"):
            raise HTTPException(status_code=400, detail="Item and Price are mandatory")
        
        # 4. Save
        txn_id = save_transaction(data)
        
        return {
            "status": "success",
            "transaction_id": txn_id,
            "transcription": text,
            "extracted_data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up audio file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/process-text")
async def process_text(request: TextProcessRequest):
    try:
        data = agent.extract_transaction(request.text)
        
        if not data.get("item") or not data.get("price"):
            raise HTTPException(status_code=400, detail="Item and Price are mandatory")
        
        txn_id = save_transaction(data)
        
        return {
            "status": "success",
            "transaction_id": txn_id,
            "extracted_data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def fetch_history():
    return get_history()

# Serve static files for the frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
