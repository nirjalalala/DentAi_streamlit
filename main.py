# app_frontend.py
import streamlit as st
import requests
import base64
import io
from PIL import Image

# --- State Management Initialization ---
if "prediction_data" not in st.session_state:
    st.session_state.prediction_data = None
if "result_image" not in st.session_state:
    st.session_state.result_image = None

# Define class names
CLASS_NAMES = ["Calculus", "Cavity", "Discoloration", "Gingivitis", "Hypodontia", "Ulcer"]

# --- Helper Functions ---
def clear_results():
    """Clears previous results from the session state."""
    st.session_state.prediction_data = None
    st.session_state.result_image = None

def display_formatted_results():
    """Displays results from session state."""
    if st.session_state.prediction_data is None:
        return

    st.write("---")
    st.write("### Analysis Results")
    data = st.session_state.prediction_data
    
    # # Debug: Show the complete API response structure
    # st.write("### Debug - API Response Structure")
    # st.json(data)
    
    try:
        detections = data["detections"]

        if detections is None or not isinstance(detections, list):
            st.error("Could not find a valid 'detections' list in the API response.")
            return
            
        if detections:
            st.write(f"Found {len(detections)} detections in the response.")
        
        if not detections:
            st.info("✅ No disease detected.")
        else:
            st.success(f"✅ Found {len(detections)} potential issue(s).")
            result_text = ""
            for i, det in enumerate(detections, 1):
                cls_id = det.get("class_id", -1)
                conf = det.get("confidence", 0) * 100
                class_name = CLASS_NAMES[cls_id] if 0 <= cls_id < len(CLASS_NAMES) else f"Unknown Class {cls_id}"
                result_text += f"{i}. 🦷 **{class_name}** - Confidence: {conf:.1f}%\n"
            st.markdown(result_text)

    except Exception as e:
        st.error(f"Error processing detections: {str(e)}")

    # image display handling
    if st.session_state.result_image:
        st.write("### Labeled Image")
        try:
            st.image(
                st.session_state.result_image,
                caption="Processed Image with Detections",
                use_container_width=True,
                channels="RGB"  # Explicitly set color channels
            )
        except Exception as e:
            st.error(f"Error displaying image: {e}")

# --- Main Application UI ---
st.title("DentAI Disease Detector")

uploaded_file = st.file_uploader(
    "Choose an image", type=["jpg", "jpeg", "png"], on_change=clear_results
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    if st.button("Predict"):
        clear_results()
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        
        with st.spinner("Analyzing the image..."):
            try:
                response = requests.post("http://127.0.0.1:8000/predict/", files=files, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.prediction_data = data
                    
            
                    encoded_image = data["image"]

                    if encoded_image:
                        try:
                            image_data = base64.b64decode(encoded_image)
                            st.session_state.result_image = Image.open(io.BytesIO(image_data))
                        except Exception as e:
                            st.error(f"Error processing image: {str(e)}")
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            
            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: {str(e)}")

display_formatted_results()