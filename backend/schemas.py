from pydantic import BaseModel
from typing import List, Optional

class GenerateIn(BaseModel):
    product: str
    audience: str
    tone: str = "Professional"
    keywords: str = ""
    variants: int = 5
    include_lp: bool = True

class Variant(BaseModel):
    headline: str
    description: str
    cta: str

class GenerateOut(BaseModel):
    variants: List[Variant]
    landing: Optional[dict] = None
    id: int
