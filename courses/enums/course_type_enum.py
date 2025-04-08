import enum

"""_summary_:
    Este enum representa los dos tipos podibles de cursos dentro del sistema
"""


class CourseTypeEnum(str, enum.Enum):
    mandatory = "mandatory"
    elective = "elective"
