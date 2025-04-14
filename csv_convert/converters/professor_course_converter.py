import csv
import datetime
from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from csv_convert.converters.csv_converter import CsvConverter
from csv_convert.dto.import_response_dto import ImportResponseDTO
from professors.models.professor import Professor
from shared.services.professor_course_service import ProfessorCourseService


class ProfessorCourseConverter(CsvConverter):

    def __init__(self, file: UploadFile, db: Session):
        super().__init__(file, db)
        self.__professor_course_service: ProfessorCourseService = ProfessorCourseService(
            db)

    async def convert_csv_to_professors(self) -> ImportResponseDTO:
        reader: csv.DictReader = await self._process_csv()
        warnings: List[str] = []  # aqui vamos a guardar todos los errores
        success: List[str] = []
        # recoreemos el reader y extraemos las columnas
        for index, row in enumerate(reader):

            try:
                # obtenemos los datos para mandar a crear la asignacion
                professor_personal_id: str = row["registro_de_personal"].strip(
                )
                course_code: str = row["codigo_de_curso"].strip()

                # mandamos a crear al profesor
                self.__professor_course_service.create_assigment(
                    professor_personal_id, course_code)
                success.append(
                    f"Fila {index + 1}: Asignación exitosa del curso '{course_code}' al docente con  '{professor_personal_id}'."
                )
            except Exception as e:
                warnings.append(f"Fila {index + 1}: {str(e)}")

        return ImportResponseDTO(success=success, warnings=warnings)
