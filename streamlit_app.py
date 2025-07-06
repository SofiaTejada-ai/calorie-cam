import io, json, requests
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

BACKEND_URL = "http://127.0.0.1:8000/predict"   # change if running elsewhere

st.set_page_config(page_title="CalorieCam", page_icon="🍽️")
st.title("CalorieCam – estimate calories from a photo")

uploaded = st.file_uploader("Upload a food photo", type=["jpg", "jpeg", "png"])

if uploaded:
    # show the image on the left
    img = Image.open(uploaded)
    st.image(img, caption="Your upload", use_container_width=True)

    with st.spinner("Calling FastAPI backend…"):
        resp = requests.post(
            BACKEND_URL,
            files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        )

    if resp.ok:
        data = resp.json()
        st.subheader("Prediction JSON")
        st.json(data)

        if data["items"]:
            # make a simple bar-chart of calories per item
            labels = [it["name"] for it in data["items"]]
            kcals  = [it["calories"] for it in data["items"]]

            fig, ax = plt.subplots()
            ax.bar(labels, kcals)
            ax.set_ylabel("Calories (kcal)")
            ax.set_title("Per-item calorie estimate")
            st.pyplot(fig)

            st.success(f"**Total calories ≈ {data['total_calories']} kcal**")
        else:
            st.warning("No food detected – try better lighting or another angle.")
    else:
        st.error(f"Server error {resp.status_code}: {resp.text}")
