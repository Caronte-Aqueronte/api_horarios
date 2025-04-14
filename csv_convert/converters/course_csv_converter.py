import csv
import datetime
from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from courses.enums.course_type_enum import CourseTypeEnum
from courses.models.course import Course
from courses.services.course_service import CourseService
from csv_convert.converters.csv_converter import CsvConverter
from csv_convert.dto.import_response_dto import ImportResponseDTO


class CourseCsvConverter(CsvConverter):

    def __init__(self, file: UploadFile, db: Session):
        super().__init__(file, db)
        self.__course_service: CourseService = CourseService(db)

    async def convert_csv_to_professors(self) -> ImportResponseDTO:
        reader: csv.DictReader = await self._process_csv()
        warnings: List[str] = []  # aqui vamos a guardar todos los errores
        success: List[str] = []
        # recoreemos el reader y extraemos las columnas
        for index, row in enumerate(reader):
            try:
                # creamos una nueva ocurrencia del course en base a las columnas
                # aplicamos strip para que no hayan espacios en blanco
                course = Course(
                    name=row["nombre"].strip(),
                    code=row["codigo"].strip(),
                    career=row["carrera"].strip(),
                    semester=row["semestre"].strip(),
                    section=row["seccion"].strip(),
                    type=CourseTypeEnum.mandatory if row["tipo"].strip(
                    ) == "obligatorio" else CourseTypeEnum.elective
                )
                # mandamos a crear el curso
                self.__course_service.create_course(course)
                success.append(
                    f"Fila {index + 1}: Curso '{course.name}' (Código: {course.code}) guardado exitosamente."
                )

            except Exception as e:
                warnings.append(f"Fila {index + 1}: {str(e)}")

        return ImportResponseDTO(success=success, warnings=warnings)
