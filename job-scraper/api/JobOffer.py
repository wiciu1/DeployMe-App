from typing import List, Optional
from pydantic import BaseModel, Field


# DTO
class JobOffer(BaseModel):
    site: str
    url: str
    title: str
    company: str
    location: str
    experience: str
    salary: str
    date_posted: str = Field(alias="datePosted")
    valid_through: str = Field(alias="validThrough")
    skills: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "site": "JustJoinIT",
                "url": "https://example.com/offer/123",
                "title": "Title",
                "company": "Company Name",
                "location": "Warszawa",
                "experience": "Junior",
                "salary": "15 000 - 20 000 PLN",
                "datePosted": "2025-08-01",
                "validThrough": "2025-08-11",
                "skills": ["Python", "Django", "FastAPI"]
            }
        }
