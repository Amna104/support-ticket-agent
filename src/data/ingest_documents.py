#!/usr/bin/env python3
"""
Ingest real documents into ChromaDB for RAG retrieval - UPDATED FOR NEW CHROMA API
"""

import chromadb
from sentence_transformers import SentenceTransformer
import os
import json

class DocumentIngestor:
    def __init__(self):
        self.persist_directory = "./chroma_db"
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # NEW Chroma client syntax
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
    def create_sample_documents(self):
        """Create sample support documents for each category"""
        documents = [
            # Billing documents
            {
                "id": "billing_001",
                "content": "Payments can be made via credit card, PayPal, or bank transfer. All major credit cards are accepted including Visa, MasterCard, and American Express.",
                "category": "Billing",
                "type": "payment_methods"
            },
            {
                "id": "billing_002", 
                "content": "Failed payments are usually due to expired cards, insufficient funds, or incorrect billing information. Check your card expiration date and ensure sufficient funds are available.",
                "category": "Billing",
                "type": "payment_issues"
            },
            {
                "id": "billing_003",
                "content": "Subscription billing occurs on the same date each month. You can view your billing cycle and next charge date in the account settings under Billing Information.",
                "category": "Billing", 
                "type": "subscription"
            },
            
            # Technical documents
            {
                "id": "technical_001",
                "content": "Common login issues can be resolved by clearing browser cache, resetting password, or ensuring JavaScript is enabled. Try using incognito mode to isolate browser issues.",
                "category": "Technical",
                "type": "login_issues"
            },
            {
                "id": "technical_002",
                "content": "Mobile app issues may be fixed by updating to the latest version from the App Store or Google Play. Ensure your operating system is up to date for compatibility.",
                "category": "Technical",
                "type": "mobile_app"
            },
            
            # Security documents
            {
    "id": "security_001",
    "content": "We use industry-standard encryption for all user data and recommend enabling two-factor authentication for additional security. Never share passwords or authentication codes with anyone.",
    "category": "Security",
    "type": "security_practices"
},
            {
                "id": "security_002",
                "content": "Password requirements: minimum 12 characters with uppercase, lowercase, numbers, and symbols. Avoid using easily guessable passwords or personal information.",
                "category": "Security",
                "type": "password_policy"
            },
            
            # General documents
            {
                "id": "general_001",
                "content": "Our support hours are Monday-Friday 9AM-6PM EST. For urgent issues outside these hours, please call our emergency support line at +1-800-123-HELP.",
                "category": "General",
                "type": "support_hours"
            }
        ]
        return documents
    
    def ingest_documents(self):
        """Ingest documents into ChromaDB"""
        try:
            # Create or get collection - NEW syntax
            collection = self.client.get_or_create_collection(
                name="support_knowledge_base",
                metadata={"hnsw:space": "cosine"}
            )
            
            # Get sample documents
            documents = self.create_sample_documents()
            
            # Prepare data for ingestion
            ids = [doc["id"] for doc in documents]
            contents = [doc["content"] for doc in documents]
            metadatas = [{
                "category": doc["category"],
                "type": doc["type"],
                "source": "internal_knowledge_base"
            } for doc in documents]
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(contents).tolist()
            
            # Add to collection - NEW syntax
            collection.upsert(
                documents=contents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✅ Successfully ingested {len(documents)} documents into ChromaDB")
            print(f"📊 Categories: {set(doc['category'] for doc in documents)}")
            
            return collection
            
        except Exception as e:
            print(f"❌ Error ingesting documents: {e}")
            # If collection exists, get it
            try:
                return self.client.get_collection("support_knowledge_base")
            except:
                raise e

if __name__ == "__main__":
    print("📥 Ingesting documents into ChromaDB...")
    ingestor = DocumentIngestor()
    collection = ingestor.ingest_documents()
    print("🎉 Document ingestion completed!")