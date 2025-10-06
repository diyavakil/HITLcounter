import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

st.set_page_config(page_title="Click Marker", layout="centered")
st.title("Click on the Image to Leave Dots")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.write("Click anywhere on the image below to add red dots.")

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 1)",  # red dots
        stroke_width=5,
        stroke_color="red",
        background_image=image,  # <-- keep it as a Pillow image here
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        points = [
            (obj["left"], obj["top"])
            for obj in objects
            if obj["type"] == "circle"
        ]
        if points:
            st.subheader("Clicked Points:")
            st.write(points)
else:
    st.info("👆 Upload an image to begin.")
