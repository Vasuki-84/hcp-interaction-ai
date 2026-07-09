from app.graph.graph import process_chat
from app.schemas.interaction import ChatMessageRequest
from app.core.logger import logger

class ChatService:
    """Service layer for handling AI Chat interactions."""
    
    @staticmethod
    def handle_chat_message(request: ChatMessageRequest) -> dict:
        """
        Processes a chat message through the LangGraph agent.
        
        Args:
            request (ChatMessageRequest): The chat message and history.
            
        Returns:
            dict: The AI assistant's response and optionally extracted form data.
        """
        try:
            # The history should include the new message
            messages = request.history + [{"role": "user", "content": request.message}]
            logger.info("Processing chat message through LangGraph agent.")
            response = process_chat(messages)
            logger.info("Successfully generated AI response.")
            return response
        except Exception:
         logger.exception("Failed to process chat message")
         raise
