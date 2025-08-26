from langchain_groq import ChatGroq
from src.utils.config import config
import logging

logger = logging.getLogger(__name__)

def get_llm(model_name: str, temperature: float = 0.1):
    """Get a configured Groq LLM instance"""
    try:
        return ChatGroq(
            model_name=model_name,
            temperature=temperature,
            groq_api_key=config.GROQ_API_KEY,
            max_retries=3,
            timeout=30
        )
    except Exception as e:
        logger.error(f"Failed to create LLM instance: {e}")
        raise

def get_classification_llm():
    return get_llm(config.CLASSIFICATION_MODEL, temperature=0.1)

def get_draft_llm():
    return get_llm(config.DRAFT_MODEL, temperature=0.3)

def get_review_llm():
    return get_llm(config.REVIEW_MODEL, temperature=0.2)

# Test function to check available models
def test_available_models():
    """Test which models are available"""
    test_models = [
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768"  # This might fail but let's test
    ]
    
    for model in test_models:
        try:
            llm = get_llm(model, temperature=0.1)
            response = llm.invoke("Say hello in one word")
            print(f"✅ {model}: Working - {response.content}")
        except Exception as e:
            print(f"❌ {model}: Failed - {str(e)[:100]}...")