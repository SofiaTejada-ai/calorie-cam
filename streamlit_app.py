import io, base64, requests
from typing import List
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt


BACKEND_URL = "http://127.0.0.1:8000/predict"   # update if you change port

st.set_page_config(
    page_title="Calorie-Cam",
    page_icon="🍽️",
    layout="centered",
)

st.title("🍽️  Calorie-Cam")
st.caption("Upload a food photo → get instant calorie breakdown and model overlay.")


uploaded = st.file_uploader("Upload a JPG / PNG image", type=["jpg", "jpeg", "png"])

if uploaded:
    # show original image in left column
    col1, col2 = st.columns(2)
    orig_img = Image.open(uploaded)
    col1.image(orig_img, caption="Original", use_container_width=True)

    # Call backend
    with st.spinner("Analyzing…"):
        try:
            resp = requests.post(
                BACKEND_URL,
                files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)},
                timeout=30,
            )
        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach the backend: {e}")
            st.stop()


    if not resp.ok:
        st.error(f"Backend error {resp.status_code}: {resp.text}")
        st.stop()

    data = resp.json()


    if data.get("overlay_png"):
        overlay_bytes = base64.b64decode(data["overlay_png"])
        col2.image(overlay_bytes, caption="Model overlay", use_container_width=True)
    else:
        col2.info("No overlay returned.")


    st.subheader("Detected items")
    st.json(data["items"])

    if data["items"]:
        labels: List[str]  = [it["name"]      for it in data["items"]]
        kcals:  List[float]= [it["calories"]  for it in data["items"]]

        fig, ax = plt.subplots()
        ax.bar(labels, kcals)
        ax.set_ylabel("Calories (kcal)")
        ax.set_title("Per-item estimate")
        st.pyplot(fig)

        st.success(f"**Total calories ≈ {data['total_calories']} kcal**")
    else:
        st.warning("No food detected. Try better lighting or a different angle.")
else:
    st.info("➡️  Upload an image to begin.")
