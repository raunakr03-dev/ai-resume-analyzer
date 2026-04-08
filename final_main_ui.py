import streamlit as st
import google.generativeai as genai
import fitz
import os

# 🔑 Configure API
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API Key not found. Please set GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("🚀 AI Resume Analyzer")

target_job = st.text_input("🎯 Enter Target Job Role (optional)")
uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf", "png", "jpg", "jpeg"])

# ================= PDF =================
def extract_pdf_text(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except:
        return None

def analyze_text(text):
    try:
        prompt = f"""
        Analyze this resume for the role: {target_job or "General"}.

        Guidelines:
        - Do NOT assume dates are incorrect unless clearly unrealistic.
        - Treat past, present, or ongoing dates as valid.
        - Avoid false assumptions or labeling something as a "red flag" unnecessarily.
        - Focus on constructive, realistic, and helpful feedback.
        - Avoid harsh or misleading statements.

        Give:
        1. Strengths
        2. Weaknesses
        3. Improvements (actionable suggestions)
        4. ATS score (out of 100)

        Resume:
        {text}
        """

        model = genai.GenerativeModel("gemini-3-flash-preview")
        response = model.generate_content(prompt)

        return response.text if response else "⚠️ No response from AI."

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ================= IMAGE =================
def analyze_image(file):
    try:
        image_bytes = file.read()

        prompt = f"""
        Analyze this resume for the role: {target_job or "General"}.

        Guidelines:
        - Do NOT assume dates are incorrect unless clearly unrealistic.
        - Treat past, present, or ongoing dates as valid.
        - Avoid false assumptions or labeling something as a "red flag" unnecessarily.
        - Focus on constructive, realistic, and helpful feedback.
        - Avoid harsh or misleading statements.

        Give:
        1. Strengths
        2. Weaknesses
        3. Improvements (actionable suggestions)
        4. ATS score (out of 100)
        """

        model = genai.GenerativeModel("gemini-3-flash-preview")

        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])

        return response.text if response else "⚠️ No response from AI."

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ================= MAIN =================
if uploaded_file:
    st.success("✅ File uploaded successfully")

    if "pdf" in uploaded_file.type:
        text = extract_pdf_text(uploaded_file)

        if text:
            st.text_area("📄 Resume Preview", text[:1000])
            result = analyze_text(text)
        else:
            st.error("❌ Failed to read PDF file.")
            st.stop()

    else:
        st.image(uploaded_file, caption="Uploaded Resume")
        result = analyze_image(uploaded_file)

    st.subheader("📊 Analysis Result")
    st.markdown(result)

    st.download_button("📥 Download Analysis", result, file_name="analysis.txt")