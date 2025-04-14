from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from courses.services.course_service import CourseService
from professors.models.professor import Professor


class ProfessorService:

    def __init__(self, db: Session):
        self.__db: Session = db
        self.__course_service: CourseService = CourseService(db)

    def get_course_service(self) -> CourseService:
        return self.__course_service

    def get_all_professors(self) -> List[Professor]:
        professors: List[Professor] = self.__db.query(Professor).all()
        return professors

    def create_professor(self, professor: Professor, courses_ids: List[int]) -> Professor:
        # verificamos si ya existe un docente con el mismo personal_id, esto puede lanzar una excepcion si ya existe
        if (self.exists_professor_personal_id(professor.personal_id)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Ya existe un docente con registro de personal especificado.")
        # mandamos a treaer todos los cursos de las selecciones
        exisiting_courses = self.__course_service.get_courses_by_ids(
            courses_ids)

        # le asignamos los cursos que se indicaron
        professor.courses = exisiting_courses
        # con add creamos el docente en la bd
        self.__db.add(professor)
        # confimarmos el cambio en la bd
        self.__db.commit()
        # recargamos el modelo para tener la version mas actualizada
        self.__db.refresh(professor)
        return professor

    def update_professor(self, professor_id: int, updated_data: Professor, courses_ids: List[int]) -> Professor:
        # mandamos a traer el el profesor que se desa actualizar, esto puede lanzar una excepcion si no existe
        existing_professor: Professor = self.get_professor_by_id(professor_id)

        # mandamos a treaer todos los cursos de las selecciones
        exisiting_courses = self.__course_service.get_courses_by_ids(
            courses_ids)

        # verificamos si ya existe otro docente con el mismo personal_id, debemos verificar que el id no sea el mismo que el del docente que estamos actualizando
        if (self.exists_professor_by_personal_id_and_id_is_not(updated_data.personal_id, professor_id)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Ya existe un docente con el registro de personal especificado.")

        # aqui camos a usar los datos que vienen del cliente y actualizamos con ellos los datos de la bd
        existing_professor.name = updated_data.name
        existing_professor.personal_id = updated_data.personal_id
        existing_professor.entry_time = updated_data.entry_time
        existing_professor.exit_time = updated_data.exit_time
        existing_professor.courses = exisiting_courses
        # realizamos el commit en la bd
        self.__db.commit()
        # recargamos el modelo para tener la version mas actualizada
        self.__db.refresh(existing_professor)

        return existing_professor

    def get_professor_by_id(self, professor_id: int) -> Professor:
        # mandamos a bscar el profesor filtrado por id
        professor: Professor = self.__db.query(Professor).filter(
            Professor.id == professor_id).first()
        # si el professor no esta presente entonces lanzamos una excepcion
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
        return professor

    def get_professor_personal_id(self, personal_id: str) -> Professor:
        # mandamos a bscar el profesor filtrado por codigo de personal
        professor: Professor = self.__db.query(Professor).filter(
            Professor.personal_id == personal_id).first()
        # si el professor no esta presente entonces lanzamos una excepcion
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontró un docente con el registro de personal {personal_id}.")
        return professor

    def exists_professor_personal_id(self, personal_id: str) -> bool:
        # se filtran los profesores por el personal_id
        professor: Professor = self.__db.query(Professor).filter(
            Professor.personal_id == personal_id).first()
        # esto devuleve un boleano, si existe el profesor con el personal_id devuelve true, si no false
        return professor is not None

    def exists_professor_by_personal_id_and_id_is_not(self, personal_id: str, professor_id: int) -> bool:
        professor: Professor = self.__db.query(Professor).filter(
            Professor.personal_id == personal_id,
            Professor.id != professor_id).first()
        # esto devuleve un boleano, si existe el profesor con el personal_id devuelve true, si no false
        return professor is not None

    def get_professors_by_ids(self, ids: List[int]) -> List[Professor]:
        # cargamos los cursos desde la base de datos usando la listam
        return self.__db.query(Professor).filter(Professor.id.in_(ids)).all()
