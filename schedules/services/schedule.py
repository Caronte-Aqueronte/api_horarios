
from typing import List

from classrooms.models.classroom import Classroom
from courses.enums.course_type_enum import CourseTypeEnum
from courses.models.course import Course
from professors.models.professor import Professor
from schedules.models.gen import Gen
from typing import Dict, Tuple


class Schedule:

    def __init__(self, genes: List[Gen]):
        self.__genes: List[Gen] = genes

        # va a guardar el valor de la aptitud dd cada uno de los genes
        self.__fitness = self.__fitness_function()

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
               or gen.get_start_time() > gen.get_professor().entry_time):

                conflicts = conflicts + 1

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
                    bonuses = bonuses + 1

        return conflicts + bonuses

    def reaload_fitness(self):
        self.__fitness = self.__fitness_function()

    def get_fitness(self) -> int:
        return self.__fitness

    def get_genes(self) -> List[Gen]:
        return self.__genes
