from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
import fitz  # PyMuPDF
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI model with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    """
    Generates a response using the Google Gemini Generative AI model.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    """
    Converts the uploaded PDF to an image using PyMuPDF and returns the first page as a base64-encoded JPEG.
    """
    if uploaded_file is not None:
        try:
            # Open the uploaded PDF with PyMuPDF
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            
            # Extract the first page as an image
            first_page = pdf_document.load_page(0)  # Load the first page
            pix = first_page.get_pixmap()  # Convert the page to an image
            
            # Convert the image to bytes
            img_byte_arr = io.BytesIO(pix.tobytes("jpeg"))
            
            # Convert the image to base64
            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr.getvalue()).decode()  # Encode to base64
                }
            ]
            return pdf_parts
        except Exception as e:
            st.error(f"Error processing the PDF file: {str(e)}")
            return None
    else:
        raise FileNotFoundError("No file uploaded")

# Function to hide Streamlit style
def hide_streamlit_style():
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")

# Hide Streamlit style
hide_streamlit_style()

st.header("ATS Tracking System")

# Input fields for job description and resume upload
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Buttons for different actions
submit1 = st.button("Tell me about the resume")
submit2 = st.button("Percentage match")
submit3 = st.button("How can I improve my Skills?")

# Prompt templates
input_prompt1 = """
You are an experienced Technical Human Resource Manager specializing in talent acquisition and resume evaluation. 
Review the uploaded resume and provide an insightful analysis, including the applicant's key strengths, areas for improvement, and relevance to the provided job description. 
Please format your response as a professional summary.
"""

input_prompt2 = """
You are a skilled Applicant Tracking System (ATS) scanner with expertise in evaluating resumes against job descriptions. 
Analyze the uploaded resume in comparison to the provided job description and give a detailed report on the percentage match. 
Provide insights on how well the resume aligns with the job requirements and suggest any missing or misaligned qualifications.
"""
input_prompt3 = """
You are an experienced Technical Human Resource Manager specializing in talent acquisition and resume evaluation. 
Review the uploaded resume and suggest the user how they can improve their skills relevance to the provided job description. 
Please format your response as a professional summary.
"""

# When the first button is pressed
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload the resume")

# When the second button is pressed
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_text, pdf_content, input_prompt2)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload the resume")
        
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload the resume")
