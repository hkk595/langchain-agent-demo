from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag.rag_pipeline import ask_question

app = FastAPI()

class Question(BaseModel):
    query: str

@app.post("/ask")
async def ask(question: Question):
    try:
        response = await ask_question(question.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
