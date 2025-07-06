#Calorie-Cam

Upload a photo of your meal → get per-item calorie estimates in seconds.  
Powered by FastAPI + YOLOv8 (segmentation) on the back-end and Streamlit on the front-end.

![demo](docs/demo.gif)

---

## Quick start

```bash
git clone https://github.com/<you>/calorie-cam.git
cd calorie-cam
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# one terminal – backend
uvicorn app.main:app --reload --port 8000

# second terminal – frontend
streamlit run streamlit_app.py
