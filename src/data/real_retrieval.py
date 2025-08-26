#!/usr/bin/env python3
"""
Real RAG retrieval system using ChromaDB - UPDATED FOR NEW CHROMA API
"""

import chromadb
from sentence_transformers import SentenceTransformer
from src.utils.config import config
import logging

logger = logging.getLogger(__name__)

class RealRetrievalSystem:
    def __init__(self):
        self.persist_directory = config.CHROMA_PERSIST_DIR
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        try:
            # NEW Chroma client syntax
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            self.collection = self.client.get_collection("support_knowledge_base")
        except Exception as e:
            logger.warning(f"ChromaDB collection not found: {e}. Using mock fallback.")
            self.collection = None
    
    def retrieve_context(self, query: str, category: str = None, n_results: int = 5) -> list[str]:
        """Retrieve relevant context using semantic search"""
        
        # If ChromaDB isn't set up, fall back to mock data
        if self.collection is None:
            logger.warning("Using mock data fallback - ChromaDB not initialized")
            from src.data.mock_knowledge import get_enhanced_context
            return get_enhanced_context(category or "General", query, "")
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query]).tolist()[0]
            
            # Build filters - NEW syntax
            where_filter = None
            if category:
                where_filter = {"category": {"$eq": category}}
            
            # Query the database - NEW syntax
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_filter,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            context_items = []
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                context_items.append({
                    "content": doc,
                    "category": metadata.get('category', 'Unknown'),
                    "type": metadata.get('type', 'Unknown'),
                    "confidence": 1 - distance  # Convert distance to confidence
                })
            
            logger.info(f"Retrieved {len(context_items)} context items with confidence: {[round(item['confidence'], 2) for item in context_items]}")
            
            # Return just the content for now
            return [item["content"] for item in context_items]
            
        except Exception as e:
            logger.error(f"Error retrieving from ChromaDB: {e}")
            # Fall back to mock data
            from src.data.mock_knowledge import get_enhanced_context
            return get_enhanced_context(category or "General", query, "")

# Global instance
retrieval_system = RealRetrievalSystem()

def get_real_context(category: str, ticket_subject: str, ticket_description: str) -> list[str]:
    """Get real context using semantic search"""
    query = f"{ticket_subject} {ticket_description}"
    return retrieval_system.retrieve_context(query, category)