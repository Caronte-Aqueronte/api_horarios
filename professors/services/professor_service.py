from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from professors.models.professor import Professor


class ProfessorService:

    def __init__(self, db: Session):
        self.__db = db

    def get_all_professors(self) -> List[Professor]:
        professors = self.__db.query(Professor).all()
        return professors

    def create_professor(self, professor: Professor) -> Professor:
        # verificamos si ya existe un docente con el mismo dpi, esto puede lanzar una excepcion si ya existe
        if (self.exists_professor_by_dpi(professor.dpi)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Ya existe un docente con el dpi especificado.")
        # con add creamos el docente en la bd
        self.__db.add(professor)
        # confimarmos el cambio en la bd
        self.__db.commit()
        # recargamos el modelo para tener la version mas actualizada
        self.__db.refresh(professor)
        return professor

    def update_professor(self, professor_id: int, updated_data: Professor) -> Professor:
        # mandamos a traer el el profesor que se desa actualizar, esto puede lanzar una excepcion si no existe
        existing_professor: Professor = self.get_professor_by_id(professor_id)

        # verificamos si ya existe otro docente con el mismo dpi, debemos verificar que el id no sea el mismo que el del docente que estamos actualizando
        if (self.exists_professor_by_dpi_and_id_is_not(updated_data.dpi, professor_id)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Ya existe un docente con el dpi especificado.")

        # aqui camos a usar los datos que vienen del cliente y actualizamos con ellos los datos de la bd
        existing_professor.name = updated_data.name
        existing_professor.dpi = updated_data.dpi
        existing_professor.entry_time = updated_data.entry_time
        existing_professor.exit_time = updated_data.exit_time
        # realizamos el commit en la bd
        self.__db.commit()
        # recargamos el modelo para tener la version mas actualizada
        self.__db.refresh(existing_professor)

        return existing_professor

    def get_professor_by_id(self, professor_id: int) -> Professor:
        # mandamos a bscar el profesor filtrado por id
        professor = self.__db.query(Professor).filter(
            Professor.id == professor_id).first()
        # si el professor no esta presente entonces lanzamos una excepcion
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
        return professor

    def exists_professor_by_dpi(self, professor_dpi: str) -> bool:
        # se filtran los profesores por el dpi
        professor = self.__db.query(Professor).filter(
            Professor.dpi == professor_dpi).first()
        # esto devuleve un boleano, si existe el profesor con el dpi devuelve true, si no false
        return professor is not None

    def exists_professor_by_dpi_and_id_is_not(self, professor_dpi: str, professor_id: int) -> bool:
        professor = self.__db.query(Professor).filter(
            Professor.dpi == professor_dpi,
            Professor.id != professor_id).first()
        # esto devuleve un boleano, si existe el profesor con el dpi devuelve true, si no false
        return professor is not None
