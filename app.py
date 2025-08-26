#!/usr/bin/env python3
"""
Main entry point for the Support Ticket Resolution Agent.
Run with: python app.py "Ticket subject" "Ticket description"
"""

import sys
import json
from src.agents.workflow import create_support_workflow
from src.agents.state import State

def main():
    if len(sys.argv) != 3:
        print("Usage: python app.py \"Ticket subject\" \"Ticket description\"")
        print("Example: python app.py \"Login issue\" \"I can't login to my account\"")
        sys.exit(1)
    
    subject = sys.argv[1]
    description = sys.argv[2]
    
    print(f"🚀 Processing support ticket...")
    print(f"Subject: {subject}")
    print(f"Description: {description}")
    print("-" * 50)
    
    # Create ticket
    ticket = {
        "subject": subject,
        "description": description
    }
    
    # Initialize state
    initial_state = State(
        ticket=ticket,
        category=None,
        context=None,
        draft_response=None,
        review_feedback=None,
        review_status=None,
        retry_count=0,
        messages=[]
    )
    
    # Create and run workflow
    workflow = create_support_workflow()
    result = workflow.invoke(initial_state)
    
    print("\n🎯 WORKFLOW COMPLETED")
    print("=" * 50)
    
    if result.get('review_status') == 'approved':
        print("✅ STATUS: Approved")
        print(f"📝 Response length: {len(result.get('draft_response', ''))} characters")
        print("\n📋 FINAL RESPONSE:")
        print("-" * 30)
        print(result.get('draft_response', 'No response generated'))
    elif result.get('review_status') == 'escalated':
        print("⚠️  STATUS: Escalated to human review")
        print(f"🔁 Retry attempts: {result.get('retry_count', 0)}")
        print("\n💬 Escalation reason:")
        print(result.get('review_feedback', 'No feedback provided'))
    else:
        print(f"❓ STATUS: {result.get('review_status', 'unknown')}")
    
    print("\n📊 STATS:")
    print(f"• Category: {result.get('category', 'Unknown')}")
    print(f"• Retry attempts: {result.get('retry_count', 0)}")
    print(f"• Context items used: {len(result.get('context', []))}")

if __name__ == "__main__":
    main()