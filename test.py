import json
from dataclasses import dataclass
from datetime import datetime

import click


@dataclass
class Params:
    name: str
    value: int = 2
    missing_param: bool = True

    def __post_init__(self):
        self.name += "awesome"

    @classmethod
    def from_config(cls, config):
        constructor_parameters = {}
        converter = {"value": int, "name": str, "missing_param": bool}
        for key, value in config.items():
            try:
                constructor_parameters[key] = converter[key](value)
            except KeyError:
                raise Exception(f"Unknown parameter '{key}'")
            except ValueError:
                raise Exception(f"Invalid value for '{key}': '{value}'")
        try:
            return cls(**constructor_parameters)
        except TypeError as e:
            raise Exception(f"Missing required parameters from the config")


def parse_config(ctx, param, value):
    config = json.load(value)
    config.update(ctx.obj)
    return Params.from_config(config)


def add_param(ctx, param, value):
    if not ctx.obj:
        ctx.obj = {}
    if value is not None:
        ctx.obj[param.name] = value


common_parameters = [
    click.option(
        "-v", "--value", is_eager=True, expose_value=False, callback=add_param, type=str
    )
]


def add_common_params(function):
    for decorator in common_parameters:
        function = decorator(function)
    return function


@click.command()
@click.argument("config", callback=parse_config, required=True, type=click.File("r"))
@add_common_params
def job(config):
    print(config)


if __name__ == "__main__":
    job()
