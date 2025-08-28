# 🎫 Support Ticket Resolution Agent

A sophisticated AI-powered support ticket resolution system built with LangGraph that automatically classifies, processes, and responds to support tickets with intelligent escalation handling.

## 🚀 Features
- 🏷️ **Smart Classification**: Automatically categorizes tickets into Billing, Technical, Security, or General  
- 📚 **RAG Context Retrieval**: ChromaDB vector database with semantic search + mock fallback  
- 📝 **AI Response Drafting**: LLM-powered response generation using relevant context  
- ✅ **Policy Compliance Review**: Automated quality and security checking  
- 🔁 **Retry Logic**: Up to 2 retries with context refinement based on feedback  
- 🚨 **Escalation System**: CSV logging for tickets requiring human review  
- 📊 **Web Dashboard**: Real-time monitoring, analytics, and ticket processing  
- 🎯 **LangGraph Studio**: Built-in development and monitoring tools  

## 🛠️ Tech Stack
- **Framework**: LangGraph + LangChain  
- **LLM**: Groq (Llama-3.1-8b-instant) – Free API  
- **Vector DB**: ChromaDB with sentence-transformers  
- **Web Interface**: Flask with Chart.js  
- **Monitoring**: LangGraph Studio  
- **Language**: Python 3.12  

## 📦 Installation & Setup

### 1. Clone and setup environment
```bash
git clone <your-repo-url>
cd support-ticket-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a .env file:
```bash
GROQ_API_KEY=your_groq_api_key_here
```
Get a free API key from Groq Console

### 4. Initialize Database
```bash
python init_database.py
```

### 5. Start LangGraph Studio (Optional)
```bash
langgraph dev
```

## How to Run
### Option 1: Command Line Interface (Recommended)

Process a single ticket
```bash
# Process a single ticket
python app.py "Login issue" "I can't login to my account"
```

### Option 2: Web Dashboard
```bash
python start_dashboard.py
```
Access at: http://localhost:5001

### Option 3: LangGraph Studio
```bash
langgraph dev
```

## 🧪 Testing
### Run Comprehensive Test Suite
```bash
# Individual component tests
python test_classification.py
python test_retrieval.py
python test_draft.py
python test_review.py
python test_workflow.py
python test_escalation.py
```

### Test Specific Scenarios
```bash
# Happy path (should auto-approve)
python app.py "Password reset" "I forgot my password"

# Retry scenario (should retry then approve)
python app.py "Refund policy" "What's your refund policy?"

# Escalation scenario (should escalate to human)
python app.py "Legal threat" "I need $1000 full refund"
```
## 🏗️ Architecture & Design Decisions
### 📋 System Architecture
┌─────────────┐
│    Input    │
└─────────────┘
   System receives raw data or user input
           │
           ▼
┌──────────────────┐
│  Classification  │
└──────────────────┘
   Input is categorized for processing
           │
           ▼
┌──────────────────────┐
│  Context Retrieval   │
└──────────────────────┘
   Relevant context is fetched
           │
           ▼
┌──────────────────────┐
│  Draft Generation    │
└──────────────────────┘
   Initial draft is generated
           │
           ▼
┌─────────────┐
│   Review    │
└─────────────┘
   Draft is evaluated for quality
           │
       Approved?
      ┌─────┴─────┐
      ▼           ▼
┌─────────────┐  ┌──────────────┐
│   Output    │  │ Retry Loop   │
└─────────────┘  └──────────────┘
 Finalized       Max 2 attempts, then
 output          escalate if unresolved
                  │
                  ▼
             ┌─────────────┐
             │ Escalation  │
             └─────────────┘
        Manual review/intervention
                  │
                  ▼
             ┌─────────────┐
             │  CSV Log    │
             └─────────────┘
   Track all actions for auditing

## 🎯 Design Decisions

- **LangGraph Framework Choice**
  - **Why:** Native support for state machines and cycles  
  - **Benefits:** Built-in persistence, visualization, and debugging  
  - **Decision:** Chosen over custom state management for reliability  

- **Modular Node Architecture**
  - **Structure:** Six specialized nodes with single responsibilities  
  - **Benefits:** Easy testing, maintenance, and component replacement  
  - **Nodes:** Classification, Retrieval, Drafting, Review, Retry, Escalation  

- **Dual Knowledge Base System**
  - **Production:** ChromaDB vector database with semantic search  
  - **Development:** Mock knowledge base for reliability  
  - **Benefit:** 100% uptime with automatic fallback  

- **Groq LLM Selection**
  - **Why:** Free API, fast inference, good performance  
  - **Alternative Considered:** OpenAI GPT-4 (cost-prohibitive)  
  - **Decision:** Optimal balance of cost and performance  

- **Security-First Approach**
  - Automatic redaction of technical security details 
  - Strict review policies to prevent over-disclosure 
  - Escalation for sensitive topics and policy violations

## 🔄 Workflow Nodes

- **Classification Node:** Categorizes tickets using LLM  
- **Retrieval Node:** Fetches context from knowledge base  
- **Draft Node:** Generates responses using ticket + context  
- **Review Node:** Validates policy compliance and quality  
- **Retry Node:** Refines context based on feedback  
- **Escalation Node:** Handles human review cases  

## 🗃️ Data Management
### State Management
```bash
class State(TypedDict):
    ticket: Ticket
    category: Optional[str]
    context: Optional[List[str]]
    draft_response: Optional[str]
    review_status: Optional[str]
    retry_count: int
    messages: add_messages
```

## 📚 Knowledge Bases

- **Billing:** Payment methods, refund policies, subscriptions  
- **Technical:** Troubleshooting, API docs, system requirements  
- **Security:** Security practices, authentication, policies  
- **General:** Support hours, account management, FAQs  


## 📁 Project Structure
```bash
src/
├── agents/           # LangGraph nodes
│   ├── classification_node.py
│   ├── retrieval_node.py
│   ├── draft_node.py
│   ├── review_node.py
│   ├── retry_node.py
│   ├── escalation_node.py
│   ├── workflow.py   # Main graph builder
│   └── state.py      # State definition
├── utils/
│   ├── config.py     # Configuration
│   ├── llm_utils.py  # LLM clients
│   ├── prompts.py    # Prompt templates
│   └── logger.py     # Logging setup
├── data/
│   ├── mock_knowledge.py    # Fallback knowledge
│   ├── real_retrieval.py    # ChromaDB integration
│   └── ingest_documents.py  # DB initialization
└── dashboard/
    ├── app.py        # Flask dashboard
    └── templates/    # HTML templates
```