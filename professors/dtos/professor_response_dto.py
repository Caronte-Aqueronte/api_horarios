from datetime import time
from pydantic import BaseModel


class ProfessorResponseDTO(BaseModel):
    id: int
    name: str
    dpi: str
    entry_time: time
    exit_time: time

    class Config:
        from_attributes = True  # permite construir el dto directamente desde objetos orm
