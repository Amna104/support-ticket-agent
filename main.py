from src.utils.config import config
from src.utils.llm_utils import test_available_models, get_classification_llm

def test_llm_connection():
    """Test that we can connect to Groq API"""
    try:
        llm = get_classification_llm()
        response = llm.invoke("Hello, are you working? Reply with just 'Yes' or 'No'.")
        print("✅ LLM connection successful!")
        print(f"Response: {response.content}")
        return True
    except Exception as e:
        print(f"❌ LLM connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing project setup...")
    print(f"Using model: {config.CLASSIFICATION_MODEL}")
    print("\nTesting available models:")
    
    # Test which models work
    test_available_models()
    
    print(f"\nTesting configured model ({config.CLASSIFICATION_MODEL}):")
    if test_llm_connection():
        print("🎉 Project setup completed successfully!")
    else:
        print("⚠️  Please check your GROQ_API_KEY in .env file")