from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time
from app.db.database import SessionLocal
from app.models.interaction import HCPInteraction

# Define Schemas for Tool Inputs
class LogInteractionInput(BaseModel):
    hcp_name: str = Field(description="Name of the Healthcare Professional")
    interaction_type: str = Field(description="Type of interaction (e.g., Meeting, Email)")
    interaction_date: str = Field(description="Date in YYYY-MM-DD format")
    interaction_time: str = Field(description="Time in HH:MM format")
    attendees: Optional[str] = Field(None, description="Names of other attendees")
    topics_discussed: Optional[str] = Field(None, description="Key topics discussed")
    materials_shared: Optional[str] = Field(None, description="Materials or samples shared")
    samples_distributed: Optional[str] = Field(None, description="Samples distributed")
    sentiment: Optional[str] = Field(None, description="Inferred sentiment (Positive, Neutral, Negative)")
    outcomes: Optional[str] = Field(None, description="ALWAYS extract if a meeting result, decision, agreement, or request is mentioned. Must be distinct from follow-up actions.")
    follow_up_actions: Optional[str] = Field(None, description="ALWAYS extract if a future action, next step, or planned task is mentioned. Must be distinct from outcomes.")

# TOOL 2: Updates the selected fields of an existing iteration
class EditInteractionInput(BaseModel):
    interaction_id: int = Field(description="ID of the interaction to edit")
    field_to_update: str = Field(description="The name of the field to update (e.g., 'topics_discussed', 'sentiment')")
    new_value: str = Field(description="The new value for the field")

#  TOOL 3: Retrieves the previous interation history from the database.
class FetchInteractionsInput(BaseModel):
    hcp_name: str = Field(description="Name of the HCP to fetch history for")

# TOOL 1: Extracts the structured data from the interation form
class ExtractEntitiesInput(BaseModel):
    hcp_name: str = Field(
        default="",
        description="Main HCP name only."
    )

    interaction_type: str = Field(
        default="Meeting",
        description="Meeting, Call, Email etc."
    )

    interaction_date: str = Field(
        default="",
        description="YYYY-MM-DD format."
    )

    interaction_time: str = Field(
        default="",
        description="HH:MM (24 hour). Empty if not mentioned."
    )

    attendees: str = Field(
        default="",
        description="Additional attendees only."
    )

    topics_discussed: str = Field(
        default="",
        description="Topics discussed."
    )
    samples_distributed: str = Field(
        default="",
        description="Samples distributed."
    )

    sentiment: str = Field(
        default="Neutral",
        description="Positive, Neutral or Negative."
    )

    materials_shared: str = Field(
        default="",
        description="Materials shared."
    )
    outcomes: str = Field(
        default="",
        description="Meeting outcome."
    )

    follow_up_actions: str = Field(
        default="",
        description="Future follow-up actions."
    )

# TOOL 4: Generates suggested next actions based on meeting outcomes.
class SuggestFollowUpInput(BaseModel):
    topics_discussed: str = Field(description="Topics discussed during the interaction")
    outcomes: str = Field(description="Outcomes or agreements from the interaction")

#  TOOL 5: Saves the interation into the database.
@tool("log_interaction", args_schema=LogInteractionInput)
def log_interaction(
    hcp_name: str,
    interaction_type: str,
    interaction_date: date,
    interaction_time: time,
    attendees: Optional[str] = None,
    topics_discussed: Optional[str] = None,
    materials_shared: Optional[str] = None,
    samples_distributed: Optional[str] = None,
    sentiment: Optional[str] = None,
    outcomes: Optional[str] = None,
    follow_up_actions: Optional[str] = None,
) -> str:
    """Logs a new HCP interaction to the database."""
    db = SessionLocal()
    from app.core.logger import logger
    try:
        new_interaction = HCPInteraction(
            hcp_name=hcp_name,
            interaction_type=interaction_type,
            interaction_date=interaction_date,
            interaction_time=interaction_time,
            attendees=attendees,
            topics_discussed=topics_discussed,
            materials_shared=materials_shared,
            samples_distributed=samples_distributed,
            sentiment=sentiment,
            outcomes=outcomes,
            follow_up_actions=follow_up_actions
        )
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        logger.info(f"Tool execution: log_interaction success. ID: {new_interaction.id}")
        return f"Successfully logged interaction with {hcp_name} on {interaction_date}. Interaction ID: {new_interaction.id}"
    except Exception as e:
        db.rollback()
        logger.error(f"Tool execution error (log_interaction): {str(e)}")
        return f"Error logging interaction: A database error occurred."
    finally:
        db.close()

