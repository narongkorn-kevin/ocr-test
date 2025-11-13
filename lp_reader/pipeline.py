from typing import Any, Dict, List
import numpy as np
from .ocr import OCRService, OCRBox
from .patterns import is_plausible_plate, normalize_plate_text, score_plate
from .utils import prepare_for_ocr


class PlateReader:
    def __init__(self) -> None:
        self.ocr = OCRService(languages=["th", "en"], gpu=False)

    def read(self, image_bgr: np.ndarray) -> Dict[str, Any]:
        image_bgr = prepare_for_ocr(image_bgr)
        boxes: List[OCRBox] = self.ocr.recognize(image_bgr)

        candidates: List[Dict[str, Any]] = []
        for box in boxes:
            if not box.text:
                continue
            if is_plausible_plate(box.text):
                from .patterns import normalize_to_plausible
                normalized = normalize_to_plausible(box.text)
                candidates.append({
                    "text": normalized,
                    "raw_text": box.text,
                    "confidence": box.confidence,
                    "bbox": box.bbox,
                    "score": score_plate(box.text, box.confidence),
                })

        candidates.sort(key=lambda x: x["score"], reverse=True)
        return {
            "candidates": candidates[:5],
            "num_ocr_boxes": len(boxes),
        }
