"""
incident/models/incident.py

Pydantic model representing a ServiceNow incident.
Field names map directly to the ServiceNow REST API table fields.

Required fields:
    short_description   - Brief summary shown as the incident tite (maps to Short description)
    description         - Full incident details (maps to Description)

Optional fields:
    caller_id           - User who reported the incident (maps to Caller)
    category            - Incident category e.g. Software (maps to Category)
    subcategory         - Incident subcategory (maps to Subcategory)
    business_service    - Affected business service (maps to Service)
    impact              - Business impact: 1=High, 2=Medium, 3=Low (maps to Impact)
    urgency             - Resolution urgency: 1=High, 2=Medium, 3=Low (maps to Urgency)
    state               - Incident state: 1=New (maps to State)
    contact_type        - Channel through which incident was reported (maps to Channel)
    assignment_group    - Group responsible for resolving the incident (maps to Assignment group)
    assigned_to         - Individual assigned to resolve the incident (maps to Assigned to)
"""
from typing import Optional
from pydantic import BaseModel


class Incident(BaseModel):

    # Required
    short_description: str
    description: str

    # Caller
    caller_id: Optional[str] = "admin"  # Defaults to System Administrator

    # Category
    category: Optional[str] = "Software"
    subcategory: Optional[str] = None

    # Service
    business_service: Optional[str] = None
    service_offering: Optional[str] = None  # maps to Service offering
    cmdb_ci: Optional[str] = None           # maps to Configuration item

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
    
    #configuration item (CI) associated with the incident