@tool("edit_interaction", args_schema=EditInteractionInput)
def edit_interaction(interaction_id: int, field_to_update: str, new_value: str) -> str:
    """Modifies a previously logged interaction based on its ID and the specific field to update."""
    EDITABLE_FIELDS = [
        'topics_discussed',
        'materials_shared',
        'samples_distributed',
        'sentiment',
        'outcomes',
        'follow_up_actions',
        'attendees'
    ]

    if field_to_update not in EDITABLE_FIELDS:
        from app.core.logger import logger
        logger.warning(f"Attempted to update restricted field: {field_to_update}")
        return f"Update failed: Field '{field_to_update}' is not allowed to be modified."

    db = SessionLocal()
    from app.core.logger import logger
    try:
        interaction = db.query(HCPInteraction).filter(HCPInteraction.id == interaction_id).first()
        if not interaction:
            logger.warning(f"Interaction edit failed: ID {interaction_id} not found.")
            return f"Interaction with ID {interaction_id} not found."
        
        setattr(interaction, field_to_update, new_value)
        db.commit()
        logger.info(f"Successfully updated {field_to_update} for interaction {interaction_id}.")
        return f"Successfully updated {field_to_update} for interaction {interaction_id}."
    except Exception as e:
        db.rollback()
        logger.error(f"Error editing interaction {interaction_id}: {str(e)}")
        return f"Error editing interaction: A database error occurred."
    finally:
        db.close()

@tool("fetch_past_interactions", args_schema=FetchInteractionsInput)
def fetch_past_interactions(hcp_name: str) -> str:
    """Retrieves the history of past interactions with a specific HCP."""
    db = SessionLocal()
    try:
        interactions = db.query(HCPInteraction).filter(HCPInteraction.hcp_name.ilike(f"%{hcp_name}%")).order_by(HCPInteraction.interaction_date.desc()).limit(5).all()
        if not interactions:
            return f"No past interactions found for {hcp_name}."
        
        res = [f"ID: {i.id}, Date: {i.interaction_date}, Topics: {i.topics_discussed}" for i in interactions]
        return "\n".join(res)
    finally:
        db.close()

@tool("extract_entities", args_schema=ExtractEntitiesInput)
def extract_entities(**kwargs) -> str:
    """
      Extract every interaction field from the user's conversation.

    ALWAYS populate:

    - hcp_name
    - interaction_type
    - interaction_date
    - interaction_time
    - attendees
    - topics_discussed
    - materials_shared
    - samples_distributed
    - sentiment
    - outcomes
    - follow_up_actions

    Return empty string only when a field truly does not exist.
    """
    return "Entities successfully extracted and sent to the frontend. Please tell the user to review the populated form and click the 'Save Interaction' button."

@tool("suggest_follow_up", args_schema=SuggestFollowUpInput)
def suggest_follow_up(topics_discussed: str, outcomes: str) -> str:
    """Analyzes topics and outcomes to suggest follow-up actions."""
    # The agent will use its LLM capability to generate the suggestion. This tool 
    # provides a structured prompt instruction back to the agent.
    return "Based on the topics and outcomes, please suggest 1-2 actionable follow-up tasks."

TOOLS = [
    log_interaction,
    edit_interaction,
    fetch_past_interactions,
    extract_entities,
    suggest_follow_up
]
