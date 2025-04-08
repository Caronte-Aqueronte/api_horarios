from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.get("/lib/{xd}")
def index(xd: int):
    return {"message": xd}
