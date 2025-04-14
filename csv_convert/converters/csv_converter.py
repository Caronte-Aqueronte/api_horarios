
import csv
from io import StringIO
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session


class CsvConverter:

    def __init__(self, file: UploadFile, db: Session):
        self.__file: UploadFile = file
        self.__db: Session = db

    async def _process_csv(self) -> csv.DictReader:
        # verificamos que el archivo sea un csv
        if not self.__file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=400, detail="El archivo debe ser un CSV.")

        content = await self.__file.read()  # llemos el archivo
        decoded = content.decode("utf-8")  # se decodifica el
        return csv.DictReader(StringIO(decoded))
