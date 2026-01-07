import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

load_dotenv()

# Prefer loading from .env but leaving your variable for now
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(resume_text, jd_text):
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
Act as an expert ATS (Applicant Tracking System) with deep knowledge of software engineering,
data science, data analytics and big data roles. Evaluate the following resume against the
job description and provide:

1. JD Match percentage (0-100%)
2. Missing important keywords
3. Profile Summary with suggestions for improvement

Resume:
{resume_text}

Job Description:
{jd_text}

Return the response only in this JSON-like format:
{{
  "JD Match": "%",
  "Missing Keywords": [],
  "Profile Summary": ""
}}
"""

    response = model.generate_content(prompt)
    return response.text


# PDF TEXT EXTRACTION
def input_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# STREAMLIT UI
st.title("Smart ATS")
st.text("Optimize your resume for better ATS compatibility")

jd = st.text_area("Paste the job description here:")
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")

if st.button("Submit"):
    if uploaded_file is None:
        st.warning("Please upload a PDF resume first.")
    elif not jd.strip():
        st.warning("Please paste the job description.")
    else:
        resume_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(resume_text, jd)
        st.subheader("Analysis Result:")
        st.write(response)
