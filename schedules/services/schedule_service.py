from typing import Dict, List, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from classrooms.models.classroom import Classroom
from classrooms.services.classroom_service import ClassroomService
from courses.models.course import Course
from courses.services.course_service import CourseService
from pdf.services.schedule_pdf_generator import SchedulePdfGenerator
from professors.models.professor import Professor
from professors.services.professor_service import ProfessorService
from schedules.dtos.schedule_dto import ScheduleDTO, ScheduleDTOBuilder
from schedules.ga.genetic_algorithm import GeneticAlgorithm
from schedules.ga.schedule import Schedule


class ScheduleService:
    def __init__(self, db: Session):
        self.__db = db
        self.__professor_service: ProfessorService = ProfessorService(db)
        self.__classroom_service: ClassroomService = ClassroomService(db)
        self.__course_service: CourseService = CourseService(db)

        pass

    def generate_schedule(self, population_size: int, max_generations: int, courses_availables_ids: List[int],
                          professors_availables_ids: List[int],
                          manual_course_classrooms_assignments: Dict[int, int],
                          target_fitness: int

                          ) -> ScheduleDTO:
        # los todos los salones seran evaluados
        classrooms: List[Classroom] = self.__classroom_service.get_all_classrooms()

        if (len(classrooms) == 0):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="No hay salones ingresados en el sistema.")

        courses: List[Course] = self.__course_service.get_courses_by_ids(
            courses_availables_ids)

        # si la lista de cursos esta vacia entonces mandamos a trer todos los cursos
        if len(courses) == 0:
            courses = self.__course_service.get_all_courses()

        professors: List[Professor] = self.__professor_service.get_professors_by_ids(
            professors_availables_ids)

        # si la lista de profesores viene vacia entonces mandamos a traer todos los profesores
        if len(professors) == 0:
            professors = self.__professor_service.get_all_professors()

        # construimos las asignaciones manuales de los cursos a salones
        manual_assignments_dict: Dict[Course, Classroom] = {}

        # vamor recorriendo cada uno de los ids que trae el diccionario de asignaciones manuales
        for course_id, classroom_id in manual_course_classrooms_assignments.items():
            # usamos cada uno de los ids para buscar los objetos, esto lanza excepcion si es que alguno no se encontro
            course = self.__course_service.get_course_by_id(course_id)
            classroom = self.__classroom_service.get_classroom_by_id(
                classroom_id)
            manual_assignments_dict[course] = classroom

        # cremos la clase que se enc
        genetic_algorithm: GeneticAlgorithm = GeneticAlgorithm(
            population_size,
            max_generations,
            courses,
            classrooms,
            professors,
            manual_assignments_dict,
            target_fitness)

        # mandos a crear el horario
        schedule: Schedule = genetic_algorithm.run()

        # construimos el dto
        dto_builder: ScheduleDTOBuilder = ScheduleDTOBuilder(
            schedule, classrooms
        )

        response: ScheduleDTO = dto_builder.build()

        return response

        # # ahora solo demos mandar a imprimir ese horario
        # schedule_pdf_generator: SchedulePdfGenerator = SchedulePdfGenerator(
        #     schedule, classrooms)

        # return schedule_pdf_generator.generate_schedule_pdf()
