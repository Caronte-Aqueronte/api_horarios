
from datetime import time
from typing import Dict, Tuple


class PeriodUtil:

    def get_start_and_end_time_for_period(self, period: int) -> Tuple[time, time]:
        # esto es un diccionario que tiene como clave un numero que corresponde al numero de periodo
        # y en su valor las horas  de inicio y fin que representan ese periodo
        times_for_periods: Dict[int, Tuple[time, time]] = {
            1: (time(13, 40), time(14, 30)),
            2: (time(14, 30), time(15, 20)),
            3: (time(15, 20), time(16, 10)),
            4: (time(16, 10), time(17, 00)),
            5: (time(17, 00), time(17, 50)),
            6: (time(17, 50), time(18, 40)),
            7: (time(18, 40), time(19, 30)),
            8: (time(19, 30), time(20, 20)),
            9: (time(20, 20), time(21, 10))
        }

        # mandamos a traer los tiempos segun la clave en el diccionario
        return times_for_periods[period]
