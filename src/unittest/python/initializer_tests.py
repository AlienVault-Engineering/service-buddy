import os

import testcase_parent
from service import loader
from service.initializer import Initializer
from service.service import Service
from vcs.vcs import VCS
from testcase_parent import ParentTestCase


class InitTestCase(ParentTestCase):
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super(InitTestCase, cls).setUpClass()
        cls.vcs = VCS(cls.service_directory, True)

    def validate_service_generation(self, definition):
        base_path = os.path.join(self.temp_dir, definition.get_app(), definition.get_fully_qualified_service_name())
        self.assertTrue(os.path.exists(os.path.join(base_path, "service/README.md")), "Did not find readme file")
        self.assertTrue(os.path.exists(os.path.join(base_path, "service/service.json")), "Did not find service file")

    def validate_generation(self, definition):
        # type: (Service) -> None
        base_path = os.path.join(self.temp_dir, definition.get_app(), definition.get_fully_qualified_service_name())
        if "exists" in definition.get_fully_qualified_service_name():
            self.assertFalse(os.path.exists(base_path), "Found code that should not exist - {}".format(base_path))
            return
        self.assertTrue(os.path.exists(base_path),
                        "Did not find generated code base - {}".format(definition.get_fully_qualified_service_name()))
        self.assertTrue(os.path.exists(os.path.join(base_path, "src")),
                        "Did not find generated code directory '{}/src' - {}".format(
                            base_path,
                            definition.get_fully_qualified_service_name()))
        self.assertTrue(os.path.exists(os.path.join(base_path, "build.py")), "Did not find generated build file")

    def test_project_init(self):
        application_map = loader.load_service_definitions(self.service_directory)
        init = Initializer(self.vcs, self.temp_dir, True, self.service_templates_test)
        init.code_generator.get_default_code_creator().dry_run = False
        init.initialize_services(application_map)
        loader.walk_service_map(application_map, application_callback=None, service_callback=self.validate_generation)

    def test_service_definition_generation(self):
        service_directory = os.path.join(testcase_parent.DIRNAME, '../resources/initializer_test')
        application_map = loader.load_service_definitions(service_directory)
        init = Initializer(self.vcs, self.temp_dir, True, self.service_templates_test)
        init.code_generator.get_default_code_creator().dry_run = False
        init.initialize_services(application_map)
        loader.walk_service_map(application_map, application_callback=None,
                                service_callback=self.validate_service_generation)
