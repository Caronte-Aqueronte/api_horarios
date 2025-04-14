
from typing import List

from classrooms.models.classroom import Classroom
from courses.enums.course_type_enum import CourseTypeEnum
from courses.models.course import Course
from schedules.models.gen import Gen
from typing import Dict, Tuple


class Schedule:

    def __init__(self, genes: List[Gen],  manual_course_classrooms_assignments: Dict[Course, Classroom]):
        self.__genes: List[Gen] = genes
        self.__manual_course_classrooms_assignments: Dict[Course,
                                                          Classroom] = manual_course_classrooms_assignments

        # va a guardar los confictos generados en la funcion fitness, cada que se ejecute el fitness este
        # valor va a setearse y no a acumularse, representando asi
        self.__conficts: int = 0

        # va a guardar el valor de la aptitud dd cada uno de los genes
        self.__fitness: int = self.__fitness_function()

    def __fitness_function(self) -> int:
        # medira el numero de conflictos que tienen un conjutno de genes
        conflicts: int = 0
        # esta variable guardara el numero de bonificaciones de un conjunto de genes
        bonuses: int = 0
        # guarda si una clase ya esta asignada en un mismo periodo
        classroom_occupancy: Dict[Tuple[int, str], bool] = {}

        # guarda si ya fue asignado un profesor en el mismo periodo
        professor_occupancy: Dict[Tuple[int, str], bool] = {}

        # guarda si ya existe una asignacion de un curso de mismo semestre y carrera en un mismo periodo
        semester_occupancy: Dict[Tuple[int, int, str], bool] = {}

        # guarda todos periodos asignados a cursos obligatorios
        # de la misma carr
        courses_per_semester: Dict[Tuple[int, str], List] = {}

        for gen in self.__genes:
            # para identificar la ocupacion de este salon debemos guardar su id y en num de periodo esta ocupado
            classroom_key: Tuple[int, str] = (
                gen.get_period(), gen.get_classroom().id)

            # para identificar la ocupacion de un docente debemos guardar su id y el num de periodo en el que esta ocupado
            professor_key:  Tuple[int, str] = (
                gen.get_period(), gen.get_professor().id)

            semester_key: Tuple[int, int, str] = (gen.get_period(), gen.get_course(
            ).semester, gen.get_course().career)

            # si existe y es true entonces el salon esta ocupado
            if classroom_key in classroom_occupancy:
                conflicts = conflicts + 1
            else:
                # si no existe entonces no sumamos conflico y guardamos un true la posicion de
                # la key identificando que esa asignacion ya ocurrio
                classroom_occupancy[classroom_key] = True

            # si existe y es true entonces el profesor ya esta ocupado en el periodo
            if professor_key in professor_occupancy:
                conflicts = conflicts + 1
            else:
                professor_occupancy[professor_key] = True

            # debemos validar si el curso esta fuera del horario del docente
            if (gen.get_start_time() < gen.get_professor().entry_time
               or gen.get_start_time() >= gen.get_professor().exit_time
               or gen.get_end_time() > gen.get_professor().exit_time):
                conflicts = conflicts + 1

            # debemos penalizar que el curso del gen no este presente en los cursos que el docente puede
            if (gen.get_course() not in gen.get_professor().courses):
                conflicts = conflicts + 1

            # si el curso del gen esta presente en las asignaciones manuales a un classroom
            # pero el classroom del gen no es el que deberia ser entonces es un conflicto
            if (gen.get_course() in self.__manual_course_classrooms_assignments):
                if (gen.get_classroom() != self.__manual_course_classrooms_assignments.get(gen.get_course())):
                    conflicts = conflicts + 10

            # si el tipo de curso es obligatorio, existe y es tre entonces un curso del mismo semestre y carrera
            # ya fue asignado en el mismo periodo
            if gen.get_course().type == CourseTypeEnum.mandatory:
                if semester_key in semester_occupancy:
                    conflicts = conflicts + 1
                else:
                    semester_occupancy[semester_key] = True

                continuity_key: Tuple[int, str] = (gen.get_course().semester, gen.get_course(
                ).career)

                # si la clave ya existe, se le añade el período, indicando que un curso
                # del mismo semestre y carrera ya fue asignado en ese período.
                courses_per_semester.setdefault(
                    continuity_key, []).append(gen.get_period())

        # en esta seccion premiamos las bonificaciones que basicamente solo es la continuidad

        # recorremos los valores del diccionario, que son listas de períodos asignados
        for periods in courses_per_semester.values():
            # ordenamos los períodos para verificar si son continuos
            periods.sort()
            # recorremos los períodos comparando cada uno con el anterior
            for i in range(1, len(periods)):
                # Si dos cursos están asignados al mismo período, se considera una bonificación
                if periods[i] - periods[i - 1] == 1:
                    bonuses = bonuses + 3
        self.__conficts = conflicts
        return bonuses - conflicts

    def reaload_fitness(self):
        self.__fitness = self.__fitness_function()

    def get_fitness(self) -> int:
        return self.__fitness

    def get_conflicts(self) -> int:
        return self.__conficts

    def get_genes(self) -> List[Gen]:
        return self.__genes
