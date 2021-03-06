import configparser
import os
import shutil
import unittest

from pypadre._package import PACKAGE_ID
from pypadre.core.model.code.code_mixin import PythonPackage
from pypadre.core.util.utils import find_package_structure
from pypadre.pod.app import PadreConfig
from pypadre.pod.app.padre_app import PadreAppFactory
from pypadre.pod.tests.util.util import connect_log_to_stdout, connect_event_to_stdout


class PadreAppTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        connect_log_to_stdout()
        connect_event_to_stdout()

        cls.config_path = os.path.join(os.path.expanduser("~"), ".padre-test.cfg")
        cls.workspace_path = os.path.join(os.path.expanduser("~"), ".pypadre-test")

        """Create config file for testing purpose"""
        config = configparser.ConfigParser()
        # test_data = {'test_key': 'value 1', 'key2': 'value 2'}
        # cls.config['TEST'] = test_data
        with open(cls.config_path, 'w+') as configfile:
            config.write(configfile)

        config = PadreConfig(config_file=cls.config_path)
        config.set("backends", str([
            {
                "root_dir": cls.workspace_path
            }
        ]))
        cls.app = PadreAppFactory.get(config)

    def create_experiment(self, *args, **kwargs):
        return self.app.experiments.create(*args, **kwargs, reference=self.test_reference)

    def create_project(self, *args, **kwargs):
        return self.app.projects.create(*args, **kwargs, reference=self.test_reference)

    def create_execution(self, *args, **kwargs):
        return self.app.executions.service.create(*args, **kwargs, reference=self.test_reference)

    def create_run(self, *args, **kwargs):
        return self.app.runs.service.create(*args, **kwargs, reference=self.test_reference)

    def create_split(self, *args, **kwargs):
        return self.app.splits.service.create(*args, **kwargs, reference=self.test_reference)

    def setUp(self):
        # clean up if last teardown wasn't called correctly
        self.tearDown()

    def setup_reference(self, file):
        # TODO can we move that to setup in some way??? reference to (__file__)
        self.test_reference = PythonPackage(package=find_package_structure(file),
                                            variable=self._testMethodName, repository_identifier=PACKAGE_ID)

    def tearDown(self):
        self.test_reference = None
        # delete data content
        try:
            if os.path.exists(os.path.join(self.workspace_path, "datasets")):
                shutil.rmtree(self.workspace_path + "/datasets")
            if os.path.exists(os.path.join(self.workspace_path, "projects")):
                shutil.rmtree(self.workspace_path + "/projects")
            if os.path.exists(os.path.join(self.workspace_path, "code")):
                shutil.rmtree(self.workspace_path + "/code")
        except FileNotFoundError:
            pass

    # noinspection PyUnresolvedReferences
    @classmethod
    def tearDownClass(cls):
        """Remove config file after test"""
        if os.path.isdir(cls.workspace_path):
            shutil.rmtree(cls.workspace_path)
        os.remove(cls.config_path)
