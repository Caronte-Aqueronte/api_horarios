from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from classrooms.dtos.classroom_reponse_dto import ClassroomResponseDTO
from classrooms.dtos.save_classroom_request_dto import SaveClassroomRequestDTO
from classrooms.models.classroom import Classroom
from classrooms.services.classroom_service import ClassroomService
from db.dependency import get_db


# le da una ruta generar a todos los endpoints de este controlador
router = APIRouter(
    prefix="/classrooms",
    tags=["Classrooms"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=List[ClassroomResponseDTO])
def get_classrooms(db: db_dependency) -> List[ClassroomResponseDTO]:
    # creamos una instancia del servicio con la sesión de la bd
    service = ClassroomService(db)

    # obtenemos todos los cursos usando el servicio
    classrooms: List[ClassroomResponseDTO] = service.get_all_classrooms()

    # convertimos los modelos a dto de respuesta y los retornamos
    return [ClassroomResponseDTO.model_validate(classroom) for classroom in classrooms]


@router.post("/", response_model=ClassroomResponseDTO, status_code=status.HTTP_201_CREATED)
def create_classroom(new_classroom: SaveClassroomRequestDTO, db: db_dependency) -> ClassroomResponseDTO:
    # creamos una instancia del servicio con la sesión de la bd
    service = ClassroomService(db)

    # convertimos el dto a modelo de base de datos
    classroom = Classroom(**new_classroom.model_dump())

    # guardamos el curso usando el servicio
    saved_classroom: Classroom = service.create_classroom(classroom)

    # convertimos el modelo guardado a dto de respuesta y lo retornamos
    return ClassroomResponseDTO.model_validate(saved_classroom)


@router.patch("/{classroom_id}", response_model=ClassroomResponseDTO)
def edit_classroom(classroom_id: int, response: SaveClassroomRequestDTO, db: db_dependency) -> ClassroomResponseDTO:
    # creamos una instancia del servicio con la sesión de la bd
    service = ClassroomService(db)

    # convertimos el dto a modelo de base de datos
    classroom = Classroom(**response.model_dump())

    # editamos el curso usando el servicio
    response: Classroom = service.update_classroom(
        classroom_id, classroom)

    # convertimos el modelo editado a dto de respuesta y lo retornamos
    return ClassroomResponseDTO.model_validate(response)


@router.get("/{classroom_id}", response_model=ClassroomResponseDTO)
def get_course(classroom_id: int, db: db_dependency) -> ClassroomResponseDTO:
    # creamos una instancia del servicio con la sesión de la bd
    service = ClassroomService(db)

    # traemos el curso por su id
    response: Classroom = service.get_classroom_by_id(classroom_id)

    # convertimos el modelo  a dto de respuesta y lo retornamos
    return ClassroomResponseDTO.model_validate(response)
