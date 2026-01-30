# Favicon Creator

Generate SVG favicons from text prompts. The backend uses Gemini image generation ("Nano Banana") to create a raster icon, then vectorizes it with vtracer. The frontend provides a prompt textarea, preview, and download.

## Prerequisites
- Python 3.11+
- Node.js 18+
- A Gemini API key

## Backend setup
1) Create and activate the virtual environment (from repo root):
```
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:
```
pip install -r backend/requirements.txt
```

3) Set your API key in `backend/.env`:
```
GEMINI_API_KEY=YOUR_REAL_KEY
```

4) Run the API (from repo root):
```
uvicorn main:app --reload --app-dir backend
```

The API will be available at `http://localhost:8000`.

## Frontend setup
1) Install dependencies:
```
cd favicon-creator-frontend
npm install
```

2) (Optional) Override the API URL:
```
export VITE_API_URL=http://localhost:8000/generate
```

3) Run the dev server:
```
npm run dev
```

Open the app at `http://localhost:5173`.

## Test script
With the backend running, you can generate a sample SVG:
```
python test_scripts/test_generate.py
```

The output will be saved to `test_scripts/output.svg`.
