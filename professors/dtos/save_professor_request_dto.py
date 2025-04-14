from datetime import time
from typing import List
from pydantic import BaseModel, Field


class SaveProfessorRequestDTO(BaseModel):

    name: str = Field(..., max_length=100, min_length=1)
    personal_id: str = Field(..., max_length=100, min_length=1)
    entry_time: time = Field(...)
    exit_time: time = Field(...)
    courses_ids: List[int] = Field(...)
