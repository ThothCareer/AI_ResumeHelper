import streamlit as st
import google.generativeai as genai
import os
from pypdf import PdfReader


# from dotenv import load_dotenv
import json

st.set_page_config(page_title="ATS Resume EXpert")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])



def get_gemini_response(input,pdf_cotent,prompt):
    # model=genai.GenerativeModel('gemini-pro-vision')
    model=genai.GenerativeModel('gemini-1.0-pro-001')

    response=model.generate_content([input,pdf_content,prompt])

    return response.text


def extract_text(file_path):
 
    text = ""
    doc = PdfReader(file_path)
    
    for page in doc.pages:
        text += page.extract_text()
    return text


def input_pdf_setup(uploaded_file,filename):

    if filename.endswith('.pdf') or filename.endswith('.docx'):
        try:
            extracted_text = extract_text(uploaded_file)
            # print(f"Extracted text from {uploaded_file}:")
            # print(extracted_text)
            print("=" * 50)

            return extracted_text
        except Exception as e:
            print(f"Error extracting text from {uploaded_file}: {e}")
    else:
        raise FileNotFoundError("No file uploaded")



## Streamlit App


st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    filename = uploaded_file.name
    st.write({filename})



submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How many keywords are covered in my resume")

submit3 = st.button("Percentage match & Final Evaluation")


input_prompt1 = st.secrets["input_prompt1"]

input_prompt2 = st.secrets["input_prompt2"]

input_prompt3 = st.secrets["input_prompt3"]


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file,filename)
        # st.write(pdf_content)
        response=get_gemini_response(input_text,pdf_content,input_prompt1)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file,filename)
        # st.write(pdf_content)
        response=get_gemini_response(input_text,pdf_content,input_prompt2)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")


elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file,filename)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")