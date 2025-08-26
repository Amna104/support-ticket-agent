from src.agents.classification_node import classify_ticket
from src.agents.state import State

def test_classification():
    """Test the classification node with different ticket types"""
    
    test_cases = [
        {
            "subject": "Payment failed for monthly subscription",
            "description": "I tried to pay for my monthly subscription but my credit card was declined. I need help resolving this."
        },
        {
            "subject": "Cannot login to my account",
            "description": "I'm getting an error when trying to login. It says 'invalid credentials' but I'm sure my password is correct."
        },
        {
            "subject": "Security concern about data privacy",
            "description": "I noticed some suspicious activity on my account and want to make sure my data is secure."
        },
        {
            "subject": "General inquiry about features",
            "description": "I wanted to know if you have any upcoming features planned for the mobile app."
        }
    ]
    
    for i, ticket_data in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Subject: {ticket_data['subject']}")
        print(f"Description: {ticket_data['description'][:100]}...")
        
        # Create a minimal state for testing
        state = {
            "ticket": ticket_data,
            "category": None,
            "context": None,
            "draft_response": None,
            "review_feedback": None,
            "review_status": None,
            "retry_count": 0,
            "messages": []
        }
        
        try:
            result = classify_ticket(state)
            print(f"✅ Classification: {result['category']}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing Classification Node...")
    test_classification()