from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.services.qdrant_services import create_collection
from app.routes.search import router as search_router
from app.routes.eval import router as eval_router


app= FastAPI(
    title="EvalRAG API",
    description="A production RAG system with Evaluation",
    version="1.0.0"
)
create_collection()

app.include_router(upload_router)
app.include_router(search_router)
app.include_router(eval_router)

@app.get('/')
def root():
    return{
        "message": "Welcome to EvalRAG",
        "docs":"/docs"
        }

@app.get("/health")
def health():
    return {"status": "healthy"}