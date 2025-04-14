import csv
import datetime
from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from csv_convert.converters.csv_converter import CsvConverter
from csv_convert.dto.import_response_dto import ImportResponseDTO
from professors.models.professor import Professor
from professors.services.professor_service import ProfessorService


class ProfessorCsvConverter(CsvConverter):

    def __init__(self, file: UploadFile, db: Session):
        super().__init__(file, db)
        self.__professor_service: ProfessorService = ProfessorService(db)

    async def convert_csv_to_professors(self) -> ImportResponseDTO:
        reader: csv.DictReader = await self._process_csv()
        warnings: List[str] = []  # aqui vamos a guardar todos los errores
        success: List[str] = []
        # recoreemos el reader y extraemos las columnas
        for index, row in enumerate(reader):

            try:
                # creamos una nueva ocurrencia del professor en base a las columnas
                # aplicamos strip para que no hayan espacios en blanco
                profesor = Professor(
                    name=row["nombre"].strip(),
                    personal_id=row["registro_de_personal"].strip(),
                    entry_time=datetime.datetime.strptime(
                        row["hora_entrada"].strip(), "%H:%M").time(),
                    exit_time=datetime.datetime.strptime(
                        row["hora_salida"].strip(), "%H:%M").time()
                )
                # mandamos a crear al docente
                self.__professor_service.create_professor(profesor, [])
                success.append(
                    f"Fila {index + 1}: Docente '{profesor.name}' (ID: {profesor.personal_id}) guardado exitosamente."
                )
            except Exception as e:
                warnings.append(f"Fila {index + 1}: {str(e)}")

        return ImportResponseDTO(success=success, warnings=warnings)
