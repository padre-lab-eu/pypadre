"""
Logic to upload experiment data to server goes here
"""
import json


class ExperimentUploader:
    """Experiment uploader to upload data to server"""
    def __init__(self, http_client, project_name="Test project"):
        """
        This initializes the Uploader class for given experiment.
        """
        self._http_client = http_client
        self.dataset_id = None
        self.experiment_id = None
        self.project_id = None
        self.create_project(project_name)

    def create_dataset(self, data):
        """Create data set"""
        url = self._http_client.base + self._http_client.paths["datasets"]
        if isinstance(data, dict):
            data = json.dumps(data)
        if self._http_client.has_token():
            response = self._http_client.do_post(url, **{"data": data})
            self.dataset_id = response.headers['Location'].split('/')[-1]

    def create_project(self, name="Test Project"):
        """Create project on server"""
        url = self._http_client.base + self._http_client.paths["projects"]
        data = {"name": name, "owner": self._http_client.user}
        if self._http_client.has_token():
            response = self._http_client.do_post(url, **{"data": json.dumps(data)})
            self.project_id = response.headers['Location'].split('/')[-1]

    def create_experiment(self, data):
        """Create experiment on server"""
        url = self._http_client.base + self._http_client.paths["experiments"]
        location = ''
        if isinstance(data, dict):
            data = json.dumps(data)
        if self._http_client.has_token():
            response = self._http_client.do_post(url, **{"data": data})
            self.experiment_id = response.headers['Location'].split('/')[-1]
            location = response.headers['Location']
        return location

    def put_experiment(self, experiment):
        """
        Upload experiment to server
        :param experiment: Experiment instance
        :type experiment: <class 'padre.experiment.Experiment'>
        :return: None
        """
        dataset_dict = experiment.dataset.metadata
        self.create_dataset(dataset_dict)

        experiment_data = experiment.metadata
        experiment_data["projectId"] = self.project_id
        experiment_data["datasetId"] = self.dataset_id
        experiment_data["pipeline"] = {"components": [
            {"description": "",
             "hyperparameters": [experiment.hyperparameters()]}
        ]}

        return self.create_experiment(experiment_data)

    def delete_experiment(self, ex):
        """
        Delete experiment from the server.

        :param ex: Id of the experiment or name of the experiment
        :type ex: str

        # todo: Implement delete by experiment name
        """
        if ex.isdigit() and self._http_client.has_token():
            url = self._http_client.base + self._http_client.paths['experiment'](ex)
            return self._http_client.do_delete(url, **{})

    def get_experiment(self, ex):
        """
        Downloads the experiment given by ex, where ex is a string with the id or url of the
        experiment. The experiment is downloaded from the server and stored in the local file store
        if the server version is newer than the local version or no local version exists.
        The function returns an experiment class, which is loaded from file.

        :param ex: Id or url of the experiment
        :return:
        # todo: Return experiment instance according to above documentation
        """
        if self._http_client.has_token():
            if not ex.isdigit():  # url of the experiment
                url = self._http_client.base + ex
            else:
                url = self._http_client.base + self._http_client.paths['experiment'](ex)
            response = json.loads(self._http_client.do_get(url, **{}).content)

            return response
        return False





