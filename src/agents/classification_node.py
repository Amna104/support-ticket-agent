from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from src.utils.llm_utils import get_classification_llm
from src.utils.prompts import get_classification_prompt
from src.utils.config import config
from src.utils.logger import setup_logging
from src.agents.state import State
import logging

logger = logging.getLogger(__name__)

def classify_ticket(state: State) -> dict:
    """Classify the support ticket into a category"""
    ticket = state["ticket"]
    
    logger.info(f"Classifying ticket: {ticket['subject']}")
    
    # Prepare the prompt
    prompt = get_classification_prompt()
    messages = prompt.format_messages(
        categories=", ".join(config.CATEGORIES),
        subject=ticket["subject"],
        description=ticket["description"]
    )
    
    # Get LLM response
    llm = get_classification_llm()
    response = llm.invoke(messages)
    
    # Extract and clean the category
    category = response.content.strip()
    
    # Validate category
    if category not in config.CATEGORIES:
        logger.warning(f"LLM returned invalid category: {category}. Defaulting to 'General'")
        category = "General"
    
    logger.info(f"Ticket classified as: {category}")
    
    return {
        "category": category,
        "messages": [HumanMessage(content=f"Ticket classified as: {category}")]
    }