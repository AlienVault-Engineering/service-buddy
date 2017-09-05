import os

import click

from click.testing import CliRunner
from service_buddy.commandline import cli
from service_buddy.context.service_context import ServiceContext
from testcase_parent import ParentTestCase

ctx = None


@cli.command(name='test-command')
@click.pass_obj
def test_method(service_ctx):
    # type: (ServiceContext) -> None
    global ctx
    ctx = service_ctx


class CommandlineTestCase(ParentTestCase):
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super(CommandlineTestCase, cls).setUpClass()

    def test_context_creation(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--service-directory', self.service_directory, '--dry-run', 'test-command'])
        self.assertTrue(ctx.vcs, "Failed to init vcs")
        self.assertTrue(ctx.application_map, "Failed to init app map")
        self.assertTrue(ctx.dry_run, "Failed to init dry run")

    def test_boostrap(self):
        runner = CliRunner()
        result = runner.invoke(cli, [  '--destination-directory',
                                             self.temp_dir, 'bootstrap','--application','app'])
        root_dir = os.path.join(self.temp_dir, "app-master")
        self.assertTrue(os.path.exists(root_dir), "Failed to create dir")
        self.assertTrue(os.path.exists(os.path.join(root_dir, "code-templates")), "Failed to create code-templates")
        service_dir = os.path.join(root_dir, "services")
        self.assertTrue(os.path.exists(service_dir), "Failed to create services")
        self.assertTrue(os.path.exists(os.path.join(service_dir,'app')), "Failed to create app directory")

    def test_list(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--service-directory', self.service_directory, '--dry-run', 'list'])
        self.assertEqual(result.exit_code, 0, "Failed to run list successfully")

    def test_clone(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--service-directory',
                                     self.service_directory,
                                     '--dry-run',
                                     '--destination-directory',
                                     self.temp_dir,
                                     'clone'
                                     ])
        self.assertEqual(result.exit_code, 0, "Failed to run list successfully")

    def test_git(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--service-directory',
                                     self.service_directory,
                                     '--dry-run',
                                     '--destination-directory',
                                     self.temp_dir,
                                     'git',
                                     "foo"])
        self.assertEqual(result.exit_code, 0, "Failed to run list successfully")

    def test_init(self):
        runner = CliRunner()
        result = runner.invoke(cli, [
                                    '--service-directory',
                                     self.service_directory,
                                     '--dry-run',
                                    '--destination-directory',
                                    self.temp_dir,
                                     'init',
                                     '--code-template-definitions',
                                     self.service_templates_test
                                     ]
                               )
        self.assertEqual(result.exit_code, 0, "Failed to run list successfully - {}".format(result.output))
