

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.kb import load_knowledge
from app.retriever import KnowledgeRetriever
from app.llm import generate_answer
from app.schemas import QueryRequest
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Company KB Chatbot")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load knowledge & retriever
knowledge = load_knowledge()
retriever = KnowledgeRetriever(knowledge)

@app.get("/")
def home():
    return "Welcome to KB Chatbot"

@app.post("/ask")
def ask(payload: QueryRequest):
    query = payload.question
    docs = retriever.retrieve(query, top_k=2)
    
    logging.info(f"Query: {query}")
    logging.info(f"Docs retrieved: {[d['title'] for d in docs]}")

    if not docs:
        return {"answer": "Main maafi chahta hoon, mujhe is baare mein jaankari nahi mili."}

    context = "\n".join(d["content"] for d in docs)
    answer = generate_answer(query, context)
    return {"answer": answer}
