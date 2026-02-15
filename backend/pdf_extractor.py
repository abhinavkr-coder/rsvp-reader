import io
import pdfplumber
import fitz  # PyMuPDF
from typing import List, Dict
import re

class PDFExtractor:
    def __init__(self):
        self.pdf = None
        self.file_content = None
        
    def load_pdf(self, pdf_content: bytes):
        self.file_content = pdf_content
        self.pdf = pdfplumber.open(io.BytesIO(pdf_content))
        
    def extract_text(self) -> str:
        if not self.pdf:
            return ""
            
        full_text = []
        for page in self.pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
                
        return "\n\n".join(full_text)
    
    def extract_with_ocr(self, pdf_content: bytes) -> str:
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        full_text = []
        
        for page_num, page in enumerate(doc):
            text = page.get_text()
            
            if len(text.strip()) < 50:
                pix = page.get_pixmap(dpi=300)
                img_data = pix.tobytes("png")
                
                try:
                    import pytesseract
                    text = pytesseract.image_to_string(io.BytesIO(img_data))
                except ImportError:
                    pass
            
            if text.strip():
                full_text.append(text)
        
        doc.close()
        return "\n\n".join(full_text)
    
    def extract_structured(self, use_ocr: bool = False) -> Dict:
        if use_ocr:
            text = self.extract_with_ocr(self.file_content if self.file_content else b'')
        else:
            text = self.extract_text()
        
        paragraphs = self._split_into_paragraphs(text)
        sentences = self._split_into_sentences(text)
        words = self._split_into_words(text)
        
        return {
            "full_text": text,
            "paragraphs": paragraphs,
            "sentences": sentences,
            "words": words
        }
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _split_into_sentences(self, text: str) -> List[str]:
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _split_into_words(self, text: str) -> List[str]:
        words = re.findall(r'\b\w+\b', text)
        return words
    
    def close(self):
        if self.pdf:
            self.pdf.close()

def extract_pdf(file_content: bytes, use_ocr: bool = False) -> Dict:
    extractor = PDFExtractor()
    try:
        extractor.load_pdf(file_content)
        return extractor.extract_structured(use_ocr)
    finally:
        extractor.close()
