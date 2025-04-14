from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from csv_convert.converters.classtoom_csv_converter import ClassroomCsvConverter
from csv_convert.converters.course_csv_converter import CourseCsvConverter
from csv_convert.converters.professor_course_converter import ProfessorCourseConverter
from csv_convert.converters.professor_csv_converter import ProfessorCsvConverter
from csv_convert.dto.import_response_dto import ImportResponseDTO
from db.dependency import get_db

router = APIRouter(
    prefix="/csv",
    tags=["CSV"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/professors")
async def create_professors(file: UploadFile, db: db_dependency):
    converter: ProfessorCsvConverter = ProfessorCsvConverter(file, db)
    messagges: ImportResponseDTO = await converter.convert_csv_to_professors()
    return messagges


@router.post("/courses")
async def create_courses(file: UploadFile, db: db_dependency):
    converter: CourseCsvConverter = CourseCsvConverter(file, db)
    messagges: ImportResponseDTO = await converter.convert_csv_to_professors()
    return messagges


@router.post("/assigments")
async def create_assgiments(file: UploadFile, db: db_dependency):
    converter: ProfessorCourseConverter = ProfessorCourseConverter(file, db)
    messagges: ImportResponseDTO = await converter.convert_csv_to_professors()
    return messagges


@router.post("/classrooms")
async def create_assgiments(file: UploadFile, db: db_dependency):
    converter: ClassroomCsvConverter = ClassroomCsvConverter(file, db)
    messagges: ImportResponseDTO = await converter.convert_csv_to_professors()
    return messagges
