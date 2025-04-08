from datetime import time
from pydantic import BaseModel


class ClassroomResponseDTO(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # permite construir el dto directamente desde objetos orm
