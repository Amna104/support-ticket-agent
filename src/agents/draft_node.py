from langchain_core.messages import HumanMessage
from src.utils.llm_utils import get_draft_llm
from src.utils.prompts import get_draft_prompt
from src.agents.state import State
import logging

logger = logging.getLogger(__name__)

def generate_draft_response(state: State) -> dict:
    """Generate a draft response using the ticket and context"""
    ticket = state["ticket"]
    context = state["context"]
    
    logger.info(f"Generating draft response for: {ticket['subject']}")
    logger.info(f"Using {len(context)} context items")
    
    # Format context for the prompt
    formatted_context = "\n".join([f"• {item}" for item in context])
    
    # Prepare the prompt
    prompt = get_draft_prompt()
    messages = prompt.format_messages(
        subject=ticket["subject"],
        description=ticket["description"],
        context=formatted_context
    )
    
    # Get LLM response
    llm = get_draft_llm()
    response = llm.invoke(messages)
    
    draft_response = response.content.strip()
    
    logger.info(f"Draft response generated ({len(draft_response)} characters)")
    logger.debug(f"Draft preview: {draft_response[:100]}...")
    
    return {
        "draft_response": draft_response,
        "messages": [HumanMessage(content=f"Draft response generated:\n{draft_response}")]
    }