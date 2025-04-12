from typing import Dict, List
import random
from classrooms.models.classroom import Classroom
from courses.models.course import Course
from professors.models.professor import Professor
from schedules.models.gen import Gen
from schedules.ga.schedule import Schedule


class GeneticAlgorithm:

    def __init__(self,
                 population_size: int,
                 max_generations: int,
                 courses: List[Course],
                 classrooms: List[Classroom],
                 professors: List[Professor],
                 manual_course_classrooms_assignments: Dict[Course, Classroom]):

        self.__population_size: int = population_size
        self.__max_generations: int = max_generations
        self.__courses: List[Course] = courses
        self.__classrooms: List[Classroom] = classrooms
        self.__professors: List[Professor] = professors
        self.__manual_course_classrooms_assignments: Dict[Course,
                                                          Classroom] = manual_course_classrooms_assignments

        self.__crossover_probability: float = 0.95
        self.__mutation_probability: float = 0.1
        self.__tournament_size: int = 3
        self.__target_fitness = 0

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
            schedule: Schedule = Schedule(genes)
            initial_population.append(schedule)

        return initial_population

    def __selection(self, population: List[Schedule]) -> Schedule:
        # seleccionamos aleatoriamente un subconjunto de individuos de la población
        # esto lo logramos con sample porque elige una cantidad de elementos X de una lista aleatoriamente
        tournament_elements: List[Schedule] = random.sample(
            population, self.__tournament_size)

        # mandamos a traer el horario con mayor aptitud
        best_schedule: Schedule = self.__get_best_schedule_of_list(
            tournament_elements)

        # Devolvemos el individuo ganador del torneo
        return best_schedule

    def __get_best_schedule_of_list(self, schedules) -> Schedule:

        # mandamos a obtener el maximo de la lista segun su aptitud
        return max(
            schedules, key=lambda schedule: schedule.get_fitness())

    def __crossover(self, parent1: Schedule, parent2: Schedule) -> Schedule:
        # generamos un numero randon entre 1 y 0
        random_number: float = random.random()

        genes_count = len(parent1.get_genes())

        # si este es menor a la probabilidad entonces significa se hace cruce
        if genes_count >= 2 and random_number <= self.__crossover_probability:

            # seleccionar un punto de cruce aleatoriom, 0 y len evitados para que no sea copia
            crossover_point: int = random.randint(
                1, len(parent1.get_genes()) - 1)

            # tomamos la parte izquierda de los genes del padre 1
            left_genes: List[Gen] = parent1.get_genes()[:crossover_point]

            # tomamos la parte derecha de los genes del padre 2
            right_genes: List[Gen] = parent2.get_genes()[crossover_point:]

            # unimos ambas partes para formar los genes del hijo
            child_genes: List[Gen] = left_genes + right_genes

            return Schedule(child_genes)

        selected_genes = random.choice(
            [parent1.get_genes(), parent2.get_genes()])

        # choise devulve un set entonces sebemos convetirlo a lista
        return Schedule(list(selected_genes))

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

    def run(self) -> Schedule:

        # hay que generar la poblacion inicial
        population: List[Schedule] = self.__generate_initial_population()

        # de la generacion que se caba de crear debemos saber cual es el mejor
        best_schedule: Schedule = self.__get_best_schedule_of_list(population)

        # debemos crear las generaciones que que el usuario quiere crear
        for _ in range(self.__max_generations):
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

            # remplazamos la vieja poblacion por la nueva
            population = new_population

            # mandamos a traer el horario mas apto
            probable_best_schedule: Schedule = self.__get_best_schedule_of_list(
                population)

            # si alcanzamos el fitness objetivo e ideal entonces nos detenemos aqui
            if (probable_best_schedule.get_fitness() >= self.__target_fitness):
                return probable_best_schedule

            # si el horario de la nueva geneeracion es mejor que el de la anterior entonces lo sustituimos
            if (probable_best_schedule.get_fitness() > best_schedule.get_fitness()):
                best_schedule = probable_best_schedule

        return best_schedule
