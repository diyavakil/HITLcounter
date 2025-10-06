import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

st.set_page_config(page_title="Image Click Marker", layout="centered")
st.title("HITL test")

# Step 1: Upload an image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.write("Click anywhere on the image to add dots")
    
    # Step 2: Use drawable canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 1)",  # Red fill for dots
        stroke_width=5,
        stroke_color="red",
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        key="canvas",
    )

    # Step 3: Show coordinates of all clicked points
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
    st.info("Upload an image to begin")
