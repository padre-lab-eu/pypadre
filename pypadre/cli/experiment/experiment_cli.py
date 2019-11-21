"""
Command Line Interface for PADRE.

"""
import os

import click
#################################
####### EXPERIMENT FUNCTIONS ##########
#################################
from click_shell import make_click_shell

from pypadre.cli.computation import computation_cli
from pypadre.cli.execution import execution_cli
from pypadre.cli.metric import metric_cli
from pypadre.cli.run import run_cli
from pypadre.core.model.experiment import Experiment
from pypadre.core.validation.json_schema import JsonSchemaRequiredHandler
from pypadre.pod.app.project.experiment_app import ExperimentApp


@click.group(name="experiment")
@click.pass_context
def experiment(ctx):
    pass


def _get_app(ctx) -> ExperimentApp:
    return ctx.obj["pypadre-app"].experiments


def _print_table(ctx, *args, **kwargs):
    ctx.obj["pypadre-app"].print_tables(Experiment, *args, **kwargs)


def _filter_selection(ctx, found):

    # filter for project selection
    if 'project' in ctx.obj:
        found = [f for f in found if f.parent == ctx.obj['project']]
    return found


@experiment.command(name="list")
@click.option('--offset', '-o', default=0, help='start number of the dataset')
@click.option('--limit', '-l', default=100, help='Number of datasets to retrieve')
@click.option('--search', '-s', default=None,
              help='search string')
@click.option('--column', '-c', help="Column to print", default=None, multiple=True)
@click.pass_context
def list(ctx, search, offset, limit, column):
    """
    List experiments defined in the padre environment
    """
    # List all the experiments that are currently saved
    _print_table(ctx, _filter_selection(ctx, _get_app(ctx).list(search=search, offset=offset, size=limit)), columns=column)


@experiment.command(name="get")
@click.argument('id', type=click.STRING)
@click.pass_context
def get(ctx, id):
    try:
        found = _filter_selection(ctx, _get_app(ctx).get(id))

        if len(found) == 0:
            click.echo(click.style(str("No experiment found for id: " + id), fg="red"))
        elif len(found) >= 2:
            click.echo(click.style(str("Multiple experiments found for id: " + id), fg="red"))
            _print_table(ctx, found)
        else:
            ctx.obj["pypadre-app"].print(found.pop())
    except Exception as e:
        click.echo(click.style(str(e), fg="red"))


@experiment.command(name="create")
@click.option('--name', '-n', default="CI created experiment", help='Name of the experiment')
@click.pass_context
def create(ctx, name):
    """
    Create a new experiment
    """
    # Create a new experiment
    def get_value(obj, e, options):
        return click.prompt(e.message + '. Please enter a value', type=str)

    app = _get_app(ctx)
    try:
        p = app.create(name=name, handlers=[JsonSchemaRequiredHandler(validator="required", get_value=get_value)])
        app.put(p)
    except Exception as e:
        click.echo(click.style(str(e), fg="red"))


@click.group(name="select", invoke_without_command=True)
@click.argument('id', type=click.STRING)
@click.pass_context
def select(ctx, id):
    """
    Select a experiment as active
    """
    # Set as active experiment
    experiments = _get_app(ctx).list({"id": id})
    if len(experiments) == 0:
        print("Experiment {0} not found!".format(id))
        return -1
    if len(experiments) > 1:
        print("Multiple matching experiments found!")
        _print_table(ctx, experiments)
        return -1
    prompt = ctx.obj['prompt'] + 'exp: ' + id + ' > '
    s = make_click_shell(ctx, prompt=prompt, intro='Selecting experiment ' + id, hist_file=os.path.join(os.path.expanduser('~'), '.click-pypadre-history'))
    ctx.obj['prompt'] = prompt
    ctx.obj['experiment'] = experiments.pop(0)
    s.cmdloop()
    del ctx.obj['experiment']


experiment.add_command(select)
select.add_command(execution_cli.execution)
select.add_command(run_cli.run)
select.add_command(computation_cli.computation)
select.add_command(metric_cli.metric)