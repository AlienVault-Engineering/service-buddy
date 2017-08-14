from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("exec")
use_plugin("python.unittest")
use_plugin("python.pycharm")
default_task = "publish"

@init
def initialize(project):
    build_number = project.get_property("bamboo_build")
    if build_number is not None and "" != build_number:
        project.version = build_number
    else:
        project.version = "0.0.999"
    #Project Manifest
    project.summary = "{{cookiecutter.project_name}}"
    project.home_page = "{cookiecutter.repository_url}}"
    project.description = "{{cookiecutter.description}}"
    project.author = "{{cookiecutter.owner}}"
    project.url = "{{cookiecutter.repository_url}}"
    project.build_depends_on_requirements("src/unittest/python/test_requirements.txt")
    project.set_property("run_unit_tests_propagate_stdout",True)
    project.set_property("run_unit_tests_propagate_stderr",True)