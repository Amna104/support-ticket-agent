#!/usr/bin/env python3
"""
Initialize the ChromaDB database with sample documents
"""

from src.data.ingest_documents import DocumentIngestor

if __name__ == "__main__":
    print("🔄 Initializing ChromaDB database...")
    ingestor = DocumentIngestor()
    collection = ingestor.ingest_documents()
    print("✅ Database initialization complete!")
    print("\n📋 You can now use real RAG retrieval instead of mock data.")
    print("   The system will automatically fall back to mock data if ChromaDB is unavailable.")