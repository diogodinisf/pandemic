import logging
from time import sleep
import random

from pandemic.types import Cell, InfectionParameters
from pandemic.animations import loading_screen
from pandemic.terminal_helper import clear, home, hide_cursor, show_cursor
from pandemic.map_vizualizer import draw_map

logger = logging.getLogger(__name__)


class Pandemic:
    """
    Simulates a pandemic crisis inside a well-defined box. At the, we all are going to die!!!

    Parameters
    ----------
    width: int
        Width of the box.
    heigth: int
        Heigth of the box.
    animation_speed: int
        Speed to show the animation of are cells dieing.
    infected: int
        Amount of cells that are patient zero.
    infection_parameters: InfectionParameters | None
        Infection parameters user-configurable.
    """

    def __init__(
            self, *,
            width: int = 20,
            heigth: int = 20,
            animation_speed: float = 0.2,
            infected: int = 1,
            infection_parameters: InfectionParameters | None = None,
        ) -> None:
        self.__width = width
        self.__heigth = heigth
        self.__animation_speed = animation_speed

        logger.info(f"Initializing Pandemic with width={width}, heigth={heigth}, "
                    "amount of patients zero={infected}, animation speed={animation_speed}")

        if not infection_parameters:
            self.__infection_parameters = InfectionParameters(
                infection_rate=0.1,
            )
        else:
            self.__infection_parameters = infection_parameters

        self.__map = self.__generate_map()  # indexation: map[x][y]
        self.__infect_patient_zero(infected)

    def run(self) -> None:
        """
        Runner to iterate over the evluotion of the infection.

        Returns
        -------
        None
        """

        logger.info("Starting pandemic runner...")
        loading_screen(repetions=2)
        clear()
        hide_cursor()
        home()
        draw_map(self.__map)

        for iteration in range(2000):
            logger.debug(f"Runner iteration: {iteration}")
            home()    
            self.__iterate_over_cells(iteration)
            draw_map(self.__map)
            sleep(1/self.__animation_speed)

        clear()
        home()
        show_cursor()

    ### helpers
    def __iterate_over_cells(self, iteration: int) -> None:
        for x in range(len(self.__map)):
            for y in range(len(self.__map[0])):
                self.__update_health_state(x, y, iteration)
                self.__infect(x, y, iteration)

    def __infect(self, x: int, y: int, iteration: int) -> None:
        cell = self.__map[x][y]

        if not self.__can_infect(cell, iteration):
            return

        neigthbords = self.__get_neigthbords(x, y)

        logger.debug(f"Cell ({x}, {y}) may infect neighbords {neigthbords}")

        for n_x, n_y in neigthbords:
            neigthbord_cell = self.__map[n_x][n_y]

            if self.__can_be_infected(neigthbord_cell) and self.__was_infected():
                neigthbord_cell.infected = 1
                neigthbord_cell.infected_on = iteration
                logger.debug(f"Neigthbord {n_x},{n_y} was infected in iteration {iteration}")

    def __was_infected(self) -> float:
        return random.random() < self.__infection_parameters.infection_rate

    def __can_infect(self, cell: Cell, iteration: int) -> bool:
        return cell.infected > 0 and cell.infected_on < iteration

    def __can_be_infected(self, cell: Cell) -> bool:
        return cell.infected == 0 and cell.immune == 0 and cell.alive

    def __get_neigthbords(self, x: int, y: int) -> set[tuple[int, int]]:
        neigthbords = {
            (x, y + 1),  # top
            (x, y - 1),  # bottom
            (x - 1, y),  # left
            (x + 1, y),  # right
        }

        if self.__infection_parameters.infectable_neighbords == 8:
            neigthbords |= {
                (x - 1, y + 1),  # top-left
                (x - 1, y - 1),  # bottom-left
                (x + 1, y + 1),  # top-right
                (x + 1, y - 1),  # bottom-right
            }

        valid_neigthbords = set()

        for neigthbord in neigthbords:
            if self.__validate_cell(*neigthbord):
                valid_neigthbords.add(neigthbord)

        return valid_neigthbords

    def __validate_cell(self, x: int, y: int) -> bool:
        return not (x < 0 or y < 0 or x >= self.__width or y >= self.__heigth)

    def __update_health_state(self, x: int, y: int, iteration: int) -> None:
        cell = self.__map[x][y]
        previously_infected = cell.infected > 0 and cell.infected_on < iteration

        # infection
        if previously_infected:
            cell.infected += 1

            if self.__infection_parameters.immunity > 0 and cell.infected > self.__infection_parameters.immunity:
                cell.infected = 0
                cell.immune = 1

        # sickness
        if cell.sick > 0 or (previously_infected and cell.infected - self.__infection_parameters.incobation > 0):
            cell.sick += 1

            if self.__infection_parameters.death > 0 and self.__infection_parameters.death_rate > 0 and cell.sick > self.__infection_parameters.death and self.__died():
                cell.alive = False
                cell.sick = 0
                cell.immune = 0
                cell.infected = 0
                return

            if self.__infection_parameters.healing > 0 and cell.sick > self.__infection_parameters.healing:
                cell.sick = 0

        # immunity
        if cell.immune > 0:
            cell.immune += 1

            if self.__infection_parameters.immunity_loss > 0 and cell.immune > self.__infection_parameters.immunity_loss:
                cell.immune = 0

    def __died(self) -> float:
        return random.random() < self.__infection_parameters.death_rate


    def __generate_map(self) -> list[list[Cell]]:
        """
        Generates map with pre-defined width and height.

        Returns
        -------
        list[list[Cell]]
            Map with all cells in healthy state.
        """
    
        return [[Cell(height=height, width=width) for height in range(self.__heigth)] for width in range(self.__width)]

    def __infect_patient_zero(self, to_infec: int) -> None:
        """
        Randomly infect patients zero.

        Parameters
        ----------
        to_infect: int
            Amount of cells to infect.

        Returns
        -------
        None
        """

        infected: set[tuple[int, int]] = set()

        while len(infected) < to_infec:
            x = random.randint(0, self.__width - 1)
            y = random.randint(0, self.__heigth - 1)

            if (x, y) not in infected:
                cell = self.__map[x][y]
                cell.infected = True
                cell._infected_on = 0
                
                infected.add((x,y))
