from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from .schemas import Prediction
from .inference import predict_stub

app = FastAPI(
    title="CalorieCam",
    docs_url="/docs",       # change or disable this
    redoc_url="/redoc",     # or set to None to turn off
    openapi_url="/openapi.json"  # also customizable
)

@app.post("/predict", response_model=Prediction)
async def predict(file: UploadFile = File(...)):
    if file.content_type.split("/")[0] != "image":
        raise HTTPException(status_code=415, detail="Upload an image file")

    image_bytes = await file.read()
    result = predict_stub(image_bytes)
    return JSONResponse(result)
