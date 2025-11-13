from typing import Tuple
import io
import numpy as np
from PIL import Image
import cv2


def bytes_to_bgr_image(file_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    rgb = np.array(image)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    return bgr


def path_to_bgr_image(path: str) -> np.ndarray:
    bgr = cv2.imread(path, cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError(f"Cannot read image: {path}")
    return bgr


def prepare_for_ocr(bgr: np.ndarray) -> np.ndarray:
    if bgr is None:
        raise ValueError("Empty image")
    import cv2
    h, w = bgr.shape[:2]
    # Resize up smaller images to help OCR (keeping aspect ratio)
    min_side = min(h, w)
    scale = 1.0
    target_min_side = 640
    if min_side < target_min_side:
        scale = target_min_side / float(min_side)
        bgr = cv2.resize(bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
    # Enhance contrast and reduce noise
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # Edge-preserving denoise while keeping text strokes
    gray = cv2.bilateralFilter(gray, d=5, sigmaColor=60, sigmaSpace=60)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    eq = clahe.apply(gray)
    prepared = cv2.cvtColor(eq, cv2.COLOR_GRAY2BGR)
    return prepared
