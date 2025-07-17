# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Installation
```bash
pip install -r requirement.txt
```

### Running the Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing the API
```bash
curl --request POST \
  --url http://0.0.0.0:8000/ask \
  --header 'Content-Type: application/json' \
  --data '{"topic": "Anthropic"}'
```

### Running Components Individually
- Test the agent directly: `python mcp_clients/agent.py`
- Test the MCP server: `python mcp_servers/serper.py`

## Architecture Overview

This is a LangGraph-based agentic AI system that integrates with Model Context Protocol (MCP) servers to provide enhanced AI capabilities with external data sources.

### Core Components

**FastAPI Application** (`main.py`):
- Single `/ask` endpoint that accepts topic queries
- Delegates to the LangGraph agent for processing
- Returns formatted AI responses

**LangGraph Agent** (`mcp_clients/agent.py`):
- Uses `create_react_agent` from LangGraph with MCP tools
- Integrates with Anthropic Claude or OpenAI models via `init_chat_model`
- Connects to MCP servers through `MultiServerMCPClient`
- Implements ReAct pattern for reasoning and tool usage

**MCP Server** (`mcp_servers/serper.py`):
- Implements news search functionality using Serper API
- Uses FastMCP framework for MCP protocol compliance
- Provides `get_news` tool that agents can invoke
- Runs on stdio transport for communication

### Data Flow
1. FastAPI receives topic query
2. Agent uses LangGraph's ReAct pattern to process request
3. Agent dynamically calls MCP tools (news search) as needed
4. MCP server fetches external data via Serper API
5. Agent synthesizes response using retrieved information
6. Formatted response returned via FastAPI

## Environment Variables

Required environment variables:
- `MODEL_VERSION` (default: "claude-3-7-sonnet-latest")
- `MODEL_PROVIDER` (default: "anthropic") 
- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`
- `SERPER_API_KEY`
- `SERPER_API_BASE`
- `MCP_SERVER_PATH_SERPER` (absolute path to serper.py)

## Key Dependencies

- **LangChain**: Core LLM framework and model initialization
- **LangGraph**: Agent orchestration with ReAct pattern
- **MCP**: Model Context Protocol for tool integration
- **FastMCP**: MCP server implementation framework
- **FastAPI**: Web API framework
- **httpx**: Async HTTP client for external API calls
