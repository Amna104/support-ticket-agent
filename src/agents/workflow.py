from langgraph.graph import StateGraph, END
from src.dashboard.app import dashboard_data
from src.agents.classification_node import classify_ticket
from src.agents.retrieval_node import retrieve_context
from src.agents.draft_node import generate_draft_response
from src.agents.review_node import review_draft_response
from src.agents.retry_node import refine_context_for_retry
from src.agents.escalation_node import escalate_to_human  # Add this import
from src.agents.state import State
from src.utils.config import config
import logging

logger = logging.getLogger(__name__)

def should_retry(state: State) -> str:
    """Determine whether to retry or end based on review status and retry count"""
    review_status = state.get("review_status")
    retry_count = state.get("retry_count", 0)
    
    if review_status == "approved":
        logger.info("Draft approved! Proceeding to end.")
        return "end"
    elif retry_count >= config.MAX_RETRIES:
        logger.warning(f"Max retries reached ({retry_count}). Proceeding to escalation.")
        return "escalate"
    else:
        logger.info(f"Retry needed. Attempt {retry_count + 1} of {config.MAX_RETRIES}")
        return "retry"

def create_support_workflow() -> StateGraph:
    """Create the main support ticket resolution workflow"""
    
    # Initialize the graph
    workflow = StateGraph(State)
    
    # Add nodes (including escalation node)
    workflow.add_node("classify_ticket", classify_ticket)
    workflow.add_node("retrieve_context", retrieve_context)
    workflow.add_node("generate_draft", generate_draft_response)
    workflow.add_node("review_draft", review_draft_response)
    workflow.add_node("refine_context", refine_context_for_retry)
    workflow.add_node("escalate", escalate_to_human)  # Add escalation node
    
    # Set entry point
    workflow.set_entry_point("classify_ticket")
    
    # Add edges
    workflow.add_edge("classify_ticket", "retrieve_context")
    workflow.add_edge("retrieve_context", "generate_draft")
    workflow.add_edge("generate_draft", "review_draft")
    
    # Add conditional edges for retry logic
    workflow.add_conditional_edges(
        "review_draft",
        should_retry,
        {
            "end": END,
            "escalate": "escalate",  # Now points to escalate node
            "retry": "refine_context"
        }
    )
    
    # Add edge from refine_context back to generate_draft
    workflow.add_edge("refine_context", "generate_draft")
    
    # Add edge from escalate to end
    workflow.add_edge("escalate", END)
    
    # Compile the graph
    compiled_workflow = workflow.compile()
    
    logger.info("Support workflow compiled successfully!")
    return compiled_workflow