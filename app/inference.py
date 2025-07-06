from ultralytics import YOLO
from PIL import Image
import io

# Load the YOLOv8n-seg model (pretrained on COCO)
model = YOLO("yolov8n-seg.pt")

# Simplified calorie lookup for now
FOOD_KCAL_PER_GRAM = {
    "banana": 0.89,
    "apple": 0.52,
    "pizza": 2.66,
    "carrot": 0.41,
    "broccoli": 0.34,
    "sandwich": 2.4
}

# Class names from the COCO dataset
COCO_CLASSES = model.names  # e.g., {0: 'person', 1: 'bicycle', ..., 46: 'banana'}

def predict(img_bytes: bytes) -> dict:
    # Convert raw bytes to PIL Image
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    # Run YOLOv8 model
    results = model.predict(img, verbose=False)[0]

    items = []
    for box, cls_id in zip(results.boxes.data, results.boxes.cls):
        class_name = COCO_CLASSES[int(cls_id)]

        if class_name not in FOOD_KCAL_PER_GRAM:
            continue  # skip non-food items

        # Fake weight estimate: bigger box = more food
        xyxy = box[:4]
        area = (xyxy[2] - xyxy[0]) * (xyxy[3] - xyxy[1])
        DEFAULT_GRAMS = {
            "banana": 118,  # average grams per USDA
            "apple": 182,
            "pizza": 125,  # 1 slice
            "carrot": 61,
            "broccoli": 91,
            "sandwich": 200
        }
        grams = DEFAULT_GRAMS.get(class_name, 100)
  # naive scale
        kcal = round(FOOD_KCAL_PER_GRAM[class_name] * grams, 1)

        items.append({
            "name": class_name,
            "grams": grams,
            "calories": kcal
        })

    total_kcal = round(sum(i["calories"] for i in items), 1)
    return {"items": items, "total_calories": total_kcal}
