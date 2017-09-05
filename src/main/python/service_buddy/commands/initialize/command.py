import click

from service_buddy.commandline import cli
from service_buddy.context.service_context import ServiceContext
from service_buddy.service.initializer import Initializer


@cli.command(name='init',short_help="Analyze service definitions and initialize any new services.")
@click.option('--destination-directory', envvar='DESTINATION', type=click.Path(exists=True),
              help='The directory where the git repositories corresponding to the service definitions exist.'
                   ' See service-manager clone to initialize them.')
@click.option('--service-template-definitions',
              envvar='SERVICE_TEMPLATE_DIR',
              type=click.Path(exists=True),
              required=True,
              help='File containing references to custom service templates.  '
                   ' JSON dictionary {service-type: {type: file|git, location: relative path | git URL}}')
@click.pass_obj
def list_service(service_ctx, destination_directory,service_template_definitions):
    # type: (ServiceContext, str,str) -> None
    vcs =service_ctx.vcs
    application_map = service_ctx.application_map
    vcs.validate_repositories(application_map)
    init = Initializer(vcs, destination_directory, service_ctx.dry_run,service_template_definitions)
    init.initialize_services(application_map)