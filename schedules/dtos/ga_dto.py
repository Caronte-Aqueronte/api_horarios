from typing import Dict

from pydantic import BaseModel, ConfigDict
from typing import Tuple

from schedules.ga.schedule import Schedule


class GaDTO(BaseModel):
    schedule: Schedule
    total_iterations: int
    history_confilcts: Dict[str, int]
    history_fitness: Dict[str, int]
    memory_usage: float
    total_time: float
    semester_continuity_percentages: Dict[str, float]

    # permite que se pueda agregas schedu;e aqui
    model_config = ConfigDict(arbitrary_types_allowed=True)
