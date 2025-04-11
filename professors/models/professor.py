from sqlalchemy import Column, Integer, String, Time
from db.database import Base
from sqlalchemy.orm import relationship

"""_summary_:
Este modelo rerpesenta la tabla que contiene el listado de profesores diponlibles en el sistema
"""


class Professor(Base):
    __tablename__ = "professor"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    dpi = Column(String(13), nullable=False, unique=True)
    entry_time = Column(Time, nullable=False)
    exit_time = Column(Time, nullable=False)

    courses = relationship("Course", back_populates="professor")
