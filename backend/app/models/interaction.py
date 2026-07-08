from sqlalchemy import Column, Integer, String, Date, Time, Text, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class HCPInteraction(Base):
    __tablename__ = "hcp_interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255), nullable=False)
    interaction_type = Column(String(100), nullable=False)
    interaction_date = Column(Date, nullable=False)
    interaction_time = Column(Time, nullable=False)
    attendees = Column(String(500), nullable=True)
    topics_discussed = Column(Text, nullable=True)
    materials_shared = Column(Text, nullable=True)
    samples_distributed = Column(Text, nullable=True)
    sentiment = Column(String(50), nullable=True)
    outcomes = Column(Text, nullable=True)
    follow_up_actions = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
