import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Securely fetch the API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API Key not found. Please check your .env file.")
else:
    genai.configure(api_key=api_key)

    # --- UI Layout ---
    st.set_page_config(page_title="Image AI Explorer", layout="wide")
    st.header("🖼️ Gemini Image Analysis")

    # Use columns for a cleaner look
    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Preview", use_container_width=True)

    with col2:
        prompt = st.text_input("What would you like to know?", placeholder="Describe this image...")
        
        # Skill: Only run if button is clicked AND input is valid
        if st.button("GET RESPONSE"):
            if uploaded_file and prompt:
                try:
                    with st.spinner("Analyzing image..."):
                        # Re-opening image to ensure it's fresh for the model
                        img_to_process = Image.open(uploaded_file)
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        
                        response = model.generate_content([prompt, img_to_process])
                        
                        st.success("Analysis Complete!")
                        st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please provide both an image and a text prompt.")