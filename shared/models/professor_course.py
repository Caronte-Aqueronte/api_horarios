from sqlalchemy import Column, Enum, ForeignKey, Integer, String

from db.database import Base


class ProfessorCourse(Base):
    """_summary_:
    Relaciona un curso con un docente
    """
    __tablename__ = "professor_course"
    professor_id = Column(Integer, ForeignKey(
        "professor.id"), primary_key=True)

    course_id = Column(Integer, ForeignKey("course.id"), primary_key=True)
