from typing import Optional
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain_core.tools import tool
from agents.documentation_agent import Documentation_agent
from agents.review_agent import Review_agent
from agents.knowledge_agent import Knowledge_agent
from memory.memory_manager import MemoryManager
from models.schema import QueryIntent
from prompts.manager_prompts import MANAGER_SYSTEM_PROMPT
from config.settings import settings

class IntentClassifier:
    """Classifies user intent to route to appropriate agent."""
    
    INTENT_KEYWORDS = {
        QueryIntent.GENERATE_DOCS: [
            "document", "documentation", "docstring", "explain code",
            "generate docs", "write docs", "add comments"
        ],
        QueryIntent.REVIEW_CODE: [
            "review", "check", "bugs", "issues", "improve",
            "refactor", "code review", "quality"
        ],
        QueryIntent.ASK_QUESTION: [
            "what", "how", "why", "explain", "describe",
            "tell me", "help me understand"
        ]
    }
    
    def classify(self, query: str) -> QueryIntent:
        query_lower = query.lower()
        scores = {}
        for intent, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in query_lower)
            scores[intent] = score
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return QueryIntent.ASK_QUESTION


def create_manager_tools(
    doc_agent: Documentation_agent,
    review_agent: Review_agent,
    knowledge_agent: Knowledge_agent
) -> list:
    """Create tools that delegate to specialized agents."""
    
    @tool
    def generate_documentation(query: str) -> str:
        """Generate documentation for code. Use when user wants to create docs, docstrings, or explain code."""
        doc_agent.build()
        result = doc_agent.invoke(query)
        return doc_agent.get_last_response(result)
    
    @tool
    def review_code(query: str) -> str:
        """Review code for bugs, issues, and improvements. Use when user wants code review or quality check."""
        review_agent.build()
        result = review_agent.invoke(query)
        return review_agent.get_last_response(result)
    
    @tool
    def ask_knowledge_base(query: str) -> str:
        """Answer questions about the codebase. Use when user has questions about code, architecture, or how things work."""
        knowledge_agent.build()
        result = knowledge_agent.invoke(query)
        return knowledge_agent.get_last_response(result)
    
    return [generate_documentation, review_code, ask_knowledge_base]


class ManagerAgent:
    """Manager agent that orchestrates specialized agents."""
    
    def __init__(self, model=None, memory: Optional[MemoryManager] = None):
        self.model = model or settings.default_model
        self.memory = memory
        self.intent_classifier = IntentClassifier()
        
        # Create specialized agents
        self.doc_agent = Documentation_agent(model=self.model, memory=memory)
        self.review_agent = Review_agent(model=self.model, memory=memory)
        self.knowledge_agent = Knowledge_agent(model=self.model, memory=memory)
        
        # Create delegation tools
        self.tools = create_manager_tools(
            self.doc_agent,
            self.review_agent,
            self.knowledge_agent
        )
        
        self._agent = None
    
    def build(self):
        """Build the manager agent."""
        self._agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=MANAGER_SYSTEM_PROMPT,
            name="manager"
        )
        return self._agent
    
    def invoke(self, query: str) -> dict:
        if self._agent is None:
            self.build()
        
        result = self._agent.invoke({
            "messages": [("user", query)]
        })
        return result
    
    async def ainvoke(self, query: str) -> dict:
        if self._agent is None:
            self.build()
        
        result = await self._agent.ainvoke({
            "messages": [("user", query)]
        })
        return result
    
    def get_last_response(self, result: dict) -> str:
        messages = result.get("messages", [])
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.type == "ai":
                return msg.content
        return ""