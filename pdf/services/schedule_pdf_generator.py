from datetime import time
import io
from typing import Any, Dict, Iterator, List, Tuple
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from classrooms.models.classroom import Classroom
from schedules.ga.schedule import Schedule
from schedules.models.gen import Gen
from schedules.utils.period_util import PeriodUtil


class SchedulePdfGenerator:
    def __init__(self, schedule: Schedule):
        self.__schedule: Schedule = schedule
        self.__period_util: PeriodUtil = PeriodUtil()

    def generate_schedule_pdf(self) -> bytes:
        buffer: io.BytesIO = io.BytesIO()

        # el documento pasara el buffer para que este escriba sobre el
        pdf: SimpleDocTemplate = SimpleDocTemplate(buffer, pagesize=A4)

        schedule_map: Dict[Tuple[int, int], Gen] = self.__get_period_map()

        headers_row: List[str] = ["Hora/Salon"]

        # mandmoas a traer todos los classrooms
        classrooms: List[Classroom] = self.__get_classrooms()

        for classroom in classrooms:
            headers_row.append(f"{classroom.name}")

        data: List[Any] = []
        data.append(headers_row)

        # la lista de los periodos siempre es del 1 al 9. range es exclusive en el bound final
        all_periods: Iterator[int] = range(1, 10)

        # vamos recorriendo cada uno de los periodos
        for period in all_periods:

            # convertimos el periodo en tiempo
            period_start_time, period_end_time = self.__period_util.get_start_and_end_time_for_period(
                period)

            # formateamos la hora a string
            str_period_time: str = f"{period_start_time.strftime('%H:%M')} - {period_end_time.strftime('%H:%M')}"

            # aqui vamos a guardar todas los textos de las celdas
            row: List[str] = [str_period_time]

            # cada ahora vamos recorriendo cada una de las clases que estan presentes en los genes
            for classroom in classrooms:

                key = (period, classroom.id)

                # si la key existe en el mapa eso signidfica que este salon en este periodo tiene una asignacion
                if key in schedule_map:
                    gen: Gen = schedule_map[key]
                    course_name = gen.get_course().name
                    prof_name = gen.get_professor().name
                    cell_text = f"Curso: {course_name}\n Docente: {prof_name}"
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

    def __get_period_map(self) -> Dict[Tuple[int, int], Gen]:
        # este mapa va a guardar todos los genes que pertenecen a un periodo y salon
        schedule_map: Dict[Tuple[int, int], Gen] = {}
        # recorremos todos los genes
        for gen in self.__schedule.get_genes():
            # la llave sere el numero de periodo jutno con el id del salon
            key: Tuple[int, int] = (gen.get_period(), gen.get_classroom().id)

            # con la llave agregamos el salon
            schedule_map[key] = gen
        return schedule_map

    def __get_classrooms(self) -> List[Classroom]:
        classrooms: List[Classroom] = []
        for gen in self.__schedule.get_genes():
            classrooms.append(gen.get_classroom())

        return classrooms
