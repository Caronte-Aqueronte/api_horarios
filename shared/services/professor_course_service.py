from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from courses.models.course import Course
from professors.models.professor import Professor
from professors.services.professor_service import ProfessorService
from shared.models.professor_course import ProfessorCourse


class ProfessorCourseService:

    def __init__(self, db: Session):
        self.__db: Session = db
        self.__professor_service: ProfessorService = ProfessorService(db)

    def create_assigment(self, personal_id: str, course_code: str) -> ProfessorCourse:
        # mandamos a buscar el docente por su codigo de personal
        professor: Professor = self.__professor_service.get_professor_personal_id(
            personal_id)
        # mandamos a buscar el cuso por su codigo
        course: Course = self.__professor_service.get_course_service(
        ).get_course_by_code(course_code)

        # verificamos que la asignacion no exista, si existe lanzamos error

        if (self.exist_assigment(professor.id, course.id)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"Ya existe un registro del docente {professor.id}  con el curso {course.id}")

        professor_course = ProfessorCourse(
            professor_id=professor.id,
            course_id=course.id
        )

        # guardamos
        self.__db.add(professor_course)
        self.__db.commit()
        self.__db.refresh(professor_course)

        return professor_course

    def exist_assigment(self, professor_id: int, course_id: int) -> bool:
        course: ProfessorCourse = self.__db.query(ProfessorCourse).filter(
            ProfessorCourse.professor_id == professor_id,
            ProfessorCourse.course_id == course_id,).first()
        # esto devuleve un boleano, si existe el la asignacion devuelve true, si no false
        return course is not None
