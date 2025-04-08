from pydantic import BaseModel
from courses.enums.course_type_enum import CourseTypeEnum


class CourseResponseDTO(BaseModel):
    id: int
    name: str
    code: str
    career: str
    semester: int
    section: str
    type: CourseTypeEnum

    class Config:
        from_attributes = True
