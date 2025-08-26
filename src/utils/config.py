import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MAX_RETRIES = 2
    CATEGORIES = ["Billing", "Technical", "Security", "General"]
    
    # Updated model configurations - using current Groq models
    CLASSIFICATION_MODEL = "llama-3.1-8b-instant"
    DRAFT_MODEL = "llama-3.1-8b-instant"
    REVIEW_MODEL = "llama-3.1-8b-instant"
    
    
    # RAG settings
    CHROMA_PERSIST_DIR = "./chroma_db"
    
config = Config()