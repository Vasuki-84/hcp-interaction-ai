from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.interaction import HCPInteraction
from app.schemas.interaction import HCPInteractionCreate
from app.core.logger import logger

class InteractionService:
    """Service layer for handling HCP interactions business logic."""
    
    @staticmethod
    def create_interaction(db: Session, interaction_data: HCPInteractionCreate) -> HCPInteraction:
        """
        Creates a new HCP interaction record in the database.
        
        Args:
            db (Session): Database session.
            interaction_data (HCPInteractionCreate): Validated data for the new interaction.
            
        Returns:
            HCPInteraction: The created database record.
            
        Raises:
            Exception: If a database error occurs during the transaction.
        """
        try:
            db_interaction = HCPInteraction(**interaction_data.model_dump())
            db.add(db_interaction)
            db.commit()
            db.refresh(db_interaction)
            logger.info(f"Successfully created interaction with ID: {db_interaction.id}")
            return db_interaction
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error during interaction creation: {str(e)}")
            raise Exception("A database error occurred while creating the interaction.")

    @staticmethod
    def get_interactions(db: Session, skip: int = 0, limit: int = 100) -> list[HCPInteraction]:
        """
        Retrieves a list of HCP interactions with pagination.
        
        Args:
            db (Session): Database session.
            skip (int): Number of records to skip.
            limit (int): Maximum number of records to return.
            
        Returns:
            list[HCPInteraction]: List of interaction records.
        """
        try:
            interactions = db.query(HCPInteraction).offset(skip).limit(limit).all()
            logger.info(f"Retrieved {len(interactions)} interactions.")
            return interactions
        except SQLAlchemyError as e:
            logger.error(f"Database error during fetching interactions: {str(e)}")
            raise Exception("A database error occurred while fetching interactions.")
