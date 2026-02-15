# RSVP Reader - Rapid Visual Serial Presentation

A powerful web application that extracts text from PDF documents and presents it using Rapid Visual Serial Presentation (RSVP) technique. Features AI-powered focal letter highlighting using PyTorch deep learning networks.

## Features

- **PDF Text Extraction**: Extract text from PDF files using pdfplumber or OCR (Tesseract)
- **RSVP Display**: Words displayed one at a time at configurable speeds (100-1000 WPM)
- **AI-Powered Focal Letter Highlighting**: PyTorch deep learning model identifies and highlights the most salient letters in each word
- **Sentence Pauses**: Automatic pauses at sentence ends for better comprehension
- **Speed Controls**: Adjust reading speed dynamically (+/- 50 WPM)
- **Review Mode**: Review paragraphs or sentences for thorough study
- **Keyboard Shortcuts**: Space (play/pause), Arrow keys (navigation and speed)
- **Responsive Design**: Beautiful dark theme interface that works on all devices

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or download this repository:
```bash
cd rsvp-reader
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Optional: OCR Support

For OCR support with scanned PDFs, install Tesseract:

**Windows:**
```bash
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH after installation
```

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

## Running the Application

Start the server:
```bash
cd backend
python main.py
```

The application will be available at: `http://localhost:8000`

## Usage

1. **Upload PDF**: Drag and drop a PDF file or click to upload
2. **Enable OCR**: Check "Use OCR" for scanned PDFs (slower but more accurate)
3. **Control Playback**: 
   - Click Play/Pause or press Space
   - Use + / - buttons or Arrow Up/Down to adjust speed (100-1000 WPM)
4. **Review Content**: Click "Review" to see the current paragraph or sentence
5. **Navigation**: Use Arrow Left/Right to navigate review content
6. **Progress**: Track your progress with the progress bar

## Project Structure

```
rsvp-reader/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── pdf_extractor.py     # PDF text extraction
│   └── focal_model.py       # PyTorch focal letter prediction model
├── frontend/
│   ├── templates/
│   │   └── index.html       # Main HTML template
│   └── static/
│       ├── style.css        # Styling
│       └── app.js           # Frontend logic
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## How RSVP Works

Rapid Visual Serial Presentation (RSVP) is a method of displaying text one word at a time in a fixed position. This technique:

- Eliminates eye movement (saccades) needed for traditional reading
- Allows faster reading speeds while maintaining comprehension
- Reduces cognitive load by presenting information sequentially
- Uses focal letter highlighting to guide visual attention

## Focal Letter Prediction

The application uses a PyTorch neural network to predict which letters in a word are most important for reading comprehension:

- **Input**: Characters in the word (embedded as vectors)
- **Architecture**: LSTM with attention mechanism
- **Output**: Attention weights for each character position
- **Result**: The character with highest attention is highlighted

## API Endpoints

### `POST /upload-pdf`
Upload and process a PDF file.

**Request:**
- `file`: PDF file (multipart/form-data)
- `use_ocr`: Boolean (optional, default: false)

**Response:**
```json
{
  "words": [
    {
      "word": "example",
      "focal_letters": [
        {"index": 3, "char": "m", "weight": 0.45}
      ],
      "is_sentence_end": false
    }
  ],
  "paragraphs": ["First paragraph...", "Second paragraph..."],
  "sentences": ["First sentence.", "Second sentence."]
}
```

### `GET /health`
Health check endpoint.

## Deployment

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t rsvp-reader .
docker run -p 8000:8000 rsvp-reader
```

### Production Deployment

For production, use:
- Gunicorn instead of Uvicorn
- Nginx as reverse proxy
- SSL/TLS encryption
- Rate limiting
- Logging and monitoring

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## Troubleshooting

**PDF not extracting text:**
- Enable OCR option
- Ensure PDF is not password protected
- Check Tesseract installation (if using OCR)

**Slow performance:**
- Reduce WPM speed
- Disable OCR if not needed
- Use a smaller PDF file

**Focal letters not highlighting:**
- Check browser console for errors
- Ensure PyTorch is installed correctly
- Try a different word/paragraph

## Keyboard Shortcuts

- `Space`: Play/Pause
- `Arrow Up`: Increase speed (+50 WPM)
- `Arrow Down`: Decrease speed (-50 WPM)
- `Arrow Left`: Previous paragraph/sentence (in review mode)
- `Arrow Right`: Next paragraph/sentence (in review mode)

## License

This project is open source and available for educational and personal use.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Credits

Built with:
- FastAPI - Modern web framework
- PyTorch - Deep learning framework
- pdfplumber - PDF text extraction
- RSVP technique for enhanced reading speed
