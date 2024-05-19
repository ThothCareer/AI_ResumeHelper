import streamlit as st
import auth_functions
import google.generativeai as genai
from pypdf import PdfReader
import hmac
from docx import Document

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

def read_word(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def input_pdf_setup(uploaded_file,filename):

    if filename.endswith('.pdf'):
        try:
            extracted_text = extract_text(uploaded_file)
            # print(f"Extracted text from {uploaded_file}:")
            # print(extracted_text)
            print("=" * 50)

            return extracted_text
        except Exception as e:
            print(f"Error extracting text from {uploaded_file}: {e}")

    elif filename.endswith('.docx'):
        try:
            extracted_text = read_word(uploaded_file)
            # print(f"Extracted text from {uploaded_file}:")
            # print(extracted_text)
            print("=" * 50)

            return extracted_text
        except Exception as e:
            print(f"Error extracting text from {uploaded_file}: {e}")
    else:
        raise FileNotFoundError("No file uploaded")



st.header("ATS Resume Helper (Biotech/Pharm)")
st.subheader("Powered by Google Gemini Pro")

## -------------------------------------------------------------------------------------------------
## Not logged in -----------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
if 'user_info' not in st.session_state:
    col1,col2,col3 = st.columns([1,2,1])

    # Authentication form layout
    do_you_have_an_account = col2.selectbox(label='Do you have an account?',options=('Yes','No','I forgot my password'))
    auth_form = col2.form(key='Authentication form',clear_on_submit=False)
    email = auth_form.text_input(label='Email')
    password = auth_form.text_input(label='Password',type='password') if do_you_have_an_account in {'Yes','No'} else auth_form.empty()
    auth_notification = col2.empty()

    # Sign In
    if do_you_have_an_account == 'Yes' and auth_form.form_submit_button(label='Sign In',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Signing in'):
            auth_functions.sign_in(email,password)

    # Create Account
    elif do_you_have_an_account == 'No' and auth_form.form_submit_button(label='Create Account',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Creating account'):
            auth_functions.create_account(email,password)

    # Password Reset
    elif do_you_have_an_account == 'I forgot my password' and auth_form.form_submit_button(label='Send Password Reset Email',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Sending password reset link'):
            auth_functions.reset_password(email)

    # Authentication success and warning messages
    if 'auth_success' in st.session_state:
        auth_notification.success(st.session_state.auth_success)
        del st.session_state.auth_success
    elif 'auth_warning' in st.session_state:
        auth_notification.warning(st.session_state.auth_warning)
        del st.session_state.auth_warning

## -------------------------------------------------------------------------------------------------
## Logged in --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:
    ## Streamlit App

    input_text=st.text_area("Paste the Job Description: ",key="input")
    uploaded_file=st.file_uploader("Upload your resume(PDF or Word)...",type=["pdf","docx"])


    if uploaded_file is not None:
        st.write("File Uploaded Successfully")
        filename = uploaded_file.name
        st.write({filename})



    submit1 = st.button("Evaluate Fit & Suggestions")

    submit2 = st.button("Keywords Matching")


    input_prompt1 = st.secrets["input_prompt1"]

    input_prompt2 = st.secrets["input_prompt2"]


    if submit1:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file,filename)
            response=get_gemini_response(input_text,pdf_content,input_prompt1)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please uplaod the resume")

    elif submit2:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file,filename)
            response=get_gemini_response(input_text,pdf_content,input_prompt2)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please uplaod the resume")

## -------------------------------------------------------------------------------------------------
## Disclaimer & Sign-Out & Acct Management ---------------------------------------------------------
## -------------------------------------------------------------------------------------------------


    st.write("---")
    st.subheader("Disclaimer")
    st.write("1: The response above was generated by artificial intelligence. It may contain errors or inaccuracies, and should not be relied upon as a substitute for professional advice.")
    st.write("2: If you feel the response isn't quite right, please press the button again to give the AI another chance.")



    # Sign out
    st.subheader('Sign out:')
    st.button(label='Sign Out',on_click=auth_functions.sign_out)
    

    # Delete Account
    st.subheader('Delete account:')
    password = st.text_input(label='Confirm your password',type='password')
    st.button(label='Delete Account',on_click=auth_functions.delete_account,args=[password])