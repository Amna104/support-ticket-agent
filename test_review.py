from src.agents.review_node import review_draft_response
from src.agents.draft_node import generate_draft_response
from src.data.mock_knowledge import get_enhanced_context

def test_review():
    """Test the review node with different draft responses"""
    
    test_cases = [
        {
            "ticket": {
                "subject": "Payment failed for monthly subscription",
                "description": "I tried to pay for my monthly subscription but my credit card was declined. The card is valid and has sufficient funds."
            },
            "category": "Billing"
        },
        {
            "ticket": {
                "subject": "I need a full refund immediately",
                "description": "Your service is terrible and I want all my money back right now. Give me a full refund of $299.99 immediately."
            },
            "category": "Billing"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Category: {test_case['category']}")
        print(f"Subject: {test_case['ticket']['subject']}")
        print(f"Description: {test_case['ticket']['description'][:80]}...")
        
        # Get context and generate draft first
        context = get_enhanced_context(
            category=test_case["category"],
            ticket_subject=test_case["ticket"]["subject"],
            ticket_description=test_case["ticket"]["description"]
        )
        
        # Create state for draft generation
        draft_state = {
            "ticket": test_case["ticket"],
            "category": test_case["category"],
            "context": context,
            "draft_response": None,
            "review_feedback": None,
            "review_status": None,
            "retry_count": 0,
            "messages": []
        }
        
        # Generate draft
        draft_result = generate_draft_response(draft_state)
        draft_response = draft_result["draft_response"]
        
        print(f"Generated draft ({len(draft_response)} characters)")
        
        # Create state for review
        review_state = {
            "ticket": test_case["ticket"],
            "category": test_case["category"],
            "context": context,
            "draft_response": draft_response,
            "review_feedback": None,
            "review_status": None,
            "retry_count": 0,
            "messages": []
        }
        
        try:
            result = review_draft_response(review_state)
            print(f"✅ Review verdict: {result['review_status'].upper()}")
            print(f"Feedback: {result['review_feedback'][:200]}...")
            
            if result['review_status'] == 'rejected':
                print("❌ Draft needs improvement")
            else:
                print("🎉 Draft approved!")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing Review Node...")
    test_review()