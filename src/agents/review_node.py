from langchain_core.messages import HumanMessage
from src.utils.llm_utils import get_review_llm
from src.utils.prompts import get_review_prompt
from src.agents.state import State
import logging
import re

logger = logging.getLogger(__name__)

def review_draft_response(state: State) -> dict:
    """Review the draft response for policy compliance and quality"""
    ticket = state["ticket"]
    category = state["category"]
    draft_response = state["draft_response"]
    
    logger.info(f"Reviewing draft response for: {ticket['subject']}")
    logger.info(f"Draft length: {len(draft_response)} characters")
    
    # Prepare the prompt
    prompt = get_review_prompt()
    messages = prompt.format_messages(
        subject=ticket["subject"],
        description=ticket["description"],
        category=category,
        draft_response=draft_response
    )
    
    # Get LLM response
    llm = get_review_llm()
    response = llm.invoke(messages)
    
    review_output = response.content.strip()
    
    # Parse the review output
    verdict_match = re.search(r"VERDICT:\s*(\w+)", review_output, re.IGNORECASE)
    feedback_match = re.search(r"FEEDBACK:\s*(.+)", review_output, re.DOTALL | re.IGNORECASE)
    
    verdict = verdict_match.group(1).lower() if verdict_match else "rejected"
    feedback = feedback_match.group(1).strip() if feedback_match else "No specific feedback provided"
    
    # Validate verdict
    if verdict not in ["approved", "rejected"]:
        logger.warning(f"Invalid verdict: {verdict}. Defaulting to 'rejected'")
        verdict = "rejected"
        feedback = "Invalid review output format. Please check the review criteria."
    
    logger.info(f"Review verdict: {verdict.upper()}")
    if verdict == "rejected":
        logger.info(f"Feedback: {feedback[:100]}...")
    
    return {
        "review_status": verdict,
        "review_feedback": feedback,
        "messages": [HumanMessage(content=f"Review completed: {verdict.upper()}\nFeedback: {feedback}")]
    }

def filter_security_details(response: str) -> str:
    """Remove specific security technical details from responses"""
    security_redactions = {
        "AES-256 encryption": "industry-standard encryption",
        "encryption keys": "security protocols", 
        "database schema": "system architecture",
        "API endpoints": "system interfaces",
        "SSL/TLS": "secure connections",
        "RSA encryption": "asymmetric encryption",
        "SHA-256": "cryptographic hashing"
    }
    
    filtered_response = response
    for technical_term, general_term in security_redactions.items():
        filtered_response = filtered_response.replace(technical_term, general_term)
    
    return filtered_response