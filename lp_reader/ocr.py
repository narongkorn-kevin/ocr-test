from dataclasses import dataclass
from typing import List, Tuple
import easyocr
import numpy as np


@dataclass
class OCRBox:
    text: str
    confidence: float
    bbox: List[Tuple[int, int]]


class OCRService:
    def __init__(self, languages: List[str] | None = None, gpu: bool = False) -> None:
        if languages is None:
            languages = ["th", "en"]
        self._reader = easyocr.Reader(languages, gpu=gpu)

    def recognize(self, image_bgr: np.ndarray):
        import cv2
        rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        # Restrict recognizer to Thai/English letters and digits to reduce false positives
        thai_letters = "".join(chr(c) for c in range(ord("ก"), ord("ฮ") + 1))
        eng_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digits = "0123456789"
        allowlist = thai_letters + eng_letters + digits
        results = self._reader.readtext(
            rgb,
            detail=1,
            allowlist=allowlist,
        )
        boxes: List[OCRBox] = []
        for bbox, text, conf in results:
            boxes.append(OCRBox(text=text.strip(), confidence=float(conf), bbox=[tuple(map(int, p)) for p in bbox]))
        return boxes
