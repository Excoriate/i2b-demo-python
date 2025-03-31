from pydantic import BaseModel, Field
from typing import List, Optional

class Skill(BaseModel):
    """Represents a skill associated with a job offer."""
    title: str

class JobOffer(BaseModel):
    """Represents a job offer fetched from the external source."""
    # Using Field aliases to map potential differences or for clarity if needed
    # For CouchDB, we might use title+location as _id later
    title: str = Field(..., description="Job title")
    hour: Optional[str] = Field(None, description="Salary/Rate information") # Renamed from 'hour' for clarity
    modo: Optional[str] = Field(None, description="Work mode (e.g., Remote)")
    time: Optional[str] = Field(None, description="Work time (e.g., Full Time)")
    detail: Optional[str] = Field(None, description="Job details/description (HTML content)")
    skills: List[Skill] = Field([], description="List of required skills")
    location: Optional[str] = Field(None, description="Job location")

    # You might add a field for the source URL or fetch timestamp if needed
    # source_url: str = Field(..., description="URL the offer was fetched from")
    # fetched_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        # If you decide to use title+location as _id in CouchDB:
        # populate_by_name = True
        # Define an id field with alias '_id'
        # id: Optional[str] = Field(None, alias="_id")
        pass
