from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.interaction import HCPInteractionCreate, HCPInteraction as HCPInteractionSchema
from app.services.interaction_service import InteractionService
from app.core.logger import logger

router = APIRouter(prefix="/interactions", tags=["Interactions"])

@router.post("/", response_model=HCPInteractionSchema, status_code=status.HTTP_201_CREATED)
def create_interaction(interaction: HCPInteractionCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Saving interaction to database...")  
        result = InteractionService.create_interaction(db, interaction)
        logger.info(f"Interaction saved successfully. ID: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating interaction: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create interaction.")

@router.get("/", response_model=list[HCPInteractionSchema], status_code=status.HTTP_200_OK)
def get_interactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return InteractionService.get_interactions(db, skip, limit)
    except Exception as e:
        logger.error(f"Error fetching interactions: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch interactions.")
