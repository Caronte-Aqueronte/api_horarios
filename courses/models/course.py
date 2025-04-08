import enum
from pydantic import BaseModel
from sqlalchemy import Column, Enum, Integer, String

from courses.enums.course_type_enum import CourseTypeEnum
from db.database import Base

"""_summary_:
Este modelo rerpesenta la tabla que contiene el listado de cursos diponlibles en el sistema
"""


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), nullable=False, unique=True)
    career = Column(String(100), nullable=False)
    semester = Column(Integer, nullable=False)
    section = Column(String(10), nullable=False)
    type = Column(Enum(CourseTypeEnum), nullable=False)
