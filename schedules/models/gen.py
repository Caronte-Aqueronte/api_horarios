from datetime import time
from typing import Dict

from sqlalchemy import Tuple
from classrooms.models.classroom import Classroom
from courses.models.course import Course
from professors.models.professor import Professor
from schedules.utils.period_util import PeriodUtil


class Gen():

    def __init__(self, classroom: Classroom, course: Course, professor: Professor,
                 period: int):
        self.__classroom: Classroom = classroom
        self.__course: Course = course
        self.__professor: Professor = professor
        # se calculan en funcion del periodo
        self.__start_time: time = None
        self.__end_time: time = None
        self.__period_utils: PeriodUtil = PeriodUtil()

        self.set_period(period)

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
        self.__start_time, self.__end_time = self.__period_utils.get_start_and_end_time_for_period(
            self.__period)

    def get_start_time(self) -> time:
        return self.__start_time

    def get_end_time(self) -> time:
        return self.__end_time
