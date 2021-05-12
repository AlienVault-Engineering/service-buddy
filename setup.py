#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'service-buddy-too',
        version = '0.1.1',
        description = 'CLI for managing micro-services',
        long_description = 'CLI for managing micro-services',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = '',
        author_email = '',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache 2.0',

        url = 'https://github.com/rspitler/service-buddy',
        project_urls = {},

        scripts = ['scripts/service-buddy'],
        packages = [
            'service_buddy_too',
            'service_buddy_too.ci',
            'service_buddy_too.codegenerator',
            'service_buddy_too.commands',
            'service_buddy_too.commands.bootstrap',
            'service_buddy_too.commands.clone',
            'service_buddy_too.commands.git',
            'service_buddy_too.commands.initialize',
            'service_buddy_too.commands.list',
            'service_buddy_too.context',
            'service_buddy_too.service',
            'service_buddy_too.util',
            'service_buddy_too.vcs'
        ],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {
            'service_buddy_too': ['codegenerator/builtin-code-templates.json']
        },
        install_requires = [
            'PyGithub',
            'cookiecutter',
            'pybitbucket',
            'click',
            'infra_buddy',
            'requests'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
