# LangChain Agentic AI Demo

## Technical Stack
- [Anthropic](https://www.anthropic.com/api)
- [OpenAI](https://openai.com/api/)
- [LangChain](https://www.langchain.com/)
- [LangGraph](https://www.langchain.com/langgraph)
- [Serper](https://serper.dev/)
- [Model Context Protocol](https://modelcontextprotocol.io/introduction)
- [FastAPI](https://fastapi.tiangolo.com/)

## Environment Variables
MODEL_VERSION<br>
MODEL_PROVIDER<br>
ANTHROPIC_API_KEY<br>
OPENAI_API_KEY<br>
SERPER_API_KEY<br>
SERPER_API_BASE<br>
MCP_SERVER_PATH_SERPER

## Installation
```bash
pip install -r requirement.txt
```

## Start the server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Example request
```bash
curl --request POST \
  --url http://0.0.0.0:8000/ask \
  --header 'Content-Type: application/json' \
  --data '{
	"topic": "Anthropic"
}'
```
