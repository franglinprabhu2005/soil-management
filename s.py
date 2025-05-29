import streamlit as st

# ✅ THIS MUST BE FIRST Streamlit command
st.set_page_config(page_title="Farmer Chatbot", layout="wide")

import google.generativeai as genai
from PyPDF2 import PdfReader
import os

# Get API key from Streamlit secrets
api_key = "AIzaSyBoGkf3vaZuMWmegTLM8lmVpvvoSOFYLYU"
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Read content from the PDF file
@st.cache_data
def load_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# Define the PDF path (update this if needed)
pdf_path = "s/mk.pdf"


# Check if file exists
if not os.path.exists(pdf_path):
    st.error("⚠️ PDF file not found. Please check the file path.")
    st.stop()

# Load content from PDF
knowledge_base = load_pdf_text(pdf_path)

# UI
st.title("👨‍🌾 Farmer Assistant Chatbot")
st.markdown("""
This chatbot helps farmers understand soil types, usage, and best crops to grow.  
இந்த chatbot உங்களுக்கு மண்ணின் வகைகள் மற்றும் ஏற்ற பயிர்கள் பற்றி விளக்கம் தரும்.
""")

# User input
user_input = st.text_input("📥 Type your question here:", "What crops are best for black soil?")

# Ask Gemini when button clicked
if st.button("Ask the Bot"):
    with st.spinner("Thinking like a farmer... 🌾"):
        prompt = f"Use the following soil data to answer the user's question:\n\n{knowledge_base}\n\nQuestion: {user_input}"
        response = model.generate_content(prompt)
        st.success("Here’s the answer:")
        st.write(response.text)

# Footer
st.markdown("---")
st.caption("Developed by Mapula Franklin for helping Indian farmers 🇮🇳")
