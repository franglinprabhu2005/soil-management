import streamlit as st
import google.generativeai as genai
import requests
from io import BytesIO
import pdfplumber

st.set_page_config(page_title="Farmer Chatbot", layout="wide")

api_key = "YOUR_API_KEY"
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

@st.cache_data
def load_pdf_text_from_url(pdf_url):
    response = requests.get(pdf_url)
    response.raise_for_status()
    pdf_file = BytesIO(response.content)
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

pdf_url = "https://raw.githubusercontent.com/franglinprabhu2005/soil-management/main/mk.pdf"

try:
    knowledge_base = load_pdf_text_from_url(pdf_url)
except Exception as e:
    st.error(f"⚠️ Unable to load PDF: {e}")
    st.stop()

st.title("👨‍🌾 Farmer Assistant Chatbot")
st.markdown("""
This chatbot helps farmers understand soil types, usage, and best crops to grow.  
இந்த chatbot உங்களுக்கு மண்ணின் வகைகள் மற்றும் ஏற்ற பயிர்கள் பற்றி விளக்கம் தரும்.
""")

user_input = st.text_input("📥 Type your question here:", "What crops are best for black soil?")

if st.button("Ask the Bot"):
    with st.spinner("Thinking like a farmer... 🌾"):
        prompt = f"Use the following soil data to answer the user's question:\n\n{knowledge_base}\n\nQuestion: {user_input}"
        response = model.generate_content(prompt)
        st.success("Here’s the answer:")
        st.write(response.text)

st.markdown("---")
st.caption("Developed by Mapula Franklin for helping Indian farmers 🇮🇳")
