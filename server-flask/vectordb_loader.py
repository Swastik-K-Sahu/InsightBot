import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)

CHROMA_PATH = "chroma"
DATA_PATH = "data"


def vectordb_loading():

    documents = load_pdfs()
    chunks = split_documents(documents)
    # print("Chunks Created")
    try:
        add_to_vectordb(chunks)
        return "VectorDB Created"
    except Exception as e:
        return f"Error loading Chroma vectorstore: {str(e)}"

def load_pdfs():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def add_to_vectordb(chunks: list[Document]):

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=embeddings
    )
    db.add_documents(chunks)
    


