from datetime import time
from pydantic import BaseModel

from classrooms.models.classroom import Classroom


class ClassroomResponseDTO(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # permite construir el dto directamente desde objetos orm

    @staticmethod
    def from_classroom(classroom: Classroom):
        return ClassroomResponseDTO(
            id=classroom.id,
            name=classroom.name
        )
