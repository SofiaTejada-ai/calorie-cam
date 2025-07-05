def predict_stub(img_bytes: bytes):
    return {
        "items": [
            {"name": "banana", "calories": 105.0, "grams": 120.0},
            {"name": "boiled egg", "calories": 78.0, "grams": 50.0}
        ],
        "total_calories": 183.0
    }
