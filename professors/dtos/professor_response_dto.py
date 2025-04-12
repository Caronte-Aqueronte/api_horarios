from datetime import time
from typing import List
from pydantic import BaseModel

from courses.dto.course_response_dto import CourseResponseDTO
from professors.models.professor import Professor


class ProfessorResponseDTO(BaseModel):
    id: int
    name: str
    dpi: str
    entry_time: time
    exit_time: time
    courses: List[CourseResponseDTO]

    class Config:
        from_attributes = True  # permite construir el dto directamente desde objetos orm

    @staticmethod
    def from_professor(professor: Professor):
        return ProfessorResponseDTO(
            professor.id,
            professor.name,
            professor.dpi,
            professor.entry_time,
            professor.exit_time,
            [CourseResponseDTO.from_course(course)
             for course in professor.courses]
        )
