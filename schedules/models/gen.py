from datetime import time
from typing import Dict

from sqlalchemy import Tuple
from classrooms.models.classroom import Classroom
from courses.models.course import Course
from professors.models.professor import Professor


class Gen():

    def __init__(self, classroom: Classroom, course: Course, professor: Professor,
                 period: int):
        self.__classroom: Classroom = classroom
        self.__course: Course = course
        self.__professor: Professor = professor
        # va del 1 al 9 indicando el indice del periodo del tiempo en el que
        # la asignacion del curso ocupa en un horario de 13:40 a 21:10
        self.__period: int = period

        # se calculan en funcion del periodo
        self.__start_time: time = None
        self.__end_time: time = None
        # calculamos las horas en funcion del horario
        self.__calculate_start_and_end_time()

    def get_classroom(self) -> Classroom:
        return self.__classroom

    def set_classroom(self, classroom: Classroom):
        self.__classroom = classroom

    def get_course(self) -> Course:
        return self.__course

    def set_course(self, course: Course):
        self.__course = course

    def get_professor(self) -> Professor:
        return self.__professor

    def set_professor(self, professor: Professor):
        self.__professor = professor

    def get_period(self) -> int:
        return self.__period

    def set_period(self, period: int):
        self.__period = period
        # calculamos las horas en funcion del horario
        self.__calculate_start_and_end_time()

    def get_start_time(self) -> time:
        return self.__start_time

    def get_end_time(self) -> time:
        return self.__end_time

    def __calculate_start_and_end_time(self):
        # esto es un diccionario que tiene como clave un numero que corresponde al numero de periodo
        # y en su valor las horas  de inicio y fin que representan ese periodo
        times_for_periods: Dict[int, Tuple[time, time]] = {
            1: Tuple(time(13, 40), time(14, 30)),
            2: Tuple(time(14, 30), time(15, 20)),
            3: Tuple(time(15, 20), time(16, 10)),
            4: Tuple(time(16, 10), time(17, 00)),
            5: Tuple(time(17, 00), time(17, 50)),
            6: Tuple(time(17, 50), time(18, 40)),
            7: Tuple(time(18, 40), time(19, 30)),
            8: Tuple(time(19, 30), time(20, 20)),
            9: Tuple(time(20, 20), time(21, 10))
        }

        # mandamos a traer los tiempos segun la clave en el diccionario
        self.__start_time, self.__end_time = times_for_periods[self.__period]
