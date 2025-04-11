from pydantic import BaseModel, field_serializer
from courses.enums.course_type_enum import CourseTypeEnum
from courses.models.course import Course
from professors.dtos.professor_response_dto import ProfessorResponseDTO


class CourseResponseDTO(BaseModel):
    id: int
    name: str
    code: str
    career: str
    semester: int
    section: str
    type: CourseTypeEnum
    professor: ProfessorResponseDTO = None

    class Config:
        from_attributes = True  # permite construir el dto directamente desde objetos orm

    @staticmethod
    def from_course(course: Course) -> "CourseResponseDTO":
        return CourseResponseDTO(
            id=course.id,
            name=course.name,
            code=course.code,
            career=course.career,
            semester=course.semester,
            section=course.section,
            type=course.type,
            professor=ProfessorResponseDTO.model_validate(course.professor)
        )
