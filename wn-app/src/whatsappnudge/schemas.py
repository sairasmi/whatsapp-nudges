# define the schema of route for input request
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Text

class FormData(BaseModel):
    nudge: Optional[str] = None
    directorate: Optional[str] = None
    district: Optional[str] = None
    designation: Optional[str] = None
    

class SingleSent(BaseModel):
    mobile: str
    nudge: str


class BulkSent(BaseModel):
    nudge: Optional[str] = None
    directorate: Optional[str] = None
    district: Optional[str] = None
    designation: Optional[str] = None


class WhatsAppHistoryManually(BaseModel):
    start_date: str
    end_date: str
