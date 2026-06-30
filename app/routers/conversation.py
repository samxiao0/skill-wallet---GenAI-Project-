from fastapi import APIRouter

from app.models.schemas import (
    ConversationRequest,
    ConversationResponse,
    FactCheckRequest,
    FactCheckResponse
)

from app.services.history_logger import (
    save_history,
    get_history
)

from app.services.event_analyzer import analyze_event
from app.services.topic_generator import generate_conversation_topics
from app.services.fact_checker import verify_topic
from app.services.history_logger import save_history
from app.models.schemas import FeedbackRequest
from app.services.feedback_logger import save_feedback

router = APIRouter()


@router.post(
    "/generate",
    response_model=ConversationResponse
)
def generate_conversation(
        request: ConversationRequest):

    topics = analyze_event(request.description)

    suggestions = generate_conversation_topics(
        topics,
        request.interests
    )

    save_history({
        "description": request.description,
        "topics": topics,
        "suggestions": suggestions
    })

    return {
        "topics": topics,
        "suggestions": suggestions
    }


@router.post(
    "/fact-check",
    response_model=FactCheckResponse
)
def fact_check(request: FactCheckRequest):

    summary = verify_topic(request.query)

    return {"summary": summary}

@router.get("/history")
def history():
    return get_history()

@router.post("/feedback")
def submit_feedback(request: FeedbackRequest):

    save_feedback({
        "suggestion": request.suggestion,
        "rating": request.rating
    })

    return {"message": "Feedback saved successfully"}