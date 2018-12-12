"""
This file contains tests covering backend.experiment_uploader.ExperimentUploader class
All unnecessary function and http calls are mocked
"""
import json
import unittest

from mock import MagicMock, patch

from padre.backend.experiment_uploader import ExperimentUploader
from padre.backend.http import PadreHTTPClient


class TestCreateDataSet(unittest.TestCase):
    """Test experiment_uploader.ExperimentUploader.create_dataset

    All unnecessary function call and http calls are mocked
    """
    def setUp(self):
        """Initializing for create_dataset test.

        All non related function calls and http calls will be mocked for this purpose.
        """
        self.test_dataset_id = '2'
        self.test_dataset_data = {'name': 'test data', 'description': 'test description'}
        self.http_client = MagicMock()
        self.http_client.has_token = MagicMock(return_value=True)
        mocked_post_response = MagicMock()
        mocked_post_response.headers = {'Location': 'api/datasets/' + self.test_dataset_id}
        self.http_client.do_post = MagicMock(return_value=mocked_post_response)

    @patch('padre.backend.experiment_uploader.ExperimentUploader.get_id_by_name')
    @patch('padre.backend.experiment_uploader.ExperimentUploader.create_project')
    def test_create_dataset_01(self, mock_project, mock_get_id):
        """Test ExperimentUploader.create_dataset function.

        Scenario: Correct id is set for data set.
        """
        mock_get_id.return_value = None
        obj = ExperimentUploader(self.http_client)
        mock_project.return_value = True
        response = obj.create_dataset(self.test_dataset_data)
        self.assertEqual(self.test_dataset_id,
                         response,
                         'Data set not created successfully')

    @patch('padre.backend.experiment_uploader.ExperimentUploader.get_id_by_name')
    @patch('padre.backend.experiment_uploader.ExperimentUploader.create_project')
    def test_create_dataset_02(self, mock_project, mock_get_id):
        """Test ExperimentUploader.create_dataset function.

        Scenario: do_post called with correct args.
        """
        mock_get_id.return_value = None
        obj = ExperimentUploader(self.http_client)
        mock_project.return_value = True
        obj.create_dataset(self.test_dataset_data)
        self.assertEqual(self.test_dataset_data,
                         json.loads(self.http_client.do_post.call_args_list[0][1]['data']),
                         'Do post not called with expected data for create_dataset')

    def tearDown(self):
        pass


class TestPutExperiment(unittest.TestCase):
    """Test experiment_uploader.ExperimentUploader.put_experiment

    All unnecessary function calls and http calls are mocked
    """

    def setUp(self):
        """Initializing for put_experiment test.

        All non related function calls and http calls will be mocked for this purpose.
        """
        self.test_experiment_url = 'api/experiments/' + '3'
        self.http_client = MagicMock()
        self.http_client.user = 'test user'
        self.http_client.has_token = MagicMock(return_value=True)

        mocked_post_project = MagicMock()
        mocked_post_project.headers = {'Location': 'api/projects/' + '1'}
        mocked_post_dataset = MagicMock()
        mocked_post_dataset.headers = {'Location': 'api/datasets/' + '2'}
        mocked_post_experiment = MagicMock()
        mocked_post_experiment.headers = {'Location': self.test_experiment_url}

        self.http_client.do_post = MagicMock()
        self.http_client.do_post.side_effect = [
            mocked_post_project,
            mocked_post_dataset,
            mocked_post_experiment]

    @patch('padre.backend.experiment_uploader.ExperimentUploader.get_id_by_name')
    def test_put_experiment(self, mock_get_id):
        """Test ExperimentUploader.put_experiment function.

        Scenario: Put experiment should return url of newly created experiment.
        """
        mock_get_id.return_value = None
        obj = ExperimentUploader(self.http_client)
        ex = MagicMock()
        ex.dataset = MagicMock()
        ex.dataset.metadata = {'name': 'test name'}
        ex.metadata = {'name': 'test experiment', 'description': 'test description'}
        ex.hyperparameters = MagicMock(return_value=
                                       {'param1':
                                            {'hyper_parameters': {'model_parameters': {'First Type': 'Type name'}}}
                                        })

        result = obj.put_experiment(ex)
        self.assertEqual(self.test_experiment_url,
                         result,
                         'Put experiment does not return url of newly created experiment')

    def tearDown(self):
        pass


class TestDeleteExperiment(unittest.TestCase):
    """Test experiment_uploader.ExperimentUploader.delete_experiment

    All unnecessary function calls and http calls are mocked
    """

    @patch('padre.backend.http.PadreHTTPClient.get_access_token')
    def setUp(self, mock_token):
        """Initializing for delete_experiment test.

        All non related function calls and http calls will be mocked for this purpose.
        """
        mock_token.return_value = None
        self.test_experiment_id = '3'
        self.http_client = PadreHTTPClient(user='test', passwd='test')
        self.http_client.has_token = MagicMock(return_value=True)
        self.http_client.do_delete = MagicMock()

    @patch('padre.backend.experiment_uploader.ExperimentUploader.get_id_by_name')
    @patch('padre.backend.experiment_uploader.ExperimentUploader.create_project')
    def test_delete_experiment(self, mock_project, mock_get_id):
        """Test ExperimentUploader.delete_experiment function.

        Scenario: do_delete should be called with correct experiment url.
        """
        mock_get_id.return_value = None
        obj = ExperimentUploader(self.http_client)
        obj.delete_experiment(self.test_experiment_id)
        delete_url = self.http_client.base + 'experiments/' + self.test_experiment_id + '/'

        self.assertEqual(delete_url,
                         self.http_client.do_delete.call_args_list[0][0][0],
                         'Delete experiment not calling do delete with correct url')

    def tearDown(self):
        pass


class TestGetIdByName(unittest.TestCase):
    """Test experiment_uploader.ExperimentUploader.get_id_by_name

    All unnecessary function calls and http calls are mocked
    """

    @patch('padre.backend.experiment_uploader.ExperimentUploader.get_id_by_name')
    @patch('padre.backend.experiment_uploader.ExperimentUploader.create_project')
    @patch('padre.backend.http.PadreHTTPClient.get_access_token')
    def setUp(self, mock_token, mock_create_project, mock_get_id):
        """Initializing http client and other attributes for test.

        All non related function calls and http calls will be mocked for this purpose.
        """
        mock_token.return_value = None
        mock_create_project.return_value = None
        mock_get_id.return_value = None
        self.test_experiment_id = '3'
        self.http_client = PadreHTTPClient(user='test', passwd='test')
        self.http_client.has_token = MagicMock(return_value=True)
        get_mock = MagicMock()
        self.entity = "datasets"
        self.test_value = "1"
        data = {"_embedded": {self.entity: [{"uid": self.test_value}]}}
        get_mock.content = json.dumps(data)
        self.http_client.do_get = MagicMock(return_value=get_mock)

        self.http_client.do_get.content = json.dumps(data)
        self.obj = ExperimentUploader(self.http_client)

    def test_get_id_by_name(self):
        """Test ExperimentUploader.get_id_by_name function.

        Scenario: Expected value returned, do_get called with expected arg
        """

        response = self.obj.get_id_by_name("test", "/" + self.entity)
        self.assertIn(self.entity + "?name=test",
                      self.http_client.do_get.call_args[0][0],
                      "do_get not called with expected arg")
        self.assertEqual(self.test_value,
                         response,
                         'Expected result not matches from get_id_by_name')

    def tearDown(self):
        pass
