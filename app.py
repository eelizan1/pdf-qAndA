import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter # from langchain 
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
# from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma


# take pdf documents and return a single string of text containing all the content 
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs: 
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages: 
            text += page.extract_text()
    return text 

# split text into chucks to be fed into model 
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000, # 1000 characters 
        chunk_overlap=200,
        length_function=len # len from python 
    )
    chunks = text_splitter.split_text(text)
    return chunks

# use chunks to create vector store
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()  # or HuggingFaceInstructEmbeddings
    vectorstore = Chroma.from_texts(texts=text_chunks, embedding=embeddings)
    print("✅ Vectorstore created:", vectorstore)
    return vectorstore


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

                # get the text chunks 
                text_chunks = get_text_chunks(raw_text)

                # create vector store with embeddings 
                vectorstore = get_vectorstore(text_chunks)

if __name__ == '__main__':
    main()