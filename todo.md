# AI-Powered Code Documentation & Review Assistant - Implementation Tasks

## Task 4: LangGraph Workflow

### Goal
Create a LangGraph workflow that orchestrates the agents with conditional routing, state management, and a validation node.

### Steps

#### 4.1 Create state/graph_state.py
Defines the state that flows through the entire graph.

#### 4.2 Create graphs/nodes/router_node.py
Classifies intent and routes to appropriate agent.

#### 4.3 Create graphs/nodes/documentation_node.py
Execute the documentation agent.

#### 4.4 Create graphs/nodes/review_node.py
Execute the review agent.

#### 4.5 Create graphs/nodes/knowledge_node.py
Execute the knowledge agent.

#### 4.6 Create graphs/nodes/validation_node.py
Validate the final response for safety and quality.

#### 4.7 Create graphs/nodes/__init__.py
Export all nodes.

#### 4.8 Create graphs/workflow.py
Main graph that wires everything together.

#### 4.9 Create graphs/__init__.py
Export the compiled graph.

---

## Task 5: Middleware & Guardrails

### Goal
Implement custom middleware using LangChain 1.0+ patterns, plus guardrails for output validation and safety.

### Steps

#### 5.1 Create middleware/logging_middleware.py
Logs agent activity at each stage of the loop.

#### 5.2 Create middleware/rate_limiter.py
Limits requests per minute to avoid hitting API rate limits.

#### 5.3 Create middleware/error_recovery.py
Catches errors during model calls and returns a graceful fallback.

#### 5.4 Create middleware/cache_middleware.py
Caches model responses for repeated queries.

#### 5.5 Create middleware/__init__.py
Export all middleware and provide get_default_middleware().

#### 5.6 Create models/guardrails/output_validator.py
Validates agent outputs against quality standards.

#### 5.7 Create models/guardrails/content_filter.py
Filters harmful or inappropriate content from responses.

#### 5.8 Create models/guardrails/quality_scorer.py
Scores response quality based on multiple factors.

#### 5.9 Create models/guardrails/__init__.py
Unified guardrails interface with GuardrailsManager.

#### 5.10 Update graphs/nodes/validation_node.py
Replace simple validation with the new guardrails system.

---

## Task 6: MCP Integration - Model Context Protocol

### Goal
Create an MCP server that exposes code tools and resources, then integrate it with LangChain agents using langchain-mcp-adapters.

### Steps

#### 6.1 Add Dependencies
`ash
uv add fastmcp langchain-mcp-adapters mcp
`

#### 6.2 Create mcp/server.py
MCP server with tools: read_file, list_files, analyze_python_file, search_in_files, get_file_stats, and resource: codebase_summary.

#### 6.3 Create mcp/client.py
Connects to MCP server and loads tools for LangChain using MultiServerMCPClient.

#### 6.4 Create mcp/config.py
MCP server configurations.

#### 6.5 Create mcp/__init__.py
Export MCP client functions.

#### 6.6 Update agents/knowledge_agent.py
Integrate MCP tools into the knowledge agent.

---

## Task 7: CLI Entry Point & Full Integration

### Goal
Create a polished CLI interface using click and rich that ties together all components.

### Steps

#### 7.1 Create main.py
CLI with commands: ingest, ask, docs, review, chat, status.

---

## Task 8: Final Polish & README

### Goal
Write a comprehensive README, clean up code, verify everything works end-to-end.

### Steps

#### 8.1 Create .env.example
Template for environment variables.

#### 8.2 Create tests/test_basic.py
Basic tests for settings, schemas, guardrails, memory, intent classifier, and router.

#### 8.3 Create tests/__init__.py
Empty init file for tests package.

#### 8.4 Final Code Review Checklist
- All imports correct
- No unused imports
- Type hints consistent
- Docstrings present
- Error handling in place
- No hardcoded secrets
- .env in .gitignore
- data/ in .gitignore

#### 8.5 Update .gitignore
Add .env, __pycache__, data/, *.db, IDE files.

---

## Final Project Summary

| Component | What It Demonstrates |
|-----------|---------------------|
| LangChain 1.0+ Agents | New create_agent pattern with middleware |
| LangGraph Workflow | StateGraph with conditional routing |
| RAG with ChromaDB | Vector store, embeddings, retrieval |
| Memory Management | Conversation history, document memory |
| MCP Integration | FastMCP server, tool exposure |
| Guardrails | Validation, filtering, quality scoring |
| Middleware | Logging, rate limiting, error recovery, caching |
| Hierarchical Agents | Manager -> Worker pattern |
| Pydantic Schemas | Type-safe data models |
| CLI Interface | Click + Rich for polished UX |
