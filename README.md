# Pandemic
Little project showing the implementation if an pandemic algorithm.

## Information
- a not infected cell cannot infect others
- infected cells can infect others
- being sick doesn't mean that can infect others

### Colors
- **BLUE**   healthy & not infected & not immune
- **GREEN**  not infected & immune & healty
- **RED**    sick (infected or not)
- **YELLOW** incobation (infected & healthy)
- **ORANGE** not infected & immune & sick
- **BLACK**  dead

### Configuration file
A configuration file is supported with option `--config <path/to/file>` and formatted as:
```JSON 
{
    "infectable_neighbords": 4,
    "infection_rate": 0.2,
    "healing": 5,
    "incobation": 3,
    "immunity": 7,
    "immunity_loss": 6,
    "death": 0,
    "death_rate": 0
}
```

## Development

Recommended to use [UV Tool](https://docs.astral.sh/uv/)

Create environment: `$ uv venv`

Install requirements: `$ uv sync` 

Run CLI: `$ uv run scripts/cli.py --help`

## Build and use

Create wheel in pandemic/dist: `$ uv build`

In your environemt: `uv pip install <pandemic(...).whl>`

## Test (not implemented, maybe will not be)

Install extra requirements: `$ uv sync --group test`
