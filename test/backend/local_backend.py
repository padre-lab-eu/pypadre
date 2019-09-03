import os
import unittest

from pypadre.app import PadreConfig
from pypadre.app.padre_app import PadreFactory
from pypadre.backend.local.file.project.experiment.execution.execution_file_backend import PadreExecutionFileBackend
from pypadre.backend.local.file.project.experiment.execution.run.run_file_backend import PadreRunFileBackend
from pypadre.backend.local.file.project.experiment.execution.run.split.split_file_backend import PadreSplitFileBackend
from pypadre.backend.local.file.project.experiment.experiment_file_backend import PadreExperimentFileBackend
from pypadre.backend.local.file.project.project_file_backend import PadreProjectFileBackend


class LocalBackends(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(LocalBackends, self).__init__(*args, **kwargs)
        config = PadreConfig(config_file=os.path.join(os.path.expanduser("~"), ".padre-test.cfg"))
        config.set("backends", str([
                    {
                        "root_dir": os.path.join(os.path.expanduser("~"), ".pypadre-test")
                    }
                ]))
        self.app = PadreFactory.get(config)

    def tearDown(self):
        pass
        # delete data content

    def __del__(self):
        pass
        # delete configuration

    def test_dataset(self):
        # TODO test putting, fetching, searching, folder/git structure, deletion, git functionality?

        # Puts all the datasets
        self.app.datasets.load_defaults()

        # Gets a dataset by name
        id = 'Boston House Prices dataset'
        datasets = self.app.datasets.list({'name':id})
        for dataset in datasets:
            assert id in dataset.name

    def test_project(self):
        from pypadre.core.model.project import Project

        project = Project(name='Test Project', description='Testing the functionalities of project backend')

        self.app.projects.put(project)
        name = 'Test Project'
        projects = self.app.projects.list({'name': name})
        for project in projects:
            assert name in project.name

    def test_experiment(self):
        # TODO test putting, fetching, searching, folder/git structure, deletion, git functionality?

        from pypadre.core.model.experiment import Experiment
        from pypadre.core.model.project import Project

        project = Project(name='Test Project 2', description='Testing the functionalities of project backend')

        def create_test_pipeline():
            from sklearn.pipeline import Pipeline
            from sklearn.svm import SVC
            # estimators = [('reduce_dim', PCA()), ('clf', SVC())]
            estimators = [('SVC', SVC(probability=True))]
            return Pipeline(estimators)

        id = 'Boston House Prices dataset'
        dataset = self.app.datasets.list({'name': id})

        experiment = Experiment(name="Test Experiment SVM",
                    description="Testing Support Vector Machines via SKLearn Pipeline",
                    dataset=dataset[0],
                    workflow=create_test_pipeline(), keep_splits=True, strategy="random", project=project)

        self.app.experiments.put(experiment)
        name = 'Test Experiment SVM'
        experiments = self.app.experiments.list({'name': name})
        for experiment in experiments:
            assert name in experiment.name

    def test_execution(self):

        from pypadre.core.model.project import Project
        from pypadre.core.model.experiment import Experiment
        from pypadre.core.model.execution import Execution

        project = Project(name='Test Project 2', description='Testing the functionalities of project backend')

        def create_test_pipeline():
            from sklearn.pipeline import Pipeline
            from sklearn.svm import SVC
            # estimators = [('reduce_dim', PCA()), ('clf', SVC())]
            estimators = [('SVC', SVC(probability=True))]
            return Pipeline(estimators)

        id = 'Boston House Prices dataset'
        dataset = self.app.datasets.list({'name': id})

        experiment = Experiment(name="Test Experiment SVM",
                                description="Testing Support Vector Machines via SKLearn Pipeline",
                                dataset=dataset[0],
                                workflow=create_test_pipeline(), keep_splits=True, strategy="random", project=project)

        execution = Execution(experiment, codehash='abdauoasg45qyh34t', command=None, append_runs=True, parameters=None,
                              preparameters=None, single_run=True,
                              single_transformation=True)
        self.app.executions.put(execution)



    def test_run(self):
        """
        project_backend: PadreProjectFileBackend = self.backend.project
        experiment_backend: PadreExperimentFileBackend = project_backend.experiment
        execution_backend: PadreExecutionFileBackend = experiment_backend.execution
        run_backend: PadreRunFileBackend = execution_backend.run
        """

        from pypadre.core.model.experiment import Experiment
        from pypadre.core.model.project import Project

        project = Project(name='Test Project 2', description='Testing the functionalities of project backend')

        def create_test_pipeline():
            from sklearn.pipeline import Pipeline
            from sklearn.svm import SVC
            # estimators = [('reduce_dim', PCA()), ('clf', SVC())]
            estimators = [('SVC', SVC(probability=True))]
            return Pipeline(estimators)

        id = 'Iris Plants Database'
        dataset = self.app.datasets.list({'name': id})
        workflow = create_test_pipeline()
        experiment = Experiment(name="Test Experiment SVM",
                                description="Testing Support Vector Machines via SKLearn Pipeline",
                                dataset=dataset[0],
                                workflow=workflow, keep_splits=True, strategy="random", project=project)

        self.app.experiments.put(experiment)
        experiment.execute()

    def test_split(self):
        project_backend: PadreProjectFileBackend = self.backend.project
        experiment_backend: PadreExperimentFileBackend = project_backend.experiment
        execution_backend: PadreExecutionFileBackend = experiment_backend.execution
        run_backend: PadreRunFileBackend = execution_backend.run
        split_backend: PadreSplitFileBackend = run_backend.split
        # TODO


if __name__ == '__main__':
    unittest.main()
