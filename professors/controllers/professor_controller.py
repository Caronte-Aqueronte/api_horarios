from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.dependency import get_db
from professors.dtos.professor_response_dto import ProfessorResponseDTO
from professors.dtos.save_professor_request_dto import SaveProfessorRequestDTO
from professors.services.professor_service import ProfessorService
from professors.models.professor import Professor
# le da una ruta generar a todos los endpoints de este controlador
router = APIRouter(
    prefix="/professors",
    tags=["Professors"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=List[ProfessorResponseDTO])
def get_professors(db: db_dependency) -> List[ProfessorResponseDTO]:
    # creamos una instancia del servicio con la sesión de la bd
    service = ProfessorService(db)

    # obtenemos todos los cursos usando el servicio
    professors: List[Professor] = service.get_all_professors()

    # convertimos los modelos a dto de respuesta y los retornamos
    return [ProfessorResponseDTO.model_validate(professor) for professor in professors]


@router.post("/", response_model=ProfessorResponseDTO, status_code=status.HTTP_201_CREATED)
def create_professor(new_professor: SaveProfessorRequestDTO, db: db_dependency) -> ProfessorResponseDTO:
    # creamos una instancia del servicio con la sesión de la bd
    service = ProfessorService(db)

    # convertimos el dto a modelo de base de datos
    professor_model = Professor(
        **new_professor.model_dump(exclude={"courses_ids"}))

    # guardamos el curso usando el servicio
    saved_professor: Professor = service.create_professor(
        professor_model, new_professor.courses_ids)

    # convertimos el modelo guardado a dto de respuesta y lo retornamos
    return ProfessorResponseDTO.model_validate(saved_professor)


@router.patch("/{professor_id}", response_model=ProfessorResponseDTO)
def edit_professor(professor_id: int, updated_professor: SaveProfessorRequestDTO, db: db_dependency) -> ProfessorResponseDTO:
    # creamos una instancia del servicio con la sesión de la bd
    service = ProfessorService(db)

    # convertimos el dto a modelo de base de datos
    professor = Professor(
        **updated_professor.model_dump(exclude={"courses_ids"}))

    # editamos el curso usando el servicio
    updated_professor: Professor = service.update_professor(
        professor_id, professor, updated_professor.courses_ids)

    # convertimos el modelo editado a dto de respuesta y lo retornamos
    return ProfessorResponseDTO.model_validate(updated_professor)


@router.get("/{professor_id}", response_model=ProfessorResponseDTO)
def get_professor(professor_id: int, db: db_dependency) -> ProfessorResponseDTO:
    # creamos una instancia del servicio con la sesión de la bd
    service = ProfessorService(db)

    # traemos el curso por su id
    professor: Professor = service.get_professor_by_id(professor_id)

    # convertimos el modelo  a dto de respuesta y lo retornamos
    return ProfessorResponseDTO.model_validate(professor)
