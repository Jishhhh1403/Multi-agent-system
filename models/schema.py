from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum

class AgentType(str, Enum):
    MANAGER = "manager"
    DOCUMENTATION = "documentation"
    REVIEW = "review"
    KNOWLEDGE = "knowledge"

class QueryIntent(str, Enum):
    GENERATE_DOCS = "generate_docs"
    REVIEW_CODE = "review_code"
    ASK_QUESTION = "ask_question"
    EXPLAIN_CODE = "explain_code"

class CodeIssue(BaseModel):
    """Represents a single issue found in code."""
    severity: Literal["critical", "warning", "info"]
    line_number: int
    description: str
    suggestion: Optional[str] = None

class DocumentationOutput(BaseModel):
    """Output from documentation generation."""
    file_path: str
    summary: str
    docstring: Optional[str] = None
    sections: List[str] = Field(default_factory=list)

class ReviewOutput(BaseModel):
    """Output from code review."""
    file_path: str
    summary: str
    issues: List[CodeIssue] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    quality_score: float = Field(ge=0, le=1)

class KnowledgeOutput(BaseModel):
    """Output from knowledge retrieval."""
    answer: str
    sources: List[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)

class AgentState(BaseModel):
    """Base state for all agents."""
    query: str
    agent_type: AgentType
    context: Optional[str] = None
    memory: Optional[dict] = None

class GraphState(BaseModel):
    """State that flows through the LangGraph workflow."""
    user_query: str
    intent: Optional[QueryIntent] = None
    current_agent: Optional[AgentType] = None
    retrieved_docs: List[str] = Field(default_factory=list)
    agent_output: Optional[dict] = None
    validation_errors: List[str] = Field(default_factory=list)
    final_response: Optional[str] = None