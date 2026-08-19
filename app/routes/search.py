from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_services import ask_question

router= APIRouter()

class SearchRequest(BaseModel):
    query:str

@router.post("/search")
def search(request:SearchRequest):
    return ask_question(request.query)

@router.post("/query")
def query(request: SearchRequest):
    return ask_question(request.query)
