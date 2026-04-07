import streamlit as st
import google.generativeai as genai
import fitz
import os

# 🔑 API
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="AI Resume Analyzer")
st.title("🚀 AI Resume Analyzer")

target_job = st.text_input("🎯 Enter Target Job Role (optional)")
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "png", "jpg", "jpeg"])

# ================= PDF =================
def extract_pdf_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def analyze_text(text):
    prompt = f"""
    Analyze this resume for the role: {target_job or "General"}.

    Give:
    1. Strengths
    2. Weaknesses
    3. Improvements
    4. ATS score

    Resume:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text

# ================= IMAGE =================
def analyze_image(file):
    image_bytes = file.read()

    prompt = f"""
    Analyze this resume for the role: {target_job or "General"}.

    Give:
    1. Strengths
    2. Weaknesses
    3. Improvements
    4. ATS score
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            prompt,
            {"mime_type": "image/jpeg", "data": image_bytes}
        ]
    )

    return response.text

# ================= MAIN =================
if uploaded_file:
    st.success("File uploaded successfully ✅")

    if "pdf" in uploaded_file.type:
        text = extract_pdf_text(uploaded_file)
        st.text_area("Preview", text[:1000])

        result = analyze_text(text)

    else:
        st.image(uploaded_file)
        result = analyze_image(uploaded_file)

    st.subheader("📊 Analysis")
    st.markdown(result)

    st.download_button("📥 Download", result, file_name="analysis.txt")