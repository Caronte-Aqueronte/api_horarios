from sqlalchemy import Column, Enum, ForeignKey, Integer, String

from courses.enums.course_type_enum import CourseTypeEnum
from db.database import Base
from sqlalchemy.orm import relationship


class Classroom(Base):
    """_summary_:
    Este modelo rerpesenta la tabla que contiene el listado de salines diponlibles en el sistema
    """
    __tablename__ = "classroom"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    def __eq__(self, other) -> bool:
        # solo si es intancia de la clase
        if not isinstance(other, Classroom):
            return False
        return self.id == other.id
