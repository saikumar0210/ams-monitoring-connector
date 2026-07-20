from typing import Optional
from pydantic import BaseModel


class Incident(BaseModel):

    # Required
    short_description: str
    description: str

    # Caller
    caller_id: Optional[str] = None

    # Category
    category: Optional[str] = "Software"
    subcategory: Optional[str] = None

    # Service
    business_service: Optional[str] = None

    # Impact / Urgency (1=High, 2=Medium, 3=Low)
    impact: Optional[str] = "2"
    urgency: Optional[str] = "2"

    # State (1=New)
    state: Optional[str] = "1"

    # Channel
    contact_type: Optional[str] = None

    # Assignment
    assignment_group: Optional[str] = None
    assigned_to: Optional[str] = None