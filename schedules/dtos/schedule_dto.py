from typing import List, Dict, Tuple
from pydantic import BaseModel
from classrooms.models.classroom import Classroom
from classrooms.dtos.classroom_reponse_dto import ClassroomResponseDTO
from courses.dto.course_response_dto import CourseResponseDTO
from courses.models.course import Course
from professors.models.professor import Professor
from schedules.ga.schedule import Schedule
from schedules.models.gen import Gen
from schedules.utils.period_util import PeriodUtil


class AssignmentDTO(BaseModel):
    course: CourseResponseDTO | None
    professor_name: str | None
    professor_dpi: str | None
    is_empty: bool = False


class ScheduleRowDTO(BaseModel):
    period: int
    time_range: str
    assignments: List[AssignmentDTO]


class ScheduleDTO(BaseModel):
    classrooms: List[ClassroomResponseDTO]
    rows: List[ScheduleRowDTO]


class ScheduleDTOBuilder:

    def __init__(self, schedule: Schedule, classrooms: List[Classroom]):
        self.schedule = schedule
        self.classrooms = classrooms
        self.period_util = PeriodUtil()

    def build(self) -> ScheduleDTO:
        # convertimos los salones a dtos
        classroom_dtos: List[ClassroomResponseDTO] = [ClassroomResponseDTO.from_classroom(
            classroom) for classroom in self.classrooms]

        # mandamos a crear el mapa para faciliar el saber las asignaciones
        schedule_map: Dict[Tuple[int, int], Gen] = self.__get_period_map()

        # construimos las filas con el dto preciso
        rows: List[ScheduleRowDTO] = []
        for period in range(1, 10):
            period_start, period_end = self.period_util.get_start_and_end_time_for_period(
                period)
            time_range: str = f"{period_start.strftime('%I:%M %p')} - {period_end.strftime('%I:%M %p')}"

            # para cada salón, creamos una asignacion
            assignments_for_period: List[AssignmentDTO] = []

            for classroom in self.classrooms:
                key = (period, classroom.id)

                # si la key que creamos existe entonces hay una asignacion en la clase en el periodo, lo extraemos
                if key in schedule_map:
                    gen: Gen = schedule_map[key]
                    course: Course = gen.get_course()
                    professor: Professor = gen.get_professor()

                    assignment_dto: AssignmentDTO = AssignmentDTO(
                        course=CourseResponseDTO.from_course(course),
                        professor_name=professor.name,
                        professor_dpi=professor.dpi,
                        is_empty=False
                    )
                else:
                    assignment_dto: AssignmentDTO = AssignmentDTO(
                        course=None,
                        professor_name=None,
                        professor_dpi=None,
                        is_empty=True
                    )
                assignments_for_period.append(assignment_dto)

            row_dto: ScheduleRowDTO = ScheduleRowDTO(
                period=period,
                time_range=time_range,
                assignments=assignments_for_period
            )
            rows.append(row_dto)

        # retornamos el dto construido
        return ScheduleDTO(
            classrooms=classroom_dtos,
            rows=rows
        )

    def __get_period_map(self) -> Dict[Tuple[int, int], Gen]:
        # este mapa va a guardar todos los genes que pertenecen a un periodo y salon
        schedule_map: Dict[Tuple[int, int], Gen] = {}
        # recorremos todos los genes
        for gen in self.schedule.get_genes():
            # la llave sere el numero de periodo jutno con el id del salon
            key: Tuple[int, int] = (gen.get_period(), gen.get_classroom().id)

            # con la llave agregamos el salon
            schedule_map[key] = gen
        return schedule_map
