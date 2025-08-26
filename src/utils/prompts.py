from langchain_core.prompts import ChatPromptTemplate

# Classification prompt
CLASSIFICATION_PROMPT = ChatPromptTemplate.from_template("""
You are a support ticket classification system. Your task is to categorize the following support ticket into one of these categories: {categories}.

Ticket Subject: {subject}
Ticket Description: {description}

Analyze the ticket and determine the most appropriate category. Consider:
- Billing: Issues related to payments, invoices, subscriptions, refunds
- Technical: Software bugs, technical issues, feature requests, system errors
- Security: Account security, privacy concerns, data protection, authentication issues
- General: General inquiries, feedback, non-urgent questions, account management

Return ONLY the category name from the list above. Do not include any other text or explanation.

Category:
""")

# Draft generation prompt
DRAFT_PROMPT = ChatPromptTemplate.from_template("""
You are a customer support agent. Based on the following support ticket and relevant context, draft a helpful and professional response.

**Support Ticket:**
Subject: {subject}
Description: {description}

**Relevant Context:**
{context}

**Instructions:**
- Address the customer's issue directly and empathetically
- Use the provided context to ensure accuracy
- Provide clear, actionable steps if applicable
- Be professional but friendly in tone
- Keep the response concise but comprehensive
- Do not make promises you can't keep (like specific refund amounts)
- Do not provide sensitive security information

Draft your response below:
""")

# Review prompt
# REVIEW_PROMPT = ChatPromptTemplate.from_template("""
# You are a quality assurance reviewer for customer support responses. Your task is to review the following draft response and determine if it meets our support policies.

# **Support Ticket:**
# Subject: {subject}
# Description: {description}

# **Category:** {category}

# **Draft Response:**
# {draft_response}

# **Review Criteria:**
# 1. ✅ ACCURACY: Response must be factually correct based on available context
# 2. ✅ HELPFULNESS: Response should address the customer's issue directly
# 3. ✅ POLICY COMPLIANCE: Response must not:
#    - Promise specific refund amounts or guarantees
#    - Provide sensitive security information
#    - Make commitments we can't keep
#    - Contain harmful or inappropriate content
# 4. ✅ TONE: Professional, empathetic, and customer-friendly
# 5. ✅ ACTIONABILITY: Provides clear next steps if applicable

# **Instructions:**
# Review the draft response and provide:
# 1. Your verdict: "approved" or "rejected"
# 2. If rejected, specific feedback on what needs improvement
# 3. Keep feedback concise and actionable

# **Output Format:**
# VERDICT: approved|rejected
# FEEDBACK: [your feedback here]

# Begin your review:
# """)

# Review prompt - STRICTER VERSION
REVIEW_PROMPT = ChatPromptTemplate.from_template("""
You are a STRICT quality assurance reviewer for customer support responses. Your task is to review the following draft response and determine if it meets our support policies.

**Support Ticket:**
Subject: {subject}
Description: {description}

**Category:** {category}

**Draft Response:**
{draft_response}

**STRICT Review Criteria - MUST REJECT IF ANY OF THESE ARE VIOLATED:**
1. 🚫 **NO REFUND PROMISES**: Must NOT promise specific refund amounts or guarantee refunds.
2. 🚫 **NO FINANCIAL COMMITMENTS**: Must NOT make any financial commitments or promises.
3. 🚫 **NO SECURITY DETAILS**: Must NOT provide specific security implementation details (e.g. encryption types, algorithms, configurations).
4. 🚫 **NO OVERPROMISING**: Must NOT overpromise outcomes or timelines.
5. ✅ **ACCURACY**: Must be factually correct based on available context.
6. ✅ **HELPFULNESS**: Must directly address the customer's issue.
7. ✅ **PROFESSIONAL TONE**: Must remain professional, empathetic, and customer-friendly.

**SPECIFIC POLICY VIOLATIONS TO LOOK FOR:**
- Phrases like "I will refund", "you will receive", "we guarantee"
- Specific dollar amounts or percentages
- Promises about specific outcomes or timelines
- Overly optimistic or definite language

**Instructions:**
Return ONLY in this exact format:
VERDICT: approved|rejected
FEEDBACK: [your specific feedback here]

Do not include any other text.

Begin your STRICT review:
""")


# Helper functions
def get_classification_prompt():
    return CLASSIFICATION_PROMPT

def get_draft_prompt():
    return DRAFT_PROMPT

def get_review_prompt():
    return REVIEW_PROMPT