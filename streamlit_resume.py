import streamlit as st
import google.generativeai as genai
import os
import fitz


from dotenv import load_dotenv
import json

# load_dotenv()

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="ATS Resume EXpert")

st.write("google_api",st.secrets["GOOGLE_API_KEY"])

genai.configure(api_key="google_api")



def get_gemini_response(input,pdf_cotent,prompt):
    # model=genai.GenerativeModel('gemini-pro-vision')
    model=genai.GenerativeModel('gemini-1.0-pro-001')

    print('get gemini step 1 works')
    # print(pdf_content)
    response=model.generate_content([input,pdf_content,prompt])
    print('get gemini step 2 works')

    return response.text


def extract_text(file_path):
 
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def input_pdf_setup(uploaded_file,filename):

    if filename.endswith('.pdf') or filename.endswith('.docx'):
        try:
            extracted_text = extract_text(uploaded_file)
            print(f"Extracted text from {uploaded_file}:")
            print(extracted_text)
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

input_prompt1 = """
 You are an experienced HR with tech exprience in the field of biotechnology and pharmaceutical industry,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
 Act as an experienced application tracking system,  create a table of keywords in skills and tools based on the job description.
Create a 2nd column labeling those keywords depending on whether they were found in this resume. Write the response in 2 columns. Proceed in a step-wise manner

"""

#  and in the field of biotechnology and pharmaceutical industry 

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of biotechnology and pharmaceutical industry and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

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