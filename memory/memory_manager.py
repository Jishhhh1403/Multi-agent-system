from typing import List, Optional
from pathlib import Path
from memory.document_memory import DocumentMemory
from memory.conversation_memory import ConversationMemory

class MemoryManager:
    """Unified interface for all memory operations."""
    
    def __init__(self):
        self.document_memory = DocumentMemory()
        self.conversation_memory = ConversationMemory()
    
    # Document Memory operations
    def ingest_codebase(self, path: Path) -> int:
        """Ingest a codebase into document memory."""
        if path.is_file():
            content = path.read_text(encoding="utf-8")
            self.document_memory.ingest_file(path, content)
            return 1
        elif path.is_dir():
            return self.document_memory.ingest_directory(path)
        return 0
    
    def retrieve_relevant_code(self, query: str, k: int = 5) -> List[dict]:
        """Retrieve relevant code for a query."""
        return self.document_memory.retrieve(query, k)
    
    # Conversation Memory operations
    def add_user_message(self, content: str) -> None:
        """Add a user message to conversation history."""
        self.conversation_memory.add_message("user", content)
    
    def add_assistant_message(self, content: str, metadata: dict = None) -> None:
        """Add an assistant message to conversation history."""
        self.conversation_memory.add_message("assistant", content, metadata)
    
    def get_conversation_context(self) -> str:
        """Get recent conversation as context."""
        return self.conversation_memory.get_context()
    
    def clear_all(self) -> None:
        """Clear all memory stores."""
        self.document_memory.clear()
        self.conversation_memory.clear()