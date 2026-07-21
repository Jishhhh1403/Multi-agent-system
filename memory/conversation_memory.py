from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from config.settings import settings

class Message(BaseModel):
    """Single message in conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[dict] = None

class ConversationMemory:
    """Manages conversation history with sliding window."""
    
    def __init__(self, max_messages: int = None):
        self.max_messages = max_messages or settings.conversation_buffer_size
        self.messages: List[Message] = []
        self.summary: Optional[str] = None
    
    def add_message(self, role: str, content: str, metadata: dict = None) -> None:
        """Add a message to history."""
        message = Message(role=role, content=content, metadata=metadata)
        self.messages.append(message)
        
        # If too many messages, compress older ones into summary
        if len(self.messages) > self.max_messages:
            self._compress_old_messages()
    
    def get_context(self, n_messages: int = None) -> str:
        """Get recent messages as context string."""
        if n_messages is None:
            n_messages = min(10, len(self.messages))
        
        recent = self.messages[-n_messages:]
        
        context_parts = []
        if self.summary:
            context_parts.append(f"Previous context summary: {self.summary}")
        
        for msg in recent:
            context_parts.append(f"{msg.role}: {msg.content}")
        
        return "\n".join(context_parts)
    
    def get_messages(self, n_messages: int = None) -> List[Message]:
        """Get recent messages."""
        if n_messages is None:
            return self.messages.copy()
        return self.messages[-n_messages:]
    
    def _compress_old_messages(self) -> None:
        """Compress old messages into a summary."""
        # Keep recent messages, summarize older ones
        keep_count = self.max_messages // 2
        compress_count = len(self.messages) - keep_count
        
        if compress_count <= 0:
            return
        
        # Get messages to compress
        to_compress = self.messages[:compress_count]
        
        # Create simple summary (in real app, use LLM)
        summary_parts = []
        if self.summary:
            summary_parts.append(self.summary)
        
        for msg in to_compress:
            if msg.role == "user":
                summary_parts.append(f"User asked about: {msg.content[:100]}...")
        
        self.summary = " ".join(summary_parts)
        
        # Keep only recent messages
        self.messages = self.messages[compress_count:]
    
    def clear(self) -> None:
        """Clear all conversation history."""
        self.messages = []
        self.summary = None