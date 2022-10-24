import click

from service_buddy_too.commandline import cli
from service_buddy_too.util.pretty_printer import pretty_print_services, print_fqsn_services



@cli.command(name='list', short_help="Print definitions for services.")
@click.option('--validate-repository', envvar='VALIDATE',  is_flag=True,
              help='Validate existence of repository in VCS.')
@click.option('--print-fqsn', envvar='PRINT_FQSN',  is_flag=True,
              help='Print the fully qualified service name')
@click.pass_obj
def git_exec(service_ctx, validate_repository, print_fqsn):
    application_map = service_ctx.application_map
    if validate_repository:
        service_ctx.vcs.validate_repositories(application_map)
    if print_fqsn:
        print_fqsn_services(application_map)
    else:
        pretty_print_services(application_map)