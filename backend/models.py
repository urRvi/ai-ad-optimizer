from typing import Optional
from sqlmodel import SQLModel, Field

class Generation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product: str
    audience: str
    tone: str
    keywords: str
    prompt: str
    output_json: str
    model: str
    cost_tokens: int = 0
