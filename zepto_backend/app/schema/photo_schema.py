from pydantic import BaseModel
from datetime import datetime

class PhotoResponse(BaseModel):

    id: int
    filename: str
    content_type: str
    created_at: datetime

