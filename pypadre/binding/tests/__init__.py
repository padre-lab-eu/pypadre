import os
import re
import unittest

from click.testing import CliRunner

from pypadre.app import PadreConfig
from pypadre.cli.pypadre import pypadre
from pypadre.core.model.project import Project
from pypadre.core.validation.validation import ValidateableFactory, ValidationErrorHandler


class PadreCli(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(PadreCli, self).__init__(*args, **kwargs)
        config = PadreConfig(config_file=os.path.join(os.path.expanduser("~"), ".padre-test.cfg"))
        config.set("backends", str([
                    {
                        "root_dir": os.path.join(os.path.expanduser("~"), ".pypadre-test")
                    }
                ]))

    def tearDown(self):
        pass
        # delete data content

    def __del__(self):
        pass
        # delete configuration

    def test_dataset(self):
        runner = CliRunner()

        runner.invoke(pypadre, ['--config-file', os.path.join(os.path.expanduser("~"), ".padre-test.cfg")])
        result = runner.invoke(pypadre, ['--config-file', os.path.join(os.path.expanduser("~"), ".padre-test.cfg"),
                                         'dataset', 'load', '-d'])
        assert result.exit_code == 0
        result = runner.invoke(pypadre, ['--config-file', os.path.join(os.path.expanduser("~"), ".padre-test.cfg"),
                                         'dataset', 'list'])
        assert 'Boston' in result.output

        result = runner.invoke(pypadre, ['--config-file', os.path.join(os.path.expanduser("~"), ".padre-test.cfg"),
                                         'dataset', 'get',
                                         re.search('([a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+)',
                                                   result.output).group(0)])
        assert 'Diabetes' in result.output

    def test_project(self):
        def handle_missing(obj, e):
            return "a"

        p = ValidateableFactory.make(Project, handlers=[
            ValidationErrorHandler(validator="required", handle=handle_missing)])

        runner = CliRunner()

        runner.invoke(pypadre, ['--config-file', os.path.join(os.path.expanduser("~"), ".padre-test.cfg")])
        result = runner.invoke(pypadre, ['--config-file', os.path.join(os.path.expanduser("~"), ".padre-test.cfg"),
                                         'project', 'create'])

        assert 'Diabetes' in result.output

if __name__ == '__main__':
    unittest.main()
