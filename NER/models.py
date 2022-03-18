from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID, uuid4



#python -m uvicorn main:app --reload


class image(BaseModel):
    unique_id: Optional[str]
    tags: List[List[str]]
