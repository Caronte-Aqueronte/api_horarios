import csv
import datetime
from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from classrooms.models.classroom import Classroom
from classrooms.services.classroom_service import ClassroomService
from csv_convert.converters.csv_converter import CsvConverter
from csv_convert.dto.import_response_dto import ImportResponseDTO
from professors.models.professor import Professor


class ClassroomCsvConverter(CsvConverter):

    def __init__(self, file: UploadFile, db: Session):
        super().__init__(file, db)
        self.__professor_service: ClassroomService = ClassroomService(db)

    async def convert_csv_to_professors(self) -> ImportResponseDTO:
        reader: csv.DictReader = await self._process_csv()
        warnings: List[str] = []  # aqui vamos a guardar todos los errores
        success: List[str] = []
        # recoreemos el reader y extraemos las columnas
        for index, row in enumerate(reader):

            try:
                # creamos una nueva ocurrencia del salon con las cols
                classroom = Classroom(
                    name=row["nombre"].strip()
                )
                # mandamos a crear al classroom
                self.__professor_service.create_classroom(classroom)
                success.append(
                    f"Fila {index + 1}: Salón '{classroom.name}' guardado exitosamente."
                )
            except Exception as e:
                warnings.append(f"Fila {index + 1}: {str(e)}")

        return ImportResponseDTO(success=success, warnings=warnings)
