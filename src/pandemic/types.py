from typing import Literal, Annotated
from dataclasses import dataclass

from pydantic import Field, BaseModel

@dataclass
class Cell:
    # personal information
    width: int
    height: int
    alive: bool = True

    # infection status - evolve with iterations
    infected_on: int = -1
    infected: int = 0
    sick: int = 0
    immune: int = 0


class InfectionParameters(BaseModel):
    infectable_neighbords: Annotated[Literal[4, 8], Field(description="4: infect only in cross, 8: infect also diagonal neigthbords")] = 4
    infection_rate: float = Field(gt=0, le=1, description="Probability of infect a neigthbord")
    death_rate: Annotated[float, Field(ge=0, le=1, description="Probability of die being sick")] = 0

    # These prameters unity is iterations
    death: Annotated[int, Field(description="Delay until possibility of death; 0: never die")] = 0
    immunity: Annotated[int, Field(descrption="Delay until get immunity; 0: never get immunity")] = 0
    incobation: Annotated[int, Field(description="Delay between being infected and sick; 0 never get sick")] = 0
    healing: Annotated[int, Field(descrptions="Delay until get better; 0: never get better")] = 0
    immunity_loss: Annotated[int, Field(description="Delay until loose immunity; 0: never loose immunity")] = 0
