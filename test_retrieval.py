from src.agents.retrieval_node import retrieve_context

def test_retrieval():
    """Test the retrieval node with different ticket types"""
    
    test_cases = [
        {
            "ticket": {
                "subject": "Payment failed for monthly subscription",
                "description": "I tried to pay for my monthly subscription but my credit card was declined."
            },
            "category": "Billing"
        },
        {
            "ticket": {
                "subject": "Cannot login to my account",
                "description": "I'm getting an error when trying to login with correct credentials."
            },
            "category": "Security"
        },
        {
            "ticket": {
                "subject": "Mobile app crashing on startup",
                "description": "The app crashes immediately when I try to open it on my iPhone."
            },
            "category": "Technical"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Category: {test_case['category']}")
        print(f"Subject: {test_case['ticket']['subject']}")
        
        # Create state for testing
        state = {
            "ticket": test_case["ticket"],
            "category": test_case["category"],
            "context": None,
            "draft_response": None,
            "review_feedback": None,
            "review_status": None,
            "retry_count": 0,
            "messages": []
        }
        
        try:
            result = retrieve_context(state)
            print(f"✅ Retrieved {len(result['context'])} context items:")
            for j, item in enumerate(result['context'][:3], 1):  # Show first 3 items
                print(f"  {j}. {item[:80]}...")
            if len(result['context']) > 3:
                print(f"  ... and {len(result['context']) - 3} more items")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing Retrieval Node...")
    test_retrieval()