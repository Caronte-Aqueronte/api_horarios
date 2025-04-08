from typing import Generator
from db.database import SessionLocal
from sqlalchemy.orm import Session

# esto btiene una sesion de bd que puede ser inyectada por todo aqul que la necesita, siempre es cerrada al final


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
