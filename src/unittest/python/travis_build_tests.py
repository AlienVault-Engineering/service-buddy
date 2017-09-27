import os
from tempfile import mkdtemp

import shutil

from service_buddy.ci.ci import BuildCreator
from service_buddy.ci.travis_build_creator import TravisBuildCreator
from service_buddy.service import loader
from service_buddy.service.service import Service
from service_buddy.util import pretty_printer
from testcase_parent import ParentTestCase

DIRNAME = os.path.dirname(os.path.abspath(__file__))


class TravisBuildTestCase(ParentTestCase):
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super(TravisBuildTestCase, cls).setUpClass()
        cls.test_resources = os.path.join(DIRNAME, '../resources/travis_build_test')
        cls.yml_folder = os.path.join(cls.test_resources,"app1","service")

    def test_travis_file_detection(self):
        build_creator = BuildCreator(dry_run=True,template_directory=self.test_resources)
        test_service = Service(app="app1", role="service",definition={"service-type":"test"})
        build_creator.create_project(service_definition=test_service,service_dir=self.yml_folder)
        temp = mkdtemp()
        build_creator.create_project(service_definition=test_service,service_dir=temp)

    def test_yml_update(self):
        temp = mkdtemp()
        source = os.path.join(self.yml_folder, '.travis.yml')
        destination = os.path.join(temp, '.travis.yml')
        shutil.copy(source,destination)
        build_creator = BuildCreator(dry_run=True,template_directory=self.test_resources)
        build_creator._get_default_build_creator()._write_deploy_stanza(temp)
        with open(destination) as desty:
            readlines = desty.readlines()
            self.assertTrue("deploy\n"in readlines,"Could not find stanza")
