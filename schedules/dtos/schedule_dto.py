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
    professor_personal_id: str | None
    is_empty: bool = False


class ScheduleRowDTO(BaseModel):
    period: int
    time_range: str
    assignments: List[AssignmentDTO]


class ScheduleDTO(BaseModel):
    classrooms: List[ClassroomResponseDTO]
    rows: List[ScheduleRowDTO]


class ScheduleDTOWithReports(BaseModel):
    total_iterations: int
    history_confilcts: Dict[str, int]
    history_fitness: Dict[str, int]
    memory_usage: float
    total_time: float
    semester_continuity_percentages: Dict[str, float]

    classrooms: List[ClassroomResponseDTO]
    rows: List[ScheduleRowDTO]


class ScheduleDTOBuilder:

    def __init__(
        self,
        schedule: Schedule,
        classrooms: List[Classroom],
        total_iterations: int,
        history_conflicts: Dict[str, int],
        history_fitness: Dict[str, int],
        memory_usage: float,
        total_time: float,
        semester_continuity_percentages: Dict[Tuple[int, str], float],
    ):
        self.__schedule: Schedule = schedule
        self.__classrooms: List[Classroom] = classrooms
        self.__period_util = PeriodUtil()

        self.__total_iterations: int = total_iterations
        self.__history_conflicts: Dict[str, int] = history_conflicts
        self.__history_fitness: Dict[str, int] = history_fitness
        self.__memory_usage: float = memory_usage
        self.__total_time: float = total_time
        self.__semester_continuity_percentages: Dict[str,
                                                     float] = semester_continuity_percentages

    def build(self) -> ScheduleDTOWithReports:
        # convertimos los salones a dtos
        classroom_dtos: List[ClassroomResponseDTO] = [ClassroomResponseDTO.from_classroom(
            classroom) for classroom in self.__classrooms]

        # mandamos a crear el mapa para faciliar el saber las asignaciones
        schedule_map: Dict[Tuple[int, int], Gen] = self.__get_period_map()

        # construimos las filas con el dto preciso
        rows: List[ScheduleRowDTO] = []
        for period in range(1, 10):
            period_start, period_end = self.__period_util.get_start_and_end_time_for_period(
                period)
            time_range: str = f"{period_start.strftime('%I:%M %p')} - {period_end.strftime('%I:%M %p')}"

            # para cada salón, creamos una asignacion
            assignments_for_period: List[AssignmentDTO] = []

            for classroom in self.__classrooms:
                key = (period, classroom.id)

                # si la key que creamos existe entonces hay una asignacion en la clase en el periodo, lo extraemos
                if key in schedule_map:
                    gen: Gen = schedule_map[key]
                    course: Course = gen.get_course()
                    professor: Professor = gen.get_professor()

                    assignment_dto: AssignmentDTO = AssignmentDTO(
                        course=CourseResponseDTO.from_course(course),
                        professor_name=professor.name,
                        professor_personal_id=professor.personal_id,
                        is_empty=False
                    )
                else:
                    assignment_dto: AssignmentDTO = AssignmentDTO(
                        course=None,
                        professor_name=None,
                        professor_personal_id=None,
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
        return ScheduleDTOWithReports(
            classrooms=classroom_dtos,
            rows=rows,
            history_confilcts=self.__history_conflicts,
            history_fitness=self.__history_fitness,
            memory_usage=self.__memory_usage,
            semester_continuity_percentages=self.__semester_continuity_percentages,
            total_iterations=self.__total_iterations,
            total_time=self.__total_time
        )

    def __get_period_map(self) -> Dict[Tuple[int, int], Gen]:
        # este mapa va a guardar todos los genes que pertenecen a un periodo y salon
        schedule_map: Dict[Tuple[int, int], Gen] = {}
        # recorremos todos los genes
        for gen in self.__schedule.get_genes():
            # la llave sere el numero de periodo jutno con el id del salon
            key: Tuple[int, int] = (gen.get_period(), gen.get_classroom().id)

            # con la llave agregamos el salon
            schedule_map[key] = gen
        return schedule_map
