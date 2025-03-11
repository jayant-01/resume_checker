from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):

    file_bytes = uploaded_file.read()

    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(file_bytes)

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    



## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("Increase Your Chance Of Getting Selected By Enhancing Your Resume For The Job Role")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")



submit1 = st.button("Tell Me About the Resume",type="primary")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match", type="primary")


input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""


input_prompt3 = """
Given a resume and a job description, generate a table illustrating the match. Use cues to represent high, medium, and low match areas, 
highlighting strengths and weaknesses. Analyze a resume and job description. Identify keywords and skills from the job description absent 
in the resume. Prioritize based on frequency and relevance to the job. Provide suggestions for integrating these keywords into the resume, 
emphasizing achievements and quantifiable results. On the top give the match percentage and required keywords extracted from job description 
that are missing in resume.
""" 

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")