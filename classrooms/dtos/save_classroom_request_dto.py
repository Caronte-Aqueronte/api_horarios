from datetime import time
from pydantic import BaseModel, Field
from courses.enums.course_type_enum import CourseTypeEnum


class SaveClassroomRequestDTO(BaseModel):

    name: str = Field(..., max_length=100, min_length=1)
