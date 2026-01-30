from __future__ import annotations

import base64
import io
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel, Field
import vtracer

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=400)


class GenerateResponse(BaseModel):
    svg: str


def _extract_image_bytes(response: types.GenerateContentResponse) -> bytes:
    parts = getattr(response, "parts", None)
    if parts:
        for part in parts:
            inline_data = getattr(part, "inline_data", None)
            if not inline_data or not inline_data.data:
                continue
            data = inline_data.data
            if isinstance(data, str):
                return base64.b64decode(data)
            return data

    for candidate in response.candidates or []:
        content = candidate.content
        if not content:
            continue
        for part in content.parts:
            inline_data = getattr(part, "inline_data", None)
            if not inline_data or not inline_data.data:
                continue
            data = inline_data.data
            if isinstance(data, str):
                return base64.b64decode(data)
            return data

    raise HTTPException(status_code=500, detail="Image generation returned no image data.")


@app.post("/generate", response_model=GenerateResponse)
def generate_favicon(request: GenerateRequest) -> GenerateResponse:
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is missing.")
    print("API Key", api_key)
    client = genai.Client(api_key=api_key)

    full_prompt = (
        "Create a clean, centered favicon icon with a transparent background. "
        "Use flat colors, minimal detail, and a single subject. Prompt: "
        f"{prompt}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=full_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        ),
    )

    image_bytes = _extract_image_bytes(response)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    raster_buffer = io.BytesIO()
    image.save(raster_buffer, format="PNG")

    svg = vtracer.convert_raw_image_to_svg(raster_buffer.getvalue(), img_format="png")

    return GenerateResponse(svg=svg)
