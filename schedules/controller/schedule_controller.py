
from typing import Annotated, List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from courses.dto.course_response_dto import CourseResponseDTO
from courses.models.course import Course
from courses. services.course_service import CourseService
from courses.dto.save_course_request_dto import SaveCourseRequestDTO
from db.dependency import get_db
from schedules.dtos.generate_schedule_request_dto import GenerateScheduleRequestDTO
from schedules.dtos.schedule_dto import ScheduleDTO
from schedules.services.schedule_service import ScheduleService

router = APIRouter(
    prefix="/schedule",
    tags=["Schedule"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=ScheduleDTO)
def generate_schedule(generate_schedule_request_dto: GenerateScheduleRequestDTO, db: db_dependency) -> ScheduleDTO:
    print(generate_schedule_request_dto)
    # creamos una instancia del servicio con la sesión de la bd
    service = ScheduleService(db)

    dto = service.generate_schedule(
        generate_schedule_request_dto.population_size,
        generate_schedule_request_dto.max_generations,
        generate_schedule_request_dto.courses_availables_ids,
        generate_schedule_request_dto.professors_availables_ids,
        generate_schedule_request_dto.manual_course_classrooms_assignments,
        generate_schedule_request_dto.target_fitness
    )

    return dto


@router.post("/export")
def export_schedule(schedule_dto: ScheduleDTO, db: db_dependency):
    # creamos una instancia del servicio con la sesión de la bd
    service = ScheduleService(db)

    pdf_bytes = service.generate_schedule_pdf(
        schedule_dto
    )
    # retonrnamos los bytes con el media tipe para que se habra en el navegador
    return Response(content=pdf_bytes, media_type="application/pdf")
