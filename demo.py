import argparse
import time
import cv2
from lp_reader.pipeline import PlateReader
from lp_reader.utils import path_to_bgr_image


def run_image(path: str) -> None:
    reader = PlateReader()
    image = path_to_bgr_image(path)
    result = reader.read(image)
    print("Candidates:")
    for c in result["candidates"]:
        print(f"- {c['text']} (conf={c['confidence']:.2f}, score={c['score']:.2f})")


def run_camera(index: int) -> None:
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera index {index}")
    reader = PlateReader()
    last_text = ""
    last_time = 0.0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            now = time.time()
            if now - last_time > 0.5:
                result = reader.read(frame)
                last_text = result["candidates"][0]["text"] if result["candidates"] else ""
                last_time = now

            display = frame.copy()
            if last_text:
                cv2.putText(display, last_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

            cv2.imshow("License Plate Reader", display)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, help="Absolute path to image file")
    parser.add_argument("--camera", type=int, help="Camera index (e.g. 0)")
    args = parser.parse_args()

    if args.image:
        run_image(args.image)
    elif args.camera is not None:
        run_camera(args.camera)
    else:
        parser.print_help()
