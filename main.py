from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

from langchain.chains import RetrievalQA

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

doc = []
loaders = TextLoader("data.txt")
Loaders = PyPDFLoader("data.pdf")
Loaders_docx = Docx2txtLoader("data.docx")


doc.extend(loaders.load())
doc.extend(Loaders.load())
doc.extend(Loaders_docx.load())


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(doc)

chunks = [doc.page_content for doc in chunks]


embeddings = VertexAIEmbeddings(model_name="text-embedding-005")
vectorstore = Chroma.from_texts(chunks, embeddings)

qa = RetrievalQA.from_chain_type(llm=ChatVertexAI(model_name="gemini-2.0-flash-001"), chain_type="stuff", retriever=vectorstore.as_retriever())

query = "What This Package Provides"
result = qa.invoke(query)

print()
print(result["result"])