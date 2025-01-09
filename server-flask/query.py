import os
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = ("""
Answer the question based only on the following context:

{context}

---

You are an intelligent assistant designed to answer questions using either retrieved context from enterprise knowledge bases 
or an external LLM when context is insufficient. When you receive a question, carefully examine the provided context first. 
If context is available, use it to provide an accurate response. If not, answer based on general knowledge using the LLM.

---

Now, answer the following question based on the above context: {question}
""")


def chatbot_response(query_text: str):

    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search_with_score(query_text, k=5)
    # print("DB Searched")
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0, max_tokens=150)
    response = model.invoke(prompt)
    
    return response.content

