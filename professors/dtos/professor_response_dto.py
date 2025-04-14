from datetime import time
from typing import List
from pydantic import BaseModel

from courses.dto.course_response_dto import CourseResponseDTO
from professors.models.professor import Professor


class ProfessorResponseDTO(BaseModel):
    id: int
    name: str
    personal_id: str
    entry_time: time
    exit_time: time
    entry_time_str: str
    exit_time_str: str

    courses: List[CourseResponseDTO]

    class Config:
        from_attributes = True  # permite construir el dto directamente desde objetos orm

    @staticmethod
    def from_professor(professor: Professor):
        return ProfessorResponseDTO(
            id=professor.id,
            name=professor.name,
            personal_id=professor.personal_id,
            entry_time=professor.entry_time,
            exit_time=professor.exit_time,
            entry_time_str=professor.entry_time.strftime('%I:%M %p'),
            exit_time_str=professor.exit_time.strftime('%I:%M %p'),
            courses=[CourseResponseDTO.from_course(course)
                     for course in professor.courses]
        )
