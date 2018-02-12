import click

from service_buddy.context.service_context import ServiceContext
from service_buddy.util.log_handler import configure_logging


@click.group()
@click.option("--application-filter", envvar='FILTER', help='Constrain command to operate on applications'
                                                            ' that match the passed filter')
@click.option("--service-filter", envvar='SERVICE_FILTER', help='Constrain command to operate on services'
                                                            ' that match the passed filter')
@click.option("--service-directory", envvar='SERVICE_DIRECTORY', type=click.Path(),
              default="./services",
              help='Directory containing service definitions in <app>/service.json format.  Default is \'./services\'')
@click.option('--destination-directory',
              envvar='DESTINATION',
              type=click.Path(),
              default="./code",
              help='The directory where the repositories for each service should be created or currently exist.')
@click.option("--verbose", is_flag=True, help='Print verbose status messages')
@click.option("--dry-run", is_flag=True, help='Preview effect of action')
@click.pass_context
def cli(ctx, application_filter, service_filter, service_directory, destination_directory, verbose, dry_run):
    # type: (object, str,str, str ,bool, bool) -> None
    """
    CLI for managing the repositories and build pipeline in a micro-service architecture..
    """
    configure_logging(verbose)
    ctx.obj = ServiceContext(
        filter_string=application_filter,
        service_filter_string=service_filter,
        service_directory=service_directory,
        destination_directory=destination_directory,
        dry_run=dry_run
    )


# noinspection PyUnresolvedReferences
from service_buddy.commands.clone import command
# noinspection PyUnresolvedReferences
from service_buddy.commands.git import command
# noinspection PyUnresolvedReferences
from service_buddy.commands.initialize import command
# noinspection PyUnresolvedReferences
from service_buddy.commands.list import command
# noinspection PyUnresolvedReferences
from service_buddy.commands.bootstrap import command

