from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from courses.controllers.course_controller import router as courses_router
from professors.controllers.professor_controller import router as professors_router
from classrooms.controllers.classroom_controller import router as classrooms_router
from schedules.controller.schedule_controller import router as schedule_controller
from classrooms.models.classroom import Classroom
from professors.models.professor import Professor
from courses.models.course import Course
from db.database import Base, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # se permiten todos los origenes
    allow_methods=["*"],  # se permiten todos los metodos
    allow_headers=["*"],  # se permiten todos los headers
)

# incluimos todos los endpoints presentes en el router de cursos
app.include_router(courses_router)
# incluimos todos los endpoints presentes en el router de docentes
app.include_router(professors_router)
# incluimos todos los endpoints presentes en el router de clases
app.include_router(classrooms_router)

app.include_router(schedule_controller)

# esto inidica a sqlalchemy que cree todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return {"message": "Hello World"}
