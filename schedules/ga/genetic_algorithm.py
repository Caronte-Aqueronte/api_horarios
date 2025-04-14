from typing import Dict, List, Tuple
import random
import time
import tracemalloc


from classrooms.models.classroom import Classroom
from courses.models.course import Course
from professors.models.professor import Professor
from schedules.dtos.ga_dto import GaDTO
from schedules.models.gen import Gen
from schedules.ga.schedule import Schedule


class GeneticAlgorithm:

    def __init__(self,
                 population_size: int,
                 max_generations: int,
                 courses: List[Course],
                 classrooms: List[Classroom],
                 professors: List[Professor],
                 manual_course_classrooms_assignments: Dict[Course, Classroom],
                 target_fitness: int,
                 selection_type: int
                 ):

        self.__population_size: int = population_size
        self.__max_generations: int = max_generations
        self.__courses: List[Course] = courses
        self.__classrooms: List[Classroom] = classrooms
        self.__professors: List[Professor] = professors
        self.__manual_course_classrooms_assignments: Dict[Course,
                                                          Classroom] = manual_course_classrooms_assignments

        self.__crossover_probability: float = 0.95
        self.__mutation_probability: float = 0.1
        self.__target_fitness = target_fitness
        self.__selection_type = selection_type

    def __generate_initial_population(self) -> List[Schedule]:
        # debemos guardar todos los horarios generados
        initial_population: List[Schedule] = []

        # tenemos que iterar el numero de veces que se quiere que se genere la poblacion inicial
        for _ in range(self.__population_size):
            # toca vamos a guardar los distintos genes
            genes: List[Gen] = []

            # por cada uno de los cursos disponibles vamos construyedno los diferentes genes aleatorios
            for course in self.__courses:

                # si ya existe un salor para este curso entonces lo obtenemos
                if course in self.__manual_course_classrooms_assignments:
                    classroom: Classroom = self.__manual_course_classrooms_assignments[course]
                else:
                    # sino elegimos una clase random
                    classroom: Classroom = self.__select_random_classroom()

                # generamos los periodos aleatorios con random
                period: int = self.__generate_random_period()

                # elegimos un profesor random para un curso
                professor: Professor = random.choice(self.__professors)

                # toca crear el gen con lo ya elejido
                gen: Gen = Gen(classroom, course, professor, period)
                genes.append(gen)

            # creamos el nuevo horario y lo agregamos a la pblacion inicial
            schedule: Schedule = Schedule(
                genes, self.__manual_course_classrooms_assignments)
            initial_population.append(schedule)

        return initial_population

    def __selection(self, population: List[Schedule]) -> Schedule:
        return self.__tournament(population) if self.__selection_type == 1 else self.__roulette(population)

    def __roulette(self, population: List[Schedule]) -> Schedule:

        total_fitness: int = sum([schedule.get_fitness()
                                 for schedule in population])

        # si el fitness total es 0 entonces devovlemos un random para evitar las diviciones por 0
        if (total_fitness == 0):
            return random.choice(population)

        # el fitnes relativo es la probabilidad de que sea elegido
        relatives_fitness: List[float] = [
            schedule.get_fitness()/total_fitness for schedule in population]

        # vamos a calcular las porciones que ocupa cada elemento en la ruleta
        cumulative_probability: List[float] = []
        accumulator: float = 0.0

        for relative_fitness in relatives_fitness:
            accumulator = accumulator + relative_fitness
            cumulative_probability.append(accumulator)

        # ahora vamos a generar el numero aletorio entre 0 y 1 para girar nuestra ruleta
        random_number: float = random.random()

        # erecorremos las acumuladas
        for i in range(len(cumulative_probability)):
            # si la seleccion de la ruleta es igual o menor a la probabilidad de una porcion entonces es porque esa se selecciono
            if random_number <= cumulative_probability[i]:
                return population[i]
        # si llego hasta aqui entonces no se pudo seleccionar nada en la ruleta y devolvemos uno random
        return random.choice(population)

    def __tournament(self, population: List[Schedule]) -> Schedule:
        # generamos el numero que indicara la muestra a seleccionar
        random_number = random.randint(1, len(population))
        # escogemos aleatoriamente la cantidad de objetos que dicto el
        sample: List[Schedule] = random.sample(population, random_number)
        return self.__get_best_schedule_of_list(sample)

    def __crossover(self, parent1: Schedule, parent2: Schedule) -> Schedule:
        # si el numero random es mayor a la probabilidad entonces no se hace cruce
        # y se elige uno de los padres al azar para copiarlo
        if random.random() > self.__crossover_probability:
            chosen_parent = random.choice([parent1, parent2])
            return Schedule(list(chosen_parent.get_genes()), self.__manual_course_classrooms_assignments)

        # lista donde se guardaran los genes del hijo
        child_genes: List[Gen] = []

        # se crean diccionarios para acceder rapido a los genes de cada padre por curso
        parent1_dict: Dict[Course, Gen] = {
            gen.get_course(): gen for gen in parent1.get_genes()}
        parent2_dict: Dict[Course, Gen] = {
            gen.get_course(): gen for gen in parent2.get_genes()}

        # se recorre cada curso para armar el hijo
        for course in self.__courses:
            # si el curso esta en padre1 y el random lo decide se usa el gen de padre1
            if random.random() < 0.5 and course in parent1_dict:
                base_gen: Gen = parent1_dict[course]
            # si no, se usa el de padre2 si lo tiene
            elif course in parent2_dict:
                base_gen: Gen = parent2_dict[course]
            else:
                # si ningun padre tiene el curso se genera uno aleatorio desde cero
                classroom: Classroom = (
                    self.__manual_course_classrooms_assignments[course]
                    if course in self.__manual_course_classrooms_assignments
                    else self.__select_random_classroom()
                )
                professor: Professor = random.choice(self.__professors)
                period: int = self.__generate_random_period()
                gen: Gen = Gen(classroom, course, professor, period)
                child_genes.append(gen)
                continue  # se salta lo de abajo porque ya se construyo el gen

            # si hay un gen base, se clona para no compartir referencias con padres
            classroom = (
                self.__manual_course_classrooms_assignments[course]
                if course in self.__manual_course_classrooms_assignments
                else base_gen.get_classroom()
            )
            professor = base_gen.get_professor()
            period = base_gen.get_period()

            gen = Gen(classroom, course, professor, period)
            child_genes.append(gen)

        # se devuelve el nuevo horario construido a partir de los genes del hijo
        return Schedule(child_genes, self.__manual_course_classrooms_assignments)

    def __mutate(self, schedule: Schedule):

        # prmierio debemos recorrer todos los genes de horario
        for gen in schedule.get_genes():

            # generamos un numero random entre 0 y 1
            random_number: float = random.random()

            if random_number < self.__mutation_probability:

                # toca generar un random entre 1 y tres que nos va a indicar que parte del gen vamos a alterar
                # si el random es 1 entonces cambiaremos el salon
                # si el random es 2 entonces cambiaremos el periodo
                # si el random es 3 entonces cambiaremos el docente
                mutation_type = random.randint(1, 3)

                if mutation_type == 1:
                    # solo mutamos el salon si el curso del gen no lo tiene asignado a la fuerza manualmente
                    if gen.get_course() not in self.__manual_course_classrooms_assignments:
                        new_classroom: Classroom = self.__select_random_classroom()
                        gen.set_classroom(new_classroom)

                elif mutation_type == 2:
                    new_period: int = self.__generate_random_period()
                    gen.set_period(new_period)

                elif mutation_type == 3:
                    new_professor: Professor = random.choice(self.__professors)
                    gen.set_professor(new_professor)
        # mandamos a recalcular el profit una vez haya mutado
        schedule.reaload_fitness()

    def __generate_random_period(self) -> int:
        # el periodo es del 1 9 porque solo esos existen de las
        return random.randint(1, 9)

    def __select_random_classroom(self) -> Classroom:
        # podmeos elejir aleatorioamente una clase  choice que escoge aleatoriamente un elemento de lista
        return random.choice(self.__classrooms)

    def run(self) -> GaDTO:

        history_confilcts: Dict[str, int] = {}
        history_fitness: Dict[str, int] = {}
        # guarda el numero de iteraciones totales para encontrar la solucion optima
        total_iterations: int = 0
        # guardamos una marca de tiempo y memoria antes de iniciar el algoritmo
        start: float = time.time()
        tracemalloc.start()  # comienza a medir la memoria usuada

        # hay que generar la poblacion inicial
        population: List[Schedule] = self.__generate_initial_population()

        # mandamos a calcular los conflictos totales de la generacion inicial y guardamos en el dict
        confilcts_population: int = self.__measure_total_conflicts_of_generation(
            population)
        history_confilcts["Población Inicial"] = confilcts_population

        # de la generacion que se caba de crear debemos saber cual es el mejor
        best_schedule: Schedule = self.__get_best_schedule_of_list(population)

        # agregamos el fitness de la poblacion inicial
        history_fitness["Población Inicial"] = best_schedule.get_fitness()

        # debemos crear las generaciones que que el usuario quiere crear
        for i in range(self.__max_generations):
            total_iterations = i + 1
            new_population: List[Schedule] = []

            for _ in range(self.__population_size):

                # generamos los padres
                parent1: Schedule = self.__selection(population)
                parent2: Schedule = self.__selection(population)

                # cruzamos los padres aparetnemente porque aveces si y aveces no se cruzan
                son: Schedule = self.__crossover(parent1, parent2)

                # mandamos a mutarlo aparentemente porque casi nunca se mutan
                self.__mutate(son)

                new_population.append(son)

            # mandamos a calcular los conflictos totales de la generacion inicial y guardamos en el dict
            confilcts_population: int = self.__measure_total_conflicts_of_generation(
                population)
            history_confilcts[f"Generación {total_iterations}"] = confilcts_population

            # remplazamos la vieja poblacion por la nueva
            population = new_population

            # mandamos a traer el horario mas apto
            probable_best_schedule: Schedule = self.__get_best_schedule_of_list(
                population)
            # guardamos la fitness del mejor de la generacion
            history_fitness[f"Generación {total_iterations}"] = probable_best_schedule.get_fitness(
            )

            # si alcanzamos el fitness objetivo e ideal entonces nos detenemos aqui
            if (probable_best_schedule.get_fitness() >= self.__target_fitness):
                best_schedule = probable_best_schedule
                break

            # si el horario de la nueva geneeracion es mejor que el de la anterior entonces lo sustituimos
            if (probable_best_schedule.get_fitness() > best_schedule.get_fitness()):
                best_schedule = probable_best_schedule

        # tomamos el tiempo final
        total_time: float = self.__measure_time(start)
        # tomamos el la ocupacion de memoria del algoritmo
        final_memory: float = self.__measure_memory()

        # debemos mandar a calcular los porcentajes de asignaciones continuas
        semester_continuity_percentages, global_continuity_percentage = self.__measure_continuity_percentage_per_semester(
            best_schedule)
        return GaDTO(schedule=best_schedule, total_iterations=total_iterations, history_confilcts=history_confilcts,
                     history_fitness=history_fitness, memory_usage=final_memory, total_time=total_time,
                     semester_continuity_percentages=semester_continuity_percentages,
                     global_continuity_percentage=global_continuity_percentage)

    def __measure_continuity_percentage_per_semester(
        self, schedule: Schedule
    ) -> Tuple[Dict[Tuple[int, str], float], float]:

        # lleva la cuenta de cuantos cursos hay para cada semestre y carrera
        quantity_courses_of_same_semester: Dict[Tuple[int, str], int] = {}

        # para cada semestre y carrera se almacena la lista de periodos asignados
        courses_continuity: Dict[Tuple[int, str], List[int]] = {}

        # dic final con el porcentaje de continuidad de cada semestre y carrera
        semester_continuity_percentages: Dict[Tuple[int, str], float] = {}

        # total de cursos en el horario actual
        total_courses: int = len(schedule.get_genes())

        # cursos consecutivos totales detectados
        total_continuity_courses: int = 0

        # recorremos todos los genes y agrupamos cuantos cursos hay por
        #    admeas de almacenar los periodos en los que aparecieron
        for gen in schedule.get_genes():
            continuity_key: Tuple[int, str] = (
                gen.get_course().semester,
                gen.get_course().career
            )

            # aumentamos la cuenta de cursos
            quantity_courses_of_same_semester[continuity_key] = (
                quantity_courses_of_same_semester.setdefault(
                    continuity_key, 0) + 1
            )

            # registramos el periodo para ese semestre y carrera
            courses_continuity.setdefault(
                continuity_key, []).append(gen.get_period())

        # calculamos la continuidad
        for continuity_key, periods in courses_continuity.items():
            # ordenamos los periodos
            periods.sort()

            continuity_courses_of_semester: int = 0
            # recorremos los periodos, iniciando por el segundo elemento y vamos comparando cada uno con el anterior
            for i in range(1, len(periods)):
                # si la resta del periodo actual menos el anterior es 1 entonces es consecutivo
                if periods[i] - periods[i - 1] == 1:
                    continuity_courses_of_semester = continuity_courses_of_semester + 2
                    total_continuity_courses = total_continuity_courses + 2
             # con la llave obtenemos la cantidad de cursos que existen de la misma carrera y semestre
            num_courses_of_same_semester: int = quantity_courses_of_same_semester[
                continuity_key]

           # ahora debemos dividir la cantidad de cursos continuos por la cantidad de cursos que existen en el semestre
           # lo multiplicamos por 100 para que convertirlo en un porcentaje
            if num_courses_of_same_semester > 0:   # evita divisin entre cero
                semester_continuity_percentages[continuity_key] = (
                    continuity_courses_of_semester / num_courses_of_same_semester
                ) * 100
            else:
                semester_continuity_percentages[continuity_key] = 0.0

        # ahora debemos dividir la cantidad de cursos totales continuos por la cantidad de cursos totales
        # lo multiplicamos por 100 para que convertirlo en un porcentaje
        if total_courses > 0:   # evita divisin entre cero
            global_continuity_percentage: float = (
                total_continuity_courses / total_courses)*100
        else:
            global_continuity_percentage: float = 0.0

        return (semester_continuity_percentages, global_continuity_percentage)

    def __measure_total_conflicts_of_generation(self, population: List[Schedule]) -> int:
        total_conflicts: int = 0
        for schedule in population:
            total_conflicts = total_conflicts + schedule.get_conflicts()
        return total_conflicts

    def __measure_memory(self) -> float:
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak / 1024  # tremalloc mide en bytes asi que lo pasamos a kilobytes

    def __measure_time(self, initial_time: float) -> float:
        return time.time() - initial_time

    def __get_best_schedule_of_list(self, schedules: List[Schedule]) -> Schedule:

        # mandamos a obtener el maximo de la lista segun su aptitud
        return max(
            schedules, key=lambda schedule: schedule.get_fitness())
