from typing import TypedDict, List, Optional, Literal
from langgraph.graph import add_messages

class Ticket(TypedDict):
    subject: str
    description: str

class State(TypedDict):
    ticket: Ticket
    category: Optional[str]
    context: Optional[List[str]]
    draft_response: Optional[str]
    review_feedback: Optional[str]
    review_status: Optional[Literal["approved", "rejected"]]
    retry_count: int
    messages: add_messages