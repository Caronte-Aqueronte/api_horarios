from typing import List, Tuple
from pydantic import BaseModel, Field


class GenerateScheduleRequestDTO(BaseModel):

    population_size: int = Field(..., gt=0)
    max_generations: int = Field(..., gt=0)
    courses_availables_ids: List[int] = Field(...)
    professors_availables_ids: List[str] = Field(...)
    manual_course_classrooms_assignments: List[Tuple[int, int]] = Field(...)
