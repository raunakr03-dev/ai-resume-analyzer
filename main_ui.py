import streamlit as st
from google import genai
from google.genai import types
import fitz  # PyMuPDF

# 🔑 API KEY (PUT YOUR REAL KEY HERE)
client = genai.Client(api_key="AIzaSyCybBHUv-7_KJ25gv50evbR8nijfDQRp90")

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("🚀 AI Resume Analyzer")
st.write("Upload your Resume (PDF / Image)")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "png", "jpg", "jpeg"])


# ================= IMAGE HANDLER =================
def analyze_image(file):
    image_bytes = file.read()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            types.Part.from_text(
                "Analyze this resume. Give strengths, weaknesses, improvements, and ATS score."
            ),
            types.Part.from_bytes(image_bytes, mime_type="image/jpeg")
        ]
    )

    return response.text


# ================= PDF HANDLER =================
def extract_pdf_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def analyze_text(text):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"""
        Analyze this resume:
        1. Strengths
        2. Weaknesses
        3. Improvements
        4. ATS score

        Resume:
        {text}
        """
    )
    return response.text


# ================= MAIN =================
if uploaded_file is not None:
    file_type = uploaded_file.type

    st.success("File uploaded successfully ✅")

    if "image" in file_type:
        st.image(uploaded_file, caption="Uploaded Resume", use_container_width=True)

        with st.spinner("Analyzing Image Resume..."):
            result = analyze_image(uploaded_file)

    elif "pdf" in file_type:
        with st.spinner("Extracting PDF..."):
            text = extract_pdf_text(uploaded_file)

        st.text_area("Extracted Text Preview", text[:1000], height=200)

        with st.spinner("Analyzing PDF Resume..."):
            result = analyze_text(text)

    st.subheader("📊 Analysis Result")
    st.write(result)