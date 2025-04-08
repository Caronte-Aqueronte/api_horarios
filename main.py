from fastapi import FastAPI
from courses.controllers.courses_controller import router as courses_router

from db.database import Base, engine

app = FastAPI()

# incluimos todos los routers prentes el router de cursos
app.include_router(courses_router)

# esto inidica a sqlalchemy que cree todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return {"message": "Hello World"}
