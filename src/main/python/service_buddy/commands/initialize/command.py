import click

from service_buddy.commandline import cli
from service_buddy.context.service_context import ServiceContext
from service_buddy.service.initializer import Initializer


@cli.command(name='init',short_help="Analyze service definitions and initialize any new services.")
@click.option('--service-template-definitions',
              envvar='SERVICE_TEMPLATE_DIR',
              type=click.Path(exists=True),
              required=True,
              default="./service-templates",
              help='File containing references to custom service templates.  '
                   ' JSON dictionary {service-type: {type: file|git, location: relative path | git URL}}')
@click.pass_obj
def list_service(service_ctx,service_template_definitions):
    # type: (ServiceContext, str,str) -> None
    vcs =service_ctx.vcs
    application_map = service_ctx.application_map
    vcs.validate_repositories(application_map)
    init = Initializer(vcs, service_ctx.destination_directory, service_ctx.dry_run,service_template_definitions)
    init.initialize_services(application_map)