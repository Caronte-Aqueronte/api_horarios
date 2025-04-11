from datetime import time
from pydantic import BaseModel, Field
from courses.enums.course_type_enum import CourseTypeEnum


class SaveProfessorRequestDTO(BaseModel):

    name: str = Field(..., max_length=100, min_length=1)
    dpi: str = Field(..., max_length=13, min_length=13)
    entry_time: time = Field(...)
    exit_time: time = Field(...)
