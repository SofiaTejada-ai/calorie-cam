from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from .schemas import Prediction
from .inference import predict

app = FastAPI(title="CalorieCam")

@app.post("/predict", response_model=Prediction)
async def predict_endpoint(file: UploadFile = File(...)):
    if file.content_type.split("/")[0] != "image":
        raise HTTPException(status_code=415, detail="Upload an image file")

    image_bytes = await file.read()
    result = predict(image_bytes)
    return JSONResponse(result)
