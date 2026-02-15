from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from pathlib import Path

from pdf_extractor import extract_pdf
from focal_model import focal_extractor

# Get the project root directory (parent of backend/)
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"
TEMPLATES_DIR = FRONTEND_DIR / "templates"

app = FastAPI(title="RSVP Reader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class WordWithFocal(BaseModel):
    word: str
    focal_letters: List[dict]
    is_sentence_end: bool

class TextResponse(BaseModel):
    words: List[WordWithFocal]
    paragraphs: List[str]
    sentences: List[str]

@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_path = TEMPLATES_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=500, detail=f"Template not found at {index_path}")
    
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/upload-pdf", response_model=TextResponse)
async def upload_pdf(file: UploadFile = File(...), use_ocr: bool = False):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        content = await file.read()
        extracted = extract_pdf(content, use_ocr=use_ocr)
        
        words_with_focal = []
        sentence_end_chars = {'.', '!', '?'}
        
        for i, word in enumerate(extracted['words']):
            focal_letters = focal_extractor.get_focal_letters(word)
            
            is_sentence_end = False
            if i < len(extracted['words']) - 1:
                next_word = extracted['words'][i + 1]
                is_sentence_end = any(char in sentence_end_chars for char in word)
            
            words_with_focal.append(WordWithFocal(
                word=word,
                focal_letters=focal_letters,
                is_sentence_end=is_sentence_end
            ))
        
        return TextResponse(
            words=words_with_focal,
            paragraphs=extracted['paragraphs'],
            sentences=extracted['sentences']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print(f"Starting RSVP Reader...")
    print(f"Base directory: {BASE_DIR}")
    print(f"Frontend directory: {FRONTEND_DIR}")
    print(f"Static directory: {STATIC_DIR}")
    print(f"Templates directory: {TEMPLATES_DIR}")
    print(f"\nServer will be available at: http://localhost:8000")
    print(f"\nPress CTRL+C to stop the server")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)