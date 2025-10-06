import streamlit as st
import base64
from io import BytesIO
from PIL import Image

st.title("Image Click Dot Drawer")

# Maximum dimensions for display
MAX_WIDTH = 1000
MAX_HEIGHT = 600

def resize_image(image, max_width=MAX_WIDTH, max_height=MAX_HEIGHT):
    """Resize image while preserving aspect ratio."""
    img = image.copy()
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    return img

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "gif"])

if uploaded_file is not None:
    # Read and process the uploaded image
    img_bytes = uploaded_file.read()
    img = Image.open(BytesIO(img_bytes))
    
    # Resize image to fit within max dimensions
    resized_img = resize_image(img)
    width, height = resized_img.size
    
    # Convert resized image to bytes for base64 encoding
    buffered = BytesIO()
    resized_img.save(buffered, format=img.format if img.format else "PNG")
    base64_img = base64.b64encode(buffered.getvalue()).decode()
    
    # Get the MIME type
    mime_type = uploaded_file.type or "image/png"
    
    # HTML and JavaScript for canvas
    html_code = f"""
    <canvas id="canvas" width="{width}" height="{height}" style="border:1px solid #000000;"></canvas>
    <script>
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    var img = new Image();
    img.src = 'data:{mime_type};base64,{base64_img}';
    img.onload = function() {{
        ctx.drawImage(img, 0, 0, {width}, {height});
    }};
    canvas.addEventListener('click', function(event) {{
        var rect = canvas.getBoundingClientRect();
        var x = event.clientX - rect.left;
        var y = event.clientY - rect.top;
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fillStyle = 'red';
        ctx.fill();
    }});
    </script>
    """
    
    # Render the HTML in Streamlit
    st.components.v1.html(html_code, height=height + 10, width=width + 10)
