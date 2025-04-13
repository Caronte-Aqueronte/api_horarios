import io
from typing import Any, List
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


from courses.dto.course_response_dto import CourseResponseDTO
from schedules.dtos.schedule_dto import ScheduleDTO


class SchedulePdfGenerator:
    def __init__(self, schedule: ScheduleDTO):
        self.__schedule: ScheduleDTO = schedule

    def generate_schedule_pdf(self) -> bytes:
        buffer: io.BytesIO = io.BytesIO()

        # el documento pasara el buffer para que este escriba sobre el
        pdf: SimpleDocTemplate = SimpleDocTemplate(buffer, pagesize=A4)

        headers_row: List[str] = ["Perido/Salon"]

        for classroom in self.__schedule.classrooms:
            headers_row.append(f"{classroom.name}")

        data: List[Any] = []
        data.append(headers_row)

        # vamos recorriendo cada uno de los periodos
        for period in self.__schedule.rows:

            # aqui vamos a guardar todas los textos de las celdas
            row: List[str] = [period.time_range]

            # cada ahora vamos recorriendo cada una de las clases que estan presentes en los genes
            for assignment in period.assignments:

                # si la key existe en el mapa eso signidfica que este salon en este periodo tiene una asignacion
                if not assignment.is_empty:
                    course: CourseResponseDTO = assignment.course
                    professor_name = assignment.professor_name
                    professor_dpi = assignment.professor_dpi
                    cell_text = f"Curso-Codigo\n{course.name}\n{course.code}\nDocente-DPI\n{professor_name}\n{professor_dpi}"
                else:
                    cell_text = "-"

                row.append(cell_text)

            data.append(row)

        # tenemos que crear la tabla, el repeatRows es para que se repitan los encabeezados en cada agina
        table = Table(data, repeatRows=1)

        # estiloas de tabla estilo a la tabla
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 20),
            ('TOPPADDING', (0, 0), (-1, 0), 6),


            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, 0), 20),
        ]))

        styles = getSampleStyleSheet()
        style_header = styles["Title"]

        elements = []
        # le damos el ncabezado del reporte
        elements.append(Paragraph("Horario", style_header))
        elements.append(Spacer(1, 12))
        # la tabla al documento
        elements.append(table)
        # construimos el reporte en el buffer
        pdf.build(elements)

        buffer.seek(0)

        return buffer.getvalue()
