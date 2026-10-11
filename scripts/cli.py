#!/usr/bin/env python 

import logging
from pathlib import Path
from typing import Annotated

import typer
import pydantic

from pandemic import Pandemic, InfectionParameters
from pandemic.terminal_helper import print_centered, clear, home, show_cursor, Color, BIG_CIRCLE, RESET_COLOR

project_path = Path(__file__).parent.parent.resolve()
logger = logging.getLogger(__name__)

app = typer.Typer()

def configure_logger(debug: bool = False) -> None:
    logs_folder = project_path / "logs"
    root_logger = logging.getLogger()
    log_level = logging.DEBUG if debug else logging.INFO
    root_logger.setLevel(log_level)

    format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)s")

    logs_folder.mkdir(exist_ok=True)
    log_filename = logs_folder / "pandemic_cli.log"

    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(format)
    root_logger.addHandler(file_handler)
    

def splash_screen() -> None:
    clear()
    all_colored_circles = "".join([f'{color}{BIG_CIRCLE}' for color in Color])
    print_centered(f"Welcome to Pandemic CLI {all_colored_circles}{RESET_COLOR}")
    print("\n")
    print_centered("Press to start...", row_offset=1)
    input()


def validate_infected(ctx: typer.Context, infected: int) -> int:
    max_infected = ctx.params.get("width") * ctx.params.get("heigth") / 2

    if infected >= max_infected:
        raise typer.BadParameter(f"required to be less than half the cells (< {max_infected})")
    
    return infected


def validate_config_file(config: typer.FileText | None) -> InfectionParameters:
    if config:
        try:
            return InfectionParameters.model_validate_json(config.read())
        except pydantic.ValidationError as ex:
            raise typer.BadParameter(f"config file {config.name} is not compliant. {ex.errors()}")

@app.command()
def main(
    width: Annotated[int, typer.Option(min=5, max=200, help="Grid width")] = 20,
    heigth: Annotated[int, typer.Option(min=5, max=100, help="Grid heigth")] = 20,
    animation_speed: Annotated[float, typer.Option(min=0.1, max=40, help="Animation speed")] = 0.2,
    infected: Annotated[int, typer.Option(min=1, help="Number of initial infected cells", callback=validate_infected)] = 1,
    infection_parameters: Annotated[typer.FileText | None, typer.Option("--config", help="Configuration file", callback=validate_config_file)] = None,
    debug: Annotated[bool, typer.Option(help="Debug logging", rich_help_panel="Utils")] = False
    ) -> None:
    configure_logger(debug=debug)
    logger.info("Starting Pandemic CLI...")
    splash_screen()

    pandemic = Pandemic(
        width=width,
        heigth=heigth,
        animation_speed=animation_speed,
        infected=infected,
        infection_parameters=infection_parameters,
    )

    try:
        pandemic.run()
    except KeyboardInterrupt:
        logger.info("Pandemic interruped by user input")
    finally:
        clear()
        home()
        show_cursor()

    logger.info("Closing Pandemic CLI, bye!")


if __name__ == "__main__":
    app()
