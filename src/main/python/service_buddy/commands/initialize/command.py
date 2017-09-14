import click

from service_buddy.commandline import cli
from service_buddy.context.service_context import ServiceContext
from service_buddy.service.initializer import Initializer


@cli.command(name='init',short_help="Analyze service definitions and initialize any new services.")
@click.option('--code-template-definitions',
              envvar='CODE_TEMPLATE_DIR',
              type=click.Path(exists=True),
              required=True,
              default="./code-templates",
              help='File containing references to custom service templates.  '
                   ' JSON dictionary {service-type: {type: file|git, location: relative path | git URL}}')
@click.option('--skip-build-creation', envvar='SKIP_BUILD_CREATE',  is_flag=True, default=False,
              help='Skip the creation of build step.')
@click.option('--skip-git-creation', envvar='SKIP_GIT_CREATE',  is_flag=True, default=False,
              help='Skip the creation of git repository.')
@click.pass_obj
def list_service(service_ctx,code_template_definitions, skip_build_creation,skip_git_creation):
    # type: (ServiceContext, str,str) -> None
    vcs =service_ctx.vcs
    application_map = service_ctx.application_map
    vcs.validate_repositories(application_map)
    init = Initializer(vcs, service_ctx.destination_directory, service_ctx.dry_run,code_template_definitions, skip_build_creation,skip_git_creation)
    init.initialize_services(application_map)