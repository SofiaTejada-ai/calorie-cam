from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_non_image_upload():
    response = client.post("/predict", files={"file": ("test.txt", b"hello", "text/plain")})
    assert response.status_code == 415
