from langchain_core.messages import HumanMessage
from src.dashboard.app import dashboard_data
from src.data.real_retrieval import get_real_context  # Change this import
from src.agents.state import State
import logging

logger = logging.getLogger(__name__)

def retrieve_context(state: State) -> dict:
    """Retrieve relevant context based on the ticket category"""
    ticket = state["ticket"]
    category = state["category"]
    
    logger.info(f"Retrieving context for category: {category}")
    logger.info(f"Ticket subject: {ticket['subject']}")
    
    # Get context from REAL knowledge base (not mock)
    context = get_real_context(  # Changed function call
        category=category,
        ticket_subject=ticket["subject"],
        ticket_description=ticket["description"]
    )
    
    logger.info(f"Retrieved {len(context)} context items")
    
    # Format context for display
    formatted_context = "\n".join([f"• {item}" for item in context])
    
    return {
        "context": context,
        "messages": [HumanMessage(content=f"Retrieved context:\n{formatted_context}")]
    }
def retrieve_context_with_logging(state: State) -> dict:
    """Retrieve context and log to dashboard"""
    result = retrieve_context(state)
    
    # Log to dashboard (we'll log after full processing)
    return result