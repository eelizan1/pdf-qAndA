import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# take pdf documents and return a single string of text containing all the content 
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs: 
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages: 
            text += page.extract_text()
    return text 

def main(): 
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books")
    st.header("Chat with multple PDF's :books:")
    st.text_input("Ask a question about your documents:")

    with st.sidebar: 
        st.subheader("Your documents")
        pdf_docs =  st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)

        # process information 
        if st.button("Process"): 
            with st.spinner("Processing"):
                # get pdf text 
                raw_text = get_pdf_text(pdf_docs)
                st.write(raw_text)

                # get the text chunks 

                # create vector store with embeddings 

if __name__ == '__main__':
    main()