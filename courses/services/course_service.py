# courses/course_service.py
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from courses.models.course import Course


class CourseService:
    # el constructor siempre rcibira la sesion de la bd
    def __init__(self, db: Session):
        self.__db: Session = db

    def get_all_courses(self) -> List[Course]:
        return self.__db.query(Course).all()

    def create_course(self, course: Course) -> Course:
        # verificamos si ya existe un curso con el mismo codigo, esto puede lanzar una excepcion si ya existe
        if (self.exist_course_by_code(course.code)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Ya existe un curso con el codigo especificado.")

        # con add creamos el curso en la bd
        self.__db.add(course)

        # confimarmos el cambio en la bd
        self.__db.commit()

        # recargamos el modelo para tener la version mas actualizada
        self.__db.refresh(course)
        return course

    def update_course(self, course_id: int, updated_data: Course) -> Course:

        # mandamos a traer el curso que se desa actualizar, esto puede lanzar una excepcion si no ecxiste
        existing_course: Course = self.get_course_by_id(course_id)

        # verificamos si ya existe otro curso con el mismo codigo, debemos verificar que el id no sea el mismo que el del curso que estamos actualizando
        if (self.exist_course_by_code_and_id_is_not(updated_data.code, course_id)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Ya existe un curso con el codigo especificado.")

        # aqui camos a usar los datos que vienen del cliente y actualizamos con ellos los datos de la bd
        existing_course.name = updated_data.name
        existing_course.code = updated_data.code
        existing_course.career = updated_data.career
        existing_course.semester = updated_data.semester
        existing_course.section = updated_data.section
        existing_course.type = updated_data.type

        # realizamos el commit en la bd
        self.__db.commit()

        # recargamos el modelo para tener la version mas actualizada
        self.__db.refresh(existing_course)

        return existing_course

    def get_course_by_id(self, course_id: int) -> Course:
        course: Course = self.__db.query(Course).filter(
            Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")
        return course

    def exist_course_by_code(self, course_code: str) -> bool:
        course: Course = self.__db.query(Course).filter(
            Course.code == course_code).first()
        # esto devuleve un boleano, si existe el curso devuelve true, si no false
        return course is not None

    def exist_course_by_code_and_id_is_not(self, course_code: str, course_id: int) -> bool:
        course: Course = self.__db.query(Course).filter(
            Course.code == course_code,
            Course.id != course_id).first()
        # esto devuleve un boleano, si existe el curso devuelve true, si no false
        return course is not None

    def get_courses_by_ids(self, ids: List[int]) -> List[Course]:
        # cargamos los cursos desde la base de datos usando la listam
        return self.__db.query(Course).filter(Course.id.in_(ids)).all()
