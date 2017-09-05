import click
from service_buddy.commandline import cli


@cli.command(name='clone',short_help="Clone all of the existing service definition repos onto the local file system")
@click.option('--destination-directory',
              envvar='DESTINATION',
              type=click.Path(exists=True),
              required=True,
              help='The directory to pull the code into.')
@click.pass_obj
def git_clone(service_ctx, destination_directory):
    service_ctx.vcs.validate_repositories(service_ctx.application_map)
    service_ctx.vcs.clone_service(service_ctx.application_map, destination_directory)
