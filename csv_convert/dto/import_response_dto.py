
from typing import List
from pydantic import BaseModel


class ImportResponseDTO(BaseModel):

    success: List[str]
    warnings: List[str]
