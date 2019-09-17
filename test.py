import click
import json


def parse_config(ctx, param, value):
    config = json.load(value)
    config.update(ctx.obj)
    return config


def add_param(ctx, param, value):
    if not ctx.obj:
        ctx.obj = {}
    if value is not None:
        ctx.obj[param.name] = value


common_parameters = [
    click.option(
        "--start-date",
        is_eager=True,
        expose_value=False,
        callback=add_param,
        type=click.DateTime(),
    ),
    click.option(
        "--end-date",
        is_eager=True,
        expose_value=False,
        callback=add_param,
        type=click.DateTime(),
    ),
    click.option(
        "--force", is_eager=True, expose_value=False, callback=add_param, type=bool
    ),
]


def common_params(function):
    for decorator in common_parameters:
        function = decorator(function)
    return function


@click.command()
@click.option("--config", callback=parse_config, required=True, type=click.File("r"))
@common_params
def job(config):
    print(config)


if __name__ == "__main__":
    job()
