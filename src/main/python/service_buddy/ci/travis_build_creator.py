import json
import os

import logging

from service_buddy.util.command_util import invoke_process


class TravisBuildCreator(object):
    def init(self, dry_run, default_config, build_templates):
        self.dry_run = dry_run
        self.build_templates = build_templates
        self.use_org = default_config.get("use-travis-open-source", True)
        self.gh_token = default_config.get('github-token', os.environ.get('GITHUB_TOKEN'))
        self.pypi_user = default_config.get('pypi-user', os.environ.get('PYPI_USER'))
        self.pypi_pass = default_config.get('pypi-pass', os.environ.get('PYPI_PASS'))
        if invoke_process(['travis', '--version']) != 0:
            raise Exception("Travis CLI must be installed to use travis build creator.  "
                            "See https://github.com/travis-ci/travis.rb#installation")
        if invoke_process(['travis', 'login', '--github-token', self.gh_token], dry_run=self.dry_run) != 0:
            raise Exception("Unable to authenticate Travis CLI. Please verify github token is configured properly.")

    def create_project(self, service_definition, service_dir):
        if service_definition.get_service_type() not in self.build_templates:
            raise Exception(
                "Build template not found for service type {}".format(service_definition.get_service_type()))
        else:
            build_template = self.build_templates.get(service_definition.get_service_type())
        if os.path.exists(self._get_travis_file(service_dir)):
            logging.warn("travis build file exists - enabling repo")
            invoke_process(['travis', 'enable'], exec_dir=service_dir, dry_run=self.dry_run)
        else:
            self.create_build(service_dir, build_template)

    def _get_travis_file(self, service_dir):
        return os.path.join(service_dir, ".travis.yml")

    @classmethod
    def get_type(cls):
        return "travis"

    def create_build(self, service_dir, build_template):
        language_ = build_template.get('language', 'python')
        args = [
            'travis',
            'init',
            language_
        ]
        if language_ == 'python':
            args.append('--python')
            args.append('2.7')

        if self.use_org:
            args.append("--org")
        else:
            args.append("--pro")
        install_script = build_template.get('install', None)
        if install_script:
            args.append('--install')
            args.append(install_script)
        script = build_template.get('script', None)
        if script:
            args.append('--script')
            args.append(script)

        invoke_process(args, exec_dir=service_dir, dry_run=self.dry_run)
        use_pypi = build_template.get('pypi-deploy', False)
        if use_pypi:
            self._write_deploy_stanza(service_dir)
            invoke_process(['travis', 'encrypt', self.pypi_pass, '--add', 'deploy.password'], exec_dir=service_dir,
                           dry_run=self.dry_run)

    def _write_deploy_stanza(self, service_dir):
        with open(self._get_travis_file(service_dir), 'a') as build_file:
            build_file.writelines([
                '\n'
                'deploy\n',
                '\tprovider: pypi\n',
                '\tuser: {}\n'.format(self.pypi_user),
                '\tdistributions: sdist bdist_wheel\n',
                '\tserver: https://upload.pypi.org/legacy\n'
            ])
