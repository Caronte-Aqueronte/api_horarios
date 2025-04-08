from fastapi import FastAPI
from classrooms.models.classroom import Classroom
from courses.controllers.course_controller import router as courses_router
from professors.controllers.professor_controller import router as professors_router
from classrooms.controllers.classroom_controller import router as classrooms_router
from professors.models.professor import Professor
from courses.models.course import Course
from db.database import Base, engine

app = FastAPI()

# incluimos todos los endpoints presentes en el router de cursos
app.include_router(courses_router)
# incluimos todos los endpoints presentes en el router de docentes
app.include_router(professors_router)
# incluimos todos los endpoints presentes en el router de clases
app.include_router(classrooms_router)

# esto inidica a sqlalchemy que cree todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return {"message": "Hello World"}
