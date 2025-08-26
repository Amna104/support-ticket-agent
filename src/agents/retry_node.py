from langchain_core.messages import HumanMessage
from src.data.mock_knowledge import get_enhanced_context
from src.agents.state import State
import logging

logger = logging.getLogger(__name__)

def refine_context_for_retry(state: State) -> dict:
    """Refine context based on review feedback for retry"""
    ticket = state["ticket"]
    category = state["category"]
    review_feedback = state["review_feedback"]
    
    # FIX: Handle missing retry_count with default value
    retry_count = state.get("retry_count", 0)  # Use get() with default
    
    logger.info(f"Refining context for retry #{retry_count + 1}")
    logger.info(f"Review feedback: {review_feedback[:100]}...")
    
    # Enhance context based on review feedback
    base_context = get_enhanced_context(
        category=category,
        ticket_subject=ticket["subject"],
        ticket_description=ticket["description"]
    )
    
    # Add context based on review feedback keywords
    additional_context = []
    
    if "refund" in str(review_feedback).lower():
        additional_context.extend([
            "Refund eligibility is determined case-by-case based on our terms of service.",
            "Refunds typically take 5-7 business days to process once approved.",
            "Partial refunds may be offered for unused portions of subscriptions."
        ])
    
    if "policy" in str(review_feedback).lower() or "compliance" in str(review_feedback).lower():
        additional_context.extend([
            "Always refer customers to our terms of service for policy questions.",
            "Avoid making specific promises about outcomes or timelines.",
            "Escalate to human review when policy interpretation is unclear."
        ])
    
    if "security" in str(review_feedback).lower():
        additional_context.extend([
            "Never share specific security implementation details with customers.",
            "Refer security concerns to security@ourcompany.com for expert handling.",
            "Use general security best practices language without specifics."
        ])
    
    refined_context = base_context + additional_context
    
    logger.info(f"Refined context with {len(additional_context)} additional items")
    
    return {
        "context": refined_context,
        "retry_count": retry_count + 1,  # Increment the count
        "messages": [HumanMessage(content=f"Context refined for retry #{retry_count + 1} based on feedback")]
    }