import click
from service_buddy.commandline import cli

from service_buddy.context.service_context import ServiceContext


@cli.command(name='git', short_help="Run arbitrary git command for each service")
@click.option('--destination-directory', envvar='DESTINATION', type=click.Path(exists=True),
              help='The directory where the git repositories corresponding to the service definitions exist.'
                   ' See service-manager clone to initialize them.')
@click.argument('cmd', nargs=-1)
@click.pass_obj
def git_exec(service_ctx,destination_directory, cmd):
    # type: (ServiceContext, str) -> None
    """
    :param cmd: The git command to execute in each service directory.
    This can be used for commands such as "--git pull" or "--git commit -m 'Big old commit'"
    """
    service_ctx.vcs.validate_repositories(service_ctx.application_map)
    service_ctx.vcs.git_exec(application_map=service_ctx.application_map,
                             destination_directory=destination_directory,
                             args=cmd)
