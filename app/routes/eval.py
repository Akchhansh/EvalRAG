from fastapi import APIRouter
from app.services.eval_service import run_evaluation

router = APIRouter()


@router.get("/eval")
def evaluate():
    return run_evaluation()