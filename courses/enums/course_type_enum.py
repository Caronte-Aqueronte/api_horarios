import enum


class CourseTypeEnum(str, enum.Enum):
    """_summary_:
    Este enum representa los dos tipos podibles de cursos dentro del sistema
    """
    mandatory = "mandatory"
    elective = "elective"
