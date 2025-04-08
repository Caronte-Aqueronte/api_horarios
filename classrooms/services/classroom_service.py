from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from classrooms.models.classroom import Classroom


class ClassroomService:

    def __init__(self, db: Session):
        self.__db = db

    def get_all_classrooms(self) -> List[Classroom]:
        classrooms = self.__db.query(Classroom).all()
        return classrooms

    def create_classroom(self, classroom: Classroom) -> Classroom:
        # verificamos si ya existe un salor con el mismo nombre, esto puede lanzar una excepcion si ya existe
        if (self.exists_classroom_by_name(classroom.name)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Ya existe un salon con el nombre especificado.")
        # con add creamos el salon en la bd
        self.__db.add(classroom)
        # confimarmos el cambio en la bd
        self.__db.commit()
        # recargamos el modelo para tener la version mas actualizada
        self.__db.refresh(classroom)
        return classroom

    def update_classroom(self, classroom_id: int, updated_data: Classroom) -> Classroom:
        # mandamos a traer el salon que se desa actualizar, esto puede lanzar una excepcion si no existe
        existing_classroom: Classroom = self.get_classroom_by_id(classroom_id)

        # verificamos si ya existe otro salon con el mismo nanme, debemos verificar que el id no sea el mismo que el del salon que estamos actualizando
        if (self.exists_classroom_by_name_and_id_is_not(updated_data.name, classroom_id)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Ya existe un salon con el nombre especificado.")

        # aqui camos a usar los datos que vienen del cliente y actualizamos con ellos los datos de la bd
        existing_classroom.name = updated_data.name
        # realizamos el commit en la bd
        self.__db.commit()
        # recargamos el modelo para tener la version mas actualizada
        self.__db.refresh(existing_classroom)

        return existing_classroom

    def get_classroom_by_id(self, classroom_id: int) -> Classroom:
        # mandamos a bscar el salon filtrado por id
        classroom = self.__db.query(Classroom).filter(
            Classroom.id == classroom_id).first()
        # si el salon no esta presente entonces lanzamos una excepcion
        if not classroom:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Salon no encontrado")
        return classroom

    def exists_classroom_by_name(self, classroom_name: str) -> bool:
        # se filtran los salones por el nombre
        classroom = self.__db.query(Classroom).filter(
            Classroom.name == classroom_name).first()
        # esto devuleve un boleano, si existe el salon con el nombre devuelve true, si no false
        return classroom is not None

    def exists_classroom_by_name_and_id_is_not(self, classroom_name: str, classroom_id: int) -> bool:
        professor = self.__db.query(Classroom).filter(
            Classroom.name == classroom_name,
            Classroom.id != classroom_id).first()
        # esto devuleve un boleano, si existe el salon con el nombre devuelve true, si no false
        return professor is not None
