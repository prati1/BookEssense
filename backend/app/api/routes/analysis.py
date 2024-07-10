from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from typing import Dict, List
from app.core.llm_client import LLMClient
from app.core.config import settings
import os

router = APIRouter()

def get_llm_client() -> LLMClient:
    llm_type = settings.llm_type
    api_key = settings.llm_api_key
    if not api_key:
        raise ValueError("LLM_API_KEY environment variable not set")
    return LLMClient(llm_type=llm_type, api_key=api_key)

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), llm_client: LLMClient = Depends(get_llm_client)):
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Invalid file type. Only plain text files are allowed.")
    
    file_content = await file.read()
    try:
        analysis_result = llm_client.analyze_characters(file_content.decode("utf-8"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return analysis_result
