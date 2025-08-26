from src.agents.workflow import create_support_workflow
from src.agents.state import State

def test_complete_workflow():
    """Test the complete support workflow"""
    
    test_cases = [
        {
            "ticket": {
                "subject": "Payment failed for monthly subscription",
                "description": "I tried to pay for my monthly subscription but my credit card was declined. The card is valid and has sufficient funds."
            }
        },
        {
            "ticket": {
                "subject": "Cannot login to my account",
                "description": "I'm getting an error when trying to login with correct credentials."
            }
        }
    ]
    
    workflow = create_support_workflow()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Subject: {test_case['ticket']['subject']}")
        print(f"Description: {test_case['ticket']['description'][:80]}...")
        
        # Create initial state
        initial_state = State(
            ticket=test_case["ticket"],
            category=None,
            context=None,
            draft_response=None,
            review_feedback=None,
            review_status=None,
            retry_count=0,
            messages=[]
        )
        
        try:
            # Run the workflow
            result = workflow.invoke(initial_state)
            
            print(f"✅ Workflow completed!")
            print(f"Final status: {result.get('review_status', 'unknown')}")
            print(f"Retry attempts: {result.get('retry_count', 0)}")
            
            if result.get('review_status') == 'approved':
                print("🎉 Response approved automatically!")
                print(f"Response length: {len(result.get('draft_response', ''))} characters")
            elif result.get('review_status') == 'escalated':
                print("⚠️  Ticket escalated to human review")
            else:
                print(f"❓ Unknown final status: {result.get('review_status')}")
                
        except Exception as e:
            print(f"❌ Workflow failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("Testing Complete Workflow...")
    test_complete_workflow()