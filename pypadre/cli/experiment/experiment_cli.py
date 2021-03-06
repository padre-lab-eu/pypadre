"""
Command Line Interface for PADRE.

"""
import os
import sys

import click

from pypadre.cli.computation import computation_cli
from pypadre.cli.execution import execution_cli
from pypadre.cli.metric import metric_cli
from pypadre.cli.run import run_cli
from pypadre.cli.util import make_sub_shell, _create_experiment_file, get_by_app
from pypadre.core.model.experiment import Experiment
from ipython_genutils.py3compat import execfile
from pypadre.core.validation.json_schema import JsonSchemaRequiredHandler
from pypadre.pod.app.project.experiment_app import ExperimentApp


#################################
####### EXPERIMENT FUNCTIONS ##########
#################################


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
    _print_table(ctx, _filter_selection(ctx, _get_app(ctx).list(search=search, offset=offset, size=limit)),
                 columns=column)


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


@experiment.command(name="initialize")
@click.option('--name', '-n', default="CI created experiment", help='Name of the experiment')
@click.option('--project', '-p', default=None, help='Name of the project')
@click.option('--path', type=click.Path(), help='Path to the file defining the experiment pipeline.', default=None)
@click.option('--edit', is_flag=True)
@click.pass_context
def create(ctx, name, project, path,edit):
    """
    Create a new experiment
    """
    if project is None:
        project_parent = ctx.obj.get("project", None)
        if project_parent is not None:
            project = project_parent.name
        else:
            project = "CI created project"

    if path is None:
        path = _create_experiment_file(path=os.path.join(os.path.expanduser("~"), project, name), file_name=name)
        click.pause("Press any key to start editing your source code...")
        click.edit(filename=path)
    else:
        if edit:
            click.pause("Press any key to start editing your source code...")
            click.edit(filename=path)

    if click.confirm('Would you like to execute and save the experiment right away?'):
        click.echo(click.style('Executing experiment: {}'.format(name), fg="green"))
        ctx.invoke(execute, name=name, path=path, project_name=project)
    else:
        click.pause(
            "The experiment creation is not complete. You can run the command 'experiment execute --path {}' "
            "to execute and save your experiment".format(path, path))


@experiment.command(name="execute")
@click.option('--name', '-n', default="CI created experiment", help='Name of the experiment')
@click.option('--path', '-p', help='path to the source code', default=None)
@click.pass_context
def execute(ctx, name, path, project_name=None):
    if path is None:
        path = os.path.join(os.path.expanduser("~"), name) + "/" + name + ".py"
    if project_name is None:
        project = ctx.obj.get('project', None)
        if project is not None:
            project_name = project.name
        else:
            project_name = "CI created project"
    try:
        global_namespace = {
            "path": path,
            "config": ctx.obj["config-app"],
            "experiment_name": name,
            "project_name": project_name
        }
        globals = sys._getframe(1).f_globals
        locals = sys._getframe(1).f_locals
        globs = {**global_namespace, **globals}
        if click.confirm('Would you like to edit the file?'):
            click.edit(filename=path)
            click.pause('Press any key to execute...')
        execfile(path, glob=globs, loc=locals, compiler=compile)
        click.echo(click.style('Execution of the experiment is finished!'.format(name), fg="green"))
        # p = app.create(name=name, project=project,
        #                handlers=[JsonSchemaRequiredHandler(validator="required", get_value=get_value)])
    except Exception as e:
        click.echo(click.style(str(e), fg="red"))


@experiment.command(name="compare")
@click.argument('self_id', type=click.STRING)
@click.argument('other_id', type=click.STRING)
@click.pass_context
def compare(ctx, self_id, other_id):
    app = _get_app(ctx)

    experiment_ = get_by_app(ctx, app, self_id)
    experiment__ = get_by_app(ctx, app, other_id)
    if not experiment_ or not experiment__:
        return -1
    out = experiment_.compare(experiment__)
    click.echo("Comparing experiment {} and {}".format(experiment_.name,experiment__.name))
    click.echo(print(out[0]))
    click.echo("Comparing the respective pipelines of the two experiments")
    click.echo(print(out[1]))


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
    make_sub_shell(ctx, 'experiment', experiments.pop(0), 'Selecting experiment ')


experiment.add_command(select)
select.add_command(execution_cli.execution)
select.add_command(run_cli.run)
select.add_command(computation_cli.computation)
select.add_command(metric_cli.metric)
