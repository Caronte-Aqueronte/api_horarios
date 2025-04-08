from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from courses.dto.course_response_dto import CourseResponseDTO
from courses.models.course import Course
from courses. services.course_service import CourseService
from courses.dto.save_course_request_dto import SaveCourseRequestDTO
from db.dependency import get_db

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=List[CourseResponseDTO])
def get_courses(db: db_dependency) -> List[CourseResponseDTO]:
    # creamos una instancia del servicio con la sesión de la bd
    service = CourseService(db)

    # obtenemos todos los cursos usando el servicio
    courses: List[Course] = service.get_all_courses()

    # convertimos los modelos a dto de respuesta y los retornamos
    return [CourseResponseDTO.from_course(course) for course in courses]


@router.post("/", response_model=CourseResponseDTO, status_code=status.HTTP_201_CREATED)
def create_course(new_course: SaveCourseRequestDTO, db: db_dependency) -> CourseResponseDTO:
    # creamos una instancia del servicio con la sesión de la bd
    service = CourseService(db)

    # convertimos el dto a modelo de base de datos
    course = Course(**new_course.model_dump())

    # guardamos el curso usando el servicio
    response: Course = service.create_course(course)

    # convertimos el modelo guardado a dto de respuesta y lo retornamos
    return CourseResponseDTO.from_course(response)


@router.patch("/{course_id}", response_model=CourseResponseDTO)
def edit_course(course_id: int, updated_course: SaveCourseRequestDTO, db: db_dependency) -> CourseResponseDTO:
    # creamos una instancia del servicio con la sesión de la bd
    service = CourseService(db)

    # convertimos el dto a modelo de base de datos
    course = Course(**updated_course.model_dump())

    # editamos el curso usando el servicio
    response: Course = service.update_course(course_id, course)

    # convertimos el modelo editado a dto de respuesta y lo retornamos
    return CourseResponseDTO.from_course(response)


@router.get("/{course_id}", response_model=CourseResponseDTO)
def get_course(course_id: int, db: db_dependency) -> CourseResponseDTO:
    # creamos una instancia del servicio con la sesión de la bd
    service = CourseService(db)

    # traemos el curso por su id
    course: Course = service.get_course_by_id(course_id)

    # convertimos el modelo  a dto de respuesta y lo retornamos
    return CourseResponseDTO.from_course(course)
