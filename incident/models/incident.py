from pydantic import BaseModel


class Incident(BaseModel):

    application: str

    service: str

    environment: str

    severity: str

    title: str

    description: str