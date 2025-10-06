import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

st.set_page_config(page_title="Click Marker", layout="centered")
st.title("Click on the Image to Leave Dots")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)  # convert to numpy array so it's displayable

    st.write("Click anywhere on the image below to add red dots.")

    # ✅ FIX: use np.array(image) for background_image
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 1)",  # red dots
        stroke_width=5,
        stroke_color="red",
        background_image=image_np,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        key="canvas",
    )

    # Extract coordinates of all clicks
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        points = []
        for obj in objects:
            if obj["type"] == "circle":
                x, y = obj["left"], obj["top"]
                points.append((x, y))
        if points:
            st.subheader("Clicked Points:")
            st.write(points)
else:
    st.info("👆 Upload an image to begin.")
