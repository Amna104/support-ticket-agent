from src.agents.draft_node import generate_draft_response
from src.data.mock_knowledge import get_enhanced_context

def test_draft_generation():
    """Test the draft generation node with different ticket types"""
    
    test_cases = [
        {
            "ticket": {
                "subject": "Payment failed for monthly subscription",
                "description": "I tried to pay for my monthly subscription but my credit card was declined. The card is valid and has sufficient funds. What should I do?"
            },
            "category": "Billing"
        },
        {
            "ticket": {
                "subject": "Cannot login to my account",
                "description": "I'm getting an 'invalid credentials' error when trying to login. I'm sure my password is correct as I just reset it yesterday."
            },
            "category": "Security"
        },
        {
            "ticket": {
                "subject": "Mobile app crashing on startup",
                "description": "The app crashes immediately when I try to open it on my iPhone 13 running iOS 16. This started happening after the last update."
            },
            "category": "Technical"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Category: {test_case['category']}")
        print(f"Subject: {test_case['ticket']['subject']}")
        print(f"Description: {test_case['ticket']['description'][:80]}...")
        
        # Get context first
        context = get_enhanced_context(
            category=test_case["category"],
            ticket_subject=test_case["ticket"]["subject"],
            ticket_description=test_case["ticket"]["description"]
        )
        
        # Create state for testing
        state = {
            "ticket": test_case["ticket"],
            "category": test_case["category"],
            "context": context,
            "draft_response": None,
            "review_feedback": None,
            "review_status": None,
            "retry_count": 0,
            "messages": []
        }
        
        try:
            result = generate_draft_response(state)
            print(f"✅ Draft generated ({len(result['draft_response'])} characters):")
            print("-" * 50)
            print(result['draft_response'])
            print("-" * 50)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing Draft Generation Node...")
    test_draft_generation()