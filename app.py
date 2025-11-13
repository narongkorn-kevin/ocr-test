from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from lp_reader.pipeline import PlateReader
from lp_reader.utils import bytes_to_bgr_image
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import base64

app = FastAPI(title="License Plate Reader (TH/EN)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

reader = PlateReader()
templates = Jinja2Templates(directory="templates")


class Candidate(BaseModel):
    text: str
    raw_text: str
    confidence: float
    bbox: list
    score: float


class PredictionResponse(BaseModel):
    candidates: List[Candidate]
    num_ocr_boxes: int


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    content = await file.read()
    image_bgr = bytes_to_bgr_image(content)
    result = reader.read(image_bgr)
    return PredictionResponse(**result)


@app.get("/", response_class=HTMLResponse)
def web_index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "candidates": [],
        "num_ocr_boxes": 0,
        "image_data_url": None,
    })


@app.post("/web/upload", response_class=HTMLResponse)
async def web_upload(request: Request, file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    content = await file.read()
    image_bgr = bytes_to_bgr_image(content)
    result = reader.read(image_bgr)
    b64 = base64.b64encode(content).decode("utf-8")
    content_type = file.content_type or "image/jpeg"
    data_url = f"data:{content_type};base64,{b64}"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "candidates": result["candidates"],
        "num_ocr_boxes": result["num_ocr_boxes"],
        "image_data_url": data_url,
    })
