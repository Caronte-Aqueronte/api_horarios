from typing import Dict, List, Tuple
from pydantic import BaseModel, Field


class GenerateScheduleRequestDTO(BaseModel):

    population_size: int = Field(..., gt=0)
    max_generations: int = Field(..., gt=0)
    target_fitness: int = Field(..., gt=0)
    courses_availables_ids: List[int] = Field(...)
    professors_availables_ids: List[int] = Field(...)
    manual_course_classrooms_assignments:  Dict[int, int] = Field(...)
