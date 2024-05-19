import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import hmac

st.set_page_config(page_title="AI Resume Assistant")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])


def get_gemini_response(input,pdf_cotent,prompt):
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


#Authentication 
def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.header("Welcome to the AI Resume Helper")
            # st.subheader("Powered by Google Gemini Pro | Developed by Paul C")
            st.subheader("Please use the login credentials provided by Paul")
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

submit1 = st.button("Improve My Resume")

# submit1 = st.button("Tell Me About the Resume")

# submit2 = st.button("Keywords (Not) in Resume?")

# submit3 = st.button("Percentage match & Final Evaluation")


input_prompt1 = st.secrets["input_prompt1"]

# input_prompt1 = """
# As an experienced HR professional with a background in the biotechnology and pharmaceutical industry, your responsibility is to meticulously scrutinize the provided resume in comparison to the job description. 
# Offer a professional and objective assessment regarding the alignment of the candidate's profile with the role. 
# Emphasize both the strengths and weaknesses of the candidate concerning the specified job requirements. Your evaluation should be rigorous and incisive. Note that the candidate is an individual, so refrain from using impersonal pronouns such as 'they' or 'them'.

# """


# input_prompt2 = st.secrets["input_prompt2"]

# input_prompt1 =  
# """
# For Section 1, Employed as a sophisticated application tracking system, meticulously dissect the given job description to compile a comprehensive table delineating essential keywords encompassing both technical and soft skills.
# Utilizing the initial table as a foundation, craft a secondary table categorizing the identified keywords based on their presence within the provided resume. Present the response in a structured format consisting of two columns.
# Ensure consistency in results by following a standardized methodology for keyword extraction and resume analysis.


# For Section 2, Imagine you are an adept ATS (Applicant Tracking System) scanner, well-versed in the nuances of the biotechnology and pharmaceutical industry, as well as the functionality of ATS systems. 
# Your objective is to assess a resume in comparison to the provided job description and determine the percentage of match between the two. 
# Initially, present the output as a percentage, followed by a list of missing keywords, and conclude with your final thoughts.



# """



# input_prompt3 = st.secrets["input_prompt3"]
# input_prompt1 = """Employed as a sophisticated application tracking system, meticulously dissect the given job description to compile a comprehensive table delineating essential keywords encompassing both technical and soft skills.
# Utilizing the initial table as a foundation, craft a secondary table categorizing the identified keywords based on their presence within the provided resume. Present the response in a structured format consisting of two columns.
# Ensure consistency in results by following a standardized methodology for keyword extraction and resume analysis.
# """

input_prompt2 = """Employed as a sophisticated application tracking system, meticulously dissect the given job description to compile a comprehensive table delineating essential keywords encompassing both technical and soft skills.
Utilizing the initial table as a foundation, craft a secondary table categorizing the identified keywords based on their presence within the provided resume. Present the response in a structured format consisting of two columns.
Ensure consistency in results by following a standardized methodology for keyword extraction and resume analysis.

"""


input_prompt3 = """
Imagine you are an adept ATS (Applicant Tracking System) scanner, well-versed in the nuances of the biotechnology and pharmaceutical industry, as well as the functionality of ATS systems. 
Your objective is to assess a resume in comparison to the provided job description and determine the percentage of match between the two. 
Initially, present the output as a percentage, followed by a list of missing keywords, and conclude with your final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file,filename)
        response_1=get_gemini_response(input_text,pdf_content,input_prompt1)
        st.subheader("The Repsonse is")
        st.write(response_1)

        response_2=get_gemini_response(input_text,pdf_content,input_prompt2)
        st.subheader("The Repsonse is")
        st.write(response_2)

        response_3=get_gemini_response(input_text,pdf_content,input_prompt3)
        st.subheader("The Repsonse is")
        st.write(response_3)


    else:
        st.write("Please uplaod the resume")

# elif submit2:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file,filename)
#         response=get_gemini_response(input_text,pdf_content,input_prompt2)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")


# elif submit3:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file,filename)
#         response=get_gemini_response(input_prompt3,pdf_content,input_text)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")