from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import AIMessage
from mcp_clients.agent import answer_topic
import uvicorn

# Create FastAPI app
app = FastAPI(title="Agentic AI Demo", description="LLM-based agent with MCP integrated.")


class Question(BaseModel):
    topic: str


class Answer(BaseModel):
    answer: str


@app.post("/ask")
async def ask(question: Question):
    try:
        response = await answer_topic(question.topic)

        answer = ""
        for message in response["messages"]:
            if isinstance(message, AIMessage):
                answer += f"{message.text()}\n"
        answer = answer.strip()

        return Answer(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
