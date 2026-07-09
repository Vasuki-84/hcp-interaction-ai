from fastapi import APIRouter, HTTPException, status
from app.schemas.interaction import ChatMessageRequest
from app.services.chat_service import ChatService
from app.core.logger import logger

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", status_code=status.HTTP_200_OK)
def chat_with_agent(request: ChatMessageRequest):
    try:
        response_data = ChatService.handle_chat_message(request)
        return response_data
    except Exception as e:
        logger.error(f"Error during chat interaction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the chat."
        )
    