import os

import click
from click import Choice

from infra_buddy.context.deploy_ctx import DeployContext
from service_buddy.ci import ci

from service_buddy.code.code_creator import CodeCreator
from service_buddy.commandline import cli
from service_buddy.context.service_context import ServiceContext
from service_buddy.service.service import Service
from infra_buddy.commands.bootstrap import command as bootstrap
from service_buddy.vcs import vcs


@cli.command(name='bootstrap', short_help="Create a repository containing the initial definition for a micro-service "
                                          "stack managed by service-buddy.")
@click.option("--application", envvar='APPLICATION', required=True,
              help='Application name for new micro-service stack.  Brevity suggested.')
@click.pass_obj
def bootstrap(service_ctx, application):
    # type: (ServiceContext, str,bool,str) -> None
    cc = CodeCreator("", service_ctx.dry_run)
    service_def = Service(app=application, role="master", definition={})
    service_def.set_service_type("service-buddy-master")
    directory = service_ctx.destination_directory
    if directory == "./code": #override default for this usecase
        directory = "./"
    config = {}
    vcs_provider = click.prompt('Please select your source code repository', type=Choice(vcs.vcs_providers) )
    config['vcs-provider'] = vcs_provider
    vcs_options = vcs.options
    for key,value in vcs_options.iteritems():
        config['vcs_{}'.format(key)] = click.prompt("VCS: {} ({})".format(value,key))
    ci_provider = click.prompt('Please select your build system - ', type=Choice(ci.build_systems) )
    config['build-system-provider'] = ci_provider
    ci_options = ci.build_system_map[ci_provider].options()
    for key,value in ci_options.iteritems():
        config['build-system-{}'.format(key)] = click.prompt("Build System: {} ({})".format(value,key))
    cc.create_project(service_definition=service_def, app_dir=directory,extra_config=config)
    
