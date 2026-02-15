# Quick Start Guide

## 3 Easy Steps to Get Started

### Step 1: Install Dependencies

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Start the Application

**Windows:**
```bash
run.bat
```

**macOS/Linux:**
```bash
./run.sh
```

Or manually:
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run the server
python backend/main.py
```

### Step 3: Open in Browser

Navigate to: http://localhost:8000

## That's It! 🎉

Now you can:
1. Upload a PDF file
2. Adjust reading speed (100-1000 WPM)
3. Use keyboard shortcuts (Space to play/pause, Arrow keys for speed/navigation)
4. Review paragraphs or sentences in detail

## Optional: OCR Support

For scanned PDFs, install Tesseract:

**Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki
**macOS:** `brew install tesseract`
**Linux:** `sudo apt-get install tesseract-ocr`

Then check "Use OCR" when uploading your PDF.

## Troubleshooting

**"Module not found" errors:**
- Make sure you ran the setup script
- Activate the virtual environment before running

**Port 8000 already in use:**
- Change port in `backend/main.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`

**Slow performance:**
- Reduce WPM speed
- Disable OCR if not needed
- Use a smaller PDF file

## Need Help?

Check the full README.md for detailed documentation.
