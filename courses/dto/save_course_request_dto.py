from pydantic import BaseModel, Field
from courses.enums.course_type_enum import CourseTypeEnum


class SaveCourseRequestDTO(BaseModel):

    name: str = Field(..., max_length=100, min_length=1)
    code: str = Field(..., max_length=20, min_length=1)
    career: str = Field(..., max_length=100, min_length=1)
    semester: int = Field(..., gt=0)
    section: str = Field(..., max_length=10, min_length=1)
    type: CourseTypeEnum = Field(...)
