from src.utils.config import config

# Mock knowledge base for each category
MOCK_KNOWLEDGE_BASE = {
    "Billing": [
        "Payments can be made via credit card, PayPal, or bank transfer.",
        "Failed payments are usually due to expired cards or insufficient funds.",
        "Subscription billing occurs on the same date each month.",
        "Refunds are processed within 5-7 business days for eligible requests.",
        "You can update payment methods in your account settings under 'Billing'."
    ],
    "Technical": [
        "Common login issues can be resolved by clearing browser cache or resetting password.",
        "Our system requires JavaScript to be enabled for full functionality.",
        "Mobile app issues may be fixed by updating to the latest version.",
        "API documentation is available at api.ourcompany.com/docs.",
        "System maintenance occurs every Sunday from 2-4 AM UTC."
    ],
    "Security": [
        "We use AES-256 encryption for all user data.",
        "Two-factor authentication is available and recommended for all accounts.",
        "Password requirements: minimum 12 characters with uppercase, lowercase, numbers, and symbols.",
        "Suspicious activity should be reported immediately to security@ourcompany.com.",
        "Session timeout is 30 minutes of inactivity for security reasons."
    ],
    "General": [
        "Our support hours are Monday-Friday 9AM-6PM EST.",
        "For urgent issues, call our support hotline at +1-800-123-4567.",
        "You can find FAQs and tutorials in our help center at help.ourcompany.com.",
        "Enterprise customers have dedicated account managers.",
        "Feature requests can be submitted through our feedback portal."
    ]
}

def get_mock_context(category: str, query: str = "") -> list[str]:
    """Get mock context for a given category"""
    if category not in MOCK_KNOWLEDGE_BASE:
        return ["No specific context available for this category."]
    
    # Return all context for the category (in real system, this would be based on query)
    return MOCK_KNOWLEDGE_BASE[category]

def get_enhanced_context(category: str, ticket_subject: str, ticket_description: str) -> list[str]:
    """Get enhanced context based on the specific ticket content"""
    base_context = get_mock_context(category)
    
    # Add some context based on keywords in the ticket
    additional_context = []
    
    if "payment" in ticket_subject.lower() or "payment" in ticket_description.lower():
        if category == "Billing":
            additional_context.extend([
                "For payment issues, check if the card expiration date is current.",
                "International payments may require 3D Secure authentication.",
                "Payment failures are logged and can be reviewed in the billing history."
            ])
    
    if "login" in ticket_subject.lower() or "login" in ticket_description.lower():
        if category in ["Technical", "Security"]:
            additional_context.extend([
                "Login attempts are limited to 5 tries per hour for security.",
                "Password reset tokens expire after 1 hour for security reasons.",
                "Check if CAPS LOCK is accidentally enabled when entering password."
            ])
    
    if "security" in ticket_subject.lower() or "security" in ticket_description.lower():
        if category == "Security":
            additional_context.extend([
                "All login attempts are logged with IP address and timestamp.",
                "Users receive email notifications for new device logins.",
                "Account lockout occurs after 5 failed login attempts."
            ])
    
    return base_context + additional_context