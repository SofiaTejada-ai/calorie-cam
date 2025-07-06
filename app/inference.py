from PIL import Image
import cv2
import io, base64, numpy as np
from typing import Dict, List
from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")
COCO_CLASSES: Dict[int, str] = model.names


FOOD_KCAL_PER_GRAM = {
    "banana":   0.89,
    "apple":    0.52,
    "pizza":    2.66,   # slice
    "carrot":   0.41,
    "broccoli": 0.34,
    "sandwich": 2.40,
}


DEFAULT_GRAMS = {
    "banana":   118,
    "apple":    182,
    "pizza":    125,   # 1 slice
    "carrot":   61,
    "broccoli": 91,
    "sandwich": 200,
}

def predict(img_bytes: bytes) -> dict:

    pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")


    result = model.predict(pil_img, verbose=False)[0]


    items: List[dict] = []
    for box, cls_id in zip(result.boxes.data, result.boxes.cls):
        class_name = COCO_CLASSES[int(cls_id)]


        if class_name not in FOOD_KCAL_PER_GRAM:
            continue


        grams = DEFAULT_GRAMS.get(class_name, 100)
        kcal  = round(FOOD_KCAL_PER_GRAM[class_name] * grams, 1)

        items.append({
            "name":      class_name,
            "grams":     grams,
            "calories":  kcal,
        })

    total_kcal = round(sum(i["calories"] for i in items), 1)


    overlay_bgr: np.ndarray = result.plot()
    overlay_rgb = cv2.cvtColor(overlay_bgr, cv2.COLOR_BGR2RGB)


    buf = io.BytesIO()
    Image.fromarray(overlay_rgb).save(buf, format="PNG")
    overlay_b64 = base64.b64encode(buf.getvalue()).decode()

    return {
        "items":          items,
        "total_calories": total_kcal,
        "overlay_png":    overlay_b64,
    }
