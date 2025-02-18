from schemas import *
from fastapi import APIRouter, status, Request

from services import FeedbackService

router = APIRouter(tags=["Feedback"], prefix="/feedback")

@router.post("/create", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(feedback: FeedbackCreate):
    return await FeedbackService.create_feedback(feedback)


@router.get("/get", response_model=List[FeedbackResponse])
async def get_all_feedback(request: Request):
    return await FeedbackService.get_all_feedback(request)

@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback_by_id(feedback_id: int, request: Request):
    return await FeedbackService.get_feedback_by_id(feedback_id, request)


@router.put("/{feedback_id}/process", response_model=FeedbackResponse)
async def process_feedback(feedback_id: int, request: Request):
    return await FeedbackService.process_feedback(feedback_id, request)