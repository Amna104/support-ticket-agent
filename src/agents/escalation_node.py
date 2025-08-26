from langchain_core.messages import HumanMessage
from src.agents.state import State
import logging
import csv
import datetime
import os

logger = logging.getLogger(__name__)

def escalate_to_human(state: State) -> dict:
    """Escalate the ticket to human review after max retries"""
    ticket = state["ticket"]
    category = state["category"]
    draft_response = state["draft_response"]
    review_feedback = state["review_feedback"]
    retry_count = state["retry_count"]
    
    logger.warning(f"Escalating ticket to human review after {retry_count} retries")
    
    # Create escalation entry
    escalation_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "ticket_subject": ticket["subject"],
        "ticket_description": ticket["description"][:500],  # Truncate if too long
        "category": category,
        "draft_response": draft_response[:1000] if draft_response else "No draft",
        "review_feedback": review_feedback[:500] if review_feedback else "No feedback",
        "retry_count": retry_count
    }
    
    # Log to CSV file
    csv_file = "escalation_log.csv"
    file_exists = os.path.isfile(csv_file)
    
    try:
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            fieldnames = list(escalation_data.keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(escalation_data)
        
        logger.info(f"Escalation logged to {csv_file}")
        
    except Exception as e:
        logger.error(f"Failed to write escalation log: {e}")
    
    # Create human-readable message
    escalation_message = f"""
🚨 ESCALATION REQUIRED 🚨

Ticket requires human review after {retry_count} automated attempts.

Ticket: {ticket['subject']}
Category: {category}

Last Draft Preview:
{draft_response[:300] if draft_response else 'No draft generated'}...

Review Feedback:
{review_feedback[:200] if review_feedback else 'No feedback'}...

Please handle this ticket manually.
"""
    
    return {
        "messages": [HumanMessage(content=escalation_message)],
        "review_status": "escalated"
    }