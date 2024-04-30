import streamlit as st
import google.generativeai as genai
# import os
from pypdf import PdfReader
# import json

st.set_page_config(page_title="AI Resume Assistant")

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

# streamlit_app.py

import hmac
import streamlit as st


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()

## Streamlit App


st.header("AI Resume Helper")
st.subheader("Powered by Google Gemini Pro | Developed by Paul C")
input_text=st.text_area("Paste the Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    filename = uploaded_file.name
    st.write({filename})



submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("Keywords (Not) in Resume?")

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