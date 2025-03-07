from langchain.document_loaders import WebBaseLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# import bs4
from langchain_community.vectorstores import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import warnings
import os

load_dotenv()

warnings.filterwarnings('ignore')

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


web_based_loader = WebBaseLoader("https://github.com/Debajyoti2004?tab=repositories")
web_docs = web_based_loader.load()

resume_folder = r"C:\Users\manab\OneDrive\Desktop\Resume_Builder\App\Resume_templates"
resume_docs = []
for file in os.listdir(resume_folder):
    if file.endswith(".txt"):
        loader = TextLoader(os.path.join(resume_folder, file))
        resume_docs.extend(loader.load())

all_docs = web_docs+resume_docs


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=512, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(all_docs)

vectorstore = FAISS.from_documents(
    documents=doc_splits,
    embedding=embeddings
)
print("vector store created successfully")
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

