import streamlit as st
import fitz  # PyMuPDF

def extract_text(file_path):
    """
    Extract text from PDF or Word files using PyMuPDF.
    
    Args:
        file_path (str): Path to the PDF or Word file.
    
    Returns:
        str: Extracted text from the file.
    """
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def main():
    st.title("PDF/Word Text Extractor")

    # File upload section
    st.subheader("Upload PDF or Word File")
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx'])

    if uploaded_file is not None:
        try:
            # Display uploaded file
            st.write("Uploaded file:")
            st.write(uploaded_file)

            # Button to extract text
            if st.button("Extract Text"):
                # Extract text from the uploaded file
                extracted_text = extract_text(uploaded_file)
                
                # Display extracted text
                st.subheader("Extracted Text:")
                st.write(extracted_text)
        except Exception as e:
            st.error(f"Error extracting text: {e}")

if __name__ == "__main__":
    main()